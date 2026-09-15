# Worked Examples — Backend APIs (Java/Kotlin, Go, TypeScript)

The interface is everything callers must know. On a backend that
includes the wire contract (REST, gRPC), the service-layer methods, and
the value objects in between. The comment test applies to each.

---

## Example 1 — REST endpoint interface: parameter sprawl vs query object

Query parameters were added to this search endpoint over time:

```http
GET /api/users?org_id=...&active=true&role=admin&role=editor
   &created_after=2024-01-01&created_before=2024-12-31
   &has_mfa=true&has_logged_in_in_days=30
   &sort=email&order=asc&limit=50&offset=0
```

This handler has one parameter for each query parameter:

```java
@GetMapping("/api/users")
public Page<UserDTO> listUsers(
    @RequestParam Optional<UUID> orgId,
    @RequestParam Optional<Boolean> active,
    @RequestParam Optional<List<Role>> role,
    @RequestParam Optional<Instant> createdAfter,
    @RequestParam Optional<Instant> createdBefore,
    @RequestParam Optional<Boolean> hasMfa,
    @RequestParam Optional<Integer> hasLoggedInInDays,
    @RequestParam Optional<String> sort,
    @RequestParam Optional<String> order,
    @RequestParam(defaultValue = "50") int limit,
    @RequestParam(defaultValue = "0") int offset
) { ... }
```

The comment that documents the endpoint reads:

> Lists users matching the filter. orgId restricts results to that
> organization. active filters by active state (where "active" excludes
> suspended users but includes pending-email-verification users from 2023
> for legacy compatibility). role can be repeated to match any of several
> roles. createdAfter and createdBefore form a half-open interval (after
> inclusive, before exclusive). hasMfa filters by whether MFA is enabled.
> hasLoggedInInDays returns users whose lastLoginAt is within the given
> number of days from now. sort must be one of email, createdAt, lastLoginAt;
> order is asc or desc. limit must be 1..200. offset is zero-based and
> the response includes a next-page link, but offset >10000 is rejected
> for performance reasons.

The comment is a whole paragraph. The wire contract leaks the implementation's
"active" interpretation, the validation rules, the performance limits,
and the legacy compatibility note. Every consumer reads this paragraph
and builds those rules into their client.

The redesign puts a query object on the wire and makes the implementation responsible for
the defaults and the validation, so the contract gets short.

```http
GET /api/users?filter=<url-encoded JSON>&page_token=...&page_size=50
```

`filter` is a single structured value, with one documented encoding
(URL-encoded JSON):

```json
{
  "orgId": "...",
  "active": true,
  "roles": ["admin"],
  "createdBetween": { "from": "2024-01-01", "to": "2024-12-31" },
  "loggedInWithin": "P30D",
  "mfa": true,
  "sort": { "field": "email", "order": "asc" }
}
```

The redesigned endpoint has this comment:

> Lists users matching the filter. Filter fields are optional and AND'd
> together. Results are paginated with opaque page tokens. The next-page
> token is returned in the response. Page size defaults to 50 and has a maximum of
> 200.

The comment has four sentences. Definitions of "active" and validation
specifics move to the filter object's schema (versioned, documented separately
from this endpoint). The pagination contract uses opaque tokens, which lets the
server change its internal offset strategy without telling clients. As a
result, callers never see the performance limits. The endpoint now matches
its contract, which is "list users by criteria" with one criteria input and
one pagination control.

The guardrail question is whether the redesign hid anything callers need. The
performance limit on deep pagination is caller-facing. Opaque
tokens expose the limit indirectly, because the token stops being valid past a limit.
The response returns a specific status the caller can branch on when that
happens (a `400`/`410`-style "page token expired, restart paging"). As a result, an
expired token isn't mistaken for a transient error.

A query string has a practical length limit, because
proxies and servers cap the URL around a few KB. A small filter fits, but a large
or heavily nested one does not. Encoding it as base64 does not remove the limit.
When the criteria object becomes too long for the URL, send the same object in a
`POST /api/users/search` body. That change keeps the contract but changes the transport.
That gives up GET's caching and idempotent-by-method semantics, so keep the
GET form while the filter stays small.

---

## Example 2 — Java service method: ordering and internals in the comment

Here is a service method that "works":

```java
public class OrderService {
    public Order processNewOrder(NewOrderRequest req, User user, Cart cart,
                                 PaymentMethod pm, ShippingOption ship,
                                 boolean dryRun, boolean skipTaxValidation) {
        // ...
    }
}
```

