# Deploys

This file covers schema, cache, and message changes across releases. During a rolling deploy or rollback, the previous release and the new release run against the same database, cache, and queues at the same time.

- Add new fields to messages and stored records as optional, with a default in readers.
- Ship code that reads a new enum value one release before shipping code that writes it.
- When a cached value's format changes, bump the version in its `cache key` (such as `user:v2:{id}`), give both `cache key` versions a TTL, and evict both on writes during the transition.
- Set a short `lock_timeout` (such as `SET lock_timeout = '2s'` in Postgres) on DDL migrations against existing tables so a blocked lock fails fast and doesn't queue every query on the table.
- Build indexes concurrently (`CREATE INDEX CONCURRENTLY` in Postgres) outside a transaction, and run data backfills in batches outside the schema migration transaction, unless the table is newly created in the same migration or confirmed to stay under a few thousand rows in production.

## Breaking schema changes

When two releases run concurrently or rollbacks skip down migrations, ship a column rename or type change across four releases (a single-instance app that stops before starting the new release can combine them with a tested down migration):

1. Add the new column (nullable) and write both the old and new columns.
2. Backfill the new column in batches (`UPDATE users SET new_col = old_col WHERE id BETWEEN $1 AND $2 AND new_col IS NULL`), then deploy code that reads the new column.
3. Stop writing the old column, mark it ignored in the ORM (`ignored_columns` in Rails), and ensure it is nullable.
4. Drop the old column in a subsequent deploy.
