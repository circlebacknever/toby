---
name: toby-swd-testing
description: >-
  Keeps tests an executable specification of behavior, and classifies a failing
  test before anyone edits it. Use it when the user asks to write, rewrite,
  delete, or weaken a test, raise coverage, update snapshots, or fix a flaky
  test. Skip it when production code changes too, which toby-build or
  toby-bug-fix covers. Skip it for a throwaway spike, which toby-swd-experiment
  covers, and for a run of the suite alone, which toby-swd-environment covers.
---

# Toby SWD Testing

Tests record the behavior callers rely on, checked through the public interface. Edit an existing test only when the required behavior changes. A test that needs an edit during a refactor is checking internals. Assert call order only when that order is the observable contract.

When a behavior is hard to test, the abstraction is too coarse. Extract a smaller module with a real interface and test through it. Do not expose internals only so a test can reach them.

## Failing and flaky tests

Open `references/failing-tests.md` to classify a failing test before you edit, skip, or delete it, and when a test fails only some of the time.

## Names

Name each test for the behavior it specifies, such as `expired token is rejected`, and never for a call, such as `calls paymentService.process`.

## Assertions

An assertion fails when the behavior under test changes, and never on a timestamp, key order, formatting, or a new optional field.

- Assert the specific value or field that proves the behavior happened.
- Assert an inexact output within a stated, justified tolerance.
- Use object subset matching when only a few fields matter.
- Use full-object equality or a snapshot only when the whole structure is the contract, such as a config file, a response schema, or a serialization format.

Read the diff before accepting a snapshot update, and confirm every change is intended.

## Coverage

Cover the success path, each documented failure mode, and the boundary conditions, then stop. Keep one behavior per test, with as many asserts as that behavior needs. Default to tests with specific example inputs. Add a property test when the contract is a round trip, agreement with a simpler reference version, or an invariant.

Check whether a test drives each entry point the change adds, such as a route, command, screen, queue consumer, or job. When none does, open `toby-swd-e2e`, which says when to add one.

## Independence

Each test shares no mutable state with other tests and passes in any order. Control time and IO, seed randomness, and assert results so the test checks itself.

## Test-first

Write the test first in two cases:

1. **A bug fix where the correct behavior is defined and will stay required.** Reproduce the bug in a failing test before touching production code. Read the failure and confirm it shows the bug's wrong result. A failure from an import error, a missing fixture, or a typo proves only that the test is broken.
2. **New behavior with a settled contract.** After the design pass settles the interface, write the test that defines the contract, then implement to it.

Skip test-first while the design is open, and do the design pass first with `toby-swd-strategy` and `toby-swd-modules`. Also skip it when no harness exists, the change is docs or formatting, or the check needs unsafe external state. Say which case applied and how you verified.

## Prove a change

An acceptance criterion counts as met after two runs of the same named command. Quote both results under the criterion's own wording. The first run is against the code before the change, or with the new path disabled, and the second is after:

    cancelling a shipped order returns 409 and leaves the order untouched
    before  test_cancel_rejects_shipped  FAIL  expected 409, got 200
    after   test_cancel_rejects_shipped  PASS

Use the same form for every criterion in every slice, as `toby-swd-plan` defines a slice, with the command written beside it. An `after` run with no `before` run proves only that the harness runs, so report that criterion unmet and state the missing run.

## Test doubles

Use the highest-fidelity dependency that is fast and deterministic:

1. **Real implementation** when it runs fast on the test machine, such as domain objects, a validator, or the repo's test database. When the repo has none, or a test needs engine behavior such as `select_for_update`, run the production engine locally or in a container.
2. **Fake**, a hand-written stand-in with realistic behavior, when the real thing is slow, external, or hard to set up.
3. **Mock** only a dependency whose calls another system sees, such as a third-party API, payment, email, or a message bus. Mock or fake time, randomness, and hard-to-trigger failures.

Assert a state such as "the order is paid", or what another system received, such as exactly one Slack post. Never assert an internal call log such as "process called once with amount=42".

Open `references/dependencies.md` before you mock a third-party provider or swap the database engine, or when a test depends on another process, version, or machine.

## Existing tests

Read the tests that cover the touched behavior before adding new ones. When coverage is thin, report the untested behavior as a risk, and state the characterization test that would cover it. A characterization test records what the code does today. When the user declines automated tests, record the verification they chose.

## Red flags

Before calling coverage done, check for each of these:

- An expected value was copied from the code's output, so the test passes with the bug in place. Work it out from the spec or by hand.
- A test exists only to hit a line.
- A flaky test was rerun until it passed.
