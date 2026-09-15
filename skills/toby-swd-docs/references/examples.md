# Worked Examples

Reuse the structure and the scope decisions in your own modules. The examples cover a backend module and a frontend module, each with an AGENTS.md and a README.md.

---

## Example 1 — Backend: a payments service AGENTS.md

Scope decision: `services/payments/` is a meaningful module with its own body of knowledge, so it gets one AGENTS.md at its root. `services/payments/util/` does not get its own, so its content moves up into this file.

```markdown
# Payments

## What this is
This module turns an authorized cart into a settled charge and a ledger entry. It is the only
part of the system that is allowed to move funds.

## Files
- `gateway.py` defines the Gateway interface and its provider implementations.
- `ledger.py` stores the append-only double-entry ledger of what the business is owed and
  has collected.
- `reconcile.py` matches processor settlement reports against the ledger.

## Constraints
- Charges must be idempotent per (order_id, attempt). The retry key passed
  through gateway.py looks redundant, but it is required because the processor may
  succeed and then time out our connection. Removing it reintroduces double
  charges.
- We may not store PAN data (PCI). That is why card data is exchanged for a
  token at the edge and only the token reaches this module.

## Cross-module decisions
- "Settlement ordering": the ledger is the source of truth. The processor
  webhook is advisory and may arrive out of order. Billing and
  analytics consume the ledger. Affected sites contain
  `// see "Settlement ordering" in AGENTS.md`.

## Extension rules
- A new processor is a new Gateway implementation plus a config entry.
  Existing gateway code stays untouched.
- The ledger is append-only, so corrections are compensating entries. Code that
  mutates a posted entry is a bug.
```

The file has no function signatures and no algorithm descriptions, because those are in interface comments in `gateway.py`. This file would stay accurate through a full rewrite of the internals.

---

## Example 2 — Backend: payments service README.md

This README.md covers the same payments module for a developer who calls the service from outside.

```markdown
# Payments Service

This service processes charges and maintains the ledger of what has been collected. You
interact with this service to authorize a cart, capture a payment, and issue
refunds. It is the only service that moves funds directly.

## Quick start

```python
from payments import Gateway, PaymentRequest

gateway = Gateway.from_config()
result = gateway.charge(PaymentRequest(
    order_id="ord_123",
    amount_cents=4999,
    token="tok_abc",         # The card token comes from the payments edge.
    idempotency_key="ord_123_attempt_1"
))
if result.settled:
    # The charge settled, so proceed here.
```

## Concepts

- **Token**: card data is exchanged for a token at the edge before it
  reaches this service. Raw card numbers are never handled here.
- **Idempotency key**: a call with the same (order_id, attempt) combination will return the
  same result even if the call is retried. Always supply one, because the service will
  reject requests without it.
- **Ledger as source of truth**: the ledger records settled charges. Webhooks
  from the processor are advisory and arrive out of order. Query the ledger
  for settlement status.

## Public API

`Gateway.charge(req)` — authorize and capture a single payment.
`Gateway.refund(charge_id, amount_cents)` — issue a partial or full refund.
`Ledger.entries_for_order(order_id)` — returns all ledger entries for an order.

Full signatures and behavior are in the interface comments in `gateway.py`.

## Known gotchas

- Refunds require a `charge_id` from a settled charge. Authorization alone
  does not produce one. Attempting to refund an authorization that was never captured raises
  `ChargeNotSettledError`.
- The idempotency key must be unique per attempt. Reusing a key from a failed
  attempt will return the original failure.
```

The README references the interface comments in `gateway.py`, so the
single copy there stays authoritative. AGENTS.md explains the implementation
details, such as why idempotency is required and how the ledger works. The
README covers only what a caller needs.

---

## Example 3 — Frontend: a feature module AGENTS.md and scope decision

Scope decision: `features/checkout/` is a feature module, so it gets one AGENTS.md at its root. `features/checkout/components/PriceRow/` is a leaf component folder, so it gets no file. If `PriceRow` has a non-obvious contract, that contract goes in its prop interface comment.

```markdown
# Checkout (feature)

## What this is
This module is the multi-step checkout flow. It manages flow state and the order of steps, and it delegates
payment to the payments service and address validation to the address package.

## Files
- `machine.ts` defines the step state machine, which tracks the current step and the legal
  transitions.
- `CheckoutProvider.tsx` supplies flow state through context and defines the contract that
  steps share.
- `steps/` contains one component per step. A step component renders its step, and
  `machine.ts` handles flow control.

## Constraints
- Tax cannot be shown until an address is validated (legal requirement in two
  regions). This is why the Review step blocks on address state even though the
  UI could render without it.

## Cross-module decisions
- "Checkout context shape": steps read flow state only from CheckoutProvider.
  Code in this feature does not read it via props drilled from the page. The context type
  is defined and commented at
  CheckoutProvider. This section is the central note. Step files contain
  `// see "Checkout context shape" in AGENTS.md`.

## Extension rules
- A new step is a component in steps/ plus a transition in machine.ts. Flow
  logic stays in machine.ts.
- Shared step state goes on the context.
```

---

## Example 4 — Frontend: checkout feature README.md

This module's README.md is minimal because its readers already work in the codebase and need none of the orientation a shared library gives outside callers. A README.md here only exists because the context contents are non-obvious to developers onboarding to this part of the codebase.

```markdown
# Checkout Feature

This feature is the multi-step checkout flow: cart → address → payment → review → confirmation.

## How it works

Wrap the checkout entry point with `<CheckoutProvider>`. Step components
consume flow state from context. They take no flow props.

```tsx
import { CheckoutProvider, CheckoutFlow } from 'features/checkout'

export function CheckoutPage() {
  return (
    <CheckoutProvider orderId={orderId}>
      <CheckoutFlow />
    </CheckoutProvider>
  )
}
```

## Concept: step isolation

Each step component renders its own content and fires transitions via
`useCheckoutMachine()`. Steps do not depend on each other. Adding a new step
means a new component in `steps/` and a new transition in `machine.ts`.
Existing steps stay unchanged.

## Known constraints

- Tax display is blocked until address validation completes. This is a legal
  requirement, so don't try to work around it.
- Flow state is in `CheckoutProvider`. Do not lift it to a parent or store
  it externally. The machine enforces valid transitions, so bypassing it
  produces inconsistent UI state.
```

The cross-module note about context contents is in AGENTS.md. The README
only explains what a developer needs to use the feature correctly.
