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

Build the thing that was asked for, in pieces someone can review one at a time. The failure this skill prevents is the nine-file diff that arrives finished. Every decision is already made inside it, so the user can only accept it or throw it away. A small answer is a valid result. "The repo already does this at file:line." is a small answer. So are "This is a four-line change." and "This needs one decision from you before any code." Telling the user the feature already exists is a good result.

## The running order

Run the work in this order: mode, size, discovery, criteria, slices, stop 1, design, plan, and stop 2. Then build the slice, prove it, record it, stop 3, and hand off. This file owns that order and how much of it each change needs. The toby-swd-* skills own what good engineering looks like at each step.

## Pick the mode before anything else

There are two modes, and a wrong pick is expensive in either direction. Acceptance criteria on a throwaway spike only add paperwork. A payments integration built as a throwaway spike ships with no criteria, no slices, and no record.

- **Experiment** is the mode for the operating guide's experiment triggers, such as spike, proof of concept, throwaway, compare options, and tune it while I watch. Hand the loop to toby-swd-experiment and stop running this skill. Write no criteria, no slices, and no record, and make no stops beyond that skill's own. Say in one line that this is experiment mode and what would move it to durable.
- **Durable implementation** is the mode for everything else, and the rest of this file covers it.

When the user picks a behavior at the end of an experiment, come back here and write the criteria from what they picked. The spike proves behavior and decides no structure. toby-swd-experiment's finish phase deletes the throwaway code, and whatever survives gets the greenfield or brownfield read on its own merits. When durable work needs a value that no amount of reading can settle, use toby-swd-experiment for that one question, then bring the answer back here.

Load `toby-swd-strategy` for every durable feature. Strategic and greenfield work gets a full design pass before any code. Tactical work gets its brownfield read and its reactive-investment pass. The operating guide's standing routes fire here on their own conditions and this file never narrows them. The active-skills line names the skills that fired.

## Size the work before anything else

There are two sizes, strategic and tactical. Pick one before discovery, say which in a line, and read the table for what each gate costs at that size.

**Strategic** applies when any of these fires: a new module or boundary; a public API, event, or persisted format; a migration; auth, permissions, billing, money, or privacy; a behavior three or more call sites depend on; a UI workflow crossing more than one screen; greenfield. These fire on what the change does to a contract someone else depends on. A change that only touches a contract stays tactical. For example, adding an optional parameter with a default to an exported function only touches it. Changing what the function returns, or what its callers must handle, is a trigger.

**Tactical** applies otherwise, which covers most work.

Before either, check that this skill should be running at all. A one-file edit following a pattern already in that file is covered by this skill's own skip clause. Make the edit and say what you changed. Writing a criteria line for a copy change adds the ceremony this skill is meant to remove.

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

Size up mid-run when a trigger you did not see fires, and say so in one line when you do. Never size down. A change that looked tactical and turned out to touch permissions was strategic the whole time.

The sections below describe each gate, and the table above says which gates each size needs.

## Discover before designing

**Brownfield work is nearly all work.** The repo's existing code already records most of these decisions, so find where. For strategic work, find all four items below before designing, and keep reading while any is missing. For tactical work, find the first and the third:

- The file that owns this behavior today.
- The nearest shipped feature built the same way, on the same layer and the same data path. Read it end to end: route, handler, model, test, doc. The new code follows its structure unless you name a reason to differ. Write one clause on what that feature got right, so the user knows which pattern the repo will soon have two copies of.
- The test covering the behavior about to change, or one sentence that names where you searched, such as "No test in `tests/orders/` covers `cancelOrder`."
- The call sites that would notice the change.

**Greenfield** means the repo has no sibling feature, no convention to inherit, and nothing nearby that resembles the change. Whatever you pick here becomes the pattern the next five features copy, including the parts you picked because it was late. Before the second file exists, name the two conventions in the repo nearest to this work, even from another layer. Say which one you're extending. Write the module's boundary down once, per toby-swd-modules and toby-swd-interfaces. Ask the user to make the naming call, because product words you invent stay in use after the implementation is gone. A rewrite that deletes this module keeps the noun. `references/examples.md` has a greenfield example that covers all three steps.

In both brownfield and greenfield work:

