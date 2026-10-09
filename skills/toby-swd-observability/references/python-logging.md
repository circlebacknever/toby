# Python logging

This file shows how to pass log fields with Python's `logging` module and with structlog.

## The default formatter

The default formatter in Python's `logging` prints only the message and drops extra fields. Write `key=value` pairs after the event name, and list a structured formatter as a follow-up.

```python
log.info("order.cancelled order_id=%s user_id=%s refund_cents=%s", order.id, user.id, refund)
```

## A JSON formatter

Python's `logging` with a JSON formatter takes fields as `extra={"order_id": order.id}`. `Logger.info()` raises `KeyError` for an `extra` key that matches a LogRecord attribute, such as `name` or `message`.

## structlog

In structlog, pass the fields as keyword arguments, as the `order.cancelled` example in `SKILL.md` does.
