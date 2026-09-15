# Artifact tasks

Seven outputs, one for each kind of written artifact: code comments, a review, a
plan, a diagram, slide copy, chart text, and a PR description. Each task gives
raw material and names the skill files a writer reads before writing it. Frozen
on 2026-09-14 before any writer ran.

Use only what the material shows, plus arithmetic on it and standard knowledge of
the language or tool the task names.

## 1. Code comments

Skill files: `skills/toby-swd-clarity/SKILL.md`,
`skills/toby-swd-clarity/references/examples.md`

Add the interface docstring and any other comments this function needs. Return
the whole function.

```python
def fetch_with_retry(session, url, attempts=4, base_delay=0.5):
    last_error = None
    for attempt in range(attempts):
        try:
            response = session.get(url, timeout=10)
            if response.status_code < 500:
                return response
            last_error = RuntimeError(f"server error {response.status_code}")
        except requests.ConnectionError as error:
            last_error = error
        if attempt < attempts - 1:
            time.sleep(base_delay * 2 ** attempt)
    raise last_error
```

Facts:

- `billing/sync.py` calls this function for the invoice API.
- The invoice API returns 409 for a duplicate invoice, and the caller handles a
  409 itself.

## 2. Code review

Skill file: `skills/toby-code-review/SKILL.md`

Review this diff against the agreed criteria. You cannot run the code.

```diff
--- a/app/reports/views.py
+++ b/app/reports/views.py
@@ -38,6 +38,26 @@ def report_view(request):
     rows = Row.objects.filter(account=request.account)
     return render(request, "reports/index.html", {"rows": rows})
 
+def export_csv(request):
+    start = request.GET.get("start")
+    end = request.GET.get("end")
+    rows = Row.objects.filter(created__gte=start, created__lte=end)
+
+    response = HttpResponse(content_type="text/csv")
+    response["Content-Disposition"] = 'attachment; filename="report.csv"'
+    writer = csv.writer(response)
+    writer.writerow(["date", "sku", "amount"])
+    for row in rows:
+        writer.writerow([row.created, row.sku, row.amount])
+    return response
--- a/app/reports/urls.py
+++ b/app/reports/urls.py
@@ -3,4 +3,5 @@ from . import views
 urlpatterns = [
     path("reports/", views.report_view, name="reports"),
+    path("reports/export/", views.export_csv, name="export"),
 ]
--- /dev/null
+++ b/tests/test_export.py
@@ -0,0 +1,9 @@
+def test_range_filter(client, account, rows):
+    response = client.get("/reports/export/?start=2026-01-01&end=2026-01-31")
+    assert response.status_code == 200
+    body = response.content.decode()
+    assert "2026-01-15" in body
+    assert "2025-12-30" not in body
```

Agreed criteria:

1. A signed-in user picks a start and end date on /reports and gets a CSV
   download containing only rows in that range. Check:
   `pytest tests/test_export.py::test_range_filter`.
2. A range with no rows returns a CSV with the header row and nothing else, at
   HTTP 200. Check: `pytest tests/test_export.py::test_empty_range`.
3. A user cannot export another account's rows. Check:
   `pytest tests/test_export.py::test_scoping`.

## 3. Plan document

Skill files: `skills/toby-feature-dev/SKILL.md` (the section "The plan
document"), `skills/toby-feature-dev/references/examples.md`, and the Plan
Format section of the guide

The user approved writing a plan. Write the plan document.

Request: "Add per-workspace seat limits. When a workspace hits its seat cap, new
invites should be rejected with a clear message, and admins should see the
current usage on the billing page. Enforce it on the API too, not just the UI."

Repo facts:

- `api/invites.ts` defines `createInvite(workspaceId, email, actor)`.
- `api/billing.ts` defines `getPlan(workspaceId)`, which returns `{ seatCap }`.
- `api/members.ts` defines `countMembers(workspaceId)`.
- `screens/Members.tsx` holds the invite form.
- `screens/Billing.tsx` shows the plan name and price.
- API tests are in `tests/api/`, and `pnpm test` runs them.
- Mode: durable implementation.

## 4. Diagram

Skill file: `skills/toby-artifact-style/SKILL.md` (the section "Copy rules")

Write a Mermaid flowchart of the install choices, with a title, and a caption of
at most two sentences under it.

Material:

```
$ scripts/install.sh --help
Usage: scripts/install.sh [--tool codex|claude|copilot|github|kiro|all] [--output-style] [--dry-run] [--force]
  --hooks         Install the voice checker and the two hooks to
                  ~/.claude/toby, then print the settings.json block to
                  paste. Does not edit settings.json itself.
  --output-style  Claude Code only. Install the writing rules as an output
                  style, and install the shorter CLAUDE.md that leaves them
                  out. Costs about 200 tokens more than the default, and
                  puts the rules in the system prompt. You must then turn
                  the style on: /config, Output style, Toby. Without that
                  step the voice rules are not loaded at all.
```

Without `--output-style`, the installer writes the full guide into `CLAUDE.md`.

## 5. Slide copy

Skill files: `skills/toby-artifact-style/SKILL.md` (the section "Copy rules"),
`skills/toby-artifact-style/references/decks.md` (the section "Shared slide
content rules"), `skills/toby-artifact-style/references/copy.md`

Write the copy for four content slides: a title and the body text for each. The
deck reports this trial to the team.

Material:

| Writer model | Outputs per guide | Fails per 1,000 words, current guide | Fails per 1,000 words, core guide |
|---|---|---|---|
| Haiku | 5 | 35.8 | 28.1 |
| Sonnet | 5 | 19.6 | 14.0 |
| Opus | 5 | 3.1 | 3.6 |
| Fable | 2 | 13.0 | 7.0 |

- The current guide is 9,539 tokens. The core guide is 2,165 tokens.
- Opus graded each output twice without knowing the guide. The two runs agreed
  on 328 of 404 distinct failing sentences.
- The team adopted the core guide.

## 6. Chart text

Skill files: `skills/toby-artifact-style/references/charts.md`,
`skills/toby-artifact-style/references/copy.md`

The chart is a grouped bar chart of the table in task 5: one group per writer
model, one bar per guide. Write its title, both axis labels, the legend entries,
a caption of at most two sentences, and the source note.

## 7. PR description

Skill file: `skills/toby-voice/references/examples/artifacts.md`

Write the PR description for this diff.

```diff
--- a/skills/toby-code-review/SKILL.md
+++ b/skills/toby-code-review/SKILL.md
@@ -31,9 +31,9 @@
-Write each finding as three short lines. If you can't fill them from the file in front of you, there's no finding, so drop it.
+Write each finding as three labelled lines, and make each line a whole sentence. If you can't fill them from the file in front of you, there's no finding, so drop it.
-- **Consequence** — This line says in plain words what breaks and for whom, at file:line. An example is "returns last month's balance to a logged-in user on first load (api/account.ts:42)."
+- **Consequence** — This line says in plain words what breaks and for whom, at file:line. An example is "The account page returns last month's balance to a logged-in user on first load (api/account.ts:42)."
```

The change came from a review where findings were written as fragments, and the
user could not follow them.
