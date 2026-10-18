# Caching

## Get-or-load

A cache with separate `get`, `set`, and `delete` methods forces every caller to handle concurrent misses, JSON serialization, and TTLs. Expose a single read method that loads and caches the value on a miss:

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

Keep raw `get` and `set` private, and add a `warm(key, value, ttl)` method only when pre-populating the cache ahead of traffic.

## Typed keys

`invalidate(key: string)` accepts any string, so `products:${id}` in one file and `product:${id}` in another both compile. Put the functions that build cache keys inside one cache class for each domain:

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

Callers never build a `cache key` string, and changing the key format edits one file.

## Outage behavior

State in `getOrLoad`'s comment what happens when the cache server is unreachable:

```ts
/**
 * Returns the cached value or loads it via the supplied function.
 * If the cache is unavailable, calls load() directly and does not cache
 * the result. getOrLoad reports cache outages through metrics and never
 * throws them to callers. The cache never returns stale data.
 */
```

When callers must know that the cache is down before hitting the database, return `Result<T, CacheUnavailable>`. When using stale-while-revalidate, state the maximum age of stale data in the comment.
