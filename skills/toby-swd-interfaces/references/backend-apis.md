# Worked Examples — Backend APIs (Java/Kotlin, Go, TypeScript)

The interface is everything callers must know — and on a backend that
includes the wire contract (REST, gRPC), the service-layer methods, and
the value objects in between. The comment test applies to each.

---

## Example 1 — REST endpoint interface: parameter sprawl vs query object

A search endpoint that grew query parameters over time:

```http
GET /api/users?org_id=...&active=true&role=admin&role=editor
   &created_after=2024-01-01&created_before=2024-12-31
   &has_mfa=true&has_logged_in_in_days=30
   &sort=email&order=asc&limit=50&offset=0
```

A handler that mirrors it:

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

Documenting the endpoint:

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

A whole paragraph. The wire contract is leaking the implementation's
"active" interpretation, the validation rules, the performance defenses,
and the legacy compatibility note. Every consumer reads this paragraph
and bakes it into their client.

The redesign: a query object on the wire, the implementation owns the
defaults and the validation, and the contract gets short.

```http
GET /api/users?filter=<base64-or-json>&page_token=...&page_size=50
```

Where `filter` is a structured value:

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

Comment:

> Lists users matching the filter. Filter fields are optional and AND'd
> together. Results are paginated with opaque page tokens; the next-page
> token is returned in the response. Page size defaults to 50, maximum
> 200.

Four sentences. Definitions of "active" and validation specifics move to
the filter object's schema (versioned, documented separately from this
endpoint). The pagination contract is opaque tokens, which lets the
server change its internal offset strategy without telling clients —
performance defenses become invisible to callers. The endpoint is now
shaped like its contract: "list users by criteria" with one criteria
input and one pagination control.

Guardrail: did anything get hidden that callers truly need? The
performance limit on deep pagination is truly caller-facing — opaque
tokens convey it implicitly (the token stops being valid past a
limit) and the response can return a clear error code when that happens.

---

## Example 2 — Java service method: ordering and internals in the comment

A service method that "works":

```java
public class OrderService {
    public Order processNewOrder(NewOrderRequest req, User user, Cart cart,
                                 PaymentMethod pm, ShippingOption ship,
                                 boolean dryRun, boolean skipTaxValidation) {
        // ...
    }
}
```

The complete comment:

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

Eleven sentences. Order ("First X, then Y"), internal exception names,
edge-case escape hatches (`skipTaxValidation`), partial-failure semantics
the caller must know about. Failure named at multiple levels.

Redesign by knowledge. The procedure is "place an order from a cart," and
the contract should look like one operation, not seven validations the
caller orchestrates:

```java
public sealed interface OrderResult {
    record Placed(Order order) implements OrderResult {}
    record Failed(OrderFailureReason reason, String details) implements OrderResult {}
}

public class OrderService {
    /**
     * Places a new order from the user's cart, validating the request and
     * charging the payment method. Returns either the placed order or a
     * typed failure with a structured reason. Atomic: either the order is
     * placed and payment captured, or neither happens.
     */
    public OrderResult placeOrder(PlaceOrderCommand cmd) { ... }
}

public record PlaceOrderCommand(UUID userId, UUID cartId, UUID paymentMethodId,
                                 ShippingOption shipping, boolean dryRun) {}

public enum OrderFailureReason {
    CART_INVALID, PAYMENT_METHOD_INVALID, SHIPPING_UNAVAILABLE,
    PAYMENT_DECLINED, TAX_UNAVAILABLE
}
```

Comment passes: four sentences, no ordering, no exception names, no
escape hatches in the surface. The `skipTaxValidation` flag is gone —
that policy is a property of the org, computed inside the service from
`userId`. The "partial failure of payment capture" reality is hidden
behind the atomic guarantee in the comment; achieving atomicity is the
implementation's job (saga, outbox, or two-phase). If atomicity truly
cannot be guaranteed, the contract changes to expose it (returns include
an in-progress status), but it doesn't expose the implementation strategy.

---

## Example 3 — Go service interface declared at the consumer

Continuing the pattern from `toby-swd-modules` backend-apis Example 3, the
question for toby-swd-interfaces is what shape the consumer-side interface
takes. The temptation is to define a "convenient" interface with
everything the consumer might want.

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

The comment on this interface:

> The users-related operations Checkout needs. GetUser returns the user;
> GetActiveUser additionally returns an error if the user is inactive
> (different error type than GetUser). GetUserWithPreferences includes
> preferences; use this when displaying the user's settings. FindUsersByOrg
> is for the admin checkout path. ResolveUserByEmail is for guest checkout
> with email-only login.

Five methods, five different uses, each describing both behavior and which
caller-site uses it. Failure named: this is a grab-bag, not an interface.
It exists to be "convenient" for any future need.

Redesign with the actually-needed method only:

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

Comment for `userLookup`:

> A user-lookup capability. GetUser returns the user with this id, or a
> NotFound error.

Two sentences. The interface is single-purpose and the comment naturally
shrinks to match.

---

## Example 4 — gRPC/protobuf message design

Protobuf forces an explicit interface and the comment test is unusually
revealing there.

Candidate A:

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

Comment for `UpdateUser(UpdateUserRequest)`:

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

A paragraph. The proto3 presence problem leaked into the contract, an
extra protocol detail (field_mask) became a caller obligation, and the
two side-effects (session revocation, async permission re-evaluation) are
buried in the prose.

Redesign by intent. Separate the operations that are conceptually distinct:

```proto
// Each operation has its own message and is its own RPC.
message ChangeUserDisplayNameRequest { string user_id = 1; string display_name = 2; }
message ChangeUserEmailRequest       { string user_id = 1; string new_email = 2; }
message DeactivateUserRequest        { string user_id = 1; string reason = 2; }
message AssignUserRoleRequest        { string user_id = 1; Role role = 2; }
```

Comments, one per RPC:

> ChangeUserDisplayName — Updates the user's display name.
>
> ChangeUserEmail — Initiates an email change; sends a verification email
> to the new address. The change takes effect after verification.
>
> DeactivateUser — Marks the user inactive and revokes all sessions.
> Reversible by ActivateUser.
>
> AssignUserRole — Sets the user's role. New permissions are visible
> immediately to subsequent requests.

Each comment is one to two sentences. Each RPC has one effect that the
caller can reason about. The proto3 presence problem disappears because
no field is "set or unset" — every field on every message is required to
the operation. The side effects move from "buried in prose" to "named in
the operation's purpose."

For high-cardinality update endpoints (admin tools that legitimately edit
many fields), keep one `UpdateUser` operation with a field_mask, document
the field_mask requirement once, and accept the trade — but understand
that the comment is necessarily longer because the operation is truly
"set whichever subset of these fields the caller asked for." The intent
form is the default; the bulk form is the exception.

---

## Cheat sheet — passing the comment test on backends

| Smell | Redesign |
|---|---|
| Endpoint with 10+ query parameters | Filter/criteria value object on the wire |
| Service method with `dryRun`, `skipX`, `useY` flags | Split into operations; encode policy on entities, not flags |
| Method whose comment lists exceptions to handle | Typed result (`Result<T>` or sealed `Outcome`) |
| RPC mutation that updates "any subset of these fields" | One RPC per intent; field-mask form only when the bulk case is real |
| Producer-defined interface with 6+ methods | Consumer-side narrow interfaces |
| Comment that says "callers must call X before Y" | Combine into one method, or hide the order behind a factory/builder |

Same pattern across all stacks: when the comment swells with ordering,
flags, exceptions, or special cases, the interface is asking the caller
to do work that belongs inside.
