# Engineering skill tasks

This suite has eight tasks, one for each `toby-swd-*` skill that produces written text: a module guide, test names with comments, an interface docstring, error messages, an experiment report, an approval request, a design note, and a placement note. Each task provides raw material and names the skill file the writer reads before drafting. We froze these tasks on 2026-09-14 before running any writer.

Use only what the material shows, plus arithmetic on it and standard knowledge of the language or tool the task names.

## 1. Module guide

Skill file: `skills/toby-swd-docs/SKILL.md`

Write the `AGENTS.md` for `services/notify/`.

Facts:

- `services/notify/` sends email and SMS notifications for order events.
- `dispatch.ts` exports `sendForEvent(event)`, which looks up the user's channel preferences and calls one sender per enabled channel.
- `senders/email.ts` calls the Postmark API, and `senders/sms.ts` calls the Twilio API.
- `templates/` contains one Handlebars file per event type, such as `order-shipped.hbs`.
- `preferences.ts` reads the `notification_preferences` table.
- Other services call `sendForEvent` and must not call a sender module directly.
- Adding an event type requires a template file in `templates/` and an entry in `EVENT_TYPES` in `dispatch.ts`; the build fails when an entry lacks a matching template.
- `pnpm test --filter notify` runs the tests, using recorded HTTP fixtures in `test/fixtures/`.

## 2. Tests for a bug fix

Skill file: `skills/toby-swd-testing/SKILL.md`

Write the pytest test functions for this fix, with a short comment above each test stating what it checks. Return only the tests.

```python
def prorate(amount_cents, days_used, days_in_period):
    if days_in_period == 0:
        return 0
    return round(amount_cents * days_used / days_in_period)
```

Facts:

- Before the fix, `days_in_period == 0` raised `ZeroDivisionError` when a plan had a zero-day trial period on 2026-09-02.
- Python's `round` rounds half to even, so `prorate(1, 1, 2)` returns `0`.
- Finance specified `0` as the charge for a zero-day period.

## 3. Interface docstring

Skill file: `skills/toby-swd-interfaces/SKILL.md`

Write the TSDoc comment for this function, and return the comment and signature:

```ts
export async function reserveSeats(
  eventId: string,
  count: number,
  holdMinutes = 10,
): Promise<Reservation>
```

Facts:

- It inserts a row in `reservations` with `expires_at` set `holdMinutes` from now.
- It throws `SoldOutError` when fewer than `count` seats remain.
- It throws `RangeError` when `count` is below 1 or above 8.
- A background job runs every minute and deletes rows whose `expires_at` has passed.
- Calling it twice for the same user creates two separate reservations.

## 4. Error messages

Skill file: `skills/toby-swd-errors/SKILL.md`

Write the user-facing message and the log line for each failure below. Return them as a table with the columns `Failure`, `Message shown to the user`, and `Log line`.

Failures:

- The uploaded CSV exceeds 20 MB.
- A row has a date that doesn't match `YYYY-MM-DD`, and the parser knows the row number.
- The import service returns 503 after the client retries three times, 2 seconds apart.
- The user's session expired during the upload.

## 5. Experiment report

Skill file: `skills/toby-swd-experiment/SKILL.md`

Write the chat report for this experiment.

Facts:

- The user asked to compare the image resize worker at concurrency 4 and concurrency 8.
- You ran 2,000 images from `fixtures/photos/` on the staging worker, once per setting.
- Concurrency 4 finished in 3 min 12 s with 1.1 GB peak memory and 0 failures.
- Concurrency 8 finished in 2 min 5 s with 2.3 GB peak memory and 14 `ENOMEM` failures.
- The staging worker has 2 GB of RAM, while production workers have 4 GB of RAM. You haven't run the test on production hardware.

## 6. Approval request

Skill file: `skills/toby-swd-environment/SKILL.md`

The current task in `~/code/admin` needs to start `next dev` on port 3000. Write the message to the user.

Output of `lsof -i :3000`:

```
COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
node    48211 happy   23u  IPv6 0x5f1e      0t0  TCP *:hbci (LISTEN)
```

Facts:

- `ps -p 48211 -o lstart,command` shows process 48211 started at 09:14 today, running `next dev` from `~/code/storefront`.
- The current task is in `~/code/admin`, which also runs `next dev`.

## 7. Design note

Skill file: `skills/toby-swd-strategy/SKILL.md`

Write the design note that compares the two approaches and recommends one.

Facts:

- Orders need a status history for the support page.
- Approach A adds an `order_events` table where each status change inserts a row and the support page queries rows in time order.
- Approach B adds a `status_history` JSON column on `orders` where each change appends to the JSON array.
- `orders` has 41 million rows, and appending to a JSON column rewrites the entire row in Postgres.
- Finance asked last quarter to include refund events in the same history.
- A nightly job already copies new rows from event tables to the analytics warehouse.

## 8. Placement note

Skill file: `skills/toby-swd-modules/SKILL.md`

Write the note stating where the new exchange-rate cache goes and why.

Facts:

- `pricing/convert.ts` calls `ratesClient.get(currency)` on every price render.
- `ratesClient` is in `clients/rates.ts`, and three modules call it: `pricing/convert.ts`, `invoices/totals.ts`, and `reports/revenue.ts`.
- The external rates API allows 100 calls a minute, while product pages made 2,400 calls a minute at peak on 2026-09-10.
- Exchange rates change at most once an hour.
- `reports/revenue.ts` queries historical rates for past dates and never reads the live rate.
