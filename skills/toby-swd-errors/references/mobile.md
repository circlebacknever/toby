# Mobile (React Native, with notes for native)

## Network errors

Retry transient errors inside the API client, so screens never see a momentary network drop:

```ts
// api/transientErrors.ts
function isTransient(e: unknown): boolean {
  return e instanceof NetworkError
      || e instanceof TimeoutError
      || (e instanceof HttpError && e.status >= 500 && e.status !== 501);
}
```

Retry only a read, or a write that sends an idempotency key the server dedupes on. A network failure after the server accepted a write looks the same as one before it.

Show sustained offline state once, as a banner in `App.tsx` driven by a `useOnlineState()` hook over `@react-native-community/netinfo`. A screen shows a failure only when it remains after the retries and being offline did not cause it. The screen gets that failure as a typed result from its data hook.

## Native module errors

A native module that throws string codes makes every screen repeat a switch over codes that differ between iOS and Android. Wrap it once and return a typed result:

```ts
type PaymentResult =
  | { status: 'completed'; transactionId: string }
  | { status: 'cancelled' }
  | { status: 'unknown' }
  | { status: 'failed'; reason: 'card_declined' | 'auth_required' | 'other' };
```

The wrapper maps each platform's codes to one reason. For a payment, the wrapper sends one idempotency key with every retry. When the retries end in a network failure, the wrapper returns `unknown`. The screen then asks the server for the payment's status before it lets the user pay again. The wrapper returns cancellation as a status, so screens handle cancellation outside their failure paths.
