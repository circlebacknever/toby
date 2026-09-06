## A1
A lookup map keeps the mapping as data, so adding a case is one line instead of touching control flow. It also guarantees every branch returns the same shape, which a switch's fall-through can hide.

## A2
Each `await` pauses that loop iteration until its promise resolves, so the next iteration only starts after the previous one finishes. That makes a for-loop with await run sequentially, unlike `array.map(async fn)`, which starts every iteration immediately and awaits none of them for you. Most people expect the loop to parallelize on its own, but only `Promise.all(array.map(...))` does that.

## A3
A mutex allows one owner at a time, and only that owner can unlock it. A semaphore allows up to N holders at once, and any holder can release a permit, not just the one who took it.

## A4
Both call sites for `retryWithBackoff` live in `src/sync/worker.ts`, where the wrapper sits at lines 88-104, so removing it doesn't leave some other file expecting retry behavior. That's still a guess about safety — I haven't run the test suite, so I don't know if a test asserts on the retry path.
