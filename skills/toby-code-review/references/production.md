# Production readiness

Trace the changed path through its callers, dependencies, and failure handlers. Use the questions that apply to its guarantees. For each finding, identify the trigger and check whether an existing guard prevents it.

- Does a retry or redelivery of a webhook, consumer, job, or payment insert a duplicate row, send a second message, or charge twice?
- Can two concurrent requests or job runs both pass a read check and write the same row without a conditional `WHERE` or row lock?
- Does code hold a database transaction or row lock open across an outbound HTTP, RPC, or queue call?
- Can a caller pass an unbounded input or page size (`limit=1000000`), or does a scheduled job load an unbounded table into memory?
- Does an outbound call lack a timeout, or use a user-supplied URL without blocking loopback, private-network, link-local, and cloud-metadata IPs?
- Does an inbound webhook skip constant-time cryptographic signature verification on the raw body?
- Can a crash between a database write and an external call or message leave the state inconsistent without an outbox or recovery job?
- During a rolling deploy or rollback, can the previous release fail to read what this release writes or fail against the migrated schema?
- Does a migration lock an existing table without `CONCURRENTLY`, batched backfills, or a `lock_timeout`?
- Does the code store cross-request state in process memory or container-local disk, or cache tenant data without the tenant id in the cache key?
- Does a login, password-reset, one-time-code, or unauthenticated email/SMS endpoint allow unlimited attempts per account or IP?
- Does a changed failure path omit the operation, request or record id, outcome, or underlying cause needed to diagnose it? Run the failure and inspect the rendered log. Fields passed to a logger can disappear when the formatter prints only the message.
- Does a state-changing entry point omit an outcome log, or log a secret, token, raw body, or personal data beyond `user_id`? Existing middleware suffices only when it records the needed outcome and context.
- Can required configuration be missing or invalid at startup, leaving an accepted request to fail later? Check the actual config loader and client construction before reporting it.
- Does a changed producer emit a format that an existing consumer or stored record reader can't handle? Follow both sides of the contract through a normal call and a failure.
- Is a promised route, job, consumer, or screen reachable through its registered entry point? A unit test that imports its handler doesn't prove registration.
- Can reverting a bug fix or removing a required handler step leave its regression test passing? Inspect what the test asserts and which entry point it drives.

When the fix is unclear, open `../toby-swd-hardening/SKILL.md`.
