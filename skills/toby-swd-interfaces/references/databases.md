# Databases and Data Access

## Repository

A `UserRepository` with `session()`, `query()`, `find_one(*filters)`, `refresh`, and `expunge` exposes SQLAlchemy sessions and `DetachedInstanceError` to callers. Give the repository methods named for what callers want to do:

```python
class UsersRepository:
    """Stores and queries users. All methods return plain domain User objects
    with the relations the operation needs. Methods that change state are
    atomic and return after a durable commit."""

    def find(self, user_id: UserId) -> User | None: ...
    def find_by_email(self, email: str) -> User | None: ...
    def list(self, query: UserQuery) -> Page[User]: ...
    def create(self, draft: NewUser) -> User: ...
    def update_profile(self, user_id: UserId, changes: ProfileChanges) -> User: ...
    def deactivate(self, user_id: UserId, reason: str) -> User: ...
```

> update_profile — Applies the profile changes to the user with this id and returns the updated user. The update is atomic. Returns NotFound if no such user exists. Returns ValidationFailed with field-level reasons if any change is invalid.

`deactivate` writes the audit log and revokes sessions in the same transaction, so the caller doesn't coordinate them. When a repository comment has to mention a session, connection, or cursor, the repository still exposes the database driver to callers.

## Query object

Three candidates for one search method:

- `find(Map<String, Object> filters)` lists the accepted map keys only in a comment, and a value of the wrong type fails only at runtime.
- `find(UUID orgId, boolean active, ...)` uses null to skip a filter, can't skip `active`, and changes every call site when you add a filter.
- `find(UserQuery q)` passes the comment test:

```java
public record UserQuery(Optional<UUID> orgId, Optional<Boolean> active,
                        Optional<Instant> createdAfter, Optional<Set<Role>> roles,
                        int pageSize, Optional<PageToken> pageToken) {
    public UserQuery() { this(empty(), empty(), empty(), empty(), 50, empty()); }
    public UserQuery withOrgId(UUID id) { ... }
}
```

> Returns users matching the query. The method combines set filters with AND, ignores unset filters, and paginates results with a next-page token when more rows exist.

The default constructor keeps the common call short: `users.find(new UserQuery().withOrgId(org))`. The page token encodes a stable cursor, because offset paging repeats or skips a row when rows change mid-iteration. The repository defines what "active" means, and only user searches use `UserQuery`.

## Transactions

An optional `tx?` parameter on every repository method forces every method and comment to forward the transaction. Let the repository look up the active transaction on its own:

```ts
interface UnitOfWork {
    run<T>(work: () => Promise<T>): Promise<T>;
}

async function placeOrder(req: NewOrder, uow: UnitOfWork) {
    return uow.run(async () => {
        const order = await orders.insert(req.toOrder());
        await inventory.reserve(req.items);
        return order;
    });
}
```

Each repository method joins the transaction that `uow.run` started, or opens its own transaction when called outside `uow.run`. A caller that must not publish an event before commit checks `UnitOfWork.isActive()`.

## Migrations

An `upgrade()` that adds a column leaves existing rows `NULL`, and `downgrade()` deletes every value written since the upgrade. Write the migration as three separate methods with one interface comment:

```python
class Migration:
    """A schema change, an idempotent data backfill, and a reverse schema
    step. Migrations run in deploy order, so the application must work with
    every intermediate schema. backfill is safe to re-run. schema_down may
    lose data written after schema_up. A zero-downtime cutover also needs a
    dual-write, dual-read window across two deploys, which this class does
    not express."""

    def schema_up(self): ...
    def backfill(self): ...
    def schema_down(self): ...
```

Write this comment before the migration code so the rollback behavior is explicit.
