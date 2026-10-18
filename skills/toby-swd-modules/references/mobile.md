# Mobile

## Auth state

Passing `user` through navigation params forces every intermediate screen to accept a value it doesn't read. It also breaks deep links when the router serializes params, and leaves screens with a stale user after a token refresh. Put auth in an `AuthProvider` above `NavigationContainer` and read it with `useAuth()`. Give auth, theme, and feature flags separate contexts, and don't pass the user through Android `Intent` extras or iOS `UINavigationController` segues.

## Data access in screens

When each screen calls `fetch` with its own base URL, auth header, error handling, and retry, every change edits every screen. Put the feed calls in a `FeedRepo` that returns `Result<T>`, and give screens a `useFeed()` hook. Keep the small repository until several screens share server data, then adopt React Query, SWR, or RTK Query.
