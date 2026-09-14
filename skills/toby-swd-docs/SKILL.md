---
name: toby-swd-docs
description: >-
  Keep the two module documents accurate: AGENTS.md for agents writing code
  in a module, README.md for humans using it. Use it when a task changes
  module structure, a public API, a cross-module decision, an extension
  rule, or human-facing module usage. One of each per meaningful module
  root, never per folder, and check the existing file for accuracy before
  editing it. Skip it for code comments and docstrings, which
  `toby-swd-clarity` owns.
---

# Toby SWD Docs

This skill means the `AGENTS.md` inside the user's own module tree, the file it teaches you to write. Toby's operating guide is a different file, already loaded by the host tool, and these rules never mean it.

A module has two categories of information that the code itself can't express. The code says *what*, and these files say *why*, *who this is for*, and *how to think about it*.

Don't mix up the two files, because they have different audiences and different jobs.

---

## AGENTS.md — for agents writing code here

An AGENTS.md is the single discoverable entry point for an agent working in this module. Its job is to record what the code can't: the conceptual model, the reasons behind non-obvious decisions, and the design decisions that span modules.

An agent without an AGENTS.md has no record of these reasons, so it finds the gaps only when something breaks. Write this file for a capable reader who has never seen this code and needs every surprise stated up front.

### Scope — one per meaningful module

Create an AGENTS.md at the root of a module, package, or feature that owns a real body of knowledge. Examples include a service, a bounded domain package, a frontend feature, a design-system package, and a store module. Don't create one for a leaf folder, a single-file utility directory, or a folder that exists for file organization alone.

Many thin AGENTS.md files repeat the over-subdivision problem, because they go out of date and teach readers to ignore them. When you are unsure, move the documentation up to the nearest meaningful module root.

### Required contents, in order

1. **What this module is and the problem it solves.** Write one or two sentences on what it does and why it exists. Skip how it works. Everything below is easier to follow once the reader has this model.
2. **Files to know and the responsibility each owns.** Give a short annotated list of only the files a new agent must understand to work here. State the responsibility each file owns. The implementation behind it belongs in the code.
3. **Non-obvious design constraints.** List the business, product, regulatory, or external constraints that force non-obvious decisions. When the code looks awkward because an outside requirement made it so, the reason goes here. Code and comments record the mechanics, and this file records the outside reason that forced them.
4. **Cross-module decisions.** Any design decision that touches several modules and can't be encapsulated in one of them is recorded here once. Affected sites get a one-line pointer comment (`// see "Event ordering" in AGENTS.md`). A copy of the explanation at each site drifts out of sync and gives no signal that it has.
5. **Extension rules and invariants.** State where new files belong, the conventions that must hold, the patterns to match, and which upstream or downstream modules a change here affects. Keep it to rules and pointers.

### Stay abstract on purpose

Describe purpose, rationale, constraints, and structure, and keep implementation mechanics out, because abstract documentation stays accurate through code changes. Detail that tracks the code belongs in code comments, where it's next to the thing it describes and gets updated when that code changes. The more abstract this content is, the longer it stays accurate.

### No duplication

Reference interface comments and let them describe the behavior. Link external specs and let them stay authoritative. State each cross-module decision once here and point to it from affected code. Duplicated documentation does the same harm as duplicated logic and more harm than absent documentation. Copies go out of date, and nothing tells the reader that the copy they are reading is stale.

### Maintenance

Update AGENTS.md whenever a structural change makes it wrong: responsibility moves, a file's job changes, a cross-module dependency is added or removed, a constraint changes. A stale file that readers treat as authoritative misleads them. If you can't keep a section accurate at its current detail level, make it shorter and more abstract. Detailed text that no longer holds misleads every reader who trusts it.

### AGENTS.md red flags

- An AGENTS.md in a trivial or leaf folder is over-subdivision, so move it up to the nearest meaningful module root.
- The file describes implementation mechanics, so it will go out of date. Rewrite it at a more abstract level.
- A cross-module reason is copied into the code at each site, which is duplication.
- A structural change shipped, and nobody updated the AGENTS.md it made wrong.
- The file documents behavior that belongs in an interface or field comment.

---

## README.md — for humans using or maintaining this module

Write a README.md for the human reading the code, and write AGENTS.md for the agent writing the code. A README says what this module does, why it exists, and what a caller needs to know before calling it.

README.md files are sparse by design, and most modules don't need one. Create one when:

- The module has a public API that humans call directly.
- The module's purpose is non-obvious from its name and structure.
- There are meaningful decisions about how to use it correctly: initialization order, required configuration, known gotchas that the API doesn't protect against.
- It's a package, library, service, or standalone feature that a human will need to orient to from scratch.

Don't create one for a leaf utility, an internal helper, or anything not meant to be consumed outside its immediate author.

### Required contents

1. **What this is.** Write one or two sentences on what problem it solves and who it's for.
2. **How to use it.** Give the minimal working example, and show the common case first. Don't put environment setup ahead of it.
3. **Concepts a caller needs.** List the abstractions a caller works with to use the module correctly, and leave implementation details out.
4. **Public API reference** (if not self-evident from the code). Cover only the public API. When possible, link to generated docs so the single source stays current. If the interface itself splits common calls from advanced or rarely used ones, mirror that split here. Don't flatten a tiered API into one list.
5. **Known constraints or gotchas.** List what will break for a user who doesn't know it, such as ordering requirements, required environment, and edge cases the API doesn't protect against.

### What README.md is not

- A tutorial on internals. Those belong in AGENTS.md or code comments.
- A changelog or version history.
- A repetition of interface comments. Link to them, and don't copy them.
- A place for implementation rationale, which is AGENTS.md's job.

### README.md maintenance

Update the README.md when the public API changes or a new constraint is added. Also update it when a user reports confusion that a good README.md would have prevented. A README.md describing an API that no longer exists is worse than no README.md.

---

## How the two files fit together

|                        | AGENTS.md                                   | README.md                                      |
|------------------------|---------------------------------------------|------------------------------------------------|
| **Audience**           | Agents writing code here                    | Humans using or maintaining the module         |
| **Job**                | Mental model, rationale, cross-module decisions | How to think about and use the module      |
| **Level**              | Structure, constraints, invariants          | Public API, concepts, gotchas                  |
| **When to create**     | Every meaningful module                     | Only when humans need orientation              |
| **Maintenance trigger**| Any structural change                       | Any public API change                          |

## Brownfield Work

When work touches an existing meaningful module, check whether the nearest module root already has an AGENTS.md. If it does not, offer to create one with only the facts learned from the current change. If responsibility moves, a public API changes, or a cross-module rule appears, update the nearest AGENTS.md when it is in scope. Otherwise offer that update as the next local step. Keep the offer small and concrete, tied to the module you just inspected.

## Compliance check

Before calling a docs change done, run both red-flag lists against the file you
wrote and name any entry that fired, because a red-flag list that nobody
runs catches nothing.

See `references/examples.md` for backend and frontend examples of both files.
