# Report tasks

Three chat replies that a user reads at the end of long work. Each task gives every fact the reply needs, and the facts use the labels and ids that the work used internally. The reader of each reply saw none of the work. This suite was written on 2026-10-08 for the readable-rules change, so its results are weaker evidence than `holdout`.

## 1. Final report after a long change

The user asked the agent to add per-account rate limits to the Harbor payments API, then left. Write the agent's final chat message to the user.

Facts:

- The work followed ticket PAY-212, phases 2a and 2b.
- `api/middleware/ratelimit.py` is new. It limits each account to 600 requests a minute across all routes.
- `api/routes/charges.py`, `api/routes/refunds.py`, and `api/routes/payouts.py` lost their own per-route limit code.
- `pytest tests/test_ratelimit.py` ran and passed 14 of 14 tests.
- The CI job `int-e2e-7` was not run, because it needs staging credentials the agent does not have.
- The limit is behind the flag `RL_STRICT`, which is off by default.
- Before this change, an account could send 600 requests a minute to each route.
- The user has to decide whether to turn `RL_STRICT` on in staging before Friday's release.

## 2. Review summary for a product owner

The product owner asked for a review of a pull request that adds CSV export to the Harbor reports page. They will not read the diff. Write the chat reply that summarizes the review for them.

Facts:

- Finding F1, severity P1: `export_csv` in `reports/views.py:88` has no login check, so anyone with the URL can download any account's report.
- Finding F2, severity P3: the export has no test for an empty report.
- Finding F3 was dropped after a recheck, because the date filter is validated in `reports/forms.py:14`.
- The review was done by reading the diff. The code was not run.
- The fix for F1 is to add the `@login_required` decorator and check that the report belongs to the user's account.

## 3. Reply to "what does that mean?"

Earlier in the chat the agent sent this message to the user:

> The g2 gate regressed on the buried-lead class (10 → 11) after the B3 edit, so I reverted B3 and re-ran; all gates hold, and the residual is the two sense-scoped hits in A1, which are pre-existing.

The user replied: "what does that mean?" Write the agent's next reply.

Facts:

- The repo has an automated check that runs with no AI model and counts style warnings by type.
- One warning type flags a section whose first sentence states background before stating the rule. The count of those warnings rose from 10 to 11 after the agent's third edit to the skill files.
- The agent undid that edit and ran the check again, and every count was back to its recorded level.
- Two warnings remain in the first file the agent edited. They flag the word "shape", and both were there before the agent started.