Here is the complete comment:

> Processes a new order. First validates that the cart belongs to the user
> and is not empty; throws CartInvalidException otherwise. Then validates
> the payment method against the user's saved methods; throws
> PaymentMethodNotFoundException if not found. Then validates the shipping
> option against the cart's contents (some items require specific shipping
> tiers); throws ShippingNotAvailableException. Then validates tax via the
> tax service unless skipTaxValidation is true (used for tax-exempt orgs).
> If dryRun is true, returns the computed Order without persisting or
> charging the payment method. Otherwise, persists the order, captures the
> payment, and returns the persisted Order with an id. The method is
> transactional; partial failures roll back, except for the payment capture,
> which is a separate transaction and may leave a captured payment with no
> persisted order in rare cases — the reconciliation job handles these.

The comment has eleven sentences. It states call order ("First X, then Y"),
internal exception names, edge-case flags (`skipTaxValidation`), and
partial-failure semantics the caller must know about. The comment fails the
test at several levels.

In a redesign by knowledge, the procedure is "place an order from a cart," so
the contract should be one operation that performs the seven validations
the caller currently coordinates:

```java
public sealed interface OrderResult {
    record Placed(Order order) implements OrderResult {}
    // details holds caller-safe text about the reason and never holds internal diagnostics.
    record Failed(OrderFailureReason reason, String details) implements OrderResult {}
}

public class OrderService {
    /**
     * Places a new order from the user's cart, validating the request and
     * charging the payment method. Returns either the placed order or a
     * typed failure with a structured reason. The operation is atomic, so either the order is
     * placed and payment captured, or neither happens.
     */
    public OrderResult placeOrder(PlaceOrderCommand cmd) { ... }
}

public record PlaceOrderCommand(UUID userId, UUID cartId, UUID paymentMethodId,
                                 ShippingOption shipping, String idempotencyKey,
                                 boolean dryRun) {}

public enum OrderFailureReason {
    CART_INVALID, PAYMENT_METHOD_INVALID, SHIPPING_UNAVAILABLE,
    PAYMENT_DECLINED, TAX_UNAVAILABLE
}
```

The comment passes, because it has four sentences and contains no call order, no
exception names, and no edge-case flags. The `skipTaxValidation` flag is gone,
because that policy is a property of the org, computed inside the service from
`userId`. The atomic guarantee in the comment hides the partial failure of
payment capture. Achieving atomicity is the
implementation's job (saga, outbox, or two-phase). If atomicity
cannot be guaranteed, the contract changes to expose it (returns include
an in-progress status). The contract still doesn't expose the implementation strategy.

The `idempotencyKey` is part of that contract too. A retry with the key
it used the first time returns the original result and never places a second
order. A mutation is safe to retry only when the request has a key the
server dedupes on, or the operation is naturally idempotent. The key is what
lets a caller re-send a `placeOrder` that timed out without risking a double
charge.

---

## Example 3 — Go service interface declared at the consumer

When one service consumes another, the question is what the consumer-side
interface should expose. Developers are tempted to define a convenient
interface with everything the consumer might want.

```go
// pkg/orders/interfaces.go
package orders

type UserLookup interface {
    GetUser(id string) (users.User, error)
    GetUserWithPreferences(id string) (users.UserWithPrefs, error)
    GetActiveUser(id string) (users.User, error)   // returns error if inactive
    FindUsersByOrg(orgID string) ([]users.User, error)
    ResolveUserByEmail(email string) (users.User, error)
}
```

This interface has the following comment:

> The users-related operations Checkout needs. GetUser returns the user;
> GetActiveUser additionally returns an error if the user is inactive
> (different error type than GetUser). GetUserWithPreferences includes
> preferences; use this when displaying the user's settings. FindUsersByOrg
> is for the admin checkout path. ResolveUserByEmail is for guest checkout
> with email-only login.

The interface has five methods for five different uses. The comment
describes both the behavior and the call site for each. The failure is
that the interface is a set of unrelated methods that exists to be convenient for any future need.

Redesign with only the method `Checkout` needs:

```go
// pkg/orders/checkout.go
type userLookup interface {
    GetUser(id string) (users.User, error)
}

func Checkout(u userLookup, orderID string) error { ... }
```

If the admin path also needs a checkout function, it declares its own:

