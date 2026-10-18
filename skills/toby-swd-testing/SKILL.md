---
name: toby-swd-testing
description: >-
  Keep tests an executable specification of behavior, and classify a failing
  test before anyone edits it. Use it when the user asks to write, rewrite,
  delete, or weaken a test, raise coverage, update snapshots, or fix a flaky
  test. Skip it when production code changes too, which toby-build or
  toby-bug-fix covers. Skip it for a throwaway spike, which toby-swd-experiment
  covers, and for a run of the suite alone, which toby-swd-environment covers.
---

# Toby SWD Testing

Tests record the behavior callers rely on, checked through the public interface. Edit an existing test only when the required behavior changes, because a test that breaks during a behavior-preserving refactor is checking internals. Assert call order only when that order is part of the contract.

When a behavior is hard to test, extract a smaller module with a real interface and test through it. Never expose private internals only for a test.

## Failing tests

Open `references/failing-tests.md` to classify a failing test before editing, skipping, or deleting it, and whenever a test fails intermittently.

## Names

Name each test for the behavior it specifies (`expired token is rejected`), and never for an internal method call (`calls paymentService.process`).

## Assertions

An assertion fails when the behavior under test changes, and never on a timestamp, field order, formatting, or a new optional field.

- Assert the specific value or field that proves the behavior happened, or assert an inexact output within a justified tolerance.
- Use subset matching when only a few fields matter, and use full equality or a snapshot only when the whole structure is the contract (such as a schema or serialized format).
- Ask before updating a snapshot, read the diff, and confirm every change is intended.

## Coverage

Cover the success path, each documented failure mode, and the boundary conditions, then stop. Keep one behavior per test, with as many assertions as that behavior needs. Default to concrete example inputs, and add a property test when the contract is a round trip, equivalence with a reference model, or an invariant.

For a migration that alters or backfills an existing table, seed pre-migration rows (including nulls and boundary values), run the migration, and assert the migrated rows. Check whether a test drives each new entry point (route, CLI command, screen, queue consumer, or job), and open `toby-swd-e2e` when none does.

## Independence

Each test shares no mutable state with other tests and passes in any order. Control time and I/O, seed randomness, and test date, window, or expiration rules with a fixed clock across non-UTC timezones and boundary dates (month ends, leap days, daylight saving).

## Test-first

Write the test first in two cases:

1. **A bug fix where the required behavior is known.** Reproduce the bug in a failing test before touching production code, and confirm it fails on the assertion for the bug and not on a setup error.
2. **New behavior with a settled contract.** After `toby-swd-strategy` and `toby-swd-modules` settle the interface, write the test that specifies the contract, then implement to it.

Skip test-first while the design is open, when the repo doesn't have a test harness, when the change is docs or formatting, or when the check needs unsafe external state. State which case applied and how you verified.

## Prove a change

An acceptance criterion counts as met after two runs of the same named command, quoted under the criterion's wording. For new or fixed behavior, the `before` run fails on the target assertion and the `after` run passes (when you wrote the test after the production edit, revert or stash the production edit first to record the `before` failure):

    cancelling a shipped order returns 409 and leaves the order untouched
    before  test_cancel_rejects_shipped  FAIL  expected 409, got 200
    after   test_cancel_rejects_shipped  PASS

For a criterion stating that existing behavior stays working, both `before` and `after` pass (`PASS`). An `after` run without a `before` run leaves the criterion unmet.

## Test doubles

Use the highest-fidelity dependency that is fast and deterministic:

1. **Real implementation** when it runs fast locally, including domain objects and the repo's test database (ask before starting a local database or container, as `toby-swd-environment` requires).
2. **Fake** (a lightweight in-memory implementation with real behavior) when the real dependency is external or slow.
3. **Mock** only at the boundary of an external system (third-party API, payment processor, email, message bus) or to simulate time, randomness, and injected faults. Validate HTTP stubs against the provider's schema or recorded fixtures.

Assert the resulting state (`order is paid`) or the external boundary payload, and never assert internal call logs. Open `references/dependencies.md` before mocking a third-party provider or swapping a database engine.

## Existing tests

Read the existing tests for the touched area before adding new ones. When coverage is thin, report the gap as a risk and state the characterization test that would pin today's behavior.

## Red flags

Check for each of these before calling testing done:

- An expected value was copied from the code's output and not worked out from the spec.
- A test only hits lines without asserting behavior, or a flaky test was rerun until it passed.
