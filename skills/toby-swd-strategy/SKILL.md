---
name: toby-swd-strategy
description: >-
  Decide whether this change leaves the design better or worse before
  writing it. Use it for non-trivial work: a feature, a bug fix with
  behavioral risk, a refactor, a public API or module-boundary change, or an
  edit where the quick patch adds a special case or a hidden dependency. It
  covers the design pass and the near-future variants. It refers the
  resulting decisions to `toby-swd-modules` and `toby-swd-interfaces`. Skip
  it for read-only investigation, a rename, a formatting pass, a throwaway
  spike, and any change whose structure the surrounding code already determines.
---

# Toby SWD Strategy

Write today's code knowing that every future change will start from its structure. Most code in any system is written by extending what's already there. So the main design question is whether the module boundary still works for the next change.

An autonomous agent is especially prone to pure tactical execution. "Make the test pass" is such a clear point to stop that tactical programming seems disciplined. Do not count a large volume of working code as progress when each piece adds a special case or a hidden dependency. That code makes the design worse with each piece added.

The deliverable is a system whose design is at least as good after your change as before it. Target a design that still works after the next change, and write the working code from that design.

## Before writing — design pass

For anything beyond a one-line change, don't implement the first idea.

- State the change in one sentence, including the obvious near-future variants ("today there is one provider, but tomorrow there will be three").
- Sketch at least two structural approaches. They must differ in *where the complexity is*: which module handles the hard part, what the interface exposes, what callers must manage. Pick the one with the simplest caller-side interface, even when its implementation is harder. In this step, you sketch two placements of the work. It does not conflict with the single-candidate rule in `toby-swd-interfaces`, which applies to one signature once the placement is settled.
- Check the near-future variants against your design. If a likely next change would force callers to change or add a new special case, adjust now while it's cheap.
- If those variants are new cases picked by a tag or type, design the dispatch now. Use a lookup map when the case bodies are small, and an interface with implementations when each case has its own state. `toby-swd-modules` lists the ladder of dispatch options. In greenfield work, build the dispatch in from the start. In brownfield work, offer it as a scoped refactor.
- A change that is only one line doesn't need an architecture review, because the design pass scales to the size of the decision.

## While writing — put complexity in the right place

Put the hard part where it costs the fewest callers. Skew the ratio of interface cost to implementation benefit heavily toward the implementation side. `toby-swd-modules` defines the deep module and lists the checks that find a shallow one.

Do not expose internal mechanics, config knobs, or special cases because they are the quickest option in the code you are editing. Every parameter a caller must manage is overhead distributed across every future call site. Prefer computing a value internally over exporting a configuration parameter or throwing back to the caller.

Aim for deep modules. Small functions help that goal only when they make a module deeper. A split that creates two shallow units in place of one deep one is a loss, even when the result looks tidy. When shrinking a function would make a deep module shallow, keep the deep module.

## After writing — reactive investment

You now have full context on this code. Improving the code now costs less than it will at any later time, because you will not have this context again.

- If you patched *around* a design problem to make your change fit, stop and fix the design instead. A workaround that adds a special case, a flag, or a surprise dependency is debt you are choosing to take on with full awareness.
- Find one design imperfection in the code you touched: an obscure name, a leaky abstraction, a dead branch, a comment that is wrong, duplicated logic. Fix it when the cleanup is small, local, and directly supports the change. Otherwise report it as follow-up. Scope discipline is part of design, so do not start cleanup outside the code you touched.
- Keep cleanups scoped to code you're already in. Do not extend a refactor across the codebase.

## The test for modifying existing code

Replace "what is the smallest edit that does what I need?" with:

> What structure would this code have if it had been designed from the start with this change already in mind?

Move the code toward that structure. Often the answer is "what's there now, plus the new part", so proceed. Sometimes it reveals the current design no longer fits. Then refactor first and add the change on top with no workaround. Choose between these two paths deliberately. Do not default to the minimal diff, because a run of reasonable-looking minimal commits makes a codebase worse one commit at a time.

## Brownfield Work

On existing code, read the current design before choosing a new one. Identify the smallest local refactor that would make the requested change fit naturally. If that refactor is small, scoped to touched code, and lowers future cost, offer it with its cost and benefit before doing it. If it would expand the task, state the tradeoff and let the user choose between the refactor and the smaller tactical change.

## When the quick fix is the correct choice

Take the tactical path when:

- The extra time would miss a hard external deadline, and the cost is understood and accepted.
- The sound refactor would change an interface other teams or callers depend on, and coordinating that is out of scope.
- The sound version requires information you don't have and can't get.

"This is faster" alone is not on the list. When you take the quick path for a real reason, make the debt visible. Leave a comment that states what the sound design would be and why you skipped it. Never leave that debt unlabeled, because the next person cannot see it to fix it.

## Writing a design note

- Put the recommendation and its main reason in the first sentence, such as "Use an `audit_log` table, because the monthly report reads events by date." Do not open with a sentence about the note or with a label.
- Describe each approach once. Then compare the approaches on the facts you were given, one fact per sentence.
- Do not add a column, an index, a volume, or a cost that the request and the code do not show. Specify an unknown only when its answer could change the recommendation.
- End after the last comparison or unknown, with no summary of the reasons.
- Terms in this skill, such as near-future variant, are for your reasoning. The note states the fact behind the term, such as "Finance asked for refund events in the same history."

## What to report back

The human can't see your design reasoning in a diff. After the task, give a short account:

- The structural choice you made and the main alternative you rejected, and why.
- Any reactive cleanup you did beyond the literal request.
- Any quick-fix compromise you took, the reason it qualified, and what the sound design would have been.

Skip this only for changes trivial enough that there was no real design decision.

## Anti-patterns

- **Tactical tornado.** A tactical tornado is a large volume of working code, written fast, where each piece adds a special case or dependency. Writing at that speed makes the design worse, so do not count it as progress.
- **Big-bang redesign.** Trying to fix the whole architecture in one pass repeats the waterfall failure mode. Build the design up from many small correct decisions.

## Compliance check

Before calling the change done, state in one line which anti-pattern above the
change came closest to and what stopped it. Say "none applies" when none does,
because the list affects the change only when someone checks it.

## Worked examples

See `references/examples.md` for side-by-side tactical-vs-strategic versions: adding a special case, a new module's design pass, modifying existing code under a deadline.
