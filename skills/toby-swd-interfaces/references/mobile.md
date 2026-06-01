# Worked Examples — Mobile (React Native, with notes for native)

Mobile interfaces have three idiosyncrasies the comment test exposes
quickly: navigation params get serialized so the interface to a screen is
literally a string contract, native bridges have an asymmetric cost
profile that tempts thin wrappers, and persistent storage interfaces are
where stale data lives if the contract isn't clear.

---

## Example 1 — Native bridge interface: passthrough wrapper vs deep state machine

Candidate A, the literal mirror of the native module:

```ts
export const Biometrics = {
  isAvailable: NativeModules.RNBiometrics.isAvailable,
  authenticate: NativeModules.RNBiometrics.authenticate,
  createKeys: NativeModules.RNBiometrics.createKeys,
  deleteKeys: NativeModules.RNBiometrics.deleteKeys,
  createSignature: NativeModules.RNBiometrics.createSignature,
  simplePrompt: NativeModules.RNBiometrics.simplePrompt,
  biometricKeysExist: NativeModules.RNBiometrics.biometricKeysExist,
};
```

The interface comment, complete:

> Wraps the native biometrics module. Call isAvailable first to check whether
> the device supports biometric auth. Then call biometricKeysExist to see
> whether a key pair already exists for this app. If not, call createKeys
> before authenticate. authenticate prompts the user; simplePrompt does the
> same but without using a key. createSignature signs a payload using the
> stored key; the key is keyed to the device, so signatures are not portable.
> On iOS, FaceID requires the NSFaceIDUsageDescription Info.plist entry or
> authenticate will fail silently with no error. On Android,
> isAvailable may return true on devices where the user has not enrolled a
> fingerprint, in which case authenticate will throw. Always wrap
> authenticate in try/catch and handle BiometryNotAvailable,
> BiometryNotEnrolled, and BiometryLockoutPermanent separately.

Twelve sentences. Describes ordering ("Call X first, then Y"). Describes
platform-specific protocol. The "interface" is really seven separate APIs
the caller must compose, with platform quirks layered on top. Failure
named.

Candidate B, the deep module:

```ts
type BiometricsState =
  | { status: 'unavailable'; reason: 'unsupported' | 'not_enrolled' | 'permanently_locked' }
  | { status: 'available' }
  | { status: 'locked'; retryAfter: Date };

type AuthResult =
  | { ok: true; signature?: string }
  | { ok: false; reason: 'user_cancelled' | 'failed' | 'locked' };

export const Biometrics = {
  status(): Promise<BiometricsState>;
  prompt(opts: { reason: string; payload?: string }): Promise<AuthResult>;
};
```

Comment:

> Reports whether biometric auth can be used on this device and prompts
> the user when needed. status returns the current capability; prompt
> displays the system biometric UI and returns a typed result. If a
> payload is supplied, the result includes a signature bound to a
> per-device key (created lazily on first use).

Four sentences. iOS/Android differences are gone from the caller's view —
they collapsed into status's discriminator. Key lifecycle, Info.plist
errors, and lockout handling all live inside. Common callers just call
`prompt({ reason: 'Confirm payment' })` and switch on the result.

Guardrail check: did anything truly caller-facing get hidden? The
caller still needs to know that a payload signature is per-device (so
sending the signature to the server is meaningful only if the server
trusts that device). One sentence covers it. The fingerprint sensor's
internal protocol does not.

---

## Example 2 — Navigation param contract: serializable identity vs object soup

In React Navigation, route params are part of a screen's public interface.
They're persisted across reloads, used by deep links, and read by
intermediate screens that pass them along.

Candidate A:

```ts
type RootStackParamList = {
  Home: undefined;
  ProductDetail: { product: Product; recommendations: Product[]; user: User };
  Checkout: { cart: Cart; user: User; shippingOptions: ShippingOption[] };
  // ...
};

navigation.navigate('ProductDetail', { product, recommendations, user });
```

The interface comment for `ProductDetail`:

> Screen for a single product. product is the product to display.
> recommendations is the related-products list to render below the main
> view; if empty, the section is hidden. user is the current user, used
> to determine whether the wishlist button shows. Note that recommendations
> are computed at navigation time and become stale if the user remains on
> the screen for longer than a few minutes; the screen does not refetch.
> Note also that this screen is reachable via deep link, in which case
> recommendations will be empty and user will be the deep-link guest user;
> in that case the screen shows a "log in to see recommendations" CTA.

Seven sentences. Describes the data flow into the screen and what happens
when each field is missing. The "interface" is leaking the structure of the
navigating screen's state and the staleness model. The deep-link case has
to be specially described because the contract was designed for the
in-app-navigation path.

Failure named: route params carry runtime state instead of identity.

Candidate B:

```ts
type RootStackParamList = {
  Home: undefined;
  ProductDetail: { productId: string };
  Checkout: { cartId: string };
};

navigation.navigate('ProductDetail', { productId: product.id });
```

Comment:

> Detail screen for the product with this id. Loads the product and
> recommendations on mount via the products repository; renders a guest
> view if the user is not signed in.

Two sentences. The route is now pure identity — what to show. Loading,
staleness, and signed-in-vs-guest are owned by the screen itself, which
reads `useAuth()` and a `useProduct(productId)` query. Deep links work
because the route is serializable and small.

The screen now uses identity in its route and queries (or context) for
everything else — auth, recommendations, current user. That's the
contract a route should have.

---

## Example 3 — Persistent storage module: untyped store vs typed accessor

A common pre-encapsulation interface:

