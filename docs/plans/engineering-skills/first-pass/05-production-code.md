# Toby's plan for logging and production code

Work mode: durable implementation. New endpoints, jobs, and consumers ship without structured logs, metrics, input bounds, idempotent writes, a shutdown path, or stateless processes.

## Group 5: code that runs in production can be debugged at 3 a.m.

- [x] Create `skills/toby-swd-observability/SKILL.md` as a hidden method skill, with a body under 700 tokens. It covers these topics:
  - using the repo's logger and format
  - one event name and named fields per log line, with the request id on every line
  - what each level means, what to log, and what never to log
  - rate, error, and duration metrics for each entry point, with labels drawn from a small fixed set of values
  - spans when the repo has tracing
  - a test for each log line or metric that an alert depends on
- [x] Create `skills/toby-swd-production/SKILL.md` as a hidden method skill, with a body under 700 tokens. It opens with a table of which checks apply to an HTTP endpoint, a queue consumer, a scheduled job, a CLI, and a library. The table marks each check as required or as applied only when the repo already has the mechanism. Bounds, idempotent writes, auth, and the outcome log are required for a new entry point. Health checks, shutdown, and rate limits apply to a new service, or where the repo already has them. The skill also covers failing closed and what happens when each dependency is down.
- [x] Add a twelve-factor section to `toby-swd-production` with the factors a code change can break and no other skill covers. These are dependencies declared in the manifest, backing services attached through config, no state kept in the process between requests or runs, safety with two instances running, and admin tasks as commands in the repo. Config points to `runtime-config.md`, and logs point to `toby-swd-observability`.
- [x] Point to `toby-swd-errors` for timeouts and retries, and repeat none of its rules.
- [x] In `skills/toby-build/SKILL.md`, open both skills when the change adds an entry point, a background job, a queue consumer, or a call to another service. The design lines list what each skill requires for that code.
- [x] In `skills/toby-build/references/checks.md`, say that a check in the required column of `toby-swd-production`, and the outcome log, are part of the criterion that adds the code. The adjacent-feature entry then does not remove them, and the other checks still need a source.
- [x] In `skills/toby-bug-fix/SKILL.md`, open `toby-swd-observability` when the logs could not show the cause, so the fix adds the log line that would have shown it.
- [x] Add a `build-service` group to `ROUTING_GROUPS` for a build that adds an entry point. Its members are `toby-build`, `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-errors`, `toby-swd-testing`, `toby-swd-e2e`, `toby-swd-campfire`, both new skills, `toby-swd-docs`, `toby-swd-clarity`, and `toby-swd-environment`, about 18,770 tokens. Add a matching scenario in `scripts/token-budget.py`. Add both skills to the README.

### Verification

- Run `python3 evals/run.py gates`. The co-load ceiling fails when `build-service` passes 19,000 tokens. When it does, shorten a skill and leave the ceiling unchanged.
- Trace "add a webhook endpoint that receives Stripe events and marks orders paid" through `toby-build`. The trace passes when the design lines cover a write keyed on the event id, a body size limit, and a log event with the order id and outcome. It fails when any of the three is missing, or when the Don't-build list removes one.
- Trace "add a nightly job that writes a CSV report and uploads it to S3". The trace passes when the design keeps no file between runs and stays safe with two instances running.
- Trace "change the label on the invoice PDF from Total to Amount due". The change adds no entry point, job, or call, so the trace must open neither skill.
- Run `python3 scripts/voice-check.py --review` on every new or changed file, and read each sentence against the READ list.

If a check fails, stop and report it before Group 6.
