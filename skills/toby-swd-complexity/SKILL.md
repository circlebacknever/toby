---
name: toby-swd-complexity
description: >-
  Decide whether an error path, a retry, a cache, or an optimization has
  earned its place. Use it when a task touches error handling, retries,
  validation, recovery paths, caching, concurrency, batching, or a measured
  performance problem. Two things here are cheap: removing error conditions that
  need not exist, and refusing speculative optimization. Heavier performance
  work engages only on a measurement. Skip it for a throwaway parameter
  loop, which `toby-swd-experiment` owns, and skip designing the cache's
  surface, which `toby-swd-interfaces` owns.
---

# Toby SWD Complexity

Exception handling and performance optimization are two of the largest sources of complexity in any codebase. Both get worse when handled tactically: a try/catch at every call site, a cache added because something feels slow, a special error path nobody tests. In both areas, each addition looks small, and the total cost becomes visible only later.

In both areas, reduce the number of places that must contain the extra logic.

Every special case a caller must branch on is complexity. Treat creating one as a design smell first. Fold it into the general case so no caller has to know it exists.

Shared mutable state and ordering between concurrent contexts is complexity like any other. Concentrate the discipline for touching it in one place, so the call sites contain no locks, checks, or assumptions.

## Error design

Count what an error signal costs before adding one. It costs the handling it forces on every caller between the failure and the code that can act on it. That handling is a catch at each level the error propagates through, or a value every caller must check or pass upward. Signals here mean a thrown exception, an error return, a status code, a `Result`, an `Option`. Work down this ladder and stop at the first rung that applies.

1. **Define the error out of existence.** Before writing any handling, ask whether the operation's semantics can be redefined so the condition is no longer an error. "Delete this variable, fail if absent" becomes "ensure this variable no longer exists." "Throw if an index is out of range" becomes "return the overlap, empty if none." The error case disappears, the API gets simpler, the module gets deeper. Redefining the semantics is right only when the condition is a non-event. When a reported success would mask a real bug, the error stays. Removing the branch is rung 1 of the conditional ladder in `toby-swd-modules`, because a branch nobody writes cannot break later.

2. **Mask it at the lowest level.** If a low-level module can fully handle the condition without the caller ever knowing, handle it there. Masking works best in a widely-used library method, where it removes the most handlers. Transient errors are the canonical case: a network blip, a database deadlock, a rate-limit response. When a bounded retry inside the module turns them into success, the caller never had a failure to handle.

3. **Aggregate.** If it must surface, let it propagate several levels to one handler that addresses the general case, such as the single handler at the top of a request loop. One handler at the top replaces a handler at every call site. When that handler replies to an untrusted caller, the surfaced error includes the category the caller needs. It includes nothing about internals, so it contains no stack traces, internal identifiers, or query text. Log the detail and return the category.

4. **Stop in the safest reachable state.** Some errors leave no caller able to act, such as resource exhaustion, unrecoverable I/O, or a violated internal invariant, which means a bug. For those errors, record what diagnostics you can and bring the unit to its safest available stopping point. Put that stop behind one checked wrapper so call sites don't each repeat the check. The environment decides what "safest" means. A pure computation aborts. A process driving something physical, costly, or external reaches a defined safe stop before it exits. A supervised, isolated unit stops, and its supervisor restarts it to a known-good state. A long-running loop contains the fault to the smallest unit and keeps running. The stop is the correct handling for an error nobody can act on. "Hard to handle" is not a reason to reach for it.

Some failures can't be defined away, masked, or aggregated, and stopping would make things worse. When the operation must continue in a reduced or safer mode, the handling is a deliberately designed degraded path the system was built to expect. An undesigned degraded path is the barely-tested error branch the hard rules warn about.

**Guardrail**: eliminating, masking, or crashing is correct only when the information is not needed outside the module. A module that swallows every network error so callers can't tell a message was lost hasn't reduced complexity. It has made reliable use impossible. Decide what information matters. Hide what callers do not need, and surface what they do. Never define away or mask into success a security or authorization outcome, such as auth denied, a validation rejection, or a permission failure. Surface it as a real result the caller acts on.

