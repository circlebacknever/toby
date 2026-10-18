# Caching

This file covers the measurement to take before adding a cache, what a cache costs, key scoping, stampedes, and TTL policy. A stampede is many requests reloading the same expired entry at once. Open it before adding a cache.

## Before adding a cache

1. Record the median, p95, and p99 of the hot path.
2. Identify which step spends the time: a query, a downstream call, or serialization.
3. Estimate the hit ratio from the access pattern. Add the cache only when `hit_ratio * time_saved_per_hit > cache_round_trip`, and state both numbers.
4. Confirm the staleness budget with the user. An account balance needs fresh data, while a product catalog can be minutes old.

Write the decision as a note:

```text
Endpoint: GET /api/products/:id
Current P95: 450ms
Source of slowness: Postgres query (joins + product variants), ~400ms
Expected hit ratio: 80% (catalog changes hourly; reads are constant)
Staleness budget: 5 minutes
Decision: cache, 5-minute TTL, repository-level
Projected median: 5ms, on a hit
Projected P95: ~450ms, because 20% of requests miss. P95 drops only above a 95% hit ratio.
```

Remove a cache whose measured hit rate stays low or whose underlying query is now fast.

## What a cache costs

- Every write path must evict or update the affected keys, and any path that skips eviction serves stale reads.
- Every cache key for non-public data must include the tenant, account, or role scope (`org:{orgId}:invoice:{id}`) so one user never reads another user's cached record.
- Never cache a transient error or empty fallback for the full TTL. Let the error fail fast or cache a negative result for at most a few seconds when guarding against repeated misses.
- After a cache flush or restart every request misses, so the database or upstream service must survive peak load with a cold cache.
- Tests must cover both the cached and uncached paths and reset the cache between tests, and metrics must track hits, misses, and miss latency.

When these costs outweigh the gain, fix the underlying query with an index, a batch read, or an N+1 fix.

## Stampede

Use the cheapest tier that solves the measured problem:

1. **Single-flight per process** runs one load per key in each process and shares the promise with concurrent callers (`getOrLoad`).
2. **Short distributed lock** (`SET NX EX`) runs one load across all processes when hundreds of workers or an expensive query make per-process loads too costly.
3. **Stale-while-revalidate** serves the slightly stale value while one background task refreshes it, when the staleness budget allows.

## TTL

Define each TTL once as a named staleness constant with the product reason:

```ts
export const STALENESS = {
  /** Users expect their own profile edits to appear within a minute. */
  USER_PROFILE: 60, // seconds
  PRODUCT_CATALOG: 600,
  AVAILABILITY: 5,
} as const;
```

Don't cache data that every read needs fresh, because even a 1-second TTL serves stale data under concurrent writes.
