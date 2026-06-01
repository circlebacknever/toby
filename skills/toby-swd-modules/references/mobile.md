# Worked Examples — Mobile (React Native, with notes for native iOS/Android)

Mobile shares most of the frontend principles but adds three native concerns
that web React doesn't have: navigation state across screens, persistent
storage, and bridges to platform APIs. Each is a common source of leakage and
shallow modules.

---

## Example 1 — Auth state threaded through nav params

A four-tab app passes the current user through navigation:

```tsx
// LoginScreen.tsx
navigation.navigate('Home', { user });

// HomeScreen.tsx
function HomeScreen({ route, navigation }) {
  const { user } = route.params;
  return <Tabs user={user} navigation={navigation} />;
}

// Tabs.tsx
function Tabs({ user, navigation }) {
  return (
    <Tab.Navigator>
      <Tab.Screen name="Feed" component={Feed} initialParams={{ user }} />
      <Tab.Screen name="Profile" component={Profile} initialParams={{ user }} />
      <Tab.Screen name="Settings" component={Settings} initialParams={{ user }} />
    </Tab.Navigator>
  );
}
// ...every screen takes `user` in its route.params and forwards it deeper
```

Same defect as web prop drilling (Check 4) — pass-through variable — with
extra hazards specific to navigation:

- React Navigation params are serialized; passing a complex `user` object
  through them silently breaks deep links and state restoration.
- Screens that don't use `user` still take it, because nested screens below
  them do.
- A token refresh requires re-navigating with new params or every screen reads
  a stale `user`.

Fix with a context provider at the navigation root:

```tsx
// AuthContext.tsx
const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: PropsWithChildren) {
  const [user, setUser] = useState<User | null>(null);
  // owns: load from secure storage on mount, refresh, sign-in, sign-out
  return <AuthContext.Provider value={{ user, signIn, signOut }}>{children}</AuthContext.Provider>;
}

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth outside AuthProvider');
  return ctx;
};

// App.tsx
<AuthProvider>
  <NavigationContainer>...</NavigationContainer>
</AuthProvider>

// Any screen that needs it:
const { user } = useAuth();
```

Routes carry only what identifies the destination (an `orderId`, a `tab`).
Identity is a separate concern owned by one module. The intermediate screens
lose the prop entirely; deep linking works because routes are now serializable
without object juggling.

Guardrail: don't pile the context with everything. Auth is one well-defined
body of knowledge; theme is another; feature flags a third. A `RootContext`
holding all of them is the god-context anti-pattern — same problem as a base
class with everything.

---

## Example 2 — AsyncStorage calls scattered across screens

A common drift in growing RN codebases:

```tsx
// OnboardingScreen.tsx
await AsyncStorage.setItem('hasSeenOnboarding', 'true');

// FeedScreen.tsx
const cached = await AsyncStorage.getItem('feed:cache:v2');
const parsed = cached ? JSON.parse(cached) : null;
// ...
await AsyncStorage.setItem('feed:cache:v2', JSON.stringify(items));

// SettingsScreen.tsx
const themePref = await AsyncStorage.getItem('user.theme.preference') ?? 'system';

// LogoutFlow.ts
await AsyncStorage.multiRemove(['authToken', 'refreshToken', 'feed:cache:v2', 'user.theme.preference']);
```

Information-leakage check (Check 2). The decision "what key holds the feed
cache, what shape it's stored in, what version it is" is reflected in two
modules (`FeedScreen` and `LogoutFlow`). The same applies to theme prefs, auth
tokens, onboarding flags. Changing a key requires editing every site that
touched it, and `LogoutFlow` is destined to drift behind every new key.

A typed storage module owns these decisions:

```tsx
// storage/userPrefs.ts
export const UserPrefs = {
  async hasSeenOnboarding() { ... },
  async markOnboardingSeen() { ... },
  async themePreference(): Promise<'light' | 'dark' | 'system'> { ... },
  async setThemePreference(v: ...) { ... },
};

// storage/feedCache.ts
export const FeedCache = {
  async load(): Promise<FeedItem[] | null> { ... },
  async save(items: FeedItem[]): Promise<void> { ... },
  async clear(): Promise<void> { ... },
};

// storage/session.ts
export const Session = {
  async tokens(): Promise<Tokens | null> { ... },
  async save(t: Tokens): Promise<void> { ... },
  async clear(): Promise<void> { ... },
};

// LogoutFlow.ts
await Session.clear();
await FeedCache.clear();
// theme prefs and onboarding deliberately survive logout
```

Keys, versions, JSON schemas, and migration concerns live inside each module.
Screens call `FeedCache.load()` and don't know what key was used. Logout asks
each owning module to clear its data and the question "what should be cleared
on logout" becomes a deliberate policy, not an accident of which screens
remembered to use `multiRemove`.

---

## Example 3 — Native bridge as a deep module, not a thin pass-through

A team adds barcode scanning. Initial wrapper around a native module:

