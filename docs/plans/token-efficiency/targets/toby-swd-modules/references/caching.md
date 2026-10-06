# Caching

## Cache calls in services

```python
def update_product(product_id: str, changes: dict) -> Product:
    product = product_repo.update(product_id, changes)
    redis.delete(f"product:{product_id}")
    redis.delete(f"product:listing:{product.category}")
    return product
```

Here each service builds keys, picks TTLs, serializes, and evicts, so every service repeats those decisions. A new listing endpoint has to repeat every eviction, and a missed one serves stale data. Put the cache inside the repository, or in a decorator around the store it composes:

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

A new derived view adds one entry to `evictDerivedFrom`, and a batch importer or admin tool that calls `save` evicts correctly with no extra code. The decorator has the same interface as the store, which is correct because it adds memoization and eviction. When it shrinks to forwarding calls, delete it and call the cache from the store. At high write volume, a worker that reads the change stream does the eviction, and still no caller keeps the key list.

Stampede locking also goes inside `getOrLoad`. A call site cannot choose well between waiting, serving stale data, and returning null. When call sites copy the lock, a bug in one copy disables caching for every key that call site reads.

## Where to put the cache

| Layer | Use the cache here? |
|---|---|
| HTTP/edge (CDN, reverse proxy) | Yes, for cacheable responses. Infra manages this layer. |
| Controller/handler | Almost never. |
| Service | Only for a service-specific composition that no repository returns. |
| Repository / data store | Yes, by default, because the repository already defines the data contract. |
| Domain method | Only to memoize a computed value. Never for I/O. |

"We should cache this" usually means the repository serving the data needs a caching implementation.
