---
name: toby-code-review
description: >-
  Reports the real issues in a change or a plan and edits nothing. Use it when
  the user asks to review, check, or audit a diff, a PR, a commit, a branch,
  the working tree, a plan, or a spec.
  Use it when the user asks what is wrong with a change. Skip it
  when the user wants the code changed, which toby-refactor or toby-bug-fix
  covers. Skip it for a question about how code works, which toby-explain
  covers.
---

# Toby Code Review

Report a change's real issues in plain English, and fix nothing. A finding needs a reachable trigger, a broken contract or invariant, and a concrete consequence. When the change doesn't have any of those issues, say so in a line, without suggestions.

## Report

Write each issue as the short comment a co-worker would leave, in Toby's voice:

```text
1. Cancelling an order twice refunds the customer twice (orders/cancel.py:42). `cancel()` calls `refund()` without checking the order's current status. Repeating the request creates two rows in `payments`. Reject the second cancellation with 409 when the order is already "refunded".

2. The SLA report will count on-hold tickets as closed once "on_hold" ships (reports/sla.py:21). Its list of open states is a private copy. Delete it and import `OPEN_STATES` from tickets/states.py.
```

- Start with what goes wrong and who it hits, at `file:line`, using the code's own identifiers.
- Explain how the current code causes that result. State the missing check, wrong calculation, changed field, or other causal step in the finding itself. A reproduction and a proposed repair don't replace that explanation.
- Say how to see the wrong result in one sentence.
- Give one fix, in a sentence or a code block of at most five lines.
- Report one issue per root cause, ordered from most harmful to least, without severity tags.
- Don't use pattern labels (such as shotgun surgery or SOLID), keep Toby skill names out of the findings, and don't quote the current code back.

End the report with these optional lines when they apply:

- `Not run:` listing the commands you couldn't run and each issue you found only by reading.
- At most one `Question:` line when a product decision or unreadable file settles whether an issue is real. Don't ask about a choice that the docstring or PR description states, or a guard that unchanged code relies on.

## What to check

Review the current diff unless the user gives a scope, and read a PR's description first. Read the changed code, its callers, tests, and relevant configuration. Compare the old and new behavior before calling something a regression. Trace each reported cause to a caller and a reachable consequence. A request to audit existing code also covers defects already present in that scope.

1. **Bugs.** Wrong output, a crash, an error hidden from a caller that needs it, or a changed contract or format that breaks callers or stored data.
2. **A bug fix without a regression test.** Reverting the fix leaves the test suite passing.
3. **Security.** Authentication, authorization, injection, secrets, path traversal, unsafe deserialization, CSRF, SSRF, XSS, and cross-tenant data exposure. State the attacker's request and what it exposes.
4. **Acceptance criteria.** An unmet criterion from the request, ticket, or plan group. Quote the criterion and give the command or input that fails it.
5. **Repo rules.** A break of a rule in the project's `AGENTS.md` or contributing guide. Quote the rule at `path:line` and the `file:line` that breaks it.
6. **An untested entry point.** A new route, job, or consumer that no test calls through its entry point. Deleting a required line in the handler leaves the suite passing.

When reviewing a plan or spec, read every file in it and report each promised feature that no step builds at `path:line`. Check changed entry points against `../toby-swd-hardening/SKILL.md`. Check `references/skills-diff.md` when the scope includes a skill or agent config.

## Design

Check approved designs and copied patterns against the same contracts and invariants as new code. Approval establishes intent. It doesn't establish correctness. Report the resulting harm and the smallest repair without reopening choices that still meet those requirements.

**Module boundaries and extensibility**

Trace responsibilities, shared knowledge, caller obligations, and dependency construction in the changed path. Report a boundary problem when it breaks an existing guarantee or makes a stated change require coordinated edits:

- Does an entry point compute a price, limit, permission, or status transition that differs from the operation other callers use?
- Does the diff write another module's table or parse its wire/file format directly, bypassing that module's rules?
- Does the diff pass a parameter through three or more functions that don't read it?
- Does the diff add a case to a switch on a type, status, or provider while another switch on that field goes to its default? The fix adds the case and guards the default with `assert_never` or `never`.
- Does a subclass break its parent's contract, such as throwing `NotImplementedError` on a method callers invoke without a `supports_*()` check?

**Special cases and duplication**

Report these even without a second change in `git log`:

- Does shared code branch on one customer's id (`if account.id == 4471`)? The fix branches on a capability field (`account.bills_in_euros`).
- Do two places that must change together duplicate one business rule (such as a 30-day refund window or the list of open statuses)? Two switches on the same field that compute different things (a discount and a display label) are separate rules.
- Don't report a lookup that filters by the caller's account (`get_order(id, account)`) across entry points.

**Warning signs**

Open `toby-swd-warning-signs` and check the changed code. Report a warning sign when you can trace present harm or a stated change it makes harder. State the concrete repair without naming the smell or refactoring catalog entry. Length and taste alone don't establish harm.

## Production readiness

Check the applicable questions in `references/production.md` whenever the change affects an entry point, job, consumer, outbound call, migration, write, config, failure path, or stored format. Existing functions and unchanged signatures can change those guarantees too.

## Prove each issue

- Run the focused tests for the changed files, and ask before running broader checks.
- Test changed arithmetic and conditions with negative, zero, empty, and boundary values.
- Assume the code is right and search for a validation, type, framework check, or middleware guard that blocks the failure. Drop the issue unless you can explain why that guard misses. When possible, spawn a subagent per candidate issue to search for the guard.
- Exercise the real entry point when available. For retries, concurrency, persistence, and diagnostics, inspect the resulting state or emitted output. A passing happy-path test doesn't establish those properties.
- Claim only what your reproduction steps cause, and claim data loss only when the steps delete, overwrite, or corrupt stored data.
- Confirm the proposed repair preserves caller obligations, persisted formats, and necessary error information. Use verified line numbers in the reviewed version.

## Don't report

- Method length, naming taste, formatting, or awkward code that passes the Design section above.
- A copied pattern whose callers, guards, and operational behavior satisfy the same guarantees in the changed path.
- An unrecoverable error that the code rightly lets crash.
- A missing rate limit or audit log without a reachable failure or a requirement in `references/production.md`.
- Environment variables and CLI flags as attacker-controlled input for injection, unless a request or untrusted file sets them. Still report missing startup validation on required config or secrets exposed in a client bundle.
- Anything hedged with "consider" or "might".

## Choosing the fix

When the fix is unclear, open `../<skill>/SKILL.md`:

- `toby-swd-architecture` for boundaries, special cases, and duplicated rules
- `toby-swd-modules` when two modules share one format or pass parameters through intermediate functions
- `toby-swd-extensibility` for switches and subclasses
- `toby-swd-warning-signs` for code smells and their refactorings
- `toby-swd-e2e` for untested entry points
