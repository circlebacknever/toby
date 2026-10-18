# Messages

This file covers poison messages, overlapping consumer or job runs, and dual writes across a database and an external system.

## Poison messages

A message that fails on every delivery (such as a malformed payload) loops forever unless the broker caps delivery attempts. Configure the broker's dead-letter policy (SQS redrive, Sidekiq dead set, or RabbitMQ `x-delivery-limit`), and test that the consumer processes later messages after a poison message. In Kafka, publish the failed message to a dead-letter topic after the final attempt and commit the offset when the consumer doesn't require strict ordering.

Alert when a dead-letter queue receives a message (or list the missing alert as a follow-up), and log the message id on the final attempt.

When a consumer requires strict per-record ordering (such as an SQS FIFO group or Kafka partition where `order.refunded` must follow `order.paid`), don't redrive out of order. Block later messages for that record, set queue retention to its maximum, and alert when a message's receive count passes the retry limit or partition lag stalls.

## Overlapping runs

When two runs of a scheduled job or two message deliveries can overlap, claim each row with an expiring conditional update before calling an external service:

```sql
UPDATE tickets
SET alert_sending_at = now()
WHERE id = $1
  AND alerted_at IS NULL
  AND (alert_sending_at IS NULL OR alert_sending_at < now() - interval '15 minutes')
```

Send the external request only when the query updates one row, and set `alerted_at = now()` afterward.

## Dual writes

Never send a message or call an external service inside an uncommitted database transaction. When losing the second step on a crash is acceptable (such as a non-critical notification), trigger it in an after-commit hook (`transaction.on_commit` in Django, `after_commit` in Rails) and state that tradeoff in the design.

When the external action must succeed for every committed write (such as a payment or fulfillment event), write an outbox row in the same database transaction. Alternatively, save a pending status (`refund_pending`) that a background worker retries until it finishes.