```go
// pkg/orders/admin_checkout.go
type adminUserLookup interface {
    FindUsersByOrg(orgID string) ([]users.User, error)
}

func AdminCheckout(u adminUserLookup, orgID string) error { ... }
```

Each interface is the narrowest one that supports its function. The
implementation in `pkg/users` happens to satisfy both because it has both
methods, but neither consumer is coupled to anything it doesn't use.

The comment for `userLookup` reads:

> Provides user lookup. GetUser returns the user with this id, or a
> NotFound error.

The comment has two sentences, because the interface has a single
purpose.

---

## Example 4 — gRPC/protobuf message design

Protobuf forces an explicit interface, so the comment test exposes its
problems.

Candidate A is this message:

```proto
message UpdateUserRequest {
  string user_id = 1;
  optional string email = 2;
  optional string display_name = 3;
  optional bool is_active = 4;
  optional Role role = 5;
  optional string locale = 6;
  // ...20 more optional fields
}
```

The comment for `UpdateUser(UpdateUserRequest)` reads:

> Updates the user with user_id. Fields that are set in the request are
> applied to the user; fields that are unset are unchanged. Note that for
> string fields, the empty string is treated as "clear this field" if and
> only if the field is present in the protobuf wire format — clients must
> use field_mask if they want to clear a field, since proto3 makes the
> empty-string-not-set distinction impossible without field_mask. The
> is_active flag, when set to false, also revokes all sessions for the user.
> Changing the role triggers a re-evaluation of permissions across the
> user's resources, which is async; callers should not assume the new role
> is in effect immediately.

The comment is a paragraph. The proto3 presence problem leaked into the
contract, so an extra protocol detail (field_mask) became a caller obligation.
The prose also hides the two side-effects (session revocation, async
permission re-evaluation).

To redesign by intent, separate the operations that are conceptually distinct:

```proto
// Each operation has its own message and is its own RPC.
message ChangeUserDisplayNameRequest { string user_id = 1; string display_name = 2; }
message ChangeUserEmailRequest       { string user_id = 1; string new_email = 2; }
message DeactivateUserRequest        { string user_id = 1; string reason = 2; }
message AssignUserRoleRequest        { string user_id = 1; Role role = 2; }
```

Each RPC has its own comment:

> ChangeUserDisplayName — Updates the user's display name.
>
> ChangeUserEmail — Initiates an email change and sends a verification email
> to the new address. The change takes effect after verification.
>
> DeactivateUser — Marks the user inactive and revokes all sessions.
> ActivateUser reverses it.
>
> AssignUserRole — Sets the user's role. Permission re-evaluation across the
> user's resources is async, so the new role may not be in effect for the
> next request. That side effect is stated in the operation's purpose.

Each comment is one to two sentences. Each RPC has one effect that the
caller can reason about. The proto3 presence problem disappears because
no field is "set or unset". Every field on every message is required to
the operation. The side effects are no longer hidden in the prose, because they are stated in
the operation's purpose.

On a published service, splitting `UpdateUser` into four RPCs is a
wire-breaking change, because existing clients call an RPC that no longer exists.
The new RPCs ship alongside the old one, which stays and is marked
`deprecated` until callers migrate. Proto field numbers are never reused.
Greenfield designs adopt the split directly. The brownfield rule in the skill
covers this split, so do not break an interface other teams build on without a
migration path.

For high-cardinality update endpoints (admin tools that legitimately edit
many fields), keep one `UpdateUser` operation with a field_mask, document
the field_mask requirement once, and accept a longer comment. The comment is
necessarily longer there, because the operation is
"set whichever subset of these fields the caller asked for." The intent
form is the default, so use the bulk form only for these high-cardinality endpoints.

---

## Cheat sheet — passing the comment test on backends

| Smell | Redesign |
|---|---|
| Endpoint with 10+ query parameters | Filter/criteria value object on the wire |
| Service method with `dryRun`, `skipX`, `useY` flags | Split into operations, and encode policy on the entities themselves |
| Method whose comment lists exceptions to handle | Typed result (`Result<T>` or sealed `Outcome`) |
| RPC mutation that updates "any subset of these fields" | One RPC per intent, with the field-mask form only when the bulk case is real |
| Producer-defined interface with 6+ methods | Consumer-side narrow interfaces |
| Comment that says "callers must call X before Y" | Combine into one method, or hide the order behind a factory/builder |

The same pattern holds in every stack. When the comment grows with ordering,
flags, exceptions, or special cases, the interface makes the caller do work
that belongs inside the module.
