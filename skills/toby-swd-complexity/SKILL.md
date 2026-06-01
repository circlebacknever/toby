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

Exception handling and performance optimization are two of the largest sources of complexity in any codebase. Both get worse when handled tactically — a try/catch at every call site, a cache added because something feels slow, a special error path that nobody tests. The failure mode is the same: each individual addition looks small, and the total weight is only visible in retrospect.

The unifying move is simple: reduce the number of places that must carry the extra logic.

## Error and exception design

The cost of an exception is the handling code it forces on every caller, propagating through every stack level it crosses. Work down this ladder; stop at the first rung that applies.

1. **Define the error out of existence.** Before writing any handling, ask whether the operation's semantics can be redefined so the condition is no longer an error. "Delete this variable, fail if absent" becomes "ensure this variable no longer exists." "Throw if an index is out of range" becomes "return the overlap, empty if none." The error case disappears, the API gets simpler, the module gets deeper.

2. **Mask it at the lowest level.** If a low-level module can fully handle the condition without the caller ever knowing, handle it there. Masking works best in a widely-used library method, where it removes the most handlers. Transient errors are the canonical case: a network blip, a database deadlock, a rate-limit response — if a bounded retry inside the module turns them into success, the caller never had a failure to handle.

3. **Aggregate.** If it must surface, let it propagate several levels to one handler that addresses the general case — the single handler at the top of a request loop — rather than a handler at every call site.

4. **Just crash.** For errors that are rare and hard or pointless to handle — out of memory, unrecoverable I/O, an internal invariant violated (which means a bug) — print diagnostics and abort, ideally behind one checked wrapper so call sites don't each repeat the check. This is a legitimate complexity reduction, not a failure to handle.

**Guardrail**: eliminating, masking, or crashing is correct only when the information is not needed outside the module. A module that swallows every network error so callers can't tell a message was lost hasn't reduced complexity; it's made reliable use impossible. Decide what information matters. Hide what callers do not need; surface what they do.

**Hard rules**: don't throw for conditions a well-designed API would not produce. If you can't decide what to do, the caller probably can't either — throwing just relocates the problem and adds cost. Treat handler code that can't be tested reliably with extra skepticism. A large share of production failures come from bugs in barely-exercised error paths.

## Performance design

Clean code tends to be fast: defined-away special cases need no checks, deep modules cross fewer layers. The first performance move is good design. Beyond that, performance work has three layers.

**Always, at design time — know what is expensive.** Develop a feel for the operations that cost orders of magnitude: network round trips, disk I/O, dynamic allocation, cache misses. When a naturally efficient option is no more complex than a slow one, take it — a hash table over an ordered map when ordering isn't needed, one block allocation over many. This costs nothing and prevents the death-by-a-thousand-cuts case where ignoring performance entirely yields a system 5–10x slow with no single fix available.

**Gate complexity on evidence.** If efficiency requires added complexity that is small and hidden behind the interface, it may be worth it (it's still incremental — be wary). If it is large or complicates an interface, start simple and optimize only if a problem appears. Exception: when there is clear upfront evidence performance will matter for a specific path, implement the fast approach immediately.

**When something is actually slow — measure, then redesign the critical path.** Never optimize on intuition; programmer intuition about what is slow is unreliable regardless of experience. Record a baseline, change one thing, re-measure. A change with no measurable effect gets reverted unless it also simplified the design. Look for a fundamental fix first: a cache, a better algorithm or data structure. Code-level critical-path redesign is the last resort.

When it is needed: describe the smallest code that must run in the common case, ignoring the current structure, and rebuild toward that — one test at the top detects all special cases, the common path then runs with no further branching, and special-case code sits off the path structured for simplicity rather than speed.

## Proportionality

The design-time moves are cheap and apply on every edit. The measurement harness, baseline discipline, and critical-path rebuild engage only for a stated performance requirement or a measured problem — never speculation. Only a measured critical path justifies complexity that good design would otherwise reject, and even then the off-path code stays tidy.

## Brownfield Work

In existing code, inspect the current error, validation, retry, cache, batching, and performance paths before adding another branch. If the same complexity is scattered across nearby call sites, name the local consolidation that would remove it and offer that refactor when it fits the task. Preserve caller-visible errors, timing, logs, metrics, and status codes unless the user approves a behavior change. If the consolidation establishes a module rule, offer to record it in the nearest meaningful AGENTS.md.

## Red flags

- An exception thrown for a condition the API could define away.
- The same error handled at many call sites instead of one.
- An error eliminated or masked that callers actually needed.
- Elaborate recovery for a rare unrecoverable error that should just abort.
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
