# Web SPAs

## Server state

When each page fetches in `useEffect` with its own loading, error, and cancellation code, a change to error handling edits every page. Use TanStack Query or SWR to handle caching, deduping, retries, and focus refetches, and keep components to rendering. When a page refetches after an input changes (such as sort order), include that input in the `cache key` or ignore stale responses.

## Shared behavior

Share behavior as a function the component calls: a `use*` hook in React, a `create*` function in Solid, or a rune-based factory in Svelte 5. Avoid higher-order component wrappers, because stacking wrappers hides which props the component accepts.

## Store slices

A single global store that holds user, theme, cart, coupon, and notifications exposes its whole state layout to every component. Give each area of state its own slice, and make that slice's methods enforce its rules:

```tsx
export const useCart = create<CartState>((set, get) => ({
  items: [],
  coupon: null,
  add(item) {
    if (get().items.some((i) => i.id === item.id)) return;   // no duplicates
    set((s) => ({ items: [...s.items, item] }));
  },
  remove(id) { set((s) => ({ items: s.items.filter((i) => i.id !== id) })); },
  total(): number { /* computes from items and coupon */ },
}));
export const useAuth = create<AuthState>((set) => ({ ... }));
```

Split slices by domain area (auth, cart, theme, wishlist) so components import only the slice they read. In Zustand, read a derived method through a selector that calls it (`useCart((s) => s.total())`), because selecting `s.total` or calling `getState().total()` in render doesn't subscribe to updates.

## Headless components

When a component gains 20 props by mixing keyboard, selection, and ARIA state with styling, move the state logic into a headless hook and let each component render its own markup. Use Radix, Headless UI, or Melt UI before writing a custom headless hook.
