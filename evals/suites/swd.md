# Engineering skill tasks

Eight outputs, one for each `toby-swd-*` skill that produces written text: a
module guide, test names and a test comment, an interface docstring, error
messages, an experiment report, an approval request, a design note, and a
placement note. Each task gives raw material and names the skill file a writer
reads before writing it. Frozen on 2026-09-14 before any writer ran.

Use only what the material shows, plus arithmetic on it and standard knowledge of
the language or tool the task names.

## 1. Module guide

Skill file: `skills/toby-swd-docs/SKILL.md`

Write the AGENTS.md for `services/notify/`.

Facts:

- `services/notify/` sends email and SMS for order events.
- `dispatch.ts` exports `sendForEvent(event)`. It looks up the user's channel
  preferences and calls one sender per channel.
- `senders/email.ts` calls the Postmark API. `senders/sms.ts` calls the Twilio
  API.
- `templates/` holds one Handlebars file per event type, such as
  `order-shipped.hbs`.
- `preferences.ts` reads the `notification_preferences` table.
- Other services call `sendForEvent` and never call a sender directly.
- A new event type needs a template file and an entry in `EVENT_TYPES` in
  `dispatch.ts`. The build fails when an entry has no template.
- Tests run with `pnpm test --filter notify`. The sender tests use recorded HTTP
  fixtures in `test/fixtures/`.

## 2. Tests for a bug fix

Skill file: `skills/toby-swd-testing/SKILL.md`

Write the pytest test functions for this fix, with a short comment above each
test that says what it checks. Return only the tests.

```python
def prorate(amount_cents, days_used, days_in_period):
    if days_in_period == 0:
        return 0
    return round(amount_cents * days_used / days_in_period)
```

Facts:

- Before the fix, `days_in_period == 0` raised `ZeroDivisionError`. A plan with
  a zero-day trial period triggered it on 2026-09-02.
- `round` in Python rounds half to even, so `prorate(1, 1, 2)` returns 0.
- Finance wants 0 for a zero-day period.

## 3. Interface docstring

Skill file: `skills/toby-swd-interfaces/SKILL.md`

Write the TSDoc comment for this function. Return the comment and the signature.

```ts
export async function reserveSeats(
  eventId: string,
  count: number,
  holdMinutes = 10,
): Promise<Reservation>
```

Facts:

- It inserts a row in `reservations` with `expires_at` set `holdMinutes` from
  now.
- It throws `SoldOutError` when fewer than `count` seats remain.
- It throws `RangeError` when `count` is below 1 or above 8.
- A background job deletes rows whose `expires_at` has passed, every minute.
- Calling it twice for the same user creates two reservations.

## 4. Error messages

Skill file: `skills/toby-swd-complexity/SKILL.md`

Write the user-facing message and the log line for each failure. Return them as
a table with the columns Failure, Message shown to the user, and Log line.

Failures:

- The uploaded CSV is over 20 MB.
- A row has a date that is not in `YYYY-MM-DD` form. The row number is known.
- The import service returns 503. The client retries three times, 2 seconds
  apart, before it shows a message.
- The user's session expired during the upload.

## 5. Experiment report

Skill file: `skills/toby-swd-experiment/SKILL.md`

Write the report for this experiment in chat form.

Facts:

- The user asked to compare the image resize worker at concurrency 4 and 8.
- The run used 2,000 images from `fixtures/photos/` on the staging worker, one
  run per setting.
- Concurrency 4: 3 min 12 s total, peak memory 1.1 GB, 0 failures.
- Concurrency 8: 2 min 5 s total, peak memory 2.3 GB, 14 failures, all
  `ENOMEM`.
- The staging worker has 2 GB of memory. Production workers have 4 GB, and no
  production run happened.

## 6. Approval request

Skill file: `skills/toby-swd-environment/SKILL.md`

The task needs the dev server on port 3000. Write the message to the user.

Output of `lsof -i :3000`:

```
COMMAND   PID  USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
node    48211 happy   23u  IPv6 0x5f1e      0t0  TCP *:hbci (LISTEN)
```

Facts:

- `ps -p 48211 -o lstart,command` shows it started at 09:14 today, running
  `next dev` from `~/code/storefront`.
- The current task is in `~/code/admin`, which also runs `next dev`.

## 7. Design note

Skill file: `skills/toby-swd-strategy/SKILL.md`

Write the design note that compares the two approaches and recommends one.

Facts:

- Orders need a status history for the support page.
- Approach A adds an `order_events` table. Each status change inserts a row, and
  the support page reads the rows in time order.
- Approach B adds a `status_history` JSON column on `orders`. Each change appends
  to the array.
- `orders` has 41 million rows. A JSON append rewrites the whole column value.
- Finance asked last quarter for refund events in the same history.
- The team already runs a nightly job that copies new rows from event tables to
  the warehouse.

## 8. Placement note

Skill file: `skills/toby-swd-modules/SKILL.md`

Write the note that says where the new exchange-rate cache goes and why.

Facts:

- `pricing/convert.ts` calls `ratesClient.get(currency)` on every price render.
- `ratesClient` is in `clients/rates.ts`, and three modules call it:
  `pricing/convert.ts`, `invoices/totals.ts`, and `reports/revenue.ts`.
- The rates API allows 100 calls a minute. Product pages made 2,400 calls a
  minute at peak on 2026-09-10.
- Rates change once an hour at most.
- `reports/revenue.ts` needs the rate at a past date and never the live rate.
