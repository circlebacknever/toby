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

Fix the cause of the wrong behavior, prove the fix with a run before and after, and keep the diff to the fix. A fix that hides the symptom for one input leaves the cause in place. It also adds a special case that the next change has to work around.

## Steps

A skill opened by path is the SKILL.md at `../<skill>/SKILL.md` from this skill's folder. Before any command beyond a narrow test, open `toby-swd-environment` by path.

1. **Reproduce.** Open `toby-swd-testing` by path and write the failing test that its bug-fix rule describes, before you touch production code. When no test harness exists, reproduce the failure with one command and quote its output. When you cannot reproduce it, list what you tried and stop before any edit.
2. **Classify a failing test.** When the report is a test that started failing, sort it into one of the four cases in `toby-swd-testing` before you edit the test or the code.
3. **Find the cause.** Follow the path from the failing input to the wrong output, and cite a file and line for each step. Write the cause as one sentence with a file and line before the first edit. A cause you cannot cite is a guess, so call it a guess and keep reading.
4. **Choose the fix.** Fix the cause where it is. When that fix would patch around a design problem, open `toby-swd-strategy` by path and follow its rule for that case. When the cause is in an error path, a retry, or a validation step, open `toby-swd-errors` by path. When the repair needs new behavior in more than one file, say so, and continue under `toby-build` with the reproduction as its first criterion.
5. **Prove it.** Run the reproduction before and after the fix, in the form that `toby-swd-testing` gives. Then run the narrowest tests that cover the touched code.

## Scope

Keep the diff to the cause and its test. Report every other defect you saw as a follow-up, one line each with a file and line. A fix in shared code changes every caller, so list the callers you checked and what each one relies on.

## Red flags

Check the fix against each entry before the report.

- The fix has no failing test or quoted command before it.
- The fix adds a branch for the one input in the report.
- A test or an assertion changed so that the suite passes.
- A catch block or a default value now hides the error.
- A dependency got installed or a cache got cleared to make the error stop, before any cause was found.

## Final response

Lead with the cause in one sentence, with its file and line. Then give the fix, the runs before and after, and what stays unverified.
