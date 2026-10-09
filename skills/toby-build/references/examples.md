# Worked cuts

These examples cut four kinds of feature into slices. All four use one invented repo with orders, a members screen, a billing module, and a search path.

## 1. Brownfield, one entry point, a new action on an existing resource

Request: "let people cancel an order from the account page."

1. **Observable**: on the account page, clicking Cancel on an open order shows that order as `cancelled` without a reload. **Source**: the user said "cancel an order from the account page". **Check**: the criterion is unmet if the `e2e/orders.spec.ts` test "cancel from account page" finds the status still `open`, or if the existing `orders_list` suite fails.
2. **Observable**: a POST to `/orders/:id/cancel` on an order already shipped returns 409 and leaves the order untouched. **Source**: the user said "no cancelling once it's out the door". The shipped-state check that the refund path already runs, at `api/orders.ts:88`, supports this criterion. **Check**: the criterion is unmet if `test_cancel_rejects_shipped` finds that the order changed.
3. **Observable**: cancelling someone else's order returns 404. **Source**: the request says nothing about this case, but `api/orders.ts:31` has the ownership check every other order route runs. **Check**: the criterion is unmet if `test_cancel_scopes_to_owner` gets any 2xx.

Slices: there is one slice, `an open order can be cancelled from the account page`. Criterion 1 is observed on the account page. Criteria 2 and 3 are observed at the cancel route. Only the account page calls that route, so the route belongs to the same slice.

Wiring: `api/routes.ts:142` registers the route with `router.post('/orders/:id/cancel', cancelOrder)`, and `screens/Account.tsx:88` renders `<CancelOrderButton order={order} />` for each open order.

Stops: show each criterion on one line and keep working. None of the items in step 1's strategic list apply. The route and the button are new, but the orders module, its API boundary, and the account page already exist. The sibling feature is the set of other order routes in `api/orders.ts`, which run the ownership check at `api/orders.ts:31`.

## 2. Two entry points, a flow crossing two screens

Request: "users should be able to invite a teammate and see the invite pending."

1. **Observable**: submitting an email on the members screen shows that address in a Pending list without a reload. **Source**: the user said "see the invite pending". **Check**: the criterion is unmet if `pnpm e2e invites.spec.ts -g "invite shows up as pending"` finds the address missing or needing a reload.
2. **Observable**: the invited address receives one invite email with a link that opens the accept screen. **Source**: the user said "invite a teammate". **Check**: the criterion is unmet if `test_invite_email_link_opens_accept` finds zero or two emails.
3. **Observable**: opening a used or expired link shows an expired state and creates no account. **Source**: in the follow-up about resent links, the user said "once I resend, the first link should be scrap". **Check**: the criterion is unmet if `test_expired_link_creates_no_account` finds that an account exists afterwards.
4. **Observable**: the members list still renders for an org with no pending invites. **Source**: `tests/members/list.test.ts` defines the current list output. **Check**: the criterion is unmet if any existing test in `pnpm test members` fails or had to change.

Slices: first `invite shows up as pending`, then `the invite email opens the accept screen`. Criteria 1 and 4 are observed at the members screen, and criteria 2 and 3 in the invite email and at the accept route. The email and the screen its link opens are one flow, so they share the second slice.

Wiring: slice one connects at `screens/Members.tsx:210` through `<InviteForm onSubmit={createInvite} />`, and slice two connects at `jobs/index.ts:17` through the `invite.created` subscription.

Stops: this flow crosses two screens, so the work is strategic. At stop 1, show the criteria, ask whether to write the plan at `docs/plans/members/team-invites/`, and wait for a yes. What the second slice builds depends on whether the pending row should also show the inviter and the expiry. So at stop 3, after the first slice, ask that question.

Slice one has no value to a user without slice two. Main deploys on every merge, so slice one reaches users before slice two exists. An invite that creates a row and mails nobody is half-built behavior that a user can trigger. Slice one therefore ships behind the release flag `team-invites`, which is off by default, and its checks run with the flag on. The flag turns on for users after slice two sends the email, and the last step of slice two removes the flag. `toby-swd-plan`'s `references/example.md` has the plan for this feature.

## 3. Greenfield, a subsystem with no sibling

Request: "we need usage metering so we can bill by seat next quarter."

The user first asked for "a quick PoC of the metering dashboard", which was experiment mode. This example starts after the user chose a layout in that experiment. The new code keeps the layout and replaces the experiment's code.

This subsystem has no sibling in the repo, because the repo has no metering module, no counter storage, and no billing screen or endpoint. A new subsystem with nothing similar in the repo makes the work strategic.

1. **Observable**: an admin opening the usage page for a workspace sees the seat count as of the last completed day. **Source**: the user said "so we can bill by seat". **Check**: the criterion is unmet if `test_usage_page_shows_completed_day_count` finds that the page shows a partial day.
2. **Observable**: a seat added and removed inside one day counts once for that day. **Source**: the user said "someone joining and leaving shouldn't double-bill them". **Check**: the criterion is unmet if `test_seat_churn_counts_once` finds a count of two.
3. **Observable**: a workspace with no activity still returns a row, with a count of zero. **Source**: `billing/invoice.ts:52` throws on a gap. **Check**: the criterion is unmet if `test_idle_workspace_returns_zero` finds a missing row.

Because this work is greenfield, do these steps before you create a second new file:

- The nearest conventions the repo already has are `billing/` for money-adjacent modules and the `jobs/` daily aggregate pattern that `jobs/revenue_rollup.ts` uses. Extend those two, and don't invent a third layout.
- Design the module's boundary once, following `toby-swd-modules` and `toby-swd-interfaces`. The module exposes `seatCountForDay(workspace, date)` and defines the storage layout that the function reads, so callers never read or write rows directly.
- The user chooses which word to use for a billed person. Today `seat`, `member`, and `active user` mean the same thing, but one of them is about to appear on an invoice.

Slices: first `the CLI reports a day's seat count` (`bin/usage show --workspace X --date Y`), then `the usage page shows it`. Counting ships first because the page has nothing to render without it. The CLI gives slice one an entry point a user can run, so slice one is not a layer cut.

Stops: a persisted format and money each make the work strategic, so write the design lines before the plan lists any file.

## 4. Changing behavior that already ships

Request: "the search should match on SKU as well as product name."

1. **Observable**: searching a full SKU returns that product first. **Source**: the user said "the search should match on SKU as well". **Check**: the criterion is unmet if `test_full_sku_ranks_first` finds any name match ranked above it, or if the existing `search_ranking` suite finds any ordering change.
2. **Observable**: a query matching a name and a different product's SKU returns the name match first. **Source**: the second reading of "match on SKU as well", handled as `references/ambiguity.md` describes, so it ships marked `assumed`. **Check**: the criterion is unmet if `test_name_match_outranks_foreign_sku` finds the SKU match first.

Slices: there is one slice, `search matches a full SKU`. The baseline run matters more than usual here, because criterion 1's Check compares the `search_ranking` output with its output before the first edit. Run it and quote it.

Wiring: no new wiring is needed. The change is inside a code path that callers already call, so the existing call site at `search/query.ts:60` makes the slice reachable from outside its module.

Stops: show the criteria only. Criterion 2 came from rereading the request, because "match on SKU as well" has a second reading where SKU matches outrank names. One edit undoes that choice, so criterion 2 ships marked `assumed`. The chosen reading ranks name matches first, so the SKU-first reading is dropped. If the user wanted the other reading, the ordering clause in `rankResults` changes.
