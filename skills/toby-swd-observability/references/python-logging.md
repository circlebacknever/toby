# Python logging

This file shows how to pass structured fields to Python's standard `logging` module and `structlog`.

## Default formatter

The default `logging` formatter prints only the message string and drops `extra` fields. Append `key=value` pairs to the message and list a JSON formatter as a follow-up:

```python
log.info("order.cancelled order_id=%s user_id=%s refund_cents=%s", order.id, user.id, refund)
```

## JSON formatter

When `logging` uses a JSON formatter, pass fields in `extra={"order_id": order.id}`. Avoid reserved `LogRecord` attribute names (`name`, `message`, `asctime`, `levelname`, `args`, `exc_info`) in `extra`, because `Logger.info()` raises `KeyError` on a collision.

## structlog

In `structlog`, pass fields as keyword arguments, as `SKILL.md` shows.
