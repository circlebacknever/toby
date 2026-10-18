# Worked Examples

---

## 1. Function docstring with bounds and units

```python
def trim(text, start, end):
    ...
```

The signature alone doesn't say whether `end` is inclusive, what happens when `start > end`, or whether offsets count bytes or characters. Put those rules in the docstring:

```python
def trim(text, start, end):
    """Return the slice of text from start to end, with end exclusive.

    Offsets count characters, so a multi-byte character counts as one.
    Clamps both offsets to [0, len(text)].
    Returns an empty string when start >= end."""
```

The docstring is four sentences, states the exact contract, and mentions no internal steps.

---

## 2. Distinct names for distinct concepts

When a file-system module uses `block` for both a logical file block and a physical disk block, a caller eventually passes a file block number where a function expects a disk block number. Rename them to `fileBlock` and `diskBlock`, and wrap each in a distinct type so callers can't swap them.

---

## 3. Commenting why an effect runs

```tsx
// Runs when the cart contents, applied coupon, or user tier changes.
// userTier is required because a tier change alters the discount even
// when items stay the same (BUG-2293).
useEffect(() => {
  reconcileCart();
}, [items, coupon, userTier]);
```

Without the comment explaining `userTier`, a future editor can remove `userTier` from the dependency array and reintroduce the bug.

---

## 4. Tagged union in place of an unlabeled array

A hook that returns `return [data, err, l]` forces callers to remember array positions and which combinations are valid. Return a tagged union with named fields and comment what each server state means:

```ts
type UserQuery =
  | { status: "loading" }
  | { status: "ready"; user: User }
  | { status: "missing" }                  // The server returned 404.
  | { status: "failed"; error: ApiError }; // The request failed or returned 5xx.
```
