---
name: toby-swd-observability
description: >-
  Contains Toby's rules for logs, metrics, alerts, and traces in code that runs
  in production. Use it when adding logging, metrics, alerts, or tracing, or a
  new entry point that needs them. Skip it for debug output during a bug hunt,
  which toby-bug-fix covers.
---

# Toby SWD Observability

Write logs and metrics for the engineer paged at 3 a.m. so they can tell from the logs alone what ran, for which request and record, and why it failed.

## Use what the repo has

Use the repo's existing logger, metrics client, and tracer in their established format, and ask before adding a library or changing the repo's log formatter.

## Log lines

Write each log line as a stable `noun.verb_past` event name plus named fields. Check the logger's formatter first: when it outputs structured fields (such as `structlog` or a JSON formatter), pass each value as a field (with `extra={...}` in standard Python `logging`, `references/python-logging.md`); when it prints only the message string, append `key=value` pairs and list a structured formatter as a follow-up.

```python
log.info("order.cancelled", order_id=order.id, user_id=user.id, refund_cents=refund, duration_ms=elapsed)
```

- Use one field name for each concept everywhere (`order_id`), and end numeric field names with their unit (`_ms`, `_seconds`, `_bytes`, `_cents`).
- Propagate `request_id` and `trace_id` across spawned async tasks, threads, outbound calls, and queued messages (`contextvars` or `AsyncLocalStorage`). When the repo sets neither, log the domain record ids and list request-id middleware as a follow-up.

## Levels

- `error`: a person must act or a request failed unexpectedly. Client 4xx validation errors are `info` or `warn`.
- `warn`: the code recovered from an unusual condition, such as a fallback or retry.
- `info`: a business state change completed (`order.created`, `order.cancelled`).
- `debug`: off in production, so never put diagnostics needed during an incident at `debug`.

## The outcome log

When an entry point (HTTP route, RPC, queue consumer, or scheduled job) mutates state or calls an external service, log one summary line when it finishes with the event name, record ids, outcome, and `duration_ms`. Read-only entry points covered by access middleware don't need a second log line.

## Other events

- Log each outbound service call with the target, `duration_ms`, and status or error.
- Log decisions that branch behavior, such as a feature flag or fallback path.
- Log an unhandled error once with its stack trace at the handler that catches and responds to it (`log.exception`).
- Inside a batch loop, log only failed items (rate-limited or sampled under high volume) and log one summary line after the loop with `succeeded_count`, `failed_count`, and `duration_ms`.

## Redacted data

Never log passwords, tokens, API keys, session cookies, card numbers, raw request or response bodies, or whole ORM/model objects. Log users by `user_id` without email addresses or full names. If a secret reaches a log, rotate it.

## Metrics

Match the metrics that sibling entry points record, ending metric names with their unit (`_seconds`, `_bytes`, `_total`). Record latencies as histograms so dashboards show p95 and p99, and record queue depth and oldest-message age for queues. Keep metric labels to small bounded sets (route templates and status classes, never `user_id` or `order_id`).

## Alerts

State which alert pages on-call when a new public entry point's error rate spikes, or list the missing alert with its metric and threshold as a follow-up. Before renaming a log event or metric, search the repo for alert and dashboard definitions (`*.rules.yml`, `monitors/`, Terraform monitors), and test any event or metric that drives a paging alert.

## Traces

When the repo uses OpenTelemetry or another tracer, propagate the trace context across calls and queues, and add manual spans only around slow internal steps that auto-instrumentation doesn't already wrap.
