# Caching

## Cache calls in services

```python
def update_product(product_id: str, changes: dict) -> Product:
    product = product_repo.update(product_id, changes)
    redis.delete(f"product:{product_id}")
    redis.delete(f"product:listing:{product.category}")
    return product
```

When services build keys, pick TTLs, serialize values, and evict keys directly, every new endpoint must repeat every eviction rule or serve stale data. Put the cache inside the repository, or in a wrapper class around the data store:

```typescript
class CachedProductsStore implements ProductsStore {
    constructor(private inner: ProductsStore, private cache: Cache) {}
    find(id: string) {
        return this.cache.getOrLoad(`product:${id}`, 600, () => this.inner.find(id));
    }
    async save(p: Product) {
        await this.inner.save(p);
        await this.evictDerivedFrom(p);   // the one list of derived keys
    }
}
```

A new cached list built from products adds one entry to `evictDerivedFrom`, and any batch importer or admin tool that calls `save` evicts all derived keys automatically. Keep the wrapper class only while it adds caching and eviction, and inline it if it only forwards calls.

Put the lock that prevents concurrent callers from loading the same missing `cache key` inside `getOrLoad`, so call sites never copy lock logic.

## Where to put the cache

| Layer | Use the cache here? |
|---|---|
| HTTP/edge (CDN, reverse proxy) | Yes, for cacheable responses. Infra manages this layer. |
| Controller/handler | Almost never. |
| Service | Only for a combined result that combines multiple repositories. |
| Repository / data store | Yes, by default, because the repository already defines the data contract. |
| Domain method | Only to memoize a pure computed value, never for I/O. |
