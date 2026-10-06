# Worked Examples

Reuse the structure and the scope decisions in your own modules. The examples cover a backend module with an AGENTS.md and a README.md, and a frontend scope decision.

---

## Example 1 — Backend: a payments service AGENTS.md

Scope decision: `services/payments/` is a meaningful module with its own body of knowledge, so it gets one AGENTS.md at its root. `services/payments/util/` does not get its own, so its content moves up into this file.

```markdown
# Payments

## What this is
This module turns an authorized cart into a settled charge and a ledger entry. It is the only
part of the system that is allowed to move funds.

## Commands
- `pytest services/payments` runs the module's tests.

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

## How to use it

```python
from payments import Gateway, PaymentRequest

gateway = Gateway.from_config()
result = gateway.charge(PaymentRequest(
    order_id="ord_123",
    amount_cents=4999,
    token="tok_abc",         # The card token comes from the payments edge.
    idempotency_key="ord_123_attempt_1"
))
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
single copy there stays authoritative. AGENTS.md states why idempotency is
required and why the ledger is the source of truth. The README covers only what
a caller needs.

---

## Example 3 — Frontend: a feature module scope decision

Scope decision: `features/checkout/` is a feature module, so it gets one AGENTS.md at its root. `features/checkout/components/PriceRow/` is a leaf component folder, so it gets no file. If `PriceRow` has a non-obvious contract, that contract goes in its prop interface comment.
