# Messages

This file covers poison messages, overlapping runs, and a request that writes the database and also sends a message or calls a service.

## Poison messages

A message that fails every time, such as one with a missing field, comes back on every redelivery. Cap the deliveries with the broker's dead-letter setting, such as an SQS redrive policy or Sidekiq's dead set. In RabbitMQ, use a quorum queue with `x-delivery-limit` and a dead-letter exchange. Test that the next message still runs after a poison message.

Kafka has no dead-letter setting. A Kafka consumer that does not depend on order publishes the message to a dead-letter topic after its last attempt, then commits the offset. Spring Kafka's `DeadLetterPublishingRecoverer` and Karafka's dead letter queue do this.

When the repo has alerting, such as alert rules or an alerting service, alert when the dead-letter queue holds a message. Otherwise list that alert as a follow-up, with its queue and threshold. Cite the broker's redrive, such as SQS `start-message-move-task`, and write a replay command only when the broker has none. The broker deletes old dead messages, such as after at most 14 days in SQS, so a message nobody watches is lost. Under an SQS redrive policy the broker moves the message, so log the message id on the consumer's last attempt. The message's receive count shows which attempt is the last.

Some consumers depend on message order for one record, as in a Kafka partition or an SQS FIFO group. There, a skipped `order.paid` lets `order.refunded` apply to an order that was never paid. For these consumers, set no dead-letter redrive, and hold that record's later messages until someone fixes the failed one. In Kafka, holding the failed message also holds every later record in its partition. Set the queue's retention to its maximum. Fix the failed message before retention ends, because the broker then deletes it and the record's later messages.

For these consumers, when the repo has alerting, alert when a message's receive count passes the retry limit. Kafka keeps no receive count, so alert on a Kafka partition whose committed offset stops increasing while its lag is above zero. When the repo has no alerting, list that alert as a follow-up, with its queue and threshold.

## Overlapping runs

When two runs of a scheduled job, or two deliveries of one message, can overlap, claim each row with a conditional write before the send. The claim expires, so a later run retries after a crash, as in `UPDATE tickets SET alert_sending_at = now() WHERE id = %s AND alerted_at IS NULL AND (alert_sending_at IS NULL OR alert_sending_at < now() - interval '15 minutes')`. Send only when one row changed, and set `alerted_at` after the send.

## Dual writes

A request can write the database and also send a message or call another service. Run that second step after the commit, such as in Django's `transaction.on_commit` or Rails' `after_commit`, so it never runs after a rollback. After a crash between the two steps, one step is done and the other is lost. When losing the second step is acceptable, such as a notification email, say so in the design.

When the other system must see every write, such as a payment, use the repo's outbox or a stored status. An outbox row goes in the same transaction as the change. A worker sends the row after the commit. A stored status is a column value such as `refund_pending`. A retry job finds each row with that status and finishes the work.
