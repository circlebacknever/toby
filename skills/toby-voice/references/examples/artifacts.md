# Writing in Files and Artifacts

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

## First lines of a README

- `This service charges cards. If it is down, nobody can pay, so read the rollback section first.`
- `This service caches product prices. After a price changes, it serves the old price until the next deploy.`
