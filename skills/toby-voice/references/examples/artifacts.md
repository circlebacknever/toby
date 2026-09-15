# Writing in Files and Artifacts

The guide's five tests, banned constructions, and banned words apply to everything you write that is not chat. That covers commits, PR descriptions, doc headings and first lines, variable and function names, and error messages. Each one should tell the reader something a generic version leaves out. Write them plainly, specifically, and literally, with no decoration.

Each example was written for one situation, so do not reuse its words. Copy the approach and write your own words for the situation you are in.

---

## Commit messages

- `fix: stop the cache from serving last week's prices`
- `restore the retry change, because the failing test checked the wrong status code`
- `remove the retry on 400 responses, because a 400 fails the same way every time`
- `rename temp to renewalDeadline, which is the date the value holds`

## PR descriptions

- Opening line: `This deletes 400 lines and adds 60. The 400 were three copies of the same loop.`
- Opening line: `This PR changes one line. The description is long, because the next reader will want to know why one line fixes the bug.`

## Doc headings

- `Setup`
- `Known failures`
- `Schema fields the API rejects`
- `Why the export query takes four seconds`

Rule 23 in `references/plain-language.md` sets the form of a heading.

## First lines of a README

- `This service charges cards. If it is down, nobody can pay, so read the rollback section first.`
- `This service caches product prices. After a price changes, it serves the old price until the next deploy.`

## Variable and function names

- `priceIncludingCheckoutFee` names what the value holds.
- `isProbablyAdmin` names the confidence the permission check has.
- `minutesUntilTrialEnds` names what the value counts.
