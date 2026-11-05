# Reports

This fixture publishes ready reports through a local API function and command function.

Run the focused checks with `python3 -m unittest discover -s tests -v`.
The `ArchiveProvider` accepts scripted receipts or exceptions and doesn't access a network.
The existing logger emits JSON to stderr through `app.telemetry.emit`.

`app.reports` defines state changes and caller-visible exceptions.
`app.routes.handle` maps domain results to status codes.
`app.cli.run_command` provides the same behavior for command callers.

## Diagnostics

Completed and failed actions emit JSON through the existing logger.
Each event includes `report_id`, `request_id`, `outcome`, and `duration_ms`.
Outcomes use `success` or `failure`, and duration is a nonnegative number in milliseconds.
Provider failures include `error_type` with the provider exception class name.
Provider exception messages can contain credentials, so logs and public responses exclude those messages.
The domain exception preserves the original provider exception as its cause for internal callers.
