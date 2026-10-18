# Failing and flaky tests

Open this file before you edit, skip, or delete a failing or intermittent test.

## Classify the failure

Classify a failing test into one of these four cases before changing it:

1. **The behavior is still valid, and production broke it.** Fix the production code.
2. **The behavior changed on purpose.** Update the test to describe the new behavior.
3. **The behavior is obsolete.** Remove the test and state why in the commit message.
4. **The test checks internal details or unrelated fields.** Rewrite the test to check the public behavior through the module's interface.

Read any test you can't classify until you understand what it checks. When you delete or weaken a test, report its name, the behavior it checked, why it is obsolete, and what replaces it. If someone deleted a failing test without classifying it, restore it and classify it first.

## Flaky tests

A flaky test passes and fails on the same code, and rerunning it hides the cause. Check async waits first, then concurrency, then test-order dependencies. Replace fixed sleeps with a wait on an observable event or condition, and check the production code for a race.
