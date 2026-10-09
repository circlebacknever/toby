---
name: toby-optimize
description: >-
  Makes working code faster or lighter from a measured baseline, with one change
  per measurement. It covers whether a cache, a batch, a queue, or parallel work
  is worth what it adds. Use it when the user says code is slow, or asks to
  speed it up or to cut latency, memory, or query count. Use it when the user
  asks to add a cache to code that already works. Skip it for new behavior that
  includes a cache, which toby-build covers, and for wrong output, which
  toby-bug-fix covers. Skip it for a speed question with no change asked for,
  which toby-explain covers, and for a throwaway sweep, which
  toby-swd-experiment covers.
---

# Toby Optimize

Make working code faster or lighter, and keep only the changes a measurement supports.

## Steps
1. Record a baseline with one named command, and quote its output.
2. Look for a better algorithm, a better data structure, a missing index, or a cache before code-level tuning.
3. Change one thing, then run the same command again. Run the tests that cover the changed code. When the changed code has no test, compare its output before and after the change, such as the rendered page or the returned rows.
4. Revert a change with no measured effect unless it also made the code simpler.
5. When the code path has a stated budget, such as a latency or memory limit, measure its worst case under load. An average can hide requests over the limit.
6. Stop once the result meets the user's target or the budget from step 5. When neither exists, stop once the causes the baseline showed are gone.

Open `toby-swd-hardening` for limits and `toby-swd-observability` for metrics when the change adds a cache, a queue, a worker pool, or parallel calls.

## Report
Give the baseline, the result, the command, the other options you did not try, and what stays unmeasured, such as production load.

## Performance design

Think about cost while you design.

**At design time, know what is expensive.** When a fast option is no more complex than a slow one, take the fast one. A cheap operation can exceed the budget when a loop that runs all the time repeats it. In such a loop, reuse memory. Skip or defer work that cannot finish now, and do not block the loop to retry it.

**Add complexity only on evidence.** Before a problem appears, add performance complexity only when it is small and the module's interface hides it from callers. When it is large or changes an interface, build the simple version and optimize after a problem appears. The exception is a path with a stated budget it must meet to be correct, such as a latency or memory limit, a frame deadline, a no-allocation policy, or a known hot path. Treat that budget as a design input from the start.

**When something is slow, measure before you change it.** Build a measurement harness only for a stated budget or a measured problem. Writing code in a style whose cost is already known, such as allocation-free code, counts as design and needs no measurement. Redesign the critical path in code only as the last resort, after step 2.

For that redesign, first write the least code the common case needs, ignoring how the code is arranged today. Then change the existing code toward that version. Put one check at the top that sends every special case off the common path. Write the special-case code to be simple even when it runs slower.

## Brownfield Work

Brownfield work means changing code that already exists. Before adding a cache or batching path, find the existing ones nearby. When the same caching or batching repeats across call sites, report the copies at file:line and the consolidation that would remove them. Preserve caller-visible errors, response bodies, logs, metrics, and status codes unless the user approves a behavior change.

## Red flags

- A performance change made without a baseline.
- A cache, queue, batcher, or other performance complexity added for an anticipated problem nobody has observed.

## References

Read the reference below that matches the code's platform, such as web or mobile.

- `references/caching.md` covers the measurement to take before adding a cache, what a cache costs, stampede tiers, and TTL policy. A stampede is many requests reloading the same expired entry at once. Open it before adding a cache.
- `references/examples.md` has a worked case of design-time performance.
- `references/web.md` covers React, Solid, and Svelte memoization, virtualization, and render work.
- `references/mobile.md` covers React Native lists, images, and bridge calls.
- `references/backend-apis.md` covers bulk calls.
- `references/databases.md` covers N+1 queries, bulk writes, indexes, and connection pools.
