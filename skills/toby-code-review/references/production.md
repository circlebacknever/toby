# Production readiness

Ask these questions when a diff adds or changes an entry point, job, consumer, outbound call, migration, write, check-before-write, or stored/queued format. Write reproduction steps that trigger the failure.

- Does a retry or redelivery of a webhook, consumer, job, or payment insert a duplicate row, send a second message, or charge twice?
- Can two concurrent requests or job runs pass a read check and both write (such as two agents claiming one ticket, or a read-modify-write without a conditional `WHERE` or row lock)?
- Does code hold a database transaction or row lock open across an outbound HTTP, RPC, or queue call?
- Can a caller pass an unbounded input or page size (`limit=1000000`), or does a scheduled job load an unbounded table into memory?
- Does an outbound call lack a timeout, or use a user-supplied URL without blocking loopback, private-network, link-local, and cloud-metadata IPs?
- Does an inbound webhook skip constant-time cryptographic signature verification on the raw body?
- Can a crash between a database write and an external call or message leave the state inconsistent without an outbox or recovery job?
- Can the previous release, running alongside this one during a deploy or rollback, fail to read what this release writes or fail against the migrated schema?
- Does a migration lock an existing table without `CONCURRENTLY`, batched backfills, or a `lock_timeout`?
- Does the code store cross-request state in process memory or container-local disk, or cache tenant data without the tenant id in the cache key?
- Does a login, password-reset, one-time-code, or unauthenticated email/SMS endpoint allow unlimited attempts per account or IP?
- Does a state-changing entry point omit the outcome log that sibling entry points write, or log a secret, token, raw body, or personal data beyond `user_id`?

When the fix is unclear, open `../toby-swd-hardening/SKILL.md`.
