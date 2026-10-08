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

Build the requested change in slices, which are small parts the user can review one at a time. The user should never first see the change as a finished diff across nine files. A small answer is a valid result, such as "The repo already does this at file:line" or "This needs one decision before any code."

## The running order

Work in this order. Pick the mode and size the work. Read the existing code, which is the discovery step. Write the acceptance criteria and cut the work into slices.

Make stop 1, where the user sees the criteria. Design the change, write the plan, and make stop 2, where the user approves the plan. Then build a slice, prove it, make stop 3, and write the handoff, which is the final report.

## Method skills
Each name below is another skill, stored at `../<name>/SKILL.md` relative to this skill's folder. Open that file by path when you reach the step listed beside it.
- Before the design pass, open `toby-swd-strategy`.
- When the design adds or changes a signature, open `toby-swd-interfaces`.
- When the design adds a module, moves code, or gives a module a new job, open `toby-swd-modules`, and fix each of its red flags in the design before the plan.
- When a criterion has a failure case, a retry, a timeout, or validation, open `toby-swd-errors`.
- When a criterion states a time or memory budget, or the design adds a cache, a batch, or a queue for speed, open `toby-optimize`.
- Before the first edit of a behavior change, open `toby-swd-testing`.
- When module structure or a public API changes, open `toby-swd-docs`.
- Before you run any command that does more than read files or print state, open `toby-swd-environment`.
- Before the handoff, open `toby-swd-clarity` when the diff adds a public name or an interface comment.

## Pick the mode first

- **Experiment** for an experiment request. Use `toby-swd-experiment` and write no criteria or slices. Stop for the user only where that skill says to stop. Say in one line what would have to happen before the code could be kept as durable work.
- **Durable implementation** for everything else. The rest of this file covers it.

When the user picks a behavior at the end of an experiment, write the criteria from what they picked. Run the discovery step on any experiment code you keep, with the same care you give new code. When durable work needs a value that you cannot find by reading the code, use `toby-swd-experiment` for that one question. Then come back to this skill with the answer.

## Size the work before discovery

Size the work as strategic or tactical, and say which in one line. The table below shows what each step of the work requires at that size.

**Strategic** applies when the change involves any of these triggers:

- a new module or boundary
- a public API, an event, or a persisted format
- a migration
- auth, permissions, billing, money, or privacy
- a behavior that three or more call sites depend on
- a UI workflow that crosses more than one screen
- greenfield work, where the repo has no similar feature and no convention to follow

A trigger counts when the change creates a contract or alters one, and a contract is something that other code or people depend on. A change that only adds an optional part to an existing contract stays tactical. An example is an optional parameter with a default added to an exported function. Changing what the function returns, or what its callers must handle, is a trigger.

**Tactical** applies otherwise, which covers most work.

When the request is a one-file edit following a pattern already in that file, skip this skill. Make the edit and say what you changed.

| Gate | Tactical | Strategic |
|---|---|---|
| Acceptance criteria | one line, in chat | the three-line form below, one per behavior |
| Discovery | the file that implements the behavior, and its test | those two plus the two in `references/strategic.md`, with the most similar existing feature read end to end |
| Slices | one | named, one task group each |
| Stop 1, the criteria | show them and keep moving | show them and wait |
| Stop 2, the plan | none | a written file, approved before the first edit |
| Stop 3, a slice boundary | none | only where the next slice depends on the answer |
| The Check line | write the command | run it against today's code and quote the output |

If you find a strategic trigger partway through the work, switch the work to strategic and say so in one line. Never switch strategic work back to tactical. A change that looked tactical and turned out to touch permissions was strategic the whole time.

For strategic work, open `references/strategic.md`. That file lists the extra discovery items, how to cut the work into slices, and stops 2 and 3. That file also covers the design lines, the plan document, and how to resume half-built work.

## Discover before designing

Find the discovery items the sizing table requires before designing, and keep reading while any is missing:

- The file that implements this behavior today.
- The test covering the behavior about to change, or one sentence that states where you searched, such as "No test in `tests/orders/` covers `cancelOrder`."

Cite a path:line for every claim about how the code behaves, or add the claim to the criteria list as an assumption. That rule also applies to claims in a summary from a search agent or any other sub-agent. Before adding a helper, module, component, hook, or error type, search the repo for the operation. Cite the closest match at path:line, and say why it doesn't fit. When you find nothing, quote the search you ran, including the pattern.

## Evidence for each criterion

Write each criterion as the three lines below before any code. For tactical work, write all three on one line in chat. Also add a separate Stays-working criterion for a nearby behavior that the change must leave unchanged. When a criterion is missing a line, ask the user for it or drop the criterion. Write one criterion per behavior the request names, and stop there.

- **Observable** — what the user or caller sees at the entry point they use, after they take an action from a stated starting state. An entry point is where something outside the changed module arrives: an HTTP request, a CLI invocation, a screen someone opens, a queue message, or an exported symbol another module calls. If a reader can check a line only by reading the diff, the line adds nothing, so rewrite it or cut it.
- **Source** — quote the user sentence or ticket line the criterion came from, or cite at path:line the repo fact that requires it. A claim about the repo with no path:line counts as your own preference. Cite a repo fact as the source only when the request says nothing about that behavior.
- **Check** — write the command that shows the criterion holds, and the result that would mean it is unmet, because a check that cannot fail proves nothing. When the run needs something you cannot get, such as an approval-gated command, a credential, an external service, or a device, mark the criterion `unverified`. State the blocker on the same line before stop 1. A check you could have run and skipped leaves the criterion unmet.

Reuse the vocabulary in the schema, the routes, and the UI. Ask the user before giving a concept a second name or naming a new product concept. Users and docs keep using an invented product word after the code that introduced it is gone.

