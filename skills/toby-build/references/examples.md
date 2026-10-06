# Worked cuts

These examples cut four kinds of feature into slices. All four use one invented repo with orders, a members screen, a billing module, and a search path.

## 1. Brownfield, one entry point — new endpoint on an existing resource

Request: "let people cancel an order from the account page."

1. Observable — a POST to `/orders/:id/cancel` on an order the caller owns returns the order with status `cancelled`. Source — the user said "cancel an order". Check — the criterion is unmet if `test_cancel_returns_cancelled_order` finds that the status stays `open`.
2. Observable — cancelling an order already shipped returns 409 and leaves the order untouched. Source — the user said "no cancelling once it's out the door". `api/orders.ts:88` supports it with the shipped-state guard that the refund path already runs. Check — the criterion is unmet if `test_cancel_rejects_shipped` finds that the order changed.
3. Observable — cancelling someone else's order returns 404. Source — the request says nothing about this case, but `api/orders.ts:31` has the ownership check every other order route runs. Check — the criterion is unmet if `test_cancel_scopes_to_owner` gets any 2xx.
4. Stays working — the order list still returns shipped and open orders unchanged. Source — `tests/orders/list.test.ts` defines the current list output. Check — the criterion is unmet if the `orders_list` suite finds any changed row.

Slices: there is one slice, `an open order can be cancelled from the account page`. All four criteria are observed at the same entry point, which is an HTTP request to the orders API.

Wiring: `api/routes.ts:142` registers the route with `router.post('/orders/:id/cancel', cancelOrder)`.

Stops: show the criteria in one line and keep working. The strategic triggers do not apply, because the boundary already exists even though the route is new. The sibling feature is the set of other order routes in `api/orders.ts`, which run the ownership check at `api/orders.ts:31`.

## 2. Two entry points — a flow crossing two screens

Request: "users should be able to invite a teammate and see the invite pending."

1. Observable — submitting an email on the members screen shows that address in a Pending list without a reload. Source — the user said "see the invite pending". Check — the criterion is unmet if `test_invite_appears_pending` finds that the address needs a reload.
2. Observable — the invited address receives one invite email with a link that opens the accept screen. Source — the user said "invite a teammate". Check — the criterion is unmet if `test_invite_email_link_opens_accept` finds zero or two emails.
3. Observable — opening a used or expired link shows an expired state and creates no account. Source — in the follow-up about resent links, the user said "once I resend, the first link should be scrap". Check — the criterion is unmet if `test_expired_link_creates_no_account` finds that an account exists afterwards.
4. Stays working — the members list still renders for an org with no pending invites. Source — `tests/members/list.test.ts` defines the current list output. Check — the criterion is unmet if the `members_list` suite finds any changed row.

Slices: first `invite shows up as pending`, then `the invite email opens the accept screen`. Criteria 1 and 4 are observed at the members screen, and criteria 2 and 3 at the mail and the accept route.

Wiring: slice one connects at `screens/Members.tsx:210` through `<InviteForm onSubmit={createInvite} />`, and slice two connects at `jobs/index.ts:17` through the `invite.created` subscription.

Stops: this flow crosses two screens, which is a strategic trigger, so show the criteria and wait, then write a plan file. The first slice ends at a point where the user has a question to answer. The pending row shows the address, but what the second slice does depends on whether it also shows the inviter and the expiry. So stop there.

Slice one has no value to a user without slice two. An invite that creates a row and mails nobody is half-built behavior that a user can trigger. So the `invites.form` flag defaults off, and slice one is observed with the flag on. The flag is switched on for users when slice two's send ships. The last checkbox in slice two deletes the flag.

## 3. Greenfield — a subsystem with no sibling

Request: "we need usage metering so we can bill by seat next quarter."

The user first asked for "a quick PoC of the metering dashboard", which was experiment mode. This example starts after they chose a layout, so the layout stays and its code is replaced.

This subsystem has no sibling in the repo, because the repo has no metering module, no counter storage, and no billing screen or endpoint. This work is greenfield, which is a strategic trigger.

1. Observable — an admin opening the usage page for a workspace sees the seat count as of the last completed day. Source — the user said "so we can bill by seat". Check — the criterion is unmet if `test_usage_page_shows_completed_day_count` finds that the page shows a partial day.
2. Observable — a seat added and removed inside one day counts once for that day. Source — the user said "someone joining and leaving shouldn't double-bill them". Check — the criterion is unmet if `test_seat_churn_counts_once` finds a count of two.
3. Observable — a workspace with no activity still returns a row, with a count of zero. Source — `billing/invoice.ts:52` throws on a gap. Check — the criterion is unmet if `test_idle_workspace_returns_zero` finds a missing row.

Before the second file exists, greenfield work adds these steps:

- The nearest conventions the repo already has are `billing/` for money-adjacent modules and the `jobs/` daily aggregate pattern that `jobs/revenue_rollup.ts` uses. Extend those two, and don't invent a third layout.
- The boundary is written once, per toby-swd-modules and toby-swd-interfaces. The module exposes `seatCountForDay(workspace, date)` and defines the storage layout that the function reads, so callers never read or write rows directly.
- The user chooses the name. Today `seat`, `member`, and `active user` mean the same thing, but one of them is about to appear on an invoice.

