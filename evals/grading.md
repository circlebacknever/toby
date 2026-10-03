# Grading

## Trigger routing

The three runs used the same eight prompts. `baseline/triggering.txt` is the before run.
`evals/out/triggering-after.txt` is the after run. `evals/out/triggering-blind.txt`
is a second after run with no mention of skip clauses in the instructions, to
check whether the first run had only followed a hint.

| Run | False fires across N1-N4 | Missed across P1-P4 |
|---|---|---|
| before | 7 | 0 |
| after | 0 | 0 |
| after, blind | 0 | 0 |

The seven that stopped firing: `toby-swd-testing` on a rename, `toby-swd-complexity`
and `toby-swd-strategy` and `toby-swd-testing` on a throwaway parameter sweep, and
`toby-feature-dev` and `toby-swd-interfaces` and `toby-swd-strategy` on a one-line
field addition. Each stopped for a named phrase in its own skip clause.

## Code review, before and after

Both skills reviewed the same diff against the same criteria. The diff has one
seeded security bug and two seeded criteria with no test. The two reviews are in
`evals/out/review-old.md` and `evals/out/review-new.md`.

| | Old skill | New skill |
|---|---|---|
| Account-scoping bug | caught | caught |
| Criterion 2 unmet, no test | caught, bundled | caught, named as its own compliance finding |
| Criterion 3 unmet, no test | caught, bundled | caught, named as its own compliance finding |
| Unvalidated date params | missed | caught |
| Owning skill named | no | yes |
| Question raised for the author | no | yes, on the missing decorator |

The compliance pass separated the two criteria findings from the bug.
The old skill reported "two of three required tests don't exist" as one line
under the bug, and the new one checked each criterion against the diff and quoted
its wording.

The run exposed one defect, because the new skill routed the security bug to
`toby-swd-interfaces`, which has no rule about security bugs. The frame now says a bug or
a security finding needs no routing, because the finding already states the fix.
