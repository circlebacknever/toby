---
name: toby-swd-clarity
description: >-
  Code communicates — to agents, to future maintainers, to whoever inherits
  this. Use this skill when naming, comments, conventions, exported contracts,
  confusing control flow, or obvious-on-read structure are part of a code
  change. It is a focused clarity pass for backend, frontend, scripts, and
  configs, not a reason to rewrite already-clear surrounding code.
---

# Toby SWD Clarity

Code is read far more than it is written. The decisions you make about names, comments, and consistency compound across every future read — every debug session, every onboarding, every agent that touches this code next. Bad clarity is one of the most durable forms of complexity because it slows everything downstream while never appearing in a diff as the problem.

Correct this before you start: **"Good code is self-documenting" is false.** Only signatures can be expressed in code; the behavior, side effects, units, invariants, and reasons a reader needs live in the designer's head and have no representation in the code itself. Good names reduce the need for comments; they never remove it. Treat comments as the mechanism by which abstraction is delivered, not as an apology for unclear code.

## Naming

Test every name by guessability: a developer who sees this name alone, with no declaration, documentation, or surrounding code, should guess what it holds or does — and what it is not. Pick the few words that capture what matters; omit the rest. A name is an abstraction.

Scale specificity to scope. A variable whose entire span of use fits in a few visible lines can be terse (a loop index `i`). A variable across a large span, a field, an argument, or anything exported needs a precise name. Over-specific is also a defect — an argument named `selection` for a method that works on any range misleads.

Generic names (`data`, `value`, `result`, `status`, `flag`, `count`) are a smell when the scope is non-trivial. Acceptable only when the meaning is visible at a glance.

Use names consistently: one name for one purpose, never that name for a second purpose, and the purpose narrow enough that every variable with the name behaves the same. When you need several of the same kind, keep the common root and add a distinguishing prefix (`srcBlock`, `dstBlock`). Boolean names read as predicates (`cursorVisible`, `isReady`, `hasChildren`). Every word must add information: drop redundant type or class-name words (`fileObject` → `file`), no Hungarian notation.

**Hard-to-name red flag**: if no precise, intuitive, not-too-long name emerges after real effort, the thing being named probably has an unclear or mixed purpose. That is a design signal — split or rethink it, don't settle for a vague name.

## Comments

Separate interface comments from implementation comments; keep implementation detail out of the interface.

An **interface comment** describes behavior, arguments, return value, side effects, exceptions, and caller preconditions — the abstraction. If it has to describe internals to be complete, the module is shallow; that is a redesign signal, not a documentation problem. Write interface comments before the implementation; they are a design tool.

Comment at a different level than the code, never the same level:

- **Precision (lower level)**, on fields, arguments, return values: add what the name and type cannot say — units, inclusive or exclusive bounds, what null or empty means, ownership, and invariants. Fields with non-obvious units, ownership, null meaning, bounds, side effects, or invariants get comments. Trivial fields with names and types that already say the whole contract can stay quiet.
- **Intuition (higher level)**, inside code: why this exists, what a block accomplishes conceptually, why a non-obvious approach was chosen, how a reader got here. For a bug-fix whose purpose isn't obvious, say why and reference the tracker.

Delete comments whose content is already obvious from the adjacent code, including comments that just restate the name. Document each decision once, in the most obvious place. Don't re-explain a called method at its call site — cross-reference instead. For a design decision that spans modules, put it in one discoverable central place and point to it from the affected sites.

## Consistency

Similar things done the same way; dissimilar things done differently — both halves carry weight. Before introducing any convention (naming, structure, error handling, style, test layout), inspect the local file and project and mimic what's already there. Reuse exact names already established for a concept.

Don't "improve" an existing convention casually. Before introducing an inconsistency, both must be true: you have significant new information that wasn't available when the convention was set, and the new approach is enough better to justify converting every existing use. If you change it, leave no instance of the old convention behind. Half-adopted conventions are worse than either option alone — they destroy a reader's ability to draw safe conclusions from a familiar-looking pattern.

## Obviousness

After writing code, read it as a developer seeing it cold. Ask whether their first guess about behavior is correct. Obviousness lives in the reader's head, and self-assessment is unreliable — if a reviewer says it's not obvious, it isn't, regardless of how clear it looks to you. When no reviewer is available, simulate a specific developer who is unfamiliar with this code.

Recurring failure modes:

- **Generic containers**: returning a tuple/pair/untyped object where the caller reads `.getKey()` or `[0]` with no semantic label. Define a named type with named fields instead.
- **Declared type differing from the real one**: a value typed as a broad supertype but actually a specific subtype with different behavior; match them.
- **Behavior that defies convention**: a constructor that spawns threads, a method that mutates unrelated state, an effect that runs on a non-obvious trigger. Document the surprise at the exact point a linear reader meets it, and again where they would otherwise act on the wrong assumption.
- **Hidden control flow**: event-driven invocation, callbacks, effects. State in the handler's own comment when and why it is invoked, since the call site isn't visible from the handler.

The fix for unavoidable surprise is a comment where the reader will hit it. Use whitespace to expose structure: blank lines between phases, spacing within dense expressions. A blank line followed by a one-line comment makes phases scannable.

## Proportionality

The cheap checks — naming, comment presence, obvious-on-read — apply on every edit. The expensive moves — converting every instance of a convention, adding a design-notes file — are reserved for code that is exported, crossed by several callers, or costly to change later.

## Brownfield Work

For existing code, first learn the local vocabulary and comment style. Improve unclear names, comments, and obvious-on-read structure in the code already being touched when the cleanup is local. If the same concept is named several ways across the codebase, offer a follow-up rename or convention cleanup instead of changing one island and leaving drift behind. If the clarity issue exposes a module rule agents should remember, offer an AGENTS.md note at the meaningful module root.

## Red flags

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
