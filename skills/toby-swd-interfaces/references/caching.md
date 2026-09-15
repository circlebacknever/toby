# Worked Examples — Caching

The cache's interface determines how much of the caching mechanism leaks
into the rest of the system. The default `get/set/delete` interface looks
harmless, but it is the most common source of cache misuse in growing
codebases.

---

## Example 1 — Cache interface: get/set/delete vs get-or-load

Here is the "obvious" interface:

```ts
interface Cache {
    get<T>(key: string): Promise<T | null>;
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    delete(key: string): Promise<void>;
}
```

Here is the complete comment:

> A typed key/value cache. get returns the cached value or null if not
> present or expired. set stores the value with the given TTL (default
> from the cache configuration if unset). delete removes the value. Note
> that ttlSeconds is enforced approximately; values may live up to a few
> seconds longer due to clock skew across cache nodes. Concurrent get on
> a missing key by N callers results in N independent loads — callers
> should coordinate misses themselves if loading is expensive. The cache
> does not serialize complex types beyond JSON; non-serializable objects
> in set produce undefined behavior.

The comment has seven sentences. It gives the caller three obligations
(load-on-miss coordination, JSON-only values, TTL fuzziness). The interface
only wraps Redis, when it should handle caching for this app.

In the deeper interface, the cache coordinates
load-on-miss itself, so the caller never does:

```ts
interface Cache {
    /**
     * Returns the cached value for the key, or loads it via the supplied
     * function and caches the result. At most one load runs per key per
     * process, so concurrent waiters share the result. ttl is the freshness
     * window in seconds.
     */
    getOrLoad<T>(key: string, ttlSeconds: number, load: () => Promise<T>): Promise<T>;

    /** Removes the cached value for the key, if any. */
    invalidate(key: string): Promise<void>;
}
```

The comment for `getOrLoad` is the four-sentence docstring above. It gives
the caller no load-on-miss coordination obligation. The cache handles single-flight per process (and
optionally a distributed lock for cross-process coordination), so the
caller writes one line.

`get` and `set` are gone from the interface. They are useful internally
to implement `getOrLoad`, but public `get` and `set` lead callers into the
scattered-cache antipattern. The narrower public interface forces callers
into the load-through pattern, which is what they wanted anyway.

The guardrail still applies, because rare cases legitimately need `set`
without an associated load (precomputed cache warming, for example). Expose a `warm(key, value,
ttl)` method that explicitly signals the intent. The mechanism (`set`)
remains hidden, so callers see only the `warm` operation in the contract.

---

## Example 2 — Invalidation as part of the data interface

Here is a common attempt at tidy separation:

```ts
class ProductsService {
    constructor(private store: ProductsStore, private cache: Cache) {}

    async getProduct(id: string): Promise<Product | null> {
        return this.cache.getOrLoad(`product:${id}`, 600, () => this.store.find(id));
    }

    async updateProduct(id: string, changes: Partial<Product>): Promise<Product> {
        const updated = await this.store.update(id, changes);
        await this.cache.invalidate(`product:${id}`);                    // remember!
        await this.cache.invalidate(`product:listing:${updated.category}`); // and this!
        return updated;
    }
}
```

The service's interface (`getProduct`, `updateProduct`) looks fine
. The hidden contract is that callers of the underlying
`ProductsStore` must not bypass this service, or cached data goes stale.
That bypass rule is an implicit caller obligation that is not stated in any
interface.

Worse, the `updateProduct` author maintains a list of cache keys to
invalidate. When someone adds the next derived view (a
`product:by_brand:${brand}` cache, say), they must edit every mutating method
that could affect that derivation.

The failure is that invalidation is a property of the data, but the
code implements it as a property of the service. The cache's interface offers
`invalidate(key)`, so the service code keeps the list of keys.

Redesign by moving the cache into the data layer:

```ts
interface ProductsStore {
    find(id: string): Promise<Product | null>;
    listing(category: string): Promise<Product[]>;
    save(p: Product): Promise<void>;
}

class CachedProductsStore implements ProductsStore {
    constructor(private inner: ProductsStore, private cache: Cache) {}

    async find(id: string) {
        return this.cache.getOrLoad(`product:${id}`, 600,
            () => this.inner.find(id));
    }
    async listing(category: string) {
        return this.cache.getOrLoad(`product:listing:${category}`, 60,
            () => this.inner.listing(category));
    }
    async save(p: Product) {
        await this.inner.save(p);
        await this.evictDerivedFrom(p);
    }

    private async evictDerivedFrom(p: Product) {
        await this.cache.invalidate(`product:${p.id}`);
        await this.cache.invalidate(`product:listing:${p.category}`);
    }
}
```

The service goes back to calling `products.find(id)` and
`products.save(updated)`. The cache keeps the same interface, so only
*who calls it* changed. `CachedProductsStore` is the one module that
contains the products' caching scheme. Adding a new derived view adds an
entry to `evictDerivedFrom`, in one place.

