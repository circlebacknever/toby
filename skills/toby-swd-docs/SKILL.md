---
name: toby-swd-docs
description: >-
  Contains Toby's rules for a module's README.md and AGENTS.md. Use it when a
  module's structure or commands change, or when the user asks to write or
  update a module's README or AGENTS.md. Skip it for other prose, which
  toby-voice covers.
---

# Toby SWD Docs

In this skill, `AGENTS.md` refers to a module documentation file inside the user's project, and never to the Toby operating guide.

## Reader check

Write enough for a reader new to the module to use or change it correctly. State what enters, what result or side effect follows, and why a non-obvious constraint exists. Explain unfamiliar domain terms with a concrete case. A claim about quality needs the behavior or decision that supports it. Keep humor that helps the reader understand the point.

For a meaningful public operation or command, give a minimal runnable example with its required setup and expected result. Include a relevant failure and the caller's next action when correct use depends on it. Use the repo's actual names and commands. Run changed examples when the environment permits it, and state which ones you couldn't check. Don't claim an example runs when you only read it.

## AGENTS.md

`AGENTS.md` is the entry point for an agent editing a module: it states every non-obvious constraint and boundary up front.

### Scope

Create an `AGENTS.md` only when the user asks or the repo already keeps one at each module root (such as a service or domain package). Never create one in a leaf folder, a single-file utility folder, or a grouping directory. Put those notes in the nearest module-root `AGENTS.md` above it.

### Sections

Use these headings in order, and omit any section that has no facts to state:

1. **What this is.** One or two sentences on what the module does, plus why it exists when the code or user states that reason.
2. **Commands.** The narrowest build, test, and lint commands for this module (`pnpm test --filter notify`).
3. **Constraints.** Business, product, regulatory, or external constraints that force non-obvious code, with the outside reason and the failure each constraint prevents.
4. **Cross-module decisions.** Decisions that span multiple modules, recorded once here with a pointer comment (`// see "Event ordering" in AGENTS.md`) at each affected call site.
5. **Extension rules.** Where new files go, the conventions to match, and which upstream or downstream modules a change affects.

### Content

- State only facts from the code, the docs, or the user's request, once, in the section where they belong.
- Name a specific file only when its filename and code don't make its role obvious.
- Describe purpose, constraints, and boundaries, and point to interface comments and external specs without copying them.
- Use literal verbs for files (`stores`, `calls`, `validates`), and update `AGENTS.md` whenever a job moves between modules, a module dependency changes, or a constraint changes.

## README.md

A `README.md` is for a human who calls or maintains the module. Create one only when the user asks or when adding a package, service, or standalone feature where:

- Humans call its public API directly, or must learn the package from scratch.
- Its purpose isn't obvious from its name and layout.
- Correct use depends on initialization order, required config, or a gotcha the type system doesn't prevent.

Leave internals, version history, and copied interface comments out, and use these sections in order:

1. **What this is.** One or two sentences on the problem it solves and who calls it.
2. **How to use it.** Required setup, a minimal example for the common case, and its expected result.
3. **Concepts.** The terms a caller needs, each connected to a concrete action or example.
4. **Public API** (when not obvious from code), linking to generated docs or interface comments.
5. **Known gotchas.** Ordering, required environment, or edge cases the API doesn't guard against.

Update `README.md` whenever the public API or caller constraints change.

## Red flags

Check each doc you wrote or touched against these items:

- You created an `AGENTS.md` in a leaf folder.
- The doc copies implementation mechanics or signatures that belong in docstrings.
- Call sites repeat a cross-module reason when they should point to `AGENTS.md`.
- A structural or API change left an existing `AGENTS.md` or `README.md` describing the old state. Update the doc or report the stale line at `file:line`.
- You could delete a line in `AGENTS.md` without causing an agent mistake.
- A reader can't explain one input, its result, and the reason for a documented constraint after reading the relevant section.
- An example needs an unstated variable, setup step, credential, or ordering assumption.

Open `references/examples.md` before writing a new `AGENTS.md` or `README.md`, or when deciding which folder gets one.
