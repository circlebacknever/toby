# Toby's plan for the feature flag skill

Work mode: durable implementation. Flags get checked in many files, tested only with the flag on, and never removed.

## Group 6: a flagged slice has one check site and a removal step

- [x] Create `skills/toby-swd-flags/SKILL.md` as a hidden method skill. It covers these topics:
  - four kinds of flag, and when each one gets removed
  - the repo's flag system, read through the one config or flags module
  - a default and an off path that match today's behavior
  - one check site at the entry point or composition root
  - tests with the flag off and with it on
  - a removal step written when the flag is added
  - the rule that a schema change stays compatible with both paths
- [x] Replace the flag sentences in `toby-build`'s "Cut the work into slices" with a pointer to `toby-swd-flags`, so the flag rules exist in one place.
- [x] In `skills/toby-build/SKILL.md`, open `toby-swd-flags` when a slice ships behind a flag, or when the request asks for a flag, a rollout, or a kill switch.
- [x] Add the skill to `build-service` in `ROUTING_GROUPS`, to the token scenario, and to the README.

### Verification

- Run `python3 evals/run.py gates`. The lost-rules gate fails if a flag sentence left `toby-build` with no survivor.
- Trace "ship the new checkout behind a flag" through `toby-build`. The trace passes when the plan states the flag kind, one check site, a test with the flag off and one with it on, and a removal step. It fails when any of the four is missing.
- Trace a two-slice feature whose first slice does not depend on the second. The trace must not add a flag, because the first slice is correct on its own.
- Run `python3 scripts/voice-check.py --review` on every new or changed file, and read each sentence against the READ list.

If a check fails, stop and report it before Group 7.
