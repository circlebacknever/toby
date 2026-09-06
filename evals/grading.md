# Grading

## Trigger routing

Same eight prompts, three runs. `baseline/triggering.txt` is the before run.
`evals/out/triggering-after.txt` is the after run. `evals/out/triggering-blind.txt`
is a second after run with no mention of skip clauses in the instructions, to
check the first run was not just following a hint.

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

Same diff, same criteria, one seeded security bug and two seeded criteria with
no test. `evals/out/review-old.md` and `evals/out/review-new.md`.

| | Old skill | New skill |
|---|---|---|
| Account-scoping bug | caught | caught |
| Criterion 2 unmet, no test | caught, bundled | caught, named as its own compliance finding |
| Criterion 3 unmet, no test | caught, bundled | caught, named as its own compliance finding |
| Unvalidated date params | missed | caught |
| Owning skill named | no | yes |
| Question raised for the author | no | yes, on the missing decorator |

The compliance pass is what separated the two criteria findings from the bug.
The old skill reported "two of three required tests don't exist" as one line
under the bug; the new one checked each criterion against the diff and quoted
its wording.

One defect the run exposed: the new skill routed the security bug to
`toby-swd-interfaces`, which owns nothing about it. The frame now says a bug or
a security finding needs no routing, because the fix is the finding.
