---
name: toby-feature-dev
description: >-
  Turn a feature request into the smallest change that satisfies it, with evidence it
  works and the requirement written where a future reader can audit it. Skip it for a one-
  file edit following a pattern already in that file, a review or cleanup pass over code
  that exists, read-only investigation or explanation, and anything the user framed as a
  spike, proof of concept, or throwaway, which belongs to toby-swd-experiment. Use it when
  the user asks to build, add, implement, wire up, or finish a behavior spanning more than
  one file or one call site: a ticket, a product ask, a half-built feature, an endpoint,
  screen, job, or flag, or a bug fix whose repair is new behavior. Use it when the request
  leaves "done" undefined and code has to start anyway. It owns mode, acceptance criteria,
  discovery, slicing, the plan the operator approves, approval stops, the behavior record,
  and handoff, and routes method to the toby-swd-* skills.
---

# Toby Feature Dev

Build the thing that was asked for, in pieces someone can watch land. The failure this skill prevents is the nine-file diff that arrives finished, every decision already made inside it. The user can accept it or throw it away. A small answer is a valid result. "The repo already does this at file:line." "This is a four-line change." "This needs one decision from you before any code." Nobody has ever been annoyed to hear the feature already exists.

## The running order

Mode. Size. Discovery. Criteria. Slices. Stop 1. Design. Plan. Stop 2. Build the slice, prove it, record it. Stop 3. Handoff. This file owns that order and how much of it a change owes. The toby-swd-* skills own what good engineering looks like at each step.

## Pick the mode before anything else

Two modes, and picking wrong is expensive in both directions. A throwaway spike carrying acceptance criteria is paperwork. A payments integration built as a throwaway spike is a payments integration built as a throwaway spike.

- **Experiment**, on the operating guide's experiment triggers — spike, proof of concept, throwaway, compare options, tune it while I watch. Hand the loop to toby-swd-experiment and stand down: no criteria, no slices, no record, no stops beyond that skill's own. Say in one line that this is experiment mode and what would move it to durable.
- **Durable implementation**, everything else, which is the rest of this file.

When the user picks a behavior at the end of an experiment, come back here and write the criteria from what they picked. The spike proves behavior and decides no structure. toby-swd-experiment's finish phase deletes the throwaway code, and what survives gets the greenfield or brownfield read on its own merits. Durable work that stalls on a value no amount of reading can settle drops into toby-swd-experiment for that one question, then returns with the answer.

Every durable feature loads toby-swd-strategy: a full design pass before any code on strategic or greenfield work, its brownfield read and reactive-investment pass on tactical work. The operating guide's standing routes fire here on their own conditions and this file never narrows them. The skills that fired name the active-skills line.

## Size the work before anything else

Two sizes. Pick one before discovery, say which in a line, and read the table for what each gate costs at that size.

**Strategic** when any of these fires: a new module or boundary; a public API, event, or persisted format; a migration; auth, permissions, billing, money, or privacy; a behavior three or more call sites depend on; a UI workflow crossing more than one screen; greenfield. These fire on what the change does to a contract someone else depends on. Contact alone stays tactical. Adding an optional parameter with a default to an exported function is contact. Changing what it returns, or what its callers must handle, is a trigger.

**Tactical** otherwise, which is most work.

Before either, check that this skill should be running at all. A one-file edit following a pattern already in that file is in this skill's own skip clause, so make the edit and say what you changed. A criteria line for a copy change is the ceremony this file exists to avoid.

| Gate | Tactical | Strategic |
|---|---|---|
| Acceptance criteria | one line, in chat | the three-line form below, one per behavior |
| Discovery | the file that owns the behavior, and its test | all four, with the sibling feature read end to end |
| Slices | one | named, one task group each |
| Stop 1, the criteria | show them and keep moving | show them and wait |
| Stop 2, the plan | none | a written file, approved before the first edit |
| Stop 3, a slice boundary | none | only where the next slice depends on the answer |
| The Check line | name the command | run it against today's code and quote the output |
| Behavior record | only when the request names a behavior | every criterion |

Size up mid-run when a trigger you did not see fires, and say so in one line when you do. Size down never. A change that looked tactical and turned out to touch permissions was strategic the whole time.

The gates below say what each one is. The table says which of them you owe.

## Discover before designing

**Brownfield, which is nearly always.** The repo has already decided most of this, so go find where. Strategic work fills all four before designing and keeps reading while any is short. Tactical work owes the first and the third:

