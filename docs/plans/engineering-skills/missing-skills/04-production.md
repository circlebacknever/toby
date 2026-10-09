# Group 4: production code gets hardening, twelve-factor, logging, and flag rules that hold up

This group meets criterion 5 in the overview. Its owner edits `skills/toby-swd-production/**`, which becomes `skills/toby-swd-hardening/**`, plus `skills/toby-swd-twelve-factor/**`, `skills/toby-swd-observability/**`, `skills/toby-swd-flags/**`, `skills/toby-swd-e2e/**`, `skills/toby-swd-errors/**`, `skills/toby-optimize/**`, and `skills/toby-swd-interfaces/references/runtime-config.md`.

## Steps

- [x] Rename `skills/toby-swd-production` to `skills/toby-swd-hardening`. Update the `name:` line, the title, and `agents/openai.yaml`.
- [x] Move shutdown, health checks, two-instance safety, and state kept in the process from hardening to the new twelve-factor skill. Hardening's table points there.
- [x] Add to `toby-swd-hardening`:
  - a row for a call to another service, with a timeout, a plan for when the service is down, and a retry only when the call is safe to repeat, pointing to `toby-swd-errors` for the timeout value
  - poison messages for a queue consumer in `references/messages.md`, using the broker's dead-letter queue with an alert and a replay command. A consumer that depends on message order gets no dead-letter redrive, and holds that record's later messages or stops and alerts.
  - a dual write in `references/messages.md`, where one request writes the database and also sends a message or calls a service, with the outbox or a stored status a retry can resume
  - `references/deploys.md`: the old release reads what the new one writes, and the new release reads what the old one wrote, including queued messages and cached entries. A column rename ships in four releases that each keep the previous release working. The four releases apply when a deploy runs two releases at once, or when a rollback skips the down migration.
  - an attempt limit per account and per IP on each endpoint that checks a password, a one-time code, or a reset token, even in a repo with no rate limiter
- [x] Require idempotent writes for a webhook, a consumer, a job, a money movement, or an endpoint whose client retries on its own. For any other endpoint, require them only where the repo already uses idempotency keys.
- [x] Count a framework or proxy body limit as the bound on body size, so the skill asks for a new limit only on list length, page size, and uploads the framework does not cap.
- [x] Create `skills/toby-swd-twelve-factor/SKILL.md`, a hidden method skill of about 650 words, with `agents/openai.yaml`. Give each factor a diff can break one line on how it breaks and one check. Say that the codebase factor is out of reach for one diff. Include:
  - a service logging to stdout while a CLI logs to stderr
  - migrations run as a release step
  - a scheduler or timer loop inside a web process
  - the same kind of database in development and production
  - the port read from config
  - secrets kept out of client bundles such as `VITE_*`
  - readiness that reports this instance started and is not shutting down, and does not fail on a dependency every instance shares
- [x] Move `skills/toby-swd-interfaces/references/runtime-config.md` to `skills/toby-swd-twelve-factor/references/config.md`. Fix its Stripe example so a missing key stops boot when the gateway is Stripe, and add the client-bundle warning.
- [x] Fix `skills/toby-swd-observability/SKILL.md`:
  - Read the logger's formatter first. When it prints extra fields, as a JSON formatter does, pass fields that way. Otherwise write `key=value` pairs after the event name, and list a structured formatter as a follow-up.
  - Inside a loop, log only a failed item with its id. After the loop, log the counts and the duration.
  - Log an error with its stack trace at the handler, record durations as histograms, and add a span only where auto-instrumentation does not already make one.
  - For a new entry point, state which alert fires on its errors, or list the missing alert as a follow-up. Before renaming an event, search for alert and dashboard definitions.
  - Define the outcome log here, as the one home for it.
- [x] Fix `skills/toby-swd-flags/SKILL.md`:
  - Delete the Permission row that the next sentence contradicts.
  - Evaluate a flag that targets users, or that must flip without a restart, once per request at the entry point.
  - A test that fails with the flag on must assert a behavior the flag is meant to change. Keep the flag-off test unchanged and add a flag-on copy.
  - For data, put only the switch of reads behind the flag, and keep writing the old column until the flag is gone. Point to `toby-swd-hardening`'s `references/deploys.md` for the releases.
  - Add a rollout list with the metric to watch and the value that means turn it off. Give the removal an owner, a date, and an order: code first, flag service last.