- `rg` finds the file, but you still have to open it, because a search hit only points to the code. Cite a path:line for every claim about how the code behaves, or add the claim to the criteria list as an assumption. That rule includes a summary from an explorer or a sub-agent. Before adding a helper, module, component, hook, or error type, search the repo for the operation. Name the closest thing you found, at path:line, and why it doesn't fit. When you find nothing, quote the search you ran, including the pattern.
- Read the behavior record for the area you're touching. Its entries are the standing claims about that area, so when an entry contradicts the request, ask the user before writing any code.

## Evidence for each criterion

Write each acceptance criterion as three short lines before any code. Add one more for what stays working, meaning the behavior beside this one that the change has to leave alone. When a criterion is missing one of the three lines, ask the user for it or drop the criterion. Write one criterion per behavior the request names, and stop there. A tactical change usually has one.

- **Observable** — this line says what the user or caller sees at the entry point they touch, after an action from a starting state. For example: "an expired token gets a 401, and the retry after refresh returns the account." An entry point is where something outside the changed module arrives. Examples are an HTTP request, a CLI invocation, a screen someone opens, a queue message, and an exported symbol another module calls. If a reader can check a line only by reading the diff, the line adds nothing to the diff, so rewrite it or cut it.
- **Source** — quote the user sentence or ticket line the criterion came from, or cite at path:line the repo fact that forces it. A repo fact with no path:line is your preference. Cite a repo fact as the source only when the request says nothing about that behavior.
- **Check** — name the command that shows the criterion holding, before writing any code. For strategic work, run the command against today's code first and quote the output at stop 1. That starting run makes the criterion provable later. For tactical work, name the command and run it after the change. Either way, if a check cannot run at all, say so before anyone approves the criterion. Name the result that would mean the criterion is unmet, because a check with no failing result passed before you wrote it. Mark the criterion `unverified` when the run needs something you cannot get, such as an approval-gated command, a credential, an external service, or a device. Name the blocker on the same line. A check you could have run and skipped leaves the criterion unmet.
- Reuse the vocabulary already in the schema, the routes, and the UI. Before giving a concept a second name, ask the user. When the request as worded and the problem as described disagree, name the gap first. A feature built to the exact words of the request can match them and still fail to solve the problem.

**Criteria are fixed text once coding starts.** If you widen a criterion, mention it in the next report. Dropping or narrowing a criterion changes what the user asked for, so give the reason and the new wording. Wait for a yes before the next edit.

## Ambiguity

Read the request again and look for a second defensible reading. Two readings that produce different observable behavior mean it is ambiguous, and you record the outcome in the criteria list either way. Choose the next step by what a wrong guess would cost.

- **Ask before any code** when a wrong guess writes data, changes a public contract or a stored format, moves money, touches permissions, ships a user-visible string, calls an external system, or costs more to unwind than the change cost to make. Send one message with at most three questions, both readings side by side, and your recommendation.
- **Ship it marked `assumed`** when a wrong guess costs one edit to undo. Take the reading this repo already follows, and record the reading taken, the reading dropped, and what changes if the user wanted the other one. Do not write `assumed: standard behavior`, because it names neither reading and settles nothing.
- **Ship the reversible half marked `blocked`** when nobody is available to answer. Record the question verbatim and stop where the irreversible part starts, and never mark a question blocked before asking it.

Do not stop for a question the repo answers, a question about anything one edit undoes, or a question the user already answered.

## Cut the work into slices

Cut tactical work into one slice, which needs only the four ship conditions below. Read those conditions and move on, because the slice names and the cut matter only once there are two slices.

A slice is the set of criteria that become observable together at one entry point. Criteria reaching different entry points are different slices: a route and a scheduled job, two screens, an API and a migration a caller can see.

Name each slice for what a person can do once it ships, in their words: `invite shows up as pending`, `search matches a full SKU`. That name becomes the plan's group heading, the stop line, and the row in the final report. The user reads one phrase from approval through handoff. A name such as `Slice 2 of 3` describes only the count, so do not use it.

A slice ships when all four hold:

