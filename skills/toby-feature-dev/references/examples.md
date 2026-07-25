# Worked cuts

Four feature shapes, cut into slices, all four in one invented repo: orders, a members screen, a billing module, a search path. The behavior record at the bottom is what these four left behind, which is why it holds two of them and one retirement. Each shape shows the criteria in full, the slice order and its name, the wiring line that proves the slice is reachable, and where a stop earns its place. The paths are invented; the shape is what survived contact with a real repo.

Every criterion below carries all three lines, because a criterion missing one is the thing the skill tells you to drop.

## 1. Brownfield, one seam — new endpoint on an existing resource

Request: "let people cancel an order from the account page."

1. Observable — a POST to `/orders/:id/cancel` on an order the caller owns returns the order with status `cancelled`. Source — user: "cancel an order". Check — `test_cancel_returns_cancelled_order`, unmet if the status stays `open`.
2. Observable — cancelling an order already shipped returns 409 and leaves the order untouched. Source — user: "no cancelling once it's out the door", backed by `api/orders.ts:88`, the shipped-state guard refunds already run. Check — `test_cancel_rejects_shipped`, unmet if the order changes.
3. Observable — cancelling someone else's order returns 404. Source — `api/orders.ts:31`, the ownership check every other order route runs; the request is silent on this. Check — `test_cancel_scopes_to_owner`, unmet on any 2xx.
4. Stays working — the order list still returns shipped and open orders unchanged. Source — the existing contract. Check — the `orders_list` suite, unmet on any changed row.

Slices: one, `an open order can be cancelled from the account page`. All four criteria arrive at the same seam, an HTTP request to the orders API.

Wiring: `api/routes.ts:142` — `router.post('/orders/:id/cancel', cancelOrder)`. Without that line the handler is a well-tested function nothing can reach.

Stops: criteria only, one line, keep moving. No strategic trigger — the route is new, the boundary isn't, and `api/orders.ts` is the sibling at path:line. No plan file for a one-slice tactical change.

Record: criteria 1 and 2 quote a person, so both get entries. Criterion 3 cites a repo fact, so it gets none.

## 2. Two seams — a flow crossing two screens

Request: "users should be able to invite a teammate and see the invite pending."

1. Observable — submitting an email on the members screen shows that address in a Pending list without a reload. Source — user: "see the invite pending". Check — `test_invite_appears_pending`, unmet if the address needs a reload.
2. Observable — the invited address receives one invite email carrying a link that opens the accept screen. Source — user: "invite a teammate". Check — `test_invite_email_link_opens_accept`, unmet on zero or two emails.
3. Observable — opening a used or expired link shows an expired state and creates no account. Source — user, on the follow-up about resent links: "once I resend, the first link should be scrap". Check — `test_expired_link_creates_no_account`, unmet if an account exists after.
4. Stays working — the members list still renders for an org with no pending invites. Source — the existing contract. Check — `members_list` suite.

Slices: two, named for what each one lets someone do — `invite shows up as pending`, then `the invite email opens the accept screen`. Criteria 1 and 4 land at the members screen; 2 and 3 land at the mail and the accept route. Different seams, different slices.

Wiring: slice one at `screens/Members.tsx:210` — `<InviteForm onSubmit={createInvite} />`. Slice two at `jobs/index.ts:17`, the `invite.created` subscription.

Stops: criteria, then a plan file, since this spans two slices. Slice one ends on a boundary carrying a real question — the pending row shows the address, and whether it also shows the inviter and the expiry decides the second slice's shape. Stop there. Had it raised nothing, three lines and keep moving.

Slice one depends on slice two to be worth anything: an invite that creates a row and mails nobody is half-built behavior a user can reach. So `invites.form` defaults off, slice one is observed with it on, and the flag flips for real when slice two's send lands. Slice two's last checkbox deletes it. A staging flag still set after its slice ships is a config option nobody decided to add.

## 3. Greenfield — a subsystem with no sibling

Request: "we need usage metering so we can bill by seat next quarter."

The same subsystem asked for differently — "a quick PoC of the metering dashboard so I can see if the layout works" — never reaches this section. That is experiment mode: hand it to toby-swd-experiment, say in one line what would move it to durable, and write no criteria, no slices, no record. What follows is what arrives after the user has seen a layout they like and asks for the real one. The layout survives; the code under it does not.

Nothing nearby resembles this: no metering module, no counter storage, no billing surface. Greenfield, so the design pass runs through toby-swd-strategy before any code, and a plan file is written whatever the slice count.

1. Observable — an admin opening the usage page for a workspace sees the seat count as of the last completed day. Source — user: "so we can bill by seat". Check — `test_usage_page_shows_completed_day_count`, unmet if it shows a partial day.
2. Observable — a seat added and removed inside one day counts once for that day. Source — user: "someone joining and leaving shouldn't double-bill them". Check — `test_seat_churn_counts_once`, unmet at two.
3. Observable — a workspace with no activity returns a zero row, no missing row. Source — `billing/invoice.ts:52`, which throws on a gap. Check — `test_idle_workspace_returns_zero`, unmet on a missing row.

Greenfield's extra work, before the second file exists:

- Nearest conventions the repo already has: `billing/` for money-adjacent modules and the `jobs/` daily aggregate shape used by `jobs/revenue_rollup.ts`. Extend those two; don't invent a third layout.
- Boundary written once, per toby-swd-modules and toby-swd-interfaces: the module exposes `seatCountForDay(workspace, date)` and owns the storage shape behind it. Callers never touch rows.
- The naming call goes to the user. `seat`, `member`, and `active user` mean the same thing today and one of them is about to appear on an invoice.

Slices: two — `the CLI reports a day's seat count` (`bin/usage show --workspace X --date Y`), then `the usage page shows it`. Counting ships first because the page has nothing to render without it, and the CLI is what keeps slice one from being a layer cut nobody can open.

