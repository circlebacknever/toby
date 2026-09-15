# Worked Examples — Web SPAs (React, Solid, Svelte)

The web stack has its own complexity patterns. Errors arrive from three
sources at once: network, render, and user input. Performance problems
come from a fourth source: re-renders, large lists, and memoization decisions.
The ladders apply. The right fix in each framework uses that framework's idioms.

---

## Example 1 — Error boundaries: scope by recoverability

Teams often add error boundaries to a React app like this:

```tsx
// App.tsx
<ErrorBoundary fallback={<AppCrashedScreen />}>
  <App />
</ErrorBoundary>
```

A single boundary around the entire app catches everything. The fallback
renders an "Application Error" screen. Every render error, anywhere,
unmounts the whole tree. The user loses their form data, their scroll
position, their open dialog. The single root boundary is aggregation at the wrong level. The
boundary aggregates more than it should because no smaller boundary was
designed.

A better design places boundaries at recoverable units.

```tsx
// App.tsx
<ErrorBoundary fallback={<HardCrashScreen />}>      // A full unmount is acceptable at this last-resort boundary.
  <Layout>
    <Routes>
      <Route path="/dashboard" element={
        <ErrorBoundary fallback={<RouteErrorScreen />}>     // This boundary covers one route.
          <Dashboard />
        </ErrorBoundary>
      } />
      <Route path="/orders/:id" element={
        <ErrorBoundary fallback={<RouteErrorScreen />}>
          <OrderDetail />
        </ErrorBoundary>
      } />
    </Routes>
  </Layout>
</ErrorBoundary>

// Inside a route, a boundary wraps the risky widget.
<ErrorBoundary fallback={<WidgetErrorPlaceholder />}>
  <ThirdPartyChart data={data} />
</ErrorBoundary>
```

The design has three levels. The outer last-resort boundary is rare and does a full reset. Per-route
boundaries let the user keep their nav state when only this route is broken.
Per-widget boundaries go around known-risky children, because a chart library
that occasionally throws on bad data shouldn't unmount the page.

The three levels apply the error ladder at the render layer. Defining the error
out doesn't apply, because a child throwing during render is a real error. The
widget-level boundary masks at the lowest level. The route-level boundary
aggregates everything that bubbled past the per-widget boundaries. The
app-level fallback is the equivalent of letting the app crash.

Solid and Svelte get the same treatment. Solid has `ErrorBoundary` built in, and Svelte uses boundary
components in libraries like `svelte-error-boundary` or the framework's
own error pages in SvelteKit.

---

## Example 2 — Async errors: a typed Result discriminator

This pattern grows as each page repeats it:

```tsx
function OrderPage({ id }: { id: string }) {
  const [order, setOrder] = useState<Order | null>(null);
  const [error, setError] = useState<Error | null>(null);
  useEffect(() => {
    try {
      api.getOrder(id).then(setOrder).catch((e) => {
        if (e instanceof NetworkError) setError(e);
        else if (e instanceof AuthError) navigate('/login');
        else if (e instanceof NotFoundError) navigate('/404');
        else setError(e);
      });
    } catch (e) {
      setError(e as Error);
    }
  }, [id]);
  // ...
}
```

Every page that loads data repeats this pattern. Each copy differs slightly
about which errors get which treatment. Each call site handles common errors
when one handler would do, so the error ladder fails at rung 3 (aggregation).

The right handling depends on where each error matters:

- **NetworkError** is usually transient. Retry inside the API client (rung
  2, masking at low level). With a sensible retry-with-backoff, a network
  blip never reaches the component.

- **AuthError** has one global handler, which navigates to login and clears
  the session. That handler is aggregation (rung 3) at the API client or
  response interceptor level, which is where the one handler belongs.
- **NotFoundError** is usually a real "this resource doesn't exist for
  this user" case. Surface it as a typed Result so the component can
  render a "not found" view, which is the accurate state for this case.
- **Unexpected errors** propagate to the route-level error boundary
  (rung 3 again, at the render layer).

The page looks like this after the cleanup:

