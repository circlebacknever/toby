# Report tasks

This suite has three chat replies that a user reads at the end of a task. The task facts include internal IDs and labels from the work, and the reader of each reply hasn't seen those internal labels.

## 1. Final report after a long change

The user asked the agent to add per-account rate limits to the Harbor payments API, then stepped away. Write the agent's final chat message to the user.

Facts:

- The work completed ticket PAY-212, phases 2a and 2b.
- `api/middleware/ratelimit.py` is a new middleware that limits each account to 600 requests a minute across all routes.
- You removed the per-route rate-limit checks from `api/routes/charges.py`, `api/routes/refunds.py`, and `api/routes/payouts.py`.
- `pytest tests/test_ratelimit.py` ran and passed 14 of 14 tests.
- You didn't run the CI job `int-e2e-7`, because it requires staging credentials you don't have.
- The new middleware runs behind the release flag `RL_STRICT`, which defaults to off.
- Before this change, an account could send 600 requests a minute to each route separately.
- The user needs to decide whether to enable `RL_STRICT` in staging before Friday's release.

## 2. Review summary for a product owner

The product owner asked for a review of a pull request that adds CSV export to the Harbor reports page, and won't read the code diff. Write the chat reply that summarizes the review for them.

Facts:

- Finding F1, severity P1: `export_csv` in `reports/views.py:88` doesn't check whether the caller is signed in, so anyone with the URL can download any account's report.
- Finding F2, severity P3: the test suite doesn't test exporting an empty report.
- You dropped candidate finding F3 after checking `reports/forms.py:14`, which already validates the date filter.
- You reviewed the PR by reading the diff and didn't run the code.
- The fix for F1 adds `@login_required` and scopes the report query to the signed-in user's account.

## 3. Reply to "what does that mean?"

Earlier in the chat the agent sent this message to the user:

> The g2 gate regressed on the buried-lead class (10 → 11) after the B3 edit, so I reverted B3 and re-ran; all gates hold, and the residual is the two sense-scoped hits in A1, which are pre-existing.

The user replied: "what does that mean?" Write the agent's next reply in plain everyday English.

Facts:

- The repo has a script that checks the skill markdown files and counts style warnings by category.
- One warning category flags a section whose first sentence states background before stating the rule. That count rose from 10 to 11 after the agent's third edit.
- The agent undid that edit and reran the script, bringing all warning counts back to their baseline numbers.
- Two warnings remain in the first file the agent edited. Both flag the word `shape` and existed before this session started.