Slices: first `the CLI reports a day's seat count` (`bin/usage show --workspace X --date Y`), then `the usage page shows it`. Counting ships first because the page has nothing to render without it. The CLI gives slice one an entry point a user can run, so slice one is not a layer cut.

Stops: a persisted format and money are both strategic triggers, so the design lines come before the plan lists any file.

## 4. Changing behavior that already ships

Request: "the search should match on SKU as well as product name."

1. Observable — searching a full SKU returns that product first. Source — the user said "the search should match on SKU as well". Check — the criterion is unmet if `test_full_sku_ranks_first` finds any name match ranked above it.
2. Observable — searching a product name returns what it returned before, in the same order. Source — `tests/search/ranking.test.ts` defines the current order. Check — the criterion is unmet if that suite finds any ordering change.
3. Observable — a query matching a name and a different product's SKU returns the name match first. Source — the ambiguity pass on "match on SKU as well" produced it, so it ships marked `assumed`. Check — the criterion is unmet if `test_name_match_outranks_foreign_sku` finds the SKU match first.

Slices: there is one slice, `search matches a full SKU`. The baseline run matters more than usual here, because criterion 2 is a claim about what `search_ranking` printed before the first edit. Run it and quote it.

Wiring: no new wiring is needed. The change is inside a code path that callers already call, so the existing call site at `search/query.ts:60` meets the fourth slice condition.

Stops: show the criteria only. Criterion 3 came out of the ambiguity pass, because "match on SKU as well" has a second reading where SKU matches outrank names. One edit undoes that choice, so criterion 3 ships marked `assumed`. The chosen reading ranks name matches first, so the SKU-first reading is dropped. If the user wanted the other reading, the ordering clause in `rankResults` changes.

# A plan the user can approve

The plan below covers slice one of the invite flow, in the operating guide's plan format.

```markdown
# Toby's plan for team invites

Mode: durable implementation. Members can invite a teammate by email and see the
invite in a pending list until it's accepted.

Criteria, in the wording agreed before coding:
1. Submitting an email on the members screen shows that address in a Pending list
   without a reload.
2. The invited address receives one invite email with a link that opens the
   accept screen.
3. Opening a used or expired link shows an expired state and creates no account.
4. The members list still renders for an org with no pending invites.

Out of scope: bulk invites, invite revocation, role selection at invite time,
resend. Each one is a follow-up.

Design:
- Structure chosen: an `invites` module exposes `createInvite(org, email)` and
  `acceptInvite(token)`. It stores the tokens and their expiry and sends the
  invite email, so the members screen and the accept route never read the
  table.
- Alternative rejected: invite rows in `members` with a `pending` status. Every
  query on `members` would then need a status filter, and the invite expiry rule
  would be repeated in three files.
- `createInvite(org, email)` returns the pending invite. It sends one email and
  throws `AlreadyMember` when the address is already in the org.
- `acceptInvite(token)` returns the new member. It throws `InviteExpired` for a
  used or expired token and creates no account.
- Refactor first: none. `members/list.ts` already takes a list of rows to render.

## Group 1: invite shows up as pending (criteria 1 and 4)

- [ ] Create `db/migrations/0043_invites.sql` with an `invites` table. The table
      has the columns id, org_id, email, invited_by, created_at, expires_at, and
      accepted_at. This step serves criterion 1. It is proved when `pnpm db:migrate`
      runs, after approval, and `\d invites` lists the columns.
- [ ] Edit `api/invites.ts` to add `createInvite(orgId, email, actor)`. The
      function returns the pending row. It rejects an address that already has
      an unexpired invite. This step serves criterion 1. The test
      `test_invite_appears_pending` proves it. The test fails if a duplicate
      invite creates a second row.
- [ ] Edit `api/routes.ts` to register `POST /orgs/:id/invites`. This step serves
      criterion 1, because the handler is unreachable without the route.
- [ ] Edit `screens/Members.tsx` to add `<InviteForm>` and a Pending section that
      reads the new endpoint. The section shows the new invite before the server
      responds. This step serves criterion 1. The test
      `test_invite_appears_pending` proves it. The test fails if the address
      appears only after a reload.
- [ ] Add the flag `flags/invites.form` with a default of off. The invite form
      stays hidden until the code from group 2 sends the email. This step keeps criterion 1
      correct while group 1 ships without group 2. Group 1 is checked with the flag on.

### Verification, a hard stop

- Run `pnpm test members_list` before the first edit, and quote the output.
  Criterion 4 is a claim about that output.
- Run `pnpm test api/invites screens/Members`. Both new tests fail before the
  change and pass after it. Quote both runs.
- Open the members screen and invite an address. The address appears in Pending
  without a reload.
- Ask for approval before running `pnpm db:migrate` against the local database.

Stop here. Do not start group 2 until the user approves.

## Group 2: the invite email opens the accept screen (criteria 2 and 3)
...
```
