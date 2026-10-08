# Caching

## Get-or-load

A cache with separate `get`, `set`, and `delete` methods needs a seven-sentence comment. Each caller must handle two requests that miss the same cache key at the same moment. Each caller must also convert values to JSON and allow for expiry times that are not exact. Make the only read method one that loads and caches the value when the value is missing:

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

`get` and `set` stay private, because public ones lead each caller to write its own miss handling. Cache warming fills the cache ahead of time. Warming is the one case that writes a value without loading it, so warming gets its own `warm(key, value, ttl)` method.

## Typed keys

`invalidate(key: string)` accepts any string, so `products:${id}` in one file and `product:${id}` in another both compile. Put the functions that build cache keys inside one cache class for each kind of data, such as products:

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

Callers never write a cache key, and a misspelled method name fails to compile. A change to the cache key format, such as a new version prefix, edits one file.

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

Callers then need no error handling for cache outages. The metrics show the outage, and during the outage every read goes to the database or other backing store. Sometimes the caller must decide whether to read without the cache, as with financial data. In that case, return `Result<T, CacheUnavailable>`. A third choice is stale-while-revalidate, which returns the old cached value while it loads a new one. A stale-while-revalidate comment states the oldest data a caller can get.
