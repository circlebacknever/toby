# Worked Examples — Databases and Data Access

The data layer is where both "naturally efficient design" and "death by a
thousand cuts" happen. Get the structural choices right (where the
joins happen, how transactions retry, what the indexes are) and the
system runs fast without per-query tuning. If those choices are wrong,
caller-side tuning cannot make the system fast.

---

## Example 1 — N+1: a design-time problem

Here is a common growth pattern:

```python
orders = order_repo.recent_for_customer(customer_id, limit=50)
for o in orders:
    print(o.shipping_address.city)        # this runs one query per order, which is N+1
    for li in o.line_items:                # this is another N+1
        print(li.product.name)              # this is another N+1
```

For 50 orders with 5 line items each, the code runs 1 query to load orders, 50 queries
for addresses, 50 queries for line items, 250 queries for products. That is 351
queries to render a list. P99 latency is bad even though no single query
is "slow."

The N+1 loop is the death-by-a-thousand-cuts case from the SKILL, because no profiler
will show one expensive call. The fundamental fix is at the design level.

The fixes below are in roughly increasing complexity:

**Eager load via the ORM (cheapest).** Tell the ORM to join when fetching:

```python
orders = (
    session.query(Order)
    .options(
        joinedload(Order.shipping_address),
        selectinload(Order.line_items).selectinload(LineItem.product),
    )
    .filter(Order.customer_id == customer_id)
    .order_by(Order.created_at.desc())
    .limit(50)
    .all()
)
```

The code runs one query for orders + addresses (joinedload), one query for all
line_items (selectinload by order ids), one query for all products
(selectinload by product ids). The query count drops from 351 to 3. The code is
the same as before, except for the eager-load hint.

**Purpose-built read model.** If the list view always needs the same
fields, build a query that returns them directly:

```python
def list_orders_for_display(customer_id):
    """Returns a flat OrderDisplay row per order, with all fields needed
    for the list view. It runs one query."""
    # SELECT order fields + address.city + line items aggregated as a JSON column
```

The repository returns `list[OrderDisplay]`, which is a flat dataclass with
exactly the fields the list view needs. Callers can't trigger N+1 because
the fields aren't relations.

**CQRS-style read store** (most complex, so reserve it for measured need). Keep
a separate denormalized table, update it on writes, and query it directly. A read
store is useful at scale when even the joined query is too slow, but it is almost
never the right first move.

The design-time choice of eager-load hints or purpose-built read models
costs no more complexity than the slow version. The default of "let the
ORM lazy-load whatever I touch" is what produces the N+1. Explicit
eager-loading is the naturally-efficient simple choice.

---

## Example 2 — Transaction retry: mask deadlocks at the wrapper

Concurrent updates in any RDBMS will produce occasional deadlocks. The
database aborts one transaction, and the application is expected to retry.

Here is the tactical code:

```go
err := db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Save(&order).Error; err != nil { return err }
    if err := tx.Update(...).Error; err != nil { return err }
    return nil
})
if err != nil {
    if isDeadlock(err) {
        // this repeats a copy of the whole transaction
        err = db.Transaction(func(tx *gorm.DB) error { ... })
    }
    return err
}
```

