# Worked Examples — Databases and Data Access

The data layer is where "naturally efficient design" and "death by a
thousand cuts" both live. Get the structural choices right (where the
joins happen, how transactions retry, what the indexes are) and the
system runs fast without per-query heroics. Get them wrong and no amount
of caller-side tuning will save you.

---

## Example 1 — N+1: a design-time problem

A common growth pattern:

```python
orders = order_repo.recent_for_customer(customer_id, limit=50)
for o in orders:
    print(o.shipping_address.city)        # one query per order — N+1
    for li in o.line_items:                # another N+1
        print(li.product.name)              # another N+1
```

For 50 orders with 5 line items each: 1 query to load orders, 50 queries
for addresses, 50 queries for line items, 250 queries for products. 351
queries to render a list. P99 latency is bad even though no single query
is "slow."

This is the death-by-a-thousand-cuts case from the SKILL — no profiler will
show one expensive call. The fundamental fix is at the design level.

Three ways out, in roughly increasing complexity:

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

One query for orders + addresses (joinedload), one query for all
line_items (selectinload by order ids), one query for all products
(selectinload by product ids). 351 queries → 3. Same code shape as
before; the eager-load hint is the only change.

**Purpose-built read model.** If the list view always needs the same
shape, build a query that returns it directly:

```python
def list_orders_for_display(customer_id):
    """Returns a flat OrderDisplay row per order, with all fields needed
    for the list view. One query."""
    # SELECT order fields + address.city + line items aggregated as a JSON column
```

The repository returns `list[OrderDisplay]` — a flat dataclass with
exactly the fields the list view needs. Callers can't trigger N+1 because
the fields aren't relations.

**CQRS-style read store** (most complex; reserve for measured need). Keep
a separate denormalized table updated on writes, queried directly. Useful
at scale when even the joined query is too slow. Almost never the right
first move.

The design-time choice — eager-load hints, purpose-built read models —
costs no more complexity than the slow version. The default of "let the
ORM lazy-load whatever I touch" is what produces the N+1; explicit
eager-loading is the naturally-efficient simple choice.

---

## Example 2 — Transaction retry: mask deadlocks at the wrapper

Concurrent updates in any RDBMS will produce occasional deadlocks. The
database aborts one transaction; the application is expected to retry.

Tactical code:

```go
err := db.Transaction(func(tx *gorm.DB) error {
    if err := tx.Save(&order).Error; err != nil { return err }
    if err := tx.Update(...).Error; err != nil { return err }
    return nil
})
if err != nil {
    if isDeadlock(err) {
        // copy of the whole transaction repeated below
        err = db.Transaction(func(tx *gorm.DB) error { ... })
    }
    return err
}
```

Wrong at multiple levels. The deadlock-retry logic lives at every call
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

One retry policy, one place that knows what's transient, jittered backoff
so retries don't synchronize. Callers see the deadlocks they actually need
to surface (after 5 attempts, still failing) and not the routine ones.

Guardrail: the transaction body must be idempotent or fully transactional
with no side effects outside the database (no email sends, no API calls
inside the transaction). The retry mechanism assumes "running this again
is safe." A transaction that calls `sendEmail` and then writes to the DB
will send the email twice when the retry succeeds. Move side effects
outside the retried block.

---

## Example 3 — Bulk operations: one round trip vs N

A common growth pattern:

```python
for user_id in user_ids:
    db.execute("UPDATE users SET last_seen = NOW() WHERE id = ?", user_id)
```

500 user IDs, 500 round trips to the database. Each round trip is a few
milliseconds. The whole operation is several seconds for what should be
a single statement.

The naturally-efficient version:

```python
db.execute(
    "UPDATE users SET last_seen = NOW() WHERE id = ANY(?)",
    user_ids,
)
```

One statement, one round trip, milliseconds. The bulk version is no more
complex than the loop version; in most languages and ORMs it's actually
shorter.

For inserts:

```python
# Tactical
for order in orders:
    db.execute("INSERT INTO orders (...) VALUES (...)", order)

# Naturally-efficient
db.execute_many(
    "INSERT INTO orders (...) VALUES (...)",
    [order.as_row() for order in orders],
)
# or in Postgres specifically
db.execute(
    "INSERT INTO orders (...) VALUES " + ",".join("(...)" for _ in orders),
    flatten_params(orders),
)
```

