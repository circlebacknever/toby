# Worked Examples — Databases and Data Access

The data layer is one of the places where correct module boundaries matter
most. Schema decisions last longer than any other part of the codebase. An ORM
pattern either keeps that knowledge in one module or leaks it.

---

## Example 1 — Repository as a deep module versus ORM exposed everywhere

A new codebase wires the ORM into business logic:

```python
# orders/service.py
def confirm_order(order_id: str) -> Order:
    with session_scope() as s:
        order = s.query(Order).filter(Order.id == order_id).one()
        order.line_items                                       # reading line_items triggers a lazy load
        if order.status != 'placed':
            raise InvalidState(...)
        # ...
        s.commit()
        return order
```

Repeated across thirty services and fifty endpoints, this pattern leaks:

- The ORM session lifecycle (every caller knows `with session_scope`).
- Lazy-loading rules (every caller knows to touch `line_items` before commit).
- Query construction syntax (every caller writes SQLAlchemy filters).
- Detachment semantics (returned `Order` is bound to a session that just
  closed, so using it later raises an error).

When the team moves from SQLAlchemy to SQLModel, or splits writes off to a
separate DB, every service is touched.

A deep `OrdersRepository` contains the data-access knowledge:

```python
# orders/repository.py
class OrdersRepository:
    """Handle how orders are stored and queried.

    Callers receive plain domain objects with all relations populated as
    needed for the operation. Callers do not manage sessions or query syntax.
    Operations are atomic. Each one returns after a durable commit."""

    def confirm(self, order_id: str) -> Order: ...      # returns detached domain Order
    def find(self, order_id: str) -> Order | None: ...
    def for_customer(self, customer_id: str, since: date) -> list[Order]: ...
    def place(self, draft: NewOrder) -> Order: ...
```

The service code then reduces to one call:

```python
def confirm_order(order_id: str) -> Order:
    return orders.confirm(order_id)
```

The repository hides the ORM, the session, the eager/lazy loading strategy, and
the transaction boundary. Switching ORMs changes only the repository. Adding a read
replica also changes only the repository. Domain `Order` is now a plain class, but the old one
was a session-bound proxy that raises an error if you use it after commit.

`OrdersRepository` is the canonical example of pulling complexity downward at
the data layer. The repository has more callers than authors, so let it handle
the data-access complexity.

---

## Example 2 — Finder-method explosion

After six months, a `UserRepository` looks like this:

```java
public interface UserRepository {
    Optional<User> findById(UUID id);
    Optional<User> findByEmail(String email);
    Optional<User> findByEmailAndActive(String email, boolean active);
    List<User> findByOrgAndActive(UUID org, boolean active);
    List<User> findByOrgAndActiveAndCreatedAfter(UUID org, boolean active, Instant since);
    List<User> findByOrgAndActiveAndRoleIn(UUID org, boolean active, Set<Role> roles);
    List<User> findByOrgAndActiveAndCreatedAfterAndRoleIn(UUID org, boolean active, Instant since, Set<Role> roles);
    // ...the interface has 25 more finders
}
```

The separate-general-from-special check applies here. Each new
caller's filter combination becomes a new method, so the interface grows
unbounded. Two finders that differ in argument order do almost the same query.
Some finders are unused but remain in the interface.

The meaning of
"active" is encoded in every caller. When "active" gets redefined (excludes
suspended? excludes pending verification?), every site needs review.

A general-purpose interface replaces the finder methods:

```java
public interface UserRepository {
    Optional<User> findById(UUID id);
    Optional<User> findByEmail(String email);
    List<User> find(UserQuery q);              // this one method handles every search
    User save(User u);
    void delete(UUID id);
}

public record UserQuery(
    Optional<UUID> orgId,
    Optional<Boolean> active,
    Optional<Instant> createdAfter,
    Optional<Set<Role>> roles
) { ... }
```

One general method covers every existing finder and future filter combinations that haven't
been requested. The "active" definition stops being encoded at call sites.
Either `active` is a real database column with a clear definition, or the
repository computes it from other fields. In both cases, `active` is defined in
one place.

Before doing this, check the somewhat-general-purpose questions. Does the query
object's interface make the common case easy?
(`UserRepository.find(new UserQuery(orgId=org))` should be simple to write.)
Does it avoid becoming a god interface? (`UserQuery` is for users, so don't
extend it to orders.) `UserQuery` passes both checks.

---

## Example 3 — Schema knowledge leaking through the type system

An auth module exposes its persistence model directly:

