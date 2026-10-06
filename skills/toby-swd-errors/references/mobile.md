# Mobile (React Native, with notes for native)

## Network errors

Retry transient errors inside the API client, so a momentary drop reaches no screen:

```ts
// api/transientErrors.ts
function isTransient(e: unknown): boolean {
  return e instanceof NetworkError
      || e instanceof TimeoutError
      || (e instanceof HttpError && e.status >= 500 && e.status !== 501);
}
```

Show sustained offline state once, as a banner in `App.tsx` driven by a `useOnlineState()` hook over `@react-native-community/netinfo`. A screen renders only the failure that survives the retries and is not caused by being offline, as a typed result from its data hook.

## Native module errors

A native module that throws string codes makes every screen repeat a switch over codes that differ between iOS and Android. Wrap it once and return a typed result:

```ts
type PaymentResult =
  | { status: 'completed'; transactionId: string }
  | { status: 'cancelled' }
  | { status: 'failed'; reason: 'card_declined' | 'auth_required' | 'network_unavailable' | 'unknown' };
```

The wrapper maps each platform's codes to one reason, retries network failures, and makes cancellation a status, so no failure path handles it.
