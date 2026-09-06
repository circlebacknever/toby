## Findings

**Broken account scoping on the export endpoint (app/reports/views.py, `export_csv`).** Any signed-in user can pull another account's report data — date, sku, amount — through this endpoint.
**Fires when** a request hits `/reports/export/?start=...&end=...`: the query is `Row.objects.filter(created__gte=start, created__lte=end)`, filtered only by date.
**Guard:** none — `report_view`, three lines above in the same diff, filters `Row.objects.filter(account=request.account)`; `export_csv` drops that clause. Route to toby-swd-interfaces.

**Unvalidated `start`/`end` query params (app/reports/views.py, `export_csv`).** A malformed or missing date string reaches the ORM filter untouched and Django raises on the cast, so the endpoint 500s instead of failing predictably.
**Fires when** `/reports/export/` is hit with no `start`/`end` or a non-date value for either — both fall straight into `created__gte=start, created__lte=end` with no parsing.
**Guard:** none — `start = request.GET.get("start")` and `end = request.GET.get("end")` are used as-is. Route to toby-swd-complexity.

**Compliance — criterion 3 unmet.** Criterion: "a user cannot export another account's rows by changing the account id in the request." Same root cause as the scoping finding above: the query never references `request.account`, and `tests/test_export.py` has no `test_scoping`.

**Compliance — criterion 2 unmet.** Criterion: "a range with no rows returns a CSV with the header row and nothing else, at HTTP 200." `tests/test_export.py` defines only `test_range_filter`; there is no `test_empty_range`, so nothing in the diff checks this path.

## Question

Does `export_csv` need the same auth/permission decorator as `report_view`, or is that handled by middleware? The diff hunk starts below `report_view`'s body, so any decorator on it is out of view — worth confirming before trusting the account-scoping fix alone to close the gap.

## Verification

Not runnable here — no repo, only the diff and criteria.md. The account-scoping and validation findings are read from the code; none of the three `tests/test_export.py` checks were executed.
