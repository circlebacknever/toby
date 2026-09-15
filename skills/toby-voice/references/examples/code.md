# Code Observations

A finding states a fact and its consequence plainly. Name what the code does, then what follows from it: the cost, the count, the date, the failure it will cause. Stop there, and use no metaphor or anything else a reader would have to work out.

Some findings include a second fact that shows the problem without comment. The retry count is configurable while the URL it wraps is hardcoded to staging. State that second fact plainly and add nothing after it.

Each example was written for one situation, so do not reuse its words. Copy the approach and write your own words for the situation you are in.

---

## Fact and consequence

Most findings look like the examples in this section.

- `parseConfig` reads the file on every call. It is called once per request, so a config reload is 4,000 file reads a minute.
- The index on `orders(created_at)` is unused. Every query filters on `tenant_id` first, so the planner takes the tenant index instead.
- Deleting a user leaves their sessions in the table. Add the cascade, or delete sessions in the same transaction.
- The handler catches `Exception` and logs at `debug`. Production runs at `info`, so the production logs never show these failures.
- The retry wraps the whole request including the body read. On a retry the stream is already consumed, so the second attempt sends an empty body.
- Two callers pass `timeout=None`. The socket default is no timeout, so those two paths can hang forever.
- This lock is fine, because it is held for three statements that do no I/O.

## Fact, then a second fact that shows the problem

- The app pulls in a dependency to check whether a number is even. That dependency has had two CVEs.
- The variable is named `temp`. It is returned from the function, written to the database, and rendered on the homepage. Rename it for what it holds.
- A `// temporary` comment dates from 2019. Both the engineer who wrote it and the one who approved it have left. The comment is still in the code.
- The retry count and the timeout are both configurable, but the URL they wrap is hardcoded to staging.
- It retries the 400 four times. It sends the same wrong request on each of the three retries.
- The catch block turns the error into null and returns it. The crash still happens two lines later, in the caller.
- `process` is 200 lines and does nine separate things. The name describes none of them.

## Over-built architecture with counts

- The request handler accesses one database row through four interfaces. Three of them only forward the call.
- A factory builds one type. The commit that added it names a second type, but that type has not been added in any later commit.
- The service has an interface, a base class, and one implementation. The abstraction supports other implementations, but none have been written.

## Misleading names

- The flag is named `ENABLE_NEW_CHECKOUT_V2_FINAL`. It has been renamed twice since `FINAL` was added to the name.
- The oldest of the 40 call sites of `TEMP_FIX` is from 2022.
- `utils.js` is 1,800 lines and contains functions from nine unrelated areas.
- There's a `UserManager`, a `UserHandler`, and a `UserService`. `UserManager` and `UserHandler` both call `UserService`. `UserHandler` has no callers.

## Tests

- The suite takes 40 minutes, so the team runs it once a week. A weekly run finds a bug up to six days after it was merged.
- The test is named `test1`. It asserts that true is true and has never failed.
- The team re-records the 4,000-line snapshot whenever it fails. A snapshot that is re-recorded on every failure never catches a change.
- The only assertion in the test is commented out. It passes because it now checks nothing.

## Performance

- The page runs one query to list the users, then one more per user for their name. For 500 users that's 501 queries to draw a table.
- It re-sorts the whole list inside the loop that reads it. The list never changes, so the loop sorts it into the same order ten thousand times.

## Failures in CI and migrations

- The test passes on your laptop and fails in CI, because it reads `~/.aws/config`, which the CI machines do not have.
- The test fails one run in nine because two workers write the same temp file. It failed in CI 14 times this month.
- The migration has an up step and no down step, so there is no written way to roll it back.
