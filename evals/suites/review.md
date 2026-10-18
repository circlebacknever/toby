# Review suite

This suite tests `toby-code-review` across three diffs. A person scores each review by reading it, because a script can't judge whether a reported issue is real.

| Fixture | What it tests |
| --- | --- |
| `fixtures/export.diff` with `fixtures/criteria.md` | three seeded defects against agreed acceptance criteria |
| `fixtures/review-clean.diff` | a clean change where the review must reply `"No issues found."` |
| `fixtures/review-tier.diff` with `fixtures/review-tier-log.txt` | an incomplete switch across files that shares one root cause |

## The export diff

`fixtures/export.diff` adds a CSV export endpoint, and `fixtures/criteria.md` lists the three acceptance criteria agreed before coding.

### Seeded issues

1. **Missing account filter.** `export_csv` filters on `start` and `end` dates alone, whereas `report_view` three lines above filters on `account=request.account`. Any signed-in user can download another account's rows (`app/reports/views.py:13`), breaking criterion 3.
2. **Untested criterion 3.** `tests/test_export.py` defines `test_range_filter` and omits `test_scoping`.
3. **Untested criterion 2.** `tests/test_export.py` omits `test_empty_range`.
4. **Unvalidated date parameters.** `start` and `end` pass straight from `request.GET` to `Row.objects.filter()`, so missing (`None`) or malformed dates raise a `ValueError` / `ValidationError` and return HTTP 500.

### What a passing review does

- Reports the cross-account data exposure in plain English at `app/reports/views.py:13`, with numbered `Reproduce:` steps that sign in as one account and export another account's rows, and a `Fix:` that filters by `account=request.account`.
- Reports the unmet acceptance criteria as separate findings, quoting each criterion.
- Omits severity tags (`P1`, `High`), code-smell labels, and Toby skill names.
- Ends with a `Not run:` line stating that the tests couldn't run in this environment.

## The clean diff

`fixtures/review-clean.diff` adds a plain-text receipt endpoint to a Django billing app. The diff is free of bugs and meets all design rules:

- `status_label` uses an exhaustive `match` ending in `assert_never`.
- `render_receipt` takes keyword-only arguments and reads the stored `order.tax_cents` and `order.total_cents` without recomputing tax.
- `receipt_view` scopes its lookup with `get_object_or_404(Order, id=order_id, account=request.account)`.
- `tests/test_receipts.py` drives the endpoint through the Django test client for both the owner account (`200`) and another account (`404`).

A passing review replies `"No issues found."` (with at most a `Not run:` line). Reporting any finding or `Question:` line fails the test.

## The tier diff

`fixtures/review-tier.diff` adds a `"platinum"` tier to `Tier` and `discount_rate()` in `billing/pricing.py`, while leaving `tier_label()` in `billing/invoice.py` unchanged with `case _: return "Standard"`. `fixtures/review-tier-log.txt` shows that adding `"gold"` in August updated both switches.

A passing review reports one issue:

- The first line states that a platinum customer's invoice header renders as `"Standard"` (`billing/invoice.py:10`).
- The `Reproduce:` steps create a platinum account, call `invoice_header()`, and show that it returns `"Acme (Standard)"`.
- The `Fix:` adds the `"platinum"` case (and `"basic"`) to `tier_label()` and guards the default branch with `assert_never(tier)`.

The review fails if it reports the two switches as duplicate code to merge (since one computes a discount and the other formats a label) or offers multiple alternative fixes.
