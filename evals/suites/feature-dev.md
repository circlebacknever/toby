# Feature-dev sizing suite

This suite tests `toby-build` on two requests of different sizes: a one-file copy change and a multi-screen seat-limit feature. A person scores each run by reading it to verify that the workflow matches the size of the request.

## Request A: a copy change
> The invite email says "Click here to join" — change it to "Accept your
> invitation". It's in one template file.

Expected: the agent notes that a one-file copy edit follows the existing template pattern (`toby-build`'s skip clause) or sizes it as tactical, and makes the edit directly without acceptance criteria, a plan file, or a stop.

## Request B: seat limits
> Add per-workspace seat limits. When a workspace hits its seat cap, new invites
> should be rejected with a clear message, and admins should see the current
> usage on the billing page. Enforce it on the API too, not just the UI.

Expected: the agent sizes this request as strategic (`Mode: durable implementation (strategic)`), because it changes a billing/limit rule and crosses multiple screens and call sites. A passing run reads the existing code with `path:line` citations, writes the three-line acceptance criteria (`Observable`, `Source`, `Check`), names the vertical slices, offers to write the plan file at stop 1, and waits for approval.

## What a failing run looks like

- Request A gets three-line acceptance criteria, a plan file, or an approval stop.
- Request B is sized as tactical or skips offering a plan file at stop 1.
- Both requests receive the same amount of process.
