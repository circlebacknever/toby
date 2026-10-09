---
name: toby-code-review
description: >-
  Reports the real issues in a change and edits nothing. Use it when the user
  asks to review, check, or audit a diff, a PR, a commit, a branch, or the
  working tree. Use it when the user asks what is wrong with a change. Skip it
  when the user wants the code changed, which toby-refactor or toby-bug-fix
  covers. Skip it for a question about how code works, which toby-explain
  covers.
---

# Toby Code Review

Report a change's real issues in plain English, and fix nothing. When the change has none of the issues below, the report is "No issues found." with no suggestion.

## Report

Write each issue like this:

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

- The first line says what goes wrong and for whom, at file:line, in the names the code uses.
- The last step shows the wrong result.
- The fix is one change to a function or file you cite, in at most a five-line code block. Give no alternatives.
- Report one issue per cause.
- Put the most harmful issue first, and use no severity labels.
- Use no label for a code pattern or design principle, such as shotgun surgery or SOLID. Leave out Toby skill names, and quote no code back.

Any report may end with these two lines, which are not issues.

- A `Not run:` line listing the commands you could not run and each issue you found only by reading.
- At most one `Question:` line, when a product decision or a file you cannot read settles whether an issue is real. Ask nothing about a choice the docstring or PR description states, or a guard that unchanged code in the diff relies on.

## What to check

Review the current diff unless the user gives a scope, and read a PR's description first. Report only issues the change introduces, and follow each cause to the callers it affects. Drop an issue you cannot write steps for.

1. **Bugs.** Wrong output, a crash, or an error hidden from a caller that needs it. A changed contract or stored format counts when it breaks a caller or data the diff does not update.
2. **A bug fix with no regression test.** The steps revert the fix and show the suite still passes.
3. **Security.** Authentication, authorization, injection, secrets, path traversal, deserializing untrusted data, CSRF, SSRF, XSS, and data exposure. Give the attacker's request and what it exposes.
4. **Acceptance criteria.** An unmet criterion from the request, the ticket, or the plan group the diff implements. Report each criterion as its own issue, and quote it. The steps run the command the criterion lists, or send the input it describes.
5. **Repo rules.** A break of a rule in `AGENTS.md`, `CLAUDE.md`, or a similar agent instructions file. The Reproduce block has two lines, the rule quoted at path:line and the file:line that breaks it.
6. **An untested entry point.** A new route, job, or consumer that no test calls through its entry point. The steps delete a line the feature needs and show the suite still passes.

For a change to a `SKILL.md` or to an agent's instructions file, hook, or config, also ask the questions in `references/skills-diff.md`.

## Design

Skip questions about a design choice the user approved in a plan.

**Module boundaries and extensibility**

Report one of these only when the request, a ticket, a TODO, or `git log` shows another change like this one is coming. One earlier commit counts when it made the same kind of change, such as adding a status. The steps make that change in the file a developer would edit first, and show the wrong result in a file they missed.

- Does an entry point compute a price, a limit, or whether a status may change, when a second entry point needs the same rule?
- Does the diff write another module's data, outside a migration or a test fixture, and skip a rule that module enforces?
- Does the diff add a case to a switch on a type, status, or provider, while another switch on that field returns a default value? The fix adds the missing case to the other switch and replaces its default branch with `assert_never` in Python or a `never` check in TypeScript.
- Does a subclass break its parent's contract, such as a `refund()` that throws `NotImplementedError` where the parent returns? The code is fine when callers check `supports_refunds()` first.

**Special cases and duplication**

Report these even with no sign of another change. The steps change one copy of the rule, or add a second customer with the same need.

- Does shared code gain a branch for one customer's id, such as `if account.id == 4471:`? The fix branches on an account field that says why this customer differs, such as `account.bills_in_euros`.
- Is one rule, such as a 30-day refund window or a list of open statuses, written in two places that must change together? Two switches on one field that compute different values, such as a discount and a label, are two rules.
- Do not report a lookup by id scoped to the signed-in account, such as `get_order(id, account)`, repeated in each entry point.

## Production readiness

Ask the questions in `references/production.md` when the diff adds an entry point, job, consumer, outbound call, migration, write, or check before a write. Ask them too when it changes a stored or queued format.

## Prove each issue

- Run the tests for the changed files, or the changed code, and ask before anything broader.
- Try changed arithmetic and conditions with negative, zero, and empty values, and on each side of each boundary.
- Assume the code is right, and search for a guard that stops the failure, such as a validation, a type, the framework, or middleware. Drop the issue unless you can say why that guard misses. When you can, give each issue's search to its own subagent, with the changed files and every file the issue cites.
- Claim only what the input in your steps causes. Claim data loss only when your steps delete, overwrite, or corrupt stored data.
- Check that the fix deletes nothing an interface or a caller needs.
- Count line numbers from the diff's hunk headers.

## Don't report

- Method length, naming taste, style a formatter catches, and code that is correct but awkward.
- A pattern every similar file in the repo uses, copied correctly.
- An error the code rightly lets crash the program.
- A missing rate limit or audit log that the diff did not remove, unless `references/production.md` asks about it.
- Environment variables and CLI flags as untrusted input.
- Anything you would write with "consider" or "might".

## Choosing the fix

When the fix is unclear, open the skill for the issue's area at `../<skill>/SKILL.md`.

- `toby-swd-architecture` for boundaries, special cases, and copied rules
- `toby-swd-extensibility` for a switch or a subclass
- `toby-swd-e2e` for an untested entry point
