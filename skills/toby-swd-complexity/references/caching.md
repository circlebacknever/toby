# Worked Examples — Caching as Complexity

`toby-swd-modules` and `toby-swd-interfaces` both have caching content. They cover
*where* the cache should live and *what its contract should be*. This file
covers the question those don't: *should you add a cache at all*, and if
so, *how much complexity have you bought*?

A cache is performance complexity. The SKILL's rule applies: gate
complexity on evidence. A cache earns its place by measurement. The
default is no cache.

---

## Example 1 — "We should cache this": measurement before commitment

A common conversation:

> "The products endpoint is slow. We should cache it."

The first question — slow how? — usually doesn't get an answer. The
fastest path from "slow" to "added Redis" involves no measurement, no
baseline, and no idea whether the cache will actually help.

The discipline before adding any cache:

1. **Measure the current latency.** Median, P95, P99 for the hot path.
   "Slow" is a feeling; numbers are a baseline.
2. **Find where the time goes.** Is it a database query? A downstream
   API call? CPU work in serialization? A 5x improvement in the wrong
   layer is no improvement.
3. **Estimate the hit ratio.** A cache that's invalidated on every
   request (because the data changes constantly, or the cache key is
   too narrow) saves nothing and costs added latency on the miss path.
4. **Estimate the staleness tolerance.** Some data must be fresh
   (account balances). Some can be minutes stale (product catalog).
   The TTL is a product decision, not a tuning parameter.

After this, the cache is either plainly right (slow database query,
high hit ratio, tolerant of seconds-to-minutes staleness) or plainly
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

Without this, you're carrying speculative complexity. With it, you have
a measurable predicted improvement and a baseline to compare against.

---

## Example 2 — The complexity a cache actually adds

A cache layer brings real and recurring costs. List them truthfully before
deciding:

- **Invalidation.** Every mutation that affects a cached value must
  evict the right keys. This is the source of most cache bugs. Code
  paths that update the data without going through the caching layer
  produce stale reads.
- **A new system to monitor.** Redis (or whatever) is now in your
  critical path. It has its own latency, outages, and operational
  surface.
- **Cold-start behavior.** When the cache restarts, every request misses
  until the cache warms. If the underlying data store can't handle peak
  traffic alone, the cache restart is now a production incident.
- **Stampede risk.** A popular key expiring at the same moment thousands
  of users request it produces a thundering herd. Mitigations exist
  (single-flight, stale-while-revalidate) but they're additional
  complexity inside the cache layer.
- **Test complexity.** Tests now need to handle cached vs uncached
  paths. Snapshot tests have to be careful about TTLs. Integration
  tests need cache reset between cases.
- **Observability cost.** Did this request hit the cache? Was that
  cached value stale? You need metrics for hit rate, miss rate, TTL
  effectiveness — none of which existed before.

The cache adds 5 lines of code at the call site and 50 lines of
operational reality. The question "is the P99 latency improvement worth
this?" should be honest about both columns.

When the answer is yes, ship the cache. When the answer is no but the
endpoint is truly too slow, the work is somewhere else: optimize
the query, add an index, denormalize, fix the N+1. Those moves usually
have smaller operational footprint than introducing a cache.

---

## Example 3 — Stampede: a performance problem dressed as an error

A cache that "just works":

```ts
// at every cache call site
const cached = await cache.get(key);
if (cached) return cached;
const fresh = await load();
await cache.set(key, fresh, 600);
return fresh;
```

Under low load, fine. Under peak load, with a popular key expiring, 1000
concurrent requests all miss, all call `load()`, all hit Postgres.
Postgres now handles 1000 connections for what should be a single query.
The hot path goes from cached-fast to slower than uncached.

This is a performance problem, not a correctness problem — eventually
the load succeeds, the cache repopulates, things stabilize. But during
the herd, the system is far slower than the uncached version, because
each load contends with 999 others.

Three mitigations, in order of complexity:

**Single-flight per process.** At most one in-flight load per key per
process; concurrent waiters share the result. Most cache libraries offer
this (`getOrLoad`, `wrap`, `loadingCache`). The internal implementation
holds a map of `key → Promise<T>` for in-flight loads.

