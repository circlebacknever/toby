# Worked Examples — Web SPAs (React, Solid, Svelte)

The web SPA stack has its own pattern vocabulary: hooks (React), composables
and signals (Solid, Vue), runes and stores (Svelte). The framework names
differ, but the same module principles apply to each. These examples show the same checks
applied across the three with the idiom of each.

The existing `examples.md` covers two foundational web cases (prop drilling
and classitis). This file adds patterns specific to building real applications
in any of the three frameworks.

---

## Example 1 — Server state mixed into components

Most apps in every framework contain this pattern:

```tsx
// React: the component fetches its own data
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

The same block is repeated in `OrderPage`, `CustomerPage`, and `InvoicePage`.
Every component re-implements cancellation on unmount, error semantics, and
loading state. All of them lack a cache, refetch on focus, and retry on
transient failure. The "interface to fetching" is a
30-line block of `useEffect` code duplicated in every page.

The repeated block is information leakage that grows with each new page. The
decisions "how do we cancel," "what the loading state holds," "what counts as
an error" are encoded in every component. If you change one decision, such as
adding a `retry-after` hint to errors, you edit fifteen components.

The deep module is a query library. All three frameworks ship an integration.
React uses TanStack Query / SWR, Solid uses TanStack Query, and Svelte uses
TanStack Query or `@tanstack/svelte-query`. Use one of these libraries:

```tsx
// This React version uses TanStack Query
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
// This Solid version uses @tanstack/solid-query, with the same structure and different reactivity
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
<!-- This Svelte 5 version uses @tanstack/svelte-query -->
<script lang="ts">
  import { createQuery } from '@tanstack/svelte-query';
  let { id }: { id: string } = $props();
  // Pass the options as a thunk so the query tracks id. v6 requires the thunk.
  const query = createQuery(() => ({ queryKey: ['product', id], queryFn: () => api.products.get(id) }));
</script>

