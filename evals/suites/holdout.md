# Held-out tasks

This suite has six tasks on a product, an incident, and a chat session that no rule in this repo was tuned against. Each task gives all the facts the output needs, and a writer that invents a fact fails the task.

## 1. Tool overview

Write the top of the README for Ledgerline: a title, an opening paragraph of at most 80 words, then two sections (`Install` and one about adding a bank format) with one short paragraph each.

Facts:

- Ledgerline is a command-line tool that reconciles bank CSV exports against an accounting system.
- It reads exports from four banks: Chase, Monzo, Wise, and ING.
- It matches a bank row to a ledger entry when the amounts match and the dates are within 2 days of each other.
- The parser writes each unmatched row to `review.csv` for a person to check.
- It reads the accounting system through an API token with read-only scope.
- A bank format is a parser in `parsers/<bank>.py`. Parsers must not make network calls, and CI fails any parser that imports `requests` or `httpx`.
- Install with `brew install ledgerline` on Python 3.11 or later.

## 2. Incident summary

Write the summary section of the postmortem for the checkout outage.

Facts:

- From 14:02 to 14:47 UTC on 9 September, 38 percent of checkout requests returned errors.
- The TLS certificate on the payments proxy expired at 14:02.
- An alert fired at 14:09 and posted to a Slack channel that the team archived in July.
- An engineer saw customer reports at 14:31 and renewed the certificate at 14:45.
- Errors stopped at 14:47, and the database didn't lose any payment data.
- The team agreed on two follow-ups: renew the certificate automatically, and route payment alerts to PagerDuty.

## 3. Design options

Write the "Options considered" section of a design doc about where to store user sessions. The team hasn't chosen an option yet.

Facts:

- A single Redis node stores user sessions today. Its memory use is at 71 percent and rises about 3 percentage points a week.
- Option A: add a second Redis node and shard sessions across both nodes. The team hasn't operated sharded Redis before.
- Option B: move sessions to the existing Postgres cluster, which has 40 percent free capacity. In staging, session reads took 9 ms at p95 on Postgres and 2 ms on Redis.
- Each page load runs one session read.

## 4. Review finding

The diff adds this line to `admin/stats.ts` at line 22:

```ts
const userCount = (await db.users.findMany()).length;
```

The `users` table has 1.2 million rows, and this handler runs on every load of the admin dashboard. Write the review finding.

## 5. Changelog entry

Write the changelog entry for version 2.4.

Facts:

- New: `ledgerline export --format xlsx` writes the reconciliation report as an Excel spreadsheet.
- Fixed: users in time zones east of UTC saw report dates one day early.
- Removed: the `--legacy-match` flag, which version 2.1 deprecated.

## 6. Five replies in one session

Reply to each message in order, as five chat turns in the same session, using only the facts below each message.

1. "quick q, does ledgerline need network access?"
   Ledgerline uses the network only to read the accounting API, and bank parsers run offline.
2. "cool. pointed it at last month's export and it matched like 3 rows out of 900 lol. is it broken?"
   The export writes dates as day/month/year, while the parser defaulted to month/day/year. Passing `--date-format dmy` parses day/month/year dates, and we haven't run it with that flag yet.
3. "ugh this is the third date bug this week"
   The other two date bugs were in the reports service, and the team fixed both on Tuesday.
4. "ok ran it with the flag, 861 matched. good?"
   861 rows matched, and the parser wrote the remaining 39 rows to `review.csv`. We haven't checked those 39 rows yet.
5. "can we just auto-accept the review rows so I don't have to look at them"
   12 of the 39 rows in `review.csv` differ from the ledger by more than $1, and auto-accepting marks all 39 rows as reconciled in the report.
