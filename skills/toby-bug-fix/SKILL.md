---
name: toby-bug-fix
description: >-
  Fixes behavior that is wrong today. It reproduces the failure, finds the cause
  at a file and line, fixes that cause, and proves the fix with a run before and
  after. Use it when the user reports a bug, a crash, an error message, a
  regression, or wrong output and wants it fixed. Use it when the user pastes a
  stack trace, or says a build or a test started failing. Skip it for a question
  about why something fails with no fix asked for, which toby-explain covers.
  Skip it for a flaky test, which toby-swd-testing covers, and for slow code,
  which toby-optimize covers.
---

# Toby Bug Fix

Fix the cause of the wrong behavior, prove the fix with a run before and after, and keep the diff to the fix.

## Steps

To open a skill by path, read `../<skill>/SKILL.md` relative to this skill's folder. State `Mode: durable implementation` (or `investigation` while reproducing). Open `toby-swd-environment` before any command beyond a narrow test, and open `toby-swd-plan` when the user asks for a plan.

1. **Reproduce.** Open `toby-swd-testing` and write the failing test its bug-fix rule describes. When the repo doesn't have a test harness, reproduce the failure with one command and quote its output. When you can't reproduce it, list what you tried and stop before any edit.
2. **Classify a failing test.** When the report is a test that started failing, classify it into one of the four cases in `toby-swd-testing` before editing the test or the code.
3. **Find the cause.** Trace the path from the failing input to the wrong output, citing `file:line` at each step, and state the cause in one sentence with its `file:line` before the first edit. Call an uncited cause a guess and keep reading.
4. **Choose the fix.** Fix the cause where it happens. When duplicated logic or a tangled condition obscures the cause, run "Before the first edit" from `toby-swd-campfire` with existing passing tests first. Open `toby-swd-architecture` when the fix moves a rule, `toby-swd-strategy` when the fix would work around a design flaw, and `toby-swd-errors` when the cause is in an error, retry, or validation path. When the repair requires new behavior across multiple files, say so and switch to `toby-build` with the reproduction as criterion 1.
5. **Prove it.** Run the reproduction before and after the fix in the form `toby-swd-testing` gives, then run the narrowest tests covering the touched code. When the test was written after the fix, revert the fix first to watch the test fail on the expected assertion (`before`), then restore the fix (`after`).
6. **Check the design.** Run "After the tests pass" from `toby-swd-campfire` on the fix, and list flaws outside the fixed function as follow-ups at `file:line`. When finding the cause required state that the logs omitted, add a log field for that state as `toby-swd-observability` describes.

## Scope

Keep the diff to the cause, its test, any `toby-swd-campfire` fix inside the fixed function, and any log field from step 6. In shared code, list every caller you checked and the behavior each relies on.

## Red flags

Check the fix against each entry before reporting:

- The fix doesn't have a failing test or quoted command output before it.
- The fix branches on the one literal input from the bug report.
- A test or assertion was weakened so the suite passes.
- A catch block or default value now hides the error.
- A dependency was installed or a cache cleared before finding the cause.

## Final response

Lead with the cause in one sentence at `file:line`. Then list the fix, the `before` and `after` runs, and what stays unverified.
