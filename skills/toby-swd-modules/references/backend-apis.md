# Backend APIs (Java/Kotlin, Go, TypeScript)

## Base controller

A `BaseController` with protected helpers and shared fields such as `currentUser` couples the base and every controller in both directions. A change to the base means reading every subclass. Move each group of helpers into its own class, and pass an instance of that class into each controller's constructor:

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

Move access logging, which every handler used to call, into one `HandlerInterceptor` or AOP advice that Spring runs on every request.

## Middleware chain

```ts
app.use(loadCurrentUser());     // writes req.user
app.use(checkRateLimit());      // reads req.user, writes req.rateLimitState
app.use(checkPermissions());    // reads req.user, writes req.allowed
app.use(injectTenantContext()); // reads req.user, writes req.tenant
app.use(audit());               // reads every field above
```

This chain is temporal decomposition. Each step reads fields that an earlier step wrote on `req`. So a handler can expect on `req` whatever the earlier steps added. No module writes down that list. Make authentication, authorization, and tenant lookup separate services that return typed values:

```ts
async getOrder(@Req() req: Request) {
  const session = this.auth.forRequest(req);              // user and tenant, or throws
  this.authz.require(session, 'order.read', { id: req.params.id });
  return this.orders.find(req.params.id, session.tenantId);
}
```

Keep middleware or interceptors only for concerns that apply to every request unchanged, such as logging and metrics.
