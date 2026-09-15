# Worked Examples — Mobile (React Native, with notes for native iOS/Android)

Most frontend principles apply to mobile, which also adds three native concerns
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

`user` is a pass-through variable, the same defect as web prop drilling (the different-layer check), with
extra hazards specific to navigation:

- React Navigation params are serialized, so passing a complex `user` object
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
  // handles loading from secure storage on mount, refresh, sign-in, and sign-out
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

// Any screen that needs the user calls useAuth:
const { user } = useAuth();
```

Routes contain only what identifies the destination (an `orderId`, a `tab`).
Identity is a separate concern handled by one module. The intermediate screens
no longer take the prop. Deep linking works because routes are now
serializable without extra object handling.

Do not put everything in the context. Auth is one well-defined body of
knowledge, theme is another, and feature flags are a third. A `RootContext`
holding all of them is the god-context anti-pattern, which has the same problem
as a base class with everything.

---

## Example 2 — AsyncStorage calls scattered across screens

Growing RN codebases often end up with this code:

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

This code fails the information-leakage check. The decision "what key holds the feed
cache, what format it's stored in, what version it is" is repeated in two
modules (`FeedScreen` and `LogoutFlow`). The same applies to theme prefs, auth
tokens, onboarding flags. Changing a key requires editing every site that
touched it. `LogoutFlow` will go out of date with every new key.

A typed storage module handles these decisions:

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
// logout deliberately keeps theme prefs and onboarding
```

Keys, versions, JSON schemas, and migration concerns are inside each module.
Screens call `FeedCache.load()` without knowing what key was used. Logout calls
`clear()` on each module that stores data, so the question "what should be cleared
on logout" becomes a deliberate policy. Today the result depends on which screens'
authors remembered to call `multiRemove`.

---

## Example 3 — Native bridge as a deep module

A team adds barcode scanning, starting with this wrapper around a native module:

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

`BarcodeNative` is a pass-through wrapper (the different-layer and depth checks). It does almost nothing except
expose the platform API verbatim. The screen now handles the protocol of requesting
permission, setting the camera, subscribing, starting, and stopping on unmount.
Every screen that scans repeats that protocol. iOS and Android differences in permission semantics
leak through to every caller.

A deep barcode module handles the protocol:

```tsx
// scanning/useBarcodeScanner.ts
export function useBarcodeScanner(opts: { onCode: (c: string) => void }) {
  const [state, setState] = useState<'idle'|'denied'|'scanning'|'error'>('idle');

  useEffect(() => {
    let cancelled = false;
    let teardown = () => {};
    (async () => {
      const granted = await ensurePermission();           // handles iOS and Android permission differences
      if (cancelled) return;
      if (!granted) { setState('denied'); return; }
      const sub = subscribe(opts.onCode);
      await startNative({ camera: 'rear' });
      teardown = () => { sub.remove(); stopNative(); };
      if (cancelled) { teardown(); return; }              // the component unmounted while the scanner was starting
      setState('scanning');
    })();
    // The effect must return the cleanup. A teardown returned from the async function
    // resolves the promise instead. React never runs it, so the camera leaks.
    return () => { cancelled = true; teardown(); };
  }, []);

  return { state };
}

// ScanScreen.tsx
const { state } = useBarcodeScanner({ onCode: handleCode });
```

The screen calls a single hook to start the operation and renders from the state it returns. The protocol
is inside the module, where iOS-vs-Android permission flow, camera index
defaults, and torch-availability checks can all be handled without callers
knowing. Adding a second scanning screen takes one line.

The same treatment applies to other bridges: location, push notifications,
biometrics, file pickers. Each bridge is one body of knowledge, namely the
platform's contract for that capability. A deep module hides that protocol
behind a small caller-facing interface.

---

## Example 4 — Per-screen network state

Scattered data access produces per-screen network code like this:

```tsx
// FeedScreen.tsx
const [items, setItems] = useState<FeedItem[]>([]);
const [loading, setLoading] = useState(true);
useEffect(() => {
  fetch(`${API}/feed`, { headers: { Authorization: `Bearer ${token}` }})
    .then(r => r.json())
    .then(j => { setItems(j.items); setLoading(false); });
}, []);

// SearchScreen.tsx makes the same call with a different state type and different error handling
const [results, setResults] = useState([]);
useEffect(() => {
  fetch(`${API}/feed?q=${query}`, { headers: { Authorization: `Bearer ${token}` }})
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(j => setResults(j.items))
    .catch(e => Sentry.captureException(e));
}, [query]);
```

The same decisions (base URL, auth header, error semantics, retry, offline
behavior) are repeated in every screen that touches the feed. The two files
contain five forms of information leakage.

A feed repository defines the contract:

```tsx
// feed/repository.ts
export const FeedRepo = {
  async list(): Promise<Result<FeedItem[]>> { ... },
  async search(q: string): Promise<Result<FeedItem[]>> { ... },
  async refresh(): Promise<void> { ... },
};

// FeedScreen.tsx
const { data, loading, error, refresh } = useFeed();   // useFeed is a hook that calls FeedRepo
```

Every caller handles one type, `Result<T>`, which covers success, failure, and offline. Auth
header, base URL, retry policy, and offline cache are inside `FeedRepo`. The
two screens now contain only rendering code.

For larger apps this is what React Query / SWR / RTK Query are designed for.
They provide the deep module so you don't have to build it from scratch. Use
them when the amount of data access justifies it, and build the lightweight repository when
it doesn't. The wrong move is to keep `fetch` calls scattered through screens.

---

## Platform notes

- **iOS/Swift, Android/Kotlin**: the same checks apply. Keep auth state in a
  shared store. Threading it through `Intent` extras or `UINavigationController`
  segues repeats the same defect. Native modules wrap the platform's protocol.
  ViewControllers and Activities are thin and stateful only about their own UI.
- **Flutter/Dart**: provider/riverpod is the equivalent of context here.
  `InheritedWidget` is a low-level primitive that most apps should use only
  through one of those wrappers.
- **Implementation inheritance in mobile native code** (extending
  `UIViewController`, `Activity`, `Fragment`) needs the same caution as the composition-over-inheritance check. The
  framework requires one or two override points, so do not build a deep class
  hierarchy on top of them for "shared behavior."
