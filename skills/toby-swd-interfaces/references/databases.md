# Worked Examples — Databases and Data Access

The data layer has a few stock interfaces, such as repositories, query
builders, transactions, and migrations. The comment test fails on these in
predictable ways, and the redesigns are equally predictable.

---

## Example 1 — Repository interface: ORM exposed vs intent methods

The team accepted this repository sketch without much thought:

```python
class UserRepository:
    def session(self) -> Session: ...
    def query(self) -> Query[User]: ...
    def find_one(self, *filters) -> User | None: ...
    def find_many(self, *filters, order_by=None, limit=None, offset=None) -> list[User]: ...
    def save(self, user: User) -> User: ...
    def delete(self, user: User) -> None: ...
    def refresh(self, user: User) -> None: ...
    def expunge(self, user: User) -> None: ...
```

The interface has this comment:

> Provides access to users. session() returns the current SQLAlchemy session;
> use this for operations not covered by other methods. query() returns a
> SQLAlchemy Query for users. find_one and find_many accept SQLAlchemy
> filter expressions; pass User.email == "x@y" style filters. save persists
> changes to the current session (does not commit; the caller must commit).
> delete schedules a deletion. refresh reloads the user from the database,
> overwriting any unsaved changes. expunge detaches the user from the
> session; necessary if you want to return a user object beyond the
> session's lifetime, otherwise accessing relationships afterwards will
> raise DetachedInstanceError.

The comment has eight sentences. SQLAlchemy concepts (Session, Query, expunge,
DetachedInstanceError) are part of the contract. Callers must know how
sessions work, how to write SQLAlchemy filters, and how to manage commit
and detachment. The failure is that this class is a SQLAlchemy bindings
layer with a domain repository's name.

Redesign with intent methods:

```python
class UsersRepository:
    """Handles how users are stored and queried. All methods return plain
    domain User objects with all relations populated as needed. Operations
    that modify state are atomic and return after durable commit."""

    def find(self, user_id: UserId) -> User | None: ...
    def find_by_email(self, email: str) -> User | None: ...
    def list(self, query: UserQuery) -> Page[User]: ...
    def create(self, draft: NewUser) -> User: ...
    def update_profile(self, user_id: UserId, changes: ProfileChanges) -> User: ...
    def deactivate(self, user_id: UserId, reason: str) -> User: ...
```

The comment for `update_profile` reads:

> Applies the profile changes to the user with this id and returns the
> updated user. The update is atomic. Returns NotFound if no such user exists. Returns
> ValidationFailed with field-level reasons if any change is invalid.

The comment has three sentences. The session, ORM, query syntax, commit policy, and
detachment problem are all internal. The caller writes
`users.update_profile(id, ProfileChanges(name="new"))` and gets a typed
result back.

The redesign gains depth, because each intent method enforces invariants the
bindings layer could not. `deactivate` can write the audit log and revoke
sessions in one transaction, because those are derived facts the caller
should not coordinate.

---

## Example 2 — Query object interface design

A single find method that covers every filter needs an interface that
replaces the one-finder-per-filter problem without creating a different problem.

Candidate A is too thin:

```java
public interface UserRepository {
    List<User> find(Map<String, Object> filters);
}
```

Candidate A has this comment:

> Returns users matching the filters. Accepted keys are "orgId" (UUID),
> "active" (Boolean), "createdAfter" (Instant), "createdBefore" (Instant),
> "roles" (Set<Role>), "limit" (Integer). Other keys are ignored. Type
> mismatches throw ClassCastException at runtime. Limit defaults to 200
> if absent; values over 1000 are silently capped.

Candidate A fails because the untyped map pushes type errors to runtime that
a typed interface would catch at compile time. The accepted keys are part of
the contract but appear only in prose. "Silently capped" leaks a detail
about the implementation.

Candidate B is too rigid:

