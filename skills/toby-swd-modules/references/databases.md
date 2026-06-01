# Worked Examples — Databases and Data Access

The data layer is one of the highest-yield places to get module boundaries
right. Schema decisions outlive everything else in the codebase, and ORM
patterns either contain or leak that knowledge.

---

## Example 1 — Repository as a deep module versus ORM exposed everywhere

A young codebase wires the ORM into business logic:

```python
# orders/service.py
def confirm_order(order_id: str) -> Order:
    with session_scope() as s:
        order = s.query(Order).filter(Order.id == order_id).one()
        order.line_items                                       # lazy load
        if order.status != 'placed':
            raise InvalidState(...)
        # ...
        s.commit()
        return order
```

Multiplied across thirty services and fifty endpoints, this pattern leaks:

- The ORM session lifecycle (every caller knows `with session_scope`).
- Lazy-loading rules (every caller knows to touch `line_items` before commit).
- Query construction syntax (every caller writes SQLAlchemy filters).
- Detachment semantics (returned `Order` is bound to a session that just
  closed; using it later blows up).

When the team moves from SQLAlchemy to SQLModel, or splits writes off to a
separate DB, every service is touched.

A deep `OrdersRepository` owns the data-access knowledge:

```python
# orders/repository.py
class OrdersRepository:
    """Owns how orders are stored and queried.

    Callers receive plain domain objects with all relations populated as
    needed for the operation; they do not manage sessions or query syntax.
    Operations are atomic and return after durable commit."""

    def confirm(self, order_id: str) -> Order: ...      # returns detached domain Order
    def find(self, order_id: str) -> Order | None: ...
    def for_customer(self, customer_id: str, since: date) -> list[Order]: ...
    def place(self, draft: NewOrder) -> Order: ...
```

Service code becomes:

```python
def confirm_order(order_id: str) -> Order:
    return orders.confirm(order_id)
```

The ORM, the session, the eager/lazy loading strategy, the transaction
boundary — all hidden. Switching ORMs is one module's problem. Adding a read
replica is the repository's choice. Domain `Order` is a plain class, not a
session-bound proxy that explodes if you look at it after commit.

This is the canonical example of pulling complexity downward (Check 3) at the
data layer. The repository is more callers than authors; let it absorb the
hard part.

---

## Example 2 — Finder-method explosion

A `UserRepository` six months in:

```java
public interface UserRepository {
    Optional<User> findById(UUID id);
    Optional<User> findByEmail(String email);
    Optional<User> findByEmailAndActive(String email, boolean active);
    List<User> findByOrgAndActive(UUID org, boolean active);
    List<User> findByOrgAndActiveAndCreatedAfter(UUID org, boolean active, Instant since);
    List<User> findByOrgAndActiveAndRoleIn(UUID org, boolean active, Set<Role> roles);
    List<User> findByOrgAndActiveAndCreatedAfterAndRoleIn(UUID org, boolean active, Instant since, Set<Role> roles);
    // ...25 more
}
```

Check 6 (separate general from special, remove special cases). Each new
caller's filter combination becomes a new method. The interface grows
unbounded; two finders that differ in argument order do almost the same query;
some are unused but no one will delete them. Worst of all, the meaning of
"active" is encoded in every caller — the day "active" gets redefined (excludes
suspended? excludes pending verification?) is the day every site needs review.

A general-purpose interface compresses the cluster:

```java
public interface UserRepository {
    Optional<User> findById(UUID id);
    Optional<User> findByEmail(String email);
    List<User> find(UserQuery q);              // one search method
    User save(User u);
    void delete(UUID id);
}

public record UserQuery(
    Optional<UUID> orgId,
    Optional<Boolean> active,
    Optional<Instant> createdAfter,
    Optional<Set<Role>> roles,
    Optional<Integer> limit
) { ... }
```

One general method covers every existing finder and the next ten that haven't
been requested. The "active" definition stops being encoded at call sites:
either `active` is a real database column with a clear definition, or the
repository computes it from other fields — either way, it's one decision in
one place.

