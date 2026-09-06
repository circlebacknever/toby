# What done means for CSV export

1. **Observable** — a signed-in user picks a start and end date on /reports and gets a
   CSV download containing only rows in that range.
   **Source** — user: "Users pick a date range and get a download."
   **Check** — `pytest tests/test_export.py::test_range_filter`. Unmet if rows outside
   the range appear in the file.

2. **Observable** — a range with no rows returns a CSV with the header row and nothing
   else, at HTTP 200.
   **Source** — user: "get a download" with no exception named for the empty case.
   **Check** — `pytest tests/test_export.py::test_empty_range`. Unmet if the endpoint
   returns 204 or an error page.

3. **Observable** — a user cannot export another account's rows by changing the
   account id in the request.
   **Source** — repo fact, app/reports/views.py:41 scopes every other report query to
   request.account.
   **Check** — `pytest tests/test_export.py::test_scoping`. Unmet if a foreign account
   id returns any row.

**Stays working** — the existing HTML report at /reports renders unchanged.
