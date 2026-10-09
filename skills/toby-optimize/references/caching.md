# Caching

This file covers the measurement to take before adding a cache, what a cache costs, stampedes, and TTL policy. A stampede is many requests reloading the same expired entry at once. Open it before adding a cache.

## Before adding a cache

1. Record the median, P95, and P99 of the hot path.
2. Find which layer spends the time: a query, a downstream call, or serialization.
3. Estimate the hit ratio from the access pattern. Add the cache when the hit ratio times the time a hit saves is larger than the round trip every request adds, and state both numbers. With a 400 ms query and a 2 ms round trip, a 30 percent hit ratio saves about 118 ms per request.
4. Get the staleness budget from the product owner. An account balance needs fresh data, and a catalog can be minutes old.

Write the decision as a note in this form:

```
Endpoint: GET /api/products/:id
Current P95: 450ms
Source of slowness: Postgres query (joins + product variants), ~400ms
Expected hit ratio: 80% (catalog changes hourly; reads are constant)
Staleness budget: 5 minutes
Decision: cache, 5-minute TTL, repository-level
Projected median: 5ms, on a hit
Projected P95: ~450ms, because 20% of requests miss. P95 drops only above a 95% hit ratio.
```

One 60-second profile cache missed 95 percent of reads, because users opened the page less than once a minute. It added about 2 ms to each read. Remove a cache whose hit rate stays low, or whose cached work is no longer slow.

## What a cache costs

- Every write path must evict the right keys, and a path that skips the cache layer serves stale reads.
- The cache server is a new dependency in the critical path, with its own outages.
- After a cache restart every request misses, so the data source behind the cache must survive peak load alone.
- A popular key that expires sends every concurrent miss to the data source at once.
- Tests need cached and uncached paths and a cache reset between cases.
- Hit rate, miss rate, and miss-path latency need new metrics.

When these costs outweigh the gain, fix the slow work with an index, a query rewrite, denormalization, or an N+1 fix.

## Stampede

Use the cheapest tier that solves the measured problem:

1. Single-flight per process runs one load per key and shares the result with concurrent waiters. Most cache libraries offer it as `getOrLoad` or `wrap`.
2. A short distributed lock (Redis `SET NX EX`) runs one load across processes. Add it only when hundreds of processes or a very expensive load make one load per process too many.
3. Stale-while-revalidate serves the old value while one background load refreshes it. Add it only when the staleness budget allows and the load is slow.

## TTL

A TTL is a staleness policy, so define each one once with its reason:

```ts
export const STALENESS = {
  /** Users expect their own edits to show quickly. */
  USER_PROFILE: 60,      // seconds
  PRODUCT_CATALOG: 600,
  AVAILABILITY: 5,
} as const;
```

A new cache uses one of these categories. Do not cache data that every read needs fresh, because a 1-second TTL still serves stale reads under load.
