# Worked Examples — Mobile (React Native, with notes for native)

Mobile complexity arrives from places web doesn't see: the network drops,
the device backgrounds, the user has 8MB of RAM left and a 6-year-old
phone. The ladders still apply.

---

## Example 1 — Offline state: mask at the network layer

A common growth pattern:

```tsx
// FeedScreen.tsx
const fetchFeed = async () => {
  try {
    const items = await api.getFeed();
    setItems(items);
  } catch (e) {
    if (isOffline(e)) {
      setError('You appear to be offline.');
    } else if (isTimeout(e)) {
      setError('Request timed out. Retry?');
    } else {
      setError('Something went wrong.');
    }
  }
};

// repeated in OrdersScreen, ProfileScreen, NotificationsScreen, ...
```

Every screen reimplements the same offline/timeout/unknown-error handling.
Worse, the user experience is inconsistent — one screen says "appear to be
offline," another says "no connection," a third just shows "Error."

Move the network error handling down to the API layer where it belongs.

```ts
// api/client.ts
async function get<T>(path: string): Promise<T> {
  const maxAttempts = 3;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fetchWithTimeout(path, 10_000);
    } catch (e) {
      if (isTransient(e) && attempt < maxAttempts) {
        await sleep(backoff(attempt));
        continue;
      }
      throw e;
    }
  }
  throw new Error('unreachable');
}
```

```ts
// api/transientErrors.ts
function isTransient(e: unknown): boolean {
  return e instanceof NetworkError
      || e instanceof TimeoutError
      || (e instanceof HttpError && e.status >= 500 && e.status < 600 && e.status !== 501);
}
```

Now a real-world momentary network drop never reaches the screen — it
gets retried and the second attempt succeeds. The error ladder rung 2
(mask at lowest level) absorbs the transient cases. The screen only sees
real failures (after 3 retries, still failing).

For sustained offline state, surface it once globally via the platform's
connectivity API:

```tsx
// hooks/useOnlineState.ts — uses @react-native-community/netinfo
export function useOnlineState(): 'online' | 'offline' | 'unknown' { ... }

// App.tsx
const status = useOnlineState();
return (
  <>
    {status === 'offline' && <OfflineBanner />}
    <MainNavigator />
  </>
);
```

The banner is one place that knows about offline state. Screens don't
implement it. Aggregated handling (rung 3) at exactly the place that
matters — the UI chrome.

What screens *do* handle: the real "I couldn't load this thing"
result, after retries failed and offline isn't the reason. That's a real
case the user needs to see, and it shows up as a typed result discriminator
on the data hook (same pattern as `web.md` Example 2).

---

## Example 2 — Native module errors: discriminated state vs untyped exceptions

A direct wrapper around a native module:

```tsx
try {
  const result = await NativeModules.PaymentSheet.present({...});
  // proceed
} catch (e) {
  if (e.code === 'USER_CANCELLED') return;
  if (e.code === 'NETWORK_ERROR') showRetry();
  if (e.code === 'INVALID_CARD') showCardError();
  if (e.code === 'AUTHENTICATION_FAILED') promptForAuth();
  if (e.code === 'SHEET_DISMISSED') return;
  // ...and 8 more error codes that may exist
  // who knows what else, just show generic error
  showGenericError();
}
```

The native module throws strings-as-codes that callers translate by hand.
The set of codes is documented in the README. iOS and Android may use
different codes for the same condition. Every screen that uses this module
repeats this switch.

Wrap the bridge with a typed result:

```ts
type PaymentResult =
  | { status: 'completed'; transactionId: string }
  | { status: 'cancelled' }
  | { status: 'failed'; reason: 'card_declined' | 'auth_required' | 'network_unavailable' | 'unknown' };

export const Payments = {
  /**
   * Presents the payment sheet and waits for the user. Returns a typed
   * result; never throws under normal use. Network failures during the
   * payment are retried internally (up to 3 attempts) and surface as
   * 'network_unavailable' only if all attempts fail.
   */
  async present(opts: PaymentOptions): Promise<PaymentResult> {
    try {
      const native = await NativeModules.PaymentSheet.present(opts);
      return { status: 'completed', transactionId: native.transactionId };
    } catch (e) {
      return classifyPaymentError(e);   // owns the iOS/Android difference, retries network
    }
  },
};
```

Caller code:

```tsx
const result = await Payments.present({...});
switch (result.status) {
  case 'completed':  navigateToConfirmation(result.transactionId); break;
  case 'cancelled':  return;        // do nothing, user closed the sheet
  case 'failed':     showFailure(result.reason); break;
}
```

Three cases, all named. The wrapper owns:
- Translating native error codes (iOS-vs-Android) into the typed reasons.
- Retrying network failures during payment.
- The "USER_CANCELLED is not really an error" convention.

This is the error ladder applied at the bridge layer — mask transient
errors (retry), define out non-errors (cancellation is a status, not a
failure), aggregate the rest into a small typed set.

---

## Example 3 — Large lists: FlatList vs ScrollView, virtualization earned

A common mistake on a phone:

```tsx
<ScrollView>
  {items.map((item) => <FeedCard key={item.id} item={item} />)}
</ScrollView>
```

ScrollView renders every child upfront. With 50 items, fine. With 500, the
initial render is slow, scroll is janky, and memory grows linearly. The
team finds the bug at 1,000 items and panics.

