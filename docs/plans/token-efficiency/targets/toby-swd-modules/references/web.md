# Web SPAs (React, Solid, Svelte)

## Server state

When each page fetches in `useEffect` with its own loading, error, and cancellation code, a change to error handling edits every page. Use TanStack Query or SWR, which handle caching, deduping, retry, and refetch on focus, and keep components to rendering. Write your own fetch layer only for a stated reason.

## Shared behavior

Share behavior as a function the component calls: a `use*` hook in React, a `create*` function in Solid, or a rune-based factory in Svelte 5. A higher-order component injects props a reader cannot see in the component's file, and three stacked wrappers hide its real interface.

## Store slices

A single global store that holds user, theme, cart, coupon, and notifications exposes its whole state layout to every component. Give each body of knowledge its own slice whose methods keep its invariants:

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

A wishlist gets a new slice and leaves the others unchanged. Slice by knowledge boundary such as auth, cart, and theme, because one slice per field makes every component import six. Zustand does not track a derived method, so read it through a selector that calls it, `useCart((s) => s.total())`. Selecting `s.total`, or calling `useCart.getState().total()` in render, does not subscribe and shows a stale value. Solid's `createStore` and Svelte's `derived` track the read.

## Headless components

A combobox that gained 20 props mixes behavior, meaning keyboard, selection, ARIA, and open state, with presentation. Put the behavior in one headless hook and let each `ProductCombobox` or `TagCombobox` render its own markup. Adopt Radix, Headless UI, or Melt UI before writing one.
