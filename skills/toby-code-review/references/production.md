# Production readiness

Ask these questions of a new entry point, job, consumer, outbound call, migration, write, or check before a write. Ask them too of a change to a stored or queued format. The steps make the failure happen.

- When a webhook, consumer, or job runs again after a retry, does it insert a second row, send a second message, or charge a card twice?
- Can two requests sent at once both pass a check and both succeed, such as two agents claiming one ticket?
- Can a caller send a value, such as `limit=1000000`, that makes one request read every row or use unbounded memory?
- Does an outbound call have no timeout?
- Can a crash between a database write and a message or call leave the work half done?
- Can the previous release, still running during a deploy, read what this release writes, or run against the migrated schema?
- Does a migration lock a large table?
- Does another instance need data that this process keeps in memory or on local disk? A cache the process can rebuild from the database is fine.
- Does a new login, password reset, or one-time-code endpoint accept unlimited failed attempts? The steps post 1,000 wrong codes or passwords.
- Does a new entry point that changes state log nothing, where similar entry points log the record id and the result?
- Does a log line write a secret or personal data beyond a user id, such as a token or an email address?

When the fix is unclear, open `../toby-swd-hardening/SKILL.md`.
