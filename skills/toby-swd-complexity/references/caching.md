# Worked Examples — Caching as Complexity

This file covers one question about caching: *should you add a cache at all*,
and if so, *how much complexity does it add*? Where to place a cache
and what its contract should be are separate questions handled elsewhere.

A cache adds performance complexity, so the SKILL's rule to base
complexity on evidence applies. Add a cache only when a measurement justifies it. The
default is no cache.

---

## Example 1 — "We should cache this": measurement before commitment

Here is a common conversation:

> "The products endpoint is slow. We should cache it."

The first question, which asks how it is slow, usually gets no answer. Going straight from "slow" to "added Redis" skips the measurement and
the baseline. Without them, you cannot tell whether the cache will help.

Do this work before adding any cache:

1. **Measure the current latency.** Record the median, P95, and P99 for the
   hot path, because those numbers give a baseline where "slow" gives only a feeling.
2. **Find where the time goes.** Check whether it is a database query, a
   downstream API call, or CPU work in serialization. Check this because a 5x improvement
   in the wrong layer gains nothing.
3.

**Estimate the hit ratio.** A cache that's invalidated on every
   request (because the data changes constantly, or the cache key is
   too narrow) saves nothing. It also adds latency on the miss path.
4. **Estimate the staleness tolerance.** Some data, such as account
   balances, must be fresh, while a product catalog can be minutes stale.
   The TTL is a product decision, so set it from the staleness budget.

After this, the cache is either plainly right (slow database query,
high hit ratio, tolerant of seconds-to-minutes staleness). Otherwise it is plainly
wrong (mostly already-fast, low repeat-access rate, near-zero staleness
budget).

The decision-making artifact for a "should we cache this" thread should
be a short note:

```
Endpoint: GET /api/products/:id
Current P95: 450ms
Source of slowness: Postgres query (joins + product variants), ~400ms
Expected hit ratio: 80% (product catalog changes hourly; reads are constant)
Staleness budget: 5 minutes acceptable
Decision: cache, 5-minute TTL, repository-level
Projected P95 with cache: 50ms (miss path) / 5ms (hit path)
```

A cache added without this note is speculative complexity. The note gives
you a measurable predicted improvement and a baseline to compare against.

---

## Example 2 — The complexity a cache adds

List the recurring costs of a cache layer in full before
deciding:

- **Invalidation.** Every mutation that affects a cached value must
  evict the right keys. Missed invalidation is the source of most cache bugs. Code
  paths that update the data without going through the caching layer
  produce stale reads.
- **A new system to monitor.** Redis (or whatever) is now in your
  critical path. It has its own latency, outages, and operational
  work.
- **Cold-start behavior.** When the cache restarts, every request misses
  until the cache warms. If the underlying data store can't handle peak
  traffic alone, the cache restart is now a production incident.
- **Stampede risk.** A popular key expiring at the same moment thousands
  of users request it sends every miss to the store at once. Mitigations exist
  (single-flight, stale-while-revalidate) but they're additional
  complexity inside the cache layer.
- **Test complexity.** Tests now need to handle cached vs uncached
  paths. Snapshot tests have to account for TTLs. Integration
  tests need cache reset between cases.
- **Observability cost.** Did this request hit the cache? Was that
  cached value stale? You need metrics for hit rate, miss rate, and TTL
  effectiveness. Those metrics did not exist before.

The cache adds 5 lines of code at the call site and ten times as much
operational work. Weigh both costs when you ask "is the P99 latency
improvement worth this?"

When the answer is yes, ship the cache. When the answer is no but the
endpoint is too slow, do other work, such as optimizing the query,
adding an index, denormalizing, or fixing the N+1. Those changes usually
add less operational work than introducing a cache.

---

## Example 3 — Stampede: a performance problem that looks like an error

This cache appears to "just work":

```ts
// this code repeats at every cache call site
const cached = await cache.get(key);
if (cached) return cached;
const fresh = await load();
await cache.set(key, fresh, 600);
return fresh;
```

Under low load, this works. Under peak load, a popular key expires and 1000
concurrent requests all miss, all call `load()`, and all hit Postgres. The
database now handles 1000 connections for what should be a single query, so
the hot path becomes slower than having no cache.

The stampede is a performance problem, but the results stay correct. The
load eventually succeeds and the cache repopulates, so the system recovers. During
the stampede, though, the system is far slower than the uncached version, because
each load contends with 999 others.

The mitigations below are in order of complexity:

**Single-flight per process.** Each process runs at most one in-flight load
per key, so concurrent waiters share the result. Most cache libraries offer
this (`getOrLoad`, `wrap`, `loadingCache`). The internal implementation
holds a map of `key → Promise<T>` for in-flight loads.

