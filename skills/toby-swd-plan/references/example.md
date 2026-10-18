# Example plan folder

This example shows a two-session plan folder for team invites, with `overview.md` and one file per slice:

```text
docs/plans/members/team-invites/
  overview.md
  01-invite-shows-up-as-pending.md
  02-invite-email-opens-accept-screen.md
```

## overview.md

```markdown
# Toby's plan for team invites

## Intent
The user's words: "Let org admins invite a teammate by email." The result: an
admin invites an address, sees it as pending, and the teammate opens the email
link, accepts, and signs in as a member.

Done when: `e2e/invites.spec.ts` "invite, accept, sign in" invites an address,
opens the link from the stub mail server, accepts, and signs in as the new
member on the members screen.

Mode: durable implementation.

## Criteria
1. Submitting an email on the members screen shows that address in a Pending list
   without a reload.
2. The invited address receives one invite email with a link that opens the
   accept screen.
3. Opening a used or expired link shows an expired state and doesn't create an
   account.
4. The members list still renders for an org without pending invites.

## Out of scope
- Bulk invites, because the members screen takes one address at a time.
- Picking a role, because every new member joins with the default member role
   that `members/roles.ts` assigns.
- Revoking or resending an invite, unless the user adds it before group 2 starts.

## Design
- Structure we chose: an `invites` module with `createInvite(orgId, email, actor)`
  and `acceptInvite(token)` that writes the `invites` table and enqueues the
  invite email.
- Alternative we rejected: storing pending invites in `members` with a `pending`
  status, which would force every member query to filter out pending rows.
- Rule: `Invite.isExpired()` computes whether an invite has expired, and both
  `acceptInvite` and the Pending list call it.
- Hardening: only an org admin can invite, the handler caps the email input at
  254 characters, and `mailer` sends the email with a timeout and idempotency key.
- Logs: handlers log `invite.created` and `invite.accepted` with `invite_id` and
  `duration_ms`, and omit the email address.
- Twelve-factor: the change uses existing processes, config, and backing services.
- Refactor first: `members/list.ts` already renders any row list without a
  refactor beforehand.

## Flag
`team-invites` is a release flag, off by default, because `main` deploys on
every merge. The invites API reads the flag once per request, and the members
screen renders the Invite section only when `GET /orgs/:id/invites` returns 200.
After group 2 ships, enable the flag for the internal org, then 10% of orgs
hashed by `org_id`, then 100%. Turn the flag off if `invite.created` errors
exceed 1% for 10 minutes. Owner: Sam, removal after 100% rollout by 2026-12-01.

## Groups
| File | Slice | Criteria | Depends on | Status |
| --- | --- | --- | --- | --- |
| 01-invite-shows-up-as-pending.md | invite shows up as pending | 1, 4 | — | done |
| 02-invite-email-opens-accept-screen.md | the invite email opens the accept screen | 2, 3 | 01 | not started |
```

## 01-invite-shows-up-as-pending.md

```markdown
# Group 1

Slice: `invite shows up as pending`. This group meets criteria 1 and 4.
Rollback: drop the `invites` table with `0043_invites_down.sql` and turn off
`team-invites`.

## Steps
- [x] Create `e2e/invites.spec.ts` with the tests "invite shows up as pending"
      and "hidden when off". Run both before the feature edits: the first fails
      and the second passes.
- [x] Edit `api/invites.ts` to add `createInvite(orgId, email, actor)`, and create
      `db/migrations/0043_invites.sql` for the `invites` table. The function
      returns the pending invite and rejects a duplicate unexpired invite. Run
      `test_create_invite_rejects_duplicate` before and after the edit.
- [x] Ask before running `pnpm db:migrate` against the local database.
- [x] Edit `api/invites/router.ts` to register `POST /orgs/:id/invites` and
      `GET /orgs/:id/invites` behind the `team-invites` flag in `flags/index.ts`.
      Add a comment at the check site stating the flag's kind and removal condition.
- [x] Edit `screens/Members.tsx` to render `<InviteForm>` and the Pending list
      when `GET /orgs/:id/invites` returns 200.

## Verification
1. Run `pnpm e2e invites.spec.ts -g "invite shows up as pending"` with
   `team-invites` on. The test signs in as an org admin, submits
   `new@example.com`, and checks the Pending list.

       before  invite shows up as pending  FAIL  no Invite form on the members screen
       after   invite shows up as pending  PASS

2. Run `pnpm test members` with `team-invites` off and on (criterion 4).

       before  pnpm test members, flag off  PASS
       after   pnpm test members, flag off  PASS
       after   pnpm test members, flag on   PASS

3. Run `pnpm e2e invites.spec.ts -g "hidden when off"` with `team-invites` off.

       before  hidden when off  PASS
       after   hidden when off  PASS

Stop here. Before group 2 starts, confirm whether a Pending row also displays
the inviter and expiration timestamp.
```
