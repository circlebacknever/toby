# Databases and Data Access

This file covers N+1 queries, bulk writes, indexes, and connection pools. Open it when a database path is slow.

## N+1 queries

A loop that reads a lazy relation, which the ORM loads only when code first reads it, runs one query per row. 50 orders with 5 line items each take 351 queries, but the profiler shows no single slow query. Pick the cheapest fix that removes the loop:

1. Add eager-load hints to the query that loads the parent rows (`joinedload`, `selectinload`, `include`). 351 queries become 3.
2. When a view always needs the same fields, add a repository method that returns a flat row type with exactly those fields from one query. A caller cannot trigger N+1 on a field that is not a relation.
3. Add a denormalized read table, updated on write, only after a measurement shows the joined query is still too slow.

## Bulk writes

Send a loop of single-row statements as one statement, such as `UPDATE ... WHERE id = ANY(?)` or a multi-row `INSERT`. The bulk write splits its input into batches of about 1,000 rows. Switch to `COPY` (Postgres) or `LOAD DATA INFILE` (MySQL) only after a measurement shows the bulk insert is the bottleneck.

## Indexes

Choose indexes when the table or the query is designed, and check each hot query with `EXPLAIN ANALYZE` before it ships. Build a new index on a table that takes writes with `CREATE INDEX CONCURRENTLY`, in a migration outside a transaction. Run `EXPLAIN ANALYZE` on a write, such as an `UPDATE` or `DELETE`, only between `BEGIN` and `ROLLBACK`, because it executes the statement.

- Index each foreign key the code looks rows up by.
- For `WHERE customer_id = ? AND status = ? ORDER BY created_at DESC`, use `(customer_id, status, created_at DESC)`. It also serves queries on its leading columns, but not a query on `status` alone.
- When most queries ask for a small subset, such as open orders, use a partial index with a `WHERE` clause.
- Add no index without a query that uses it, because every index slows every write.

## Connections

Hold a connection only for the queries. Open the transaction in a `with` scope, build the view data inside it, and render after it closes. Size the pool and give it a short acquire timeout, as the Bounds section of `toby-swd-hardening` says. Then a request returns "service unavailable" when every pooled connection is in use, and never hangs. When an endpoint still holds connections too long, profile it for lazy loads and slow queries.