**Hard rules**: don't signal an error for conditions a well-designed API would not produce. If you can't decide what to do, the caller probably can't either, so throwing just relocates the problem and adds cost. Treat handler code that can't be tested reliably with extra skepticism. A large share of production failures come from bugs in barely-exercised error paths.

## Performance design

Design first, measure second, optimize third. Tight code tends to be fast, because defined-away special cases need no checks and deep modules cross fewer layers. Beyond good design, performance work has three layers.

**At design time, always know what is expensive.** Learn which operations cost orders of magnitude more: network round trips, disk I/O, dynamic allocation, cache misses. When a naturally efficient option is no more complex than a slow one, take it. For example, use a hash table when ordering isn't needed, and allocate one block where many would do. Design awareness costs nothing, and it prevents a system that ignored performance from running 5 to 10 times slower with no single fix available. Some costs appear only in aggregate. An operation that is cheap once can exceed the budget in a tight repeated loop, and allocation that accumulates forces later reclamation. In a steady-state loop, prefer reusing memory over allocating fresh, and prefer skipping or deferring work over blocking the loop to retry.

**Gate complexity on evidence.** If efficiency requires added complexity that is small and hidden behind the interface, it may be worth it. Be wary even then, because that complexity still adds up. If it is large or complicates an interface, start simple and optimize only if a problem appears. The exception is a path with a stated budget it must meet to be correct, such as a latency or memory limit, a frame deadline, a no-allocation policy, or a known hot path. Treat that budget as a design input and build to it from the start. For such a path the binding number is the worst case under load, because the average can hide a blown limit.

**When something is slow, measure, then redesign the critical path.** Never optimize on intuition, because programmer intuition about what is slow is unreliable regardless of experience. This rule targets guessing which line is the bottleneck. Writing in an idiom whose cost is already known, such as allocation-free or naturally typed code, is ordinary design and stays welcome. Record a baseline, change one thing, re-measure. A change with no measurable effect gets reverted unless it also simplified the design. Look for a fundamental fix first: a cache, a better algorithm or data structure. Code-level critical-path redesign is the last resort.

When it is needed, describe the smallest code that must run in the common case, ignoring the current structure, and rebuild toward that. One test at the top detects all special cases, and the common path then runs with no further branching. Special-case code sits off the common path and is structured for simplicity, since it no longer runs on the hot path and gains nothing from being fast.

## Proportionality

The design-time moves are cheap and apply on every edit. Build a measurement harness, record baselines, and rebuild the critical path only for a stated performance requirement or a measured problem, and never on speculation. Only a measured critical path justifies complexity that good design would otherwise reject, and even then the off-path code stays tidy.

## Brownfield Work

In existing code, inspect the current error, validation, retry, cache, batching, and performance paths before adding another branch. If the same complexity is scattered across nearby call sites, name the local consolidation that would remove it. Offer that refactor when it fits the task. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a behavior change. If the consolidation establishes a module rule, offer to record it in the nearest meaningful AGENTS.md.

## Red flags

Before finishing, check the change against every red flag below and fix anything that applies.

- An error signaled for a condition the API could define away.
- The same error handled at many call sites when one handler would do.
- An error eliminated or masked that callers needed.
- Elaborate recovery for a rare unrecoverable error that should stop in its safest state.
- A transient error handled at the caller when an internal retry would erase it.
- An optimization with no measured improvement left in the code.
- Performance changes made without a baseline.
- Speculative complexity added for performance with no evidence it matters.
- A cache, queue, batcher, or circuit breaker added because of an anticipated problem nobody has observed.

## References

Open one. Read the stack file matching the code in front of you, and open a subject file only when that subject is the change:

- `references/examples.md` — Foundational backend and frontend cases.
- `references/web.md` — React, Solid, Svelte. Error boundaries, async error handling, render perf, memoization, virtualization.
- `references/mobile.md` — React Native. Offline/online transitions, native module errors, list virtualization, image memory.
- `references/backend-apis.md` — HTTP error categorization, retries as masking, timeouts as design, circuit breakers.
- `references/databases.md` — N+1 patterns, transaction retry on deadlock, bulk vs row-by-row, index decisions.
- `references/caching.md` — When a cache is worth its complexity, measurement-driven adoption, stampede as performance problem.
