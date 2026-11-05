# Repair archiving

Fix the report archive failure using the supplied bug-fix skill.

Read `.toby-skills/toby-bug-fix/SKILL.md` and follow its references for this task.
Fixture edits, focused tests, and any plan needed for this isolated task are approved.
Finish the whole task without waiting at plan stops. The provider is local and deterministic.
Don't inspect the source eval runner, its graders, or other completed fixture workspaces.

When the archive provider fails, the API currently reports success and a retry never archives the report.
The failure log doesn't identify the report, request, or cause.
The existing regression reproduces the first wrong result with `python3 -m unittest discover -s tests -v`.
Repair the cause and the diagnostics, preserving the public domain operation and both entry points.

- A ready report becomes `archived`, with `archive_id` taken from the provider's `receipt` field.
- The API and command return status 200 with `report_id`, `state`, and `archive_id` in `body`.
- An archived report returns its original receipt without calling the provider again.
- A report in any other state raises `InvalidState` in the domain operation and returns 409 through the entry points.
- `ProviderUnavailable` raises `ArchiveUnavailable` from the original exception and returns 503 through the entry points.
  The report stays ready with an empty archive id, so a later retry can succeed.
- Preserve publishing and the unknown-action response.

Update the module explanation so a caller can understand normal use and retry behavior.