```tsx
// BarcodeNative.ts
import { NativeModules } from 'react-native';

export const BarcodeNative = {
  startScanner: NativeModules.BarcodeScanner.startScanner,
  stopScanner: NativeModules.BarcodeScanner.stopScanner,
  setCameraIndex: NativeModules.BarcodeScanner.setCameraIndex,
  onScanned: NativeModules.BarcodeScanner.onScanned,
  isTorchAvailable: NativeModules.BarcodeScanner.isTorchAvailable,
  toggleTorch: NativeModules.BarcodeScanner.toggleTorch,
  requestPermission: NativeModules.BarcodeScanner.requestPermission,
};
```

Then screens use it directly:

```tsx
// ScanScreen.tsx
useEffect(() => {
  (async () => {
    const granted = await BarcodeNative.requestPermission();
    if (!granted) return setError('camera-denied');
    await BarcodeNative.setCameraIndex(0);
    BarcodeNative.onScanned((code) => { ... });
    await BarcodeNative.startScanner();
  })();
  return () => { BarcodeNative.stopScanner(); };
}, []);
```

This is a pass-through wrapper (Check 4, Check 8). It does almost nothing but
expose the platform API verbatim. The screen now owns the protocol — request
permission, set camera, subscribe, start, stop on unmount — and every screen
that scans repeats it. iOS and Android differences in permission semantics
leak through to every caller.

A deep barcode module owns the protocol:

```tsx
// scanning/useBarcodeScanner.ts
export function useBarcodeScanner(opts: { onCode: (c: string) => void }) {
  const [state, setState] = useState<'idle'|'denied'|'scanning'|'error'>('idle');

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const granted = await ensurePermission();           // owns iOS/Android nuance
      if (cancelled) return;
      if (!granted) { setState('denied'); return; }
      const sub = subscribe(opts.onCode);
      await startNative({ camera: 'rear' });
      setState('scanning');
      return () => { sub.remove(); stopNative(); };
    })();
    return () => { cancelled = true; };
  }, []);

  return { state };
}

// ScanScreen.tsx
const { state } = useBarcodeScanner({ onCode: handleCode });
```

One hook, one operation, one piece of state to render against. The protocol
lives inside the module, where iOS-vs-Android permission flow, camera index
defaults, and torch-availability checks can all be handled without callers
knowing. Adding a second scanning screen takes one line.

The same shape applies to other bridges: location, push notifications,
biometrics, file pickers. Each is one body of knowledge — the platform's
contract for that capability — and a deep module hides the protocol behind a
small caller-facing interface.

---

## Example 4 — Per-screen network state instead of a repository

A symptom of scattered data access:

```tsx
// FeedScreen.tsx
const [items, setItems] = useState<FeedItem[]>([]);
const [loading, setLoading] = useState(true);
useEffect(() => {
  fetch(`${API}/feed`, { headers: { Authorization: `Bearer ${token}` }})
    .then(r => r.json())
    .then(j => { setItems(j.items); setLoading(false); });
}, []);

// SearchScreen.tsx (different shape, same call, different error handling)
const [results, setResults] = useState([]);
useEffect(() => {
  fetch(`${API}/feed?q=${query}`, { headers: { Authorization: `Bearer ${token}` }})
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(j => setResults(j.items))
    .catch(e => Sentry.captureException(e));
}, [query]);
```

The same decisions (base URL, auth header, error semantics, retry, offline
behavior) are repeated in every screen that touches the feed — five forms of
information leakage in one file pair.

A feed repository owns the contract:

```tsx
// feed/repository.ts
export const FeedRepo = {
  async list(): Promise<Result<FeedItem[]>> { ... },
  async search(q: string): Promise<Result<FeedItem[]>> { ... },
  async refresh(): Promise<void> { ... },
};

// FeedScreen.tsx
const { data, loading, error, refresh } = useFeed();   // a hook over FeedRepo
```

`Result<T>` is one shape every caller handles — success, failure, offline. Auth
header, base URL, retry policy, and offline cache live inside `FeedRepo`. The
two screens shrink to rendering code.

For larger apps this is what React Query / SWR / RTK Query are designed for —
they provide the deep module so you don't have to build it from scratch. Use
them when the surface justifies it; build the lightweight repository when it
doesn't. The wrong move is to keep `fetch` calls scattered through screens.

---

## Platform notes

- **iOS/Swift, Android/Kotlin**: the same checks apply. Auth state in a
  shared store, not threaded through `Intent` extras or `UINavigationController`
  segues. Native modules wrap the platform's protocol; ViewControllers and
  Activities are thin and stateful only about their own UI.
- **Flutter/Dart**: provider/riverpod plays the role of context here.
  `InheritedWidget` directly is the low-level primitive most apps shouldn't use
  except through one of those wrappers.
- **Implementation inheritance in mobile native code** (extending
  `UIViewController`, `Activity`, `Fragment`): same caution as Check 5. The
  framework demands one or two override points; resist building a deep family
  tree on top of those for "shared behavior."
