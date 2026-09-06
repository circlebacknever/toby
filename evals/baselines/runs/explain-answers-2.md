## A1
A lookup map wins when every branch is just returning a value keyed on input, because a switch adds fallthrough risk and control-flow ceremony for something that's really just a table. Adding a case becomes a new row in the map instead of a new branch in the code — same data, less code to misread.

## A2
Take `for (const x of items) { await f(x); }`. The `await` pauses that iteration of the loop itself, so the next iteration doesn't start until the current promise resolves — the loop runs sequentially, one call at a time, not all at once. That's different from `items.map(x => f(x))`, which fires every call immediately and hands you an array of pending promises; people expect `for` with `await` to behave like that and it doesn't, because the pause lives inside the loop body, not around it.

## A3
A mutex has one owner: whoever locks it is the only one who can unlock it. A semaphore just counts permits up to N, and any code can signal it, whether or not it ever acquired one.

## A4
I haven't verified it, so calling it safe was ahead of the evidence. What I have: the retry wrapper at `src/sync/worker.ts:88-104`, and `rg "retryWithBackoff"` showing both call sites in that same file — no other module reaches it. That rules out an external dependency on the retry behavior, but I haven't run the test suite, so whether removing it breaks something inside `worker.ts` itself is still open.
