---
name: toby-swd-testing
description: >-
  Tests are executable specifications of behavior. Apply this skill on every
  task that writes, modifies, or deletes tests — new test files, additions to
  existing suites, bug fix regression tests, snapshot updates, test rewrites.
  Also apply whenever production code is changing and tests need to follow. The
  default reflex of "make the failing test green by tweaking the assertion" is
  how suites rot into theater. Backend and frontend alike.
---

# Toby SWD Testing

A test suite exists for three jobs: pin down what the system does so callers can rely on it, catch regressions when something changes, and make refactoring safe enough that the team will do it. Do those three jobs. A suite that locks in implementation details does worse than nothing, because it slows every change, lies about coverage, and trains the team to ignore failures.

**Describe behavior at the public interface.** Inputs go in, outputs come out, observable side effects show up where callers would notice them. Internal call order, private method signatures, the order helpers fire, and intermediate data shapes are invisible from outside the module and should be invisible to the test. Write tests that survive a correct refactor. A test that fails because you renamed a helper while preserving behavior is detecting the diff and nothing else.

## Name tests by behavior

The test name is the spec. A reader who sees only the name should know what the system does in that scenario.

Use:
- `checkout confirms a paid order`
- `withdrawal reduces the account balance`
- `expired token is rejected`

Avoid:
- `calls paymentService.process`
- `sets internalOpenIndex to 1`
- `returns object with status field`

If you can't name the behavior, you don't know what you're testing. That is a design signal. Usually the abstraction boundary you're testing through is wrong, or the behavior under test is tangled with something else.

## Test through public interfaces

Tests at the boundary survive refactors. Tests that reach into internals do not.

Concretely: don't import private modules to test them. Don't assert on private state. Don't verify that helper X was called before helper Y unless that call sequence is the observable contract — which is rare. Mock external dependencies at the system boundary. Internal collaborators stay real, because mocking them couples the test to current structure.

When a behavior is hard to test through the public interface, the abstraction is usually too coarse. The fix is to extract a smaller module with a real interface, then test through it. Do not reach into internals to "make it testable". That failure is what toby-swd-modules exists to prevent.

## Narrow assertions

An assertion should fail when the behavior under test changes. It should not fail when something incidental changes — a timestamp, a key order, a formatting tweak, a new optional field in a response.

Useful patterns:
- Assert on the specific value or field that proves the behavior happened.
- When the output is inexact by nature, assert it falls within a stated, justified tolerance of the expected value. Exact-equality assertions flake or lie on such outputs.
- Use object subset matching when only a few fields matter.
- Reserve full-object equality and snapshot matching for cases where the entire structure is the contract — config files, public response schemas, serialization formats.

Snapshot blobs that nobody reads are not tests. They are CI noise generators with version control.

Before accepting a snapshot update, read the diff and confirm every change is intended. An unread snapshot update is the same as deleting the test.

## How much to test

Cover the contract's distinct observable outcomes — the success path, each documented failure mode, and the boundary conditions — then stop. One behavioral concept per test; multiple asserts are fine when they prove one behavior. A behavioral outcome can be pinned by example (one named scenario) or by property (an invariant that holds over a range of generated inputs). Prefer whichever states the contract more directly.

## Each test stands alone

No shared mutable state between tests, no ordering dependencies, deterministic, and self-validating. Deterministic means controlling time and IO, and pinning randomness to a recorded seed so the run reproduces. Self-validating means the test asserts, and does not print for a human to read. A test whose result depends on what ran before it is already broken. When the system itself must reproduce the same outputs across runs or machines, that determinism is part of the contract under test. When a result depends on a library or platform version, record it so a later mismatch is visible.

## Test-first, with judgment

Write the test before the implementation when the behavior is well-defined. Two cases qualify:

1. **Bug fixes with defined durable behavior.** Reproduce the bug in a failing test before touching production code. This proves the test catches the bug, proves the fix works, and leaves a regression guard behind. A bug fix without a regression test is incomplete work and the bug can return without notice.
2. **New behavior with a settled contract.** Once the design pass identifies the abstraction and its interface, test-first pins down the contract and drives the implementation toward it.

