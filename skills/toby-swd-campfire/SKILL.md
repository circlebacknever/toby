---
name: toby-swd-campfire
description: >-
  Contains Toby's refactor before a change and the design check after it. Use
  it when a change lands in code that makes the change hard, or after the tests
  pass to check the design. Skip it when the user asks for a refactor alone,
  which toby-refactor covers.
---

# Toby SWD Campfire

Leave each file the change touches easier to change than you found it. Make the change easy before the first edit, and check the design after the tests pass.

When the user asked for the smallest diff, avoid unrelated refactors. Keep the boundary or invariant repair necessary for the requested behavior. Run the design check and list optional cleanup separately. A shortcut allowed by `toby-swd-strategy` needs its stated reason.

## Before the first edit

Ask what the code would look like if it had been designed for this change. When the current code has one of the obstacles below, refactor first with behavior unchanged, then add the feature on top:

- a business value (such as a 30-day refund window) or a multi-condition rule that you would otherwise copy or edit in two places
- a business rule computed inside an entry point that this change must edit or reuse
- a branch you would have to hunt for across multiple files, or a misleading name in the touched path

Run that refactor as its own step before the feature edit when all three hold:

- It stays inside the files the change edits anyway, plus at most one new module for a rule moved out of an entry point.
- You state it before the first edit in the design block or plan.
- Existing tests or a new test that locks in today's behavior (`toby-swd-testing`) cover the moved code, and serialized field names, caught exceptions, transactions, and metric keys stay unchanged.

Run the tests after the refactor and before the feature edit without altering any test assertion. When the refactor exceeds the scope above, list it as a follow-up at `file:line` with its cost and what it simplifies. Skip this step in generated or vendored files.

## After the tests pass

Run the applicable design questions in `toby-swd-architecture` on the finished diff, including the module, interface, invariant, and operational questions. Fix what the requested behavior requires and rerun the affected checks. Fix every wrong comment, dead branch, or misleading name in changed lines. List optional cleanup outside those lines as a follow-up at `file:line`. In a planned build, update the plan before a design-check repair. A repair required for correctness stays part of the task.

## Report

List each refactor and design-check fix at `file:line`, with one line stating what the next change no longer has to touch.
