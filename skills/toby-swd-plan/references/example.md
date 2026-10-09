# Example plan folder

This plan covers team invites, which take two sessions, so it is a folder with an overview and one file per slice. The folder looks like this:

```text
docs/plans/members/team-invites/
  overview.md
  01-invite-shows-up-as-pending.md
  02-invite-email-opens-accept-screen.md
```

## overview.md

```markdown
# Toby's plan for team invites

Mode: durable implementation. Members can invite a teammate by email and see the
invite as pending until the teammate accepts it.

## Criteria
1. Submitting an email on the members screen shows that address in a Pending list
   without a reload.
2. The invited address receives one invite email with a link that opens the
   accept screen.
3. Opening a used or expired link shows an expired state and creates no account.
4. The members list still renders for an org with no pending invites.

Out of scope: bulk invites, revoking an invite, picking a role, and resending.
Each one is a follow-up.

## Design
- Structure chosen: an `invites` module with `createInvite(orgId, email, actor)`
  and `acceptInvite(token)`. It is the only code that reads or writes the
  `invites` table, and it sends the email.
- Alternative rejected: invite rows in `members` with a `pending` status. Every
  query on `members` would need a status filter.
- Rule: `Invite.isExpired()` returns whether an invite has expired.
  `acceptInvite` and the Pending list both call it.
- Hardening: only an org admin can invite, and the email field is capped at 254
  characters. The email goes through the existing `mailer` job, which already
  has a timeout and retries.
- Logs: the handlers log `invite.created` and `invite.accepted` with the invite
  id, and never the email address.
- Twelve-factor: none apply. The change adds no process, config value, or
  backing service.
- Refactor first: none. `members/list.ts` already renders any list of rows.

## Flag
`team-invites` is a release flag, off by default. Main deploys on every merge,
so group 1 reaches users before group 2 sends the email. The invites API reads
the flag once per request. The members screen shows the Invite section only
when `GET /orgs/:id/invites` returns 200, so only the API reads the flag.
Rollout: turn it on for the team, then for every org. Turn it off if
`invite.created` errors stay above 1% for ten minutes. The last step of group 2
removes it: delete the code that reads it, deploy, then delete it from the flag
service. Owner: Sam, by 2026-12-01.

## Whole-feature test
`e2e/invites.spec.ts`, "invite, accept, sign in". The test invites an address
as an admin, opens the link from the stub mail server, accepts, and signs in as
the new member. Group 2 adds it.

## Groups
| File | Slice | Criteria | Status |
| --- | --- | --- | --- |
| 01-invite-shows-up-as-pending.md | invite shows up as pending | 1, 4 | done |
| 02-invite-email-opens-accept-screen.md | the invite email opens the accept screen | 2, 3 | not started |
```

## 01-invite-shows-up-as-pending.md

```markdown
# Group 1: invite shows up as pending

This group meets criteria 1 and 4. Every step serves criterion 1.
Verification check 2 covers criterion 4.

## Steps
- [x] Create `e2e/invites.spec.ts` with the tests "invite shows up as pending"
      and "hidden when off". Run the first one and watch it fail.
- [x] Edit `api/invites.ts` to add `createInvite(orgId, email, actor)`, and create
      `db/migrations/0043_invites.sql` for the table it writes. The function
      returns the pending invite and rejects an address that already has an
      unexpired invite. `test_create_invite_rejects_duplicate` fails before it
      and passes after.
- [x] Ask before running `pnpm db:migrate` against the local database.
- [x] Edit `api/invites/router.ts` to register `POST /orgs/:id/invites` and
      `GET /orgs/:id/invites`. Edit `screens/Members.tsx` to add `<InviteForm>`
      and a Pending section that reads the GET route and shows a new invite
      before the server responds.
- [x] Add the `team-invites` flag to `flags/index.ts`, off by default. The
      invites router returns 404 when the flag is off. The members screen
      shows the Invite section only when `GET /orgs/:id/invites` returns 200.
      Put the flag's kind and removal condition in a comment where the router
      reads it.

## Verification
1. Run `pnpm e2e invites.spec.ts -g "invite shows up as pending"` with the flag
   on. The test signs in as an org admin, submits `new@example.com`, and reads
   the Pending list. It fails before the work. After the work, the group fails
   when the address is missing, needs a reload, or is gone after a reload.

       before  invite shows up as pending  FAIL  no Invite form on the members screen
       after   invite shows up as pending  PASS

2. Run `pnpm test members` with the flag off, before the first edit and after
   the last. The group fails when any existing test fails or had to change. Run
   it again with the flag on. Each test that fails there must assert behavior
   the flag changes. Keep that test as the flag-off case, with the flag set off
   inside the test, and add a flag-on copy. This check covers criterion 4.

       before  pnpm test members, flag off  PASS
       after   pnpm test members, flag off  PASS
       after   pnpm test members, flag on   PASS

3. Run `pnpm e2e invites.spec.ts -g "hidden when off"` with the flag off. The
   group fails when the Invite section renders, or when the POST route returns
   anything but 404.

       before  hidden when off  PASS
       after   hidden when off  PASS

Stop here. Before group 2, the user decides whether a Pending row also shows
who sent the invite and when it expires.

In session 1, the user chose to show both. Group 2's steps now add the
inviter's name and the expiry date to each Pending row.
```
