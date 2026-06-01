# Worked Examples — Web SPAs (React, Solid, Svelte)

Interfaces in web SPAs are mostly invisible at compile time and brutal at
runtime. A hook's return shape, a component's prop contract, and a store
slice's method surface are read by every consumer; getting them wrong costs
the same as a bad backend API, just distributed across the team rather than
across organizations.

These examples walk the comment test on the shapes you'll touch most.

---

## Example 1 — Hook return shape: positional tuple vs typed result

A pattern that grows in React codebases:

```tsx
function useProduct(id: string): [Product | null, Error | null, boolean, () => Promise<void>, (p: Product) => Promise<void>] {
  // ...
}

// caller:
const [product, error, loading, refetch, mutate] = useProduct(id);
```

The interface comment, written truthfully:

> Returns a 5-tuple. Position 0 is the loaded product, or null when loading
> or after a failed fetch. Position 1 is the last error, or null. Position 2
> is true from mount through the first response. Position 3 is a refetch
> function that returns a promise resolving after the fresh response.
> Position 4 is a mutation function that optimistically updates the local
> value and rolls back on server rejection. Callers should treat position 1
> being non-null and position 0 being non-null as a stale-data state, where
> the previous value is still displayed.

That comment is six sentences. It describes the data structure (positions
0-4). It describes ordering (which is non-null when). It is hard to read and
impossible to use correctly from the destructuring site, because the names
`product`, `error`, `loading`, `refetch`, `mutate` are not part of the
contract — they are the caller's choice. Two callers will read the positions
differently.

Failure named: the contract leaks positional layout the caller must memorize,
and the discriminator state (loaded? failed? stale?) is encoded in null
combinations rather than expressed.

Redesign with a typed result:

```tsx
type ProductQuery =
  | { status: 'loading'; product: null; error: null }
  | { status: 'success'; product: Product; error: null }
  | { status: 'error'; product: null; error: Error }
  | { status: 'stale';  product: Product; error: Error };

function useProduct(id: string): ProductQuery & { refetch(): Promise<void>; mutate(p: Product): Promise<void> } {
  // ...
}

// caller:
const q = useProduct(id);
if (q.status === 'loading') return <Spinner />;
if (q.status === 'error')   return <Error err={q.error} />;
return <View product={q.product} />;
```

The interface comment now:

> Returns the current query state for the product with this id. The status
> discriminator names the four legal combinations (loading, success, error,
> stale). refetch triggers a fresh load; mutate updates locally and reconciles
> with the server.

Four sentences. No positions. The discriminator removes the "what does null
mean here" question from every caller. This is the same point as Check 3's
"narrow assertions" in testing — a discriminated union expresses the contract
in the type system; the caller no longer needs to remember invariants.

Solid and Svelte versions use the same shape (signals or stores wrapping the
discriminator).

---

## Example 2 — Component prop contract: design-it-twice on a Dialog

Task: a `Dialog` component used in form confirmations, destructive-action
warnings, and informational alerts.

**Candidate A — the one big component:**

```tsx
<Dialog
  isOpen={open}
  onClose={close}
  title="Delete account?"
  description="This cannot be undone."
  variant="destructive"
  primaryAction={{ label: 'Delete', onClick: doDelete, loading: deleting }}
  secondaryAction={{ label: 'Cancel', onClick: close }}
  icon={<Warning />}
  size="md"
  initialFocus="primary"
  closeOnEsc={true}
  closeOnOverlayClick={false}
/>
```

Interface comment, complete:

> Renders a modal dialog when isOpen is true. title and description appear at
> the top; primaryAction and secondaryAction render as buttons in the footer
> in that order. variant controls the icon color and primary button color
> (destructive=red, default=blue, success=green). If icon is provided it
> overrides variant's default. initialFocus determines which button receives
> focus when the dialog opens; pass 'primary' for confirmations and
> 'secondary' for destructive actions to prevent accidental confirmation.
> closeOnEsc and closeOnOverlayClick should both be false for destructive
> dialogs to prevent data loss. The dialog traps focus and restores it to
> the previously focused element on close.

