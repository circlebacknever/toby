---
name: toby-swd-docs
description: >-
  Two artifacts live in every meaningful module: AGENTS.md (for agents writing
  code here) and README.md (for humans using or maintaining this module). Use
  this skill when a task changes module structure, public APIs, cross-module
  decisions, extension rules, or human-facing module usage. Check existing docs
  for accuracy before editing them. One of each per meaningful module root,
  never per folder.
---

# Toby SWD Docs

A module carries two categories of information that can't live in the code itself. The code says *what*. These files say *why*, *who this is for*, and *how to think about it*.

Two artifacts. Different audiences. Different jobs. Don't conflate them.

---

## AGENTS.md — for agents writing code here

An AGENTS.md is the single discoverable entry point for an agent working in this module. Its job is to carry what the code can't: the conceptual model, the reasons behind non-obvious decisions, and the design decisions that span modules.

An agent without an AGENTS.md is operating blind. It doesn't know what it doesn't know, and finds out only when something breaks. Write this file like you are briefing someone smart who is meeting this code cold and has no time for surprises.

### Scope — one per meaningful module, not per folder

Create an AGENTS.md at the root of a module, package, or feature that owns a real body of knowledge: a service, a bounded domain package, a frontend feature, a design-system package, a store module. Don't create one for a leaf folder, a single-file utility directory, or a folder that exists for file organization alone.

Many thin AGENTS.md files reproduce the over-subdivision problem — they rot, they drift, and they train readers to ignore them. When in doubt, push the documentation up to the nearest meaningful module root.

### Required contents, in order

1. **What this module is and the problem it solves.** One or two sentences: what it does and why it exists, not how it works. Everything below lands easier once the reader holds this model.
2. **Key files and the responsibility each owns.** A short annotated list of only the files a new agent must understand to work here. State the responsibility, never the implementation.
3. **Non-obvious design constraints.** Business, product, regulatory, or external constraints that force non-obvious decisions. When the code looks awkward because an outside requirement made it so, the reason lives here — not in the code, not in a comment.
4. **Cross-module decisions.** Any design decision that touches several modules and can't be encapsulated in one of them is recorded here once. Affected sites get a one-line pointer comment (`// see "Event ordering" in AGENTS.md`), never a copy of the explanation.
5. **Extension rules and invariants.** Where new files belong, conventions that must hold, patterns to match, which upstream or downstream modules a change here affects. Rules and pointers; not a tutorial.

### Stay abstract on purpose

Describe purpose, rationale, constraints, and structure — never implementation mechanics. Abstract documentation survives code changes; detail that tracks the code belongs in code comments, where it's next to the thing it describes and gets updated when that code changes. The further this content sits from the code, the longer it stays accurate.

### No duplication

Reference interface comments rather than restating behavior. Link external specs rather than paraphrasing them. State each cross-module decision once here and point to it from affected code. Duplicated documentation is as dangerous as duplicated logic, and worse than absent documentation — copies drift with no signal to the reader that what they're reading is stale.

### Maintenance

Update AGENTS.md whenever a structural change makes it wrong: responsibility moves, a key file's job changes, a cross-module dependency is added or removed, a constraint changes. A stale authoritative file actively misleads. If you can't keep a section accurate at its current detail level, make it shorter and more abstract rather than leaving detailed text that no longer holds.

### AGENTS.md red flags

- AGENTS.md in a trivial or leaf folder — over-subdivision; push it up.
- The file describes implementation mechanics — it will rot; raise the level.
- A cross-module reason copied into code instead of pointed to — duplication.
- A structural change shipped without updating an AGENTS.md it invalidated.
- Behavior documented here that belongs in an interface or field comment.

---

## README.md — for humans using or maintaining this module

A README.md is for the human reading the code, not the agent writing it. Its job is to explain how to think about this module and how to work with its public surface — what it does, why it exists, and what someone needs to know before touching it or calling it.

README.md files are sparse by design. Most modules don't need one. Create one when:

- The module has a public API that humans call directly.
- The module's purpose is non-obvious from its name and structure.
- There are meaningful decisions about how to use it correctly: initialization order, required configuration, known gotchas that the API doesn't protect against.
- It's a package, library, service, or standalone feature that a human will need to orient to from scratch.

Don't create one for a leaf utility, an internal helper, or anything not meant to be consumed outside its immediate author.

### Required contents

1. **What this is.** One or two sentences: what problem it solves and who it's for.
2. **How to use it.** The minimal working example. Show the common case first. Don't bury it under environment setup.
3. **Key concepts.** The mental model a user must hold to use this correctly — not implementation details, but the abstractions a caller operates with.
4. **Public API reference** (if not self-evident from the code). Only the public surface. Link to generated docs rather than duplicate them when possible.
5. **Known constraints or gotchas.** Things that will bite a user who doesn't know them: ordering requirements, required environment, edge cases the API doesn't protect against.

### What README.md is not

- A tutorial on internals. Those belong in AGENTS.md or code comments.
- A changelog or version history.
- A repetition of interface comments. Link to them; don't copy.
- A place for implementation rationale — that is AGENTS.md's job.

### README.md maintenance

Update when the public API changes, when a new constraint is added, or when a user reports confusion that a good README.md would have prevented. A README.md describing a defunct API is worse than no README.md.

---

## How the two files fit together

|                        | AGENTS.md                                   | README.md                                      |
|------------------------|---------------------------------------------|------------------------------------------------|
| **Audience**           | Agents writing code here                    | Humans using or maintaining the module         |
| **Job**                | Mental model, rationale, cross-module decisions | How to think about and use the module      |
| **Level**              | Structure, constraints, invariants          | Public API, key concepts, gotchas              |
| **When to create**     | Every meaningful module                     | Only when humans need orientation              |
| **Maintenance trigger**| Any structural change                       | Any public API change                          |

## Brownfield Work

When work touches an existing meaningful module, check whether the nearest module root already has an AGENTS.md. If it does not, offer to create one with only the facts learned from the current change. If responsibility moves, a public API changes, or a cross-module rule appears, update the nearest AGENTS.md when it is in scope; otherwise offer that update as the next local step. Keep the offer small and concrete, tied to the module you just inspected.

See `references/examples.md` for backend and frontend examples of both files.
