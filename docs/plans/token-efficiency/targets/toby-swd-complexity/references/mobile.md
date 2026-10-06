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

## Lists

Use `FlatList` for every list that can grow, because it costs the same to write as `ScrollView` and renders only the visible rows. Move to `FlashList` when measured scrolling drops frames on a large or image-heavy list. Keep `ScrollView` for a small, fixed set of differently built sections, such as a settings screen. Apply these without measuring, since each costs nothing: a stable id as the key, `renderItem` defined outside the render, explicit image sizes, and `scrollEventThrottle={16}` for scroll-driven animation.

## Images

Request an image at the size it is drawn. A 4 MB photo decodes to tens of megabytes for a 40 px avatar, so 50 of them crash the app. Ask the server or CDN for an 80 px thumbnail, and pair long image lists with `expo-image` or `react-native-fast-image`.

## Bridge calls

Each JS-to-native call costs a few milliseconds, so a loop of 500 `getContact(id)` calls takes seconds. Add one native method that returns the whole list, even under the New Architecture.
