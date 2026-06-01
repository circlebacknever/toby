# Worked Examples

Original code. The moves are what transfer.

---

## Example 1 — Backend: define the error out of existence

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
    """Ensure no session with sid exists. No-op if it already does not."""
    store.pop(sid, None)
```

The error case is gone, every call site loses its handler, and the function is
deeper. Guardrail check: does any caller need to know the session was already
absent? If one rare caller does, give it a separate query rather than keeping
the exception on the common path.

---

## Example 2 — Backend: aggregate, and know when to just crash

A web server's per-URL handlers each call `get_param(name)`, which throws when a
required parameter is missing. The tactical version wraps every `get_param` call
in its own try/except that returns a 400 — dozens of identical handlers.

Aggregate: let the exception propagate to the single dispatch loop at the top,
which catches it once and produces the 400. One handler replaces dozens.

Separately, the same server calls `malloc`-equivalent allocation deep in request
parsing. Out-of-memory is rare and there is nothing useful to do — checking it
at every allocation is pure complexity. This is the just-crash case: one checked
allocation wrapper that aborts with a diagnostic. Note the boundary: a corrupt
request body is *not* a crash case (it is expected and per-request) — it rides
the aggregation path to the 400.

---

## Example 3 — Frontend: stop the thousand cuts without premature optimization

A list view re-fetches the full dataset on every keystroke of a filter box, and
each row component re-derives a sorted copy of the list. No single line is
"slow"; together the view is sluggish.

The design-time move, not a measured micro-optimization: typing into a filter is
a known-expensive trigger if it crosses the network, so debounce the fetch and
filter client-side when the set is small — both are as simple as the slow
version and cost no extra complexity. The per-row re-sort is redundant work on a
known-hot path; lift the sorted derivation to the parent so it runs once. These
are naturally-efficient simple choices, the everyday layer, not a profiler
session.

If after this the view is still slow, then measure: baseline the render, change
one thing, re-measure, and revert anything with no measurable effect unless it
also simplified the component.

---

## Example 4 — Frontend: error masking taken too far

A data hook catches every fetch error and returns empty data:

```ts
try { return await api.getOrders(); }
catch { return []; }   // caller cannot distinguish "no orders" from "failed"
```

This masks information the caller truly needs: an empty list and a failed
request look identical, so the UI cannot show a retry state and silently lies to
the user. Masking is correct only when the information is not needed outside the
module; here it is needed. Surface it as part of the contract instead — a result
that distinguishes loaded-empty from failed — even though that adds to the
hook's interface. The interface cost is the point: callers need this, so it must
be exposed.
