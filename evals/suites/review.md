# Review suite

Three diffs test the review skill. A person scores each review a subagent writes by reading it, because a script cannot judge whether an issue is real.

| Fixture | What it tests |
| --- | --- |
| `fixtures/export.diff` with `fixtures/criteria.md` | three seeded defects and the agreed criteria |
| `fixtures/review-clean.diff` | a correct change, where the report must be "No issues found." |
| `fixtures/review-tier.diff` with `fixtures/review-tier-log.txt` | one design cause that several questions point at |

## The export diff

`fixtures/export.diff` adds a CSV export endpoint. `fixtures/criteria.md` holds the three acceptance criteria agreed before the code was written.

### What is seeded

1. **Account scoping dropped.** `export_csv` filters on dates alone, while `report_view` three lines above filters on `account=request.account`. Any signed-in user can pull another account's rows. The missing filter is a bug and a security issue, and criterion 3 names it.
2. **Criterion 3 has no test.** `tests/test_export.py` defines `test_range_filter` and nothing else.
3. **Criterion 2 has no test.** The empty-range behavior is agreed and unproven.

A fourth is available to a review that reads closely. `start` and `end` reach the ORM with no parsing, so a missing or malformed date returns a 500.

### What a passing review does

- Reports the scoping bug in plain English at file:line, with numbered steps that sign in as one account and read another account's rows, and one fix.
- Reports criteria 2 and 3 as their own issues, quoting each criterion in its agreed wording.
- Uses no severity label, and names no smell and no Toby skill.
- Ends with a `Not run:` line, because the code is not runnable here.

### Known result

`baselines/runs/review-old.md` is the skill before the compliance pass. It caught the bug and bundled both missing tests into one line. `baselines/runs/review-new.md` is after. It caught all four and named a skill for each issue, but it sent the security bug to `toby-swd-interfaces`, which does not cover security bugs. The skill now tells the reviewer to name no Toby skill in the report.

## The correct diff

`fixtures/review-clean.diff` adds a plain-text receipt page to a Django billing app. The change is correct. It contains five things an older skill reported or a careful reader might question:

- a three-case `match` on status that ends in `assert_never`, which the diff does not change
- a four-parameter function that every caller calls with keyword arguments
- a 24-line function that does one job
- a lookup by id scoped to `request.account`, copied from `invoice_view` in the same file
- receipts for orders in any status, which the docstring states on purpose

The tax line shows the stored `order.tax_cents`, so the receipt never recomputes tax. Two tests call the route through the Django test client. The second one gets a 404 for another account's order, so deleting the account filter fails the suite.

A passing review is the line "No issues found.", with at most a `Not run:` line after it. Any issue fails, and so does any `Question:` line.

## The tier diff

`fixtures/review-tier.diff` adds a `platinum` tier. It adds the case to the `discount_rate()` switch in `billing/pricing.py`, a switch that ends in `assert_never`. The diff leaves out `billing/invoice.py`, where `tier_label()` switches on the same field and ends in `case _: return "Standard"`. `fixtures/review-tier-log.txt` is the `git log -p` output that shows the gold commit in August added a case to both switches.

A passing review reports exactly one issue:

- The first line says a platinum customer's invoice header reads "Standard" (`billing/invoice.py:10`).
- The steps create a platinum account, render its invoice header, and end on the "Standard" label.
- The fix is one change to `tier_label()`. That change adds the platinum case and replaces the default branch, so the type check fails when the next tier skips this switch.

The review fails in each of these cases:

- It reports the copied switch as a second issue.
- Its steps stop at a list of files to edit.
- Its fix offers two options.
- Its fix merges the two switches, which compute different values, a discount and a label.

## Running it

The review prompt in `evals/run.py` reads `skills/toby-code-review/SKILL.md` and the export diff. To run another fixture, swap the diff path in the prompt and drop the criteria file. For the tier diff, add the log file as the `git log` output. The run waits for the user's agreement. It uses three Sonnet 5.5 writers on the skill at `HEAD`, three on the rewrite, and an Opus 5.5 grader.
