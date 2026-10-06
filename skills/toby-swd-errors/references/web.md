# Web SPAs (React, Solid, Svelte)

## Error boundaries

One boundary around the whole app unmounts everything on any render error, so the user loses form data, scroll position, and open dialogs. Place boundaries at three levels:

- One root boundary as the last resort, which resets the app.
- One boundary per route, so the navigation survives a broken route.
- One boundary around each child known to throw, such as a third-party chart, so the page survives a broken widget.

In Solid the component is `<ErrorBoundary>`, and in Svelte 5 it is `<svelte:boundary>`, with `+error.svelte` pages in SvelteKit.

## Async errors

Give each error class one handler at the layer where it can be acted on:

- The API client retries network errors with backoff.
- One response interceptor handles an auth error by clearing the session and opening login.
- The data hook returns not-found as a status, because the page has a view for it.
- The route boundary catches every other error.

```tsx
function OrderPage({ id }: { id: string }) {
  const q = useOrder(id);
  switch (q.status) {
    case 'loading':   return <Spinner />;
    case 'not_found': return <OrderNotFound />;
    case 'success':   return <OrderView order={q.order} />;
  }
}
```

The page has no error branch, because every other error class is handled before it reaches the page.