Seven sentences, references internal behavior ("controls the icon color"),
prescribes call order ("pass 'primary' for confirmations"). Eleven props,
caller makes eleven decisions for what is conceptually one action.

Failure named: one component bundles three distinct intents (confirm,
destructive-confirm, info), and exposes the differences between them as
prop combinations the caller must assemble correctly each time.

**Candidate B — three named intents over one core:**

```tsx
<ConfirmDialog
  open={open} onClose={close}
  title="Save changes?"
  onConfirm={doSave}
/>

<DestructiveConfirmDialog
  open={open} onClose={close}
  title="Delete account?"
  body="This cannot be undone."
  confirmLabel="Delete"
  onConfirm={doDelete}
/>

<InfoDialog open={open} onClose={close} title="Heads up" body="..." />
```

Interface comment for `DestructiveConfirmDialog`:

> Renders a destructive-action confirmation when open is true. Calls
> onConfirm if the user proceeds; calls onClose in all other paths
> (cancel, esc, overlay click). Focus defaults to the cancel button;
> esc and overlay-click are enabled and treated as cancel.

Three sentences. No prop combinations to memorize. The destructive-confirm
intent owns the safe defaults (focus on cancel, confirm button styled red);
callers can't accidentally produce an unsafe variant. Common-case caller
burden drops from eleven decisions to four.

Each named dialog composes one deep core under the hood. The presets are
thin in caller-facing code (a few decisions) and add real value by encoding
the intent's invariants.

This is the same design-it-twice pattern as the `UserCard` case in
`examples.md`. The mistake to avoid is treating "named intents over a core"
as automatic — only do it when the call sites really are three distinct
intents, not three sets of prop combinations that happen to recur.

---

## Example 3 — Store slice interface: setState exposed vs intent methods

A Zustand slice that grew organically:

```tsx
interface CartStore {
  items: CartItem[];
  coupon: Coupon | null;
  shipping: ShippingOption | null;
  setItems(items: CartItem[]): void;
  setCoupon(coupon: Coupon | null): void;
  setShipping(shipping: ShippingOption | null): void;
  getState(): CartState;
}
```

Comment attempt:

> Holds the cart state. setItems replaces the items array; callers must
> compute the new array including duplicate handling (item with the same
> productId merges quantities; item with a different size variant does not
> merge). setCoupon replaces the coupon; callers must verify the coupon is
> valid for the current items before setting, or the displayed total will
> be wrong. setShipping replaces the shipping option; callers must compute
> the shipping cost before setting; the total is derived from items + coupon
> + shipping at read time.

The comment is long because the "interface" is `setX` for each field, but
the real operations the cart supports (add an item, apply a coupon, pick
shipping) carry invariants the store doesn't enforce. Every caller now owns
those invariants. The store's interface and its implementation have the
same shape: it is the canonical shallow module.

Failure named: the slice exposes the state shape, not the operations on it.
Invariants live in callers.

Redesign — interface expresses intent, slice enforces invariants:

```tsx
interface CartStore {
  // state, read-only
  readonly items: CartItem[];
  readonly coupon: Coupon | null;
  readonly shipping: ShippingOption | null;
  readonly total: Money;

  // operations
  add(item: CartItem): void;                              // dedupes by variant
  remove(itemId: string): void;
  changeQuantity(itemId: string, qty: number): void;      // validates qty >= 1
  applyCoupon(code: string): Promise<Result<void>>;       // validates against items
  pickShipping(option: ShippingOption): void;             // recomputes total
  clear(): void;
}
```

Comment:

> Owns the cart. items, coupon, shipping, and total reflect the current
> state. The mutation methods enforce invariants (no duplicate variants,
> qty >= 1, coupon valid for the current items) and recompute total. Errors
> from applyCoupon are returned as Result; the cart state is unchanged on
> failure.

