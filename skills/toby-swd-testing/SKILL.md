---
name: toby-swd-testing
description: >-
  Tests behavior through the public interface, and classifies a failing test
  before anyone edits it. Use it when the user asks to write, rewrite, delete,
  or weaken a test, raise coverage, update snapshots, or fix a flaky test. Skip
  it when production code changes too, which toby-build or toby-bug-fix covers.
  Skip it for a throwaway spike, which toby-swd-experiment covers, and for a
  run of the suite alone, which toby-swd-environment covers.
---

# Toby SWD Testing

Tests check the behavior callers rely on through the public interface. Edit an existing test only when the required behavior changes, because a test that breaks during a refactor is checking internals. Assert call order only when that order is part of the contract.

When a behavior is hard to test, extract a smaller module with a real interface and test through it. Never expose private internals only for a test.

## Failing tests

Open `references/failing-tests.md` to classify a failing test before editing, skipping, or deleting it, and whenever a test fails intermittently.

## Names

Name each test for the behavior it checks (`rejects an expired token`), and never for an internal method call (`calls paymentService.process`).

## Assertions

An assertion fails when the behavior under test changes, and never on a timestamp, field order, formatting, or a new optional field.

- Assert the specific value or field that proves the behavior happened, or assert an inexact output within a justified tolerance.
- Use subset matching when only a few fields matter. Use full equality or a snapshot only when the whole structure is the contract (such as a schema or wire format).
- Ask before updating a snapshot, read the diff, and confirm every change is intended.

## Coverage

Cover the success path, each documented failure mode, and the boundary conditions, then stop. Keep one behavior per test, with as many assertions as that behavior needs. Default to concrete example inputs, and add a property test when checking a round trip or an invariant across inputs.

For a migration that alters or backfills an existing table, seed pre-migration rows (including nulls and boundary values). Run the migration and assert the migrated rows. Check that a test drives each new entry point (route, CLI command, screen, consumer, or job), and open `toby-swd-e2e` when none does.

## Independence

Each test shares no mutable state with other tests and passes in any order. Control time and I/O, seed randomness, and test date or expiration rules with a fixed clock across non-UTC timezones and boundary dates.

## Test-first

Write the test first in two cases:

1. **A bug fix.** Reproduce the bug in a failing test before touching production code, and confirm it fails on the assertion for the bug.
2. **New behavior with a settled contract.** After `toby-swd-strategy` and `toby-swd-modules` settle the interface, write the test that checks the contract, then implement to it.

Skip test-first while the design is open, when the repo lacks a test harness, on docs or formatting, or when the check needs unsafe external state. State which case applied and how you verified.

## Prove a change

Prove each acceptance criterion by running the same named command before and after the edit, and quote both runs under the criterion. For new or fixed behavior, the `before` run fails on the target assertion and the `after` run passes. When you wrote the test after the production edit, revert the production edit first to record the `before` failure:

    cancelling a shipped order returns 409 and leaves the order untouched
    before  test_cancel_rejects_shipped  FAIL  expected 409, got 200
    after   test_cancel_rejects_shipped  PASS

For a criterion stating that existing behavior stays working, both `before` and `after` pass (`PASS`). If you only ran `after`, mark the criterion unmet.

## Test doubles

Pick the first dependency option below that runs fast and deterministically:

1. **Real implementation** when it runs fast locally, including domain objects and the repo's test database. Ask before starting a local database or container (`toby-swd-environment`).
2. **Fake** (a lightweight in-memory implementation with real behavior) when the real dependency is external or slow.
3. **Mock** only at the boundary of an external system (third-party API, payment processor, email, message bus) or to control time, randomness, and faults. Validate HTTP stubs against the provider's schema or recorded fixtures.

Assert the resulting state (`order is paid`) or the external boundary payload, and never assert internal call logs. Open `references/dependencies.md` before mocking a third-party provider or swapping a database engine.

## Existing tests

Read the existing tests for the touched area before adding new ones. When coverage is thin, report the gap as a risk and state the test that would lock in today's behavior.

## Red flags

Check for each of these before calling testing done:

- You copied an expected value from the code's output and didn't work it out from the spec.
- A test only hits lines without asserting behavior, or you reran a flaky test until it passed.
