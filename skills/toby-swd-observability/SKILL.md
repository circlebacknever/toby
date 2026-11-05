---
name: toby-swd-observability
description: >-
  Checks whether production behavior can be diagnosed from logs, metrics,
  alerts, and traces. Use it for changed operations, writes, external calls,
  retries, or failure paths, including bug fixes, and for telemetry changes.
  Skip it for temporary debug output alone, which toby-bug-fix covers.
---

# Toby SWD Observability

Emit enough context for an engineer to identify the operation, affected request or record, outcome, and failure cause. Use the repo's logs, metrics, and traces for that task. Pure computations and local helpers don't need their own outcome logs.

## Use what the repo has

Use the repo's existing logger, metrics client, and tracer in their established format, and ask before adding a library or changing the repo's log formatter.

## Log lines

Write each log line as a stable `noun.verb_past` event name plus named fields. Check the logger's formatter first: when it outputs structured fields (`structlog` or JSON), pass each value as a field (`references/python-logging.md`). When the formatter prints only the message string, append `key=value` pairs and list a structured formatter as a follow-up.

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

For an entry point that mutates state or calls an external service, emit one summary event on success and on failure. Include the operation, safe record ids, outcome, and `duration_ms`. Existing middleware can supply it only when its emitted fields identify the operation and relevant result. An access line with only method, URL, and status doesn't explain a failed business operation. Avoid a duplicate event when the existing event already supplies the required context.

## Other events

- Log each outbound service call with the target, `duration_ms`, and status or error.
- Log consequential decisions needed to explain an outcome, such as a fallback or retry exhaustion. Use bounded reason codes and counts, and avoid a line for every branch or loop iteration.
- Log an unhandled error once with its stack trace at the handler that catches and responds to it (`log.exception`).
- Inside a batch loop, rate-limit or sample item-failure logs under high volume, and log one summary line after the loop with `succeeded_count`, `failed_count`, and `duration_ms`.

## Diagnostic check

When a changed operation needs production diagnostics, run a representative success and failure through the repo's existing test or local harness. Inject an external failure safely. Capture the emitted output through the configured formatter or exporter. Check that it identifies the operation, safe request or record context, outcome, and cause. Check relevant duration and retry fields, and confirm the output excludes secrets and raw payloads. A mock assertion that a logger method was called doesn't prove the fields are emitted.

Keep the command and observed evidence with the task's verification. Reuse the check for the behavior when it can capture the output too. If the formatter, exporter, or runtime isn't available, identify what you inspected and mark emitted diagnostics unverified. Don't claim that adding a logging call proves diagnostics work.

## Redacted data

Never log passwords, tokens, API keys, session cookies, card numbers, raw request or response bodies, or whole ORM/model objects. Log users by `user_id` without email addresses or full names. If code logs a secret, rotate that secret.

## Metrics

Match the metrics that sibling entry points record, ending metric names with their unit (`_seconds`, `_bytes`, `_total`). Record latencies as histograms so dashboards show p95 and p99, and record queue depth and oldest-message age for queues. Keep metric labels to small bounded sets (route templates and status classes, never `user_id` or `order_id`).

## Alerts

State which alert pages on-call when a new public entry point's error rate spikes, or list the missing alert with its metric and threshold as a follow-up. Before renaming a log event or metric, search the repo for alert and dashboard definitions (`*.rules.yml`, `monitors/`, Terraform), and test any event or metric that drives a paging alert.

## Traces

When the repo uses OpenTelemetry or another tracer, propagate the trace context across calls and queues. Add manual spans only around slow internal steps that auto-instrumentation doesn't already wrap.
