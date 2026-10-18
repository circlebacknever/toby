---
name: toby-build
description: >-
  Changes what code does, in slices the user can review one at a time. It
  proves each slice with a check run before and after the edit, and leaves the
  design at least as good as before. Use it when the user asks to
  add, build, implement, wire up, or finish a behavior, such as a feature, a
  ticket, an endpoint, a method, a screen, a job, a flag, a new status, or logs
  and metrics. Use it to add or change a feature in a plan or a spec.
  Skip it for wrong output, which toby-bug-fix covers, and for
  slow code, which toby-optimize covers. Skip it when behavior stays the same,
  which toby-refactor covers, and for a throwaway, which toby-swd-experiment
  covers. Skip it for a one-file edit that copies a pattern already in that
  file. Use it for a one-file edit that adds a case to a type, kind, or status
  branch, or changes a money or permissions rule.
---

# Toby Build

When the repo already does what the user asked, say so at file:line and stop.

To open a skill, read `../<name>/SKILL.md` relative to this skill's folder. Open `toby-swd-environment` before any state-changing, runtime-affecting, destructive, or full-repo command, or during user-led verification. When the work needs a value that only a trial run can settle, such as a batch size, open `toby-swd-experiment` for that value.

## 1. Size the work

State `Mode: durable implementation (tactical)` or `Mode: durable implementation (strategic)` in one line. The work is strategic, and needs a written plan, when any of these apply:

- a new module or boundary
- an API that code outside this deploy calls, such as a mobile app, a partner's server, or a package's users
- an event, or a persisted format
- a migration, unless it only adds a table or adds a column that is nullable or has a default
- a new or changed rule for auth, permissions, billing, money, or privacy
- a behavior that three or more call sites depend on
- a UI workflow that crosses more than one screen
- a new subsystem without a similar one in the repo, such as a data store or service
- work the user expects to take more than one session

Adding an optional parameter with a default or a response field, or reusing an existing check such as an owner filter, stays tactical. Removing, renaming, or retyping a field, or changing what an exported function returns or what its callers must handle, is strategic. When a strategic trigger turns up mid-build, switch to strategic, say so, and stay strategic.

Tactical work is one slice, with its criteria and design in chat. For strategic work, open `references/strategic.md`.

## 2. Read the code

Read the file that implements the behavior today, its tests, and every place that reads, renders, stores, or documents the touched behavior. When you don't find a test, state where you searched, such as "`tests/orders/` doesn't have a test for `cancelOrder`." Include every caller or doc the change breaks in the work.

Cite `path:line` for each claim about how the code behaves, or mark it as an assumption. Before adding a helper, module, component, hook, or error type, search the repo and cite the closest match or the search that found none.

## 3. Write the criteria

1. Picture how the user will use the finished result, and open `references/criteria.md`.
2. Write one criterion per behavior the result needs, plus one for a nearby behavior that must keep working in strategic work (in tactical work, list the existing tests in the Check).
3. For strategic work, open `toby-swd-e2e` before writing the Check lines.

Take the reading that covers the whole request and solves the user's problem. Open `references/ambiguity.md` only when two readings fit the words and neither has a usual answer under the operating guide's Decisions section.

## 4. Cut slices and stop

For strategic work, open `toby-swd-plan` before naming the slices. Each slice ships only when:

- It leaves the system working.
- It is correct on its own, or hidden behind an off-by-default flag (`toby-swd-flags`).
- A user or caller reaches it from outside its module, at a cited `path:line` such as a registered route or render site.

At stop 1 of strategic work, show the three-line criteria under `What done means for [task]`, the slice names, and the plan's path, offer to write the plan there, and wait. Tactical work states each criterion on one line in chat and continues in the same reply. Never write "assuming yes, proceeding" past a stop.

## 5. Design

When the change copies a nearby structure or passes an optional parameter unchanged, write `Structure: follows <path:line>` and skip `toby-swd-strategy` and `toby-swd-interfaces`. Otherwise open `toby-swd-strategy` and run its design pass, and open `toby-swd-architecture` when the change adds or moves a business rule, a write, or an outbound call.

Open `toby-swd-campfire` and run its "Before the first edit" check. Then open each skill whose condition holds:

- Open `toby-swd-modules` for a new module or boundary, or when a value threads through functions that don't read it.
- Open `toby-swd-interfaces` for a new or changed signature that callers must handle.
- Open `toby-swd-extensibility` when the design branches on a type, kind, status, or provider, or adds an implementation or subclass.
- Open `toby-swd-errors` for a failure case, retry, timeout, or validation.
- Open `toby-optimize` for a stated time or memory budget, or a cache, batch, or queue added for speed.
- Open `toby-swd-hardening` and `toby-swd-observability` for a new entry point, job, consumer, outbound call, write, or failure path, or any request about logs, metrics, alerts, or hardening.
- Open `toby-swd-twelve-factor` for a new process, worker, scheduled job, config value, secret, or backing service.

State the structure chosen, the alternative rejected, any new signature, the one function that computes each new rule, and any preparatory refactor (or `Structure: follows <path:line>`). Read the installed source of any library behavior the design relies on, or state it as an assumption. Read "Don't build" in `references/checks.md` before writing the plan or the first edit.

## 6. Write the plan and stop

For strategic work, write the plan and stop for approval at stop 2 before the first edit.

## 7. Build one slice at a time

Open `toby-swd-testing` before the first edit.

- Build one criterion at a time.
- Read the installed source for each library function, config field, env var, CLI flag, prop, or error type the change uses and didn't define, unless the repo already calls it at a `path:line` you cite.
- When the code needs a different module, boundary, or signature than the design states, stop, update the design, and state what changed.
- Open `toby-swd-docs` when module structure changes or the change alters an API described in a `README.md` or `AGENTS.md`.

## 8. Prove the slice

Run each criterion's check before and after the change in the form `toby-swd-testing` gives. Run the change the way a user would and quote the output, or open `toby-swd-e2e` and quote the entry-point test. Then run "After the tests pass" in `toby-swd-campfire`.

## 9. Check the finished work

Check the work against every red flag in `references/checks.md`. Open `toby-swd-clarity` when the diff adds a public name or an interface comment.

## Final response

Lead with the behavior that now exists as the user sees it, and any criterion left unmet or unverified. Then write the sections at the end of `references/checks.md`.
