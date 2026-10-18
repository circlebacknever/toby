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

## AGENTS.md

`AGENTS.md` is the entry point for an agent editing a module: it states every non-obvious constraint and boundary up front.

### Scope

Create an `AGENTS.md` only when the user asks or the repo already keeps one at each module root (such as a service, domain package, or frontend feature). Never create one in a leaf folder, a single-file utility folder, or a grouping directory. Put those notes in the nearest module-root `AGENTS.md` above it.

### Sections

Use these headings in order, and omit any section that has no facts to state:

1. **What this is.** One or two sentences on what the module does, plus why it exists when the code or user states that reason.
2. **Commands.** The narrowest build, test, and lint commands for this module (`pnpm test --filter notify`).
3. **Constraints.** Business, product, regulatory, or external constraints that force non-obvious code, with the outside reason for each.
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
2. **How to use it.** The minimal working example for the common case, before environment setup.
3. **Concepts.** The core abstractions a caller works with.
4. **Public API** (when not obvious from code), linking to generated docs or interface comments.
5. **Known gotchas.** Ordering, required environment, or edge cases the API doesn't guard against.

Update `README.md` whenever the public API or caller constraints change.

## Red flags

Check each doc you wrote or touched against these items:

- An `AGENTS.md` was created in a leaf folder.
- The doc copies implementation mechanics or signatures that belong in interface comments.
- A cross-module reason is duplicated across call sites when the sites should point to `AGENTS.md`.
- A structural or API change left an existing `AGENTS.md` or `README.md` describing the old state (update it when docs are in scope, or report the stale line at `file:line`).
- A line in `AGENTS.md` could be deleted without causing an agent mistake.

Open `references/examples.md` before writing a new `AGENTS.md` or `README.md`, or when deciding which folder gets one.
