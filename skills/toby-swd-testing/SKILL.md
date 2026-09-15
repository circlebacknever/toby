---
name: toby-swd-testing
description: >-
  Keep tests an executable specification of behavior. Use it when writing,
  changing, deleting, weakening, or snapshotting a test, and whenever a
  behavior change in production code needs a matching test. It covers
  regression tests for a fix and refusing to make a failing test green by
  tweaking the assertion. Skip it when the change leaves behavior unchanged: a
  rename, a formatting pass, a comment edit. Skip it for a throwaway spike,
  which `toby-swd-experiment` covers.
---

# Toby SWD Testing

A test suite records what the system does, so callers can rely on it. It also catches regressions when something changes. It makes refactoring safe enough that the team will do it. A suite that tests implementation details is worse than no suite. It slows every change, overstates coverage, and teaches the team to ignore failures.

**Describe behavior at the public interface.** A test puts inputs in, checks the outputs, and checks side effects where callers would notice them. Internal call order, private method signatures, the order helpers fire, and intermediate data types are invisible from outside the module. Keep them out of the test. Write tests that still pass after a correct refactor. A test that fails because you renamed a helper while preserving behavior is detecting only the diff.

## Name tests by behavior

Write the test name as the spec, so a reader who sees only the name knows what the system does in that scenario.

Use:
- `checkout confirms a paid order`
- `withdrawal reduces the account balance`
- `expired token is rejected`

Avoid:
- `calls paymentService.process`
- `sets internalOpenIndex to 1`
- `returns object with status field`

If you can't name the behavior, you don't know what you're testing. A test you can't name shows a design problem. Usually the abstraction boundary you're testing through is wrong, or the behavior under test is mixed with something else.

## Test through public interfaces

Test at the boundary, because those tests still pass after refactors, while tests of internals break when the internals change.

Don't import private modules to test them. Don't assert on private state. Don't verify that helper X was called before helper Y unless that call sequence is the observable contract, which is rare. Mock external dependencies at the system boundary. Internal collaborators stay real, because mocking them couples the test to current structure.

When a behavior is hard to test through the public interface, the abstraction is usually too coarse. The fix is to extract a smaller module with a real interface, then test through it. Do not test internals directly to "make it testable". toby-swd-modules is for preventing that failure.

## Narrow assertions

An assertion should fail when the behavior under test changes. It should not fail when something incidental changes: a timestamp, a key order, a formatting tweak, a new optional field in a response.

Useful patterns:
- Assert on the specific value or field that proves the behavior happened.
- When the output is inexact by nature, assert it falls within a stated, justified tolerance of the expected value. Exact-equality assertions on such outputs fail at random or pass when they should fail.
- Use object subset matching when only a few fields matter.
- Reserve full-object equality and snapshot matching for cases where the entire structure is the contract, such as config files, public response schemas, and serialization formats.

An unread snapshot blob protects no behavior. It only adds noise to CI and to version control.

Before accepting a snapshot update, read the diff and confirm every change is intended. An unread snapshot update is the same as deleting the test.

## How much to test

Cover the contract's distinct observable outcomes, then stop: the success path, each documented failure mode, and the boundary conditions. Keep one behavioral concept per test. Multiple asserts are fine when they prove that one behavior. A behavioral outcome can be checked by example (one named scenario) or by property (an invariant that holds over a range of generated inputs). Prefer whichever states the contract more directly.

## Each test is independent

Write each test so it shares no mutable state with other tests, depends on no test order, and is deterministic and self-validating. A deterministic test controls time and IO, and it sets randomness from a recorded seed so the run can be repeated. Self-validating means the test checks its result with assertions, so a human does not have to read printed output. A test whose result depends on what ran before it is already broken. When the system itself must reproduce the same outputs across runs or machines, that determinism is part of the contract under test. When a result depends on a library or platform version, record it so a later mismatch is visible.

## Test-first, with judgment

When the behavior is well-defined, write the test before the implementation. The two cases below qualify for test-first.

1. **Bug fixes with defined durable behavior.** Reproduce the bug in a failing test before touching production code. The failing test proves it catches the bug, then proves the fix works, and then remains as a regression guard. A bug fix without a regression test is incomplete work, because the bug can return without notice.
2. **New behavior with a settled contract.** Once the design pass identifies the abstraction and its interface, write the test first to define the contract, then implement to satisfy it.

