---
name: toby-swd-observability
description: >-
  Contains Toby's rules for logs, metrics, alerts, and traces in code that runs
  in production. Entry skills open this file by path. Do not trigger it from a
  user request alone.
disable-model-invocation: true
---

# Toby SWD Observability

Write logs and metrics for the engineer paged at 3 a.m. who has never read this code. From the logs alone, that person can tell what the system did, for which request, and why it failed.

## Use what the repo has

Find the repo's logger, metrics client, and tracer in a nearby handler, and use them in their existing format. Ask before adding a library or switching the repo to a structured logger.

## Log lines

Write each log line as an event name plus named fields. Read the logger's formatter first, because some formatters drop extra fields. When the formatter prints extra fields, as structlog and JSON formatters do, pass each value as a field.

```python
log.info("order.cancelled", order_id=order.id, user_id=user.id, refund_cents=refund, duration_ms=elapsed)
```

With Python's `logging`, pass these fields as `extra={...}`, as `references/python-logging.md` shows.

When the formatter prints only the message, write `key=value` pairs after the event name, and list a structured formatter as a follow-up.

- Keep the event name stable, in the form `noun.verb_past`.
- When the repo sets a request id or trace id, keep it on each new line, and pass it on in new outbound calls and queued messages. When the repo sets neither, log the ids the entry point acted on, and list request-id middleware as a follow-up.
- Use one field name for one thing everywhere, such as `order_id`.

## Levels

- `error` means a person needs to act. Bad user input is `info` or `warn`.
- `warn` means the code handled something rare, such as a fallback that ran.
- `info` records a state change, such as created, paid, or cancelled.
- `debug` is off in production, so put nothing there the on-call engineer needs.

## The outcome log

When an entry point changes state or calls another service, log one line as it finishes. The line holds the event name, the ids it acted on, the result, and the duration, as in the `order.cancelled` example. A request log from middleware records the path and the status, and the outcome log adds which record changed and how. A queue consumer and a scheduled job are entry points too. A read-only entry point needs no outcome log.

## What else to log

- Each call to another service, with the target, the duration, and the result.
- Each decision that changes the result, such as a flag value.
- Each error, once, with its stack trace, at the handler that deals with it, such as with `log.exception` in Python.
- Inside a loop, only a failed item, with its id. After the loop, one line with the success count, the failure count, and the duration.

## What never to log

Never log passwords, tokens, API keys, cookies, card numbers, a raw request or response body, or a whole model object. Log a person by user id, and leave out the email and the name. Treat a secret written to a log as leaked, and rotate it.

## Metrics

Give a new entry point the metrics its sibling entry points record, including their business-event counters. Record a duration as a histogram, so a dashboard can show p95 and p99. When the change adds a queue, record its depth and the age of its oldest message. When the repo has no metrics client, add `duration_ms` to an outcome log the entry point already writes, and ask before adding a client.

Keep each metric label to a small fixed set of values, such as a route template or a status class.

## Alerts

State which alert pages someone when a new entry point's error rate rises, unless only staff call it. When none does, list the missing alert as a follow-up, with its metric and threshold.

Before renaming an event or a metric, search the repo for alert and dashboard definitions, such as `*.rules.yml`, a `monitors/` folder, or a Terraform `datadog_monitor`. When the definitions live in another repo, list the rename as a risk. When an alert reads a log event or a metric, test that the code emits it with the fields the alert reads.

## Traces

When the repo already uses tracing, such as OpenTelemetry, pass the trace context on. Add a span around a new outbound call or slow step only where auto-instrumentation does not already create one. Auto-instrumentation covers most HTTP clients and database drivers. Ask before adding tracing to a repo that has none.