Three sentences. No "callers must" anywhere. Invariants live in one place,
where they can be tested once. The store is now deep — the interface has
six operations expressing intent, but the implementation owns dedup,
validation, total computation, coupon validity, async network calls during
`applyCoupon`, and rollback semantics.

Same shape in Solid (`createStore`) and Svelte (`writable` + module). The
intent-method interface transcends the framework.

---

## Example 4 — Headless behavior: defining the hook's interface

A team is building their own combobox. They start by drafting the hook:

**Candidate A — exposes the implementation:**

```tsx
function useCombobox<T>(opts: {
  items: T[];
  isOpen: boolean;
  setIsOpen: (v: boolean) => void;
  highlightedIndex: number;
  setHighlightedIndex: (i: number) => void;
  inputValue: string;
  setInputValue: (v: string) => void;
  selectedItem: T | null;
  setSelectedItem: (item: T | null) => void;
  filter: (item: T, query: string) => boolean;
}) { ... }
```

Comment:

> Returns combobox state and handlers. Callers manage isOpen, highlightedIndex,
> inputValue, and selectedItem as React state and pass setters in. The hook
> wires keyboard events (Arrow keys move highlightedIndex; Enter selects;
> Esc closes; Tab closes and confirms). The hook does not own the state;
> callers must store and pass it back on every render.

Failure named: the hook exposes internal state-management decisions as
caller obligations. "Callers must" is in the comment four times. Every
combobox usage now reimplements the same useState dance.

**Candidate B — hook owns the state machine:**

```tsx
function useCombobox<T>(opts: {
  items: T[];                                  // current item set
  getId: (item: T) => string;
  filter?: (item: T, query: string) => boolean;  // default: substring match on getLabel
  getLabel?: (item: T) => string;                // default: String(item)
  onSelect?: (item: T) => void;
}): {
  // ARIA-correct prop bundles
  rootProps: HTMLAttributes<HTMLDivElement>;
  inputProps: InputHTMLAttributes<HTMLInputElement>;
  listProps: HTMLAttributes<HTMLUListElement>;
  itemProps(index: number): LIAttributes;

  // observable state for rendering
  isOpen: boolean;
  filteredItems: T[];
  highlightedIndex: number;
  selectedItem: T | null;

  // imperative controls
  open(): void; close(): void; reset(): void;
} { ... }
```

Comment:

> A headless combobox state machine. Pass the current items and an id
> function; receive prop bundles that wire ARIA attributes and keyboard
> handlers to the input, list, and items. filteredItems reflects the current
> input value through filter; highlightedIndex tracks keyboard navigation;
> onSelect fires when the user confirms a choice via Enter or click.

Four sentences. The caller spreads the prop bundles onto their elements and
renders against `filteredItems`. Keyboard, ARIA, open/close, filter, and
focus management are all internal. No "callers must" — the hook owns the
state and exposes it for rendering, not mutation.

The depth gain is substantial: the implementation runs to a few hundred
lines (intelligently handling Tab vs Enter, IME composition events, screen
reader announcements, Home/End navigation, etc.), and the caller pays for
none of that complexity in their interface comment.

---

## Cheat sheet — passing the comment test in web idioms

| If your interface forces the caller to... | The redesign is usually... |
|---|---|
| Destructure a positional tuple and remember what each position means | A typed object or discriminated union as the return type |
| Combine 8+ props to express a single intent | Named preset components over a deep core |
| Call `setX` after computing what `X` should be | A method that takes the operation, not the new state |
| Maintain state and pass it back into a hook every render | Hook owns the state; caller reads it for rendering |
| Wrap effect-based logic the same way in every component | A custom hook/composable/rune for that effect |
| Pass children-via-props with rigid slots | `children` plus a small subcomponent API (compound components) |

The pattern is consistent: when the comment has to describe what the caller
will do with the return values, the interface is too low-level — the module
should be doing more of the work.