For very large batches (10k+ rows in a single insert), chunk: insert in
batches of 1000 or so to avoid blocking the database with a single huge
statement. The chunking logic lives inside the bulk method, not at every
caller.

For Postgres specifically, `COPY` is dramatically faster than INSERT for
very large bulk loads (10k+ rows). For MySQL, `LOAD DATA INFILE`. These
are escalation tiers — reach for them when measured bulk INSERT is the
bottleneck, not by default.

---

## Example 4 — Index decisions: design-time work that prevents the slow path

Indexes are the canonical case of "naturally efficient costs no more
complexity than slow." The decision is made when the table or the query
pattern is designed. The cost of getting it wrong shows up months later
as a slow query that requires a panicked production fix.

Three index decisions that pay back consistently:

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
order matters; the index supports `(customer_id)` queries, `(customer_id,
status)` queries, and `(customer_id, status, created_at)` queries, but
not bare `(status)` queries.

**Partial indexes for sparse conditions.** If "open orders" are 5% of
the orders table but most queries are about open orders, a partial index
serves them faster and is smaller:

```sql
CREATE INDEX idx_orders_open ON orders (customer_id, created_at DESC)
WHERE status = 'open';
```

What not to do: add an index per column "just in case." Indexes have
write cost (every insert/update updates every relevant index) and storage
cost. The right count is "the few that serve your real query patterns,"
not "all of them."

Measurement validates: `EXPLAIN ANALYZE` your hot queries before shipping.
The plan tells you whether the optimizer is using the index you expected.
If it isn't, the index is the wrong shape for the query — fix the index
or the query.

This is design-time naturally-efficient work. The wrong default — no
indexes, add them when something is slow — produces the death-by-
thousand-cuts case at scale, when every query is slow and there's no
single index to add. Index choice is a load-bearing decision at the
schema-design stage.

---

## Example 5 — Connection pooling and per-request transactions

A subtle case where complexity arrives invisibly:

```python
# in a Flask handler
def handler():
    user = session.query(User).filter_by(id=current_user_id).one()
    orders = session.query(Order).filter_by(user_id=user.id).all()
    # ...30 more lines, lots of lazy-load triggers
    return render(...)
```

The implicit transaction held by `session` lives for the entire request.
If the request takes 500ms because of N+1 queries and a slow renderer,
that connection is held for 500ms. Under high load, the connection pool
exhausts. Every request now waits for a free connection. The system
appears to deadlock; new requests get rejected.

Two design-time choices that prevent this:

**Short, scoped transactions.** Don't hold a database connection for
the full request. Open a transaction when you need it, commit/release
as soon as possible:

```python
def handler():
    with session_scope() as s:
        user = s.query(User).filter_by(id=current_user_id).one()
        orders = s.query(Order).options(joinedload(Order.line_items)).filter_by(user_id=user.id).all()
        user_data = build_user_view(user)
        orders_data = build_orders_view(orders)
    # session is now closed; rendering doesn't hold a connection
    return render(user_data, orders_data)
```

**A bounded pool with timeouts.** Configure the pool to fail fast when
exhausted, rather than queue forever:

```python
engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_timeout=2,        # fail fast if no connection available within 2s
)
```

A request that can't get a connection in 2 seconds fails — caller sees
"service unavailable," which is recoverable, instead of waiting forever
in the pool queue, which appears as a hang.

These are the design-time moves. The measurement-driven move comes later
— if a specific endpoint holds connections too long even after scoping,
profile what it's actually doing. Usually it's lazy-loading (Example 1
above) or an unexpected slow query.

---

## Cheat sheet — database complexity

| Symptom | Move |
|---|---|
| Loop of queries (N+1) | Eager-load with hints or purpose-built read model |
| Deadlock-retry logic at every call site | One `WithRetry` wrapper; idempotent transaction bodies |
| Loop of single-row INSERTs/UPDATEs | Batch operation; one statement |
| Slow query in production | EXPLAIN first; usually a missing index or bad query plan |
| Connection pool exhausted | Short scoped transactions; pool_timeout to fail fast |
| Index added "just in case" | Don't; index for measured query patterns only |
