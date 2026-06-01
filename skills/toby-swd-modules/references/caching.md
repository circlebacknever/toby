# Worked Examples — Caching

Caches are one of the most-common forms of "small thing that goes everywhere"
and one of the easiest places to leak knowledge into call sites. Three things
determine whether a cache is a deep module or a maintenance liability: where
the cache calls live, who owns invalidation, and whether the cache or the
caller handles concurrent misses.

---

## Example 1 — Cache calls scattered across services

The instinct when adding Redis to a slow endpoint:

```python
def get_product(product_id: str) -> Product:
    key = f"product:{product_id}"
    cached = redis.get(key)
    if cached:
        return Product.from_json(cached)
    product = product_repo.find(product_id)
    redis.setex(key, 600, product.to_json())
    return product

def update_product(product_id: str, changes: dict) -> Product:
    product = product_repo.update(product_id, changes)
    redis.delete(f"product:{product_id}")              # don't forget!
    redis.delete(f"product:listing:{product.category}") # ...and this one
    return product

def get_product_listing(category: str) -> list[Product]:
    key = f"product:listing:{category}"
    cached = redis.get(key)
    # ...same pattern repeated
```

Two checks fail at once. Check 2 (information leakage): the cache key schema
(`"product:..."`), the TTL (600 seconds), the serialization format, and the
invalidation rules are duplicated wherever they're touched. Check 4 (different
layer, different abstraction): the service is supposed to be about products,
not about Redis, but half the code is Redis bookkeeping. When the team
introduces a second category-listing endpoint, the new author either
duplicates the cache machinery or — much worse — forgets to invalidate, and
stale listings appear in production.

Treat the cache as a layer below the repository, not as code sprinkled into
the service:

```python
class ProductsRepository:
    """Owns product persistence. Reads may be served from cache.
    Invalidation is internal: every mutation method evicts whatever it
    needs to keep reads consistent."""

    def find(self, product_id: str) -> Product | None: ...
    def listing(self, category: str) -> list[Product]: ...
    def update(self, product_id: str, changes: dict) -> Product:
        product = self._update(product_id, changes)
        self._evict_for(product)              # one place that knows what to drop
        return product
```

The service code returns to one-line operations. The cache key schema, TTL,
serialization, and invalidation policy live inside `ProductsRepository` (or in
a thin caching decorator around an underlying `ProductsStore` it composes).
Adding a new derived listing means adding a method and an entry to
`_evict_for`; never editing fifteen services.

This is the canonical place to pull complexity down (Check 3): the cache
serves many callers, and the right author for the hard parts is the module
that already owns the data.

---

## Example 2 — Cache as a decorator around storage

The sound composition pattern that follows from Example 1:

```typescript
interface ProductsStore {
    find(id: string): Promise<Product | null>;
    listing(category: string): Promise<Product[]>;
    save(p: Product): Promise<void>;
}

class PostgresProductsStore implements ProductsStore { ... }

class CachedProductsStore implements ProductsStore {
    constructor(
        private inner: ProductsStore,
        private cache: Cache,
    ) {}

    async find(id: string): Promise<Product | null> {
        return this.cache.getOrLoad(`product:${id}`, 600, () => this.inner.find(id));
    }
    async listing(category: string): Promise<Product[]> { ... }
    async save(p: Product): Promise<void> {
        await this.inner.save(p);
        await this.cache.delete(`product:${p.id}`);
        await this.cache.delete(`product:listing:${p.category}`);
    }
}

// composition root
const products: ProductsStore = new CachedProductsStore(
    new PostgresProductsStore(...),
    cache,
);
```

`CachedProductsStore` is a real module, not a pass-through wrapper. It owns:
cache-key construction, TTL policy, eviction rules, and load-through semantics
behind `getOrLoad`. The interface (`ProductsStore`) is identical to the
underlying store — that is correct here, because this is the decorator case
called out in Check 4 as legitimate. Each implementation adds distinct
functionality: the cache version adds memoization and invalidation that
callers cannot see and do not manage.

If `CachedProductsStore` ever shrinks to forwarding without adding behavior
(no TTL choices, no eviction logic, no stampede protection — just a `get` and
`set`), it has degraded into a pass-through wrapper and should be deleted in
favor of using `cache` directly inside `PostgresProductsStore`.

---

## Example 3 — Stampede protection inside the cache, not at call sites

