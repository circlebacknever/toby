"""Materialize a small application and its proposed refactor for independent reviews."""

from __future__ import annotations

import textwrap


def source(text: str) -> str:
    """Remove indentation from a source literal and preserve its final newline."""
    return textwrap.dedent(text).lstrip("\n")


BASE = {
    "README.md": source('''
        # Parcel

        Parcel manages orders and their payment and shipping work.

        ## Contracts

        Orders are private to their account. Invoice arithmetic uses integer cents
        and rounds tax half up. The event consumer is deployed separately and reads
        `order_id` from the existing JSON format. The producer must remain compatible.
        One inventory unit can satisfy one reservation, including concurrent requests.
        Retrying a payment or a paid-order dispatch must perform its external effect once.
        Paid orders must eventually publish their event after an interrupted attempt.
        The order listing accepts a client limit and returns at most 100 rows.
        Tracking calls must specify a timeout of three seconds.
        Failed syncs must print the request, record, and original exception with the
        deployed formatter. The billing key is required and must fail validation at startup.
        The `/returns` endpoint must remain reachable. Refunds require a paid order
        created between zero and thirty days ago, inclusive.

        ## Commands

        Run `python3 -B -m unittest discover -s tests` from this directory.
        The tests use SQLite and local substitutes for external services.
    '''),
    "CHANGE.md": source('''
        # Payment cleanup

        This change simplifies the billing and shipping modules while retaining the contracts in README.md.

        The design was approved before implementation. It uses the shorter `id`
        field in shipment messages and copies the legacy refund and sync handlers.
        Review the implementation against the existing consumer and product contracts.
    '''),
    "parcel/__init__.py": '"""Order operations used by the HTTP and worker entry points."""\n',
    "parcel/database.py": source('''
        """Create the application's SQLite connection and schema."""
        import sqlite3

        def connect(path=":memory:"):
            connection = sqlite3.connect(path, timeout=5)
            connection.row_factory = sqlite3.Row
            return connection

        def initialize(connection):
            connection.executescript("""
                CREATE TABLE IF NOT EXISTS orders (
                    id TEXT PRIMARY KEY, account_id TEXT NOT NULL,
                    status TEXT NOT NULL, created_day INTEGER NOT NULL DEFAULT 0
                );
                CREATE TABLE IF NOT EXISTS inventory (
                    id TEXT PRIMARY KEY, available INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS reservations (
                    id INTEGER PRIMARY KEY, product_id TEXT NOT NULL,
                    quantity INTEGER NOT NULL
                );
                CREATE TABLE IF NOT EXISTS outbox (
                    order_id TEXT PRIMARY KEY, payload TEXT NOT NULL
                );
            """)
            connection.commit()
    '''),
    "parcel/orders.py": source('''
        """Look up an order for the account making the request."""
        def lookup_order(connection, account_id, order_id):
            row = connection.execute(
                "SELECT * FROM orders WHERE id = ? AND account_id = ?",
                (order_id, account_id),
            ).fetchone()
            return dict(row) if row else None
    '''),
    "parcel/billing.py": source('''
        """Calculate an invoice total in integer cents."""
        def invoice_total(subtotal_cents, tax_percent):
            if subtotal_cents < 0 or not 0 <= tax_percent <= 100:
                raise ValueError("Invalid invoice amount or tax")
            tax_cents = (subtotal_cents * tax_percent + 50) // 100
            return subtotal_cents + tax_cents
    '''),
    "parcel/events.py": source('''
        """Write shipment messages for the separately deployed consumer."""
        import json

        def encode_order(order_id):
            return json.dumps({"order_id": order_id, "version": 1}).encode()

        def read_order(payload):
            return json.loads(payload)["order_id"]
    '''),
    "parcel/inventory.py": source('''
        """Reserve units without allocating the same unit twice."""
        def reserve(connection, product_id, quantity):
            if quantity < 1:
                raise ValueError("Quantity must be positive")
            with connection:
                row = connection.execute(
                    "UPDATE inventory SET available = available - ? "
                    "WHERE id = ? AND available >= ? RETURNING available",
                    (quantity, product_id, quantity),
                ).fetchone()
                if row is None:
                    return False
                connection.execute(
                    "INSERT INTO reservations(product_id, quantity) VALUES (?, ?)",
                    (product_id, quantity),
                )
            return True
    '''),
    "parcel/payments.py": source('''
        """Collect one charge even when the provider loses its response."""
        import uuid

        def collect_charge(gateway, order_id, amount_cents):
            key = "charge:" + order_id
            for attempt in range(2):
                try:
                    return gateway.charge(amount_cents, idempotency_key=key)
                except TimeoutError:
                    if attempt == 1:
                        raise
    '''),
    "parcel/dispatch.py": source('''
        """Persist paid orders and publish their events through the outbox."""
        import json

        def mark_paid(connection, publisher, order_id):
            order = connection.execute(
                "SELECT status FROM orders WHERE id = ?", (order_id,)
            ).fetchone()
            if order["status"] == "paid":
                return "paid"
            payload = json.dumps({"order_id": order_id})
            with connection:
                connection.execute(
                    "UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,)
                )
                connection.execute(
                    "INSERT INTO outbox(order_id, payload) VALUES (?, ?)",
                    (order_id, payload),
                )
            return "paid"

        def flush_outbox(connection, publisher):
            for row in connection.execute("SELECT * FROM outbox").fetchall():
                publisher.publish(row["payload"], event_id=row["order_id"])
                with connection:
                    connection.execute(
                        "DELETE FROM outbox WHERE order_id = ?", (row["order_id"],)
                    )
    '''),
    "parcel/search.py": source('''
        """List a bounded page of orders for one account."""
        def page_orders(connection, account_id, requested_limit):
            limit = min(max(int(requested_limit), 1), 100)
            rows = connection.execute(
                "SELECT * FROM orders WHERE account_id = ? ORDER BY id LIMIT ?",
                (account_id, limit),
            )
            return [dict(row) for row in rows]
    '''),
    "parcel/tracking.py": source('''
        """Fetch one shipment status within the caller's timeout budget."""
        def track(client, shipment_id):
            return client.get("/shipments/" + shipment_id, timeout=3)
    '''),
    "parcel/worker.py": source('''
        """Sync a record and print enough context to diagnose a failed attempt."""
        def sync_record(client, record_id, request_id, logger):
            try:
                client.sync(record_id)
            except Exception:
                logger.exception(
                    "sync.failed record_id=%s request_id=%s", record_id, request_id
                )
                return False
            logger.info("sync.completed record_id=%s request_id=%s", record_id, request_id)
            return True
    '''),
    "parcel/runtime.py": source('''
        """Configure the formatter deployed in the worker process."""
        import logging

        def configure_logger(stream):
            logger = logging.Logger("parcel.worker")
            handler = logging.StreamHandler(stream)
            handler.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
            logger.addHandler(handler)
            return logger
    '''),
    "parcel/config.py": source('''
        """Validate the values required before the application accepts traffic."""
        def load_config(environment):
            billing_key = environment.get("BILLING_API_KEY", "").strip()
            if not billing_key:
                raise ValueError("BILLING_API_KEY is required")
            return {"billing_key": billing_key}
    '''),
    "parcel/routes.py": source('''
        """Register public endpoints and dispatch incoming requests."""
        from .refunds import refund_order
        from .orders import lookup_order
        from .search import page_orders

        def health(request):
            return 200, {"status": "up"}

        def returns(request):
            return 200, {"returns": []}

        def order(request):
            row = lookup_order(request["connection"], request["account_id"], request["order_id"])
            return (200, row) if row else (404, {})

        def order_list(request):
            return 200, page_orders(request["connection"], request["account_id"], request["limit"])

        def refund(request):
            return refund_order(request["order"], request["today"])

        ROUTES = {"/health": health, "/returns": returns, "/orders/get": order,
                  "/orders/list": order_list, "/orders/refund": refund}

        def dispatch(path, request):
            handler = ROUTES.get(path)
            return handler(request) if handler else (404, {})
    '''),
    "parcel/eligibility.py": source('''
        """Apply the same refund policy to HTTP requests and support commands."""
        def can_refund(order, today):
            return order["status"] == "paid" and 0 <= today - order["created_day"] <= 30
    '''),
    "parcel/refunds.py": source('''
        """Refund an eligible order through the common policy."""
        from .eligibility import can_refund

        def refund_order(order, today):
            if not can_refund(order, today):
                return 409, {"error": "Order cannot be refunded"}
            order["status"] = "refunded"
            return 200, {"status": "refunded"}
    '''),
    "parcel/support.py": source('''
        """Let support use the same refund policy as the HTTP endpoint."""
        from .eligibility import can_refund

        def refund_allowed(order, today):
            return can_refund(order, today)
    '''),
    "parcel/legacy.py": source('''
        """Retain old handlers that this change doesn't migrate."""
        def refund_allowed(order, today):
            return 0 <= today - order["created_day"] <= 30

        def log_failure(logger, record_id, request_id):
            logger.error("sync failed", extra={"record_id": record_id, "request_id": request_id})
    '''),
    "parcel/admin.py": source('''
        """Restrict administrative counts to trusted table names and account scope."""
        TABLES = {"orders": "orders", "stock": "inventory"}

        def count_rows(connection, actor, kind):
            if actor["role"] != "admin":
                raise PermissionError("Admin role required")
            table = TABLES[kind]
            return connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]

        def cache_key(account_id, order_id):
            return account_id, order_id
    '''),
    "parcel/wire.py": source('''
        """Preserve required receipt fields while allowing optional metadata."""
        def receipt(order_id, amount_cents):
            return {"order_id": order_id, "amount_cents": amount_cents}

        def read_receipt(payload):
            return payload["order_id"], payload["amount_cents"]
    '''),
    "tests/test_smoke.py": source('''
        """Check ordinary local calls without using an external service."""
        import unittest
        from parcel.billing import invoice_total
        from parcel.database import connect, initialize
        from parcel.events import read_order
        from parcel.routes import dispatch, returns
        from parcel.config import load_config
        from parcel.wire import receipt, read_receipt

        class SmokeTests(unittest.TestCase):
            def test_invoice(self):
                self.assertEqual(invoice_total(1000, 20), 1200)

            def test_existing_message(self):
                self.assertEqual(read_order(b'{"order_id":"o1","version":1}'), "o1")

            def test_handlers(self):
                self.assertEqual(dispatch("/health", {})[0], 200)
                self.assertEqual(returns({})[0], 200)

            def test_config(self):
                self.assertEqual(load_config({"BILLING_API_KEY": "test"})["billing_key"], "test")

            def test_receipt(self):
                self.assertEqual(read_receipt(receipt("o1", 1200)), ("o1", 1200))

            def test_orders(self):
                with connect() as connection:
                    initialize(connection)
                    connection.execute("INSERT INTO orders VALUES ('o1', 'a1', 'paid', 0)")
                    result = dispatch("/orders/get", {"connection": connection,
                                      "account_id": "a1", "order_id": "o1"})
                    self.assertEqual(result[1]["id"], "o1")

        if __name__ == "__main__":
            unittest.main()
    '''),
}


