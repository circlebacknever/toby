Not runnable here — no repo, just the diff and criteria. Findings rest on reading alone.

## Findings

**Export leaks every account's rows — no account scope on the query.**
- Consequence: any signed-in user who hits `/reports/export/` gets rows from every account, not just their own (app/reports/views.py, `export_csv`, `rows = Row.objects.filter(created__gte=start, created__lte=end)`).
- Fires when: an authenticated user requests `GET /reports/export/?start=...&end=...` with any valid date range — no account check gates the query at all.
- Guard: none — `report_view` two lines up scopes the same model with `Row.objects.filter(account=request.account)` (views.py:41 in the diff context); `export_csv` drops that clause. Criteria item 3 names this exact scoping requirement and it's unmet.
- Fix direction: add `account=request.account` to the filter in `export_csv`.

**Two of three required tests don't exist.**
- Consequence: criteria items 2 and 3 (`test_empty_range`, `test_scoping`) have no corresponding test — only `test_range_filter` is in the diff.
- Fires when: someone runs the acceptance checks as written in criteria.md; `pytest tests/test_export.py::test_empty_range` and `::test_scoping` fail to collect.
- Guard: none — `tests/test_export.py` is a new file with a single test function.
- Fix direction: add both tests; `test_scoping` is the one that would have caught the finding above.

## Verification gap

None of the tests ran — no repo to run them in, just the diff. `test_range_filter` itself is unverified, and the two missing tests can't be written or run in this environment either.
