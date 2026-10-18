# Worked Examples

This file shows worked cases for defining an error out of existence, aggregating error handling, and avoiding over-masking.

---

## 1. Redefining the contract

```python
def remove_session(store, sid):
    if sid not in store:
        raise KeyError(sid)  # Forces every caller to wrap the call in try/except.
    del store[sid]
```

Callers invoke `remove_session` to ensure a session is gone after logout or a partial failure. Redefine the contract from "delete and raise if absent" to "ensure the session is absent":

```python
def remove_session(store, sid):
    """Ensure no session with sid exists. Do nothing if it is already absent."""
    store.pop(sid, None)
```

Every caller drops its `try/except` block. In the same way, "throw if slice indices are out of range" becomes "return the overlapping slice, or an empty slice when out of range."

---

## 2. Aggregating handlers

A web server's route handlers each call `get_param(name)`, which raises when a required parameter is missing. Catching that exception in every route duplicates the same 400 handler dozens of times.

Let `MissingParamError` propagate to one request-dispatch middleware that catches it once and returns `400 Bad Request`. By contrast, when a low-level allocator hits out-of-memory, callers can't recover, so check it inside one allocation wrapper that logs diagnostics and aborts the process.

---

## 3. Over-masking

A frontend data hook catches every fetch failure and returns an empty array:

```ts
try { return await api.getOrders(); }
catch { return []; } // The caller can't tell an empty order list from a failed request.
```

Because an empty list and a network outage return the same value, the screen renders "You have 0 orders" during an outage. Return a tagged union that distinguishes `loaded` (with `[]`) from `failed` so the caller can show a retry state.
