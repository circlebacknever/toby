---
name: toby-swd-docs
description: >-
  Contains Toby's rules for a module's README.md and AGENTS.md. Entry skills
  open this file by path. Do not load it from a user request alone.
disable-model-invocation: true
---

# Toby SWD Docs

`AGENTS.md` in this skill means a file in the user's module tree, and never the operating guide.

## AGENTS.md

AGENTS.md is the entry point for an agent writing code in a module. Write it for a capable reader who has never seen the code and needs every surprise stated up front.

### Scope

Create one at the root of a module, package, or feature that covers a distinct area of knowledge. Examples are a service, a domain package, a frontend feature, and a store module. Do not create one for a leaf folder, a single-file utility directory, or a folder that only groups files. Many small files go stale, and readers stop trusting them. When unsure, put the content in the nearest meaningful module root.

### Sections

Use these headings in this order, and leave out a section that has no fact to state.

1. **What this is.** Write one or two sentences on what the module does. Give the reason it exists only when the code or the user states it.
2. **Commands.** Give the narrowest command that builds, tests, or lints this module, such as `pnpm test --filter notify`. Cite a file in a later section only when its job does not show in its name or code.
3. **Constraints.** List the business, product, regulatory, or external constraints that force non-obvious code, with the outside reason for each.
4. **Cross-module decisions.** Record once each decision that touches several modules and that no single module can contain. Each affected site gets a one-line pointer comment, such as `// see "Event ordering" in AGENTS.md`.
5. **Extension rules.** State where new files go, the conventions and patterns to match, and which upstream or downstream modules a change affects.

### Content

- Write only what the code, the docs, or the user's request states. Do not add a reason, a retry policy, an input, a return value, or a future case that none of those sources gives.
- State each rule once, in the section where it applies.
- Describe purpose, constraints, and structure, and leave implementation mechanics to code comments, so the file stays accurate through code changes.
- Point to interface comments and external specs, and do not copy them.
- Write what a file does with a verb such as stores or calls, and never that it knows something or lives somewhere.

Update AGENTS.md when responsibility moves, a file's job changes, a cross-module dependency is added or removed, or a constraint changes. When a section cannot stay accurate at its detail level, make it shorter and more abstract.

## README.md

A README.md is for a human who calls or maintains the module. Most modules need none. Create one only when one of these holds:

- The module has a public API that humans call directly.
- The module's purpose is not clear from its name and structure.
- Correct use depends on initialization order, required configuration, or a known gotcha the API does not protect against.
- It is a package, library, service, or standalone feature that a human has to learn from scratch.

Leave internals, implementation reasons, version history, and copies of interface comments out of it. Use these sections in order:

1. **What this is.** Write one or two sentences on the problem it solves and who it is for.
2. **How to use it.** Give the minimal working example for the common case, before any environment setup.
3. **Concepts.** List the abstractions a caller works with.
4. **Public API**, when the code does not make it plain. Cover only the public API, and link to generated docs when they exist. When the interface splits common calls from advanced ones, keep that split.
5. **Known gotchas.** List what breaks for a user who does not know it, such as ordering, required environment, and edge cases the API does not protect against.

Update the README.md when the public API changes, a constraint is added, or a user reports confusion that the README.md should have prevented.

## Red flags

Before finishing, check each file you wrote for these, and report each one that matched:

- An AGENTS.md is in a leaf folder.
- The file describes implementation mechanics or behavior that belongs in an interface comment.
- A cross-module reason is copied at each site, when the sites should point to AGENTS.md.
- A structural change or an API change shipped with the file still describing the old state.
- A line in an AGENTS.md would cause no agent mistake if it were removed. Delete that line.

## Existing modules

When work touches a meaningful module, check the nearest module root for an AGENTS.md. Check an existing file for accuracy before editing it. When responsibility moves, a public API changes, or a cross-module rule appears, update the nearest AGENTS.md when docs are in the task's scope. Otherwise report the line the change made stale, at file:line, as a risk.

Open `references/examples.md` before writing a new AGENTS.md or README.md, or when deciding which folder gets one.
