# Toby's plan for the end-to-end test skill

Work mode: durable implementation. Builds ship with unit tests and no test that drives the feature through the entry point a user reaches.

## Group 2: each slice gets one test through its entry point

- [x] Create `skills/toby-swd-e2e/SKILL.md` as a hidden method skill, with `disable-model-invocation: true` and `allow_implicit_invocation: false` in `agents/openai.yaml`.
- [x] Write the body. It covers these topics:
  - finding the repo's end-to-end harness before writing one
  - driving the entry point the way a caller does, through an HTTP request, a CLI run, a browser session, or a queued message
  - keeping every dependency inside the system real, and faking only third parties at the network edge
  - test data that each test creates for itself
  - one test per slice, plus each failure a criterion names
  - one test that walks through every slice of the feature, added with the last slice
  - what to do when the test cannot run here
- [x] Point to `toby-swd-environment` for starting a server or a container, and to `toby-swd-testing` for the before-and-after runs. Repeat neither rule.
- [x] In `skills/toby-build/SKILL.md`, open `toby-swd-e2e` when writing the Check line for a strategic slice, and when a tactical change alters what an entry point returns and no existing test drives that entry point.
- [x] In `skills/toby-swd-testing/SKILL.md`, add one sentence that opens `toby-swd-e2e` for a test through the entry point.
- [x] Add `toby-swd-e2e` to `build-strategic` in `ROUTING_GROUPS`, add it to the strategic scenario in `scripts/token-budget.py`, and add it to the README's skill list.

### Verification

- Run `python3 evals/run.py gates`. The validator fails if no entry skill opens `toby-swd-e2e`, and the co-load ceiling fails above 19,000.
- Trace "add an endpoint that cancels an order and emails the customer" through `toby-build`. The trace passes when the slice's Check line is a request against the running app, with the email provider faked at the network edge. It fails when the Check line names only a unit test.
- Trace "change the rounding in `invoice_total` from half-up to half-even", where `tests/test_invoice.py` already calls the CLI that prints totals. The trace must not open `toby-swd-e2e`, because a test already drives that entry point.
- Run `python3 scripts/voice-check.py --review` on every new or changed file, and read each sentence against the READ list.

If a check fails, stop and report it before Group 3.
