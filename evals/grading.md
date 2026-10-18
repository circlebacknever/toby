# Grading

## Trigger routing

The three runs used the same eight prompts. `evals/baselines/triggering-before.txt` holds the run before skip clauses, `evals/baselines/runs/triggering-after.txt` holds the run after, and `evals/baselines/runs/triggering-blind.txt` holds the blind confirmation run.

| Run | False fires across N1-N4 | Missed across P1-P4 |
|---|---|---|
| before | 7 | 0 |
| after | 0 | 0 |
| after, blind | 0 | 0 |

Seven false firings stopped after the skip-clause update: `toby-swd-testing` on a rename, `toby-swd-errors`, `toby-swd-strategy`, and `toby-swd-testing` on a throwaway parameter sweep, and `toby-build`, `toby-swd-interfaces`, and `toby-swd-strategy` on a one-line field addition.

## Code review, before and after

Both versions of the skill reviewed the same diff against the same criteria. The diff has one seeded security bug and two seeded criteria without tests. The two reviews are in `evals/baselines/runs/review-old.md` and `evals/baselines/runs/review-new.md`.

| Check | Old skill | New skill |
|---|---|---|
| Account-scoping bug | caught | caught |
| Criterion 2 unmet, missing test | caught, bundled | caught as its own finding |
| Criterion 3 unmet, missing test | caught, bundled | caught as its own finding |
| Unvalidated date params | missed | caught |
| Toby skill named in finding | no | yes |
| Question raised for the author | no | yes, on the missing decorator |

The compliance pass separated the two criteria findings from the bug. The old skill bundled both missing tests into one line under the bug, while the new skill checked each criterion against the diff and quoted its wording.

The run also exposed one defect: the new skill routed the security bug to `toby-swd-interfaces`, which doesn't cover security bugs. `toby-code-review` now keeps Toby skill names out of the review findings.
