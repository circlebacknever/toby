# Worked Examples — Web SPAs (React, Solid, Svelte)

The web stack has its own complexity patterns. Errors arrive from three
sources at once (network, render, user input) and performance pressure
arrives from a fourth (re-renders, large lists, memoization decisions).
The ladders apply; the framework idioms shape the move.

---

## Example 1 — Error boundaries: scope by recoverability, not by ambition

A common reflex when adding error boundaries to a React app:

```tsx
// App.tsx
<ErrorBoundary fallback={<AppCrashedScreen />}>
  <App />
</ErrorBoundary>
```

A single boundary around the entire app catches everything. The fallback
renders an "Application Error" screen. Every render error, anywhere,
unmounts the whole tree. The user loses their form data, their scroll
position, their open dialog. This is aggregation at the wrong level — the
boundary aggregates more than it should because no smaller boundary was
designed.

Better: place boundaries at recoverable units, not at the root.

```tsx
// App.tsx
<ErrorBoundary fallback={<HardCrashScreen />}>      // last-resort, full unmount acceptable
  <Layout>
    <Routes>
      <Route path="/dashboard" element={
        <ErrorBoundary fallback={<RouteErrorScreen />}>     // per-route boundary
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

// Inside a route — boundary around the risky widget
<ErrorBoundary fallback={<WidgetErrorPlaceholder />}>
  <ThirdPartyChart data={data} />
</ErrorBoundary>
```