```ts
// pseudo
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
Across processes, you still get one call per process — usually acceptable
unless you have hundreds of processes.

**Cross-process locking.** Add a short-lived distributed lock (Redis
`SET NX EX`) around the load. Other processes wait briefly and read
from cache when the lock holder finishes. Only worth the complexity when
in-process single-flight isn't enough — you have many processes and the
load is so expensive that even one-per-process is too many.

**Stale-while-revalidate.** Continue serving the stale value to most
callers while a single load refreshes the cache in the background. The
hot path stays fast even during the refresh; users see slightly-old
data for a short window. The complexity is real (a background refresh
worker, a "is this stale?" check). Worth it when staleness budget allows
and load latency is significant.

Pick the lowest tier that solves the measured problem. Don't skip to
stale-while-revalidate because it sounds clever.

---

## Example 4 — Cache TTL: a product decision, not a magic number

A pattern that produces cache bugs:

```ts
await cache.set('user:profile', profile, 3600);   // 1 hour, picked by author
```

Where did 1 hour come from? The author guessed. The TTL is now a magic
number scattered across the codebase. When the requirements change —
"users complain that their profile changes don't show up for a long time"
— nobody knows whether to change the TTL, where to find all the places
it's used, or whether the change will break something else.

The TTL is a contract about staleness. State it as one:

```ts
// staleness/policies.ts
export const STALENESS = {
  /** User-editable settings — must reflect changes quickly. */
  USER_PROFILE: 60,             // seconds
  /** Product catalog — changes are infrequent and not user-visible immediately. */
  PRODUCT_CATALOG: 600,
  /** Live availability data — must be near-fresh. */
  AVAILABILITY: 5,
} as const;

await cache.set('user:profile', profile, STALENESS.USER_PROFILE);
```

Each TTL is documented with the reasoning. Changing the staleness policy
is a one-line edit at a named location. New caches in the codebase ask
"which staleness category does this fit?" rather than "what number should
I put here?"

For data that truly shouldn't be cached (every read must be fresh),
don't cache it. A 1-second TTL is a bug magnet — it caches just long
enough to produce occasional stale reads under load while delivering
almost no hit-rate benefit.

---

## Example 5 — Cache that's worse than no cache

A pattern that adds complexity for negative benefit:

```ts
// Every read tries the cache; cache returns null almost always
async function getUserProfile(userId: string): Promise<UserProfile> {
  const cached = await cache.get(`profile:${userId}`);
  if (cached) return cached;

  const fresh = await profileRepo.find(userId);
  await cache.set(`profile:${userId}`, fresh, 60);     // 60-second TTL
  return fresh;
}
```

Looks fine. Then measure:

- Average user visits their profile page < once per minute.
- 95% of `cache.get` calls return null (TTL expired between visits).
- The cached path adds a Redis round-trip (~1ms) to every read.
- The miss path also writes to Redis (~1ms additional).

The cache adds ~2ms per request and saves time on ~5% of requests. Net
effect: slightly slower than no cache, plus all the operational
complexity from Example 2.

This is what speculative caching produces. The cache "feels right" —
profiles are a hot data type, after all — but the access pattern doesn't
support it.

The right move depends on the actual goal:

- If the issue was "the database is slow," fix the database (Example 4
  in `databases.md` — indexes). The cache wasn't going to help much
  because hit rate was low.
- If the issue was "we want to reduce database load," a cache might
  help — but with a longer TTL (and a willingness to serve up-to-1-hour
  stale profiles) to push hit rate up. The cache earns its complexity
  by actually hitting.
- If the issue was perceived rather than measured, no cache at all.

The lesson: caches earn their complexity by *hitting often enough to
matter*. If the access pattern produces low hit rate, the cache is just
complexity.

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

The cache decision is a complexity decision. Every cache you don't add
is a system that's simpler to operate, easier to test, and clearer to
reason about. Caches earn their place by measured improvement, not by
"feeling like the right move."
