---
name: toby-swd-clarity
description: >-
  Make the code readable to whoever inherits it. Use it for naming,
  comments, docstrings, conventions, and control flow a reader trips on,
  inside the code being touched. It leaves already-clear surrounding code
  alone. Skip it for module documentation files, which `toby-swd-docs` owns,
  and for the design of a contract, which `toby-swd-interfaces` owns.
---

# Toby SWD Clarity

Code is read far more than it is written. Names, comments, and consistency compound across every future read: every debug session, every onboarding, every agent that touches this code next. Bad clarity outlasts every other kind of complexity. It slows everything downstream and never shows up in a diff as the problem.

**"Good code is self-documenting" is false.** Correct that before you start. Only signatures can be expressed in code. The behavior, side effects, units, invariants, and reasons a reader needs live in the designer's head and have no representation in the code itself. Good names reduce the need for comments, but they never remove it. Treat comments as the mechanism by which abstraction is delivered. They carry the units, invariants, and reasons that have no home in the code.

## Naming

Test every name by guessability. Show the name alone, with no declaration, documentation, or surrounding code. A developer should guess what it holds or does, and what it does not. Pick the few words that capture what matters, and omit the rest. Treat the name as an abstraction.

Scale specificity to scope. A variable whose entire span of use fits in a few visible lines can be terse (a loop index `i`). A variable across a large span, a field, an argument, or anything exported needs a precise name. Over-specific is also a defect. An argument named `selection` for a method that works on any range misleads.

Generic names (`data`, `value`, `result`, `status`, `flag`, `count`) are a smell when the scope is non-trivial. Acceptable only when the meaning is visible at a glance.

Use names consistently. One name, one purpose, never that name for a second purpose. Keep the purpose narrow enough that every variable carrying the name behaves the same. When you need several of the same kind, keep the common root and add a distinguishing prefix (`srcBlock`, `dstBlock`). Boolean names read as predicates (`cursorVisible`, `isReady`, `hasChildren`). Every word must add information: drop redundant type or class-name words (`fileObject` → `file`), no Hungarian notation.

**Hard-to-name red flag**: if no precise, intuitive, not-too-long name emerges after real effort, the thing being named probably has an unclear or mixed purpose. That is a design signal, so split or rethink it. Do not settle for a vague name. The signal is about the operation as a whole. A single dense expression that computes one nameable result is one abstraction, even when its internal steps have no good individual names.

## Comments

Four kinds, each with its own home.

| Kind | Sits on | Carries |
|---|---|---|
| Interface | the entry point | what a caller needs, with no internals |
| Data-structure member | a non-trivial field | units, what null means, bounds, ownership |
| Implementation intuition | a non-obvious block | why it does what it does |
| Cross-module | one discoverable place | a decision spanning modules, stated once and pointed to |

Keep implementation detail out of the interface.

An **interface comment** describes the abstraction: behavior, arguments, return value, side effects, exceptions, and caller preconditions. If it has to describe internals to be complete, the module is shallow, and that is a redesign signal. Reach for the design, since better wording won't fix a leaky abstraction. Write interface comments before the implementation, because they are a design tool.

Comment at a different level than the code. A comment pitched at the code's own level just restates it and rots in place:

- **Precision (lower level)**, on fields, arguments, return values: add what the name and type cannot say — units, inclusive or exclusive bounds, what null or empty means, ownership, and invariants. Fields with non-obvious units, ownership, null meaning, bounds, side effects, or invariants get comments. Trivial fields with names and types that already say the whole contract can stay quiet.
- **Intuition (higher level)**, inside code: why this exists, what a block accomplishes conceptually, why a non-obvious approach was chosen, how a reader got here. For a bug-fix whose purpose isn't obvious, say why and reference the tracker.

Delete comments whose content is already obvious from the adjacent code, including comments that just restate the name. Document each decision once, in the most obvious place. Cross-reference a called method from its call site. Re-explaining it there gives you two copies that drift apart. For a design decision that spans modules, put it in one discoverable central place and point to it from the affected sites.

