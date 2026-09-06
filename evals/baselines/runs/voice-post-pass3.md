## 1
Found it. The test asserts on a timestamp formatted in the machine's local timezone, and CI runs in UTC, so once every nine runs the two land on opposite sides of a day boundary. Not fixed yet — the fix is either freezing the clock in the test or asserting in UTC, and I want to check which other tests share this helper before I touch it.

## 2
The sync job isn't idempotent, so a retry wrapper writes the same rows twice on any run that fails partway through. Wrapping it trades a failure you can see for one you can't: a duplicate load that passes every check until someone reconciles a report against it. Give the writes a dedup key or an upsert first — that costs less than the twice-a-week failure is costing you now.

## 3
Moves rate-limit checks out of the four route handlers and into one middleware, and deletes the token-bucket code each of them carried a copy of. Adds a test for the 429 path, which had none.

Behavior change: the limit is now per account, where it used to be per route per account. A user hitting four endpoints shares one bucket instead of four.

## 4
I don't know. Nothing in Tuesday's deploy diff allocates, and I don't have profiler data to say where the growth is coming from. A heap snapshot from before and after that deploy would settle it — I can wire one into the next release and diff it against a run on the old build.
