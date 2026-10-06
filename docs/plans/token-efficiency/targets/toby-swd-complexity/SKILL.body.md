# Toby SWD Complexity

For error handling and for performance work, reduce the number of places that must contain the extra logic.

Every special case a caller must branch on is complexity. Treat creating one as a design smell first. Merge it into the general case so callers do not have to know it exists.

Put the rules for shared mutable state and the ordering of concurrent tasks in one module, so call sites hold no locks or ordering assumptions.

## Error design

Count the handling a new error signal forces at every level between the failure and the code that can act on it. An error signal is a thrown exception, an error return, a status code, a `Result`, or an `Option`. Work through these four steps in order and stop at the first one that applies.

1. **Define the error out of existence.** Before writing any handling, ask whether the operation's semantics can be redefined so the condition is no longer an error. "Delete this variable, fail if absent" becomes "ensure this variable no longer exists." "Throw if an index is out of range" becomes "return the overlap, empty if none." Redefine the semantics only when the condition needs no response, and keep the error when a reported success would hide a bug.

2. **Mask it at the lowest level.** If a low-level module can fully handle the condition without the caller ever knowing, handle it there. Transient errors include a network blip, a database deadlock, and a rate-limit response. Put a bounded retry for them inside the module, so the caller sees success. Retry only an operation that is safe to repeat, which means an idempotent one or one with an idempotency key the server dedupes on.

3. **Aggregate.** When the error must surface, let it propagate to one handler, such as the top of a request loop, and remove the per-call-site handlers. When that handler replies to an untrusted caller, return the error category the caller needs and log the detail. The reply contains no stack trace, internal identifier, or query text.

4. **Stop in the safest reachable state.** No caller can act on resource exhaustion, unrecoverable I/O, or a violated internal invariant, which is a bug. For those errors, record what diagnostics you can and bring the unit to its safest available stopping point. Put that stop behind one checked wrapper so call sites don't each repeat the check. A pure computation aborts. A process driving something physical, costly, or external reaches a defined safe stop before it exits. A supervised, isolated unit stops, and its supervisor restarts it to a known-good state. A long-running loop contains the fault to the smallest unit and keeps running. Do not stop on an error only because it is hard to handle.

When a failure cannot be defined away, masked, or aggregated, and stopping does more harm, continue in a degraded mode designed for it. An undesigned degraded path is a barely-tested error branch.

Define away, mask, or stop on an error only when no caller needs to know it happened. Never define away or mask into success a security or authorization outcome, such as an auth denial, a validation rejection, or a permission failure. Return it as a result the caller acts on.

Do not throw a condition to the caller only because you cannot choose how to handle it, because the caller usually cannot choose either. Prefer a design whose error handler a test can run, because bugs in barely-exercised error paths cause a large share of production failures.

## Performance design

Do the design before you measure, and measure before you optimize.

**At design time, know what is expensive.** When a naturally efficient option is no more complex than a slow one, take it. A cheap operation repeated in a steady-state loop can exceed the budget. In such a loop, reuse memory over allocating fresh, and skip or defer work over blocking the loop to retry.

**Add complexity only on evidence.** Add performance complexity before a problem appears only when it is small and hidden behind the interface. When it is large or changes an interface, build the simple version and optimize after a problem appears. The exception is a path with a stated budget it must meet to be correct, such as a latency or memory limit, a frame deadline, a no-allocation policy, or a known hot path. Treat that budget as a design input from the start. Measure the path at its worst case under load, because the average can hide an exceeded limit.

**When something is slow, measure, then redesign the critical path.** Build a measurement harness only for a stated budget or a measured problem. Never optimize on a guess about which line is slow. Writing in an idiom whose cost is known, such as allocation-free code, is design and needs no measurement. Record a baseline, change one thing, and re-measure. Revert a change with no measurable effect unless it also simplified the design. Try a fundamental fix first, such as a cache, a better algorithm, or a better data structure. Redesign the critical path in code only as the last resort.

For that redesign, write the smallest code the common case must run, ignoring the current structure, and rebuild toward it. Put one check at the top that sends every special case off the common path, and write the special-case code for simplicity over speed.

## Brownfield Work

Before adding an error, validation, retry, cache, or batching path, find the existing ones nearby. When the same handling repeats across call sites, report the copies at file:line and the consolidation that would remove them. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a behavior change.

## Red flags

- An error signaled for a condition the API could define away.
- The same error handled at many call sites when one handler would do.
- An error eliminated or masked that callers needed.
- Elaborate recovery for a rare unrecoverable error that should stop in its safest state.
- A transient error handled at the caller when an internal retry would remove it.
- A remote call with no timeout.
- A retry added above a client or SDK that already retries.
- Retry backoff with no jitter.
- A performance change made without a baseline, or left in the code with no measured improvement.
- A cache, queue, batcher, circuit breaker, or other performance complexity added for an anticipated problem nobody has observed.

## References

Read the stack file that matches the code, and open a subject file only when that subject is the change.

- `references/examples.md` has one worked case each for error steps 1, 3, and 4, the masking limit, and design-time performance. Open it when you cannot tell which error step applies.
- `references/web.md` covers React, Solid, and Svelte error boundaries, async errors, memoization, virtualization, and render work.
- `references/mobile.md` covers React Native network errors, native module errors, lists, images, and bridge calls.
- `references/backend-apis.md` covers HTTP and gRPC retries, timeouts, circuit breakers, and bulk calls.
- `references/databases.md` covers N+1 queries, transaction retry, bulk writes, indexes, connection pools, and concurrent writes.
- `references/caching.md` covers the measurement to take before adding a cache, what a cache costs, stampede tiers, and TTL policy. Open it before adding a cache.