- The file that owns this behavior today.
- The nearest shipped feature built the same way, on the same layer and the same data path. Read it end to end: route, handler, model, test, doc. The new code follows its structure unless you name a reason to differ. One clause on what that feature got right tells the user which pattern they are about to have two of.
- The test covering the behavior about to change, or "none — searched <what you searched>".
- The call sites that would notice the change.

**Greenfield** — no sibling feature, no convention to inherit, nothing nearby resembling the change. Whatever you pick here becomes the pattern the next five features copy, including the parts you picked because it was late. Before the second file exists, name the two conventions nearest to this work that the repo already has, even from another layer, and say which one you're extending. Write the module's boundary down once, per toby-swd-modules and toby-swd-interfaces. Ask for the naming call, because product vocabulary you invent outlives the implementation and the rewrite that deletes this module keeps the noun. `references/examples.md` runs a greenfield cut through all three.

Both modes:

- `rg` finds the file. The file still has to be opened. A search hit is a pointer. A claim about how the code behaves carries a path:line or enters the criteria list as an assumption, an explorer's or sub-agent's summary included. Before adding a helper, module, component, hook, or error type, search the repo for the operation. Name the closest thing you found, at path:line, and why it doesn't fit. Nothing found means quoting the search you ran, the pattern and all.
- Read the behavior record for the area you're touching. Its entries are the standing claims about that area, so an entry contradicting the request is a question for the user before any code.

## Every criterion is its own proof

Write each acceptance criterion as three short lines before any code, plus one for what stays working: the behavior beside this one the change has to leave alone. Missing one of the three means it isn't a criterion, so ask, or drop it. Write one criterion per behavior the request names, and stop there. A tactical change usually has one.

- **Observable** — given a starting state, when an action happens, the user or caller sees a result, at the entry point they touch: "an expired token gets a 401, and the retry after refresh returns the account." An entry point is where something outside the changed module arrives. An HTTP request, a CLI invocation, a screen someone opens, a queue message, an exported symbol another module calls. A line checkable only by reading the diff is the diff with a checkbox on it, so rewrite it or cut it.
- **Source** — the user sentence or ticket line it came from, quoted, or the repo fact that forces it, cited at path:line. A repo fact with no path:line is your preference. Source to a repo fact only where the request is silent on that behavior.
- **Check** — the command that shows it holding, named before any code. Strategic work runs it against today's code first and quotes the output at stop 1, because that starting run is what makes the criterion provable later. Tactical work names the command and runs it after. Either way, a criterion whose check cannot run at all says so before anyone approves it. Name the result that would mean the criterion is unmet; a check with no failing result passed before you wrote it. `unverified` is available when the run needs something out of reach: an approval-gated command, a credential, an external service, a device. Name the blocker on the same line. A check you could have run and skipped leaves the criterion unmet.
- Reuse the vocabulary already in the schema, the routes, and the UI. A second name for a concept that has one is a question for the user. When the request as worded and the problem as described disagree, name the gap first. Building the words exactly is how a feature ships correct and useless.

**Criteria are fixed text once coding starts.** Widening one is a note in the next report. Dropping or narrowing one changes what the user asked for. Give the reason and the new wording, and wait for a yes before the next edit.

## Ambiguity

Read the request again hunting for a second defensible reading. Two readings that produce different observable behavior mean it is ambiguous, and the criteria list records the outcome either way. What a wrong guess costs decides what happens next.

- **Ask before any code** when a wrong guess writes data, changes a public contract or a stored format, moves money, touches permissions, ships a user-visible string, calls an external system, or costs more to unwind than the change cost to make. One message, at most three questions, both readings side by side, your recommendation.
- **Ship it marked `assumed`** when a wrong guess costs one edit to undo. Take the reading this repo already follows, and carry the reading taken, the reading dropped, and what changes if the user wanted the other one. `assumed: standard behavior` marks nothing and settles nothing.
- **Ship the reversible half marked `blocked`** when nobody is available to answer. Record the question verbatim and stop where the irreversible part starts, and never mark a question blocked before asking it.

Questions the repo answers, questions about anything one edit undoes, and questions the user already answered earn no stop.

## Cut the work into slices

Tactical work has one slice and owes only the four ship conditions below, so read those and move on. The naming and the cut matter once there are two.

