# What done means for CSV export

1. **Observable**: a signed-in user picks a start and end date on `/reports` and gets a CSV download containing only rows in that range.
   - **Source**: the user said "Users pick a date range and get a download."
   - **Check**: fails if `pytest tests/test_export.py::test_range_filter` finds rows outside the range in the CSV.

2. **Observable**: a date range with no matching rows returns a CSV containing only the header row at HTTP 200.
   - **Source**: the user said "get a download" without an error for empty ranges.
   - **Check**: fails if `pytest tests/test_export.py::test_empty_range` gets a 204 or an error response.

3. **Observable**: a user can't export another account's rows.
   - **Source**: `app/reports/views.py:41` scopes `report_view` to `request.account`.
   - **Check**: fails if `pytest tests/test_export.py::test_scoping` returns any row belonging to another account.

4. **Observable**: the existing HTML report at `/reports` still renders unchanged.
   - **Source**: existing `report_view` behavior in `app/reports/views.py:38`.
   - **Check**: fails if the existing `/reports` view test fails.
