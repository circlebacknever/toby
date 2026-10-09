---
name: toby-swd-campfire
description: >-
  Contains Toby's refactor before a change and the design check after it. Entry
  skills open this file by path. Do not trigger it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Campfire

Leave each file the change touches easier to change than you found it. Make the change easy before the first edit, and check the design once the tests pass.

When the user asked for the smallest diff, or you take the shortcut that `toby-swd-strategy` allows, skip the edits both sections ask for. Run the design check anyway, and list each refactor or fix you skipped as a follow-up at file:line.

## Before the first edit

Ask what the code would look like if it had been designed with this change in mind. When the answer is the current code plus the new part, add the part. When the current code has a problem from the list below, refactor first with behavior unchanged, then add the change on top with no workaround.

Look for what would make this change harder than it needs to be:

- a business value, such as a 30-day refund window, that you would copy or edit in two places
- a rule with more than one condition, or a block over three lines, that you would copy or edit in two places
- a rule that an entry point computes and the change must edit or copy
- a case you would have to search for across several files
- a misleading name

Refactor first, as its own step, when all of these hold:

- It stays in the files the feature would edit anyway, plus at most one new module for a rule you move out of an entry point.
- You state it before the first edit, in the design lines of `toby-build` or in the plan.
- A test already covers the code it moves, or the plan lists a characterization test for it, as `toby-swd-testing` describes.

Run the tests after the refactor and before the feature code, and change no test to make them pass. When the user asked for commits, the refactor gets its own commit.

When the refactor fails a condition above, list it as a follow-up. Give its file:line, its cost, and what it would make easier, so the user can choose to do it first.

Skip this section in generated or vendored code. Start no cleanup outside the code the change touches, and plan no separate cleanup phase.

## After the tests pass

Run the design check in `toby-swd-architecture` on every finished diff. Fix what it finds, and run the tests again. When the lines the change touched have an unclear name, dead branch, or wrong comment, fix one, or list it as a follow-up at file:line.

In a planned build, add each fix to the plan as a step before you make it. List a fix that needs an untouched file as a follow-up at file:line.

## Report

List each refactor and each fix at file:line, with one line on what the next change no longer has to touch.
