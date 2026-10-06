# Backend APIs (Java/Kotlin, Go, TypeScript)

## REST search endpoint

A `GET /api/users` with eleven query parameters needs a ten-sentence comment. It has to state what "active" means, each validation range, the offset cap, and a legacy rule. Put one filter object on the wire and keep the defaults and validation inside the server:

```http
GET /api/users?filter=<url-encoded JSON>&page_token=...&page_size=50
```

> Lists users matching the filter, whose optional fields are AND'd together. Each response returns an opaque token for the next page. The default page size is 50, up to a maximum of 200. An expired page token returns a distinct status that tells the caller to restart paging.

The filter's schema defines each field, versioned apart from the endpoint. The opaque token lets the server change its paging strategy without a client change. The deep-paging limit still reaches the caller, as the expired-token status, so the caller does not treat it as a transient error. When the filter outgrows the URL limit of a few KB, send the same object as the body of `POST /api/users/search`, which gives up GET caching.

## Service method with flags

`processNewOrder(req, user, cart, pm, ship, dryRun, skipTaxValidation)` needs an eight-sentence comment that states the call order, internal exception names, and a partial failure. Replace it with one command and a typed result:

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

A dry run becomes its own `quoteOrder(cmd)` operation. `skipTaxValidation` is gone, because tax exemption is a property of the org that the service reads from `userId`. The comment promises atomicity, so the implementation provides it with a saga, an outbox, or two-phase commit. When it cannot, the result adds an in-progress status. A retry that sends the same `idempotencyKey` returns the first result, so a caller can re-send a call that timed out without a double charge.

## Go consumer interface

Each consumer declares the narrowest interface it calls, in its own file:

```go
// pkg/orders/checkout.go
type userLookup interface {
    GetUser(id string) (users.User, error)
}

func Checkout(u userLookup, orderID string) error { ... }
```

`AdminCheckout` declares its own one-method interface with `FindUsersByOrg`. The concrete type in `pkg/users` satisfies both, and a new method there changes neither consumer. A five-method `UserLookup` shared by every consumer needs a comment that names a call site for each method.

## gRPC update messages

An `UpdateUser` with 25 optional fields needs a paragraph about proto3 presence, `field_mask`, and two hidden side effects. Give each intent its own RPC:

```proto
message ChangeUserEmailRequest { string user_id = 1; string new_email = 2; }
message DeactivateUserRequest  { string user_id = 1; string reason = 2; }
message AssignUserRoleRequest  { string user_id = 1; Role role = 2; }
```

> DeactivateUser — Marks the user inactive and revokes all sessions.
>
> AssignUserRole — Sets the user's role. Permission re-evaluation is async, so the new role may not apply to the next request.

Every field is required, so the presence problem goes away, and each side effect is in the comment of the RPC that causes it. On a published service, ship the new RPCs beside the old one, mark the old one `deprecated` until callers migrate, and never reuse a field number. An admin endpoint that edits many fields keeps one `UpdateUser` with a documented `field_mask`.
