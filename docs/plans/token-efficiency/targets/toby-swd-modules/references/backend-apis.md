# Backend APIs (Java/Kotlin, Go, TypeScript)

## Base controller

A `BaseController` with protected helpers and shared fields such as `currentUser` couples the base and every controller in both directions. A change to the base means reading every subclass. Turn each group of helpers into an injected collaborator:

```java
@RestController
public class OrderController {
    private final OrderService orders;
    private final AuthzGuard authz;        // was requireRole()
    private final ResponseBuilder respond; // was ok() and error()

    @GetMapping("/orders/{id}")
    public ResponseEntity<?> getOrder(@PathVariable String id, Principal p) {
        authz.require(p, Role.ORDER_READ);
        return respond.ok(orders.find(id));
    }
}
```

Access logging, which every handler used to call, moves to a `HandlerInterceptor` or AOP advice that the dispatcher applies once.

## Middleware chain

```ts
app.use(loadCurrentUser());     // writes req.user
app.use(checkRateLimit());      // reads req.user, writes req.rateLimitState
app.use(checkPermissions());    // reads req.user, writes req.allowed
app.use(injectTenantContext()); // reads req.user, writes req.tenant
app.use(audit());               // reads every field above
```

This chain is temporal decomposition. Each step reads fields an earlier step wrote on `req`, so the request contract is the union of those fields and no module defines it. Make authentication, authorization, and tenancy named services that return typed values:

```ts
async getOrder(@Req() req: Request) {
  const session = this.auth.forRequest(req);              // user and tenant, or throws
  this.authz.require(session, 'order.read', { id: req.params.id });
  return this.orders.find(req.params.id, session.tenantId);
}
```

Keep middleware or interceptors only for concerns that apply to every request unchanged, such as logging and metrics.
