---
name: toby-plain
description: >-
  Rewrites the previous reply, or a file the user points to, in plain everyday
  English. Trigger only when the user explicitly invokes the skill by name or
  with the `/toby-plain` slash command. Don't trigger on "explain this", "I
  don't understand", or a request to reword text, which toby-explain and
  toby-voice cover.
disable-model-invocation: true
argument-hint: "[optional file path or note]"
---

# Toby Plain

Rewrite the previous reply, or the file or passage the user points to, the way a clear human engineer explains it to a teammate at a whiteboard. Every sentence must make sense on the first read to someone who hasn't read the code.

## What to rewrite

Rewrite the file or passage the user names, or rewrite your previous reply when the user names nothing. When the user names one part (such as "the part about caching"), rewrite only that part. Put the rewrite in chat and leave files on disk untouched unless the user asks you to edit a file.

## Fix the four things that make AI writing confusing

Check the original text for each problem below and fix it as you rewrite:

1. **A giant paragraph for one small point.** Find the one fact the paragraph is trying to say, and state that fact in one sentence of 20 words or fewer. Delete the throat-clearing, the restatement of the question, and the recap at the end.
2. **Passive voice with no actor.** Never write "the token is invalidated", "a 409 is returned", or "the value is passed". Name who does the action (`the browser`, `the server`, ` the database`, `you`, `I`) and put an active verb right after it (`"The server cancels the token"`).
3. **Confusing terminology and noun stacks.** Replace textbook terms (`idempotency`, `temporal decomposition`, `characterization test`, `denormalized projection`, `negative cache entry`) and four-noun chains (`user session token refresh failure`) with what actually happens (`"sending a unique ID so a retry doesn't charge the card twice"`, `"how often refreshing a login token fails"`). Keep a technical term or code identifier only when the user has to type it or see it on screen, and explain it in plain words the first time you use it.
4. **Inside-out code traces.** Don't start with file paths, helper names, or class hierarchies. State the outcome the user cares about first, then walk one concrete example through the steps in the order they happen (`"When a customer clicks Cancel..."`).

## How to structure the rewrite

Match the layout to what the original text is doing:

- **One-sentence lead.** Start every rewrite with one plain sentence that gives the answer, the problem, or the decision.
- **How something works or broke.** Walk one concrete example from start to finish in numbered steps, in the order the steps happen.
- **Multiple facts, problems, or changes.** Put each point on its own bullet, in one or two short sentences. Never pack three separate facts into one paragraph.
- **A decision the user must make.** Ask the question in plain words, list at most three options with what goes right or wrong under each, and recommend one.

Keep every warning, number, and open question from the original, and don't invent new facts or run new commands. When the original was confusing because it skipped a step or contradicted itself, say which step was missing or which two lines conflicted. Start directly with the answer, without "In plain English:" or an apology, and don't add a closing offer.

## Before and after examples

### 1. Giant paragraph for one small point

> Confusing: "The latency regression observed in the checkout confirmation view is attributable to the fact that client-side filter state updates trigger an unthrottled re-fetch of the catalog endpoint on each input event, while simultaneously each rendered row component derives its own sorted copy of the item array during reconciliation."

Plain: The checkout page freezes when you type because every keystroke re-downloads the whole product catalog, and every row re-sorts the list from scratch. Wait until typing stops before fetching the catalog, and sort the list once in the parent component.

### 2. Passive voice and unexplained jargon

> Confusing: "Charges are made idempotent via an `idempotency_key` persisted under a unique constraint. If a timeout is encountered on the outbound processor call, the key must be reused on retry so duplicate settlement is prevented, whereas a new key is generated only after a terminal decline is returned."

Plain: When we charge a card, we send the payment processor a unique ID (`idempotency_key`) for that attempt.

- If the connection drops before we get an answer, we retry with that same ID so the processor doesn't charge the customer twice.
- If the processor declines the card and the customer tries a new card, we generate a new ID for the new attempt.

### 3. Inside-out code trace

> Confusing: "In `orders/cancel.py:42`, `OrderCancelService.execute()` invokes `RefundGateway.issue()` prior to the state guard in `Order.transition_to_cancelled()`, which only validates `self.status != 'refunded'` after the external call completes, permitting duplicate refunds under concurrent `POST /orders/{id}/cancel` requests."

Plain: Clicking Cancel twice on a shipped order refunds the customer twice.

1. The first Cancel request sends the refund to Stripe before marking the order as refunded in our database.
2. If a second Cancel request arrives while Stripe is still responding, our database still shows the order as shipped, so the server sends a second refund.

Fix: Mark the order as refunded in the database before calling Stripe, and reject any second Cancel request with a 409 error.

### 4. Decision buried in abstract tradeoffs

> Confusing: "We need to determine the schema migration strategy for the `invites` relation. Option A utilizes a nullable `invited_at` column on `members` with query-scope filtering, while Option B introduces a dedicated `invites` table decoupled from member queries."

Plain: Should we store pending invites in their own `invites` table, or as rows in the existing `members` table?

- **Separate `invites` table (recommended):** Keeps pending invites out of `members`, so existing member queries can't accidentally include people who haven't accepted yet.
- **Nullable columns on `members`:** Avoids a new table, but every query that lists or bills active members has to remember to filter out pending invites.
