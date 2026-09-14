# Held-out tasks

Six outputs on a product and a session that no rule in this repo was tuned
against. The content suite trained the rules, so a change that only fixes the
content suite fails here. Each task gives every fact the output needs, and a
writer who adds a fact has broken the task.

## 1. Tool overview

Write the top of the README for Ledgerline: a title, an opening paragraph of at
most 80 words, then two sections, `Install` and one about adding a bank format,
with one short paragraph each.

Facts:

- Ledgerline is a command-line tool that reconciles bank CSV exports against an
  accounting system.
- It reads exports from four banks: Chase, Monzo, Wise, and ING.
- It matches a bank row to a ledger entry when the amounts are equal and the
  dates are within 2 days of each other.
- Rows it cannot match go to `review.csv` for a person to check.
- It reads the accounting system through an API token with read-only scope.
- A bank format is a parser in `parsers/<bank>.py`. Parsers must not make network
  calls, and CI fails any parser that imports `requests` or `httpx`.
- Install with `brew install ledgerline`. It needs Python 3.11 or later.

## 2. Incident summary

Write the summary section of the postmortem for the checkout outage.

Facts:

- From 14:02 to 14:47 UTC on 9 September, 38 percent of checkout requests
  returned errors.
- The TLS certificate on the payments proxy expired at 14:02.
- An alert fired at 14:09 and went to a Slack channel that was archived in July.
- An engineer saw customer reports at 14:31 and renewed the certificate at 14:45.
- Errors stopped at 14:47. No payment data was lost.
- Two follow-ups are agreed: renew the certificate automatically, and send
  payment alerts to the on-call pager.

## 3. Design options

Write the "Options considered" section of a design doc about where to store
user sessions. The decision has not been made.

Facts:

- Sessions are in a single Redis node, now at 71 percent of its memory, growing
  about 3 percentage points a week.
- Option A: add a second Redis node and shard sessions across both. The team
  has not run sharded Redis before.
- Option B: move sessions to the existing Postgres cluster, which has 40 percent
  headroom. In staging, session reads took 9 ms at p95 on Postgres and 2 ms on
  Redis.
- The session read runs once per page load.

## 4. Review finding

The diff adds this to `admin/stats.ts` at line 22:

```ts
const userCount = (await db.users.findMany()).length;
```

The `users` table has 1.2 million rows, and this handler runs on every load of
the admin dashboard. Write the review finding.

## 5. Changelog entry

Write the changelog entry for version 2.4.

Facts:

- New: `ledgerline export --format xlsx` writes the reconciliation report as a
  spreadsheet.
- Fixed: users in time zones east of UTC saw report dates one day early.
- Removed: the `--legacy-match` flag, which was deprecated in version 2.1.

## 6. Five replies in one session

Reply to each message in order, as five chat turns in the same session. Facts for
each turn follow the message.

1. "quick q, does ledgerline need network access?"
   Only to call the accounting API. Parsers make no network calls.
2. "cool. pointed it at last month's export and it matched like 3 rows out of 900 lol. is it broken?"
   The export writes dates as day/month/year, and the parser read them as
   month/day/year. `--date-format dmy` reads them correctly. Nobody has run it
   with that flag yet.
3. "ugh this is the third date bug this week"
   The other two date bugs were in the reports service, and both were fixed on
   Tuesday.
4. "ok ran it with the flag, 861 matched. good?"
   861 rows matched and 39 went to `review.csv`. Nobody has looked at the 39.
5. "can we just auto-accept the review rows so I don't have to look at them"
   12 of the 39 rows have amounts that differ from the ledger by more than $1.
   Auto-accepting marks all 39 as reconciled in the report.
