# Web SPAs (React, Solid, Svelte)

This file covers memoization, virtualization, and render work in React, Solid, and Svelte. Open it when a web view is slow.

## Memoization

- Leave components unmemoized by default. Where the React Compiler runs, hand-written `useMemo` and `useCallback` are redundant. Solid and Svelte 5 track dependencies, so they need no hand-written memoization.
- Use `useMemo` for a computation a profile shows to be expensive, such as a fuzzy filter over thousands of items, and whose inputs change less often than the component renders.
- Use `useCallback` only for a callback passed to a memoized child or used in another hook's dependency array.
- Memoize an object prop only when the child that receives it is memoized.

When a component re-renders too often, fix the cause higher in the tree. Common causes are an unstable parent value, a context that changes every render, and unstable list keys.

## Virtualization

| Item count | Virtualize? |
|---|---|
| Under 100 | No |
| 100 to 1,000 | Only when measured |
| 1,000 to 10,000 | Likely, after measuring per-row cost |
| Over 10,000 | Yes |

A virtualization library brings scroll-position bugs, harder focus and sticky-row handling, and noisy snapshots. The browser's find in page also misses off-screen rows. When a list of 2,000 is slow, look first for an expensive per-row computation or an unsized image.

## Render work

Before memoizing a filter-and-sort in render, sort the data and lowercase its search fields once when it loads. Debounce the filter input by about 100 ms. Then memoize the remaining filter only if a profile still shows the filter as slow.
