# Mobile

## Native bridge

A wrapper that re-exports seven `RNBiometrics` methods needs a nine-sentence comment stating the required call order and iOS/Android quirks. Hide that sequence behind two methods:

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

> Reports whether the device supports biometric auth and prompts the user when needed. status returns the current capability. prompt displays the system biometric UI and returns a typed result. When the caller supplies a payload, the result includes a signature from a per-device key that the module creates on first use.

Creating and deleting the signing key, the `Info.plist` entry, and lockout handling stay inside the module. Design a Swift or Kotlin bridge the same way, with two calls, typed results, and platform steps hidden inside.

## Route params

The navigation library serializes route params, persists them across reloads, and fills them from deep links, so pass only ids in route params:

```ts
type RootStackParamList = {
  ProductDetail: { productId: string };
  Checkout: { cartId: string };
};
```

> Shows the detail screen for the product with this id. Loads the product and recommendations on mount via the products repository. Renders a guest view if the user isn't signed in.

With an id, the screen reads `useProduct(productId)` and `useAuth()`, and deep links work unchanged.

## Storage

A `get`/`set`/`delete`/`clear` wrapper over AsyncStorage makes each caller handle JSON, key names, version suffixes, and the Android size limit. Give each kind of stored data its own typed module:

```ts
interface UserPrefs {
  themePreference(): Promise<'light' | 'dark' | 'system'>;
  setThemePreference(v: 'light' | 'dark' | 'system'): Promise<void>;
}
interface FeedCache { load(): Promise<FeedItem[] | null>; save(items: FeedItem[]): Promise<void>; clear(): Promise<void>; }
interface Session   { tokens(): Promise<Tokens | null>; save(t: Tokens): Promise<void>; clear(): Promise<void>; }
```

`Session.save` writes to Keychain or Keystore, because AsyncStorage isn't encrypted. `FeedCache` handles its version suffix and the size limit. Logout calls `Session.clear()` and `FeedCache.clear()` and keeps `UserPrefs`, so the list of data that logout clears stays in one file.

## Screen data hook

A hook that returns `data`, `loading`, `error`, `isRefetching`, and `canX` flags needs rules such as "treat undefined as not allowed." Return one state per valid combination:

```ts
type OrderScreenState =
  | { status: 'loading' }
  | { status: 'error'; error: Error }
  | { status: 'loaded'; order: Order; actions: OrderActions };
```

`actions` contains only the actions the current user may perform, so the screen can't show an action that the handler rejects. Each action returns `Result`, so callers don't need a `try/catch`.
