# Web SPAs

This file covers error boundary placement and async error routing in React, Solid, and Svelte applications.

## Error boundaries

Place error boundaries at three levels so a widget failure doesn't wipe out unsaved form state:

- One root boundary as a last resort to reset the app.
- One boundary per route (`<ErrorBoundary>` in React/Solid, `<svelte:boundary>` and `+error.svelte` in SvelteKit) so navigation survives a route crash.
- One boundary around third-party or crash-prone widgets (such as charts or editors).

## Async errors

Route each async error class at the layer that can act on it:

- The API client retries transient network failures on reads and idempotent writes.
- One response interceptor handles `401` by clearing the session and redirecting to sign-in.
- Data hooks return `forbidden` (`403`) and `not_found` (`404`) as typed union variants for the screen to render, and rethrow unexpected errors to the route boundary.

```tsx
function OrderPage({ id }: { id: string }) {
  const q = useOrder(id);
  switch (q.status) {
    case 'loading':   return <Spinner />;
    case 'not_found': return <OrderNotFound />;
    case 'forbidden': return <NoAccess />;
    case 'success':   return <OrderView order={q.order} />;
  }
}
```
