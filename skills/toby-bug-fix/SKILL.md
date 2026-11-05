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

1. **Reproduce.** Open `toby-swd-testing` and reproduce the bug with its test-first procedure. When a test harness isn't available, use a bounded command and keep its output. If reproduction fails, follow the investigation step below before attempting a functional repair.
2. **Classify a failing test.** When the report is a test that started failing, classify it into one of the four cases in `toby-swd-testing` before editing the test or the code.
3. **Find the cause.** Trace the failing input to the wrong output using observed evidence and `file:line` citations. State the cause before the first functional edit. A citation locates the code, and the reproduction establishes how it causes the failure. Treat an unproven cause as a guess and gather evidence.
4. **Choose the fix.** Repair the cause where the relevant knowledge and invariants are managed. Open `toby-swd-strategy` and `toby-swd-architecture` to check the affected design, including an existing pattern you reuse. Run "Before the first edit" from `toby-swd-campfire` when nearby structure obstructs the repair. Open the applicable skills listed below. When the repair adds a feature across multiple files, switch to `toby-build` with the reproduction as criterion 1.
5. **Prove it.** Run the reproduction before and after the fix in the form `toby-swd-testing` gives, then run the narrowest tests covering the touched code. When you wrote the test after the fix, revert the fix first to watch the test fail on the expected assertion (`before`), then restore the fix (`after`).
6. **Check the result.** Run "After the tests pass" from `toby-swd-campfire` and compare the diff with the applicable design checks. Repair diagnostic gaps needed to understand a repeat failure, then execute the diagnostic check in `toby-swd-observability`. Inspect emitted events and preserved error causes, including context across a queue or outbound call when relevant. Report any check you couldn't run.

## Investigation

When the failure won't reproduce, state the competing causes and the observation that would distinguish them. Use bounded, reversible instrumentation or fault injection to collect that observation. Keep it inside the affected path, redact sensitive values, and record the command and output. Follow the operating guide's approval rules for external systems and runtime changes.

Remove temporary instrumentation when the investigation ends, or keep it as a tested diagnostic improvement. If the evidence still doesn't establish the cause, report what you tried and stop before a functional repair.

## Design skills

Route by what the repair affects, including existing behavior:

- Open `toby-swd-modules` for responsibilities, hidden knowledge, dependency boundaries, or caller coordination.
- Open `toby-swd-interfaces` for changed signatures, side effects, errors, ordering, or lifetime guarantees.
- Open `toby-swd-errors` for error, retry, timeout, or validation paths, and `toby-swd-extensibility` for changed type or provider branches.
- Open `toby-swd-hardening` and `toby-swd-observability` for entry points, jobs, consumers, writes, outbound calls, and failure paths.
- Open `toby-swd-twelve-factor` for dependencies, config, secrets, process state, startup, shutdown, concurrency, or log destinations.
- Open `toby-swd-clarity` for names, comments, types, or non-obvious control flow, and `toby-swd-docs` when the repair changes documented behavior or constraints.

## Scope

Keep the causal repair, its regression test, the required structural changes, and diagnostics for a repeat failure in scope. A repair may cross functions or files when the cause does. Defer unrelated cleanup with its reason at `file:line`. In shared code, list every caller you checked and the behavior each relies on.

## Red flags

Check the fix against each entry before reporting:

- The fix doesn't have a failing test or quoted command output before it.
- The fix branches on the one literal input from the bug report.
- You weakened a test or assertion so the suite passes.
- A catch block or default value now hides the error.
- You installed a dependency or cleared a cache before finding the cause.

## Final response

Lead with the cause in one sentence at `file:line`. Then say how you fixed it and how you know it worked. If you couldn't check something, say so.
