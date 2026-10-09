---
name: toby-build
description: >-
  Changes what code does, in slices the user can review one at a time. It
  proves each slice with a check run before and after the edit, and leaves the
  design at least as good as before. Use it when the user asks to
  add, build, implement, wire up, or finish a behavior, such as a feature, a
  ticket, an endpoint, a method, a screen, a job, a flag, a new status, or logs
  and metrics. Skip it for wrong output, which toby-bug-fix covers, and for
  slow code, which toby-optimize covers. Skip it when behavior stays the same,
  which toby-refactor covers, and for a throwaway, which toby-swd-experiment
  covers. Skip it for a one-file edit that copies a pattern already in that
  file. Use it for a one-file edit that adds a case to a type, kind, or status
  branch, or changes a money or permissions rule.
---

# Toby Build

When the repo already does what the user asked, say so at file:line and stop.

To open a skill, read `../<name>/SKILL.md` relative to this skill's folder. Before any command that does more than read files or print state, open `toby-swd-environment`. When the work needs a value that only a trial run can settle, such as a batch size, open `toby-swd-experiment` for that value.

## 1. Size the work

Say in one line whether the work is tactical or strategic. The work is strategic when any of these apply:

- a new module or boundary
- an API that code outside this deploy calls, such as a mobile app, a partner's server, or a package's users
- an event, or a persisted format
- a migration, unless it only adds a table or adds a column that is nullable or has a default
- a new or changed rule for auth, permissions, billing, money, or privacy
- a behavior that three or more call sites depend on
- a UI workflow that crosses more than one screen
- a new subsystem with nothing similar in the repo, such as a data store or service
- work the user expects to take more than one session

A change that only adds an optional part, such as a parameter with a default or a response field, stays tactical. So does reusing a check the repo already runs, such as an owner filter. Removing, renaming, or retyping a field, or changing what an exported function returns or what its callers must handle, makes the work strategic.

When one of these turns up partway through, switch to strategic, say so, and stay strategic.

Tactical work is one slice, with its criteria and design in chat. For strategic work, open `references/strategic.md`.

## 2. Read the code

Before designing, read the file that implements the behavior today and the test that covers it. When no test covers it, say where you searched, such as "No test in `tests/orders/` covers `cancelOrder`."

Cite a path:line for each claim about how the code behaves, or list the claim as an assumption. Before adding a helper, module, component, hook, or error type, search the repo for one. Cite the closest match, or the search that found nothing.

## 3. Write the criteria

Before any code, open `references/criteria.md` and write one criterion per behavior the request names. In strategic work, add one for a nearby behavior that must keep working. In tactical work, the criterion's Check also lists the existing tests that must keep passing.

For strategic work, open `toby-swd-e2e` before you write the Check lines.

Reread the request for a second reasonable reading. Open `references/ambiguity.md` when the two readings would build different behavior, or when the literal request leaves the user's problem unsolved.

## 4. Cut slices and stop

For strategic work, open `toby-swd-plan` before you name the slices.

A slice ships only when these hold:

- It leaves the system working.
- It is correct on its own, or hidden by a flag that is off by default. Open `toby-swd-flags` for a release flag, kill switch, or experiment flag.
- A user or caller reaches it from outside its module. Give the path:line of the wiring, such as the registered route or the render site.

At stop 1, show the criteria under `What done means for [task]`, then the slice names. Tactical work continues in the same reply. For strategic work, give the plan's path, ask whether to write the plan there, and wait for a yes. Never write "assuming yes, proceeding" past a stop.

## 5. Design

Open `toby-swd-architecture` and follow its "Default structure" when the change adds or moves a business rule, a write, or an outbound call. For every change, open `toby-swd-strategy` and run its design pass. Open `toby-swd-campfire` and answer its "Before the first edit" list. Then open each skill whose condition holds:

- Open `toby-swd-modules` for a new module or boundary.
- Open `toby-swd-interfaces` for a new or changed signature, including a parameter added with a default. Skip it for a field added beside fields of the same kind, and copy their format.
- Open `toby-swd-extensibility` when the design branches on a type, kind, status, or provider, or adds an implementation or a subclass.
- Open `toby-swd-errors` for a failure case, a retry, a timeout, or validation.
- Open `toby-optimize` for a stated time or memory budget, or a cache, batch, or queue added for speed.
- Open `toby-swd-hardening` and `toby-swd-observability` for a new entry point, job, consumer, or outbound call, or a new write or failure path in a handler. Open both for a request about logging, metrics, alerts, or hardening.
- Open `toby-swd-twelve-factor` for a new process, worker, scheduler, or scheduled job, a new config value or secret, or a new backing service.

State the structure chosen, the alternative rejected, any new signature, the one function that computes each new rule, and any refactor that runs first. A `Structure: follows <path:line>` line replaces the structure chosen and the alternative rejected. When the design depends on a guess about how a library behaves, read the library's installed code. When you cannot, ask the user before the first edit.

Before writing the plan or the first edit, read "Don't build" in `references/checks.md`.

## 6. Write the plan and stop

For strategic work, write the plan. At stop 2, the user approves the plan before the first edit.

## 7. Build one slice at a time

Before the first edit, open `toby-swd-testing`.

- Build one criterion at a time.
- Read the installed source for each library function, config field, env var, CLI flag, prop, or error type the change uses and did not define. Skip one the repo already calls at a path:line you can cite.
- When the code needs a different module, boundary, or signature than the design states, stop, edit the design, and say what changed.
- Open `toby-swd-docs` when module structure changes or the change alters an API that a README or AGENTS.md describes.

## 8. Prove the slice

Run each criterion's check before and after the change, as "Prove a change" in `toby-swd-testing` describes.

Run the change the way a user would and quote what came back. A test that drives the entry point as the `toby-swd-e2e` table says replaces that run, so open that skill and quote the test.

Then run "After the tests pass" in `toby-swd-campfire`.

## 9. Check the finished work

Before the handoff, check the work against every red flag in `references/checks.md`. Open `toby-swd-clarity` when the diff adds a public name or an interface comment.

## Final response

Lead with the behavior that now exists, as the user sees it, and any criterion left unmet or unverified. Then write the sections at the end of `references/checks.md`.