A high-traffic product page caches an expensive `featuredProducts` query for
10 minutes. When the cache key expires, a hundred concurrent requests all
miss, all hit the database, and the system briefly tips over. The tactical
fix at the call site:

```typescript
// in the service
async function featuredProducts(): Promise<Product[]> {
    const cached = await cache.get('featured');
    if (cached) return cached;
    if (await mutex.tryAcquire('featured:lock', 30)) {
        try {
            const fresh = await expensiveQuery();
            await cache.set('featured', fresh, 600);
            return fresh;
        } finally { await mutex.release('featured:lock'); }
    }
    // ...wait and retry? return stale? hard to decide here
}
```

Three things wrong:

- The same locking dance now has to live at every cache call site that risks
  a stampede.
- The "what to do while another caller is loading" decision is made at the
  call site, where the author has the least context. (Wait? Return stale?
  Return null?)
- A bug in the lock release path takes out the cache for thirty seconds for
  every key that uses this pattern.

This belongs inside the cache (Check 3, pull complexity down):

```typescript
class Cache {
    async getOrLoad<T>(
        key: string,
        ttlSeconds: number,
        load: () => Promise<T>,
    ): Promise<T> {
        // single-flight: at most one in-flight load per key per process,
        // plus a distributed lock for cross-process coordination
        // returns stale-while-revalidate if a fresh load is already in
        // progress and the previous value is still in the cache
        // ...
    }
}

// call site
const featured = await cache.getOrLoad('featured', 600, () => expensiveQuery());
```

The interface is now `getOrLoad(key, ttl, load)`. The caller writes one line.
Stampede protection, stale-while-revalidate, single-flight per process, and
distributed locking move inside the cache module where they're written once
and right.

Same reasoning as the retry-interval example in `examples.md` Example 2:
parameters the cache can choose better than the caller stay inside the cache.

---

## Example 4 — Invalidation owned by the data module, not by callers

A reporting service writes a row to `events` and then carefully invalidates
six cache keys that derive from it:

```go
func (s *EventsService) Record(ev Event) error {
    if err := s.repo.Insert(ev); err != nil { return err }
    s.cache.Delete(fmt.Sprintf("daily_count:%s", ev.Date()))
    s.cache.Delete(fmt.Sprintf("weekly_count:%s", ev.Week()))
    s.cache.Delete(fmt.Sprintf("user_events:%s", ev.UserID))
    s.cache.Delete(fmt.Sprintf("org_events:%s", ev.OrgID))
    s.cache.Delete(fmt.Sprintf("daily_uniques:%s", ev.Date()))
    s.cache.Delete("global_today")
    return nil
}
```

The list looks like a precondition that every writer must remember. It is —
and the same list will need to be replicated in every batch importer, every
admin tool that injects events, every migration that backfills. Six caches
deriving from one table is a deliberate design decision, and the decision is
currently encoded nowhere callers can trust.

Move the decision into the events module:

```go
type EventsRepository struct {
    inner EventsStore
    cache Cache
}

func (r *EventsRepository) Insert(ev Event) error {
    if err := r.inner.Insert(ev); err != nil { return err }
    r.evictDerivedFrom(ev)
    return nil
}

func (r *EventsRepository) evictDerivedFrom(ev Event) { ... }
```

Now there is one place that knows what derivations exist. Adding a new
derived view adds an entry there, not edits to every writer. The batch
importer and the admin tool call `Insert` and get correct invalidation
automatically.

For higher-volume systems this same logic moves to an event/CDC stream and a
worker that invalidates based on database changes. The principle is the same:
invalidation is a decision; one module owns it; callers don't carry the
list.

---

## Where the cache should sit

| Layer | Use the cache here? |
|---|---|
| HTTP/edge (CDN, reverse proxy) | Yes — for cacheable responses. Owned by infra, not application code. |
| Controller/handler | Almost never. Cache logic in handlers is the scattered antipattern of Example 1. |
| Service | Rarely. Use it here only if the cached value is a service-specific composition that no repository would own. |
| Repository / data store | The default home. The repository already owns the data contract; caching is part of that contract. |
| Inside a domain method | Only for derived/computed values, and behind a clear function (`memoize` style). Not for I/O. |

The phrase "we should cache this" usually means "the repository serving this
should have a caching implementation." Reach for the lower layer first.
