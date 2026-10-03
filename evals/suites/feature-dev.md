# Feature-dev sizing suite

Two requests, one small and one large. The skill has to give them different
amounts of process. A person scores each run by reading it, because the test
is whether the amount of process fits the request.

## Request A — a copy change
> The invite email says "Click here to join" — change it to "Accept your
> invitation". It's in one template file.

Expected: the agent sizes this request as tactical and makes the edit with no
criteria, plan, or stop. This is a one-file edit following
a pattern already in that file, which the skill's own skip clause names. A run
that produces acceptance criteria and a named Check command for this has failed.

## Request B — seat limits
> Add per-workspace seat limits. When a workspace hits its seat cap, new invites
> should be rejected with a clear message, and admins should see the current
> usage on the billing page. Enforce it on the API too, not just the UI.

Expected: the agent sizes this request as strategic, because it matches two
triggers. Billing is on the trigger list, and the behavior changes at three call
sites. A passing run produces the three-line criteria form, all four discovery
items, named slices, a wait at stop 1, and a written plan.

## What a failing run looks like

- Request A gets criteria, a plan, or a stop.
- Request B gets sized tactical, or its plan file skipped.
- Either request gets the same amount of process as the other.
