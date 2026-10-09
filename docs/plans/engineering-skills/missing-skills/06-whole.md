# Group 6: one held-out feature request reads correctly through every skill it opens

This group meets criteria 5, 8, and 9 in the overview. Its owner edits `scripts/validate-skills.py`, `scripts/token-budget.py`, `README.md`, and `docs/plans/engineering-skills/`.

## Steps

- [x] Update `ROUTING_GROUPS` in `scripts/validate-skills.py` and the scenarios in `scripts/token-budget.py` for the new, renamed, and moved skills and references. Keep the existing group keys, because the gates compare each key with its baseline.
- [x] Update the README skill list with the final names. Replace the inline list of hidden skills with one sentence. Add one sentence saying the hardening, twelve-factor, observability, flags, end-to-end, and architecture skills come from running services, which neither source book covers.
- [x] Move the earlier plan's flat files and `lost-rules.txt` from `docs/plans/engineering-skills/` to `docs/plans/engineering-skills/first-pass/`.
- [x] Run `python3 skills/toby-voice/scripts/voice-check.py --review` on every new or changed prose file. Fix each FIX line, answer each DECIDE line, and read every sentence against the READ list.
- [x] Give one Opus subagent every new and changed skill, and ask it to quote each sentence that reads as machine-written, with a rewrite. Apply the rewrites that keep the meaning.
- [x] Run `grep -rn` for every removed or renamed name and path across `skills`, `base`, `scripts`, `evals`, and `README.md`. Fix each stale pointer.
- [x] Run `python3 evals/run.py gates` and keep its output for the final report.
- [x] Walk twelve small-app requests through each entry skill and every skill it opens, such as a CSV export, a CLI option, a library argument, and a notes field. Give each finding to two verifiers, one that checks the over-building is real and one that checks the fix keeps every needed safeguard. Apply the findings that pass both.

## Verification

- Give an Opus subagent the request "add a team inbox where support agents claim a ticket, and a Slack message goes out when a ticket waits an hour", over several sessions. Walk it through `toby-build` and every skill that build opens. Ask it to quote any sentence that would lead to a rule in a route handler, a timer inside the web process, a Slack call with no timeout, a claim that two agents can both win, a plan in one file, or a plan with no test through the whole feature. A quote that holds up sends the work back to the group that owns the file.
- Give a second subagent the full diff and the user's original request, and ask which goal is still unmet. A goal it can show unmet with a quoted line goes back to its group.
- Walk the same twelve small-app requests again after the fixes. A quoted sentence that still adds code the request does not need, or a safeguard a scenario needs that no sentence still requires, sends the work back to the group that owns the file.
- Run `python3 scripts/validate-skills.py`, `bash scripts/sync.sh --check`, and `python3 tests/test-voice-hook.py`. Any error fails this group.
