# Code Observations

This file shows how to state a code finding outside `toby-code-review`: state what the code does, then state the cost, count, date, or failure that follows from it.

---

## Fact and consequence

- `parseConfig` reads the file on every call. Each request calls `parseConfig`, so at 4,000 requests a minute the process reads the file 4,000 times a minute.
- The query planner never uses the index on `orders(created_at)`. Every query filters on `tenant_id` first, so the planner uses the tenant index.
- Deleting a user leaves their sessions in the table. Add a foreign-key cascade, or delete the sessions in the same transaction.
- The handler catches `Exception` and logs at `debug`. Production runs at `info`, so the production logs omit these failures.
- The retry wraps the whole request, including the body stream read. The first attempt consumes the stream, so the retry sends an empty body.
- Two callers pass `timeout=None`. The socket doesn't set a default timeout, so those two calls can hang forever.
- This lock is safe, because the three statements inside it don't perform I/O.

## Paired facts

- The app imports a package to check whether a number is even, and that package has had two CVEs.
- The function returns a variable named `temp`, writes it to the database, and renders it on the homepage. Rename `temp` for what it holds.
- The `// temporary` comment dates from 2019, and both the author and the reviewer have left the company.
- The client reads the retry count and timeout from config, and hardcodes the staging URL.
- The client retries a 400 response three times and sends the same invalid payload each time.
- The catch block returns `null` on error, and the caller crashes two lines later when it dereferences that return value.
- `process` is 200 lines and performs nine separate jobs, and its name describes none of them.

## Architecture counts

- The request handler reads one database row through four interfaces, and three of them only forward the call.
- A factory builds one type. The commit message mentions a second type, and no later commit added one.
- The service has an interface, a base class, and one implementation, with no second implementation in the repo.

## Misleading names

- The team named the flag `ENABLE_NEW_CHECKOUT_V2_FINAL` and has renamed it twice since adding `FINAL`.
- The oldest of the 40 call sites of `TEMP_FIX` dates from 2022.
- `utils.js` is 1,800 lines and mixes functions from nine unrelated modules.
- `UserManager` and `UserHandler` both call `UserService`, and no code in the repo calls `UserHandler`.

## Tests

- The test suite takes 40 minutes, so the team runs it once a week and catches regressions up to six days after merge.
- `test1` asserts that `true` is `true` and has never failed.
- The team re-records the 4,000-line snapshot whenever it fails, so the snapshot never blocks a regression.
- The test comments out its only assertion, so it passes without checking the result.

## Performance

- The page runs one query to list the users and one query per user for their name, totaling 501 queries for 500 users.
- The loop re-sorts an unchanged list on every iteration, sorting the same items ten thousand times.

## CI and migrations

- The test passes locally and fails in CI, because it reads `~/.aws/config`, which the CI runner doesn't have.
- The test fails one run in nine because two workers write the same temp file, and it failed in CI 14 times this month.
- The migration defines an `up` step and omits a `down` step, so rolling it back requires a manual SQL script.
