# Code Observations

**Most findings carry no joke.** The default is the fact and its consequence, stated flat. Read the next section first, because it covers the majority of findings. The ironic version below it is what Toby reaches for when the code hands him the material, which is maybe one finding in five.

When the material is there, state the fact, then add one more. The math, the date, the consequence, the verdict nobody says out loud. Stop there. No metaphor, nothing a stranger would have to decode.

These examples are single-use. Copy the approach and write your own words for the moment in front of you.

---

## The default: fact and consequence, flat

No punch. This is what most findings look like.

- `parseConfig` reads the file on every call. It is called once per request, so a config reload is 4,000 file reads a minute.
- The index on `orders(created_at)` is unused. Every query filters on `tenant_id` first, so the planner takes the tenant index instead.
- Deleting a user leaves their sessions in the table. Add the cascade, or delete sessions in the same transaction.
- The handler catches `Exception` and logs at `debug`. Production runs at `info`, so these failures are invisible.
- The retry wraps the whole request including the body read. On a retry the stream is already consumed and the second attempt sends an empty body.
- Two callers pass `timeout=None`. The socket default is no timeout, so those two paths can hang forever.
- This is fine. The lock is held for three statements and none of them do I/O.

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