**Criteria are fixed text once coding starts.** If you change a criterion so it covers more, mention the change in the next report. Dropping or narrowing a criterion changes what the user asked for, so give the reason and the new wording, and wait for a yes before the next edit.

## Ambiguity

When doing what the request says would not solve the problem the user described, say so before any code. A feature can match the request's words and still leave the problem unsolved.

Read the request again and look for a second reasonable way to understand it. Two readings that produce different observable behavior mean the request is ambiguous. Record in the criteria list whether you found a second reading. Choose the next step by what a wrong guess would cost.

- **Ask before any code** when the code built from a wrong guess would write data, change a public contract or a stored format, or move money. Ask first also when that code would touch permissions, ship a user-visible string, call an external system, or cost more to undo than to make. Send one message with at most three questions, both readings side by side, and your recommendation.
- **Ship it marked `assumed`** when a wrong guess costs one edit to undo. Take the reading that matches how this repo already behaves, and record the reading taken, the reading dropped, and what changes if the user wanted the other one. Do not write `assumed: standard behavior`, because it states neither reading and leaves the question open.
- **Ship the part that can be undone, marked `blocked`,** when nobody is available to answer. Record the question verbatim and stop where the irreversible part starts. Never mark a question blocked before asking it.

Do not ask a question the repo or the user already answered.

## Cut the work into slices

Tactical work is one slice and has to meet only the four conditions below before it ships.

A slice ships when all four hold:

- It leaves the system working. Run the command that covers the touched area, using the before-and-after runs the "Prove the slice" section describes.
- The user can observe its result without reading the diff, through a request they can send, a screen they can open, or a command they can run.
- It is correct on its own. Half-built behavior a user can reach is a defect. So when a slice depends on a later one, ship it behind a feature flag that is off by default, or hold it until the later slice ships. Observe a flagged slice with the flag on. State the flag, how to turn it on, and the later slice that removes it.
- It is reachable from outside its own module. Give the path and line of the wiring, meaning the code that connects the slice to the rest of the system: the registered route, the render site, the caller of the exported symbol, the CLI subcommand, or the event subscription.

## Checkpoints

The sizing table says which of these three stops you must make. The operating guide is the Toby instructions file that every session loads. Its stops before commands that change the user's machine still apply at either size, and so do the stops in `toby-swd-environment`.

1. **The criteria, before the first edit.** Show the list under the heading `What done means for [task]`, then the slice cut by name. When the sizing table also requires stop 2, say so here. A yes from the user at this stop also tells you to write the plan.

Stops 2 and 3 are in `references/strategic.md`.

Never write "assuming yes, proceeding" and keep going past a stop. Doing that removes every checkpoint in this skill.

## Design before the plan

Run the `toby-swd-strategy` design pass after stop 1 and before the plan.

When the design needs a refactor first, put it first in the plan as its own step, with its cost.

Tactical work states the structure chosen, the alternative rejected, and any new signature in chat before the first edit. For strategic work, write the design lines that `references/strategic.md` lists.

## Build one slice at a time

- Build one criterion at a time. Write its test first, watch it fail, make it pass, and run it, unless `toby-swd-testing` gives a case for skipping test-first. In that case, state the case, check the criterion by hand, and quote the output.
- When the code needs a different module, boundary, or signature than the design states, stop, edit the design, and say what changed before continuing.
- Confirm every symbol this change didn't define against the installed source or the pinned manifest. A symbol can be a library function, config field, env var, CLI flag, component prop, or error type. Skip the check when this repo already calls the symbol somewhere you can cite at path:line. The version in the lockfile is the one that runs, so do not trust docs for a later version.
- Re-read a file before editing it a second time when any other edit or command ran since you last read it.
- When the change alters an existing callable, list its callers as the Brownfield Work section of `toby-swd-interfaces` describes, and put the list in the handoff.
- Commit a refactor separately, before the feature code that uses it.

## Prove the slice before starting the next

Prove each criterion by running its check before the change and again after it, as the Prove a change section of `toby-swd-testing` describes.

- A green type-check, a lint pass, or an existing suite that never runs the changed lines proves only that the repo still builds, as it did before.
- Run the change the way a user would and quote what came back. When that needs an approval-gated command, write out the command and ask for approval. Label each verification step run-by-me or for-you, and give the user only steps you could not run, each with what blocked you.

## Don't build

`references/checks.md` lists the seven things that get built without anyone asking for them. Build none of them unless a criterion requires one and that criterion's Source line quotes the user or the ticket. Read the seven before writing the plan's out-of-scope line, or before the first edit where there is no plan. Never write a criterion yourself to allow one of them, because the list exists to prevent that.

## Red flags

Before writing the handoff, check the finished work against all eight entries in `references/checks.md`. List every red flag that applied in the handoff, at file:line and under its entry name. Include the ones you fixed on the spot. When no flag applied, say so after reading all eight.

## Final response

Lead with the behavior that now exists, stated the way the user would observe it. State any unmet or unverified criterion in the first line, with its status and what is missing.

Always write these two sections before the operating guide's final-message list:

1. List each criterion in its pre-code wording, marked met, unmet, or unverified, with the check that proved it or what is missing. For multi-slice work, list each slice by name, marked done or not-done, with its evidence.
2. Give the structure chosen and the alternative rejected, in one line each. Say where the plan is, and list any step that ran differently from the approved wording.

Then give the operating guide's final-message list. Phrase each assumption that is still open as a question the user can answer in one word. List the questions this run could not resolve. List what you found and left alone, one line each, with the skill that covers each item. A missing section tells the user you checked it and found nothing.
