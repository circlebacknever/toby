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

Report a change's real issues in plain English, and fix nothing. When the change doesn't have any of the issues below, reply `"No issues found."` without suggestions.

## Report

Write each issue in this format:

```text
1. Cancelling a shipped order refunds the customer twice (orders/cancel.py:42).
   Reproduce:
   1. Create an order and mark it shipped.
   2. Send POST /orders/{id}/cancel twice.
   3. The payments table now has two refund rows for that order.
   Fix: Return 409 from cancel() when the order status is already "refunded".

2. The SLA report will count on-hold tickets as closed once "on_hold" ships (reports/sla.py:21).
   Reproduce:
   1. Add "on_hold" to OPEN_STATES in tickets/states.py, as ticket SUP-88 asks.
   2. Put a ticket on hold, and run the SLA report.
   3. The report counts that ticket as closed.
   Fix: Delete the list at reports/sla.py:21 and import OPEN_STATES from tickets/states.py.
```

- State what goes wrong and for whom on the first line, at `file:line`, using the code's own identifiers.
- Show the wrong result in the last Reproduce step.
- Give one fix at a cited function or file, in at most a five-line code block, without alternatives.
- Report one issue per root cause, ordered from most harmful to least, without severity tags.
- Don't use pattern labels (such as shotgun surgery or SOLID), keep Toby skill names out of the findings, and don't quote the current code back.

End the report with these optional lines when they apply:

- `Not run:` listing the commands you couldn't run and each issue you found only by reading.
- At most one `Question:` line when a product decision or unreadable file settles whether an issue is real. Don't ask about a choice that the docstring or PR description states, or a guard that unchanged code relies on.

## What to check

Review the current diff unless the user gives a scope, and read a PR's description first. Report only issues the change introduces, trace each cause to its callers, and drop any issue you can't write reproduction steps for.

1. **Bugs.** Wrong output, a crash, an error hidden from a caller that needs it, or a changed contract or format that breaks callers or stored data.
2. **A bug fix without a regression test.** The steps revert the fix and show the test suite still passes.
3. **Security.** Authentication, authorization, injection, secrets, path traversal, unsafe deserialization, CSRF, SSRF, XSS, and cross-tenant data exposure. State the attacker's request and what it exposes.
4. **Acceptance criteria.** An unmet criterion from the request, ticket, or plan group. Quote the criterion and give the command or input that fails it.
5. **Repo rules.** A break of a rule in the project's `AGENTS.md` or contributing guide. Quote the rule at `path:line` and the `file:line` that breaks it.
6. **An untested entry point.** A new route, job, or consumer that no test calls through its entry point. The steps delete a required line in the handler and show the suite still passes.

When reviewing a plan or spec, read every file in it and report each promised feature that no step builds at `path:line`. Check each new entry point against `../toby-swd-hardening/SKILL.md`, and check `references/skills-diff.md` when the diff touches a `SKILL.md` or agent config.

## Design

Skip design questions on choices the user already approved in a plan.

**Module boundaries and extensibility**

Report one of these when two modules share knowledge of one format or rule, or when the request, a ticket, a TODO, or `git log` shows a follow-on change coming:

- Does an entry point compute a price, limit, or status transition rule that another entry point also needs?
- Does the diff write another module's table or parse its wire/file format directly, bypassing that module's rules?
- Does the diff pass a parameter through three or more functions that don't read it?
- Does the diff add a case to a switch on a type, status, or provider while another switch on that field falls through to a default? The fix adds the case and guards the default with `assert_never` or `never`.
- Does a subclass break its parent's contract, such as throwing `NotImplementedError` on a method callers invoke without a `supports_*()` check?

**Special cases and duplication**

Report these even without a second change in `git log`:

- Does shared code branch on one customer's id (`if account.id == 4471`)? The fix branches on a capability field (`account.bills_in_euros`).
- Do two places that must change together duplicate one business rule (such as a 30-day refund window or the list of open statuses)? Two switches on the same field that compute different things (a discount and a display label) are separate rules.
- Don't report a lookup that filters by the caller's account (`get_order(id, account)`) across entry points.

**Warning signs**

Open `toby-swd-warning-signs` and check the changed code. Report a warning sign only when the diff introduces it and the request, a ticket, a TODO, or `git log` shows a change it makes harder. State the concrete edit in `Fix:` without naming the smell or refactoring catalog entry.

## Production readiness

Check `references/production.md` whenever the diff adds or changes an entry point, job, consumer, outbound call, migration, write, check-before-write, or stored/queued format.

## Prove each issue

- Run the focused tests for the changed files, and ask before running broader checks.
- Test changed arithmetic and conditions with negative, zero, empty, and boundary values.
- Assume the code is right and search for a validation, type, framework check, or middleware guard that blocks the failure. Drop the issue unless you can explain why that guard misses. When possible, spawn a subagent per candidate issue to search for the guard.
- Claim only what your reproduction steps cause, and claim data loss only when the steps delete, overwrite, or corrupt stored data.
- Confirm your proposed fix doesn't delete anything a caller or interface requires, and count line numbers from the diff's hunk headers.

## Don't report

- Method length, naming taste, formatting, or awkward code that passes the Design section above.
- A pattern every sibling file in the repo uses, copied accurately.
- An unrecoverable error that the code rightly lets crash.
- A missing rate limit or audit log the diff didn't remove, unless `references/production.md` requires it.
- Environment variables and CLI flags as attacker-controlled input for injection, unless a request or untrusted file sets them. Still report missing startup validation on required config or secrets exposed in a client bundle.
- Anything hedged with "consider" or "might".

## Choosing the fix

When the fix is unclear, open `../<skill>/SKILL.md`:

- `toby-swd-architecture` for boundaries, special cases, and duplicated rules
- `toby-swd-modules` when two modules share one format or pass parameters through intermediate functions
- `toby-swd-extensibility` for switches and subclasses
- `toby-swd-warning-signs` for code smells and their refactorings
- `toby-swd-e2e` for untested entry points
