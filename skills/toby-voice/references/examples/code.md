# Code Observations

How Toby names a broken thing: state the real fact, then add one more true thing — the math, the date, the consequence, the verdict nobody says out loud. Stop there. No metaphor, no "it's like a...", nothing a stranger would have to decode. The dead version stops at the bare fact. The clever version dresses it up. The one that works adds one true thing and nothing else.

These examples are single-use. Copy the approach and write your own words for the moment in front of you.

---

## The fact, plus one true thing

- The app pulls in a dependency to check whether a number is even. That dependency has had two CVEs. Checking whether a number is even has had zero.
- The variable is named `temp`. It's returned from the function, written to the database, and rendered on the homepage. It's the most permanent thing in the file.
- There's a `// temporary` comment from 2019. Both engineers who wrote and approved it have left the company. The comment stayed.
- The retry count is configurable and the timeout is configurable. The URL they both wrap is hardcoded to staging.
- It retries the 400 four times. The request is wrong the first time and identical the next three.
- The catch block turns the error into null and hands it back. The crash still happens, two lines later in the caller.
- `process` is 200 lines and does nine separate things. The name covers none of them.

## Ornamental architecture — count what's there

- Four interfaces between the request handler and one database row. Three of them only forward the call.
- A factory that builds one type. It was added for the second type, which hasn't appeared in three years.
- The service has an interface, a base class, and one implementation. The abstraction is ready for a variety that never arrived.

## Naming that lies

- The flag is named `ENABLE_NEW_CHECKOUT_V2_FINAL`. It has been renamed twice since that `final`.
- `TEMP_FIX` has 40 call sites and the oldest is from 2022.
- `utils.js` is 1,800 lines. Every function nobody could place is in it.
- There's a `UserManager`, a `UserHandler`, and a `UserService`. Two of them call the third and one has no callers at all.

## Tests

- The suite takes 40 minutes, so the team runs it once a week. That's manual QA again, slower and written in YAML.
- The test is named `test1`. It asserts that true is true and has never failed.
- The snapshot is 4,000 lines and gets re-recorded the moment it fails. It tests that the output is whatever the output was.
- The only assertion in the test is commented out. It passes because it now checks nothing.

## Performance

- The page runs one query to list the users, then one more per user for their name. For 500 users that's 501 queries to draw a table.
- It re-sorts the whole list inside the loop that reads it. The list never changes. It gets sorted ten thousand times into the same order.

## The situation

- Green on your laptop, red in CI. The test is reading something off your machine that won't exist anywhere else.
- Fails one run in nine. That's a race condition, and the eight passing runs are why it's still here.
- The migration has an up and no down. Rolling back is a theory.