The questions to check before doing this (the somewhat-general-purpose
framing): does the query object's interface make the common case easy?
(`UserRepository.find(new UserQuery(orgId=org))` should be simple to write.)
Does it avoid becoming a god interface? (`UserQuery` is for users — don't
extend it to orders.) Both pass.

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
    // ...20 more fields
}
```

`User` plays three roles at once: database row, JSON DTO, and domain entity.
Every consumer of `User` is now coupled to schema columns, JSON wire shape,
and internal hashing implementation. The `LegacyMfaSecret` field is visible
everywhere even though only one migration cared about it.

Split by audience:

```go
// auth/internal/store/user_row.go
type userRow struct { ... }                  // schema-shaped, package-private

// auth/user.go
type User struct {                            // domain entity, narrow
    ID       string
    Email    string
    Status   UserStatus
}

// auth/api/user_dto.go
type UserDTO struct { ... }                   // JSON shape, owned by the API layer
```

Each type lives in the module that owns the decision it represents. The
storage row format can be changed without touching anything outside
`internal/store`. The JSON shape can evolve without coupled migrations. The
domain `User` only carries what the rest of the system needs to know about
users — a much smaller surface than every row column. Schema secrets stay
secret.

This is Check 2 (information leakage) at the data layer. One type bound to
three concerns is the same defect as one module owning three pieces of
knowledge.

---

## Example 4 — Transaction boundary as a pass-through obligation

A pattern that grew up because someone wanted "control":

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
except to pass to the next call. This is a pass-through variable (Check 4),
and it is an unusually costly one — adding the next repository method means
adding `tx` to every call site that ever touches it.

Two fixes depending on where the responsibility belongs:

If the *service* owns the unit of work, hide the parameter behind a context
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

If the *controller* owns transaction scoping (less common), the service still
shouldn't accept `tx`; it should be transparent. Either way, `tx` does not
appear in the signatures of `placeOrder` or repository methods.

---

## Example 5 — ORM lazy loading as a hidden interface

A subtle case that hurts at scale. Service code:

```python
orders = order_repo.recent_for_customer(customer_id, limit=50)
for o in orders:
    print(o.shipping_address.city)      # one query per order — N+1
    for li in o.line_items:              # another N+1
        print(li.product.name)            # another N+1
```

The "interface" of `Order` looks like a normal object. The actual contract
includes which relations the ORM happens to lazy-load and how many queries
that produces — a hidden, per-call performance interface. This is the depth
check (Check 8) failing: callers must know what's expensive, and the cost is
not visible in any signature.

Two ways to make the interface honest:

- **Make eagerness explicit at the call.** The repo accepts a small spec of
  what to load: `order_repo.recent_for_customer(customer_id, limit=50,
  include=[Order.shipping_address, Order.line_items, LineItem.product])`. The
  hidden N+1 is now an explicit join; callers that don't ask don't get the
  cost.
- **Return a purpose-built shape.** If the use case is "list orders with
  product names," the repo provides
  `order_repo.list_for_display(customer_id)` returning a flat dataclass that
  contains exactly the fields needed, produced by one query. Callers cannot
  trigger N+1 by reading the wrong field because the field is just a column
  on the result.

The wrong fix is to leave the lazy interface in place and tell callers to "be
careful." Performance behavior documented nowhere is the same defect as a
precondition documented nowhere.

---

## Cross-cutting notes

- **Migration knowledge** belongs in one module. A column rename touched in
  twelve services because each constructs raw SQL or hardcodes a column alias
  is the same leakage pattern as Example 3.
- **Caching the repository** is properly Example 1 from `caching.md`, not a
  concern of the service. The repository is the natural home for read-through
  caching because it already owns the data-access contract.
- **Read models versus write models** become natural splits when one query
  shape is wildly different from the entity shape (reporting, dashboards).
  That's a deliberate split per Check 7, not the default — most apps don't
  need it.
