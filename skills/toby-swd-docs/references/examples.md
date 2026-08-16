# Worked Examples

The structure and the scope decisions are what transfer. Backend and frontend, AGENTS.md and README.md.

---

## Example 1 — Backend: a payments service AGENTS.md

Scope decision: `services/payments/` is a meaningful module that owns a real body of knowledge, so it gets one AGENTS.md at its root. `services/payments/util/` does not get its own, and that content pushes up here.

```markdown
# Payments

## What this is
Turns an authorized cart into a settled charge and a ledger entry. Owns the
money path; nothing else in the system is allowed to move funds.

## Files
- gateway.py — the Gateway interface and its provider implementations. Owns
  "how we talk to an external processor."
- ledger.py — append-only double-entry ledger. Owns "what we believe we are
  owed and have collected."
- reconcile.py — matches processor settlement reports against the ledger.

## Constraints that force non-obvious design
- Charges must be idempotent per (order_id, attempt). The retry key threading
  through gateway.py looks redundant; it is required because the processor may
  succeed and then time out our connection. Removing it reintroduces double
  charges.
- We may not store PAN data (PCI). That is why card data is exchanged for a
  token at the edge and only the token reaches this module.

## Cross-module decisions
- "Settlement ordering": the ledger is the source of truth; the processor
  webhook is advisory and may arrive out of order. Billing and
  analytics consume the ledger. Affected sites carry
  `// see "Settlement ordering" in AGENTS.md`.

## Extension rules
- A new processor is a new Gateway implementation plus a config entry.
  Existing gateway code stays untouched.
- The ledger is append-only. Corrections are compensating entries. Code that
  mutates a posted entry is a bug.
```

Note what is absent: no function signatures, no algorithm descriptions. Those live in interface comments in `gateway.py`. This file would survive a full rewrite of the internals unchanged.

---

## Example 2 — Backend: payments service README.md

Same module, different audience. This file is for a developer calling the payments service from outside.

```markdown
# Payments Service

Processes charges and maintains the ledger of what has been collected. You
interact with this service to authorize a cart, capture a payment, and issue
refunds. It owns the money path; other services do not move funds directly.

## Quick start

```python
from payments import Gateway, PaymentRequest

gateway = Gateway.from_config()
result = gateway.charge(PaymentRequest(
    order_id="ord_123",
    amount_cents=4999,
    token="tok_abc",         # card token from the payments edge
    idempotency_key="ord_123_attempt_1"
))
if result.settled:
    # proceed
```

## Concepts

- **Token**: card data is exchanged for a token at the edge before it
  reaches this service. Raw card numbers are never handled here.
- **Idempotency key**: the same (order_id, attempt) combination will return the
  same result even if the call is retried. Always supply one; the service will
  reject requests without it.
- **Ledger as source of truth**: the ledger reflects settled charges; webhooks
  from the processor are advisory and arrive out of order. Query the ledger
  for settlement status.

## Public API

`Gateway.charge(req)` — authorize and capture a single payment.
`Gateway.refund(charge_id, amount_cents)` — partial or full refund.
`Ledger.entries_for_order(order_id)` — returns all ledger entries for an order.

Full signatures and behavior are in the interface comments in `gateway.py`.

## Known gotchas

- Refunds require a `charge_id` from a settled charge. Authorization alone
  does not produce one. Attempting to refund an authorization that was never captured raises
  `ChargeNotSettledError`.
- The idempotency key must be unique per attempt. Reusing a key from a failed
  attempt will return the original failure.
```

Note: the README references the interface comments in `gateway.py` and lets the
single copy there stay authoritative. Implementation details — why idempotency
is required, how the ledger works — live in AGENTS.md. The README stays on what a
caller needs.

---

## Example 3 — Frontend: a feature module AGENTS.md and scope decision

Scope decision: `features/checkout/` is a feature module — one AGENTS.md at its root. `features/checkout/components/PriceRow/` is a leaf component folder — no file. If `PriceRow` has a non-obvious contract, that goes in its prop interface comment.

```markdown
# Checkout (feature)

## What this is
The multi-step checkout flow. Owns flow state and the order of steps; delegates
payment to the payments service and address validation to the address package.

## Files
- machine.ts — the step state machine. Owns "what step the user is on and what
  transitions are legal."
- CheckoutProvider.tsx — supplies flow state via context. Owns the shared
  contract between steps.
- steps/ — one component per step; each renders, none owns flow control.

## Constraints
- Tax cannot be shown until an address is validated (legal requirement in two
  regions). This is why the Review step blocks on address state even though the
  UI could render without it.

## Cross-module decisions
- "Checkout context shape": steps read flow state only from CheckoutProvider.
  Nothing in this feature reads it via props drilled from the page. The shape
  is defined and commented at
  CheckoutProvider; this is the central note. Step files carry
  `// see "Checkout context shape" in AGENTS.md`.

## Extension rules
- A new step is a component in steps/ plus a transition in machine.ts. Flow
  logic stays in machine.ts.
- Shared step state goes on the context.
```

---

## Example 4 — Frontend: checkout feature README.md

This module's README.md is minimal because it serves developers already inside the codebase, with none of the orientation a shared library owes outside callers. A README.md here only exists because the context shape is non-obvious to developers onboarding to this part of the codebase.

```markdown
# Checkout Feature

The multi-step checkout flow: cart → address → payment → review → confirmation.

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
`useCheckoutMachine()`. Steps do not know about each other. Adding a new step
means a new component in `steps/` and a new transition in `machine.ts`.
Existing steps stay unchanged.

## Known constraints

- Tax display is blocked until address validation completes. This is a legal
  requirement. Don't try to work around it.
- Flow state lives in `CheckoutProvider`. Do not lift it to a parent or store
  it externally — the machine enforces valid transitions and bypassing it
  produces inconsistent UI state.
```

The cross-module note about context shape lives in AGENTS.md. The README
only explains what a developer needs to use the feature correctly.
