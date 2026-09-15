# Engineering note tasks

Six outputs: a module guide, a design note, and a placement note, twice each.
Tasks 1 to 3 come from `swd.md`. Tasks 4 to 6 are new, and no rule was written
against them. Each task gives raw material and names the skill file a writer
reads before writing it. Frozen on 2026-09-15 before any writer ran.

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

## 2. Design note

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

## 3. Placement note

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

## 4. Module guide

Skill file: `skills/toby-swd-docs/SKILL.md`

Write the AGENTS.md for `packages/search/`.

Facts:

- `packages/search/` answers product searches for the storefront.
- `index.ts` exports `search(query, options)`. It builds an OpenSearch query and
  sends it through the client in `client.ts`.
- `ranking.ts` applies the boosts in `boosts.json` to the query.
- `synonyms.json` lists synonym pairs, such as `sofa` and `couch`.
- Legal requires a deleted product to disappear from search within 24 hours.
  `hooks/onProductDelete.ts` removes the product from the index, and
  `jobs/reindex.ts` rebuilds the whole index every night.
- Other packages call `search` and never call `client.ts` directly.
- Tests run with `pnpm test --filter search`. They need a local OpenSearch
  container, which `docker compose up search-test` starts.

## 5. Design note

Skill file: `skills/toby-swd-strategy/SKILL.md`

Write the design note that compares the two approaches and recommends one.

Facts:

- Users can upload an avatar image.
- Approach A stores each image in a `bytea` column on `users`.
- Approach B stores each image in the S3 bucket `static-assets` and keeps the
  object key on `users`.
- The app has 2.1 million users. Avatars average 180 KB, and the largest
  allowed file is 5 MB.
- A CDN already serves files from `static-assets`.
- The nightly database backup takes 3 h 40 min, and ops wants it under 4 h.
- The mobile app requests each avatar at three sizes.

## 6. Placement note

Skill file: `skills/toby-swd-modules/SKILL.md`

Write the note that says where a new `normalizePhone(input)` function goes and why.

Facts:

- `signup/form.ts` strips spaces and dashes from phone numbers inline.
- `contacts/import.ts` has its own `cleanPhone` function. It strips spaces and
  dashes and adds `+1` to a 10-digit number.
- `sms/send.ts` rejects a number that does not start with `+`.
- `shared/format/` holds `formatCurrency.ts` and `formatDate.ts`, and 14 modules
  import from it.
- The product supports only US and Canada numbers today.
- Support counted 312 failed SMS sends in August 2026 from numbers with no `+1`.
