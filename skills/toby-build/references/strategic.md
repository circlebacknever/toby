# Strategic work

This file has the parts of `toby-build` that apply only to strategic work. Open it when the sizing step marks the work strategic. The rules in the main toby-build file still apply.

## Discover before designing

Strategic discovery adds these two items to the two in the skill body.

- The shipped feature most like this one, built on the same layer and reading and writing the same data. Read it end to end: route, handler, model, test, doc. Check that feature against the red flags in `toby-swd-modules` before copying it, and follow its structure when it passes. When a flag applies, design the new code without that flaw. A shallow module has an interface nearly as complex as the work it does, and copying one gives you two.
- The call sites the change would affect.

**Greenfield** means the repo has no sibling feature and no convention to inherit. Before you create a second new file, state the two repo conventions most like this work, even if one comes from another layer. Say which one you are extending. `references/examples.md` has a greenfield example.

## Cut the work into slices

A slice is the set of criteria that become observable together at one entry point. Criteria observed at different entry points belong to different slices. Examples are a route and a scheduled job, two screens, or an API and a migration a caller can see.

Name each slice for what a person can do once it ships, in their words: `invite shows up as pending`, `search matches a full SKU`. Use that name as the slice's group heading in the plan, at the slice's stop, and as its row in the final report. A name such as `Slice 2 of 3` describes only the count, so do not use it.

A slice named for a layer, such as "the data layer", is a layer cut. A user cannot observe or reach a layer cut, so it fails two of the four conditions a slice must meet to ship. Cut the work again so each slice ends at an entry point a user reaches. `references/examples.md` shows four features cut into slices, with every step written out.

## Checkpoints

2. **The plan, after the design pass and before the first edit.** The user approves the plan file before any edit.
3. **The end of a slice, when the next slice depends on the user's answer to a question.** Stop there when a decision came up that the user must make, a criterion turned out wrong, or discovery missed a strategic trigger. Open with what the user can now do that they couldn't before, using the slice's name, then say what proved it and what the next slice does, and wait. At a boundary with no such question, write the same three lines and continue. Stopping there anyway is stop inflation, which means a stop with no question for the user.

## The design lines

The design pass produces these lines:

- The structure chosen, and the main reason for it.
- The alternative rejected, and why.
- The sibling feature, what it got right, and its red flags at file:line, or "none".
- Each rule the feature adds, such as a count, a limit, or a table of values. Give the one function that computes it and every caller of that function.
- Each new or changed module, with the details it hides so its callers do not need to know them.
- Each new or changed signature, with its interface comment.
- Any refactor that runs before the feature code.

Strategic work puts these lines in the plan's design block. Tactical work states the first two and any new signature in chat before the first edit.

## The plan document

The operating guide is the Toby instructions file that every session loads. Follow its Plan Format section, with these additions.

- The plan opens with the criteria in their pre-code wording and what's out of scope, then the design block. One task group per slice follows, in the order the slices ship, titled with the slice's name.
- Each command that the operating guide or `toby-swd-environment` says to ask about before running gets its own step, with the exact command.
- The plan records the work as you do it. Check items off as they are done. When execution diverges from an approved step, edit the plan and say what changed before continuing.
- A step the user can approve gives the path of the file it touches and whether the step creates, edits, or deletes it. It says what changes there, concretely enough for someone to disagree with, quotes the criterion the step is for, and says what proves it, with the result that would mean it failed. `references/examples.md` has a task group written at that detail.

## Resuming half-built work

Before touching code, recover the mode, the criteria list, the plan, the steps already checked off, and the last checkpoint decision. When you cannot find one of these, rebuild it from the code and the original request. List which ones you rebuilt. Confirm them before continuing, because criteria rebuilt from a diff repeat the diff's mistakes. Half-built experiment code stays experiment code until the user says otherwise.
