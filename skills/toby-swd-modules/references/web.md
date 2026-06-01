# Worked Examples — Web SPAs (React, Solid, Svelte)

The web SPA stack has its own pattern vocabulary: hooks (React), composables
and signals (Solid, Vue), runes and stores (Svelte). The framework names
differ; the module principles don't. These examples show the same checks
applied across the three with the idiom of each.

The existing `examples.md` covers two foundational web cases (prop drilling
and classitis). This file adds patterns specific to building real applications
in any of the three frameworks.

---

## Example 1 — Server state mixed into components

The pattern most apps grow into, in every framework:

```tsx
// React — fetch-in-component
function ProductPage({ id }: { id: string }) {
  const [product, setProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetch(`/api/products/${id}`)
      .then((r) => (r.ok ? r.json() : Promise.reject(r.statusText)))
      .then((p) => { if (!cancelled) setProduct(p); })
      .catch((e) => { if (!cancelled) setError(e); })
      .finally(() => { if (!cancelled) setLoading(false); });
    return () => { cancelled = true; };
  }, [id]);

  if (loading) return <Spinner />;
  if (error) return <ErrorState err={error} />;
  return <ProductView product={product!} />;
}
```

The exact same shape, repeated, in `OrderPage`, `CustomerPage`, `InvoicePage`.
Every component re-implements: cancellation on unmount, error semantics,
loading state, cache (there isn't one), refetch on focus (there isn't one
either), retry on transient failure (nope). The "interface to fetching" is a
30-line block of `useEffect` machinery duplicated everywhere.

This is information leakage (Check 2) in slow motion. The decisions "how do
we cancel," "what's the loading state shape," "what counts as an error" are
encoded in every component. The day you change one — say, you want errors to
include a `retry-after` hint — is the day you edit fifteen components.

The deep module is a query library — TanStack Query / SWR for React,
TanStack Query for Solid, TanStack Query or `@tanstack/svelte-query` for
Svelte (all three frameworks ship an integration). Use one:

```tsx
// React with TanStack Query
function ProductPage({ id }: { id: string }) {
  const { data: product, isLoading, error } = useQuery({
    queryKey: ['product', id],
    queryFn: () => api.products.get(id),
  });
  if (isLoading) return <Spinner />;
  if (error) return <ErrorState err={error} />;
  return <ProductView product={product!} />;
}
```

```tsx
// Solid with @tanstack/solid-query — same shape, different reactivity
function ProductPage(props: { id: string }) {
  const query = createQuery(() => ({
    queryKey: ['product', props.id],
    queryFn: () => api.products.get(props.id),
  }));
  return (
    <Switch>
      <Match when={query.isLoading}><Spinner /></Match>
      <Match when={query.error}><ErrorState err={query.error} /></Match>
      <Match when={query.data}><ProductView product={query.data!} /></Match>
    </Switch>
  );
}
```

```svelte
<!-- Svelte with @tanstack/svelte-query -->
<script lang="ts">
  import { createQuery } from '@tanstack/svelte-query';
  export let id: string;
  $: query = createQuery({ queryKey: ['product', id], queryFn: () => api.products.get(id) });
</script>

{#if $query.isLoading}
  <Spinner />
{:else if $query.error}
  <ErrorState err={$query.error} />
{:else}
  <ProductView product={$query.data} />
{/if}
```

Cancellation, deduping, retry, cache, refetch-on-focus, request waterfalls
across components — all owned inside one library that's deep by design. The
component is back to rendering. When the team later decides every error
deserves a toast, that's one configuration change in one place, not a
patch across the codebase.

Build your own only if you have a reason. "We don't want a dependency" loses
on cost-benefit by the third component.

---

## Example 2 — Shared behavior via hook / composable / rune

A pattern from the bad old days, still appearing in new code:

```tsx
// React — higher-order component for "needs window size"
function withWindowSize<P>(Component: React.ComponentType<P & WindowSize>) {
  return class extends React.Component<P, WindowSize> {
    state = { width: window.innerWidth, height: window.innerHeight };
    handleResize = () => this.setState({ width: window.innerWidth, height: window.innerHeight });
    componentDidMount() { window.addEventListener('resize', this.handleResize); }
    componentWillUnmount() { window.removeEventListener('resize', this.handleResize); }
    render() { return <Component {...this.props} {...this.state} />; }
  };
}

// then everywhere:
export default withWindowSize(withCurrentUser(withTheme(MyComponent)));
```

This is Check 5 in non-class clothing. `withWindowSize` and `MyComponent` are
in a parent-child relationship where the wrapper invisibly injects props,
overrides nothing visible, and yet `MyComponent` cannot be understood without
reading the wrapper. Three wrappers deep ("wrapper hell") and the component's
real interface is unknowable from its file.

The composition replacement looks nearly identical across the three
frameworks. The thing being shared is a small piece of logic, packaged as
a function the consumer calls.

