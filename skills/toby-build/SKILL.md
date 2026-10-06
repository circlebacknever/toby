---
name: toby-build
description: >-
  Changes what code does in the smallest step that leaves the design at least as
  good as before. It proves each change with one check run before the edit and
  again after it. Use it when the user asks to add, build, implement, wire up,
  or finish a behavior. The behavior can be a feature, a ticket, an endpoint, a
  method, a screen, a job, or a flag. Skip it for wrong output, which
  toby-bug-fix covers, and for slow code, which toby-optimize covers. Skip it
  when behavior stays the same, which toby-refactor covers, and for a throwaway,
  which toby-swd-experiment covers. Skip it for a one-file edit that copies a
  pattern already in that file.
---

# Toby Build

Build the requested change in slices the user can review one at a time, so the user never first sees a finished nine-file diff. A small answer is a valid result, such as "The repo already does this at file:line" or "This needs one decision before any code."

## The running order

Run in this order: mode, size, discovery, criteria, slices, stop 1, design, plan, stop 2. Then build the slice, prove it, stop 3, and hand off.

## Method skills
Open each file below by path, at the step named. Each is the SKILL.md of a sibling folder in the skills folder that holds this skill.
- Before the design pass, open `toby-swd-strategy`.
- When the design adds or changes a signature, open `toby-swd-interfaces`.
- When the design adds a module, moves code, or gives a module a new job, open `toby-swd-modules`, and fix each of its red flags in the design before the plan.
- When a criterion has a failure case, a retry, a timeout, or validation, open `toby-swd-errors`.
- When a criterion states a time or memory budget, or the design adds a cache, a batch, or a queue for speed, open `toby-optimize`.
- Before the first edit of a behavior change, open `toby-swd-testing`.
- When module structure or a public API changes, open `toby-swd-docs`.
- Before any command beyond safe inspection, open `toby-swd-environment`.
- Before the handoff, open `toby-swd-clarity` when the diff adds a public name or an interface comment.

## Pick the mode first

- **Experiment** for an experiment request. Use `toby-swd-experiment`, write no criteria or slices, make no stops beyond that skill's own, and say in one line what would make the work durable.
- **Durable implementation** for everything else. The rest of this file covers it.

When the user picks a behavior at the end of an experiment, write the criteria from what they picked. Run discovery on any spike code you keep, as you would on new code. When durable work needs a value that reading the code cannot settle, use `toby-swd-experiment` for that one question and return to this skill with the answer.

## Size the work before discovery

Size the work as strategic or tactical, say which in one line, and read the table for what each gate requires at that size.

**Strategic** applies when any of these fires: a new module or boundary; a public API, event, or persisted format; a migration; auth, permissions, billing, money, or privacy; a behavior three or more call sites depend on; a UI workflow crossing more than one screen; greenfield. These triggers apply to what the change does to a contract someone else depends on. A change that only touches a contract stays tactical, such as an optional parameter with a default added to an exported function. Changing what the function returns, or what its callers must handle, is a trigger.

**Tactical** applies otherwise, which covers most work.

When the request is a one-file edit following a pattern already in that file, skip this skill. Make the edit and say what you changed.

| Gate | Tactical | Strategic |
|---|---|---|
| Acceptance criteria | one line, in chat | the three-line form below, one per behavior |
| Discovery | the file that implements the behavior, and its test | all four, with the sibling feature read end to end |
| Slices | one | named, one task group each |
| Stop 1, the criteria | show them and keep moving | show them and wait |
| Stop 2, the plan | none | a written file, approved before the first edit |
| Stop 3, a slice boundary | none | only where the next slice depends on the answer |
| The Check line | write the command | run it against today's code and quote the output |

Size up mid-run when a trigger you did not see fires, and say so in one line when you do. Never size down, because a change that looked tactical and turned out to touch permissions was strategic the whole time.

For strategic work, open `references/strategic.md`. It has the other two discovery items, the slice cut, stops 2 and 3, the design lines, the plan document, and resuming half-built work.

## Discover before designing

Find the discovery items the sizing table requires before designing, and keep reading while any is missing:

- The file that implements this behavior today.
- The test covering the behavior about to change, or one sentence that states where you searched, such as "No test in `tests/orders/` covers `cancelOrder`."

Cite a path:line for every claim about how the code behaves, or add the claim to the criteria list as an assumption. That rule includes a summary from an explorer or a sub-agent. Before adding a helper, module, component, hook, or error type, search the repo for the operation. Cite the closest match at path:line, and say why it doesn't fit. When you find nothing, quote the search you ran, including the pattern.

## Evidence for each criterion

Write each criterion as the three lines below before any code. Tactical work writes them on one line in chat. Add a separate Stays-working criterion for the behavior beside this one that the change must leave alone. When a criterion is missing a line, ask the user for it or drop the criterion. Write one criterion per behavior the request names, and stop there.

- **Observable** — what the user or caller sees at the entry point they touch, after an action from a starting state. An entry point is where something outside the changed module arrives: an HTTP request, a CLI invocation, a screen someone opens, a queue message, or an exported symbol another module calls. If a reader can check a line only by reading the diff, the line adds nothing, so rewrite it or cut it.
- **Source** — quote the user sentence or ticket line the criterion came from, or cite at path:line the repo fact that forces it. Treat a repo fact with no path:line as your own preference. Cite a repo fact as the source only when the request says nothing about that behavior.
- **Check** — write the command that shows the criterion holds, and the result that would mean it is unmet, because a check that cannot fail proves nothing. When the run needs something you cannot get, such as an approval-gated command, a credential, an external service, or a device, mark the criterion `unverified`. State the blocker on the same line before stop 1. A check you could have run and skipped leaves the criterion unmet.

