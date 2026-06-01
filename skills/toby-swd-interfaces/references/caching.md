# Worked Examples — Caching

The cache's interface determines how much of the caching mechanism leaks
into the rest of the system. The default `get/set/delete` surface looks
innocuous and is the most common source of cache misuse in growing
codebases.

---

## Example 1 — Cache interface: get/set/delete vs get-or-load

The "obvious" interface:

```ts
interface Cache {
    get<T>(key: string): Promise<T | null>;
    set<T>(key: string, value: T, ttlSeconds?: number): Promise<void>;
    delete(key: string): Promise<void>;
}
```

Comment, complete:

> A typed key/value cache. get returns the cached value or null if not
> present or expired. set stores the value with the given TTL (default
> from the cache configuration if unset). delete removes the value. Note
> that ttlSeconds is enforced approximately; values may live up to a few
> seconds longer due to clock skew across cache nodes. Concurrent get on
> a missing key by N callers results in N independent loads — callers
> should coordinate misses themselves if loading is expensive. The cache
> does not serialize complex types beyond JSON; non-serializable objects
> in set produce undefined behavior.

Seven sentences. Three caller obligations (load-on-miss coordination,
JSON-only values, TTL fuzziness). The interface is at the level of "wraps
Redis," not at the level of "owns caching for this app."

The deeper interface inverts the contract — instead of asking the caller
to coordinate load-on-miss, the cache does it:

```ts
interface Cache {
    /**
     * Returns the cached value for the key, or loads it via the supplied
     * function and caches the result. At most one load runs per key per
     * process; concurrent waiters share the result. ttl is the freshness
     * window in seconds.
     */
    getOrLoad<T>(key: string, ttlSeconds: number, load: () => Promise<T>): Promise<T>;

    /** Removes the cached value for the key, if any. */
    invalidate(key: string): Promise<void>;
}
```

Comment for `getOrLoad`: four sentences (the docstring above). No load-on-miss
coordination obligation. The cache owns single-flight per process (and
optionally a distributed lock for cross-process coordination) — the
caller writes one line.

`get` and `set` are gone from the interface. They are useful internally
to implement `getOrLoad`, but as public methods they invite the
scattered-cache antipattern. The narrower public surface forces callers
into the load-through pattern, which is what they wanted anyway.

Guardrail: rare cases legitimately need `set` without an associated load
(precomputed cache warming, for example). Expose a `warm(key, value,
ttl)` method that explicitly signals the intent. The mechanism (`set`)
remains hidden; the operation (`warm`) is the named contract.

---

## Example 2 — Invalidation as part of the data interface, not the cache's

A common attempt at tidy separation:

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

The service's interface (`getProduct`, `updateProduct`) is fine on its
face. The hidden contract is that callers of the underlying
`ProductsStore` must not bypass this service, or cached data goes stale.
That's an implicit caller obligation that doesn't appear in any
interface.

Worse, the `updateProduct` author maintains a list of cache keys to
invalidate. The next derived view (a `product:by_brand:${brand}` cache,
say) means editing every mutating method that could affect that
derivation.

Failure named: invalidation is a property of the data, but it's
implemented as a property of the service. The cache's interface offers
`invalidate(key)` and the service code carries the list of keys.

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
`products.save(updated)`. The cache's interface has not changed; what
changed is *who calls it*. `CachedProductsStore` is the one module that
knows the products' caching scheme. Adding a new derived view adds an
entry to `evictDerivedFrom`, in one place.

The data interface (`ProductsStore`) has the same comment as before:

> Stores and retrieves products. Operations are atomic; reads may be
> served from cache.

The cache interface is unchanged. The redesign was at the *composition*
level — moving the cache from a peer of the service to a decorator of
the store. This is a recurring pattern: when an interface's natural
operation has a side effect on a peer module, the side effect probably
belongs *inside* whichever module owns the underlying decision, not in
the caller.

---

## Example 3 — Cache key as an interface element

The naive cache treats keys as strings. That is the interface most caches
expose, and it's where typos and version mismatches happen:

```ts
// in productsService.ts
this.cache.invalidate(`product:${p.id}`);

// in adminTools.ts
await cache.invalidate(`products:${id}`);     // typo — plural

// in reports.ts
await cache.invalidate(`product:listing:${oldCategory}`);  // forgot the new category
```

The `Cache.invalidate(key: string)` interface accepts any string. The
keying convention is documented nowhere. Three different
modules can each independently get the key wrong.

The redesign treats keys as typed values that the cache layer issues:

```ts
class ProductsCache {
    constructor(private cache: Cache) {}

    // Key constructors that callers must use
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

The key scheme is now a private detail of `ProductsCache`. No caller
writes a string. Typos at the call site fail at compile time
(no method by that name). Version bumps to the key scheme happen in one
file.

Comment for `ProductsCache.getProduct`:

> Returns the cached product, or loads it via the supplied function and
> caches the result.

One sentence. The keying convention does not appear anywhere callers can
see.

This is the same redesign pattern as `databases.md` Example 1 (ORM
exposed vs intent methods). The shallow interface accepted a string;
the deep interface accepts a typed identity.

---

## Example 4 — Cache failure semantics in the interface

The often-skipped question: what happens when the cache itself is down?

```ts
async function getProduct(id: string): Promise<Product | null> {
    return cache.getOrLoad(`product:${id}`, 600, () => store.find(id));
}
```

If `cache.getOrLoad` throws when Redis is unreachable, the caller now
must handle "Redis is down" as a failure mode for what looks like a
product fetch. If `cache.getOrLoad` silently falls back to calling
`load` directly, the caller doesn't know the cache is failing — and a
herd of cache misses hitting the database is a different kind of bad day.

The choice is part of the interface. Document it:

```ts
interface Cache {
    /**
     * Returns the cached value or loads it via the supplied function.
     * If the cache itself is unavailable, falls through to load() and
     * does not cache the result. Cache outages are surfaced via metrics
     * and the optional onCacheError callback, never as exceptions to
     * callers. The cache never returns stale data; if it cannot serve a
     * value, it loads fresh.
     */
    getOrLoad<T>(key: string, ttl: number, load: () => Promise<T>): Promise<T>;
}
```

Three sentences. Cache failure semantics — fall through, don't throw —
are part of the contract, so callers don't write defensive code, and
the cache layer commits to handling its own outages. This is the kind of
caller-facing information the guardrail (step 7 of the procedure)
explicitly preserves: graceful degradation in the face of cache outage
is what `getOrLoad` promises, and that promise has to be visible.

The alternative interface, which surfaces outages explicitly, is also
valid for systems where degraded reads need to be a deliberate decision
(financial data, for instance):

```ts
interface CacheStrict {
    getOrLoad<T>(key: string, ttl: number, load: () => Promise<T>): Promise<Result<T, CacheUnavailable>>;
}
```

Same comment-test discipline applies — whichever choice you make, name
it in the contract.

---

## Cheat sheet — caching interfaces

| Smell | Redesign |
|---|---|
| `Cache.get(key)` + `Cache.set(key, val, ttl)` exposed to callers | Single `getOrLoad(key, ttl, load)` plus rare `warm` |
| Cache invalidation list maintained in service code | Move cache into the data layer; invalidation is internal |
| String keys constructed at every call site | Typed cache module with private key constructors |
| Caller checks `cache.get()` then chooses what to do on miss | The cache should be deciding; load-through is the default |
| Cache failure surfaced as exceptions to every caller | Fall-through with metrics; outage is the cache's problem |
| Same key written by two unrelated modules | Cache owned by the data module that produces the key |