```tsx
function OrderPage({ id }: { id: string }) {
  const q = useOrder(id);                     // returns the discriminated query result
  switch (q.status) {
    case 'loading':   return <Spinner />;
    case 'not_found': return <OrderNotFound />;
    case 'success':   return <OrderView order={q.order} />;
    // network/auth/unexpected errors never reach here:
    //  - network: retried inside the API client
    //  - auth: handled globally by the response interceptor
    //  - unexpected: bubbled to the route's ErrorBoundary
  }
}
```

The page handles only the cases that are its concern. The other
three groups of handlers are removed from this file and from every other page
that used the same pattern.

`useOrder` returns a discriminated query result, which is a `status` plus the
data for that state. This page renders only the states it handles. The `error`
and `stale` arms are absent by design. The rungs above handle the error cases
through the client's retry, the interceptor, and the boundary, so those cases
never reach the component. The treatment is the same. The result has fewer
arms because the handling moved.

---

## Example 3 — Memoization gone wrong: `useMemo`/`useCallback` everywhere

A team adopts "memoize all functions and computed values to avoid
re-renders":

```tsx
function ProductCard({ product, onSelect }: { product: Product; onSelect: (p: Product) => void }) {
  const priceFormatted = useMemo(() => formatPrice(product.price, product.currency), [product.price, product.currency]);
  const tagsClass = useMemo(() => `tag tag-${product.category}`, [product.category]);
  const handleClick = useCallback(() => onSelect(product), [onSelect, product]);
  const titleProps = useMemo(() => ({ id: `product-${product.id}-title` }), [product.id]);
  // ...
}
```

The author believes that `useMemo` prevents the re-render. 
Every `useMemo` adds a closure allocation, a comparison of
dependencies, and a tiny bit of work on every render. For values that are
cheap to compute, the memoization itself costs more than what it saves.
The number of `useMemo` calls matches the author's worry about
performance. It has no link to how often the component renders.

Blanket memoization is speculative performance complexity added without
measurement. It also hides the design problems it appears to solve. When a component
re-renders too often, the right fix is usually higher up the tree. Examples are a stable
parent reference, a context that doesn't change every render, list keys
that are stable.

The team wants these rules:

- **Default: no memoization.** Components are designed to re-render. The
  React Compiler (v1.0, opt-in) memoizes at build time, so where it runs the
  hand-written `useMemo`/`useCallback` is redundant. Plain React 19 without
  the compiler re-renders as it always has. Solid and Svelte don't need to answer the
  question, because fine-grained reactivity updates only what changed.

- **`useMemo`** is for expensive computations whose dependencies are stable
  enough that the memo will hit. "Expensive" means measurably expensive, such as
  parsing a large blob or computing a derived structure over many items.
- **`useCallback`** is for callbacks passed to memoized children that
  compare by referential equality, or to the dependency arrays of other
  hooks. A callback used only as a JSX DOM event prop (`onClick`) doesn't
  need it.
- **Object-prop memoization** is for stabilizing references passed to
  memoized children. It is almost never useful when the consumer isn't
  itself memoized.

This version is worth its complexity:

```tsx
function ProductList({ products, filter }: { products: Product[]; filter: string }) {
  // Re-running this expensive scan on every keystroke is the bottleneck.
  const filtered = useMemo(() => fuzzyFilter(products, filter), [products, filter]);
  return <>{filtered.map((p) => <ProductCard key={p.id} product={p} />)}</>;
}
```

Keep one `useMemo` on the one expensive computation. Let everything
else re-evaluate, because users don't notice that cost.

In Solid, this class of problem mostly does not occur, because
`createSignal` and `createMemo` are fine-grained. Unnecessary
memoization is unusual even at scale. In Svelte 5 with `$derived`, the
equivalent is automatic. In React, the framework's default is already the
right answer for most components, so don't add a memoization layer.

---

## Example 4 — Virtualization: a measured decision

A team is about to render 200 items in a list. Someone says "we should
virtualize this."

Try the cheap design first, with no special case. Render the 200 list items
as small components, which the browser handles easily, so no virtualization
library is needed.

