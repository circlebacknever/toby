# Worked Examples

The code below is original, and the reasoning applies to other code.

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
    """Return text[start:end] as characters (not bytes). end is exclusive.
    If start >= end the result is empty; both are clamped to [0, len(text)].
    Does not mutate text."""
```

The comment has four sentences and no internals, and it answers every caller
question. It is a precision (lower-level) comment, the half most often skipped.

---

## Example 2 — Backend: the name-reuse bug, and the fix

A file-system module uses `block` for both a physical disk block and a logical
block within a file. The names look "reasonably close," so nobody questions
them. A logical block number is eventually used where a physical one was
required, and the result is silent data corruption that took months to find.

The consistency rule gives each name one purpose. Rename to `fileBlock` and `diskBlock`
so the two cannot be confused at a glance, and better still give them distinct
types so they cannot be interchanged at all. The clarity fix here is also a
correctness fix. Treat a name that can be confused as a value that can be
confused.

---

## Example 3 — Frontend: comments on event-driven code

```tsx
useEffect(() => {
  reconcileCart();
}, [items, coupon, userTier]);
```

A reader scanning the component linearly never sees what triggers
`reconcileCart` or why it has those three dependencies. Event-driven invocation
is the hidden-control-flow case, and React effects are its modern form.
Document at the point of surprise:

```tsx
// Runs whenever the cart contents, the applied coupon, or the user's tier
// changes. userTier is included because tier-based discounts must be
// recomputed on tier change even if items did not change — omitting it was
// the cause of BUG-2293.
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
  user: User | null;   // null while loading or after a failed fetch
  error: ApiError | null;  // set only on transport/HTTP failure, never on 404
  loading: boolean;    // true from mount until the first response settles
}
return result;
```

The `error is never set on 404` and `null while loading or failed` facts cannot
be expressed in the types. Without the field comments a caller cannot use `UserQuery`
correctly, and no amount of good naming supplies them.

---

## Example 5 — Consistency: matching local handler names

The codebase names handlers `handleSubmit`, `handleChange`, `handleRowClick`.
A new component is added with `onSaveClicked` and `submitHandler`. Each is
defensible in isolation. Together they break the pattern that lets a reader
predict the next handler's name. Inspect the file, see the established
`handleX` form, and match it. Introducing a new handler-naming scheme is
worth it only with significant new information and a commit that converts every
existing handler. Otherwise the half-and-half state is worse than either.