The tactical code is wrong at multiple levels. The deadlock-retry logic is repeated at every call
site. Subtle bugs (forgetting the retry, retrying the wrong errors,
retrying mutations that weren't idempotent) repeat across the codebase.

Mask the transient at the wrapper (rung 2):

```go
func WithRetry(ctx context.Context, db *gorm.DB, fn func(tx *gorm.DB) error) error {
    const maxAttempts = 5
    for attempt := 1; ; attempt++ {
        err := db.WithContext(ctx).Transaction(fn)
        if err == nil { return nil }
        if !isTransient(err) || attempt >= maxAttempts {
            return err
        }
        if err := sleepCtx(ctx, jitteredBackoff(attempt)); err != nil { return err }
    }
}

func isTransient(err error) bool {
    return errors.Is(err, ErrDeadlock) ||
           errors.Is(err, ErrSerializationFailure) ||
           errors.Is(err, ErrConnReset)
}
```

Every transactional call site uses `WithRetry`:

```go
err := WithRetry(ctx, db, func(tx *gorm.DB) error {
    if err := tx.Save(&order).Error; err != nil { return err }
    if err := tx.Update(...).Error; err != nil { return err }
    return nil
})
```

The wrapper gives one retry policy, one place that defines what's transient, and
jittered backoff so retries don't synchronize. Callers only see deadlocks that
persist through 5 attempts, because the wrapper masks routine ones.

Guardrail: the transaction body must be idempotent or fully transactional
with no side effects outside the database (no email sends, no API calls
inside the transaction). The retry mechanism assumes "running this again
is safe." A transaction that calls `sendEmail` and then writes to the DB
will send the email twice when the retry succeeds. Move side effects
outside the retried block.

Second guardrail: do the reads inside `fn`. A deadlock or serialization
failure rolls the transaction back, so the snapshot the body computed against
is gone. If `fn` closes over rows read before `WithRetry`
and writes values derived from them, each retry re-applies a stale
computation against data that has since changed. The result is a lost update
that commits without error. Read the rows, compute, and write inside `fn`, so every attempt
starts from what the database currently holds.

---

## Example 3 — Bulk operations: one round trip vs N

Here is a common growth pattern:

```python
for user_id in user_ids:
    db.execute("UPDATE users SET last_seen = NOW() WHERE id = ?", user_id)
```

500 user IDs mean 500 round trips to the database. Each round trip is a few
milliseconds. The whole operation is several seconds for what should be
a single statement.

Here is the naturally-efficient version:

```python
db.execute(
    "UPDATE users SET last_seen = NOW() WHERE id = ANY(?)",
    user_ids,
)
```

The bulk version runs one statement in one round trip and takes milliseconds.
It is no more complex than the loop version. In most languages and ORMs it's
shorter.

The same fix applies to inserts:

```python
# Tactical
for order in orders:
    db.execute("INSERT INTO orders (...) VALUES (...)", order)

# Naturally-efficient
db.execute_many(
    "INSERT INTO orders (...) VALUES (...)",
    [order.as_row() for order in orders],
)
# or use this form in Postgres specifically
db.execute(
    "INSERT INTO orders (...) VALUES " + ",".join("(...)" for _ in orders),
    flatten_params(orders),
)
```

For very large batches (10k+ rows in a single insert), insert in chunks
of 1000 or so. Chunking avoids blocking the database with a single huge
statement. The chunking logic is inside the bulk method, which keeps
every caller free of it.

For Postgres specifically, `COPY` is dramatically faster than INSERT for
very large bulk loads (10k+ rows). For MySQL, use `LOAD DATA INFILE`. Use
these tools only after a measurement shows that a bulk INSERT is the
bottleneck.

---

## Example 4 — Index decisions: design-time work that prevents the slow path

Indexes are the canonical case of "naturally efficient costs no more
complexity than slow." The decision is made when the table or the query
pattern is designed. The cost of getting it wrong shows up months later
as a slow query that requires an urgent production fix.

The three index decisions below are consistently worth their cost:

**Index foreign keys you query by.** A `line_items` table with
`order_id` foreign key should have an index on `order_id` if you ever
look up line items by order. Without the index, "load all line items for
this order" is a full table scan.

```sql
CREATE INDEX idx_line_items_order_id ON line_items (order_id);
```

**Index the columns in your common WHERE/ORDER BY pairs.** A query like
`WHERE customer_id = ? AND status = 'open' ORDER BY created_at DESC` is
best served by `(customer_id, status, created_at DESC)`. The column
order matters, because the index supports `(customer_id)` queries,
`(customer_id, status)` queries, and `(customer_id, status, created_at)`
queries, but not bare `(status)` queries.

**Partial indexes for sparse conditions.** If "open orders" are 5% of
the orders table but most queries are about open orders, a partial index
serves them faster and is smaller:

```sql
CREATE INDEX idx_orders_open ON orders (customer_id, created_at DESC)
WHERE status = 'open';
```

Do not add an index per column "just in case." Indexes have
write cost (every insert/update updates every relevant index) and storage
cost. The right count is the few that serve your real query patterns.

Run `EXPLAIN ANALYZE` on your hot queries before shipping to validate the indexes.
The plan tells you whether the optimizer is using the index you expected.
If it isn't, the index does not match the query, so fix the index
or the query.

Choosing indexes is naturally efficient design-time work. The wrong default
is to create no indexes and add them when something is slow. That default
produces the death-by-thousand-cuts case at scale, when every query is slow
and there's no single index to add. Index choice is a high-consequence decision at the
schema-design stage.

---

## Example 5 — Connection pooling and per-request transactions

In this case, the added complexity is hard to see:

```python
# this code is in a Flask handler
def handler():
    user = session.query(User).filter_by(id=current_user_id).one()
    orders = session.query(Order).filter_by(user_id=user.id).all()
    # ...30 more lines follow, with lots of lazy-load triggers
    return render(...)
```

The implicit transaction held by `session` stays open for the entire request.
If the request takes 500ms because of N+1 queries and a slow renderer,
that connection is held for 500ms. Under high load, the connection pool
exhausts. Every request now waits for a free connection. The system
appears to deadlock, and then new requests get rejected.

Two design-time choices prevent this pool exhaustion:

**Short, scoped transactions.** Don't hold a database connection for
the full request. Open a transaction when you need it, and commit/release
as soon as possible:

```python
def handler():
    with session_scope() as s:
        user = s.query(User).filter_by(id=current_user_id).one()
        orders = s.query(Order).options(joinedload(Order.line_items)).filter_by(user_id=user.id).all()
        user_data = build_user_view(user)
        orders_data = build_orders_view(orders)
    # session is now closed, so rendering doesn't hold a connection
    return render(user_data, orders_data)
```

**A bounded pool with timeouts.** Configure the pool to fail fast when
exhausted, because queuing forever hides the exhaustion as a hang:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=2,        # fail fast if no connection is available within 2s
)
```

A request that can't get a connection in 2 seconds fails, and the caller sees
"service unavailable," which is recoverable. The unbounded version waits
forever in the pool queue, which appears as a hang.

These are the moves to make at design time, but the move driven by
measurement comes later.
If a specific endpoint holds connections too long even after scoping,
profile what it is doing. Usually it's lazy-loading (Example 1
above) or an unexpected slow query.

---

## Example 6 — Concurrency control: where the conflict gets caught

Two transactions read an inventory row, both see one unit left, and both sell it.
Example 2 shows how to retry a conflict once the database raises one. This example answers
the earlier question of how to guard the row so the database detects the conflict
at all. Each of the two strategies below keeps the concurrency control in one place.

**Optimistic — a version column.** The row has a `version`, and the update
asserts it hasn't changed since the read:

```sql
UPDATE inventory SET qty = qty - 1, version = version + 1
WHERE id = $1 AND version = $2;
-- if 0 rows were updated, another writer won, so reload and decide
```

The check is in the WHERE clause, so every writer enforces it identically.
This approach holds no lock, so writers do not wait. Optimistic locking is cheap when conflicts are rare. The
caller handles the 0-row case (reload, maybe retry).

**Pessimistic — lock the row.** Take the row's write lock for the rest of the
transaction:

```sql
SELECT qty FROM inventory WHERE id = $1 FOR UPDATE;  -- concurrent writers block here
-- decide, then UPDATE. The lock releases at commit
```

Locking is correct under heavy contention, where optimistic retries would
thrash. Its cost is a held lock, so keep the transaction short and touch rows
in a consistent order. Otherwise, locking replaces the lost-update race with a deadlock.

Isolation level is a further safeguard under both strategies. `READ COMMITTED`, the common
default, permits the read-then-write race above, which is why one of the two
guards is needed. `SERIALIZABLE` makes the database detect the interleaving
and abort one transaction. It is the strictest model, but it causes more aborts
to retry (back to Example 2). Pick one strategy per contended resource and hold
to it. Mixing optimistic and pessimistic access to the same row allows the
race each was meant to prevent.

---

## Cheat sheet — database complexity

| Symptom | Move |
|---|---|
| Loop of queries (N+1) | Eager-load with hints or purpose-built read model |
| Deadlock-retry logic at every call site | One `WithRetry` wrapper; idempotent transaction bodies |
| Loop of single-row INSERTs/UPDATEs | Batch operation; one statement |
| Slow query in production | EXPLAIN first; usually a missing index or bad query plan |
| Connection pool exhausted | Short scoped transactions; pool_timeout to fail fast |
| Lost update under concurrent writes | Version column (optimistic) or `SELECT … FOR UPDATE` (pessimistic); one per resource |
| Index added "just in case" | Don't; index for measured query patterns only |
