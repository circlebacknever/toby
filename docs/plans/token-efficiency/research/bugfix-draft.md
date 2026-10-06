# Toby Bug Fix

Fix the cause of the wrong behavior, prove the fix with a run before and after, and keep the diff to the fix. A fix that hides the symptom for one input leaves the cause in place. It also adds a special case that the next change has to work around.

## Steps

1. **Reproduce.** Load `toby-swd-testing` and write the failing test that its bug-fix rule describes, before you touch production code. When no test harness exists, reproduce the failure with one command and quote its output. When you cannot reproduce it, list what you tried and stop before any edit.
2. **Classify a failing test.** When the report is a test that started failing, sort it into one of the four cases in `toby-swd-testing` before you edit the test or the code.
3. **Find the cause.** Follow the path from the failing input to the wrong output, and cite a file and line for each step. Write the cause as one sentence with a file and line before the first edit. A cause you cannot cite is a guess, so call it a guess and keep reading.
4. **Stop when the user asked only why.** Report the cause, the reproduction, and the fix you would make, and edit nothing.
5. **Choose the fix.** Fix the cause where it is. When that fix would patch around a design problem, load `toby-swd-strategy` and follow its rule for that case. When the cause is in an error path, a retry, or a validation step, load `toby-swd-errors`. When the repair needs new behavior in more than one file, say so, and continue under `toby-feature-dev` with the reproduction as its first criterion.
6. **Prove it.** Run the reproduction before and after the fix, in the form that `toby-swd-testing` gives. Then run the narrowest tests that cover the touched code.

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
