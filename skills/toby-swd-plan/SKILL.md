---
name: toby-swd-plan
description: >-
  Contains Toby's rules for writing a plan as slices with checks that can fail.
  Entry skills open this file by path. Do not trigger it from a user request
  alone.
disable-model-invocation: true
---

# Toby SWD Plan

Write the plan as one group of steps per slice.

## Slices

A slice is the work behind one new thing a person can do. Put every route, job, or email that thing needs in the same slice. Criteria at unrelated entry points, such as a claim route and an hourly job, go in different slices.

One entry point can hold several slices. Each slice is correct on its own and small enough for one session, such as `report downloads as CSV` and then `CSV export keeps the current filters`.

Name each slice for what a person can do once it ships, in their words, such as `invite shows up as pending`. Use that name for the group heading, the group file, the stop at its end, and its row in the final report.

Put a migration or a route in the step whose test fails without it.

Order the slices so each one ships working, with no half-built behavior a person can reach. When a slice is not correct until a later one ships, merge the two. Use a flag only when the earlier slice will ship first, such as when main deploys on every merge. Open `toby-swd-flags` before you write the flag's step.

## One file or a folder

A plan folder holds these files:

- `<plan-name>/overview.md` has the mode, the problem, the criteria in their pre-code wording, what is out of scope, the design block, and the whole-feature test. The overview ends with a table of the group files in order, each marked not started, in progress, or done. Mark a row done when that group's verification passes.
- One `NN-<slice-name>.md` per group, such as `team-invites/01-invite-shows-up-as-pending.md`, has the criteria the slice meets, its steps, and its verification.

A one-file plan has the same parts in the same order.

## Steps

Give each step the path of the file, whether it creates, edits, or deletes that file, and what changes there. Give the number of the criterion each step serves. When every step in a group serves the same criterion, say so once under the group heading.

Give each command that needs the user's approval its own step, with the exact command. The operating guide and `toby-swd-environment` list those commands. Check off each step as it finishes. When the work departs from an approved step, edit the plan and say what changed before you continue. At each stop, write the user's answer at the end of that group, and edit the next group's steps to match before you start them.

A step gets its own check only when that check can fail while the group's check passes. A unit test for a rejected duplicate is one example.

## Verification

Start each group's verification with one check that runs the slice where a person reaches it, such as an end-to-end test. Run the check before the group's work and watch it fail, then run it again after. `toby-swd-e2e` describes that test. Only after a run, write each check's before and after results under that check, so you can quote them in a later session.

Leave out a check that passes whether or not the work is right. For example, "`\d invites` lists the columns" passes once the migration runs, before any code writes an invite. "`grep` finds the new route" passes when the handler returns the wrong body.

Add the existing tests for the touched area when a criterion says that behavior stays the same.

## The whole feature

When the feature has two or more slices, state its end-to-end scenario in the overview, such as invite, accept, then sign in. The last group adds one test that walks through that scenario, and its verification runs that test. When the feature has one slice, its group's end-to-end test is the whole-feature test.

`references/example.md` has a plan folder for a two-slice feature, with its overview and its first group file.
