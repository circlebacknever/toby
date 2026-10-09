# Deploys

This file covers data that two releases share. During a rolling deploy, the previous release runs beside this one. After a rollback, the previous release reads what this one wrote. Each release must read what the other writes, including messages already queued and entries already cached.

- Add a field to a message or a stored record as optional, with a default where it is read.
- Ship code that reads a new value in an existing field, such as a new enum member, one release before code that writes it.
- When a cached value's format changes, change its cache key, such as `user:v2:{id}`. Ship code that evicts both keys on every write one release before the code that reads the new key. Give both keys a TTL. A single instance that stops before the new release starts can change the cache key in one release. The TTL bounds stale reads after a rollback.
- Build an index concurrently where the database supports it, such as `CREATE INDEX CONCURRENTLY` in Postgres, in a migration that runs outside a transaction.
- Run a backfill in batches outside the migration's transaction, so it holds no long lock on the table.
- Skip the two bullets above for a table this change creates. Skip them too when the user or the repo shows the production table stays under a few thousand rows. On such a table, a plain `CREATE INDEX` and one `UPDATE` inside the migration lock it for milliseconds. When the production row count is unknown, apply both bullets, because a dev database's row count does not show it.

## Breaking schema changes

Use the releases below when a deploy runs two releases at once, such as a rolling or blue-green deploy. Use them also when a rollback skips the down migration. A single instance that stops before the new release starts can ship the change in one release, with a tested down migration.

Ship a column rename in these releases, so each one works beside the release before it:

1. Add the new column, and write both columns.
2. After release 1 is live, backfill the new column in batches. Copy inside the database with one statement per batch, and skip rows release 1 already wrote, such as `UPDATE users SET new_col = old_col WHERE id BETWEEN $1 AND $2 AND new_col IS NULL`. Then ship the code that reads the new column.
3. Write only the new column. Remove the old column from the model, such as with Rails `ignored_columns`, and make it nullable when new rows leave it empty.
4. Drop the old column.
