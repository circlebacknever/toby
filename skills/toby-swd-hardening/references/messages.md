# Messages

This file covers poison messages, overlapping consumer or job runs, and dual writes across a database and an external system.

## Poison messages

A message that fails on every delivery (such as a malformed payload) loops forever unless capped. Configure the broker's dead-letter policy (an SQS redrive policy, Sidekiq's dead set, or a RabbitMQ quorum queue with `x-delivery-limit`), and test that the consumer processes subsequent messages after a poison message. In Kafka, publish the failed message to a dead-letter topic after the final attempt and commit the offset when message ordering isn't required.

Alert when a dead-letter queue receives a message (or list the missing alert as a follow-up with its queue and threshold), and log the message id on the final attempt before redrive.

When a consumer requires strict per-record ordering (such as a Kafka partition or SQS FIFO message group where `order.refunded` must not run before `order.paid`), don't redrive out of order: block later messages for that record, set queue retention to its maximum, and alert when a message's receive count exceeds the retry threshold or when partition lag grows while the committed offset stalls.

## Overlapping runs

When two runs of a scheduled job or two message deliveries can overlap (such as when execution exceeds the SQS visibility timeout or cron runs on multiple hosts), claim each row with an expiring conditional update before performing an external action:

```sql
UPDATE tickets
SET alert_sending_at = now()
WHERE id = $1
  AND alerted_at IS NULL
  AND (alert_sending_at IS NULL OR alert_sending_at < now() - interval '15 minutes')
```

Perform the external send only when one row updated, and set `alerted_at = now()` afterward.

## Dual writes

Never send a message or call an external service inside an uncommitted database transaction. When losing the second step on a crash is acceptable (such as a non-critical notification), trigger it in an after-commit hook (`transaction.on_commit` in Django, `after_commit` in Rails) and state that tradeoff in the design.

When the external action must succeed for every committed write (such as a payment or fulfillment event), write an outbox row in the same database transaction or store a pending status (`refund_pending`) that a background worker retries to completion.
