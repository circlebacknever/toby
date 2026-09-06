# Feature-dev sizing suite

Two requests, one small and one large. The skill has to give them different
amounts of process. Scored by reading, because the question is whether the
ceremony fits the request.

## Request A — a copy change
> The invite email says "Click here to join" — change it to "Accept your
> invitation". It's in one template file.

Expected: tactical, and handed straight back. This is a one-file edit following
a pattern already in that file, which the skill's own skip clause names. A run
that produces acceptance criteria and a named Check command for this has failed.

## Request B — seat limits
> Add per-workspace seat limits. When a workspace hits its seat cap, new invites
> should be rejected with a clear message, and admins should see the current
> usage on the billing page. Enforce it on the API too, not just the UI.

Expected: strategic, on two triggers at once. Billing is on the trigger list,
and the behavior lands at three call sites. Owes the three-line criteria form,
all four discovery items, named slices, a wait at stop 1, a written plan, and a
behavior-record entry per criterion.

## What a failing run looks like

- Request A gets criteria, a plan, or a stop.
- Request B gets sized tactical, or its plan file skipped.
- Either request gets the same amount of process as the other.
