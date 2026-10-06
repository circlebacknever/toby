# Strategic work

This file has the parts of `toby-build` that apply only to strategic work. Open it when the sizing step names the work strategic, and keep the skill body's rules in force.

## Discover before designing

Strategic discovery adds these two items to the two in the skill body.

- The nearest shipped feature built the same way, on the same layer and the same data path. Read it end to end: route, handler, model, test, doc. Check that feature against the red flags in `toby-swd-modules` before copying it, and follow its structure when it passes. When a flag fires, design the new code without it, because a copied shallow module becomes two shallow modules.
- The call sites the change would affect.

**Greenfield** means the repo has no sibling feature and no convention to inherit. Before the second file exists, state the two conventions in the repo nearest to this work, even from another layer, and say which you are extending. `references/examples.md` has a greenfield example.

## Cut the work into slices

A slice is the set of criteria that become observable together at one entry point. Criteria observed at different entry points belong to different slices. Examples are a route and a scheduled job, two screens, or an API and a migration a caller can see.

Name each slice for what a person can do once it ships, in their words: `invite shows up as pending`, `search matches a full SKU`. That name becomes the plan's group heading, the stop line, and the row in the final report. A name such as `Slice 2 of 3` describes only the count, so do not use it.

A slice named for a layer, such as "the data layer", is a layer cut. It fails the observable and reachable conditions, so re-cut it at an entry point a user reaches. `references/examples.md` has four cuts worked end to end.

## Checkpoints

2. **The plan, after the design pass and before the first edit.** The user approves the plan file before any edit.
3. **The slice boundary where the next slice depends on the answer.** Stop there when a decision surfaced, a criterion turned out wrong, or discovery missed a strategic trigger. Open with what the user can now do that they couldn't before, using the slice's name, then say what proved it and what the next slice does, and wait. At a boundary with no such question, write the same three lines and continue. Stopping there anyway is stop inflation.

## The design lines

The design pass produces these lines:

- The structure chosen, and the main reason for it.
- The alternative rejected, and why.
- The sibling feature, what it got right, and its red flags at file:line, or "none".
- Each rule the feature adds, such as a count, a limit, or a table of values. Give the one function that computes it and every caller of that function.
- Each new or changed module, with the knowledge it hides from its callers.
- Each new or changed signature, with its interface comment.
- Any refactor that runs before the feature code.

Strategic work puts these lines in the plan's design block. Tactical work states the first two and any new signature in chat before the first edit.

## The plan document

Follow the operating guide's Plan Format, with these additions.

- The plan opens with the criteria in their pre-code wording and what's out of scope, then the design block. One task group per slice follows, in the order the slices ship, titled with the slice's name.
- Each command on the ask-list in the operating guide or `toby-swd-environment` appears as its own step with the exact command.
- The plan is the execution record. Check items off as they are done. When execution diverges from an approved step, edit the plan and say what changed before continuing.
- A step the user can approve gives the path of the file it touches and whether the step creates, edits, or deletes it. It says what changes there, concretely enough for someone to disagree with, quotes the criterion the step is for, and says what proves it, with the result that would mean it failed. `references/examples.md` has a task group written at that detail.

## Resuming half-built work

Before touching code, recover the mode, the criteria list, the plan, the steps already checked off, and the last checkpoint decision. Rebuild any you cannot find from the code and the original request, and list which ones you rebuilt. Confirm them before continuing, because criteria rebuilt from a diff repeat the diff's mistakes. Half-built experiment code stays experiment code until the user says otherwise.
