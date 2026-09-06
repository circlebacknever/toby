# Feature-dev sizing: two requests against the skill alone

## Request A — invite email copy change

**Mode:** Durable implementation. No experiment trigger fired (not a spike, PoC, throwaway, or tuning loop).

**Size:** Tactical. No strategic trigger fires: not a new module or boundary, not a public API/event/persisted format, not a migration, not auth/permissions/billing/money/privacy, not a behavior three-plus call sites depend on, not a multi-screen workflow, not greenfield. Default applies: "**Tactical** otherwise, which is most work."

**Gates owed at tactical:**
- Acceptance criteria: one line, in chat.
- Discovery: "the file that owns the behavior, and its test."
- Slices: one.
- Stop 1: "show them and keep moving" — no wait.
- Stop 2 (plan file): none owed at tactical.
- Stop 3: none.
- Check line: name the command, run it *after* the edit.
- Behavior record: "only when the request names a behavior" — a copy swap on one string is not a behavior in the sense the record tracks (no trigger/observable-result pair changes), so no entry.

**Judgement:** The skill's own trigger list says to skip it outright for "a one-file edit following a pattern already in that file" — this is exactly that. Even scored honestly against the tactical row, the process is heavier than the request: a one-line copy change doesn't need a named Check command or an acceptance-criteria line to be a defensible unit of work. Right call here is to just make the edit.

## Request B — per-workspace seat limits

**Mode:** Durable implementation. Nothing here reads as a spike or throwaway.

**Size:** Strategic. Deciding line: "**Strategic** when any of these fires: a new module or boundary; a public API, event, or persisted format; a migration; **auth, permissions, billing, money, or privacy**; a behavior three or more call sites depend on; a UI workflow crossing more than one screen; greenfield." Seat caps are billing/permission enforcement, and the request explicitly names three call sites (invite creation API, billing page UI, "the API too"), so two separate triggers fire independently.

**Gates owed at strategic:**
- Acceptance criteria: the three-line form (Observable / Source / Check), one per behavior. This request names at least three behaviors: invites rejected over cap with a clear message, admin sees current usage on the billing page, and the cap enforced at the API layer (not just the UI) — so at least three criteria, each with its own proof.
- Discovery: all four — the file owning the behavior, the nearest shipped sibling feature read end to end (route/handler/model/test/doc), the test covering the area today, and the call sites that would notice the change.
- Slices: named, one task group per slice — plausibly "invite rejected at the cap," "usage shown on the billing page," "API enforces the cap independent of the UI," cut by seam, not by layer.
- Stop 1: show the criteria and **wait** for a yes.
- Stop 2: a written plan file, reviewed and approved before the first edit.
- Stop 3: only at slice boundaries where the next slice depends on an answer surfaced mid-run — not automatic at every boundary.
- Check line: run the named command against today's code first and quote that output at stop 1, before any change.
- Behavior record: an entry for every criterion.

**Judgement:** Proportionate. This touches billing enforcement, crosses API and UI, and the request itself calls out that UI-only enforcement isn't good enough — that's the exact shape strategic sizing exists for, and skipping the plan/record gates here is how "reject invites" quietly ships with the cap enforceable only in the browser.