- It leaves the system working. Show that by running the command that covers the touched area after the slice, and quote the output. Where a criterion is a claim about what that command printed before the change, run it first too and quote both. Without that starting run the criterion is unprovable, and that is what you report.
- The user can observe its result without reading the diff, for example through a request they can send, a screen they can open, or a command they can run.
- It is correct on its own. Half-built behavior a user can reach is a defect, so a slice depending on a later one ships behind a flag defaulted off, or waits. Observe a flagged slice with the flag on. Name the flag, how to turn it on, and the slice that deletes it.
- It's reachable from outside its own module. Name the wiring at path and line: the registered route, the render site, the caller of the exported symbol, the CLI subcommand, the event subscription.

Cutting by layer is a wrong cut, and `references/checks.md` catalogues it as **layer cut**. `references/examples.md` has four cuts worked end to end, brownfield and greenfield.

## Checkpoints

There are three stops, in the running order above. The sizing table says which of them you owe. The machine-safety stops in the operating guide and toby-swd-environment stay in force at either size.

1. **The criteria, before the first edit.** Show the list under the heading `What done means for [task]`, then the slice cut by name. Where stop 2 also fires, say so here, since the user's yes at this stop is also the request for the plan.
2. **The plan, after the design pass and before the first edit.** The plan is a written file that the user reviews and approves before execution, as the plan document section describes.
3. **The slice boundary where the next slice depends on the answer.** This stop applies when a decision surfaced, a criterion turned out wrong, or discovery missed a strategic trigger. Open with what the user can now do that they couldn't before, using the slice's name. Then say what proved it and what the next slice does, and wait. At a boundary with no such question, write the same three lines and keep moving. Stopping there anyway is **stop inflation** in `references/checks.md`.

Never write "assuming yes, proceeding" past a stop, which leaves this skill with no checkpoints at all.

## The plan document

Write the plan as a file, and never agree on a plan in scrollback, because nobody can check off items in scrollback. The operating guide owns the format: `Toby's plan for [task]`, task groups, checkboxes, and a verification block ending each group. This file owns when the plan gets written and what a step must contain for someone to approve it.

- The plan is **written when** the user asks. A yes at stop 1 counts as asking only when stop 1 named the plan.
- The plan goes **where** the repo already keeps plans. When there is no obvious place, propose a path and get a yes, which is the same gate the behavior record has.
- The plan **opens with** the mode, the one-line problem, the criteria in their pre-code wording, and what's out of scope. One task group per slice follows, in the order the slices ship. Each group takes its slice's name as its title and ends in its verification block. An operator approving a plan is approving the boundary as much as the work.
- **Anything on** the ask-list in the operating guide or toby-swd-environment appears as its own step with the exact command. That ask-list includes a migration, install, seed, snapshot, deletion, process, or port.
- **The plan is the execution record.** Check items off as they are done. When execution diverges from an approved step, edit the plan and say what changed before continuing.
- **A step an operator can approve** names the file it touches at path, and whether the step creates, edits, or deletes that file. It says what changes there, concretely enough for someone to disagree with. It names the criterion it serves, by its wording, and what proves it, with the result that would mean it failed. `references/examples.md` contains a task group written at that detail.

## Build one slice at a time

- Work on one criterion per cycle: write the test first, watch it fail, make it pass, and run it. toby-swd-testing owns when test-first is skipped. When you skip it, name the skip in toby-swd-testing's words, run the criterion by hand, and quote the output.
- Write what the design called for. If you find yourself writing less code than the design called for, the design was wrong, so fix the design and say you did.
- Confirm every symbol this change didn't define against the installed source or the pinned manifest. A symbol can be a library function, config field, env var, CLI flag, component prop, or error type. Skip the check when this repo already calls the symbol somewhere you can cite at path:line. The lockfile version is the one that runs, so docs for a later version are a guess.
- Re-read a file before editing it a second time when anything else happened in between. Your memory of a file you changed three steps ago is a guess, however sure it feels.
- When the change alters an existing function, method, or other callable, run the caller sweep `toby-swd-interfaces` owns and put its result in the handoff.
- Refactors go in their own commit unless the refactor is what makes the behavior fit.

## Prove the slice before starting the next

- A criterion counts as met after two runs of one named command, quoted under the criterion's own wording. The first run is against the code before the change, or with the new path disabled, and the second run is after the change:

      cancelling a shipped order returns 409 and leaves the order untouched
      before  test_cancel_rejects_shipped  FAIL  expected 409, got 200
      after   test_cancel_rejects_shipped  PASS

  Use the same form for every criterion in every slice, with the command named beside it. The check has to execute the new code path, so a pair with only an `after` proves the harness runs. Report that criterion met-unproven and name the run that never happened.
