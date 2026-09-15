# Worked Examples — Web SPAs (React, Solid, Svelte)

Interfaces in web SPAs are mostly unchecked at compile time, so they fail at
runtime. Every consumer reads a hook's return type, a component's prop
contract, and a store slice's methods. Getting them wrong costs the same as a
bad backend API. A public API breaks callers in other companies, while a
mistake in these interfaces affects only your own team.

The examples below run the comment test on the contracts you change most often.

---

## Example 1 — Hook return type: positional tuple against typed result

This pattern appears often in React codebases:

```tsx
function useProduct(id: string): [Product | null, Error | null, boolean, () => Promise<void>, (p: Product) => Promise<void>] {
  // ...
}

// caller:
const [product, error, loading, refetch, mutate] = useProduct(id);
```

Here is the full interface comment:

> Returns a 5-tuple. Position 0 is the loaded product, or null when loading
> or after a failed fetch. Position 1 is the last error, or null. Position 2
> is true from mount through the first response. Position 3 is a refetch
> function that returns a promise resolving after the fresh response.
> Position 4 is a mutation function that optimistically updates the local
> value and rolls back on server rejection. Callers should treat position 1
> being non-null and position 0 being non-null as a stale-data state, where
> the previous value is still displayed.

That comment is six sentences. It describes the data structure (positions
0-4) and the ordering (which is non-null when). It is hard to read and
impossible to use correctly from the destructuring site. The reason is that the names
`product`, `error`, `loading`, `refetch`, `mutate` are the caller's choice,
and the contract does not include them. Two callers can read the positions
differently.

The failure is that the contract leaks positional layout the caller must memorize.
The discriminator state (loaded? failed? stale?) is also encoded in null
combinations the caller has to decode.

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

Here is the interface comment now:

> Returns the current query state for the product with this id. The status
> discriminator has one value for each of the four legal combinations (loading, success, error,
> stale). refetch triggers a fresh load. mutate updates locally and reconciles
> with the server.

The comment has four sentences and mentions no positions. The discriminator removes the "what does null
mean here" question from every caller. A discriminated union expresses the
contract in the type system, so the caller no longer needs to remember
invariants.

Solid and Svelte versions work the same way (signals or stores wrapping the
discriminator).

---

## Example 2 — Component prop contract: design-it-twice on a Dialog

The task is a `Dialog` component used in form confirmations, destructive-action
warnings, and informational alerts.

**Candidate A is one big component:**

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

Here is the complete interface comment:

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

