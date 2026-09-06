## A1
A lookup map turns each case into a data row; a switch turns each case into a branch of control flow. That matters here because the cases are just key-to-value mappings with no shared logic between them, so a map keeps adding a case a one-line diff instead of a new branch to reason about.

## A2
Inside a plain `for` loop, `await` pauses that iteration before the loop moves to the next one — the loop body runs to the `await`, yields to the event loop, and only resumes (and advances to the next iteration) once the promise settles. The misconception most people bring in is expecting the loop to behave like `forEach` with an async callback, which fires every iteration immediately and never waits — there, the awaits inside are orphaned and the function returns before any of them settle. A plain `for...of` with `await` is sequential by construction; `map`/`forEach` with an async callback is not, because nothing awaits the callback's returned promise.

## A3
A mutex is a lock: one owner at a time, and only that owner can release it. A semaphore is a counter: up to N holders at once, and any thread can signal it, not just the one that decremented it.

## A4
I checked two things: the retry wrapper itself (`src/sync/worker.ts:88-104`) and its call sites, found with `rg "retryWithBackoff"` — both in that same file. That means removing it has no reach outside `worker.ts`, which is what "safe" was resting on. I have not run the test suite, so whether the two call sites actually depend on the retry behavior at runtime is unverified — that claim is a guess until the tests run.
