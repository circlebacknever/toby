---
name: toby-swd-clarity
description: >-
  Make the code readable to whoever maintains it next. Use it for naming,
  comments, docstrings, conventions, and control flow that confuses a reader,
  inside the code being touched. It leaves already-clear surrounding code
  alone. Skip it when the user wants a clear or concise explanation in chat,
  which `toby-explain` is for. This skill changes code and writes no prose for
  the reader. Skip it for module documentation files, which `toby-swd-docs`
  is for, and for the design of a contract, which `toby-swd-interfaces` is for.
---

# Toby SWD Clarity

People read code far more often than they write it. Each name, comment, and convention affects every later read, including each debug session, each onboarding, and each agent that touches this code next. Unclear code outlasts every other kind of complexity, because it slows every later task, but a diff never shows it as the problem.

**"Good code is self-documenting" is false.** Correct that belief before you start. Only signatures can be expressed in code. The behavior, side effects, units, invariants, and reasons a reader needs are known only to the designer. The code itself does not represent them. Good names reduce the need for comments, but they never remove it. Treat comments as the way a module states its abstraction. They record the units, invariants, and reasons that the code cannot express.

## Naming

Test every name by whether a reader can guess its meaning. Show the name alone, with no declaration, documentation, or surrounding code. A developer should guess what it holds or does, and what it does not. Pick the few words that capture what matters, and omit the rest. Treat the name as an abstraction.

Make a name more specific as its scope grows. A variable whose entire span of use fits in a few visible lines can be terse (a loop index `i`). A variable across a large span, a field, an argument, or anything exported needs a precise name. An over-specific name is also a defect. An argument named `selection` for a method that works on any range misleads.

Generic names (`data`, `value`, `result`, `status`, `flag`, `count`) are a smell when the scope is non-trivial. They are acceptable only when the meaning is visible at a glance.

Use names consistently, so each name has one purpose. Keep the purpose narrow enough that every variable with the name behaves the same. When you need several of the same kind, keep the common root and add a distinguishing prefix (`srcBlock`, `dstBlock`). Boolean names read as predicates (`cursorVisible`, `isReady`, `hasChildren`). Every word in a name must add information. Drop redundant type or class-name words (`fileObject` → `file`), and do not use Hungarian notation.

**Hard-to-name red flag**: if you cannot find a precise, intuitive, not-too-long name after real effort, the thing being named probably has an unclear or mixed purpose. A name that is hard to pick is a design signal, so split or rethink the thing being named. Do not settle for a vague name. The signal is about the operation as a whole. A single dense expression that computes one nameable result is one abstraction, even when its internal steps have no good individual names.

## Comments

Each kind of comment in the table below belongs in its own place.

| Kind | Where it goes | What it says |
|---|---|---|
| Interface | the entry point | what a caller needs, with no internals |
| Data-structure member | a non-trivial field | units, what null means, bounds, ownership |
| Implementation intuition | a non-obvious block | why it does what it does |
| Cross-module | one discoverable place | a decision spanning modules, stated once and pointed to |

Keep implementation detail out of the interface.

Write every comment as whole sentences that pass the five tests in the operating guide. A docstring's first line may start with its verb, as in `Return the trimmed text.` A field comment is a whole sentence too: `// This is null while the request is loading or after it fails.`

An **interface comment** describes the abstraction: behavior, arguments, return value, side effects, exceptions, and caller preconditions. If it has to describe internals to be complete, the module is shallow. A shallow module is a signal to redesign it. Change the design, since better wording won't fix a leaky abstraction. Write interface comments before the implementation, because they are a design tool.

Comment at a different level than the code. A comment written at the code's own level restates the code and becomes wrong when the code changes. Use one of these two levels:

- **Precision (lower level)**, on fields, arguments, return values: add what the name and type cannot say, such as units, inclusive or exclusive bounds, what null or empty means, ownership, and invariants. Fields with non-obvious units, ownership, null meaning, bounds, side effects, or invariants get comments. Trivial fields with names and types that already say the whole contract need no comment.
- **Intuition (higher level)**, inside code: why this exists, what a block accomplishes conceptually, why a non-obvious approach was chosen, how a reader got here. For a bug-fix whose purpose isn't obvious, say why and reference the tracker.

