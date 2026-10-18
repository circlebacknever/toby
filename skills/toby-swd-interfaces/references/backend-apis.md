# Backend APIs

## REST search endpoint

A `GET /api/users` with eleven query parameters needs a ten-sentence comment defining allowed ranges, offsets, and legacy rules. Accept one filter object in the request and keep defaults and validation on the server:

```http
GET /api/users?filter=<url-encoded JSON>&page_token=...&page_size=50
```

> Lists users matching the filter, which combines optional fields with AND. Each response returns an opaque token for the next page. The default page size is 50, up to a maximum of 200. An expired page token returns a distinct status that tells the caller to restart paging.

The filter schema defines each field and versions independently of the endpoint, while the opaque page token lets the server change its paging strategy without breaking clients. When the filter can exceed URL length limits, accept the same filter object in `POST /api/users/search` (noting that CDNs and browsers don't cache `POST` responses).

## Command and result objects

```java
Order placeOrder(UUID userId, List<LineItem> items, Address shipTo, Address billTo,
                 PaymentMethodId pm, String couponCode, boolean giftWrap,
                 String giftMessage, boolean skipTaxValidation, IdempotencyKey key);
```

This ten-argument signature requires callers to pass `null` and `false` for unused options. Group the input into a command record and return a sealed result:

```java
public sealed interface PlaceOrderResult {
    record Placed(Order order) implements PlaceOrderResult {}
    record Declined(DeclineReason reason) implements PlaceOrderResult {}
    record OutOfStock(List<Sku> unavailable) implements PlaceOrderResult {}
}

/**
 * Places an order and captures payment atomically: the method either places
 * the order and captures the payment, or does neither. Repeating a call with
 * the same IdempotencyKey within 24h returns the original result.
 */
PlaceOrderResult placeOrder(PlaceOrderCommand cmd);
```

Remove the `skipTaxValidation` flag and read tax-exemption status from the user's organization inside `placeOrder`.

## Go consumer interface

```go
// billing/invoicer.go declares only the method it calls.
type userDirectory interface {
    BillingContact(ctx context.Context, orgID OrgID) (Contact, error)
}
```

When each consumer declares a small interface with only the method it calls, one `users.Service` struct can satisfy every consumer without forcing any caller to depend on unrelated methods.

## gRPC messages

An `UpdateUser` RPC with 25 optional fields needs a long comment explaining `field_mask` rules and hidden side effects. Give each business action its own RPC and describe its side effects in its comment:

```protobuf
service UserService {
  // Changes the user's primary email and sends a verification link to the new address.
  rpc ChangeEmail(ChangeEmailRequest) returns (ChangeEmailResponse);
  // Deactivates the user, revokes all active sessions, and records an audit entry.
  rpc DeactivateUser(DeactivateUserRequest) returns (DeactivateUserResponse);
}
```