```go
// auth/user.go
type User struct {
    ID              string    `db:"id" json:"id"`
    Email           string    `db:"email" json:"email"`
    HashedPassword  string    `db:"hashed_password" json:"-"`
    PasswordHashAlg string    `db:"password_hash_alg" json:"-"`
    LastLoginAt     time.Time `db:"last_login_at" json:"lastLoginAt"`
    MFAEnabled      bool      `db:"mfa_enabled" json:"mfaEnabled"`
    MFASecret       string    `db:"mfa_secret" json:"-"`
    LegacyMfaSecret string    `db:"legacy_mfa_secret" json:"-"`
    DeletedAt       *time.Time `db:"deleted_at" json:"-"`
    // ...the struct has 20 more fields
}
```

`User` is used as three things at once: database row, JSON DTO, and domain entity.
Every consumer of `User` is now coupled to schema columns, JSON wire format,
and internal hashing implementation. The `LegacyMfaSecret` field is visible
everywhere even though only one migration used it.

Split `User` into one type per audience:

```go
// auth/internal/store/user_row.go
type userRow struct { ... }                  // matches the schema columns and is package-private

// auth/user.go
type User struct {                            // this domain entity is narrow
    ID       string
    Email    string
    Status   UserStatus
}

// auth/api/user_dto.go
type UserDTO struct { ... }                   // the API layer defines this JSON format type
```

Each type is defined in the module where the decision it represents is made. The
storage row format can be changed without touching anything outside
`internal/store`. The JSON format can change without coupled migrations. The
domain `User` only contains what the rest of the system needs to know about
users, which is far less than every row column. Schema details stay inside
`internal/store`.

The three-role `User` is information leakage at the data layer. One type used for
three concerns has the same defect as one module that contains three pieces of
knowledge.

---

## Example 4 — Transaction boundary as a pass-through obligation

Someone who wanted control built this pattern:

```typescript
// service.ts
async function placeOrder(input: NewOrder, tx: Transaction): Promise<Order> {
    const order = await ordersRepo.insert(input, tx);
    await inventoryRepo.reserve(input.items, tx);
    await paymentsRepo.authorize(input.payment, tx);
    return order;
}

// controller.ts
const order = await db.transaction(async (tx) => {
    return placeOrder(req.body, tx);
});
```

Every method along the chain takes a `tx` argument it doesn't use directly
except to pass to the next call. `tx` is a pass-through variable (the
different-layer check). It is an unusually costly one. Adding the next
repository method means adding `tx` to every call site that ever touches it.

The fix depends on where the responsibility belongs:

If the unit of work is the *service*'s job, hide the parameter behind a context
the repos read internally:

```typescript
async function placeOrder(input: NewOrder): Promise<Order> {
    return uow.run(async () => {                  // uow injects an ambient tx
        const order = await orders.insert(input);
        await inventory.reserve(input.items);
        await payments.authorize(input.payment);
        return order;
    });
}
```

If transaction scoping is the *controller*'s job (less common), the service still
shouldn't accept `tx`.  Either way, `tx` does not
appear in the signatures of `placeOrder` or repository methods.

---

## Example 5 — ORM lazy loading as a hidden interface

This case is hard to spot, but it gets expensive at scale. Consider this service code:

```python
orders = order_repo.recent_for_customer(customer_id, limit=50)
for o in orders:
    print(o.shipping_address.city)      # runs one query per order, an N+1 pattern
    for li in o.line_items:              # runs another N+1 pattern
        print(li.product.name)            # runs another N+1 pattern
```

The "interface" of `Order` looks like a normal object. The actual contract
includes which relations the ORM happens to lazy-load and how many queries
those loads produce. That hidden contract is a per-call performance interface,
which fails the depth check. Callers must know what's expensive, but the cost is
not visible in any signature.

Either of two changes makes the interface's cost visible:

- **Make eagerness explicit at the call.** The repo accepts a small spec of
  what to load: `order_repo.recent_for_customer(customer_id, limit=50,
  include=[Order.shipping_address, Order.line_items, LineItem.product])`. The
  hidden N+1 is now an explicit join. Only callers that ask for a relation pay the
  cost.
- **Return a purpose-built type.** If the use case is "list orders with
  product names," the repo provides
  `order_repo.list_for_display(customer_id)`. It returns a flat dataclass with
  exactly the fields needed, produced by one query. Callers cannot
  trigger N+1 by reading the wrong field because the field is just a column
  on the result.

The wrong fix is to leave the lazy interface in place and tell callers to "be
careful." Undocumented performance behavior is the same defect as an undocumented
precondition.

---

## Cross-cutting notes

- **Migration knowledge** belongs in one module. When each service constructs raw
  SQL or hardcodes a column alias, a column rename touches twelve services.
  That spread is the same leakage pattern as Example 3.
- **Caching the repository** is covered in Example 1 of `caching.md`. The
  service does not implement it. The repository is the right place for read-through
  caching because it already defines the data-access contract.
- **Read models versus write models** become sensible splits when one query
  type is very different from the entity (reporting, dashboards).
  That split is deliberate under the split/merge check, but most apps don't need
  it.
