---
name: toby-swd-complexity
description: >-
  Complexity compounds when error handling and performance work are handled
  tactically — scattered across call sites, added speculatively, piled up with
  each new case. Use this skill when a task touches errors, retries, validation,
  recovery paths, performance, caching, concurrency, batching, or special cases.
  The cheap moves are to remove unnecessary error conditions and refuse
  speculative optimization. The heavier performance work engages only on a
  measured problem.
---

# Toby SWD Complexity

Exception handling and performance optimization are two of the largest sources of complexity in any codebase. Both get worse when handled tactically — a try/catch at every call site, a cache added because something feels slow, a special error path that nobody tests. The failure mode is the same, because each addition looks small and the total weight is only visible in retrospect.

Both areas share one move. Reduce the number of places that must carry the extra logic.

Every special case a caller must branch on is complexity. Treat creating one as a design smell before a performance one, and fold it into the general case so no caller has to know it exists.

Shared mutable state and ordering between concurrent contexts is complexity like any other: concentrate the discipline for touching it in one place, so locks, checks, and assumptions don't scatter across call sites.

## Error design

The cost of an error signal — a thrown exception, an error return, a status code, a `Result` or `Option` — is the handling it forces on every caller between the failure and the code that can act on it: a catch at each level it propagates through, or a value every caller must check or thread upward. Work down this ladder and stop at the first rung that applies.

1. **Define the error out of existence.** Before writing any handling, ask whether the operation's semantics can be redefined so the condition is no longer an error. "Delete this variable, fail if absent" becomes "ensure this variable no longer exists." "Throw if an index is out of range" becomes "return the overlap, empty if none." The error case disappears, the API gets simpler, the module gets deeper. Redefining the semantics is right only when the condition is a non-event. When a reported success would mask a real bug, the error stays. This is the same move as rung 1 of the conditional ladder in `toby-swd-modules`: the branch that is not written cannot rot.

2. **Mask it at the lowest level.** If a low-level module can fully handle the condition without the caller ever knowing, handle it there. Masking works best in a widely-used library method, where it removes the most handlers. Transient errors are the canonical case: a network blip, a database deadlock, a rate-limit response. When a bounded retry inside the module turns them into success, the caller never had a failure to handle.

3. **Aggregate.** If it must surface, let it propagate several levels to one handler that addresses the general case — the single handler at the top of a request loop. One handler at the top replaces a handler at every call site. When that handler replies to an untrusted caller, the surfaced error carries the category the caller needs and nothing about internals — no stack traces, internal identifiers, or query text. Log the detail and return the category.

4. **Stop in the safest reachable state.** For errors no caller can act on — resource exhaustion, unrecoverable I/O, a violated internal invariant (which means a bug) — record what diagnostics you can and bring the unit to its safest available stopping point, behind one checked wrapper so call sites don't each repeat the check. What "safest" means belongs to the environment: a pure computation aborts; a process driving something physical, costly, or external reaches a defined safe stop before it dies; a supervised, isolated unit stops and is restarted to a known-good state; a long-running loop contains the fault to the smallest unit and keeps running. The stop is the correct handling for an error nobody can act on. "Hard to handle" is not a reason to reach for it.

Some failures can't be defined away, masked, or aggregated, and stopping would make things worse. When the operation must continue in a reduced or safer mode, the handling is a deliberately designed degraded path the system was built to expect. An undesigned degraded path is the barely-tested error branch the hard rules warn about.

**Guardrail**: eliminating, masking, or crashing is correct only when the information is not needed outside the module. A module that swallows every network error so callers can't tell a message was lost hasn't reduced complexity. It has made reliable use impossible. Decide what information matters. Hide what callers do not need, and surface what they do. A security or authorization outcome — auth denied, a validation rejection, a permission failure — is never an error to define away or mask into success. Surface it as a real result the caller acts on.

**Hard rules**: don't signal an error for conditions a well-designed API would not produce. If you can't decide what to do, the caller probably can't either, so throwing just relocates the problem and adds cost. Treat handler code that can't be tested reliably with extra skepticism. A large share of production failures come from bugs in barely-exercised error paths.

## Performance design

Tight code tends to be fast, because defined-away special cases need no checks and deep modules cross fewer layers. The first performance move is good design. Beyond that, performance work has three layers.

**Always, at design time — know what is expensive.** Develop a feel for the operations that cost orders of magnitude: network round trips, disk I/O, dynamic allocation, cache misses. When a naturally efficient option is no more complex than a slow one, take it — reach for a hash table when ordering isn't needed, allocate one block where many would do. This costs nothing and prevents the death-by-a-thousand-cuts case where ignoring performance entirely yields a system 5–10x slow with no single fix available. Some costs show up only in aggregate. An operation cheap once becomes a budget-breaker in a tight repeated loop, and allocation that accumulates forces later reclamation. In a steady-state loop, prefer reusing memory over allocating fresh, and prefer skipping or deferring work over blocking the loop to retry.

**Gate complexity on evidence.** If efficiency requires added complexity that is small and hidden behind the interface, it may be worth it (it's still incremental — be wary). If it is large or complicates an interface, start simple and optimize only if a problem appears. Exception: when a path has a stated budget it must meet to be correct — a latency or memory limit, a frame deadline, a no-allocation policy, a known hot path — treat that budget as a design input and build to it from the start. For such a path the binding number is the worst case under load, because the average can hide a blown limit.

**When something is slow — measure, then redesign the critical path.** Never optimize on intuition, because programmer intuition about what is slow is unreliable regardless of experience. This rule targets guessing which line is the bottleneck. Writing in the idiom whose cost class is already known — allocation-free, naturally typed — is ordinary design and stays welcome. Record a baseline, change one thing, re-measure. A change with no measurable effect gets reverted unless it also simplified the design. Look for a fundamental fix first: a cache, a better algorithm or data structure. Code-level critical-path redesign is the last resort.

When it is needed, describe the smallest code that must run in the common case, ignoring the current structure, and rebuild toward that. One test at the top detects all special cases, and the common path then runs with no further branching. Special-case code sits off the path structured for simplicity, since it no longer runs on the hot path and gains nothing from being fast.

## Proportionality

The design-time moves are cheap and apply on every edit. The measurement harness, baseline discipline, and critical-path rebuild engage only for a stated performance requirement or a measured problem — never speculation. Only a measured critical path justifies complexity that good design would otherwise reject, and even then the off-path code stays tidy.

## Brownfield Work

In existing code, inspect the current error, validation, retry, cache, batching, and performance paths before adding another branch. If the same complexity is scattered across nearby call sites, name the local consolidation that would remove it and offer that refactor when it fits the task. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a behavior change. If the consolidation establishes a module rule, offer to record it in the nearest meaningful AGENTS.md.

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

Worked examples organized by domain. Read the file matching the code you are in:

- `references/examples.md` — Foundational backend and frontend cases.
- `references/web.md` — React, Solid, Svelte. Error boundaries, async error handling, render perf, memoization, virtualization.
- `references/mobile.md` — React Native. Offline/online transitions, native module errors, list virtualization, image memory.
- `references/backend-apis.md` — HTTP error categorization, retries as masking, timeouts as design, circuit breakers.
- `references/databases.md` — N+1 patterns, transaction retry on deadlock, bulk vs row-by-row, index decisions.
- `references/caching.md` — When a cache earns its complexity, measurement-driven adoption, stampede as performance problem.