```ts
export const Storage = {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  delete(key: string): Promise<void>;
  clear(): Promise<void>;
};
```

Comment, fully honest:

> Wraps AsyncStorage. Values must be strings; serialize JSON yourself. Keys
> are conventionally namespaced with a colon (e.g., 'user:theme',
> 'feed:cache:v2'). When changing the shape of stored data, bump the key's
> version suffix (':v1' to ':v2') so old clients don't read corrupted data.
> clear() removes everything including auth tokens; use deleteSpecific keys
> on logout instead. The set() method does not validate value size; iOS
> AsyncStorage has a per-key 2MB limit beyond which writes silently fail.

Six sentences. The "interface" is `get/set/delete/clear`, but the
operational contract — JSON serialization, key namespacing, versioning,
not-clearing-auth-on-logout, the iOS size limit — is documentation a
caller must internalize. Every screen that uses Storage gets a copy of
this knowledge.

Failure named: this is a wrapper around AsyncStorage, not a module. The
domain knowledge (what's stored, what shape, what versions exist) belongs
inside.

Redesign as typed accessors per domain:

```ts
// storage/userPrefs.ts
export const UserPrefs = {
  hasSeenOnboarding(): Promise<boolean>;
  markOnboardingSeen(): Promise<void>;
  themePreference(): Promise<'light' | 'dark' | 'system'>;
  setThemePreference(v: 'light' | 'dark' | 'system'): Promise<void>;
};

// storage/feedCache.ts
export const FeedCache = {
  load(): Promise<FeedItem[] | null>;
  save(items: FeedItem[]): Promise<void>;
  clear(): Promise<void>;
};

// storage/session.ts
export const Session = {
  tokens(): Promise<Tokens | null>;
  save(t: Tokens): Promise<void>;
  clear(): Promise<void>;
};
```

Each module's interface comment is now two or three sentences. `UserPrefs`
owns its key schema and migration; `FeedCache` owns its versioning and the
2MB limit (it batches writes or drops oldest items if needed); `Session`
owns the secure-storage detail (`Session.save` writes to Keychain/Keystore,
not AsyncStorage). The screens that use these modules don't know any of
that.

Logout becomes a deliberate composition rather than a clear-everything:

```ts
await Session.clear();
await FeedCache.clear();
// UserPrefs and onboarding deliberately survive logout
```

What to clear on logout is a decision the orchestrating code now makes
once, in one place — not a side effect of `Storage.clear()` that could
include or exclude auth depending on whether some caller remembered to
multiRemove.

---

## Example 4 — Cross-cutting: screen-level data hook interface

The interface a screen consumes for its data is a recurring case where the
comment test catches problems early.

Candidate A:

```ts
function useOrderScreen(orderId: string) {
  return {
    data: order,                          // Order | undefined
    loading,                              // boolean
    error,                                // Error | undefined
    isRefetching,                         // boolean
    actions: {
      refund(amount: number): Promise<{ success: boolean; error?: Error }>;
      cancel(reason: string): Promise<{ success: boolean; error?: Error }>;
      addNote(text: string): Promise<{ success: boolean; error?: Error }>;
    },
    permissions: {
      canRefund: boolean;
      canCancel: boolean;
      canAddNote: boolean;
    }
  };
}
```

Comment:

> Loads the order with the given id and returns its data, status flags,
> action handlers, and permissions. The actions return a result object;
> callers should check success and show the error if false. Permissions
> are derived from the current user's role and the order's state. While
> isRefetching is true, data still holds the previous value; while loading
> is true, data is undefined. Permissions may be undefined for an instant
> on first mount before the user context resolves; treat undefined as
> "not allowed."

Six sentences, describes invariants about combinations of fields, "treat X
as Y" instructions in the comment. The hook returns five named fields and
expects the caller to coordinate them.

Candidate B, smaller surface, typed state:

```ts
type OrderScreenState =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'loaded'; order: Order; actions: OrderActions };

interface OrderActions {
  refund(amount: number): Promise<Result<void>>;
  cancel(reason: string): Promise<Result<void>>;
  addNote(text: string): Promise<Result<void>>;
}

function useOrderScreen(orderId: string): OrderScreenState;
```

Comment:

> Loads the order with this id and returns its current screen state. The
> status discriminator names the three legal states; in the loaded state,
> actions reflects the operations the current user is allowed to perform
> (an action absent from actions is not permitted). Action methods return
> Result so callers can surface failures without try/catch.

Three sentences. Two improvements at the contract level:

- The discriminator eliminates the "what does undefined mean" problem.
- Permissions move from "boolean per action" to "presence of the action in
  the actions object." A button that exists when permitted is impossible
  to render in the wrong state; a button that checks `permissions.canRefund`
  before calling `actions.refund` is one if-statement away from a bug.

This second move — encoding "allowed" as presence rather than as a parallel
boolean — is the kind of contract redesign the comment test reveals,
because writing "permissions may be undefined for an instant" is the
signal that the shape is wrong.

---

## Platform notes

- **iOS/Swift, Android/Kotlin**: same checks. A `ViewController` or
  `Fragment` accepting twelve init parameters has the same shape as the
  RN screen passing a `user` object through route params. Identity in,
  state through composition.
- **Flutter**: route params are arguments; the same identity-in/data-via-providers
  principle applies. Riverpod/Provider play the context role.
- **Native modules**: the bridge interface should hide the platform's
  protocol the way Example 1 does, regardless of which side you're writing
  on. A Swift `BiometricsBridge` that exposes `isAvailable`, `createKeys`,
  `authenticate` as separate methods is the same defect as a JS wrapper
  that does so.
