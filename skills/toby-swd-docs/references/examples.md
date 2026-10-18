# Worked Examples

This file shows how to structure a module's `AGENTS.md` and `README.md` and how to decide which folder gets one.

---

## 1. Service AGENTS.md

Scope decision: `services/payments/` covers a distinct domain, so it gets one `AGENTS.md` at its root, while `services/payments/util/` does not.

```markdown
# Payments

## What this is
This module turns an authorized cart into a settled charge and a ledger entry. It is the only
part of the system that moves funds.

## Commands
- `pytest services/payments` runs the module's tests.

## Constraints
- Charges are idempotent per `idempotency_key` (one key per payment intent). A retry after a
  timeout must reuse the same key, because the processor may have succeeded before the connection
  dropped. Rotating the key on a timeout charges the card twice.
- PCI rules forbid storing raw card numbers, so the edge service exchanges card numbers for tokens
  and passes only tokens to this module.

## Cross-module decisions
- "Settlement ordering": the ledger is the source of truth, because processor webhooks arrive
  out of order. Billing and analytics read the ledger. Affected sites contain
  `// see "Settlement ordering" in AGENTS.md`.

## Extension rules
- A new payment processor is a new `Gateway` implementation plus a config entry, leaving existing
  gateway code unchanged.
- The ledger is append-only, so refunds and adjustments write compensating entries and never
  mutate posted rows.
```

---

## 2. Service README.md

This `README.md` covers the same payments module for developers who call it from other services.

```markdown
# Payments Service

This service authorizes carts, captures charges, issues refunds, and maintains the payment ledger.

## How to use it

```python
from payments import Gateway, PaymentRequest

gateway = Gateway.from_config()
result = gateway.charge(PaymentRequest(
    order_id="ord_123",
    amount_cents=4999,
    token="tok_abc",         # Card token from the payments edge.
    idempotency_key="ord_123_charge_1"
))
```

## Concepts

- **Token**: the edge exchanges raw card data for a token before calling this service.
- **Idempotency key**: retrying a timed-out call with the same `idempotency_key` returns the
  original result without charging twice. Generate a new key only after the processor returns a
  terminal decline and the customer submits a new payment attempt.
- **Ledger**: the ledger records settled charges and refunds, and callers query the ledger for settlement state.

## Public API

- `Gateway.charge(req)` authorizes and captures a payment.
- `Gateway.refund(charge_id, amount_cents)` issues a partial or full refund.
- `Ledger.entries_for_order(order_id)` returns all ledger entries for an order.

Full signatures and error types are in the docstrings in `gateway.py`.

## Known gotchas

- `Gateway.refund` requires a `charge_id` from a settled charge, and refunding an uncaptured
  authorization raises `ChargeNotSettledError`.
- Reusing an `idempotency_key` with a different `amount_cents` or `order_id` raises
  `IdempotencyConflictError`.
```

---

## 3. Frontend module scope

Scope decision: `features/checkout/` is a feature module and gets one `AGENTS.md` at its root. `features/checkout/components/PriceRow/` holds one component and has no subfolders, so its caller constraints belong in the doc comment on `PriceRowProps`.
