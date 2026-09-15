# Worked cuts

These examples cut four kinds of feature into slices. All four use one invented repo with orders, a members screen, a billing module, and a search path. The behavior record at the bottom has entries for two of the four features and one retired entry. Each example shows the criteria in full, the slice order and names, and the wiring line that proves the slice is reachable. It also shows where a stop is worth making. The paths are invented, but the method comes from work in a real repo.

Every criterion below has all three lines, because a criterion missing one is the thing the skill tells you to drop.

## 1. Brownfield, one entry point — new endpoint on an existing resource

Request: "let people cancel an order from the account page."

1. Observable — a POST to `/orders/:id/cancel` on an order the caller owns returns the order with status `cancelled`. Source — the user said "cancel an order". Check — the criterion is unmet if `test_cancel_returns_cancelled_order` finds that the status stays `open`.
2. Observable — cancelling an order already shipped returns 409 and leaves the order untouched. Source — the user said "no cancelling once it's out the door". `api/orders.ts:88` supports it with the shipped-state guard that the refund path already runs. Check — the criterion is unmet if `test_cancel_rejects_shipped` finds that the order changed.
3. Observable — cancelling someone else's order returns 404. Source — the request says nothing about this case, but `api/orders.ts:31` has the ownership check every other order route runs. Check — the criterion is unmet if `test_cancel_scopes_to_owner` gets any 2xx.
4. Stays working — the order list still returns shipped and open orders unchanged. Source — the behavior is part of the existing contract. Check — the criterion is unmet if the `orders_list` suite finds any changed row.

Slices: there is one slice, `an open order can be cancelled from the account page`. All four criteria are observed at the same entry point, which is an HTTP request to the orders API.

Wiring: `api/routes.ts:142` registers the route with `router.post('/orders/:id/cancel', cancelOrder)`. Without that line, the handler is unreachable, however well it is tested.

Stops: show the criteria in one line and keep working. The strategic triggers do not apply, because the boundary already exists even though the route is new. `api/orders.ts` is the sibling at path:line. A one-slice tactical change gets no plan file.

Record: criteria 1 and 2 quote a person, so both get entries. Criterion 3 cites a repo fact, so it gets none.

## 2. Two entry points — a flow crossing two screens

Request: "users should be able to invite a teammate and see the invite pending."

1. Observable — submitting an email on the members screen shows that address in a Pending list without a reload. Source — the user said "see the invite pending". Check — the criterion is unmet if `test_invite_appears_pending` finds that the address needs a reload.
2. Observable — the invited address receives one invite email with a link that opens the accept screen. Source — the user said "invite a teammate". Check — the criterion is unmet if `test_invite_email_link_opens_accept` finds zero or two emails.
3. Observable — opening a used or expired link shows an expired state and creates no account. Source — in the follow-up about resent links, the user said "once I resend, the first link should be scrap". Check — the criterion is unmet if `test_expired_link_creates_no_account` finds that an account exists afterwards.
4. Stays working — the members list still renders for an org with no pending invites. Source — the behavior is part of the existing contract. Check — the `members_list` suite tests it.

Slices: there are two, each named for what it lets someone do. The first is `invite shows up as pending`, and the second is `the invite email opens the accept screen`. Criteria 1 and 4 are observed at the members screen, and criteria 2 and 3 at the mail and the accept route. The criteria are observed at different entry points, so they form different slices.

Wiring: slice one connects at `screens/Members.tsx:210` through `<InviteForm onSubmit={createInvite} />`, and slice two connects at `jobs/index.ts:17` through the `invite.created` subscription.

Stops: show the criteria, then write a plan file, since this feature spans two slices. The first slice ends at a point where the user has a question to answer. The pending row shows the address, but what the second slice does depends on whether it also shows the inviter and the expiry. So stop there. If the user had no question at that point, the report would be three lines and the work would continue.

Slice one has no value to a user without slice two. An invite that creates a row and mails nobody is half-built behavior that a user can trigger. So the `invites.form` flag defaults off, which means slice one is observed with the flag on. The flag is switched on for users when slice two's send ships. The last checkbox in slice two is the step that deletes the flag. A staging flag still set after its slice ships is a config option that was added without a decision.

## 3. Greenfield — a subsystem with no sibling

Request: "we need usage metering so we can bill by seat next quarter."

A user could ask for the same subsystem as "a quick PoC of the metering dashboard so I can see if the layout works". That request is experiment mode, so this section does not apply to it. Hand it to toby-swd-experiment, say in one line what would move it to durable, and write no criteria, no slices, no record. The example below starts after the user has seen a layout they like and asks for the real dashboard. The layout is kept, but the code that implements it is replaced.

This subsystem has no sibling in the repo, because the repo has no metering module, no counter storage, and no billing screen or endpoint. This work is greenfield, so the design pass uses toby-swd-strategy before any code is written. A plan file is written whatever the slice count.