Skip test-first when the design is still being worked out. If you write each next bit of implementation only to pass a failing test, TDD replaces design. The result is code that covers the feature and has no real abstraction. Do the design pass first (see toby-swd-strategy and toby-swd-modules), then write tests against the interface you settled on.

Also skip test-first when no relevant harness exists or the change is documentation-only. Skip it too when the edit is formatting or metadata, or when the only useful verification needs unsafe external state. Say which case applies and how you verified instead.

### Experiment loops

Defer test writing and test runs while the behavior is still being discovered. That rule covers `toby-swd-experiment`, user feedback, a proof of concept, a spike, parameter tuning, design exploration, and manual observation. Record candidate values and what the user observed. Once the user chooses the behavior, add or update tests for the durable contract if a reliable harness can protect it.

If the user will run manual tests or asks for no automated validation, treat their manual testing as the loop's verification. Report skipped checks during cleanup, when the throwaway work is deleted or merged into the project.

## Mocks and test doubles

Default to the highest-fidelity dependency that is fast and deterministic.

1. **Real implementation** when it's fast enough and stays in-process. Examples are real domain objects, in-memory databases, and real validators.
2. **Fake** when the real thing is slow, external, or hard to set up. A fake is a hand-written stand-in with realistic behavior, faster than the real thing and more faithful than a mock.
3. **Mock** only at system boundaries: external APIs, payment, email, time, randomness, file systems, and specific failure modes that are hard to trigger otherwise.

When the real dependency is across a process, sandbox, or hardware boundary you can't run in-process, that boundary is the system boundary. Fake the channel or simulate the environment, and test each side against the contract. Mocking the other side's internals couples the test to its structure.

Mocking internal collaborators couples tests to call sequences and current structure. The test passes today, but a later refactor breaks fifteen tests, and the team starts deleting tests to keep CI green. Keep internal collaborators real so that this series of events does not happen.

Verify state and results over interactions. "The order is paid" is a behavior, while "paymentService.process was called once with amount=42" is a call log.

## Before deleting or weakening a test

Before changing a failing test, classify it into one of these buckets:

1. **Behavior still valid, production broke it.** Fix the production code.
2. **Behavior intentionally changed.** Update the test to describe the new behavior.
3. **Behavior is obsolete.** Remove the test and explain why in the commit message.
4. **Bad test.** The test is coupled to internals, asserts on incidental data, or doesn't test what its name claims. Rewrite it to protect the same useful behavior through a better interface.

Read a test you can't classify until you understand it. The suite passes but protects no behavior after mass-updated snapshots, deleted cases that "break a lot," or assertions weakened to get a PR merged.

When you deliberately delete or weaken a test, report its name, the behavior it protected, why that behavior is obsolete, and what coverage replaces it. Do not remove a test without reporting it.

## Brownfield Work

In an existing codebase, inspect the tests that already cover the touched behavior before adding new ones. If coverage is thin, offer a focused regression test for a bug or a characterization test for behavior the code already depends on. Keep the test at the public boundary when one exists, and avoid testing incidental internals only because legacy tests did. If the user declines automated tests, record the chosen verification source and keep the production change scoped.

## Red flags

Before calling test coverage done, check it against every red flag below.

- **Test fails on a correct refactor.** The test is coupled to internals.
- **Test name describes a call.** "calls X with Y" describes a mock log. The reader still can't tell what the system is supposed to do.
- **Snapshot blob.** The snapshot is a large auto-updated string that goes unreviewed when it changes.
- **Flaky test.** It passes on retry and fails at random. It is a broken test, so fix the nondeterminism and never loop it until it goes green.
- **Mock of an internal collaborator.** The mock verifies the call sequence, which says nothing about what the system produces.
- **Coverage-driven test.** The test was written to hit a line. It protects no behavior. It reads like the implementation with the word "expect" added in places.
- **Hard-to-name test.** The abstraction under test is wrong or mixed.
- **Test deleted to make the suite green.** Deleting the test is almost always wrong, so classify it first.
- **Bug fix without a regression test.** The fix is unverified, so the bug can now return without anyone noticing.