Delete comments whose content is already obvious from the adjacent code, including comments that just restate the name. Document each decision once, in the most obvious place. Cross-reference a called method from its call site. Re-explaining it there gives you two copies, and a later edit to one leaves the other wrong. For a design decision that spans modules, put it in one discoverable central place and point to it from the affected sites.

Leave these uncommented: operations the code already shows (`i++ // increment i`), restatements of the name, commented-out code, and anything the type already proves. Git holds the change history.

Apply the same care to logs and diagnostics. Keep secrets, credentials, tokens, and personal data out of them, and out of source. A comment that marks a field as sensitive is more useful than the field's value in a log line.

## Consistency

Do similar things the same way, and do dissimilar things differently. Follow both halves of that rule. Before introducing any convention (naming, structure, error handling, style, test layout), inspect the local file and project and mimic what's already there. Reuse exact names already established for a concept.

Factor code together only when the instances share the same knowledge, so a change to one should change all. Blocks that look alike but exist for different reasons are separate decisions that happen to share text. Merging them ties together code that should change independently, and the next change has to split the blocks apart again.

Don't change an existing convention casually. Introduce an inconsistency only when you have information that was not available when the convention was set. The new approach must also be enough better to justify converting every existing use. If you change it, leave no instance of the old convention behind. Half-adopted conventions are worse than either option alone, because a reader can no longer draw safe conclusions from a familiar-looking pattern.

## Obviousness

After writing code, read it as a developer who is seeing it for the first time. Ask whether their first guess about behavior is correct. Whether code is obvious depends on the reader. Self-assessment is unreliable. Take a reviewer's report of confusion over your own read of the code, however clear it looks to you. When no reviewer is available, simulate a specific developer who is unfamiliar with this code.

Watch for these recurring failures:

- **Generic containers**: returning a tuple/pair/untyped object where the caller reads `.getKey()` or `[0]` with no semantic label. Define a named type with named fields instead.
- **Declared type differing from the real one**: a value is typed as a broad supertype but is a specific subtype with different behavior, so make the two types match. The Liskov substitution test covers this mismatch, because a value under a type must behave the way every user of that type expects. In frontend code, a component takes another component's prop contract and then drops or reinterprets a prop, so code that swapped the two would break.
- **Behavior that defies convention**: a constructor that spawns threads, a method that mutates unrelated state, an effect that runs on a non-obvious trigger. Document the surprise at the exact point a linear reader meets it, and again where they would otherwise act on the wrong assumption.
- **Hidden control flow**: event-driven invocation, callbacks, effects. State in the handler's own comment when and why it is invoked, since the call site isn't visible from the handler.

The fix for unavoidable surprise is a comment where the reader will reach it. Use whitespace to expose structure: blank lines between phases, spacing within dense expressions. A blank line followed by a one-line comment makes phases scannable.

## Proportionality

The cheap checks apply on every edit: naming, comment presence, obvious-on-read. The expensive ones are converting every instance of a convention and adding a design-notes file. Reserve those for code that is exported, called from several places, or costly to change later.

## Brownfield Work

For existing code, first learn the local vocabulary and comment style. Improve unclear names, comments, and obvious-on-read structure in the code already being touched when the cleanup is local. If the same concept is named several ways across the codebase, offer a follow-up rename or convention cleanup. Renaming the concept in one place leaves the other names unchanged and the reader worse off than before. If the clarity issue exposes a module rule agents should remember, offer an AGENTS.md note at the meaningful module root.

## Red flags

Before calling a clarity pass done, check the code you touched against every red flag below.

- **Vague name**: broad enough to refer to many things.
- **Hard to pick a name**: signals unclear or mixed purpose.
- **Name reused for two purposes**: the classic source of silent bugs.
- **Comment repeats the code**: no information beyond the declaration.
- **Implementation detail in an interface comment**: a sign of a shallow module.
- **Missing precision**: a field or argument with no units, bounds, or null-meaning where those aren't obvious.
- **Self-documenting-code assumption**: shipping non-trivial code with no interface or field comments.
- **Half-adopted convention**: same concept done two ways in one codebase.
- **Nonobvious code**: behavior not graspable on a quick read.

See `references/examples.md` for worked backend and frontend cases.