Leave these uncommented: operations the code already shows (`i++ // increment i`), restatements of the name, commented-out code, and anything the type already proves. Git holds the change history.

Logs and diagnostics are a surface too. Keep secrets, credentials, tokens, and personal data out of them, and out of source. Naming a field sensitive in a comment is worth more than the value in a log line.

## Consistency

Similar things done the same way, dissimilar things done differently. Both halves carry weight. Before introducing any convention (naming, structure, error handling, style, test layout), inspect the local file and project and mimic what's already there. Reuse exact names already established for a concept.

Factor code together only when the instances share the same knowledge, so a change to one should change all. Blocks that look alike but answer to different reasons are separate decisions that happen to share text. Merging them couples things that should move apart, and the next change tears them back out.

Don't "improve" an existing convention casually. Before introducing an inconsistency, both must hold. You have information that was not available when the convention was set. The new approach is enough better to justify converting every existing use. If you change it, leave no instance of the old convention behind. Half-adopted conventions are worse than either option alone, because they destroy a reader's ability to draw safe conclusions from a familiar-looking pattern.

## Obviousness

After writing code, read it as a developer seeing it cold. Ask whether their first guess about behavior is correct. Obviousness lives in the reader's head, and self-assessment is unreliable. Take a reviewer's report of confusion over your own read of the code, however clear it looks to you. When no reviewer is available, simulate a specific developer who is unfamiliar with this code.

Recurring failure modes:

- **Generic containers**: returning a tuple/pair/untyped object where the caller reads `.getKey()` or `[0]` with no semantic label. Define a named type with named fields instead.
- **Declared type differing from the real one**: a value typed as a broad supertype but actually a specific subtype with different behavior; match them. This is the Liskov substitution test. A value under a type must behave the way every user of that type expects. Frontend form: a component that takes another's prop contract and then drops or reinterprets a prop, so code that swapped the two would break.
- **Behavior that defies convention**: a constructor that spawns threads, a method that mutates unrelated state, an effect that runs on a non-obvious trigger. Document the surprise at the exact point a linear reader meets it, and again where they would otherwise act on the wrong assumption.
- **Hidden control flow**: event-driven invocation, callbacks, effects. State in the handler's own comment when and why it is invoked, since the call site isn't visible from the handler.

The fix for unavoidable surprise is a comment where the reader will hit it. Use whitespace to expose structure: blank lines between phases, spacing within dense expressions. A blank line followed by a one-line comment makes phases scannable.

## Proportionality

The cheap checks apply on every edit: naming, comment presence, obvious-on-read. The expensive ones are converting every instance of a convention and adding a design-notes file. Reserve those for code that is exported, crossed by several callers, or costly to change later.

## Brownfield Work

For existing code, first learn the local vocabulary and comment style. Improve unclear names, comments, and obvious-on-read structure in the code already being touched when the cleanup is local. If the same concept is named several ways across the codebase, offer a follow-up rename or convention cleanup. Changing one island leaves the rest drifted and the reader worse off than before. If the clarity issue exposes a module rule agents should remember, offer an AGENTS.md note at the meaningful module root.

## Red flags

Before calling a clarity pass done, check the code you touched against every red flag below.

- **Vague name**: broad enough to refer to many things.
- **Hard to pick a name**: signals unclear or mixed purpose.
- **Name reused for two purposes**: the classic source of silent bugs.
- **Comment repeats the code**: no information beyond the declaration.
- **Implementation detail in an interface comment**: shallow module.
- **Missing precision**: a field or argument with no units, bounds, or null-meaning where those aren't obvious.
- **Self-documenting-code assumption**: shipping non-trivial code with no interface or field comments.
- **Half-adopted convention**: same concept done two ways in one codebase.
- **Nonobvious code**: behavior not graspable on a quick read.

See `references/examples.md` for worked backend and frontend cases.
