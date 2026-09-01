---
name: toby-swd-strategy
description: >-
  Every code change either invests in the system's future or borrows against it.
  Use this skill for non-trivial software engineering work: features, bug fixes
  with behavioral risk, refactors, public API or module-boundary changes, and
  edits where a quick patch may add special cases or hidden dependencies. Skip
  it for read-only investigation, tiny mechanical edits, formatting-only churn,
  and changes whose structure is already fixed by the surrounding code.
---

# Toby SWD Strategy

Write today's code knowing every future change inherits its structure. Most code in any system is written by extending what's already there. So the highest-yield point in software is whether the module boundary holds when the next change arrives.

An autonomous agent is especially prone to pure tactical execution. "Make the test pass" is such a tidy stopping signal that tactical programming feels like discipline. Do not treat it as discipline. Do not count a large volume of working code as progress when each piece adds a special case or a hidden dependency. That output moves the design backwards at speed.

The deliverable is a system whose design is at least as good after your change as before it. Target a design that survives the next change. Working code falls out of that.

## Before writing — design pass

For anything beyond a one-line change, don't implement the first idea.

- State the change in one sentence, including the obvious near-future variants ("today it's one provider; tomorrow there will be three").
- Sketch at least two structural approaches. They must differ in *where complexity lives* — which module owns the hard part, what the interface exposes, what callers must manage. Pick the one with the simplest caller-side interface, even if its insides are harder.
- Check the near-future variants against your design. If a likely next change would force callers to change or add a new special case, adjust now while it's cheap.
- If those variants are new cases picked by a tag or type, design the dispatch now. Use a lookup map when the case bodies are small, an interface with implementations when each case owns state. `toby-swd-modules` has the ladder. Greenfield builds it in; brownfield offers it as a scoped refactor.
- Proportionality: a real one-liner doesn't need an architecture review. The design pass scales to the size of the decision.

## While writing — pull complexity to the right place

A good module is deep: a simple interface over substantial work. The interface is the cost the module imposes on the rest of the system, and the implementation is the benefit. Skew that ratio heavily toward the implementation side.

Resist exposing internal mechanics, config knobs, or special cases just because they're the shortest path from where you are. Every parameter a caller must manage is overhead distributed across every future call site. Prefer computing a value internally over exporting a configuration parameter or throwing back to the caller.

Depth is the goal, and small functions serve it only when they deliver it. A split that creates two shallow units in place of one deep one is a loss, however tidy it looks. When the urge to shrink a function fights a deep module, the deep module wins.

## After writing — reactive investment

You are now inside this code with full context. This is the cheapest moment in the system's life to improve it, and it doesn't come back.

- If you patched *around* a design problem to make your change fit, stop and fix the design instead. A workaround that adds a special case, a flag, or a surprise dependency is debt you are choosing to take on with full awareness.
- Find one design imperfection in the code you touched: an obscure name, a leaky abstraction, a dead branch, a comment that lies, duplicated logic. Fix it when the cleanup is small, local, and directly supports the change. Otherwise report it as follow-up. Scope discipline is part of design, so do not wander into cleanup outside the code you touched.
- Keep cleanups scoped to code you're already in. Do not let a refactor sprawl across the codebase.

## The test for modifying existing code

Replace "what is the smallest edit that does what I need?" with:

> What structure would this code have if it had been designed from the start with this change already in mind?

Move the code toward that structure. Often the answer is "basically what's there, plus the new bit", so proceed. Sometimes it reveals the current design no longer fits. Then refactor first and add the change on top with no workaround. Decide deliberately. Do not default to the minimal diff, which rots a codebase one reasonable-looking commit at a time.

## Brownfield Work

On existing code, read the current shape before choosing a design. Identify the smallest local refactor that would make the requested change fit naturally. If that refactor is small, scoped to touched code, and lowers future cost, offer it with its cost and benefit before doing it. If it would expand the task, name the tradeoff and let the user choose between the refactor and the smaller tactical change.

## When the quick fix is the correct call

Take the tactical path when:

- A hard external deadline will not survive the extra time, and the cost is understood and accepted.
- The sound refactor would change an interface other teams or callers depend on, and coordinating that is out of scope.
- The sound version requires information you don't have and can't get.

"This is faster" alone is not on the list. When you take the quick path for a real reason, make the debt visible. Leave a comment naming what the sound design would be and why you skipped it. Never leave that debt unlabeled, because the next person cannot see it to pay it down.

## When exploration is the work

When work is a proof of concept, spike, parameter experiment, or user-feedback loop, use toby-swd-experiment. Treat experiment output as learning material. After the user chooses a behavior, delete the experiment or fold the chosen behavior into normal design flow.

## What to report back

The human can't see your design reasoning in a diff. After the task, give a short account:

- The structural choice you made and the main alternative you rejected, and why.
- Any reactive cleanup you did beyond the literal request.
- Any quick-fix compromise you took, the reason it qualified, and what the sound design would have been.

Skip this only for changes trivial enough that there was no real design decision.

## Anti-patterns

- **Tactical tornado.** Large volume of working code, fast, each piece adding a special case or dependency. That velocity degrades design, so do not count it as progress.
- **Deferring cleanup to "after this."** There is always another after this. Make the investment today, in this change, because a deferred investment never happens.
- **Big-bang redesign.** Trying to fix the whole architecture in one pass is the waterfall failure mode. Accrete the design from many small correct decisions instead.

## Worked examples

See `references/examples.md` for side-by-side tactical-vs-strategic versions: adding a special case, a new module's design pass, modifying existing code under a deadline.