A slice is the criteria that land observable together at one entry point. Criteria reaching different entry points are different slices: a route and a scheduled job, two screens, an API and a migration a caller can see.

Name each slice for what a person can do once it lands, in their words: `invite shows up as pending`, `search matches a full SKU`. That name is the plan's group heading, the stop line, and the row in the final report, so the user reads one phrase from approval through handoff. `Slice 2 of 3` names the counting.

A slice ships when all four hold:

- It leaves the system working, shown by the command covering the touched area run after the slice and quoted. Where a criterion is a claim about what that command printed before the change, run it first too and quote both. Without that starting run the criterion is unprovable, and that is what you report.
- The user can observe its result without reading the diff — a request they can send, a screen they can open, a command they can run.
- It stands correct on its own. Half-built behavior a user can reach is a defect, so a slice depending on a later one ships behind a flag defaulted off, or waits. A flagged slice meets the observation bar with the flag on. Name the flag, how to turn it on, and the slice that deletes it.
- It's reachable from outside its own module. Name the wiring at path and line: the registered route, the render site, the caller of the exported symbol, the CLI subcommand, the event subscription.

Cutting by layer is the classic wrong cut, catalogued as **layer cut** in `references/checks.md`. Four cuts worked end to end, brownfield and greenfield, live in `references/examples.md`.

## Checkpoints

Three stops, on the running order above. The sizing table says which of them you owe. The machine-safety stops in the operating guide and toby-swd-environment stay in force at either size.

1. **The criteria, before the first edit.** Show the list under the heading `What done means for [task]`, then the slice cut by name. Where stop 2 also fires, say so here, since the yes at this stop is what asks for the plan.
2. **The plan, after the design pass and before the first edit.** A written file, reviewed and approved before execution. See below.
3. **The slice boundary where the next slice depends on the answer** — a decision surfaced, a criterion that turned out wrong, a strategic trigger discovery missed. Open with what the user can now do that they couldn't this morning, in the slice's name, then what proved it, then what the next slice does, and wait. A boundary carrying no such question gets the same three lines and keeps moving, catalogued as **stop inflation** in `references/checks.md`.

Never write "assuming yes, proceeding" past a stop, which leaves this skill with no checkpoints at all.

## The plan document

The operating guide owns the format — `Toby's plan for [task]`, task groups, checkboxes, a verification block ending each group. This file owns when the plan gets written and what a step carries for someone to approve it. Do not agree a plan in scrollback, because nobody can check it off.

- **Written when** the user asks, which includes the yes at stop 1. Naming the plan at that stop is what gets one.
- **Where** the repo already keeps plans. With nowhere obvious, propose a path and get a yes, the same gate the behavior record gets.
- **Opens with** the mode, the one-line problem, the criteria in their pre-code wording, and what's out of scope, then one task group per slice in the order they ship, each carrying its slice's name and ending in its verification block. An operator approving a plan is approving the boundary as much as the work.
- **Anything on** the operating guide's or toby-swd-environment's ask-list — migration, install, seed, snapshot, deletion, process or port — appears as its own step with the exact command.
- **The plan is the execution record.** Check items off as they land, and when execution diverges from an approved step, edit the plan and say what moved before continuing.
- **A step an operator can approve** names four things: the file it touches at path and whether it's created, edited, or deleted; what changes there, concretely enough to disagree with; the criterion it serves, by its wording; and what proves it, with the result that would mean it failed. `references/examples.md` carries a task group written at that detail.

## Build one slice at a time

- One criterion per cycle: test first, watch it fail, make it pass, run it. toby-swd-testing owns when test-first is skipped. Name the skip in its words, run the criterion by hand, and quote the output.
- Write what the design called for. Shrinking the code below the design while implementing means the design was wrong, so go fix the design and say you did.
- Confirm every symbol this change didn't define — library function, config field, env var, CLI flag, component prop, error type — against the installed source or the pinned manifest, unless this repo already calls it somewhere you can cite at path:line. The lockfile version is what runs. Docs for a later one are a guess.
- Re-read a file before editing it a second time when anything else happened in between. Your memory of a file you changed three steps ago is a guess with a confident tone.
- When the change alters an existing callable surface, run the caller sweep `toby-swd-interfaces` owns and carry its result into the handoff.
- Refactors go in their own commit unless the refactor is what makes the behavior fit.

## Prove the slice before starting the next