```tsx
// React — useWindowSize hook
function useWindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });
  useEffect(() => {
    const onResize = () => setSize({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return size;
}

// in any component:
function MyComponent() {
  const { width, height } = useWindowSize();
  // ...
}
```

```tsx
// Solid — composable returning signals
function createWindowSize() {
  const [width, setWidth] = createSignal(window.innerWidth);
  const [height, setHeight] = createSignal(window.innerHeight);
  const onResize = () => { setWidth(window.innerWidth); setHeight(window.innerHeight); };
  onMount(() => window.addEventListener('resize', onResize));
  onCleanup(() => window.removeEventListener('resize', onResize));
  return { width, height };
}

function MyComponent() {
  const { width, height } = createWindowSize();
  // width() and height() are getters
}
```

```svelte
<!-- Svelte 5 — rune or, with stores, a writable -->
<script lang="ts">
  function createWindowSize() {
    let width = $state(window.innerWidth);
    let height = $state(window.innerHeight);
    $effect(() => {
      const onResize = () => { width = window.innerWidth; height = window.innerHeight; };
      window.addEventListener('resize', onResize);
      return () => window.removeEventListener('resize', onResize);
    });
    return { get width() { return width; }, get height() { return height; } };
  }
  const size = createWindowSize();
</script>

<div>{size.width} × {size.height}</div>
```

The shared behavior is a function the component calls and composes. No
hidden injection, no wrapper chain. If a component needs three shared
behaviors, it calls three functions — they appear at the top of the
component's body where a reader naturally meets them, in the order they
were called. This is composition, exactly the pattern Check 5 recommends.

The same applies to the more substantial cases: data fetching (above),
form state (below), media queries, intersection observers, undo/redo,
keyboard shortcuts. If a behavior would otherwise tempt a base class or
an HOC, package it as a hook/composable/rune function and call it.

---

## Example 3 — Store slice as a deep module

A pattern in growing apps: state starts in a component, gets lifted to a
parent, then to a context, then to a global store — but the store grows by
accretion, becoming a grab-bag.

```tsx
// React with Zustand — the grab-bag store
const useStore = create((set) => ({
  user: null,
  setUser: (u) => set({ user: u }),
  theme: 'light',
  setTheme: (t) => set({ theme: t }),
  cart: [],
  setCart: (c) => set({ cart: c }),
  addToCart: (item) => set((s) => ({ cart: [...s.cart, item] })),
  removeFromCart: (id) => set((s) => ({ cart: s.cart.filter((i) => i.id !== id) })),
  coupon: null,
  setCoupon: (c) => set({ coupon: c }),
  notifications: [],
  addNotification: (n) => set((s) => ({ notifications: [...s.notifications, n] })),
  // ...30 more
}));
```

This is classitis at the store level. Auth, theme, cart, coupons, and
notifications share nothing except a tendency to live globally. Selectors
get longer and longer, all components subscribe to the same store, every
mutation can in principle touch anything, and the "interface" of the store
is the entire state shape exposed by getter and the entire set of mutations
exposed by name. Maximum shallowness.

Re-slice by knowledge (Check 1). Each slice owns one body of state and the
operations that maintain its invariants.

```tsx
// React + Zustand — slices per domain
export const useCart = create<CartState>((set, get) => ({
  items: [],
  coupon: null,
  add(item) {
    if (get().items.some((i) => i.id === item.id)) return;     // invariant
    set((s) => ({ items: [...s.items, item] }));
  },
  remove(id) { set((s) => ({ items: s.items.filter((i) => i.id !== id) })); },
  applyCoupon(code) { /* validates, sets, may throw a typed error */ },
  total(): number { /* computes from items + coupon */ }
}));

export const useAuth = create<AuthState>((set) => ({ ... }));      // separate
export const useTheme = create<ThemeState>((set) => ({ ... }));    // separate
```

```ts
// Solid — equivalent shape with createStore or signals + a module
import { createStore } from 'solid-js/store';

const [cart, setCart] = createStore<CartState>({ items: [], coupon: null });
export const Cart = {
  state: cart,
  add(item: Item) {
    if (cart.items.some((i) => i.id === item.id)) return;
    setCart('items', (xs) => [...xs, item]);
  },
  remove(id: string) { setCart('items', (xs) => xs.filter((i) => i.id !== id)); },
  total(): number { /* ... */ },
};
```

```ts
// Svelte — writable + module
import { writable, derived, get } from 'svelte/store';

const items = writable<Item[]>([]);
const coupon = writable<Coupon | null>(null);

export const Cart = {
  items,
  coupon,
  total: derived([items, coupon], ([$items, $coupon]) => /* ... */),
  add(item: Item) {
    items.update((xs) => xs.some((i) => i.id === item.id) ? xs : [...xs, item]);
  },
  remove(id: string) { items.update((xs) => xs.filter((i) => i.id !== id)); },
};
```

