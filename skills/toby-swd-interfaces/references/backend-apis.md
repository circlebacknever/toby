# Backend APIs (Java/Kotlin, Go, TypeScript)

## REST search endpoint

A `GET /api/users` with eleven query parameters needs a ten-sentence comment. The comment has to define "active", give the allowed range for each parameter, and state the largest allowed offset. The comment also has to explain one rule kept for old clients. Send one filter object in the request, and keep the defaults and validation on the server:

```http
GET /api/users?filter=<url-encoded JSON>&page_token=...&page_size=50
```

> Lists users matching the filter, whose optional fields are AND'd together. Each response returns an opaque token for the next page. The default page size is 50, up to a maximum of 200. An expired page token returns a distinct status that tells the caller to restart paging.

The filter has its own schema that defines each field. That schema has a version number separate from the endpoint's. The opaque token lets the server change its paging strategy without a client change.

The server still tells the caller when the caller has paged too far, by returning the expired-token status. So the caller does not mistake the limit for a temporary error. A URL allows only a few KB. When the filter is too long for a URL, send the same object as the body of `POST /api/users/search`. Responses to that POST cannot be cached the way GET responses can.

## Service method with flags

`processNewOrder(req, user, cart, pm, ship, dryRun, skipTaxValidation)` needs an eight-sentence comment. The comment states the order of calls, the names of internal exceptions, and what happens when only part of the order succeeds. Replace the method with one method that takes a single command object and returns a typed result:

```java
public sealed interface OrderResult {
    record Placed(Order order) implements OrderResult {}
    // details holds caller-safe text and never internal diagnostics.
    record Failed(OrderFailureReason reason, String details) implements OrderResult {}
}

/** Places a new order from the user's cart and charges the payment method.
 *  Returns the placed order or a typed failure reason. Either the order is
 *  placed and the payment captured, or neither happens. */
public OrderResult placeOrder(PlaceOrderCommand cmd);

public record PlaceOrderCommand(UUID userId, UUID cartId, UUID paymentMethodId,
                                ShippingOption shipping, String idempotencyKey) {}
```

A dry run becomes its own `quoteOrder(cmd)` operation. The `skipTaxValidation` flag is removed, because tax exemption is a setting on the user's organization. The service looks that setting up from `userId`. The comment promises atomicity, so the implementation provides it with a saga, an outbox, or two-phase commit. When the implementation cannot make the order and the charge succeed or fail together, add an in-progress status to `OrderResult`. A retry that sends the same `idempotencyKey` returns the first result, so a caller can re-send a call that timed out without a double charge.

## Go consumer interface

Each consumer declares the narrowest interface it calls, in its own file:

```go
// pkg/orders/checkout.go
type userLookup interface {
    GetUser(id string) (users.User, error)
}

func Checkout(u userLookup, orderID string) error { ... }
```

`AdminCheckout` declares its own one-method interface with `FindUsersByOrg`. The concrete type in `pkg/users` satisfies both, and a new method there changes neither consumer. By comparison, suppose every consumer shares one five-method `UserLookup` interface. That interface's comment then has to say which caller uses each method.

## gRPC update messages

An `UpdateUser` with 25 optional fields needs a paragraph of comment. The paragraph explains how proto3 tells an unset field from a field set to its default value. The paragraph also explains how `field_mask` works and two side effects the caller cannot see. Give each kind of change its own RPC:

```proto
message ChangeUserEmailRequest { string user_id = 1; string new_email = 2; }
message DeactivateUserRequest  { string user_id = 1; string reason = 2; }
message AssignUserRoleRequest  { string user_id = 1; Role role = 2; }
```

> DeactivateUser — Marks the user inactive and revokes all sessions.
>
> AssignUserRole — Sets the user's role. Permission re-evaluation is async, so the new role may not apply to the next request.

Every field is required, so callers no longer need to tell unset fields from default values. Each side effect is described in the comment of the RPC that causes it. On a published service, ship the new RPCs beside the old one, mark the old one `deprecated` until callers migrate, and never reuse a field number. An admin endpoint that edits many fields keeps one `UpdateUser` with a documented `field_mask`.
