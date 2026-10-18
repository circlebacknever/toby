# Backend APIs

This file shows how to replace a `BaseController` and a stateful middleware chain with explicit dependencies in Java, Go, and TypeScript.

## Base controller

A `BaseController` with protected helpers and shared fields such as `currentUser` couples the base class and every controller in both directions. Move each helper group into a dedicated dependency injected into the controller, and keep record-level rules inside the service operation:

```java
@RestController
public class OrderController {
    private final OrderService orders;
    private final AuthGuard auth;
    private final ResponseBuilder respond;

    @GetMapping("/orders/{id}")
    public ResponseEntity<?> getOrder(@PathVariable String id, Principal p) {
        Session session = auth.requireRole(p, Role.ORDER_READ);
        return respond.ok(orders.findForAccount(id, session.accountId()));
    }
}
```

Move request-wide access logging into one framework interceptor or middleware that runs on every route.

## Middleware chain

```ts
app.use(loadCurrentUser());     // writes req.user
app.use(checkRateLimit());      // reads req.user, writes req.rateLimitState
app.use(checkPermissions());    // reads req.user, writes req.allowed
app.use(injectTenantContext()); // reads req.user, writes req.tenant
app.use(audit());               // reads every field above
```

Here each middleware step mutates `req` in sequence, and the type system can't check which fields exist at each step. Replace the chain with a typed session helper at the entry point and pass the tenant scope into the operation:

```ts
async getOrder(@Req() req: Request) {
  const session = this.auth.requireSession(req, 'order.read');
  return this.orders.find(req.params.id, session.tenantId);
}
```

Keep middleware only for concerns that apply uniformly to every route, such as request logging, metrics, and rate limiting.