- [x] Fix `skills/toby-swd-e2e/SKILL.md`. Add harness names for Python, Go, Ruby, and mobile. Add rows for a library function, a mobile screen, and an inbound webhook. Say how a queue test runs the broker and the consumer.
- [x] In `skills/toby-swd-errors/SKILL.md`, point "log the detail" at `toby-swd-observability`, and move the sentence about shared mutable state into the Brownfield or red-flag text where an opener reaches it. In `skills/toby-optimize/SKILL.md`, open `toby-swd-hardening` and `toby-swd-observability` when the change adds a cache, a queue, a worker pool, or parallel calls, and delete the sentences that repeat the five steps.
- [x] Update every pointer to the old name and the old path in the owned files.

## Fixes from the second audit

- [x] Store a caller's id in the same transaction as the write it guards. A scheduled job marks the record with a conditional write before it sends.
- [x] Limit retries in `toby-swd-errors` and its references to calls that are safe to repeat, and retry a connection reset only before COMMIT.
- [x] Rewrite rule 3 of `references/config.md` to match `toby-swd-architecture`. Code imports the typed config and the clients built at startup, and takes a client as an argument only when a test cannot patch the import.
- [x] Run a queue consumer as its own process type. After `SIGTERM`, fail readiness and keep serving for a few seconds.
- [x] Make a flag fall back to its last fetched value, and run the existing tests at the value that runs today's code.
- [x] Use the framework's in-process test client for an end-to-end test when one exists, against a database made for the run.

- [x] Tie each production rule to a condition the change meets, so a one-instance app gets no request-id middleware, metrics client, health check, overlap claim, retry wrapper, or config module it does not need. Request ids, metrics, and config modules follow what the repo already has. A webhook that moves a status uses a conditional write, and an event-id table only guards an insert, an increment, or a send.

## Removed on purpose

- The idempotency requirement on every HTTP endpoint, because a form post that nobody retries does not need an idempotency key.
- Readiness that fails on any dependency, because a shared database outage would take every instance out of the load balancer at once.
- The word "timing" in the list of behavior `toby-optimize` preserves in brownfield work, because an optimization changes timing on purpose.
- The option number in the code comment of `toby-swd-twelve-factor`'s `references/config.md`, because `toby-swd-extensibility` can renumber its options. The comment reads correctly without the number.
- The red flag "A remote call with no timeout." in `toby-swd-errors`, because the Outbound calls section of `toby-swd-hardening` states that rule.
- The words "circuit breaker" in the red flag of `toby-optimize`, because `toby-swd-errors`' `references/backend-apis.md` has the circuit breaker rule.
- The sentence in `references/config.md` that gave every module its clients as constructor arguments, because a Django app reads `settings` and builds clients at module scope.
- Steps 1, 2, and 4 of the data list in `toby-swd-flags`, because `toby-swd-hardening`'s `references/deploys.md` holds the release sequence.
- The sentence that a deploy stops a scheduler inside the web process, because a deploy restarts a separate scheduler process too.
- The rule that a hit ratio below 50 percent rarely saves time, because a 30 percent hit ratio on a 400 ms query saves about 118 ms a request.
- The hardening sentence about an unbounded `limit` parameter, to fit the body budget. The rule to limit page size stays.

## Verification

- Give an Opus subagent the five owned skills and ask it to quote advice that would cause an outage, data loss, a leak, or code a single-instance app with one developer does not need. A quote that holds up fails this group.
- Give a second subagent the request "add a worker that reads `invoice.created` messages and emails a PDF" and the owned skills. It fails this group when it cannot quote sentences that require a dead-letter path, a check that sending twice emails once, and a log of the invoice id.
- Run `grep -rn "toby-swd-production\|runtime-config.md" skills base README.md scripts evals --exclude-dir=gold`. A hit that points at the old name or path fails this group.
- Run `python3 scripts/validate-skills.py`. An error in an owned file fails this group.
