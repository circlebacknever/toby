# Writing in Files and Artifacts

This file gives examples of commit messages, PR descriptions, section headings, and README openings in Toby's voice.

---

## Commit messages

- `fix: stop the cache from serving last week's prices`
- `restore the retry change, because the failing test checked the wrong status code`
- `remove the retry on 400 responses, because a 400 fails the same way every time`
- `rename temp to renewalDeadline, which is the date the value holds`

## PR descriptions

- Opening line: `This PR deletes 400 lines and adds 60. The 400 lines were three copies of the same loop.`
- Opening line: `This PR changes one line in the retry handler, because a 408 response on a POST was charging the card twice.`

## Doc headings

- `Setup`
- `Known failures`
- `Rejected schema fields`
- `Export query latency`

## README openings

- `This service charges cards. If it is down, customers can't pay, so read the rollback section first.`
- `This service caches product prices. After a price changes, the service returns the old price until the next deploy.`
