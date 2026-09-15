# Smell Catalog

Under the main skill, a change counts only when it makes a literal countable reduction, such as fewer lines, branches, or duplicated blocks. Its Out of scope section excludes anything that moves code between modules or changes a signature. So the skill says nothing about a design smell that needs a fix at a module boundary. Fixing that smell isn't the skill's job. The skill also has no rule to report it.

This file lists those smells. Each entry below is marked Fix here or Flag, don't fix.

- **Fix here** means the fix stays local and gives a countable reduction, like anything else in What to look for. Do it in the same pass.
- **Flag, don't fix** means the fix crosses a module boundary or changes a public signature. Name the smell, the file:line, and the skill to route it to in the final response. Leave the code alone.

## Fix here

- **Comment invalidated at a distance.** A change makes a comment somewhere else in the codebase wrong. The comment can be a caller's documented assumption, an invariant note at a distant call site, or a doc comment describing changed behavior. The entry applies when the diff changes a function's behavior, return type, error conditions, or an invariant. A search for callers or the described behavior must also find a comment that still states the old one. Fix here: correct the comment to match the new behavior. The edit is one line inside one module. Exception: only flag a comment when you can name its file:line and the exact clause the diff makes false. "Something elsewhere might describe this" isn't checkable, so drop that finding.

- **Dead function or class.** A function, method, or class compiles and could run, but it has no callers anymore. The entry applies when the diff removes its last caller, or when a repo-wide grep for the symbol name finds only its own definition. Fix here: delete it. Only its own definition names it in the repo, so removing it changes no signature or caller. The only change is fewer lines. Exception: the entry does not apply to anything exported or public that code outside this repo might consume. It also does not apply to anything reached through reflection, dependency injection, dynamic dispatch, or a test-only harness. Before you delete it, grep the identifier as a string and confirm its export status.

- **Magic number or string.** An unexplained literal is used in the logic, such as in a comparison, a multiplier, or a branch condition. It represents a concept the reader has to guess at. The entry applies when a changed line checks against, multiplies by, or branches on a bare literal with no obvious meaning from the surrounding lines. It also applies when the same literal appears at two or more sites for the same concept. Fix here: name it. One constant, declared once, gives the literal a meaning and removes the repeated copies. Exception: the entry does not apply to a self-evident value in a narrow scope, such as a loop's 0 or -1 or an HTTP status checked once inline. A literal is a finding when a reader could not explain it on first reading, or when it repeats where a change to one should change all.

- **Stale comment beside changed code.** A comment right next to code the diff just changed still describes what the code used to do. The entry applies when a changed line or block behaves differently now. The comment immediately above or beside it, visible in the same hunk, must also still state the old version. Fix here: rewrite the comment in the same hunk to match what the code does now, at roughly the same line count. Exception: the entry does not apply to a comment describing something the diff left alone, such as an invariant that still holds or a unit that's still correct. Flag it only when the diff visibly changes the exact thing the adjacent comment claims.

## Flag, don't fix

Each of these needs a change this skill's Out of scope note already excludes: a signature, a public return type, or module responsibilities. Name the entry, the file:line, and the skill listed, then leave the code alone.

`toby-code-review`'s `references/smells.md` has the full entry for every name below. Each entry there gives the definition, the Fires-when criterion you quote against the code, and the exception that makes it a non-finding. Read it there before flagging. Keeping a second copy here is how the accessors entry ended up in four files with three wordings.

| Entry | Route to | Fires when |
|---|---|---|
| Long parameter list / data clump | `toby-swd-interfaces` | a changed or new signature has enough parameters that a caller has to check the declaration to get the order right, or the same two or three parameters appear together more than once in the diff |
| Output argument | `toby-swd-interfaces` | the diff adds or changes a function that writes into a parameter it received as its way of producing a result, where a return value would say the same thing |
| Flag / selector argument | `toby-swd-interfaces` | a changed or new function branches on a bool or enum parameter near the top of its body into substantially different code paths, and the parameter is used only to choose which path runs |
| Message chain | `toby-swd-interfaces` | a changed line chains three or more navigations through different objects' accessors to reach a final value or call |
| Primitive obsession | `toby-swd-interfaces` | a new field or parameter representing a recognizable domain concept is typed as a raw primitive, and the same parsing or validation for that concept already appears at two or more sites |
| Accessors as the public surface | `toby-swd-interfaces` | a new or changed class's public methods are mostly getters and setters for its own fields, with no operation that names intent |
| Speculative generality | `toby-swd-interfaces` | a new parameter or option has no current caller using anything but its default, and grepping for callers finds no concretely named near-future use either |
| Artificial coupling | `toby-swd-modules` | the diff adds a general-purpose constant or helper inside a specific, unrelated class, and that class's own purpose does not explain why the constant or helper is in it |
| Feature envy | `toby-swd-modules` | a changed method's body is mostly a chain of getters and fields pulled from one other object, with little use of its own class's state, and the method's work could move to that other object |
| Divergent change | `toby-swd-modules` | the diff states one intent, but the edits inside one file or class serve visibly unrelated purposes, like a pricing-rule tweak and a display-copy tweak |
| Shotgun surgery | `toby-swd-modules` | the diff makes small, similar edits across many files that all encode one underlying decision. Examples are a field added to N structs or a case added to N switch statements |
| Shallow module | `toby-swd-modules` | explaining a new or changed module's parameters, methods, and required setup takes about as long as explaining its internals |
| Information leakage | `toby-swd-modules` | the diff touches two or more modules to express what is really one decision |
| Pass-through method | `toby-swd-modules` | a new or changed method's body is a single call to another method, passing the same arguments through unchanged |

Check the exceptions as closely as the criteria. An entry whose exception covers the code under review is not a finding. The exceptions appear only in the `toby-code-review` catalog.

## Smells left off this list on purpose

**Refused bequest** (a subclass that uses only part of what it inherits) doesn't get an entry. The part of this smell that a diff can show is a subclass overriding an inherited method to throw or no-op. `toby-swd-modules`' "Deep implementation-inheritance hierarchy" red flag already covers that half. Checking the rest of the definition means comparing the parent class's public methods against everything the subclass calls. That comparison means opening and reading an unrelated file end to end. A cleanup pass under this skill doesn't read a full file, so flag the override half under the existing red flag and stop there.

This list also leaves out four rules on purpose: a function-length limit, "comments are always failures," "duplication is evil," and "TDD mandates test-first". Each one contradicts a position that `toby-swd-modules`, `toby-swd-clarity`, or `toby-swd-interfaces` already states for this repo. Those skills hold that depth matters more than line count and that comments record what code can't say. They also hold that duplication is removed only when the copies share knowledge, and that interfaces come first in design. Adding any of them here would make this skill contradict the skills that were followed when the code was written.
