---
name: toby-swd-plan
description: >-
  Contains Toby's rules for writing a plan as slices with checks that can fail.
  Use it when writing or revising a plan file. Skip it for a status update in
  chat.
---

# Toby SWD Plan

Write the plan as one group of steps per vertical slice.

## Intent

Open the plan with the user's intent in their words, the result that fulfills it, the work mode, and the command that checks the whole task. List every follow-up you would suggest once the plan finishes, placing each in a slice or under `Out of scope` with its reason.

## Slices

A slice is the work behind one new action a person can run or see. Put every route, migration, job, or email that action needs in the same slice, and put criteria at unrelated entry points in separate slices.

Name each slice for what a person can do once it ships (`invite shows up as pending`). Use that exact name for the group heading, the group filename, the stop at its end, and its row in the final report. Order slices so every slice leaves the system working. When an earlier slice deploys before a later slice completes the flow, guard it with an off-by-default release flag (`toby-swd-flags`).

## File layout

Save a plan with up to three groups at `docs/plans/<feature-group>/<plan-name>.md`. Save a larger or multi-session plan as a folder at `docs/plans/<feature-group>/<plan-name>/`:

- `<plan-name>/overview.md` contains the intent, the whole-task check, the work mode, the criteria, each assumption, `Out of scope` items, the design block, and a table of group files with their criteria, dependencies, and status (`not started`, `in progress`, or `done`).
- One `NN-<slice-name>.md` per slice contains the criteria it meets, its steps, any rollback step for schema or external state changes, and its verification block.

A single-file plan contains the same sections in the same order.

## Steps

Give each step the file path, whether it creates, edits, or deletes the file, what changes there, and the criterion number it serves. Give any command on the operating guide's or `toby-swd-environment`'s approval list its own step with the exact command.

Check off each step as it finishes. When work departs from an approved step or turns up a missing step, update the plan and state what changed before continuing. Include a step-level check only when it can fail while the group's end-to-end check passes (such as a unit test for duplicate rejection).

## Verification

Start each group's verification with the end-to-end check (`toby-swd-e2e`) that drives the slice's entry point. Run each check before and after the slice's edits and record the output under the check. Checks for new behavior must fail (`FAIL`) before and pass (`PASS`) after, while checks for existing behavior must pass (`PASS`) both before and after.

Leave out checks that pass even when the behavior is broken, such as "`\d invites` lists the columns" or "`grep` finds the new route".

## The whole feature

When a feature has two or more slices, add and run one end-to-end test in the last group that walks through every slice in order. Then compare the finished behavior against the intent in `overview.md`.

Open `references/example.md` for a two-slice plan folder example.
