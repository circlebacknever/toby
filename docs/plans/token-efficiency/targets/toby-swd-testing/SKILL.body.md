# Toby SWD Testing

Tests record the behavior callers rely on, checked through the public interface. A refactor, a new feature, or a bug fix leaves existing tests unchanged. Only a change to required behavior edits an existing test, so a test that needs an edit during a refactor checks internals. Assert call order only when that order is the observable contract.

When a behavior is hard to test, the abstraction is too coarse. Extract a smaller module with a real interface and test through it. Do not expose internals only so a test can reach them.

## Names

Name each test for the behavior it specifies, such as `expired token is rejected`, and never for a call, such as `calls paymentService.process`. When you cannot name the behavior, the boundary is wrong or the test mixes two behaviors.

## Assertions

An assertion fails when the behavior under test changes, and never on a timestamp, key order, formatting, or a new optional field.

- Assert the specific value or field that proves the behavior happened.
- Assert an inexact output within a stated, justified tolerance.
- Use object subset matching when only a few fields matter.
- Use full-object equality or a snapshot only when the whole structure is the contract, such as a config file, a response schema, or a serialization format.

Read the diff before accepting a snapshot update, and confirm every change is intended, because accepting an unread update deletes the test.

## Coverage

Cover the success path, each documented failure mode, and the boundary conditions, then stop. Keep one behavior per test, with as many asserts as that behavior needs. Default to named examples. Add a property test when the contract is a round trip, agreement with a simpler reference version, or an invariant.

## Independence

Each test shares no mutable state with other tests and passes in any order. Control time and IO, seed randomness, and assert results so the test checks itself. When a result depends on a library or platform version, record the version. When the system must give the same output across runs or machines, test that determinism as part of the contract.

## Test-first

Write the test first in two cases:

1. **A bug fix with defined durable behavior.** Reproduce the bug in a failing test before touching production code. Read the failure and confirm it shows the bug's wrong result. A failure from an import error, a missing fixture, or a typo proves only that the test is broken.
2. **New behavior with a settled contract.** After the design pass settles the interface, write the test that defines the contract, then implement to it.

Skip test-first while the design is open, and do the design pass first with `toby-swd-strategy` and `toby-swd-modules`. Also skip it when no harness exists, the change is docs or formatting, or the check needs unsafe external state. Say which case applied and how you verified.

## Test doubles

Use the highest-fidelity dependency that is fast and deterministic:

1. **Real implementation** when it is fast and in-process, such as domain objects, an in-memory database, or a validator.
2. **Fake**, a hand-written stand-in with realistic behavior, when the real thing is slow, external, or hard to set up.
3. **Mock** only a dependency whose calls another system sees, such as a third-party API, payment, email, or a message bus. Mock or fake time, randomness, and failures that are hard to trigger. Put each mock on an adapter class you own, which wraps the third-party client. Test against the application's own database with the real implementation or a fake.

Across a process, sandbox, or hardware boundary, fake the channel or simulate the environment, and test each side against the contract. Assert a state such as "the order is paid", and do not assert a call log such as "process called once with amount=42".

## Failing tests

Classify a failing test before changing it:

1. **The behavior is still valid, and production broke it.** Fix the production code.
2. **The behavior changed on purpose.** Update the test to describe the new behavior.
3. **The behavior is obsolete.** Remove the test and say why in the commit message.
4. **The test is bad**, because it is coupled to internals, asserts incidental data, or checks something its name does not claim. Rewrite it to protect the same behavior through a better interface.

Read a test you cannot classify until you understand it. When you delete or weaken a test, report its name, the behavior it protected, why it is obsolete, and what replaces it.

## Existing tests

Read the tests that cover the touched behavior before adding new ones. When coverage is thin, report the untested behavior as a risk, and state the characterization test that would cover it. When the user declines automated tests, record the verification they chose.

## Red flags

Before calling coverage done, check for each of these:

- A test fails on a correct refactor or is named for a call.
- A large snapshot was updated without review.
- An expected value was copied from the code's output, so the test passes with the bug in place. Work it out from the spec or by hand.
- A flaky test was rerun until it passed. Look for the cause in async waits first, then concurrency, then test order. Replace a fixed sleep with a wait on the event, or a poll with a timeout, and check the code under test for a race.
- A test exists only to hit a line.
- A test was deleted to make the suite pass before it was classified.
- A bug fix has no regression test.
