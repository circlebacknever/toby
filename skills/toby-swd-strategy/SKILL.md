---
name: toby-swd-strategy
description: >-
  Contains Toby's design pass, run before a change. Use it before any change
  beyond one line, and before a switch to a new tool or framework. Skip it for
  a change that copies a pattern already in the file.
---

# Toby SWD Strategy

Leave the code you change easier to change than it was. Don't count working code as progress when it adds a special case or a hidden dependency.

## Design pass

For anything beyond a one-line change, don't implement the first idea. When the change copies the structure of nearby code or passes a new optional parameter unchanged to an existing call, write `Structure: follows <path:line>` and skip this pass. For a routine single-function signature whose first comment passes `toby-swd-interfaces`, one design is enough unless the module boundary changes. When replacing a tool or structure, design each option to remove the old one completely.

- State the change in one sentence, and list each likely next change that the request, a ticket, a TODO, or `git log` states (leaving out any you inferred).
- Sketch at least two approaches that differ in which module handles the hard part, what the interface exposes, and what callers must manage. Make the second approach the strongest alternative a competent engineer would pick, and choose the one with the simplest caller-side interface.
- Check each stated next change against the design. When one would force callers to change or add a special case, adjust the design now.
- When those changes add cases picked by a tag or type, choose the dispatch now using `toby-swd-extensibility` (a lookup map for small stateless branches, or an interface with implementations when cases hold state).

In `toby-swd-modules`, check 3 ("Pull complexity downward") decides where complexity goes, and check 7 ("Split or merge") decides when to split a function.

## Existing code

Before editing existing code, follow "Before the first edit" in `toby-swd-campfire`. After the tests pass, follow its "After the tests pass".

## The shortcut

Take a tactical shortcut only when one of these holds:

- The user accepted the shortcut and its cleanup cost to meet a hard external deadline.
- The sound refactor would change an interface that other teams or external callers depend on, and coordinating that change is out of scope.
- The sound design depends on facts you don't have and can't read from the repo.

Speed alone doesn't qualify. When you take a shortcut, leave a comment stating the sound design, why it was deferred, and the condition for completing it.

## Report

After a change with a design decision, report the structure chosen and the main alternative rejected, plus any cleanup beyond the request and any shortcut taken.

Open `references/examples.md` when comparing two approaches for a caller-facing change or labeling a deadline shortcut. Open `references/design-note.md` when writing a design note in chat.