REPLACEMENTS = {
    "parcel/orders.py": [(
        '"SELECT * FROM orders WHERE id = ? AND account_id = ?",\n        (order_id, account_id),',
        '"SELECT * FROM orders WHERE id = ?",\n        (order_id,),',
    )],
    "parcel/billing.py": [(
        'tax_cents = (subtotal_cents * tax_percent + 50) // 100',
        'tax_cents = subtotal_cents // 100 * tax_percent',
    )],
    "parcel/events.py": [(
        '{"order_id": order_id, "version": 1}',
        '{"id": order_id, "version": 1}',
    )],
    "parcel/payments.py": [(
        'key = "charge:" + order_id\n    for attempt in range(2):',
        'for attempt in range(2):\n        key = str(uuid.uuid4())',
    )],
    "parcel/search.py": [(
        'limit = min(max(int(requested_limit), 1), 100)',
        'limit = int(requested_limit)',
    )],
    "parcel/tracking.py": [(
        'client.get("/shipments/" + shipment_id, timeout=3)',
        'client.get("/shipments/" + shipment_id)',
    )],
    "parcel/worker.py": [(
        'logger.exception(\n            "sync.failed record_id=%s request_id=%s", record_id, request_id\n        )',
        'logger.error("sync failed", extra={"record_id": record_id, "request_id": request_id})',
    )],
    "parcel/config.py": [(
        'billing_key = environment.get("BILLING_API_KEY", "").strip()\n    if not billing_key:\n        raise ValueError("BILLING_API_KEY is required")',
        'billing_key = environment.get("BILLING_API_KEY", "")',
    )],
    "parcel/routes.py": [(
        'ROUTES = {"/health": health, "/returns": returns, "/orders/get": order,',
        'ROUTES = {"/health": health, "/orders/get": order,',
    )],
    "parcel/refunds.py": [(
        'if not can_refund(order, today):',
        'if not 0 <= today - order["created_day"] <= 30:',
    )],
    "parcel/admin.py": [(
        'return account_id, order_id',
        'return (account_id, order_id)',
    )],
    "parcel/wire.py": [(
        '{"order_id": order_id, "amount_cents": amount_cents}',
        '{"order_id": order_id, "amount_cents": amount_cents, "source": "web"}',
    )],
}


