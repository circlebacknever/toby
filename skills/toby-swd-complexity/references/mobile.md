# Worked Examples — Mobile (React Native, with notes for native)

Mobile apps face complexity that web apps don't see. The network drops,
the device backgrounds, and the user has 8MB of RAM left and a 6-year-old
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
Worse, the user experience is inconsistent. One screen says "appear to be
offline," another says "no connection," and a third just shows "Error."

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

Now a real-world momentary network drop never reaches the screen, because
it gets retried and the second attempt succeeds. The error ladder rung 2
(mask at lowest level) absorbs the transient cases. The screen only sees
real failures (after 3 retries, still failing).

The loop is safe here because `get` is idempotent, so repeating it changes
nothing. A mutating `post` can't reuse it as-is. A retry after a lost
response can submit the same write twice, so a write needs an idempotency
key the server dedupes on before the same retry logic applies.

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

The banner is the one place that knows about offline state, so screens don't
implement it. The banner is aggregated handling (rung 3) in the UI chrome,
which is where offline state matters.

What screens *do* handle: the real "I couldn't load this thing"
result, after retries failed and offline isn't the reason. That's a real
case the user needs to see, and it shows up as a typed result discriminator
on the data hook (same pattern as `web.md` Example 2).

---

## Example 2 — Native module errors: a discriminated result

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

The wrapper names all three cases and owns these jobs:
- Translating native error codes (iOS-vs-Android) into the typed reasons.
- Retrying network failures during payment.
- The "USER_CANCELLED is not really an error" convention.

The wrapper applies the error ladder at the bridge layer. It masks transient
errors (retry), defines out non-errors (cancellation becomes a status and
never enters the failure path), and aggregates the rest into a small typed set.

---

## Example 3 — Large lists: FlatList by default, virtualization earned

A common mistake on a phone:

```tsx
<ScrollView>
  {items.map((item) => <FeedCard key={item.id} item={item} />)}
</ScrollView>
```

ScrollView renders every child upfront, which works with 50 items. With 500, the
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

`FlatList` virtualizes, so only the visible items and a small overdraw zone
are rendered. Memory stays bounded. `FlatList` is the design-time, naturally
efficient choice from the SKILL, because it has the same complexity as
ScrollView and much better performance. Use it for every list that might grow.

Escalate to `FlashList` for large or image-heavy lists where measured
`FlatList` scrolling drops frames. FlashList v2 is a New-Architecture-only
rewrite that sizes cells automatically, and the v1 chore of estimating item
heights is gone. On a New-Architecture app it's a reasonable default for
big lists. `FlatList` is still built in, needs no extra dependency, and
handles small-to-medium lists.

Stay with `ScrollView` for known-small, known-bounded lists with
heterogeneous content where virtualization breaks layout (for example, a
settings screen with 8 sections, each built differently). The
virtualization here adds complexity for zero perf benefit.

Know these performance pitfalls without measuring:

- **Unstable keys** (the array index as key) mean that on reorder, insert,
  or delete, the wrong row gets recycled and component state attaches to the
  wrong item. Use a stable id. FlatList falls back to the index only when no
  `keyExtractor` and no `item.key`/`item.id` is present.
- **`renderItem` defined inline** as a new function each render makes child
  rows re-render. Define it outside the component or memoize it.
- **Images without `width`/`height`** in styles cause layout thrash. Always
  size images explicitly.
- **`scrollEventThrottle` left at default** on iOS sends roughly one event
  per scroll gesture, so animations driven by scroll position barely update.
  Set it to `16` for ~60fps. For scroll-linked animation, `Animated.event`
  with `useNativeDriver` skips the JS-thread round trip entirely.

These are known patterns where the naturally-efficient version is no more
complex than the slow version, so they are outside the speculative-
optimization ban. Take them on every list you write.

---

## Example 4 — Image memory: lazy, sized, and the right resolution

A profile screen with 50 avatars, each a 4MB camera-roll image:

```tsx
<Image source={{ uri: user.profilePictureUrl }} style={styles.avatar} />
```

The phone fetches 50 × 4MB = 200MB over the wire, then decodes each JPEG to
a full bitmap to draw a 40×40 thumbnail. A 4MB JPEG expands to tens of
MB of RGBA once decoded. The decoded bitmaps are what exhaust memory. After
two screens, the app crashes with an OOM.

The team's first instinct is to lazy-load, which helps. The larger fix is to
skip the 4MB version when the screen needs a 40px thumbnail.

```tsx
<Image
  source={{ uri: thumbnailUrl(user.profilePictureUrl, 80) }}    // 80px thumbnail
  style={styles.avatar}
  resizeMode="cover"
/>
```

`thumbnailUrl` either points to a pre-generated thumbnail
(server-side image processing or a CDN with resize) or to an on-the-fly
resize service. The avatar is now 4KB. The phone's memory
pressure drops by orders of magnitude.

For lists of images that scroll past the viewport, pair FlatList's
virtualization with an image-caching library so off-screen images are
unloaded. Use expo-image (the default in Expo projects) or
react-native-fast-image (bare RN).

For a very large user-uploaded image, such as a full-screen photo, load
progressively. Show the thumbnail first, and swap in the full resolution
when it's ready. The user sees something immediately and
doesn't wait staring at a blank screen.

The avatar screen makes the same point as `examples.md` Example 3, where death
by thousand cuts is the failure mode. Each image is "just an image," but
together, with no resizing strategy, the images OOM the device.

The naturally-efficient choice (use thumbnails) costs no more complexity
than the slow choice (use originals) when the API supports it. When the
API doesn't, the right move is at the server / CDN layer, where the
resize belongs.

---

## Example 5 — Bridge call cost: batch the back-and-forth

The JS-to-native bridge in React Native is asynchronous and serialized, so
each call costs at least a few milliseconds. This pattern adds up bridge calls quickly:

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
happens. The loop is the database N+1 problem at a different layer, with
the same cause.

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
thinking about JS performance, so the JS side often needs to ask for it.

For New Architecture / Fabric / TurboModules, the bridge is faster, but
the same principle holds, and you should still cut the number of crossings. Synchronous
TurboModule calls help for the per-call cost, and batching helps for the
total work.

---

## Cheat sheet — mobile complexity

| Symptom | Move |
|---|---|
| Per-screen network error handling | Retry transient at API layer; offline banner global |
| Native module throws string codes | Typed result discriminator; wrapper classifies |
| ScrollView with many children | FlatList for small lists; FlashList v2 for large or image-heavy ones |
| 4MB images for 40px avatars | Thumbnails at the right resolution; lazy where possible |
| Loop of bridge calls (N+1 over the bridge) | Batched native API; one crossing |
| Foreground/background transitions losing state | AppState listener; restore on resume |
| Memory pressure on large lists | Bound rendered window; recycle aggressively |
