---
name: toby-swd-strategy
description: >-
  Checks affected responsibilities, contracts, dependencies, invariants, and
  failure behavior. Use it for existing code and before a switch to a new tool
  or framework. A copied pattern still needs the applicable checks.
  Skip it for prose and formatting edits that leave
  those design properties unchanged.
---

# Toby SWD Strategy

Leave the code you change easier to change than it was. Don't count working code as progress when it adds a special case or a hidden dependency.

## Design pass

Identify the responsibilities, caller contracts, invariants, dependencies, and failure behavior the change affects. Check the applicable parts of `toby-swd-modules`, `toby-swd-interfaces`, and `toby-swd-architecture` before accepting a design. These checks apply to existing code and small changes too.

A nearby pattern can justify one design after it passes those checks. Cite the pattern and the reason it fits. An unchanged signature or an optional parameter doesn't establish that the behavior or caller burden stays unchanged. Compare alternatives when the change introduces a boundary, changes a contract, or exposes a flaw in the existing structure. When replacing a tool or structure, design each option to remove the old one completely.

- State the change in one sentence. List each likely next change that the request, a ticket, a TODO, or `git log` states, and leave out any you guessed.
- When comparing approaches, sketch two that differ in which module handles the hard part, what the interface exposes, and what callers must manage. Make the second approach the strongest alternative a competent engineer would pick. Choose using the caller's work, information hidden, invariants enforced, and required operational behavior.
- Check each stated next change against the design. When one would force callers to change or add a special case, adjust the design now.
- When those changes add cases picked by a tag or type, choose the dispatch now using `toby-swd-extensibility`. Use a lookup map for small stateless branches, or an interface with implementations when cases keep their own state.

In `toby-swd-modules`, check 3 ("Pull complexity downward") decides where complexity goes, and check 7 ("Split or merge") decides when to split a function.

## Existing code

Before editing existing code, follow "Before the first edit" in `toby-swd-campfire`. After the tests pass, follow its "After the tests pass".

## The shortcut

Take a shortcut only when one of these holds:

- The user accepted the shortcut and its cleanup cost to meet a hard external deadline.
- The sound refactor would change an interface that other teams or external callers depend on, and coordinating that change is out of scope.
- The sound design depends on facts you don't have and can't read from the repo.

Speed alone doesn't qualify. When you take a shortcut, leave a comment stating the sound design, why you deferred it, and when to finish it.

## Report

After a change with a design decision, say in a sentence how you structured it. Mention any shortcut you took, and mention the alternative you rejected if the user might prefer it.

Open `references/examples.md` when comparing two approaches for a caller-facing change or labeling a deadline shortcut. Open `references/design-note.md` when writing a design note in chat.