{#if $query.isLoading}
  <Spinner />
{:else if $query.error}
  <ErrorState err={$query.error} />
{:else}
  <ProductView product={$query.data} />
{/if}
```

One library, designed as a deep module, handles cancellation, deduping, retry, cache,
refetch-on-focus, and request waterfalls across components. The component now
only renders. When the team later decides every error
should show a toast, the team makes one configuration change in one place.

Build your own only if you have a reason, because avoiding a dependency costs more
than it saves by the third component.

---

## Example 2 — Shared behavior via hook / composable / rune

This older pattern still appears in new code:

```tsx
// This React higher-order component gives a component the window size
function withWindowSize<P>(Component: React.ComponentType<P & WindowSize>) {
  return class extends React.Component<P, WindowSize> {
    state = { width: window.innerWidth, height: window.innerHeight };
    handleResize = () => this.setState({ width: window.innerWidth, height: window.innerHeight });
    componentDidMount() { window.addEventListener('resize', this.handleResize); }
    componentWillUnmount() { window.removeEventListener('resize', this.handleResize); }
    render() { return <Component {...this.props} {...this.state} />; }
  };
}

// Components then use it everywhere like this:
export default withWindowSize(withCurrentUser(withTheme(MyComponent)));
```

The higher-order component leaks information the way implementation inheritance does, without using a class. `withWindowSize` and `MyComponent` are
in a parent-child relationship where the wrapper invisibly injects props and
overrides nothing visible. Yet `MyComponent` cannot be understood without
reading the wrapper. With three wrappers ("wrapper hell"), a reader cannot learn
the component's real interface from its file.

The composition replacement looks nearly identical across the three
frameworks. The thing being shared is a small piece of logic, packaged as
a function the consumer calls.

```tsx
// In React, the shared logic is a useWindowSize hook
function useWindowSize() {
  const [size, setSize] = useState({ width: window.innerWidth, height: window.innerHeight });
  useEffect(() => {
    const onResize = () => setSize({ width: window.innerWidth, height: window.innerHeight });
    window.addEventListener('resize', onResize);
    return () => window.removeEventListener('resize', onResize);
  }, []);
  return size;
}

// Any component calls it like this:
function MyComponent() {
  const { width, height } = useWindowSize();
  // ...
}
```

```tsx
// In Solid, the shared logic is a composable that returns signals
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
<!-- In Svelte 5, the shared logic uses a rune, or a writable when you use stores -->
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

The shared behavior is a function the component calls and composes. The
component has no hidden injection and no wrapper chain. If a component needs three shared
behaviors, it calls three functions. They appear at the top of the
component's body, where a reader sees them first, in the order they
were called. Calling shared functions is composition, so it passes the composition-over-inheritance check.

The same applies to the more substantial cases: data fetching (above),
form state (below), media queries, intersection observers, undo/redo,
keyboard shortcuts. If a behavior would otherwise lead someone to write a base class
or an HOC, package it as a hook/composable/rune function and call it.

---

## Example 3 — Store slice as a deep module

In growing apps, state starts in a component, gets lifted to a parent, then
to a context, then to a global store. The store then gains one unrelated field after another and becomes
a grab-bag.

```tsx
// This React store uses Zustand and is the grab-bag store
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
  // The store has 30 more entries like these.
}));
```

The grab-bag store is classitis at the store level. Auth, theme, cart,
coupons, and notifications share nothing except being global. Selectors
get longer and longer. All components subscribe to the same store.

Every
mutation can change any part of the state. The "interface" of the store
is the entire state layout exposed by getter and the entire set of mutations
exposed by name. An interface that is the whole state layout makes the store
as shallow as a module gets.

Divide the store again by knowledge (the decompose-by-knowledge check). Each slice holds one body of state and the
operations that maintain its invariants.

```tsx
// With React and Zustand, each domain gets its own slice
export const useCart = create<CartState>((set, get) => ({
  items: [],
  coupon: null,
  add(item) {
    if (get().items.some((i) => i.id === item.id)) return;     // This check keeps the no-duplicates invariant
    set((s) => ({ items: [...s.items, item] }));
  },
  remove(id) { set((s) => ({ items: s.items.filter((i) => i.id !== id) })); },
  applyCoupon(code) { /* Validates the code, sets the coupon, and may throw a typed error */ },
  total(): number { /* computes from items + coupon */ }
}));

export const useAuth = create<AuthState>((set) => ({ ... }));      // This is a separate slice.
export const useTheme = create<ThemeState>((set) => ({ ... }));    // This is a separate slice.
```

```ts
// In Solid, createStore or signals plus a module give an equivalent structure
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
// In Svelte, the slice is a module built on writable
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

The three frameworks handle one reactivity caveat differently, because `total`
is a derived value. Solid tracks `total` on read, so `Cart.total()` in JSX
re-runs when `items` or `coupon` changes. Svelte's `derived` store does the same. Zustand
doesn't track derived reads. A component gets the live value through a
selector that calls it, `useCart((s) => s.total())`, so the subscription
recomputes on change. Selecting the bare method (`s.total`) or calling
`useCart.getState().total()` outside a selector doesn't subscribe, and the
value goes stale.

Each slice is now a deep module. The interface (`add`, `remove`, `total`,
`applyCoupon`) expresses intent. The state layout and the invariants are
inside the slice. Components call `Cart.add(item)`.

In the grab-bag form, they called directly
into `useStore.setState((s) => ({ cart: [...s.cart, item] }))`. The "what
counts as a duplicate" rule
is in one place, `add`. Adding the next state concern (a `wishlist`)
creates a new slice. It leaves the other slices unchanged.

Do not split the store into so many slices that every component imports
six. Slice by real knowledge boundary (auth, cart, theme). One slice per field
splits the store too far.

---

## Example 4 — Headless behavior versus mega-prop component

This component grew for a year and a half:

```tsx
// This combobox kept gaining props
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
  // The component takes 11 more props like these.
/>
```

The mega-prop `Combobox` is overexposure (it fails the depth check and is a split candidate under the split/merge check). The component's
common case requires a caller to make 20 decisions, most of which are
irrelevant most of the time. The component handles rendering, filtering,
keyboard handling, focus management, popover positioning, multi-select,
creation, and grouping, so every feature adds to one list of props.

The component mixes two things: the *behavior* of a combobox (keyboard navigation,
selection state, ARIA semantics, popover open/close) and the *presentation*
(how options look, how the trigger looks, the popover style). Split the behavior from the presentation.

```tsx
// In React, a headless behavior hook and a presentational component split the two
function useCombobox<T>(opts: { items: T[]; getId: (t: T) => string }) {
  // This hook manages open/closed state, highlighted index, keyboard nav, ARIA props,
  //       selection, filter input
  return { /* Returns the state and the handlers */ };
}

// The component author composes the parts
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
// In Solid, the same idea is built on signals
function createCombobox<T>(opts: { items: () => T[]; getId: (t: T) => string }) {
  // returns signals for open/highlighted/filtered + accessor props
  return { /* ... */ };
}
```

```svelte
<!-- In Svelte 5, a factory returns runes and actions -->
<script lang="ts">
  import { createCombobox } from '$lib/combobox';
  let { products }: { products: Product[] } = $props();
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

The behavior is one deep module (the hook / composable / factory). The
presentation is whatever the consumer writes. Each `ProductCombobox`,
`UserCombobox`, `TagCombobox` is a few lines of presentational code that
composes the behavior. The mega-prop form put 20 props into one component
that every combobox had to use.

Radix, Headless UI, and Melt UI package the headless pattern as libraries.
Adopting one of those libraries is usually cheaper than writing your own. They
are structured that way because behavior and presentation are different bodies
of knowledge. A single component
that ships both has a wide and shallow interface.

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

The principles are the same in every column. Components call the deep module, which is the
function/hook/composable/rune and holds the shared knowledge. The rest of the framework handles reactivity.
