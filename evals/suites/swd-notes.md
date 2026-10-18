# Engineering note tasks

This suite has six tasks: two module guides, two design notes, and two placement notes. Tasks 1 to 3 come from `swd.md`, and tasks 4 to 6 are held-out tasks that no rule was tuned against. Each task provides raw material and names the skill file the writer reads before drafting. We froze these tasks on 2026-09-15 before running any writer.

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

## 2. Design note

Skill file: `skills/toby-swd-strategy/SKILL.md`

Write the design note that compares the two approaches and recommends one.

Facts:

- Orders need a status history for the support page.
- Approach A adds an `order_events` table where each status change inserts a row and the support page queries rows in time order.
- Approach B adds a `status_history` JSON column on `orders` where each change appends to the JSON array.
- `orders` has 41 million rows, and appending to a JSON column rewrites the entire row in Postgres.
- Finance asked last quarter to include refund events in the same history.
- A nightly job already copies new rows from event tables to the analytics warehouse.

## 3. Placement note

Skill file: `skills/toby-swd-modules/SKILL.md`

Write the note stating where the new exchange-rate cache goes and why.

Facts:

- `pricing/convert.ts` calls `ratesClient.get(currency)` on every price render.
- `ratesClient` is in `clients/rates.ts`, and three modules call it: `pricing/convert.ts`, `invoices/totals.ts`, and `reports/revenue.ts`.
- The external rates API allows 100 calls a minute, while product pages made 2,400 calls a minute at peak on 2026-09-10.
- Exchange rates change at most once an hour.
- `reports/revenue.ts` queries historical rates for past dates and never reads the live rate.

## 4. Module guide

Skill file: `skills/toby-swd-docs/SKILL.md`

Write the `AGENTS.md` for `packages/search/`.

Facts:

- `packages/search/` runs product searches for the storefront.
- `index.ts` exports `search(query, options)`, which builds an OpenSearch query and sends it through `client.ts`.
- `ranking.ts` applies the boosts in `boosts.json` to the query.
- `synonyms.json` lists synonym pairs, such as `sofa` and `couch`.
- Legal requires deleted products to disappear from search within 24 hours. `hooks/onProductDelete.ts` removes deleted products from the index, and `jobs/reindex.ts` rebuilds the full index every night.
- Other packages call `search` and must not call `client.ts` directly.
- `pnpm test --filter search` runs the tests against a local OpenSearch container started with `docker compose up search-test`.

## 5. Design note

Skill file: `skills/toby-swd-strategy/SKILL.md`

Write the design note that compares the two approaches and recommends one.

Facts:

- Users can upload an avatar image.
- Approach A stores each image in a `bytea` column on `users`.
- Approach B stores each image in the S3 bucket `static-assets` and saves the object key on `users`.
- The app has 2.1 million users, avatars average 180 KB, and the maximum upload size is 5 MB.
- A CDN already serves files from `static-assets`.
- The nightly database backup takes 3 h 40 min today, and ops requires backups to finish in under 4 hours.
- The mobile app requests each avatar at three pixel sizes.

## 6. Placement note

Skill file: `skills/toby-swd-modules/SKILL.md`

Write the note stating where a new `normalizePhone(input)` function goes and why.

Facts:

- `signup/form.ts` strips spaces and dashes from phone numbers inline.
- `contacts/import.ts` defines its own `cleanPhone` function that strips spaces and dashes and prepends `+1` to 10-digit numbers.
- `sms/send.ts` rejects any phone number that doesn't start with `+`.
- `shared/format/` contains `formatCurrency.ts` and `formatDate.ts`, and 14 modules import from it.
- The product supports only US and Canada phone numbers today.
- Support counted 312 failed SMS sends in August 2026 caused by numbers missing the `+1` prefix.
