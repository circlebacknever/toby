# Caching

## Get-or-load

A `get`/`set`/`delete` cache needs a seven-sentence comment, because the caller must coordinate concurrent misses, serialize to JSON, and allow for fuzzy TTLs. Make load-through the only read:

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

`get` and `set` stay private, because public ones lead each caller to write its own miss handling. Cache warming, the one case that needs a write with no load, gets an explicit `warm(key, value, ttl)`.

## Typed keys

`invalidate(key: string)` accepts any string, so `products:${id}` in one file and `product:${id}` in another both compile. Put the key constructors inside a per-domain cache module:

```ts
class ProductsCache {
    constructor(private cache: Cache) {}
    private productKey(id: string)       { return `product:${id}`; }
    private listingKey(category: string) { return `product:listing:${category}`; }

    getProduct(id: string, load: () => Promise<Product | null>) {
        return this.cache.getOrLoad(this.productKey(id), 600, load);
    }
    async invalidateProduct(p: Product) {
        await this.cache.invalidate(this.productKey(p.id));
        await this.cache.invalidate(this.listingKey(p.category));
    }
}
```

Callers never write a key, a misspelled method fails to compile, and a key-scheme version bump changes one file.

## Outage behavior

What `getOrLoad` does when the cache server is down is part of its contract, so state it:

```ts
/**
 * Returns the cached value or loads it via the supplied function.
 * If the cache is unavailable, calls load() directly and does not cache
 * the result. Cache outages are reported through metrics and never thrown
 * to callers. The cache never returns stale data.
 */
```

Callers then write no defensive code, and the metrics show the outage, during which every read reaches the store. Where a degraded read must be a deliberate choice, such as financial data, return `Result<T, CacheUnavailable>`. Stale-while-revalidate is a third choice, and its comment states the maximum age a caller can receive.
