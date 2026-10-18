# Mobile

This file covers network retries, offline state, and native-module error wrappers in React Native and mobile apps.

## Network errors

Retry transient failures inside the API client so screens don't handle brief drops:

```ts
// api/transientErrors.ts
function isTransient(e: unknown): boolean {
  return e instanceof NetworkError
      || e instanceof TimeoutError
      || (e instanceof HttpError && e.status >= 500 && e.status !== 501);
}
```

Retry only reads and writes that send an `idempotency key`. Show sustained offline state once as an app-level banner from `useOnlineState()`, and return a typed error from the data hook only when retries fail while online.

## Native module errors

Wrap native modules that throw platform-specific error codes in one module that returns a tagged union:

```ts
type PaymentResult =
  | { status: 'completed'; transactionId: string }
  | { status: 'cancelled' }
  | { status: 'unknown' }
  | { status: 'failed'; reason: 'card_declined' | 'auth_required' | 'other' };
```

Map iOS and Android error codes to `reason` inside the wrapper, and reuse one `idempotency key` across retries of a payment attempt. When retries end in `unknown`, query the server before allowing another charge.
