---
name: toby-swd-campfire
description: >-
  Contains Toby's refactor before a change and the design check after it. Use
  it when a change lands in code that makes the change hard, or after the tests
  pass to check the design. Skip it when the user asks for a refactor alone,
  which toby-refactor covers.
---

# Toby SWD Campfire

Leave each file the change touches easier to change than you found it: make the change easy before the first edit, and check the design after the tests pass.

When the user asked for the smallest diff, or you take a shortcut allowed by `toby-swd-strategy`, skip the refactor edits, run the design check anyway, and list each skipped fix as a follow-up at `file:line`.

## Before the first edit

Ask what the code would look like if it had been designed for this change. When the current code has one of the obstacles below, refactor first with behavior unchanged, then add the feature on top without a workaround:

- a business value (such as a 30-day refund window) or a multi-condition rule that you would otherwise copy or edit in two places
- a business rule computed inside an entry point that this change must edit or reuse
- a branch you would have to hunt for across multiple files, or a misleading name in the touched path

Run the preparatory refactor as its own step when all three hold:

- It stays inside the files the change edits anyway, plus at most one new module for a rule moved out of an entry point.
- You state it before the first edit in the design block or plan.
- Existing tests or a new characterization test (`toby-swd-testing`) cover the moved behavior, and you confirm implicit contracts (serialized field names, caught exception types, transaction scope, and metric keys) stay intact.

Run the tests after the refactor and before the feature edit without altering any test assertion. When the refactor exceeds the scope above, list it as a follow-up at `file:line` with its cost and what it simplifies. Skip this step in generated or vendored files.

## After the tests pass

Run the 11-point design check in `toby-swd-architecture` on the finished diff, fix what it finds, and rerun the tests. Fix every wrong comment, dead branch, or misleading name in the lines the diff changed. For untouched lines in the same function, fix one or list it as a follow-up at `file:line`. In a planned build, add any design-check fix to the plan before making it, and list fixes in untouched files as follow-ups.

## Report

List each preparatory refactor and design-check fix at `file:line`, with one line stating what the next change no longer has to touch.
