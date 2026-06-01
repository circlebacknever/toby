# Worked Examples — Backend APIs (Java/Kotlin, Go, TypeScript)

Different stacks, same checks. Each example shows a real pattern you'll meet in
a Spring/Nest/Go codebase and the modular structure that beats it.

---

## Example 1 — Java/Spring: BaseController as implementation inheritance

The pattern, repeated in countless Spring codebases:

```java
public abstract class BaseController {
    protected UserContext currentUser;
    protected RequestLogger logger;
    protected ValidationResult lastValidation;

    protected void requireRole(String role) { ... }
    protected ResponseEntity<?> ok(Object body) { ... }
    protected ResponseEntity<?> error(String code, int status) { ... }
    protected void logAccess() { ... }
    // ...12 more protected helpers
}

public class OrderController extends BaseController {
    @GetMapping("/orders/{id}")
    public ResponseEntity<?> getOrder(@PathVariable String id) {
        logAccess();
        requireRole("ORDER_READ");
        // ...
        return ok(order);
    }
}
```

What's wrong: applies Check 5. `BaseController` and every `*Controller` share a
two-way coupling. A new field added to the base is visible everywhere; a base
method's behavior is overridable from any subclass; `currentUser` and
`lastValidation` are instance variables that both sides mutate. The base class
accumulates a grab-bag of helpers because adding one is easier than designing a
real boundary. After two years no one knows which controllers depend on which
base behavior, and changing `BaseController` requires reading thirty files.

Fix with composition. The "base" is not one class; it is several focused
collaborators each controller injects:

```java
@RestController
public class OrderController {
    private final OrderService orders;
    private final AuthzGuard authz;             // requireRole moved here
    private final ResponseBuilder respond;       // ok/error moved here

    public OrderController(OrderService orders, AuthzGuard authz, ResponseBuilder respond) {
        this.orders = orders; this.authz = authz; this.respond = respond;
    }

    @GetMapping("/orders/{id}")
    public ResponseEntity<?> getOrder(@PathVariable String id, Principal p) {
        authz.require(p, Role.ORDER_READ);
        return respond.ok(orders.find(id));
    }
}
```

`AuthzGuard` is one module owning authorization decisions; `ResponseBuilder`
owns response shape. Each is deep behind a small interface. `OrderController`
holds them, doesn't inherit from them. The fields are now narrow and named for
what they do, instead of a `currentUser` reachable from anywhere.

Logging access, which `BaseController` did via a helper, moves to a Spring
interceptor or AOP advice — the cross-cutting concern lives in one place where
the dispatcher can apply it, not as a method every handler must remember to
call.

---

## Example 2 — Java: getters/setters versus methods that express intent

The Java-bean default:

```java
public class Order {
    private OrderStatus status;
    private BigDecimal amount;
    private Instant paidAt;

    public OrderStatus getStatus() { return status; }
    public void setStatus(OrderStatus s) { this.status = s; }
    public BigDecimal getAmount() { return amount; }
    public void setAmount(BigDecimal a) { this.amount = a; }
    public Instant getPaidAt() { return paidAt; }
    public void setPaidAt(Instant t) { this.paidAt = t; }
}
```

The "interface" is a list of fields with extra syntax. Callers must know to set
`paidAt` whenever they set `status` to `PAID`, must validate `amount > 0`
themselves, must enforce the legal status transitions. That knowledge — what an
`Order` means — has leaked into every caller.

The deeper interface expresses intent:

```java
public class Order {
    private OrderStatus status;
    private BigDecimal amount;
    private Instant paidAt;

    public static Order place(BigDecimal amount) { ... }   // validates amount
    public void markPaid(Instant when) {                    // enforces transition
        if (status != OrderStatus.PLACED) throw new IllegalState(...);
        this.status = OrderStatus.PAID;
        this.paidAt = when;
    }
    public void cancel(String reason) { ... }
    public boolean isSettled() { return status == OrderStatus.PAID; }
    public BigDecimal amount() { return amount; }           // a real query, not exposure
}
```

Fields stay private. `markPaid` and `cancel` are the legal transitions —
callers can't drift the state into invalid combinations. Where a value
truly needs to be exposed (`amount()`), it's a method that names what the
caller wants to know, not a `getAmount` whose meaning is "the bytes of the
field." The class is now deep: a few intent methods, substantial invariant
enforcement behind them.

This is the same point as Check 8 (depth check): `getX/setX` makes the
interface and the implementation the same shape. That's the definition of a
shallow module.

---

## Example 3 — Go: define interfaces where they're consumed

A common mistake imported from Java/C# into Go:

```go
// pkg/users/user.go
package users

type UserService interface {           // declared next to implementation
    GetUser(id string) (User, error)
    CreateUser(u User) error
    UpdateUser(u User) error
    DeleteUser(id string) error
    ListByOrg(orgID string) ([]User, error)
    SearchByEmail(email string) ([]User, error)
}

type userServiceImpl struct { ... }

func (s *userServiceImpl) GetUser(...) ... { ... }
// ...
```

Two problems. First, the interface is colocated with the implementation, so
every consumer drags in the whole `users` package and the whole interface even
when they only need one method. Second, the interface enumerates every method
the implementation exposes — it's a mirror of the struct, not an abstraction.
That's a shallow interface; it has no asymmetry between cost and benefit.

Idiomatic Go: each consumer declares the narrow interface it actually needs,
right where it uses it. The implementation in `users` is a concrete struct with
public methods; no one declares it implements anything explicitly.

```go
// pkg/orders/checkout.go
package orders

type userLookup interface {              // 1 method, defined by the consumer
    GetUser(id string) (users.User, error)
}

func Checkout(u userLookup, orderID string) error { ... }
```

The `orders` package depends on a one-method interface it defined for its own
purposes. Tests inject a fake implementing only that method. When `users` adds
methods, `orders` is unaffected because it never asked for them. Depth comes
from the cost-to-benefit asymmetry: the consumer pays for one method's worth
of interface and gets whatever the implementation does behind it.

This is the same principle as Check 8 in a different syntax: the interface
should be much smaller than the implementation. Go's convention makes it
mechanical to enforce.

---

## Example 4 — TypeScript/Nest middleware as temporal decomposition

A growing Nest app threads request handling through a stack of middlewares:

```ts
app.use(parseBody());
app.use(parseAuthHeader());
app.use(loadCurrentUser());          // reads from req, writes req.user
app.use(checkRateLimit());           // reads req.user, writes req.rateLimitState
app.use(checkPermissions());         // reads req.user, req.route, writes req.allowed
app.use(injectTenantContext());      // reads req.user, writes req.tenant
app.use(audit());                    // reads everything written above
```

This is temporal decomposition (Check 1). The reason there are seven
middlewares is "first do this, then that, then the next thing." The thing
being passed between them is `req`, a giant bag that each step reads from and
writes to. Every middleware knows about fields the previous ones produced —
information about who the user is, what their permissions are, which tenant
they belong to is leaked across all seven modules.

Adding the next concern means another middleware that reads `req.user`,
`req.tenant`, `req.allowed`, and writes a new field. The interface to "handle a
request" is whatever the union of all those fields adds up to, and no module
owns the contract.

Re-slice by knowledge, not order. The bodies of these middlewares belong to
distinct subjects: authentication is one body of knowledge, authorization is
another, multitenancy is a third, audit is a fourth. Make each a module with
its own boundary:

```ts
@Injectable()
class AuthSession {
    constructor(...) {}
    forRequest(req): Session { ... }    // returns user + tenant or throws
}

@Injectable()
class Authz {
    require(session: Session, action: string, resource: Resource): void { ... }
}

// Handler:
async getOrder(@Req() req: Request) {
    const session = this.auth.forRequest(req);
    this.authz.require(session, 'order.read', { id: req.params.id });
    return this.orders.find(req.params.id, session.tenantId);
}
```

The handler now invokes three named operations, each owning its knowledge.
`req.user` is gone — `session` is a value with a real type, not a field on a
shared mutable bag. Audit, rate-limit, and tenant context become explicit
dependencies of operations that actually need them, not blind passes over
every request.

Cross-cutting interceptors (logging, metrics) can still exist; they're the
narrow category Nest interceptors and Express middleware actually fit. The
seven-middleware pipeline collapses to two or three when each represents a
real cross-cut and the rest move into named modules.

---

## Pattern summary across the three stacks

| Symptom | Java/Spring fix | Go fix | TypeScript/Nest fix |
|---|---|---|---|
| Shared behavior across many handlers | Inject collaborators; avoid base classes | Helper packages, accept interfaces, return structs | Provider classes with `@Injectable` |
| Anemic data class | Methods that enforce invariants; private fields | Methods on the struct that own the invariant | Methods on the class; readonly fields |
| Cross-cutting concern | AOP advice or `HandlerInterceptor` | Wrapping middleware at the router | Nest interceptors/guards |
| Wide interface near implementation | One narrow interface per consumer | One narrow interface per consumer (idiomatic) | One narrow interface per consumer |

The principles are the same; the idiom is what changes.
