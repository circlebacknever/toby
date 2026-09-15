# Worked Examples — Mobile (React Native, with notes for native)

In mobile code, the comment test quickly finds problems in navigation
params, native bridges, and persistent storage. Navigation params get
serialized, so the interface to a screen is a string contract.
Native bridges cost more on one side than the other, which makes thin wrappers
tempting. Persistent storage holds stale data when the interface contract is
unclear.

---

## Example 1 — Native bridge interface: passthrough wrapper vs deep state machine

Candidate A is a literal copy of the native module:

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

Here is the complete interface comment:

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

The comment has twelve sentences. It describes ordering ("Call X first, then
Y") and platform-specific protocol. The "interface" is seven separate APIs
the caller must compose, plus platform quirks. The comment
test detects that failure.

Candidate B is the deep module:

```ts
type BiometricsState =
  | { status: 'unavailable'; reason: 'unsupported' | 'not_enrolled' | 'permanently_locked' }
  | { status: 'available' }
  | { status: 'locked'; retryAfter: Date };

type AuthResult =
  | { ok: true; signature?: string }
  | { ok: false; reason: 'user_cancelled' | 'failed' | 'locked' };

interface Biometrics {
  status(): Promise<BiometricsState>;
  prompt(opts: { reason: string; payload?: string }): Promise<AuthResult>;
}
```

Comment:

> Reports whether biometric auth can be used on this device and prompts
> the user when needed. status returns the current capability. prompt
> displays the system biometric UI and returns a typed result. If a
> payload is supplied, the result includes a signature bound to a
> per-device key (created lazily on first use).

The comment has four sentences. iOS/Android differences are gone from the
caller's view, because status's discriminator covers them. Key lifecycle,
Info.plist errors, and lockout handling are all inside the module. Common callers call
`prompt({ reason: 'Confirm payment' })` and switch on the result.

The guardrail check is whether anything caller-facing got hidden. The
caller still needs to know that a payload signature is per-device. So
sending the signature to the server is meaningful only if the server
trusts that device. One sentence in the comment states that fact. The
comment leaves out the fingerprint sensor's internal protocol.

---

## Example 2 — Navigation param contract: serializable identity vs full objects

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

Here is the interface comment for `ProductDetail`:

> Screen for a single product. product is the product to display.
> recommendations is the related-products list to render below the main
> view; if empty, the section is hidden. user is the current user, used
> to determine whether the wishlist button shows. Note that recommendations
> are computed at navigation time and become stale if the user remains on
> the screen for longer than a few minutes; the screen does not refetch.
> Note also that this screen is reachable via deep link, in which case
> recommendations will be empty and user will be the deep-link guest user;
> in that case the screen shows a "log in to see recommendations" CTA.

The comment has seven sentences. It describes the data flow into the screen
and what happens when each field is missing. The "interface" is leaking the structure of the
navigating screen's state and the staleness model. The deep-link case has
to be specially described because the contract was designed for the
in-app-navigation path.

The failure is that route params contain runtime state when they should contain only identity.

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

> Shows the detail screen for the product with this id. Loads the product and
> recommendations on mount via the products repository. Renders a guest
> view if the user is not signed in.

The comment has two sentences. The route now contains only identity, which
is what to show. Loading,
staleness, and signed-in-vs-guest are handled by the screen itself, which
reads `useAuth()` and a `useProduct(productId)` query. Deep links work
because the route is serializable and small.

The screen now uses identity in its route and queries (or context) for
everything else, such as auth, recommendations, and the current user. A
route should have that identity-only contract.

---

## Example 3 — Persistent storage module: untyped store vs typed accessor

Apps often start with this interface before they encapsulate storage:

```ts
interface Storage {
  get(key: string): Promise<string | null>;
  set(key: string, value: string): Promise<void>;
  delete(key: string): Promise<void>;
  clear(): Promise<void>;
}
```

Here is the complete comment:

> Wraps AsyncStorage. Values must be strings; serialize JSON yourself. Keys
> are conventionally namespaced with a colon (e.g., 'user:theme',
> 'feed:cache:v2'). When changing the layout of stored data, bump the key's
> version suffix (':v1' to ':v2') so old clients don't read corrupted data.
> clear() removes everything including auth tokens; use deleteSpecific keys
> on logout instead. The set() method does not validate value size; on
> Android a value over ~2MB throws on read (the SQLite CursorWindow limit)
> and the database has a configurable total cap. iOS has no comparable
> per-key limit.

The comment has six sentences. The "interface" is `get/set/delete/clear`,
but a caller must still learn the operational contract. That contract covers
JSON serialization, key namespacing, versioning, not clearing auth on logout,
and the Android size limit. Every screen that uses Storage must repeat
this knowledge.

The failure is that `Storage` is a wrapper around AsyncStorage with a
module's name. The domain knowledge (what's stored, in what layout, what
versions exist) belongs inside the module.

