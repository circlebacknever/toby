# Failing and flaky tests

This file has the steps for a test that fails, and for a test that fails only some of the time. Open it before you edit, skip, or delete a failing test.

## Classify the failure

Classify a failing test before changing it:

1. **The behavior is still valid, and production broke it.** Fix the production code.
2. **The behavior changed on purpose.** Update the test to describe the new behavior.
3. **The behavior is obsolete.** Remove the test and say why in the commit message.
4. **The test is bad**, because it is coupled to internals, asserts incidental data, or checks something its name does not claim. Rewrite it to protect the same behavior through a better interface.

Read a test you cannot classify until you understand it. When you delete or weaken a test, report its name, the behavior it protected, why it is obsolete, and what replaces it.

When a test was deleted to make the suite pass before anyone classified it, restore the test and classify it.

## Flaky tests

A flaky test passes and fails on the same code. Rerunning it until it passes hides the cause. Look for the cause in async waits first, then concurrency, then test order. Replace a fixed sleep with a wait on the event, or a poll with a timeout, and check the code under test for a race.