Three levels: an outer last-resort boundary (rare, full reset), per-route
boundaries (the user keeps their nav state, just this route is broken),
and per-widget boundaries around known-risky children (a chart library
that occasionally throws on bad data shouldn't take out the page).

This is the error ladder applied at the render layer. Defining-out doesn't
apply (a child throwing during render is a real error). Masking at lowest
level: the widget-level boundary is the masking layer. Aggregation: the
route-level boundary aggregates everything that bubbled past per-widget.
Just-crash: the app-level fallback is the just-crash equivalent.

Same shape in Solid (`ErrorBoundary` is built in) and Svelte (boundary
components in libraries like `svelte-error-boundary` or the framework's
own error pages in SvelteKit).

---

## Example 2 — Async errors: try/catch in every effect vs Result discriminator

The pattern that grows:

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

Repeated in every page that loads data, each slightly different about
which errors get which treatment. Common errors handled at every call site
instead of one. The error ladder failing at rung 3 (aggregation).

The cleanest move depends on which errors matter where:

- **NetworkError** is usually transient. Retry inside the API client (rung
  2 — masking at low level). With a sensible retry-with-backoff, a network
  blip never reaches the component.
- **AuthError** has one global handler — navigate to login, clear session.
  This is aggregation (rung 3) at the API client or response interceptor
  level, not at each call site.
- **NotFoundError** is usually a real "this resource doesn't exist for
  this user" case. Surface it as a typed Result so the component can
  render a "not found" view instead of "error."
- **Unexpected errors** propagate to the route-level error boundary
  (rung 3 again, at the render layer).

After the cleanup:

```tsx
function OrderPage({ id }: { id: string }) {
  const q = useOrder(id);                     // returns the discriminated query result
  switch (q.status) {
    case 'loading':   return <Spinner />;
    case 'not_found': return <OrderNotFound />;
    case 'loaded':    return <OrderView order={q.order} />;
    // network/auth/unexpected errors never reach here:
    //  - network: retried inside the API client
    //  - auth: handled globally by the response interceptor
    //  - unexpected: bubbled to the route's ErrorBoundary
  }
}
```

The page handles only the cases that are truly its concern. The other
three handler buckets disappear from this file and from every other page
that used the same pattern.

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

The author's mental model: `useMemo` prevents the re-render. The actual
behavior: every `useMemo` adds a closure allocation, a comparison of
dependencies, and a tiny bit of work on every render. For values that are
cheap to compute, the memoization itself costs more than what it saves.
Density of `useMemo` doesn't track render frequency — it tracks the
author's anxiety.

This is speculative performance complexity added without measurement. It
also hides the design problems it pretends to solve: if a component
re-renders too often, the right fix is usually higher up the tree (a stable
parent reference, a context that doesn't change every render, list keys
that are stable).

The rule the team actually wants:

- **Default: no memoization.** Components re-render. That's their job.
  React 19 (and Solid/Svelte) handle this case better than humans guess.
- **`useMemo`** is for expensive computations whose dependencies are stable
  enough that the memo will actually hit. "Expensive" means measurable —
  parsing a large blob, computing a derived structure over many items.
- **`useCallback`** is for callbacks passed to memoized children that
  compare by referential equality, or to dependency arrays of other hooks.
  Not for callbacks that get passed to native DOM event handlers — those
  don't care.
- **Object-prop memoization** is for stabilizing references passed to
  memoized children. Almost never useful when the consumer isn't itself
  memoized.

The version that earns its complexity:

```tsx
function ProductList({ products, filter }: { products: Product[]; filter: string }) {
  // Genuinely expensive — re-running this scan on every keystroke is the bottleneck.
  const filtered = useMemo(() => fuzzyFilter(products, filter), [products, filter]);
  return <>{filtered.map((p) => <ProductCard key={p.id} product={p} />)}</>;
}
```

One `useMemo`, on the one expensive computation. Everything else
re-evaluates and nobody notices.

In Solid, this whole class of problem largely disappears — `createSignal`
and `createMemo` are fine-grained, so unnecessary memoization is unusual
even at scale. In Svelte 5 with `$derived`, the equivalent is automatic.
The React lesson is: the framework's default is already the right answer
for most components; resist the urge to add a layer.

---

## Example 4 — Virtualization: a measured decision, not a default

A team is about to render 200 items in a list. Someone says "we should
virtualize this."

The cheap-design move first: no special case. Render 200 list items.
Each is a small component. The browser handles this without breaking a
sweat. No virtualization library needed.

The team renders 2000 items. Things get slower on low-end devices but the
P95 is still acceptable. Probably no virtualization yet — measure the
specific bottleneck. Often it's not the number of items but a single
expensive per-row computation, or a giant image being rendered without
sizing constraints.

The team renders 50,000 items. Now it's a measured problem. Virtualization
earns its complexity:

```tsx
// react-virtual or TanStack Virtual
import { useVirtualizer } from '@tanstack/react-virtual';

const virtualizer = useVirtualizer({
  count: items.length,
  getScrollElement: () => scrollRef.current,
  estimateSize: () => 60,
  overscan: 5,
});
```

The "is this worth the complexity" answer for each step:

| Item count | Default rendering | Virtualization |
|---|---|---|
| < 100 | Yes | No — added complexity loses |
| 100-1000 | Yes for most components; profile interaction-heavy ones | Only when measured |
| 1000-10,000 | Maybe; depends on per-row cost | Likely, measure first |
| 10,000+ | No | Yes, almost always |

Adding virtualization to a 100-item list because "lists should be
virtualized" is exactly the speculative-complexity anti-pattern. The
library adds a real cost: scroll-position bugs, focus management, sticky
items become harder, snapshot tests get noisy, you lose ctrl-F to find
text in the list. Each cost is real; pay it when it's earned.

Same call applies for Solid (`solid-virtual`) and Svelte (`svelte-virtual`
or framework-specific patterns).

---

## Example 5 — Render performance: design-time choices over post-hoc memoization

A common slow render the team blames on React, then tries to memo their
way out of:

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

The filter + sort runs on every keystroke. 500 items, two passes (filter,
sort), one allocation per pass. The team's first instinct is `useMemo` on
the result. That helps. But the design-time move is cheaper *and* better:

- Pre-lowercase the customer name once when orders are loaded, not on
  every comparison. (500 string lowercases * keystrokes * keystrokes...)
- Sort once when orders are loaded, not on every render.
- Debounce the filter input. Users don't see results between keystrokes
  anyway; running the filter at 60fps when they're typing is wasted work.

```tsx
function Dashboard() {
  const orders = useOrders();          // already sorted by total descending, lowercased customerLower added
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

The `useMemo` is now real — the filter is the only expensive thing left.
The pre-sort and pre-lowercase happen once at load, not per render. The
debounce eliminates work the user can't perceive. Three design-time moves,
each almost free, and the slow render disappears without any memoization
heroics.

This is the same point as `examples.md` Example 3: design-time moves are
the cheap layer and they prevent the death-by-a-thousand-cuts case. The
profiler session is for after.

---

## Cheat sheet

| Symptom | Move |
|---|---|
| try/catch in every useEffect/effect | Error ladder: retry transient at API layer, route boundary for unexpected, typed Result for "not found" |
| Single huge ErrorBoundary at the root | Per-route + per-widget boundaries; root is last-resort |
| useMemo/useCallback on everything | Default to no memoization; memoize the one measurably-expensive computation |
| Virtualizing a 100-item list | Don't. The library cost is real; benefit isn't |
| Filter/sort in render | Pre-sort/pre-index at load; debounce input |