The team renders 2000 items. Things get slower on low-end devices but the
P95 is still acceptable. The team probably needs no virtualization yet, so
measure the specific bottleneck. The item count is rarely the cause. The usual cause
is a single expensive per-row computation, or a giant image being rendered
without sizing constraints.

When the team renders 50,000 items and measures the slowdown,
virtualization is worth its complexity:

```tsx
// Use react-virtual or TanStack Virtual.
import { useVirtualizer } from '@tanstack/react-virtual';

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => scrollRef.current,
  estimateSize: () => 60,
  overscan: 5,
});
```

This table gives the "is this worth the complexity" answer for each step:

| Item count | Default rendering | Virtualization |
|---|---|---|
| < 100 | Yes | No, because the added complexity costs more than it saves |
| 100-1000 | Yes for most components, but profile interaction-heavy ones | Only when measured |
| 1000-10,000 | Maybe, depending on per-row cost | Likely, but measure first |
| 10,000+ | No | Yes, almost always |

Adding virtualization to a 100-item list because "lists should be
virtualized" is exactly the speculative-complexity anti-pattern. The
library adds costs. Scroll-position bugs appear, focus management and sticky
items become harder, snapshot tests get noisy, and ctrl-F no longer finds
text in the list. Accept each cost only when a measurement
justifies it.

The same decision applies to Solid (`solid-virtual`) and Svelte (`svelte-virtual`
or framework-specific patterns).

---

## Example 5 — Render performance: design-time choices come first

Here is a common slow render, which the team blames on React and then tries to fix
with memoization:

```tsx
function Dashboard() {
  const [filter, setFilter] = useState('');
  const orders = useOrders();           // 500 items

  return (
    <>
      <FilterInput value={filter} onChange={setFilter} />
      {orders
        .filter((o) => o.customer.toLowerCase().includes(filter.toLowerCase()))
        .sort((a, b) => b.total - a.total)
        .map((o) => <OrderRow key={o.id} order={o} />)
      }
    </>
  );
}
```

The filter + sort runs on every keystroke. Each run makes two passes (filter,
sort) over 500 items, with one allocation per pass. The team's first instinct is `useMemo` on
the result. That helps, but the design-time changes are cheaper *and* better:

- Pre-lowercase the customer name once when orders are loaded, so each
  comparison reuses it. That removes 500 string lowercases per keystroke.
- Sort once when orders are loaded, so every render reads the sorted list.
- Debounce the filter input. Users don't see results between keystrokes
  anyway, so running the filter at 60fps when they're typing is wasted work.

```tsx
function Dashboard() {
  const orders = useOrders();          // useOrders returns orders sorted by total descending, with a lowercased customerLower field
  const [filter, setFilter] = useState('');
  const debouncedFilter = useDebouncedValue(filter, 100);
  const filtered = useMemo(
    () => orders.filter((o) => o.customerLower.includes(debouncedFilter.toLowerCase())),
    [orders, debouncedFilter]
  );
  return (
    <>
      <FilterInput value={filter} onChange={setFilter} />
      {filtered.map((o) => <OrderRow key={o.id} order={o} />)}
    </>
  );
}
```

The `useMemo` is now worth its cost, because the filter is the only expensive thing left.
The pre-sort and pre-lowercase happen once at load, so every render reads
the result. The debounce eliminates work the user can't perceive. The three design-time
changes are each almost free, so the slow render disappears without any
extra memoization.

The `Dashboard` fix makes the same point as `examples.md` Example 3. Design-time
moves are the cheap layer, and they prevent the case where many small costs add up to a slow render.
The profiler session comes after them.

---

## Cheat sheet

| Symptom | Move |
|---|---|
| try/catch in every useEffect/effect | Use the error ladder: retry transient errors at the API layer, send unexpected errors to a route boundary, and return a typed Result for "not found" |
| Single huge ErrorBoundary at the root | Add per-route and per-widget boundaries, and keep the root boundary as the last resort |
| useMemo/useCallback on everything | Default to no memoization, and memoize the one measurably-expensive computation |
| Virtualizing a 100-item list | Don't, because the library adds cost without a benefit |
| Filter/sort in render | Pre-sort and pre-index at load, and debounce the input |