Reuse the vocabulary in the schema, the routes, and the UI. Ask the user before giving a concept a second name or naming a new product concept. Invented product words stay in use after the code is gone.

**Criteria are fixed text once coding starts.** If you widen a criterion, mention it in the next report. Dropping or narrowing a criterion changes what the user asked for, so give the reason and the new wording, and wait for a yes before the next edit.

## Ambiguity

When the request as worded and the problem as described disagree, state the gap before any code. A feature can match the request's words and still leave the problem unsolved.

Read the request again and look for a second defensible reading. Two readings that produce different observable behavior mean the request is ambiguous. Record the outcome in the criteria list either way, and choose the next step by what a wrong guess would cost.

- **Ask before any code** when a wrong guess writes data, changes a public contract or a stored format, moves money, touches permissions, ships a user-visible string, calls an external system, or costs more to undo than the change cost to make. Send one message with at most three questions, both readings side by side, and your recommendation.
- **Ship it marked `assumed`** when a wrong guess costs one edit to undo. Take the reading this repo already follows, and record the reading taken, the reading dropped, and what changes if the user wanted the other one. Do not write `assumed: standard behavior`, because it names neither reading and settles nothing.
- **Ship the reversible half marked `blocked`** when nobody is available to answer. Record the question verbatim and stop where the irreversible part starts. Never mark a question blocked before asking it.

Do not ask a question the repo or the user already answered.

## Cut the work into slices

Tactical work is one slice and needs only the four ship conditions below.

A slice ships when all four hold:

- It leaves the system working. Run the command that covers the touched area, using the before-and-after runs the "Prove the slice" section describes.
- The user can observe its result without reading the diff, through a request they can send, a screen they can open, or a command they can run.
- It is correct on its own. Half-built behavior a user can reach is a defect, so a slice depending on a later one ships behind a flag defaulted off, or does not ship until the later slice does. Observe a flagged slice with the flag on, and state the flag, how to turn it on, and the slice that deletes it.
- It is reachable from outside its own module. Give the path and line of the wiring: the registered route, the render site, the caller of the exported symbol, the CLI subcommand, or the event subscription.

## Checkpoints

The sizing table says which of these three stops you must make. The machine-safety stops in the operating guide and `toby-swd-environment` stay in force at either size.

1. **The criteria, before the first edit.** Show the list under the heading `What done means for [task]`, then the slice cut by name. Where stop 2 also fires, say so here, since the user's yes at this stop is also the request for the plan.

Stops 2 and 3 are in `references/strategic.md`.

Never write "assuming yes, proceeding" past a stop, which leaves this skill with no checkpoints at all.

## Design before the plan

Run the `toby-swd-strategy` design pass after stop 1 and before the plan.

When the design needs a refactor first, put it first in the plan as its own step, with its cost.

Tactical work states the structure chosen, the alternative rejected, and any new signature in chat before the first edit. Strategic work writes the design lines in `references/strategic.md`.

## Build one slice at a time

- Build one criterion per cycle. Write its test first, watch it fail, make it pass, and run it, unless `toby-swd-testing` gives a case for skipping test-first. In that case, state the case, run the criterion by hand, and quote the output.
- When the code needs a different module, boundary, or signature than the design states, stop, edit the design, and say what changed before continuing.
- Confirm every symbol this change didn't define against the installed source or the pinned manifest. A symbol can be a library function, config field, env var, CLI flag, component prop, or error type. Skip the check when this repo already calls the symbol somewhere you can cite at path:line. The lockfile version runs, so docs for a later version are a guess.
- Re-read a file before editing it a second time when anything else happened in between.
- When the change alters an existing callable, list its callers as `toby-swd-interfaces` Brownfield Work describes, and put the list in the handoff.
- Commit a refactor separately, before the feature code that uses it.

## Prove the slice before starting the next

Prove each criterion with the two-run form in `toby-swd-testing`, section Prove a change.

- A green type-check, a lint pass, or an existing suite that never runs the changed lines proves only that the repo still builds, as it did before.
- Run the change the way a user would and quote what came back. When that needs an approval-gated command, write out the command and ask for approval. Label each verification step run-by-me or for-you, and give the user only steps you could not run, each with what blocked you.

## Don't build

`references/checks.md` lists the seven things that get built without anyone asking for them. Each stays out unless a criterion asks for it and that criterion's Source line quotes the user or the ticket. Read the seven before writing the plan's out-of-scope line, or before the first edit where there is no plan. Never write a criterion yourself to allow one of them, because the catalog is there to prevent that.

## Red flags

Before writing the handoff, check the finished work against all eight entries in `references/checks.md`. Every flag that fired goes in the handoff at file:line under its entry name, including the ones you fixed on the spot. When no flag fired, say so after reading all eight.

## Final response

Lead with the behavior that now exists, stated the way the user would observe it. State any unmet or unverified criterion in the first line, with its status and what is missing.

Always write these two sections before the operating guide's final-message list:

1. List each criterion in its pre-code wording, marked met, unmet, or unverified, with the check that proved it or what is missing. For multi-slice work, list each slice by name, marked done or not-done, with its evidence.
2. Give the structure chosen and the alternative rejected, in one line each. Say where the plan is, and list any step that ran differently from the approved wording.

Then give the operating guide's final-message list. Phrase each standing assumption so the user can settle it in a word. List the questions this run could not resolve. List what you found and left alone, one line each, with the skill that covers each item. Dropping a section is a claim you checked it and found it empty.