The right default for any list of unknown growth potential is `FlatList`
or `FlashList` (Shopify's higher-performance alternative):

```tsx
<FlatList
  data={items}
  keyExtractor={(item) => item.id}
  renderItem={({ item }) => <FeedCard item={item} />}
/>
```

`FlatList` virtualizes — only the visible items and a small overdraw zone
are rendered. Memory stays bounded. This is the design-time naturally-
efficient choice from the SKILL — same complexity as ScrollView, much
better performance. Take it always for lists that might grow.

When to escalate to `FlashList`: measured cell-recycling problems with
`FlatList` on long lists with heterogeneous cell heights, or when the
specific perf characteristics warrant it. Don't reach for FlashList on
day one; FlatList covers 95% of cases.

When to stay with `ScrollView`: known-small, known-bounded lists with
heterogeneous content where virtualization breaks layout (e.g., a
settings screen with 8 sections, each a different shape). The
virtualization here adds complexity for zero perf benefit.

Performance pitfalls to know without measuring:

- **No `keyExtractor`** or unstable keys → FlatList re-renders rows
  unnecessarily. Use a stable id, not the array index.
- **`renderItem` defined inline** as a new function each render → child
  rows re-render. Define it outside the component or memoize it.
- **Images without `width`/`height`** in styles → layout thrash. Always
  size images explicitly.
- **`scrollEventThrottle` left at default** (which on iOS is 0, meaning
  no events!) → animations driven by scroll position appear broken.
  Set it to `16` for 60fps.

These aren't speculative optimizations — they're known patterns where the
naturally-efficient version is no more complex than the slow version.
Take them on every list you write.

---

## Example 4 — Image memory: lazy, sized, and the right resolution

A profile screen with 50 avatars, each a 4MB camera-roll image:

```tsx
<Image source={{ uri: user.profilePictureUrl }} style={styles.avatar} />
```

The phone fetches 50 × 4MB = 200MB of pixel data, decodes each to fit a
40×40 thumbnail. The decoded form is several times larger than the JPEG
on disk. Two screens in, the app crashes with an OOM.

The team's instinct: lazy-load. Useful. The deeper move: don't fetch the
4MB version when you need a 40px thumbnail.

```tsx
<Image
  source={{ uri: thumbnailUrl(user.profilePictureUrl, 80) }}    // 80px thumbnail
  style={styles.avatar}
  resizeMode="cover"
/>
```

Where `thumbnailUrl` either points to a pre-generated thumbnail
(server-side image processing or a CDN with resize) or to an on-the-fly
resize service. The avatar is now 4KB, not 4MB. The phone's memory
pressure drops by orders of magnitude.

For lists of images that scroll past the viewport: pair with FlatList's
virtualization and image caching (`react-native-fast-image` or expo-image)
so off-screen images are unloaded.

For the very large user-uploaded image case (display a full-screen
photo): load progressively. Show the thumbnail first, swap in the full
resolution when it's ready. The user sees something immediately and
doesn't wait staring at a blank screen.

This is the same point as `examples.md` Example 3 — death by thousand
cuts is the failure mode. Each image is "just an image." Together, with
no resizing strategy, they OOM the device.

The naturally-efficient choice (use thumbnails) costs no more complexity
than the slow choice (use originals) when the API supports it. When the
API doesn't, the right move is at the server / CDN layer, not the client.

---

## Example 5 — Bridge call cost: batch the back-and-forth

The JS-to-native bridge in React Native is asynchronous and serialized.
Each call has a few-milliseconds floor. A pattern that gets there fast:

```tsx
// loading a contact list
const ids = await ContactsBridge.getAllContactIds();      // 1 bridge call
const contacts = [];
for (const id of ids) {
  contacts.push(await ContactsBridge.getContact(id));     // N bridge calls
}
```

With 500 contacts, that's 501 bridge crossings. At a few ms each, the
list takes 2-3 seconds to load over the bridge before any rendering
happens. This is identical to the database N+1 problem — same shape,
different layer.

The fix is a batch API at the bridge:

```ts
const contacts = await ContactsBridge.getAllContacts();    // 1 bridge call
```

If the native side already has the data in memory (often the case with
contacts, photos, calendar events), serializing the whole list once is
much cheaper than serializing one record 500 times. The bridge call
goes from ~2 seconds to ~50ms.

If the native module doesn't already offer a batched call, write one.
Native bridges are not usually the place where someone wrote the API
thinking about JS performance — the JS side often needs to ask for it.

For New Architecture / Fabric / TurboModules, the bridge is faster but
the same principle holds: fewer crossings is fewer crossings. Synchronous
TurboModule calls help for the per-call cost; batching helps for the
total work.

---

## Cheat sheet — mobile complexity

| Symptom | Move |
|---|---|
| Per-screen network error handling | Retry transient at API layer; offline banner global |
| Native module throws string codes | Typed result discriminator; wrapper classifies |
| ScrollView with many children | FlatList by default; FlashList for measured cell-recycling needs |
| 4MB images for 40px avatars | Thumbnails at the right resolution; lazy where possible |
| Loop of bridge calls (N+1 over the bridge) | Batched native API; one crossing |
| Foreground/background transitions losing state | AppState listener; restore on resume |
| Memory pressure on large lists | Bound rendered window; recycle aggressively |
