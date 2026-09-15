# Worked Examples

The code below is original. The reasoning applies to other code too.

---

## Example 1 — Backend: a precision comment on a function

```python
def trim(text, start, end):
    ...
```

The name and signature cannot answer the questions a caller has: is
`end` inclusive? what happens if `start > end`? are these byte offsets or
character indices? A developer who believes code documents itself would stop
here, because the names look fine. The names are fine. The missing information
cannot be expressed in code, so it goes in the interface comment:

```python
def trim(text, start, end):
    """Return the slice of text from start to end.

    Offsets count characters, so a multi-byte character counts as one.
    The end offset is exclusive. Both offsets are clamped to [0, len(text)].
    The result is empty when start >= end. The function does not change text."""
```

The comment has six sentences and no internals. It answers every question a
caller has. It is a precision (lower-level) comment, the half most often skipped.

---

## Example 2 — Backend: the name-reuse bug, and the fix

A file-system module uses `block` for both a physical disk block and a logical
block within a file. The names look "reasonably close," so readers do not question
them. A logical block number is eventually used where a physical one was
required. The result is silent data corruption that took months to find.

The consistency rule gives each name one purpose. Rename to `fileBlock` and `diskBlock`
so the two cannot be confused at a glance. Better still, give them distinct
types so they cannot be interchanged at all. The clarity fix here is also a
correctness fix. Treat a confusable name as seriously as a value that can be
confused.

---

## Example 3 — Frontend: comments on event-driven code

```tsx
useEffect(() => {
  reconcileCart();
}, [items, coupon, userTier]);
```

A reader scanning the component linearly never sees what triggers
`reconcileCart` or why it has those three dependencies. React effects are the modern form of
event-driven invocation, which is the hidden-control-flow case.
Document at the point of surprise:

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

## Example 4 — Frontend: generic container and state-layout comments

A hook returns an unlabeled array:

```ts
return [data, err, l];   // caller does result[0], result[2]...
```

This return value is the generic-container failure, because its values are
positional and unlabeled, which hides their meaning.
Return a named type, and comment the fields (data-structure-member comments,
the category most often missed on frontend state):

```ts
interface UserQuery {
  user: User | null;   // This is null while loading and after a failed fetch.
  error: ApiError | null;  // This is set only when the request fails. A 404 leaves it null.
  loading: boolean;    // This is true from mount until the first response arrives.
}
return result;
```

The types cannot say that a 404 leaves `error` null, or that `user` is null while
loading. Without the field comments a caller cannot use `UserQuery`
correctly. Good naming cannot supply that information.

---

## Example 5 — Consistency: matching local handler names

The codebase names handlers `handleSubmit`, `handleChange`, `handleRowClick`.
A new component is added with `onSaveClicked` and `submitHandler`. Each is
defensible in isolation. Together they break the pattern that lets a reader
predict the next handler's name.

Inspect the file, see the established
`handleX` form, and match it. Introducing a new handler-naming scheme is
worth it only with significant new information and a commit that converts every
existing handler. Otherwise the half-and-half state is worse than either naming scheme alone.