AFTER_FILES = {
    "parcel/inventory.py": source('''
        """Reserve units without allocating the same unit twice."""
        def reserve(connection, product_id, quantity):
            if quantity < 1:
                raise ValueError("Quantity must be positive")
            with connection:
                row = connection.execute(
                    "SELECT available FROM inventory WHERE id = ?", (product_id,)
                ).fetchone()
                if row is None or row["available"] < quantity:
                    return False
                connection.execute(
                    "UPDATE inventory SET available = ? WHERE id = ?",
                    (row["available"] - quantity, product_id),
                )
                connection.execute(
                    "INSERT INTO reservations(product_id, quantity) VALUES (?, ?)",
                    (product_id, quantity),
                )
            return True
    '''),
    "parcel/dispatch.py": source('''
        """Persist paid orders and publish their events through the outbox."""
        import json

        def mark_paid(connection, publisher, order_id):
            order = connection.execute(
                "SELECT status FROM orders WHERE id = ?", (order_id,)
            ).fetchone()
            if order["status"] == "paid":
                return "paid"
            payload = json.dumps({"order_id": order_id})
            with connection:
                connection.execute(
                    "UPDATE orders SET status = 'paid' WHERE id = ?", (order_id,)
                )
            publisher.publish(payload, event_id=order_id)
            return "paid"

        def flush_outbox(connection, publisher):
            for row in connection.execute("SELECT * FROM outbox").fetchall():
                publisher.publish(row["payload"], event_id=row["order_id"])
                with connection:
                    connection.execute(
                        "DELETE FROM outbox WHERE order_id = ?", (row["order_id"],)
                    )
    '''),
}


def changed_files() -> dict[str, str]:
    """Apply each proposed edit once and reject a stale fixture anchor."""
    result = dict(BASE)
    for path, replacements in REPLACEMENTS.items():
        for old, new in replacements:
            if result[path].count(old) != 1:
                raise ValueError(f"Fixture anchor must occur once: {path}: {old!r}")
            result[path] = result[path].replace(old, new, 1)
    result.update(AFTER_FILES)
    return result