Each slice is now a deep module: the interface (`add`, `remove`, `total`,
`applyCoupon`) expresses intent; the state shape and the invariants live
inside. Components call `Cart.add(item)`, not `useStore.setState((s) =>
({ cart: [...s.cart, item] }))`. The "what counts as a duplicate" rule
lives once, in `add`. Adding the next state concern (a `wishlist`)
creates a new slice; it does not extend the same monolith.

Guardrail: don't shatter into so many slices that every component imports
six. Slice by real knowledge boundary (auth, cart, theme), not per
field.

---

## Example 4 — Headless behavior versus mega-prop component

A pattern that compounds for a year and a half:

```tsx
// The combobox that grew
<Combobox
  options={products}
  value={selected}
  onChange={setSelected}
  placeholder="Search products..."
  loading={isFetching}
  emptyState={<NoResults />}
  optionRenderer={(p) => <ProductOption product={p} />}
  filterFn={fuzzyMatch}
  multi={false}
  allowCreate={true}
  onCreate={handleCreate}
  groupBy={(p) => p.category}
  groupRenderer={(g) => <GroupHeader name={g} />}
  selectedRenderer={(p) => <ProductChip product={p} />}
  disabled={!user.canEdit}
  size="md"
  popoverAlign="start"
  closeOnSelect={false}
  // ...11 more props
/>
```

This is overexposure (Check 8 / a Check 7 split candidate). The component's
common case requires a caller to make 20 decisions, most of which are
irrelevant most of the time. The component owns rendering, filtering,
keyboard handling, focus management, popover positioning, multi-select,
creation, grouping — every feature concatenated into one prop surface.

Two things are tangled: the *behavior* of a combobox (keyboard navigation,
selection state, ARIA semantics, popover open/close) and the *presentation*
(how options look, how the trigger looks, the popover style). Split them.

```tsx
// React — headless behavior hook + presentational component
function useCombobox<T>(opts: { items: T[]; getId: (t: T) => string }) {
  // owns: open/closed state, highlighted index, keyboard nav, ARIA props,
  //       selection, filter input
  return { /* state + handlers */ };
}

// component author composes
function ProductCombobox({ products }: { products: Product[] }) {
  const cb = useCombobox({ items: products, getId: (p) => p.id });
  return (
    <div {...cb.rootProps}>
      <input {...cb.inputProps} placeholder="Search products..." />
      {cb.isOpen && (
        <ul {...cb.listProps}>
          {cb.filtered.map((p, i) => (
            <li key={p.id} {...cb.itemProps(i)}>
              <ProductOption product={p} />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
```

```tsx
// Solid — same idea, signals instead of state
function createCombobox<T>(opts: { items: () => T[]; getId: (t: T) => string }) {
  // returns signals for open/highlighted/filtered + accessor props
  return { /* ... */ };
}
```

```svelte
<!-- Svelte — a class or factory returning runes + actions -->
<script lang="ts">
  import { createCombobox } from '$lib/combobox';
  export let products: Product[];
  const cb = createCombobox({ items: () => products, getId: (p) => p.id });
</script>

<div use:cb.rootAction>
  <input use:cb.inputAction placeholder="Search products..." />
  {#if cb.isOpen}
    <ul use:cb.listAction>
      {#each cb.filtered as p, i}
        <li use:cb.itemAction={i}><ProductOption product={p} /></li>
      {/each}
    </ul>
  {/if}
</div>
```

The behavior is one deep module (the hook / composable / factory); the
presentation is whatever the consumer writes. Each `ProductCombobox`,
`UserCombobox`, `TagCombobox` is a few lines of presentational code that
composes the behavior, not 20 props to a black box that tries to be every
combobox.

This pattern is what Radix, Headless UI, and Melt UI productize. Adopting
one of those libraries is usually cheaper than writing your own; the
principle to take away is *why* they're structured that way — behavior
and presentation are different bodies of knowledge, and a single component
that ships both ends up with a wide and shallow interface.

---

## Cross-framework cheat sheet

| Pattern | React idiom | Solid idiom | Svelte idiom |
|---|---|---|---|
| Shared behavior | Custom hook (`use*`) | Composable (`create*`) | Rune-based factory or composable |
| Local reactive state | `useState`, `useReducer` | `createSignal`, `createStore` | `$state`, `writable` |
| Side effect on dependency change | `useEffect` | `createEffect` | `$effect` |
| Derived value | `useMemo` | `createMemo` | `$derived`, `derived(store, …)` |
| Cross-tree shared value | `Context` + `useContext` | `Context.Provider` + `useContext` | `setContext` / `getContext` |
| Global state slice | Zustand / Redux Toolkit slice | `createStore` in a module | `writable` in a module |
| Server state | TanStack Query, SWR | TanStack Solid Query | TanStack Svelte Query |
| Form state | React Hook Form, TanStack Form | Solid forms / TanStack Form | Svelte forms / TanStack Form |

The principles are the same in every column: the deep module is the
function/hook/composable/rune; components call it; shared knowledge lives
inside it; the rest of the framework is reactive plumbing.