Skip test-first when the design is still being worked out. Letting the next failing test drive the next bit of implementation is TDD as a substitute for design. You end up with a feature-shaped pile of code and no real abstraction. Do the design pass first (see toby-swd-strategy and toby-swd-modules), then write tests against the interface you settled on.

Also skip test-first when no relevant test harness exists, the change is documentation-only, the edit is pure formatting or metadata, or the only useful verification would require unsafe external state. Say which case applies and how you verified instead.

### Experiment loops

Defer test writing and test runs while behavior is still being discovered through toby-swd-experiment, user feedback, a proof of concept, a throwaway spike, parameter tuning, design exploration, or manual observation. Record candidate values and what the user observed. Once the user chooses the behavior, add or update tests for the durable contract if a reliable harness can protect it.

If the user says they will run manual tests or asks for no automated validation, treat that as the verification source for the loop. Report skipped checks during cleanup, when the throwaway work is deleted or folded into the project.

## Mocks and test doubles

Default to the highest-fidelity dependency that is fast and deterministic.

1. **Real implementation** when it's fast enough and stays in-process. Real domain objects, in-memory databases, real validators.
2. **Fake** when the real thing is slow, external, or hard to set up — a hand-written stand-in with realistic behavior. Faster than the real thing, more faithful than a mock.
3. **Mock** only at system boundaries: external APIs, payment, email, time, randomness, file systems, and specific failure modes that are hard to trigger otherwise.

When the real dependency lives across a process, sandbox, or hardware boundary you can't run in-process, that boundary is the system boundary. Fake the channel or simulate the environment, and test each side against the contract. Mocking the other side's internals couples the test to its structure.

Mocking internal collaborators couples tests to call sequences and current structure. The test passes today, a refactor breaks fifteen tests tomorrow, the team starts deleting tests to keep CI green. Avoid the chain.

Verify state and results over interactions. "The order is paid" is a behavior. "paymentService.process was called once with amount=42" is a call log.

## Before deleting or weakening a test

Classify the failing test before changing it. Four buckets:

1. **Behavior still valid, production broke it.** Fix the production code.
2. **Behavior intentionally changed.** Update the test to describe the new behavior.
3. **Behavior is obsolete.** Remove the test and explain why in the commit message.
4. **Bad test** — coupled to internals, asserts on incidental data, or doesn't test what its name claims. Rewrite it to protect the same useful behavior through a better interface.

Read a test you can't classify until you understand it. Mass-updating snapshots, deleting cases that "break a lot," or replacing strong assertions with weaker ones to land a PR leaves a suite that passes and protects nothing.

When you do delete or weaken a test deliberately, report the test name, the behavior it protected, why that behavior is obsolete or wrong, and what coverage replaces it. No silent removals.

## Brownfield Work

In an existing codebase, inspect the tests that already cover the touched behavior before adding new ones. If coverage is thin, offer a focused regression test for a bug or a characterization test for behavior the code already depends on. Keep the test at the public boundary when one exists, and avoid locking in incidental internals just because legacy tests did. If the user declines automated tests, record the chosen verification source and keep the production change scoped.

## Red flags

Before calling test coverage done, check it against every red flag below.

- **Test fails on a correct refactor.** Coupled to internals.
- **Test name describes a call.** "calls X with Y" names a mock log. The reader still can't tell what the system is supposed to do.
- **Snapshot blob.** Large auto-updated string nobody reviews on change.
- **Flaky test.** Passes on retry, fails at random. It is a broken test, so fix the nondeterminism and never loop it until it goes green.
- **Mock of an internal collaborator.** Verifies the call sequence, which says nothing about what the system produces.
- **Coverage-driven test.** Written to hit a line. It protects no behavior and reads like the implementation with the word "expect" sprinkled in.
- **Hard-to-name test.** The abstraction under test is wrong or mixed.
- **Test deleted to make the suite green.** Almost always the wrong move; classify first.
- **Bug fix without a regression test.** The fix is unverified and silent re-breakage is now possible.