```java
public interface UserRepository {
    List<User> find(UUID orgId, boolean active, Instant createdAfter, Instant createdBefore,
                    Set<Role> roles, int limit);
}
```

Candidate B has this comment:

> Returns users matching all filters. Pass null for orgId, createdAfter,
> or createdBefore to skip that filter. Pass an empty set for roles to
> skip role filtering. The active flag cannot be skipped; pass true or
> false explicitly. limit must be 1..1000.

Candidate B fails because null-as-skip is the same problem as the untyped map. The
"active" filter is awkward because a primitive boolean can't be optional.
Adding the next filter changes every call site.

Candidate C uses a value object:

```java
public interface UserRepository {
    Page<User> find(UserQuery q);
}

public record UserQuery(
    Optional<UUID> orgId,
    Optional<Boolean> active,
    Optional<Instant> createdAfter,
    Optional<Instant> createdBefore,
    Optional<Set<Role>> roles,
    int pageSize,
    Optional<PageToken> pageToken
) {
    public UserQuery() { this(empty(), empty(), empty(), empty(), empty(), 50, empty()); }
    public UserQuery withOrgId(UUID id) { ... }
    public UserQuery withActive(boolean a) { ... }
    // ...more builder-style with* methods follow
}
```

The comment for `find` reads:

> Returns users matching the query. Filters are AND'd. Unset filters are
> ignored. Results are paginated. The response includes the next page
> token if there are more results.

The comment has three sentences. `UserQuery` has its own comment describing each filter,
but it's a value object. Its contract is "what each field means", so a
reader who needs `orgId` only reads that one comment.

Offset/limit pagination becomes inconsistent when rows are inserted or deleted
mid-iteration, so a page can repeat a row or skip one.
The opaque `pageToken` encodes a stable cursor, so paging stays correct under
concurrent writes. A token and a page size add a little more to the interface
than a bare row limit.

The default constructor and the builder methods make the common case easy:
`users.find(new UserQuery().withOrgId(org).withActive(true))`. The
somewhat-general-purpose bias applies here. `UserQuery` covers today's
known queries and a reasonable set of near-future ones without becoming a god
interface for arbitrary searches.

---

## Example 3 — Transaction interface: explicit `tx` vs unit of work

This pattern appears often in TypeScript codebases around Knex/Prisma:

```ts
interface OrdersRepository {
    insert(order: Order, tx?: Transaction): Promise<Order>;
    update(id: string, changes: Partial<Order>, tx?: Transaction): Promise<Order>;
    find(id: string, tx?: Transaction): Promise<Order | null>;
}

interface InventoryRepository {
    reserve(items: Item[], tx?: Transaction): Promise<void>;
    release(reservationId: string, tx?: Transaction): Promise<void>;
}

// caller:
async function placeOrder(req: NewOrder) {
    return db.transaction(async (tx) => {
        const order = await orders.insert(req.toOrder(), tx);
        await inventory.reserve(req.items, tx);
        await payments.charge(req.payment, tx);
        return order;
    });
}
```

`OrdersRepository.insert` has this comment:

> Inserts the order. If a transaction is provided, the insert runs in that
> transaction; otherwise it runs in its own transaction and commits
> immediately. Callers composing multiple operations must thread tx through
> every call to keep them atomic.

The comment requires a sentence about transaction threading. Every
repository method has the same `tx?` argument and the same caveat. The
"interface" leaks the transaction protocol into every signature.

The failure is that `tx` is a pass-through variable that every method must
accept "in case" the caller is composing.

Redesign with ambient transaction context:

```ts
interface OrdersRepository {
    insert(order: Order): Promise<Order>;
    update(id: string, changes: Partial<Order>): Promise<Order>;
    find(id: string): Promise<Order | null>;
}

interface InventoryRepository {
    reserve(items: Item[]): Promise<void>;
    release(reservationId: string): Promise<void>;
}

interface UnitOfWork {
    run<T>(work: () => Promise<T>): Promise<T>;
}

// This is the caller:
async function placeOrder(req: NewOrder, uow: UnitOfWork) {
    return uow.run(async () => {
        const order = await orders.insert(req.toOrder());
        await inventory.reserve(req.items);
        await payments.charge(req.payment);
        return order;
    });
}
```

