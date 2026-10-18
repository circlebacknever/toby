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

1. Record a baseline with one named command after warmup, run multiple trials, and quote the median and p95 (or range).
2. Look for a better algorithm, a better data structure, a missing index, or batching before code-level tuning or caching.
3. Change one thing, then run the same command and the covering tests (or compare the exact output before and after when tests don't exist).
4. Revert any change whose difference stays within run-to-run noise unless it also simplified the code.
5. When the code path has a stated latency or memory budget, measure its p95 and p99 under load, because averages hide tail spikes.
6. Stop once the result meets the user's target or budget, or once the bottlenecks shown in the baseline are gone.

Open `toby-swd-hardening` for pool/concurrency limits and `toby-swd-observability` for metrics when adding a cache, queue, worker pool, or parallel fan-out.

## Report

List the baseline, the after measurement, the command and trial count, the options you didn't try, and what stays unmeasured (such as production data volume).

## Performance design

Think about cost while you design.

- **Know what is expensive at design time.** When a fast option is as simple as a slow one, pick the fast one. In a hot loop, reuse memory, hoist invariant work out of the loop, and never block the loop on retries or I/O.
- **Add complexity only on evidence.** Before a slowdown is measured, add performance complexity only when it is small and hidden behind the module's interface. Treat a stated latency, memory, frame-time, or allocation budget as a required design input from the start.
- **Redesign the critical path last.** After step 2, write the minimum code the common case needs, route special cases off the top with one check, and keep the special-case path simple.

## Brownfield Work

Before adding a cache or batcher to existing code, search for nearby ones and report duplicated caching or batching at `file:line`. Preserve caller-visible errors, response bodies, logs, metrics, and status codes unless the user approves a behavior change.

## Red flags

- A performance change shipped without a before-and-after measurement outside run-to-run noise.
- A cache, queue, or batcher added for a hypothetical problem nobody has measured.

## References

Read the reference that matches the stack:

- `references/caching.md` covers pre-cache measurements, cache costs, tenant key scoping, stampede tiers, and TTL policy. Open it before adding a cache.
- `references/examples.md` shows design-time performance fixes.
- `references/web.md` covers React, Solid, and Svelte memoization, virtualization, and render work.
- `references/mobile.md` covers React Native lists, images, and bridge calls.
- `references/backend-apis.md` covers bulk API calls.
- `references/databases.md` covers N+1 queries, bulk writes, indexes, and connection pools.
