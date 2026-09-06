# Review suite

One diff, one set of agreed criteria, three seeded defects. Scored by reading
the review a subagent writes, because no scorer can judge whether a finding is
real.

`fixtures/export.diff` adds a CSV export endpoint. `fixtures/criteria.md` holds
the three acceptance criteria agreed before the code was written.

## What is seeded

1. **Account scoping dropped.** `export_csv` filters on dates alone, while
   `report_view` three lines above filters on `account=request.account`. Any
   signed-in user can pull another account's rows. This is a bug and a security
   finding, and criterion 3 names it.
2. **Criterion 3 has no test.** `tests/test_export.py` defines `test_range_filter`
   and nothing else. The compliance pass is what catches this.
3. **Criterion 2 has no test.** The empty-range behavior is agreed and unproven.

A fourth is available to a review that reads closely: `start` and `end` reach the
ORM with no parsing, so a missing or malformed date 500s.

## What a passing review does

- Reports the scoping bug with a consequence, a trigger, and the absent guard.
- Names criteria 2 and 3 as their own compliance findings, quoting each
  criterion in its agreed wording.
- Names no severity label.
- Says the code was not run and which findings rest on reading alone.
- Routes design and coverage findings to the owning skill, and routes the bug
  nowhere, because the fix is the finding.

## Known result

`results/review-old.md` is the skill before the compliance pass. It caught the
bug and bundled both missing tests into one line. `results/review-new.md` is
after. It caught all four and named the owning skill, and it routed the security
bug to `toby-swd-interfaces`, which owns nothing about it. That last one is why
the frame now says a bug needs no routing.