- A criterion counts as met on two runs of one named command, quoted under the criterion's own wording — the run against the code as it stood before the change or with the new path disabled, then the run after:

      cancelling a shipped order returns 409 and leaves the order untouched
      before  test_cancel_rejects_shipped  FAIL  expected 409, got 200
      after   test_cancel_rejects_shipped  PASS

  Same form every criterion, every slice, with the command named beside it. The check has to execute the new code path, so a pair carrying only an `after` proves the harness runs. Report that criterion met-unproven and name the run that never happened.
- A green type-check, a lint pass, or an existing suite that never enters the changed lines proves the repo still builds. It built before you started.
- Run the change the way a user would and quote what came back. When that needs an approval-gated command, name the exact command and ask for it. Saying "this needed approval" with no command named is a skipped step. Hand manual steps to the user only for what you couldn't run, labelled run-by-me or for-you. Every for-you says what blocked you. A step handed over with no reason reads as a chore assignment.

## Write the behavior down

A year out, the code says what it does and nothing says what it was for. The next reader audits it against their own guess and files the difference as a bug.

- **Fires** when the request holds words for a behavior — the user's or the ticket's — and the record doesn't state it yet. `references/behavior-record.md` holds what writes no entry and where an inferred behavior goes. A run that writes none names its reason from that list.
- **Home** is a prose file the repo already keeps for stated behavior. With nothing present, propose `docs/behavior.md` and get a yes before creating it, the same gate the plan file gets.
- **Entry** is a heading holding the behavior in one sentence: trigger plus observable result, at the public interface `toby-swd-testing` tests through, naming no function, file, or internal state. Add who asked, quoted, and when. Two sentences means two behaviors, so split them. The test description quotes that sentence verbatim, character for character.
- **Check**, before handoff: run the grep in `references/behavior-record.md` and report what it printed. Every line it prints is a sentence the product claims and no test defends, and each one gets named in the handoff.
- **Retire** an entry in the diff that deletes its test, and edit a falsified sentence in the diff that falsifies it. `references/behavior-record.md` carries both, the entry rules in full, and the two-branch case.

## Don't build

`references/checks.md` holds the seven things that get built without anyone asking for them. Each stays out unless a criterion names it and that criterion's Source line quotes the user or the ticket. Read the seven before writing the plan's out-of-scope line, or before the first edit where there is no plan. Never write a criterion yourself to license one of them, which is what the catalog exists to stop.

## Resuming half-built work

Before touching code, recover the mode, the criteria list, the plan and which steps are checked off, and the last checkpoint decision from the thread, the diff, the plan file, the behavior record, and the repo. When none of them survive, rebuild them from the code that exists and the original request, show them, and confirm before continuing. Criteria read back off a diff agree with that diff, including where it was wrong. Name whichever ones you couldn't recover. Half-built experiment code is still experiment code until the user says otherwise.

## Red flags

Check the finished work against all eight entries in `references/checks.md`, plus the red-flag list of every skill on the active-skills line, before writing the handoff. Every flag that fired goes in the handoff at file:line under its entry name, including the ones you fixed on the spot. A pass with nothing fired says so, after reading the eight.

## Final response

Lead with the behavior that now exists, stated the way the user would observe it. Any criterion unmet or unverified is named in the first line, with which of the two it is and what is missing. A report that closes with what didn't land is written in the order that flatters it.

Two sections this file adds, and both always appear:

1. Each criterion in its pre-code wording, marked met with the check that proved it, or unverified with why. Multi-slice work lists each slice by name, done or not-done, with its evidence.
2. Behavior record entries written, edited, or retired, and the result of the check. A run where none fired says so and why. Where the plan lives, and any step that ran differently from the approved wording.

Then the operating guide's list: anything incomplete or risky, tests deleted or weakened, heavy commands skipped, processes left running, assumptions still waiting. Phrase each standing assumption so the user can settle it in a word, and name the questions this run could not resolve. Add placeholders left in a production path at file:line, and what you found and left alone, one line each, handed to the skill that owns it. Dropping a section is a claim you checked it and found it empty.

## References

- `references/checks.md` — the seven don't-build entries and the eight red flags, each under the name a handoff cites.
- `references/behavior-record.md` — what the record skips, the entry and binding rules in full, the grep, retiring, and the two-branch case.
- `references/examples.md` — worked slice cuts for four kinds of feature, greenfield and brownfield, a plan with steps at approval detail, and a filled behavior record with its bindings and a retired entry.