1. Observable — an admin opening the usage page for a workspace sees the seat count as of the last completed day. Source — the user said "so we can bill by seat". Check — the criterion is unmet if `test_usage_page_shows_completed_day_count` finds that the page shows a partial day.
2. Observable — a seat added and removed inside one day counts once for that day. Source — the user said "someone joining and leaving shouldn't double-bill them". Check — the criterion is unmet if `test_seat_churn_counts_once` finds a count of two.
3. Observable — a workspace with no activity still returns a row, with a count of zero. Source — `billing/invoice.ts:52` throws on a gap. Check — the criterion is unmet if `test_idle_workspace_returns_zero` finds a missing row.

Before the second file exists, greenfield work adds these steps:

- The nearest conventions the repo already has are `billing/` for money-adjacent modules and the `jobs/` daily aggregate pattern that `jobs/revenue_rollup.ts` uses. Extend those two, and don't invent a third layout.
- The boundary is written once, per toby-swd-modules and toby-swd-interfaces. The module exposes `seatCountForDay(workspace, date)` and defines the storage layout that the function reads, so callers never read or write rows directly.
- The user chooses the name. Today `seat`, `member`, and `active user` mean the same thing, but one of them is about to appear on an invoice.

Slices: there are two, first `the CLI reports a day's seat count` (`bin/usage show --workspace X --date Y`), then `the usage page shows it`. Counting ships first because the page has nothing to render without it. The CLI gives slice one an entry point a user can run, so slice one is not a layer cut.

Stops: show the criteria, then run the design pass, then write the plan. A persisted format and money are both strategic triggers, so the design lines come before the plan names any file.

## 4. Changing behavior that already ships

Request: "the search should match on SKU as well as product name."

1. Observable — searching a full SKU returns that product first. Source — the user said "the search should match on SKU as well". Check — the criterion is unmet if `test_full_sku_ranks_first` finds any name match ranked above it.
2. Observable — searching a product name returns what it returned before, in the same order. Source — the existing `search_ranking` suite is the contract. Check — the criterion is unmet if that suite finds any ordering change.
3. Observable — a query matching a name and a different product's SKU returns the name match first. Source — the ambiguity pass on "match on SKU as well" produced it, so it ships marked `assumed`. Check — the criterion is unmet if `test_name_match_outranks_foreign_sku` finds the SKU match first.

Slices: there is one slice, `search matches a full SKU`. The baseline run matters more than usual here, because criterion 2 is a claim about what `search_ranking` printed before the first edit. Run it and quote it. After the first edit, the only evidence for "it returned the same order before" is someone's memory.

Wiring: no new wiring is needed. The change is inside a code path that callers already call, so the existing call site at `search/query.ts:60` meets the fourth slice condition.

Stops: show the criteria only. Criterion 3 came out of the ambiguity pass, because "match on SKU as well" has a second reading where SKU matches outrank names. One edit undoes that choice, so criterion 3 ships marked `assumed`. The chosen reading ranks name matches first, so the SKU-first reading is dropped. If the user wanted the other reading, the ordering clause in `rankResults` changes.

# A plan an operator can approve

The plan below covers slice one of the invite flow, in the operating guide's plan format. The detail in each step is what makes it reviewable.

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

## Group 1: the invite appears as pending (criteria 1 and 4)

- [ ] Create `db/migrations/0043_invites.sql` with an `invites` table. The table
      has the columns id, org_id, email, invited_by, created_at, expires_at, and
      accepted_at. This step serves criterion 1. It is proved when the migration
      runs against a scratch database and `\d invites` lists the columns.
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
- Append criteria 1 and 2 to `docs/behavior.md`. Copy criterion 1's sentence into
  the test docstring, and run the record check.

Stop here. Do not start group 2 until the operator approves.

## Group 2: the email and the accept screen (criteria 2 and 3)
...
```

# Behavior record, filled

The record below is `docs/behavior.md`, or whichever file this repo already keeps for stated behavior.

```markdown
# What this product does, and who asked for it

Each heading states one behavior the way someone outside the code sees it. Under each heading, the entry gives
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

Each binding quotes the sentence verbatim in the test description:

```python
def test_cancel_returns_cancelled_order():
    """A cancel request from the account holder on an open order returns the order with status cancelled."""
```

```tsx
it("After an invite is submitted, the invited address appears in the members screen's pending list", () => { ... })
```

The heading is the identifier, so the check is one fixed-string grep per entry. The record has no ID to allocate, increment, or collide on. When two branches write the same sentence, they describe the same behavior, so the merge conflict is the correct outcome.

The record has no test list, because the grep derives it. A derived list cannot go out of date. It has no rationale or alternatives, which toby-swd-docs and toby-swd-strategy cover. It has no task list, which is the plan's job. It records no status beyond whether an entry is above or below the Retired heading.
