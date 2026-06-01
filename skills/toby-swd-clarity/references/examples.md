# Worked Examples

Original code. The reasoning is what transfers.

---

## Example 1 — Backend: precision comment carries what the name cannot

```python
def trim(text, start, end):
    ...
```

The name and signature cannot answer the questions a caller actually has: is
`end` inclusive? what happens if `start > end`? are these byte offsets or
character indices? Self-documenting-code reasoning would stop here because the
names look fine. They are fine; the missing information has no place in code, so
it goes in the interface comment:

```python
def trim(text, start, end):
    """Return text[start:end] as characters (not bytes). end is exclusive.
    If start >= end the result is empty; both are clamped to [0, len(text)].
    Does not mutate text."""
```

Four sentences, no internals, every caller question answered. This is the
precision (lower-level) function of comments, the half most often skipped.

---

## Example 2 — Backend: the name-reuse bug, and the fix

A file-system module uses `block` for both a physical disk block and a logical
block within a file. The names look "reasonably close," so nobody questions
them, and a logical block number is eventually used where a physical one was
required — silent data corruption that took months to find.

Consistency rule: one name, one purpose. Rename to `fileBlock` and `diskBlock`
so the two cannot be confused at a glance, and better still give them distinct
types so they cannot be interchanged at all. The clarity fix here is also a
correctness fix; that is the usual pattern, not a coincidence.

---

## Example 3 — Frontend: event-driven code is the canonical non-obvious case

```tsx
useEffect(() => {
  reconcileCart();
}, [items, coupon, userTier]);
```

A reader scanning the component linearly never sees what triggers
`reconcileCart` or why those three dependencies. Event-driven invocation is
exactly the book's hidden-control-flow case; React effects are its modern form.
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

The "why userTier" note is the non-obvious dependency a future editor would
otherwise delete and reintroduce the bug.

---

## Example 4 — Frontend: generic container and state-shape comments

A hook returns a loosely shaped object:

```ts
return [data, err, l];   // caller does result[0], result[2]...
```

This is the generic-container failure: positional, unlabeled, meaning obscured.
Return a named shape, and comment the fields (data-structure-member comments,
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
live in the types; without the field comments a caller cannot use this
correctly, and no amount of good naming supplies them.

---

## Example 5 — Consistency: when in Rome

The codebase names handlers `handleSubmit`, `handleChange`, `handleRowClick`.
A new component is added with `onSaveClicked` and `submitHandler`. Each is
defensible in isolation; together they break the pattern that lets a reader
predict the next handler's name. Inspect the file, see the established
`handleX` form, and match it. Introducing a "better" handler-naming scheme is
worth it only with significant new information and a commit that converts every
existing handler — otherwise the half-and-half state is worse than either.
