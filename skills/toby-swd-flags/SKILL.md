---
name: toby-swd-flags
description: >-
  Contains Toby's rules for a feature flag's kind, check site, tests, data,
  rollout, and removal. Use it when adding, rolling out, or removing a release
  flag, a kill switch, or an experiment flag. Skip it for a config value that
  isn't a flag, which toby-swd-twelve-factor covers.
---

# Toby SWD Flags

Add a flag so unfinished or risky code can ship turned off, and plan its removal when you add it.

## Pick the kind

| Kind | Use it for | Remove it when |
| --- | --- | --- |
| Release | a slice that isn't complete until a later slice ships | the feature is on for everyone |
| Kill switch | a risky path or external dependency you may need to disable during an incident | you retire the path |
| Experiment | comparing two behaviors on production traffic | the team picks the winner |

State the kind in the plan. When a feature is permanent for specific customer tiers, use the repo's entitlement or plan check and don't add a feature flag.

## Flag system

Read the new flag through the repo's existing flags or config module (`toby-swd-twelve-factor`'s `references/config.md`), and ask before adding a flag provider, module, or dependency.

## Defaults

Set a release flag to `off` by default so the app runs today's code unchanged. Set a kill switch to `on` by default so turning it `off` runs the safe fallback. When the flag service is unreachable, keep the last fetched value and fall back to the default only before the first fetch.

## One check site

Read the flag once per request at the entry point, and pass the chosen behavior or implementation down. For percentage rollouts and experiments, hash the flag on a stable id (`user_id` or `org_id`) so each user gets a consistent experience, and pass that value into any background job.

When a frontend and an API both depend on the flag, read the flag from the API response on the frontend, or make the API accept requests from both frontend paths. When the two paths differ by more than a couple of lines, extract each into its own function and branch once at the check site. Never nest flags.

## Tests

1. Run the existing test suite with the flag set to today's path (`off` for a release flag, `on` for a kill switch), and confirm every test passes unchanged.
2. Flip the flag and rerun the suite: keep each test that fails on intentionally changed behavior as the old-path test, add a copy asserting the new path, and fix any unexpected failure.
3. Run all tests for the new slice (including its `toby-swd-e2e` test) with the flag on.

## Data

A flag guards code paths and can't hide a breaking schema change. Follow `toby-swd-hardening`'s `references/deploys.md`: write both the old and new columns while the flag exists, backfill before enabling the flag, put only the new-column read behind the flag, and drop the old column after you remove the flag.

## Rollout

State the rollout steps (such as internal team, 5% of users, then 100%) and the metric threshold that triggers a rollback (`checkout.failed` above 1% for 10 minutes, `toby-swd-observability`).

## Removal

When adding a flag, record its owner, target removal date, and removal condition in the plan and in a comment at the check site. After rollout completes, deploy a code change that removes the flag check and dead code path first, then delete the flag from the flag service once that deploy is live.