The comment has seven sentences, references internal behavior ("controls the
icon color"), and prescribes call order ("pass 'primary' for confirmations").
The component has eleven props, so the caller makes eleven decisions for what
is conceptually one action.

The failure is that one component bundles three distinct intents (confirm,
destructive-confirm, info). It exposes the differences between them as
prop combinations the caller must assemble correctly each time.

**Candidate B puts three named intents over one core:**

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
> onConfirm if the user proceeds. Calls onClose in all other paths
> (cancel, esc, overlay click). Focus defaults to the cancel button.
> esc and overlay-click are enabled and treated as cancel.

The comment has three sentences and lists no prop combinations to memorize. The destructive-confirm
intent defines the safe defaults (focus on cancel, confirm button styled red), so
callers can't accidentally produce an unsafe variant. Common-case caller
burden drops from eleven decisions to four.

Each named dialog composes one deep core internally. The presets are
thin in caller-facing code (a few decisions) and add value by encoding
the intent's invariants.

The dialog redesign follows the same design-it-twice pattern as the `UserCard` case in
`examples.md`. The mistake to avoid is treating "named intents over a core"
as automatic. Only do it when the call sites are three distinct
intents. Three sets of prop combinations that happen to recur do not qualify.

---

## Example 3 — Store slice interface: setState exposed vs intent methods

This Zustand slice was extended without a design:

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

The comment is long because the "interface" is `setX` for each field. The
real operations the cart supports (add an item, apply a coupon, pick
shipping) have invariants the store does not enforce, so every caller now has to enforce
those invariants. The store's interface and its implementation have the
same names, which makes it the canonical shallow module.

The failure is that the slice exposes the state layout and leaves the
operations, and the invariants they need, to callers.

Redesign so the interface expresses intent and the slice enforces invariants:

```tsx
interface CartStore {
  // State fields are read-only
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

> Stores the cart. items, coupon, shipping, and total hold the current
> state. The mutation methods enforce invariants (no duplicate variants,
> qty >= 1, coupon valid for the current items) and recompute total. Errors
> from applyCoupon are returned as Result. The cart state is unchanged on
> failure.

The comment has three sentences and never says "callers must". The invariants
are in one place, where they can be tested once. The store is now deep. The interface has
six operations that express intent. The implementation handles dedup,
validation, total computation, coupon validity, async network calls during
`applyCoupon`, and rollback semantics.

Solid (`createStore`) and Svelte (`writable` + module) get the same treatment,
because the intent-method interface works the same way in any framework.

---

## Example 4 — Headless behavior: defining the hook's interface

A team is building their own combobox. They start by drafting the hook:

**Candidate A exposes the implementation:**

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

The failure is that the hook exposes internal state-management decisions as
caller obligations. "Callers must" is in the comment four times. Every
combobox usage now reimplements the same sequence of useState calls.

**In Candidate B, the hook handles the state machine:**

```tsx
function useCombobox<T>(opts: {
  items: T[];                                  // items is the current item set
  getId: (item: T) => string;
  filter?: (item: T, query: string) => boolean;  // default: substring match on getLabel
  getLabel?: (item: T) => string;                // default: String(item)
  onSelect?: (item: T) => void;
}): {
  // These are ARIA-correct prop bundles
  rootProps: HTMLAttributes<HTMLDivElement>;
  inputProps: InputHTMLAttributes<HTMLInputElement>;
  listProps: HTMLAttributes<HTMLUListElement>;
  itemProps(index: number): LiHTMLAttributes<HTMLLIElement>;

  // This state is observable for rendering
  isOpen: boolean;
  filteredItems: T[];
  highlightedIndex: number;
  selectedItem: T | null;

  // These are imperative controls
  open(): void; close(): void; reset(): void;
} { ... }
```

Comment:

> Implements a headless combobox state machine. Pass the current items and an id
> function. Receive prop bundles that wire ARIA attributes and keyboard
> handlers to the input, list, and items. filteredItems is computed from the current
> input value through filter. highlightedIndex tracks keyboard navigation.
> onSelect fires when the user confirms a choice via Enter or click.

The comment has four sentences. The caller spreads the prop bundles onto
their elements and renders against `filteredItems`. Keyboard, ARIA,
open/close, filter, and focus management are all internal. The comment never
says "callers must", because the hook holds the state and exposes it read-only
for rendering.

Candidate B is much deeper. The implementation has a few hundred
lines (handling Tab vs Enter, IME composition events, screen
reader announcements, Home/End navigation, and so on). The caller's interface comment omits all of that
complexity.

---

## Cheat sheet — passing the comment test in web idioms

| If your interface forces the caller to... | The redesign is usually... |
|---|---|
| Destructure a positional tuple and remember what each position means | A typed object or discriminated union as the return type |
| Combine 8+ props to express a single intent | Named preset components over a deep core |
| Call `setX` after computing what `X` should be | A method that takes the operation and computes the new state internally |
| Maintain state and pass it back into a hook every render | The hook holds the state, and the caller reads it for rendering |
| Wrap effect-based logic the same way in every component | A custom hook/composable/rune for that effect |
| Pass children-via-props with rigid slots | `children` plus a small subcomponent API (compound components) |

When the comment has to describe what the caller will do with the return
values, the interface is too low-level. The module should do more of the
work.