Repository comments are now about the operations only. The transaction
context (implemented via AsyncLocalStorage / context propagation /
dependency-injected scoped connection) is invisible. Every repository
method runs inside whatever transaction the caller established with
`uow.run`, or in its own if not.

The comment for `OrdersRepository.insert` now reads:

> Inserts the order and returns it with its assigned id.

The comment is one sentence, because the `UnitOfWork.run` contract handles
the transactional guarantee separately.

The guardrail question is whether the redesign hid anything callers need, and it
did. Sometimes the caller needs to know whether they are inside a transaction (for example, to avoid
firing an out-of-process event that would commit independently). For that
case, expose `UnitOfWork.isActive()` as a one-method check and keep the `tx`
parameter off every method.

---

## Example 4 — Migration as an interface

Migrations are an interface between code versions, so what a migration
exposes determines what is possible between those versions.

Candidate A is the schema-mutation script:

```python
def upgrade():
    op.add_column('users', sa.Column('phone_number', sa.String(20)))

def downgrade():
    op.drop_column('users', 'phone_number')
```

Teams rarely write the interface comment, because Alembic scripts look
obvious. The contract is not obvious:

> Adds a phone_number column to the users table on upgrade; drops it on
> downgrade. Note: any existing User domain objects after upgrade will
> have phone_number set to None, even though the field type is
> Optional[str], which is the same value as an explicitly-null phone
> number. The downgrade loses any phone numbers stored after upgrade —
> rolling forward over a downgrade re-runs the upgrade against existing
> data and is non-destructive only if no phone_number values were
> written during the rolled-back window.

The migration's contract is more complex than the script suggests. The script leaks
the difference between "schema migration" and "data migration". It handles
the schema migration and offers no plan for the data migration.

This redesign covers the *interface to migrations*, beyond this one migration:

```python
class Migration:
    """A migration has three parts: a schema change, an idempotent data
    backfill, and a reverse schema step. Migrations run in deployment order,
    so the application must work with every intermediate schema. backfill
    is safe to re-run. schema_down is reverse-only and may be destructive, because
    dropping a column added on the way up loses whatever was written to it.
    A zero-downtime cutover needs more: a dual-write, dual-read window held
    across two deploys, which is a larger interface this one doesn't express."""

    def schema_up(self): ...
    def backfill(self): ...     # This step is idempotent.
    def schema_down(self): ...  # This step is reverse-only and may lose data.
```

The `Migration` class is more than most teams need when they start. Most teams ship
`upgrade()` / `downgrade()` and accept the gaps. The comment test exposes
the real interface (schema, data, code coordination across deploys). After that, the
team can decide whether to invest in the deeper abstraction or accept the
limits of the shallow one. The team then makes that choice knowing the full contract.

---

## Cheat sheet — passing the comment test in the data layer

| Smell | Redesign |
|---|---|
| Repository method that returns ORM-managed objects | Return plain domain objects and commit before return |
| `find_*` method per filter combination | One `find(Query)` with a value object |
| `tx?` parameter on every method | Ambient unit-of-work through `UnitOfWork.run(work)` |
| Update method that takes `Partial<Entity>` | Intent operations (`changeEmail`, `deactivate`) that preserve invariants |
| Query method that returns "all matching rows" | Paginated result with opaque page token |
| Comment mentions "session", "connection", "cursor" | The underlying driver is leaking, so hide it |

When the comment refers to mechanism (sessions, queries, transactions, cursors),
the repository is organized around mechanism. It should be organized around the knowledge it contains, so redesign its boundaries around that knowledge.