Stops: criteria, then the design pass, then the plan. Both a persisted shape and money are strategic triggers, so the design lines are owed before the plan can name a file.

## 4. Changing behavior that already ships

Request: "the search should match on SKU as well as product name."

1. Observable — searching a full SKU returns that product first. Source — user: "the search should match on SKU as well". Check — `test_full_sku_ranks_first`, unmet if any name match outranks it.
2. Observable — searching a product name returns what it returned before, in the same order. Source — the existing `search_ranking` suite, which is the contract. Check — that suite, unmet on any ordering change.
3. Observable — a query matching a name and a different product's SKU returns the name match first. Source — the ambiguity pass on "match on SKU as well", shipped `assumed`. Check — `test_name_match_outranks_foreign_sku`, unmet if the SKU match leads.

Slices: one, `search matches a full SKU`. The baseline run matters more than usual here, because criterion 2 is a claim about what `search_ranking` printed before the first edit. Run it and quote it. After the first edit, "it returned the same order before" is a memory.

Wiring: none new. The change sits inside a reached path, so the fourth slice condition is met by the existing call site at `search/query.ts:60`, cited.

Stops: criteria only. Criterion 3 came out of the ambiguity pass — "match on SKU as well" holds a second reading where SKU matches outrank names. One edit undoes it, so it ships marked `assumed`: reading taken is name-first, reading dropped is SKU-first, and what changes if they wanted the other is the ordering clause in `rankResults`.

# A plan an operator can approve

Slice one of the invite flow. Format is AGENTS.md's; the detail in each step is what makes it reviewable.

```markdown
# Toby's plan for team invites

Mode: durable implementation. Members can invite a teammate by email and watch the
invite sit in a pending list until it's accepted.

Criteria, in the wording agreed before coding:
1. Submitting an email on the members screen shows that address in a Pending list
   without a reload.
2. The invited address receives one invite email carrying a link that opens the
   accept screen.
3. Opening a used or expired link shows an expired state and creates no account.
4. The members list still renders for an org with no pending invites.

Out of scope: bulk invites, invite revocation, role selection at invite time,
resend. Each is a follow-up, none is in this plan.

## Group 1 — invite shows up as pending (criteria 1, 4)

- [ ] Create `db/migrations/0043_invites.sql` — `invites` table: id, org_id,
      email, invited_by, created_at, expires_at, accepted_at. Serves criterion 1.
      Proved by the migration running against a scratch database and
      `\d invites` showing the columns.
- [ ] Edit `api/invites.ts` — add `createInvite(orgId, email, actor)` returning the
      pending row, rejecting an address already invited and unexpired. Serves
      criterion 1. Proved by `test_invite_appears_pending`; fails if a duplicate
      creates a second row.
- [ ] Edit `api/routes.ts` — register `POST /orgs/:id/invites`. Serves criterion 1.
      Without this the handler is unreachable.
- [ ] Edit `screens/Members.tsx` — add `<InviteForm>` and a Pending section reading
      the new endpoint, appending optimistically. Serves criterion 1. Proved by
      `test_invite_appears_pending`; fails if the address needs a reload.
- [ ] Add `flags/invites.form` defaulted off, so the invite entry point stays dark
      until group 2's send lands. Serves criterion 1 standing correct on its own;
      group 1 is observed with the flag on.

### Verification — hard stop

- Run `pnpm test members_list` before the first edit and quote it. Criterion 4 is a
  claim about that output.
- Run `pnpm test api/invites screens/Members`. Both new tests fail before the
  change and pass after; quote both runs.
- Open the members screen, invite an address, see it in Pending with no reload.
- Approval needed on its own: `pnpm db:migrate` against the local database.
- Behavior record: append criteria 1 and 2 to `docs/behavior.md`, bind criterion 1's
  sentence into the test docstring, run the record check.

Stop here. Group 2 waits for a yes.

## Group 2 — the email and the accept screen (criteria 2, 3)
...
```

# Behavior record, filled

`docs/behavior.md`, or whichever file this repo already keeps for stated behavior.

```markdown
# What this product does, and who asked for it

One heading, one behavior, stated the way someone outside the code sees it. Under it,
who asked and the words they used. Every heading is quoted verbatim in a test
description. Anything under Retired stopped being true on the date beside it.

## A cancel request from the account holder on an open order returns the order with status cancelled
Asked 2026-07-24 by the user: "let people cancel an order from the account page"

## A cancel request on a shipped order is refused and the order is left unchanged
Asked 2026-07-24 by the user: "no cancelling once it's out the door"

## After an invite is submitted, the invited address appears in the members screen's pending list
Asked 2026-08-02 by the support lead: "they invite someone and then have no idea whether it worked"

## Retired

## A cancel request more than 24 hours after the order was placed is refused
Asked 2026-03-11 by the user: "cancellations only inside a day"
Retired 2026-05-02 — per-merchant cancellation policies replaced the fixed window. The 24 hours came from one merchant's support queue in March.
```

Bindings, the sentence quoted verbatim in the test description:

```python
def test_cancel_returns_cancelled_order():
    """A cancel request from the account holder on an open order returns the order with status cancelled."""
```

```tsx
it("After an invite is submitted, the invited address appears in the members screen's pending list", () => { ... })
```

The heading is the identifier, so the check is one fixed-string grep per entry and there is nothing to allocate, increment, or collide on. Two branches writing the same sentence wrote the same behavior, and that conflict is the correct outcome.

What the record does not hold: no test list, since the grep derives it and a list you never wrote can't go stale; no rationale or alternatives, which toby-swd-docs and toby-swd-strategy own; no task list, which is the plan's job; no status beyond living above or below the Retired heading.
