# Mobile (React Native, with notes for native iOS/Android)

## Auth state

Passing `user` through navigation params makes every intermediate screen take a value it does not read. It also breaks deep links, because params are serialized, and leaves screens with a stale user after a token refresh. Put auth in an `AuthProvider` above `NavigationContainer` and read it with `useAuth()`. Give auth, theme, and feature flags separate contexts, because one `RootContext` holding all three has every problem of a catch-all base class. The same rule applies to `Intent` extras and `UINavigationController` segues.

## Data access in screens

When each screen calls `fetch` with its own base URL, auth header, error handling, and retry, every change edits every screen. Put the feed calls in a `FeedRepo` that returns `Result<T>`, and give screens a `useFeed()` hook. Adopt React Query, SWR, or RTK Query once several screens share server data. Below that, the small repository is enough.
