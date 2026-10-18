# Worked cuts

These examples cut four kinds of feature into slices in a repo with orders, a members screen, a billing module, and a search path.

## 1. Single entry point

Request: "let people cancel an order from the account page."

1. **Observable**: on the account page, clicking Cancel on an open order shows that order as `cancelled` without a reload.
   - **Source**: the user said "cancel an order from the account page".
   - **Check**: the criterion is unmet if the `e2e/orders.spec.ts` test "cancel from account page" finds the status still `open`, or if the existing `orders_list` suite fails.
2. **Observable**: a POST to `/orders/:id/cancel` on an order already shipped returns 409 and leaves the order untouched.
   - **Source**: the user said "no cancelling once it's out the door". The shipped-state check at `api/orders.ts:88` supports this criterion.
   - **Check**: the criterion is unmet if `test_cancel_rejects_shipped` finds that the order changed.
3. **Observable**: cancelling someone else's order returns 404.
   - **Source**: `api/orders.ts:31` runs this ownership check on every other order route.
   - **Check**: the criterion is unmet if `test_cancel_scopes_to_owner` gets any 2xx.

Slices: one slice, `an open order can be cancelled from the account page`. Criterion 1 is observed on the account page, and criteria 2 and 3 are observed at the cancel route that only the account page calls.

Wiring: `api/routes.ts:142` registers `router.post('/orders/:id/cancel', cancelOrder)`, and `screens/Account.tsx:88` renders `<CancelOrderButton order={order} />` for each open order.

Stops: tactical work states each criterion on one line in chat and continues. The orders module, its API boundary, and the account page already exist, and the sibling routes in `api/orders.ts` run the ownership check at `api/orders.ts:31`.

## 2. Two screens

Request: "users should be able to invite a teammate and see the invite pending."

1. **Observable**: submitting an email on the members screen shows that address in a Pending list without a reload.
   - **Source**: the user said "see the invite pending".
   - **Check**: the criterion is unmet if `pnpm e2e invites.spec.ts -g "invite shows up as pending"` finds the address missing or needing a reload.
2. **Observable**: the invited address receives one invite email with a link that opens the accept screen.
   - **Source**: the user said "invite a teammate".
   - **Check**: the criterion is unmet if `test_invite_email_link_opens_accept` finds zero or two emails.
3. **Observable**: opening a used or expired link shows an expired state and doesn't create an account.
   - **Source**: the user said "once I resend, the first link should be scrap".
   - **Check**: the criterion is unmet if `test_expired_link_creates_no_account` finds a new account.
4. **Observable**: the members list still renders for an org without pending invites.
   - **Source**: `tests/members/list.test.ts` defines the current list output.
   - **Check**: the criterion is unmet if any existing test in `pnpm test members` fails or had to change.

Slices: first `invite shows up as pending`, then `the invite email opens the accept screen`. Criteria 1 and 4 are observed at the members screen, and criteria 2 and 3 in the invite email and accept route.

Wiring: slice one connects at `screens/Members.tsx:210` through `<InviteForm onSubmit={createInvite} />`, and slice two connects at `jobs/index.ts:17` through the `invite.created` subscription.

Stops: this flow crosses two screens, so the work is strategic. At stop 1, show the criteria, the slice names, and the plan's path (`docs/plans/members/team-invites/`), and offer to write the plan there.

Main deploys on every merge, so slice one ships behind the release flag `team-invites` (off by default) and runs its checks with the flag on. The flag turns on after slice two ships, and a follow-up step removes the flag after rollout. `toby-swd-plan`'s `references/example.md` shows the full plan.

## 3. Greenfield subsystem

Request: "we need usage metering so we can bill by seat next quarter."

The user first ran an experiment for the dashboard layout, and this build replaces the experiment code while keeping the chosen layout. The repo doesn't have a metering module, counter storage, or a billing endpoint, so the work is strategic.

1. **Observable**: an admin opening the usage page for a workspace sees the seat count as of the last completed day.
   - **Source**: the user said "so we can bill by seat".
   - **Check**: the criterion is unmet if `test_usage_page_shows_completed_day_count` finds that the page shows a partial day.
2. **Observable**: a seat added and removed inside one day counts once for that day.
   - **Source**: the user said "someone joining and leaving shouldn't double-bill them".
   - **Check**: the criterion is unmet if `test_seat_churn_counts_once` finds a count of two.
3. **Observable**: a workspace without activity returns a row with a count of zero.
   - **Source**: `billing/invoice.ts:52` throws on a missing day row.
   - **Check**: the criterion is unmet if `test_idle_workspace_returns_zero` finds a missing row.

Before creating a second new file in greenfield work:

- Extend the two closest repo patterns: `billing/` for money-adjacent modules and `jobs/revenue_rollup.ts` for daily aggregation.
- Design the module boundary once with `toby-swd-modules` and `toby-swd-interfaces`, exposing `seatCountForDay(workspace, date)` and hiding the storage layout.
- Use `seat` for a billed person, matching the user's words, and list that term as an assumption.

Slices: first `the CLI reports a day's seat count` (`bin/usage show --workspace X --date Y`), then `the usage page shows it`. The CLI gives slice one a runnable entry point, so slice one isn't a layer cut.

## 4. Existing behavior

Request: "the search should match on SKU as well as product name."

1. **Observable**: searching a full SKU returns that product first.
   - **Source**: the user said "the search should match on SKU as well".
   - **Check**: the criterion is unmet if `test_full_sku_ranks_first` finds any name match ranked above it, or if the existing `search_ranking` suite fails.
2. **Observable**: a query matching a name and a different product's SKU returns the name match first.
   - **Source**: the request doesn't specify tie-breaking, so this criterion keeps the name-first order in `search_ranking`, marked `assumed`.
   - **Check**: the criterion is unmet if `test_name_match_outranks_foreign_sku` ranks the SKU match first.

Slices: one slice, `search matches a full SKU`, reached through the existing call site at `search/query.ts:60`.

Stops: tactical work states each criterion on one line in chat and continues. If the user wants SKU matches ranked above name matches, one edit to `rankResults` changes that order.