The data interface (`ProductsStore`) has the same comment as before:

> Stores and retrieves products. Operations are atomic. Reads may be
> served from cache.

The redesign changed the *composition*,
because it moved the cache from a peer of the service to a decorator of
the store. The same pattern recurs in other code. When an interface's natural
operation has a side effect on a peer module, the side effect belongs
*inside* whichever module makes the underlying decision. Never give it to the
caller.

---

## Example 3 — Cache key as an interface element

The naive cache treats keys as strings. Most caches expose string keys, and
string keys are where typos and version mismatches happen:

```ts
// in productsService.ts
this.cache.invalidate(`product:${p.id}`);

// in adminTools.ts
await cache.invalidate(`products:${id}`);     // typo — plural

// in reports.ts
await cache.invalidate(`product:listing:${oldCategory}`);  // forgot the new category
```

The `Cache.invalidate(key: string)` interface accepts any string. The
keying convention is documented nowhere, so three different
modules can each get the key wrong.

The redesign treats keys as typed values that the cache layer issues:

```ts
class ProductsCache {
    constructor(private cache: Cache) {}

    // Callers must use these key constructors.
    private productKey(id: string)        { return `product:${id}`; }
    private listingKey(category: string)  { return `product:listing:${category}`; }

    async getProduct(id: string, load: () => Promise<Product | null>) {
        return this.cache.getOrLoad(this.productKey(id), 600, load);
    }
    async invalidateProduct(p: Product) {
        await this.cache.invalidate(this.productKey(p.id));
        await this.cache.invalidate(this.listingKey(p.category));
    }
}
```

The key scheme is now a private detail of `ProductsCache`. Callers never
write a string. Typos at the call site fail at compile time
(no method by that name). Version bumps to the key scheme happen in one
file.

The comment for `ProductsCache.getProduct` reads:

> Returns the cached product, or loads it via the supplied function and
> caches the result.

The comment is one sentence. The keying convention does not appear
anywhere callers can see.

This redesign follows the same pattern as `databases.md` Example 1 (ORM
exposed vs intent methods). The redesign replaced the shallow interface's string with
a typed identity in the deep interface.

---

## Example 4 — Cache failure semantics in the interface

Designs often skip the question of what happens when the cache itself is down.

```ts
async function getProduct(id: string): Promise<Product | null> {
    return cache.getOrLoad(`product:${id}`, 600, () => store.find(id));
}
```

If `cache.getOrLoad` throws when Redis is unreachable, the caller now
must handle "Redis is down" as a failure mode for what looks like a
product fetch. If `cache.getOrLoad` silently falls back to calling
`load` directly, the caller doesn't know the cache is failing. The
database then receives a large volume of cache misses, which is a different failure.

The choice is part of the interface, so document it:

```ts
interface Cache {
    /**
     * Returns the cached value or loads it via the supplied function.
     * If the cache itself is unavailable, calls load() directly and
     * does not cache the result. Cache outages are surfaced via metrics
     * and the optional onCacheError callback and are never thrown as exceptions to
     * callers. The cache never returns stale data. If it cannot serve a
     * value, it loads fresh.
     */
    getOrLoad<T>(key: string, ttl: number, load: () => Promise<T>): Promise<T>;
}
```

The comment has three sentences. Silent handling of cache failures is part
of the contract, so callers do not write defensive code. The cache layer
commits to handling its own outages. This failure behavior is the kind of
caller-facing information that, under the guardrail (step 7 of the procedure), you keep in
the interface. `getOrLoad` promises graceful degradation during a cache
outage, and that promise has to be visible.

The alternative interface, which surfaces outages explicitly, is also
valid for systems where degraded reads need to be a deliberate decision
(financial data, for instance):

```ts
interface CacheStrict {
    getOrLoad<T>(key: string, ttl: number, load: () => Promise<T>): Promise<Result<T, CacheUnavailable>>;
}
```

The same comment test applies. Whichever choice you make, state it in the contract. Stale-while-revalidate is a third documented choice.
It serves a bounded-age value while a background load refreshes it, so the
"never stale" line above no longer holds. The staleness window becomes part
of the contract, the same way the rule about calling `load()` directly does.
Callers can rely on a freshness guarantee only when the comment states it.

---

## Cheat sheet — caching interfaces

| Smell | Redesign |
|---|---|
| `Cache.get(key)` + `Cache.set(key, val, ttl)` exposed to callers | Single `getOrLoad(key, ttl, load)` plus rare `warm` |
| Cache invalidation list maintained in service code | Move cache into the data layer so invalidation is internal |
| String keys constructed at every call site | Typed cache module with private key constructors |
| Caller checks `cache.get()` then chooses what to do on miss | Make load-through the default so the cache handles the miss |
| Cache failure surfaced as exceptions to every caller | Fall-through with metrics, and the cache handles the outage |
| Same key written by two unrelated modules | Cache kept inside the data module that produces the key |
