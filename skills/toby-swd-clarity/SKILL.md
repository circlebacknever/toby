---
name: toby-swd-clarity
description: >-
  Contains Toby's rules for names, comments, and docstrings inside code. Use it
  when naming something in code, or writing or fixing a comment or docstring.
  Skip it for prose outside code, which toby-voice covers.
---

# Toby SWD Clarity

Names and types state part of a contract, and comments state the rest: behavior, side effects, reasons, and invariants the type system can't enforce. Where the language allows, encode units, nullability, and valid states in the type. Non-trivial code without an interface comment is unfinished.

## Naming

Pick each name so a reader who sees only the identifier guesses what the variable holds or what the function does. Make names more specific as their scope widens: `i` fits a three-line loop, while fields, parameters, and exports need exact names. Avoid overly narrow names (such as `selection` on a function that accepts any text range). Use `data`, `value`, `result`, `status`, `flag`, or `count` only in tiny scopes where the meaning is obvious.

Give each name one meaning, and pair related variables with a shared root and prefix (`srcBlock` and `dstBlock`). When a function or variable needs a long, awkward name, split its two jobs apart. Keep a dense expression whole when its result has one clear name.

## Consistency

Do similar things the same way, and dissimilar things differently. Match the file and repo's conventions for naming, structure, error handling, and test layout, and reuse the existing term for each domain concept.

Change an existing convention only when new evidence justifies converting every call site in the same diff. When one concept has multiple names across the repo, list the repo-wide rename as a follow-up and don't add another local name.

## Proportionality

On every edit, check that a developer new to the file understands the touched names, types, and comments on the first read. When a change alters a cross-module constraint on exported or shared code, update the module's existing `AGENTS.md` as `toby-swd-docs` describes. Leave clear code outside the diff alone.

## Red flags

Check the touched code against each item before finishing:

- A name is vague, hard to coin, or reused for two purposes.
- A comment restates the code, or an interface comment describes internal mechanics.
- A field or parameter omits its units, bounds, or what null means when the type doesn't show them.
- Non-trivial exported code lacks an interface or field comment.
- The touched code handles the same concept in two ways, or a quick read misreads the control flow.

Open `references/comments.md` when adding or editing a comment, docstring, or non-obvious control flow. Open `references/examples.md` when typing a hook return or documenting units, bounds, null meaning, or callbacks.
