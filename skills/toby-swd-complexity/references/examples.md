# Worked Examples

The code below is original. The techniques it shows apply to other code.

---

## Example 1 — Backend: redefine the function so the error cannot happen

```python
def remove_session(store, sid):
    if sid not in store:
        raise KeyError(sid)   # callers now wrap every call in try/except
    del store[sid]
```

Most callers call this to make sure a session is gone, often after a partial
failure where they cannot know if it exists. The exception forces a try/except
at every site. Redefine the semantics from "delete it, fail if absent" to
"ensure it is absent":

```python
def remove_session(store, sid):
    """Ensure no session with sid exists. Do nothing if it is already absent."""
    store.pop(sid, None)
```

The error case is gone, so every call site can delete its handler. The function is also
deeper. Check whether any caller needs to know the session was already
absent. If one rare caller does, give it a separate query and keep the common
path exception-free.

---

## Example 2 — Backend: aggregate, and know when to just crash

A web server's per-URL handlers each call `get_param(name)`, which throws when a
required parameter is missing. The tactical version wraps every `get_param` call
in its own try/except that returns a 400. That produces dozens of identical
handlers.

Aggregate the handling in one place. Let the exception propagate to the single dispatch loop at the top,
which catches it once and produces the 400. That one handler replaces the dozens of per-call handlers.

Separately, the same server calls a `malloc`-equivalent allocator many call levels down in request
parsing. Out-of-memory is rare. When it happens there is nothing useful to do, so checking it
at every allocation is pure complexity. Out-of-memory is a case where the program should crash, so
use one checked allocation wrapper that aborts with a diagnostic. A corrupt
request body is expected and per-request, so the aggregated handler turns it into
the 400, and it does not trigger the abort.

---

## Example 3 — Frontend: prevent many small slowdowns at design time

A list view re-fetches the full dataset on every keystroke of a filter box. Also,
each row component re-derives a sorted copy of the list. No single line is
"slow", but together they make the view sluggish.

Make the design-time changes before any measurement. Typing into a filter is
known to be expensive when each keystroke makes a network request. Debounce the fetch and
filter client-side when the set is small. Both are as simple as the slow
version.

The per-row re-sort is redundant work on a
known-hot path. Lift the sorted derivation to the parent so it runs once. The
debounce and the lifted sort are naturally efficient and simple, and they come
before any profiler session.

If the view is still slow after these changes, measure it. Baseline the render, change
one thing, and re-measure. Revert anything with no measurable effect unless it
also simplified the component.

---

## Example 4 — Frontend: error masking taken too far

A data hook catches every fetch error and returns empty data:

```ts
try { return await api.getOrders(); }
catch { return []; }   // caller cannot distinguish "no orders" from "failed"
```

This masks information the caller needs, because an empty list and a failed
request look identical. The UI cannot show a retry state, so it gives false information to
the user. Masking is correct only when the information is not needed outside the
module. Here the caller needs it.

Surface the failure as part of the contract,
with a result that distinguishes loaded-empty from failed. That result adds to
the hook's interface. The hook accepts that cost on purpose, because callers
need the distinction.
