# Writing in Files and Artifacts

The Prose, Register, and Banned Words rules apply to everything you write that is not chat. That covers commits, PR descriptions, doc headings and first lines, variable and function names, and error messages. Each one should tell the reader something a generic version leaves out. Write them plainly, specifically, and literally, with no decoration.

These examples are single-use. Copy the approach and write your own words for the moment in front of you.

---

## Commit messages

- `fix: stop the cache from serving last week's prices`
- `revert the revert: the first version was right and the test was wrong`
- `remove the retry on 400s: it was four guaranteed failures with a delay between them`
- `rename temp to renewalDeadline, which is what it has held since 2021`

## PR descriptions

- Opening line: `This deletes 400 lines and adds 60. The 400 were three copies of the same loop.`
- Opening line: `One-line change, long description, because the next person will want to know why one line was enough.`

## Doc headings

- `Setup`
- `Known failures`
- `Schema fields the API rejects`
- `Why the export query takes four seconds`

Rule 23 in `references/plain-language.md` sets the form of a heading.

## First lines of a README

- `This service charges cards. If it is down, nobody can pay, so read the rollback section first.`
- `This is a cache. It is correct until the source data changes, and wrong from then until the next deploy.`

## Variable and function names

- `priceIncludingTheFeeWeDontShowUntilCheckout` names what the value holds.
- `isProbablyAdmin` names the confidence the permission check has.
- `minutesUntilTheTrialQuietlyEnds` names the moment the user finds out.
