# Worked Examples

---

## Example 1: Backend, a precision comment on a function

```python
def trim(text, start, end):
    ...
```

The name and signature cannot answer the questions a caller has: is
`end` inclusive? what happens if `start > end`? are these byte offsets or
character indices? The missing information cannot be expressed in code, so it
goes in the interface comment:

```python
def trim(text, start, end):
    """Return the slice of text from start to end, with end exclusive.

    Offsets count characters, so a multi-byte character counts as one.
    Both offsets are clamped to [0, len(text)].
    The result is empty when start >= end."""
```

The comment has four sentences and says nothing about how the function works inside. It answers each question above.

---

## Example 2: Backend, the name-reuse bug, and the fix

A file-system module uses `block` for both a physical disk block and a logical
block within a file. The names look "reasonably close," so readers do not question
them. A logical block number is eventually used where a physical one was
required. The result is silent data corruption that took months to find.

Rename to `fileBlock` and `diskBlock` so the two cannot be confused at a glance.
Better still, give them distinct types so they cannot be interchanged at all.

---

## Example 3: Frontend, comments on event-driven code

```tsx
useEffect(() => {
  reconcileCart();
}, [items, coupon, userTier]);
```

A reader scanning the component linearly never sees what triggers
`reconcileCart` or why it has those three dependencies. A React effect runs when its
dependencies change, so a reader cannot see when the effect runs by reading the code
from top to bottom. `comments.md` calls this hidden control flow. Put the comment
directly above the effect, where a reader first wonders why the effect runs:

```tsx
// This effect runs when the cart contents, the applied coupon, or the
// user's tier changes. userTier is in the list because a tier change
// changes the discount even when the items stay the same. Leaving it out
// caused BUG-2293.
useEffect(() => {
  reconcileCart();
}, [items, coupon, userTier]);
```

The "why userTier" note explains the non-obvious dependency, which a future
editor would otherwise delete and so reintroduce the bug.

---

## Example 4: Frontend, an unlabeled array and comments on each state

A hook returns an unlabeled array:

```ts
return [data, err, l];   // caller does result[0], result[2]...
```

The caller has to remember what each position in the array holds, because the
array has no labels. `comments.md` calls this a generic container.
Return a union with one variant per state, and comment what the type cannot show:

```ts
type UserQuery =
  | { status: "loading" }
  | { status: "ready"; user: User }
  | { status: "missing" }                  // The server returned 404.
  | { status: "failed"; error: ApiError }; // The request failed or returned 5xx.
```

The union rules out a user and an error at the same time, so no comment has to
list the valid combinations. The comments map each state to a server response,
which the type cannot show.