```ts
// this is pseudocode
async getOrLoad<T>(key: string, ttl: number, load: () => Promise<T>): Promise<T> {
  const cached = await this.cache.get<T>(key);
  if (cached !== null) return cached;

  // single-flight: if a load is in flight for this key, await it
  const inFlight = this.loadingMap.get(key);
  if (inFlight) return inFlight as Promise<T>;

  const promise = (async () => {
    try {
      const fresh = await load();
      await this.cache.set(key, fresh, ttl);
      return fresh;
    } finally {
      this.loadingMap.delete(key);
    }
  })();
  this.loadingMap.set(key, promise);
  return promise;
}
```

This handles 1000 concurrent in-process requests with one downstream call.
Across processes, you still get one call per process, which is usually
acceptable unless you have hundreds of processes.

**Cross-process locking.** Add a short-lived distributed lock (Redis
`SET NX EX`) around the load. Other processes wait briefly and read
from cache when the lock holder finishes. Locking is worth the complexity
only when in-process single-flight isn't enough. That happens when you have
many processes and the load is so expensive that even one call per process
is too many.

**Stale-while-revalidate.** Continue serving the stale value to most
callers while a single load refreshes the cache in the background. The
hot path stays fast even during the refresh, but users see slightly-old
data for a short window. The complexity is real (a background refresh
worker, a "is this stale?" check). Stale-while-revalidate is worth it when
the staleness budget allows it and load latency is significant.

Pick the lowest tier that solves the measured problem. Don't skip to
stale-while-revalidate because it sounds clever.

---

## Example 4 — Cache TTL: a product decision

This pattern produces cache bugs:

```ts
await cache.set('user:profile', profile, 3600);   // the author picked 1 hour
```

The author guessed the 1-hour value. That TTL is now a magic number
scattered across the codebase. Suppose the requirements change because
"users complain that their profile changes don't show up for a long time".
It is unclear whether to change the TTL, where to find all the places
it's used, or whether the change will break something else.

The TTL is a contract about staleness. State it as one:

```ts
// staleness/policies.ts
export const STALENESS = {
  /** User-editable settings must reflect changes quickly. */
  USER_PROFILE: 60,             // seconds
  /** Product catalog changes are infrequent and not user-visible immediately. */
  PRODUCT_CATALOG: 600,
  /** Live availability data must be near-fresh. */
  AVAILABILITY: 5,
} as const;

await cache.set('user:profile', profile, STALENESS.USER_PROFILE);
```

Each TTL is documented with the reasoning. Changing the staleness policy
is a one-line edit at a named location. Authors of new caches ask
"which staleness category does this fit?" Authors pick a category and do not have to guess "what
number should I put here?"

When every read of the data must be fresh,
don't cache it. A 1-second TTL causes bugs, because it caches long
enough to produce occasional stale reads under load while delivering
almost no hit-rate benefit.

---

## Example 5 — Cache that's worse than no cache

This pattern adds complexity for negative benefit:

```ts
// Every read tries the cache, but the cache returns null almost always
async function getUserProfile(userId: string): Promise<UserProfile> {
  const cached = await cache.get(`profile:${userId}`);
  if (cached) return cached;

  const fresh = await profileRepo.find(userId);
  await cache.set(`profile:${userId}`, fresh, 60);     // the TTL is 60 seconds
  return fresh;
}
```

The code looks correct until you measure it:

- The average user visits their profile page less than once per minute.
- 95% of `cache.get` calls return null (TTL expired between visits).
- The cached path adds a Redis round-trip (~1ms) to every read.
- The miss path also writes to Redis (~1ms additional).

The cache adds ~2ms per request and saves time on ~5% of requests. The net
effect is a path slightly slower than no cache, plus all the operational
complexity from Example 2.

Speculative caching produces this result. The cache "feels right" because
profiles are a hot data type, but the access pattern doesn't
support it.

The right move depends on the goal:

- If the issue was "the database is slow," fix the database with the
  indexes in Example 4 of `databases.md`. The cache wasn't going to help much
  because hit rate was low.
- If the issue was "we want to reduce database load," a cache might
  help with a longer TTL that pushes the hit rate up. That TTL requires a
  willingness to serve profiles up to 1 hour stale. The cache is worth its
  complexity only when it hits.
- If the issue was perceived and never measured, add no cache at all.

A cache is worth its complexity only when it *hits often enough to
matter*. If the access pattern produces a low hit rate, the cache adds
complexity and nothing else.

---

## Cheat sheet — caching complexity

| Question | Answer |
|---|---|
| Should I add a cache? | First, baseline the current latency and find where time goes |
| What's the hit ratio? | Estimate from access patterns; under 50% rarely justifies caching |
| How fresh must the data be? | TTL = staleness budget; name it and document the reason |
| Stampede risk? | Single-flight in-process is the cheap default; locking and stale-while-revalidate cost more |
| How do I know it's working? | Hit rate, miss rate, miss-path latency, all as metrics |
| When to remove a cache? | Hit rate stays low; the work it was protecting is no longer slow |

When you decide on a cache, you also decide on complexity. When the evidence does not
justify a cache, skip it. The system then stays simpler to operate, easier to
test, and clearer to reason about. Add a cache only on measured improvement.