Redesign as typed accessors per domain:

```ts
// storage/userPrefs.ts
interface UserPrefs {
  hasSeenOnboarding(): Promise<boolean>;
  markOnboardingSeen(): Promise<void>;
  themePreference(): Promise<'light' | 'dark' | 'system'>;
  setThemePreference(v: 'light' | 'dark' | 'system'): Promise<void>;
}

// storage/feedCache.ts
interface FeedCache {
  load(): Promise<FeedItem[] | null>;
  save(items: FeedItem[]): Promise<void>;
  clear(): Promise<void>;
}

// storage/session.ts
interface Session {
  tokens(): Promise<Tokens | null>;
  save(t: Tokens): Promise<void>;
  clear(): Promise<void>;
}
```

Each module's interface comment is now two or three sentences. `UserPrefs`
handles its key schema and migration. `FeedCache` handles its versioning and the
Android size limits (it batches writes or drops oldest items if needed).
`Session` handles the secure-storage detail (`Session.save` writes to
Keychain/Keystore, because AsyncStorage is not encrypted). The screens that use these modules
don't know any of that.

Logout code now names each store to clear:

```ts
await Session.clear();
await FeedCache.clear();
// Logout deliberately keeps UserPrefs and onboarding
```

The orchestrating code now sets what to clear on logout
once, in one place. With `Storage.clear()` it was a side effect that could
include or exclude auth depending on whether some caller remembered to
multiRemove.

---

## Example 4 — Cross-cutting: screen-level data hook interface

The interface a screen consumes for its data is a recurring case where the
comment test finds problems early.

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

The comment has six sentences, describes invariants about combinations of
fields, and gives "treat X as Y" instructions. The hook returns five fields and
requires the caller to coordinate them.

Candidate B has a smaller interface and typed state:

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
> status discriminator names the three legal states. In the loaded state,
> actions holds the operations the current user is allowed to perform
> (an action absent from actions is not permitted). Action methods return
> Result so callers can surface failures without try/catch.

The comment has three sentences, and the contract improves in two places:

- The discriminator eliminates the "what does undefined mean" problem.
- Permissions move from "boolean per action" to "presence of the action in
  the actions object." A button that exists when permitted is impossible
  to render in the wrong state. A button that checks `permissions.canRefund`
  before calling `actions.refund` breaks if one if-statement is wrong.

The second change encodes "allowed" as presence of the action, so a parallel
boolean never exists. It is the kind of contract redesign the comment test
leads to. Writing "permissions may be undefined for an instant" is the
signal that the design is wrong.

---

## Platform notes

- **iOS/Swift, Android/Kotlin**: the same checks apply. A `ViewController` or
  `Fragment` accepting twelve init parameters costs a caller as much as the
  RN screen passing a `user` object through route params. Pass identity in,
  and get state through composition.
- **Flutter**: route params are arguments. The same
  identity-in/data-via-providers principle applies, with Riverpod or Provider as the context.
- **Native modules**: the bridge interface should hide the platform's
  protocol the way Example 1 does, regardless of which side you're writing
  on. A Swift `BiometricsBridge` that exposes `isAvailable`, `createKeys`,
  `authenticate` as separate methods is the same defect as a JS wrapper
  that does so.