- A green type-check, a lint pass, or an existing suite that never enters the changed lines proves only that the repo still builds, and it built before you started.
- Run the change the way a user would and quote what came back. When that needs an approval-gated command, name the exact command and ask for it. Saying "this needed approval" with no command named is a skipped step. Hand manual steps to the user only for what you couldn't run, labelled run-by-me or for-you. Every for-you step says what blocked you. A step handed over with no reason reads as a chore assignment.

## Write the behavior down

Write down what the request said the behavior should be. A year later, the code shows what it does, and nothing records what it was for. The next reader then checks the code against their own guess and files the difference as a bug.

- **Fires** when the request contains words for a behavior, from the user or the ticket, and the record doesn't state that behavior yet. `references/behavior-record.md` lists the changes that write no entry and says where an inferred behavior goes. When a run writes no entry, name the reason from that list.
- **Home** is a prose file the repo already keeps for stated behavior. When no such file exists, propose `docs/behavior.md` and get a yes before creating it, which is the same gate the plan file has.
- **Entry** is a heading that states the behavior in one sentence. The sentence gives the trigger and the observable result at the public interface `toby-swd-testing` tests through. It names no function, file, or internal state. Add who asked, quoted, and when. Two sentences means two behaviors, so split them. The test description quotes that sentence verbatim, character for character.
- **Check**, before handoff: run the grep in `references/behavior-record.md` and report what it printed. Every line it prints is a sentence the product claims and no test checks, so name each one in the handoff.
- **Retire** an entry in the diff that deletes its test, and edit a falsified sentence in the diff that falsifies it. `references/behavior-record.md` covers both, the entry rules in full, and the two-branch case.

## Don't build

`references/checks.md` lists the seven things that get built without anyone asking for them. Each stays out unless a criterion names it and that criterion's Source line quotes the user or the ticket. Read the seven before writing the plan's out-of-scope line, or before the first edit where there is no plan. Never write a criterion yourself to allow one of them, because the catalog is there to prevent that.

## Resuming half-built work

Before touching code, recover five things: the mode, the criteria list, the plan, which steps are checked off, and the last checkpoint decision. Look in the thread, the diff, the plan file, the behavior record, and the repo. When you cannot find any of them, rebuild them from the code that exists and the original request, show them, and confirm before continuing. Criteria read back off a diff agree with that diff, including where it was wrong. Name whichever ones you couldn't recover. Half-built experiment code is still experiment code until the user says otherwise.

## Red flags

Before writing the handoff, check the finished work against all eight entries in `references/checks.md`. Also check it against the red-flag list of every skill on the active-skills line. Every flag that fired goes in the handoff at file:line under its entry name, including the ones you fixed on the spot. When no flag fired, say so after reading all eight.

## Final response

Lead with the behavior that now exists, stated the way the user would observe it. Any criterion unmet or unverified is named in the first line, with which of the two it is and what is missing. Do not save what didn't ship for the end of the report, because that order makes the work look better than it is.

This file adds two sections, and both always appear:

1. List each criterion in its pre-code wording, marked met with the check that proved it, or unverified with the reason. For multi-slice work, list each slice by name, marked done or not-done, with its evidence.
2. List the behavior record entries written, edited, or retired, and the result of the check. When no entry fired, say so and why. Say where the plan is, and name any step that ran differently from the approved wording.

Then give the operating guide's list: anything incomplete or risky, tests deleted or weakened, heavy commands skipped, processes left running, and assumptions still waiting.

Phrase each standing assumption so the user can settle it in a word. Name the questions this run could not resolve. List any placeholder left in a production path at file:line. List what you found and left alone, one line each, with the skill that owns each item. Dropping a section is a claim you checked it and found it empty.

## References

- `references/checks.md` lists the seven don't-build entries and the eight red flags, each under the name a handoff cites.
- `references/behavior-record.md` covers what the record skips, the entry and binding rules in full, the grep, retiring, and the two-branch case.
- `references/examples.md` has worked slice cuts for four kinds of feature, greenfield and brownfield. It also has a plan with steps at approval detail, and a filled behavior record with its bindings and a retired entry.
