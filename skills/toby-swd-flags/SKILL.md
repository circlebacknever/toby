---
name: toby-swd-flags
description: >-
  Contains Toby's rules for a feature flag's kind, check site, tests, data,
  rollout, and removal. Entry skills open this file by path. Do not trigger it
  from a user request alone.
disable-model-invocation: true
---

# Toby SWD Flags

Add a flag so unfinished or risky code can ship turned off, and write its removal when you add it.

## Pick the kind

| Kind | Use it for | Remove it when |
| --- | --- | --- |
| Release | a slice that is not correct until a later slice ships | the feature is on for everyone |
| Kill switch | a risky path or dependency you may need to turn off in an incident | the path is retired |
| Experiment | comparing two behaviors on real traffic | the decision is made |

State the kind in the plan. When only some customers get a feature, use the repo's entitlement or plan system, and add no flag.

## Use the repo's flag system

Find how the repo reads flags, and read the new flag the same way, through the one config or flags module. `toby-swd-twelve-factor`'s `references/config.md` describes that module. Ask before adding a flag provider, a flags module, or a new dependency.

## Defaults

A release flag defaults to off, and the off path runs exactly today's code. A kill switch defaults to on. Its off path runs the safe behavior, so give that path a test. When the flag service is down, the code uses the last value it fetched, and uses the default only when it has never fetched one.

## One check site

Read the flag once per request, at the entry point, and pass the value down or pick an implementation there. Read a flag once at startup only when every user gets the same value and a restart to change it is acceptable. When a frontend and its API both read the flag, they can disagree for one user. Make the API accept requests from both frontend paths, or make the frontend use the value the API returns.

When the paths differ in more than a line or two, put each in its own function, and branch once at the check site. Do not nest one flag inside another.

## Tests

Run the existing tests with the flag at the value that runs today's code. That value is off for a release flag, and on for a kill switch around existing code. The tests must pass unchanged.

Then run them with the flag at its other value. Each test that fails must assert a behavior the flag is meant to change. Keep that test unchanged for today's value, and add a copy for the other value with the new expected result. Fix any other failure now, because it is a regression. Run the new slice's tests, including its end-to-end test, with the flag on.

## Data

Ship a schema change in the releases that `toby-swd-hardening`'s `references/deploys.md` lists, because a flag cannot hide it. Put only the code that reads the new column behind the flag. Keep writing the old column until the flag is gone, because the off path reads it. On a single instance, one release can add the column, write both columns, and add the flagged read.

Backfill before you turn the flag on. In the release that removes the flag, write only the new column. Drop the old column one release later, as steps 3 and 4 of `toby-swd-hardening`'s `references/deploys.md` say. A single instance that stops before the new release starts can do both in one release. That release needs a tested down migration.

## Rollout

Write the rollout as a list of steps, such as the team, then 5% of users, then everyone. For each step, state the metric to watch and the value at which someone turns the flag off. One example is checkout errors above 1% for ten minutes. A small app can use two steps, the team and then everyone. `toby-swd-observability` covers the metrics.

## Removal

When you add the flag, write its removal as a plan step or a ticket. Give the removal an owner, a date, and a condition. State the flag, how to turn it on, and the later slice that removes it. Put the kind and that condition in a comment at the check site.

Remove the flag by deleting the check and the path that lost. That path is the off path for a release flag, the losing path for an experiment, and the retired path for a kill switch. Delete the code that reads the flag first, deploy, and then delete the flag from the flag service. Deleting it from the service first makes the running code read the default, which turns a released feature off.
