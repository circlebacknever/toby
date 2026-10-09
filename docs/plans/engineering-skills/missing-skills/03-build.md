# Group 3: `toby-build` is short and writes plans as folders of slices

This group meets criteria 3, 5, 6, and 7 in the overview. Its owner edits `skills/toby-build/**`, `skills/toby-swd-plan/**`, `base/toby.md`, and the copies `scripts/sync.sh` writes.

## Steps

- [x] Cut the body of `skills/toby-build/SKILL.md` from 2,624 words to about 1,200. Write the body as numbered steps in the order the work runs, and open each method skill inside the step that uses it. Delete the separate method-skill list and "The running order".
- [x] Keep "tactical" and "strategic" as the two sizes. Keep the strategic triggers in the body, because sizing happens first, and keep one sentence per size in the body.
- [x] Add work the user expects to take more than one session to the strategic triggers. Restore the rule that adding only an optional part to a contract stays tactical, such as one more field in a response.
- [x] Move the three-line criterion form, the rules for its Source line, the vocabulary rule, and "Criteria are fixed text" to a new `references/criteria.md`. Open that file at the criteria step for every build, because tactical work needs its rules too. The body keeps the one-line form and the rule that a Check states the result that means it failed.
- [x] Write the design step. When the change adds or moves a business rule, an entry point, a write, or an outbound call, open `toby-swd-architecture` and `toby-swd-strategy`. Then open by trigger:
  - `toby-swd-modules` for a new module or boundary
  - `toby-swd-interfaces` for a new or changed signature
  - `toby-swd-extensibility` when the design branches on a type, kind, status, or provider, or adds an implementation or a subclass
  - `toby-swd-errors` for a failure case, a retry, a timeout, or validation
  - `toby-optimize` for a stated time or memory budget, or a cache, batch, or queue added for speed
  - `toby-swd-hardening` and `toby-swd-observability` for a new entry point, job, consumer, or outbound call, a new write or failure path in an existing handler, or a request about logging, metrics, alerts, or hardening
  - `toby-swd-twelve-factor` for a new process, worker, or scheduler, a new config value or secret, or a new backing service
  - `toby-swd-flags` when a slice ships behind a flag or the request asks for one
- [x] State these design lines at both sizes: the structure chosen, the alternative rejected, the one function that computes each rule the change adds, and any refactor that runs first. Strategic work also writes the rest of the design lines in `references/strategic.md`, which gains a line for the hardening, twelve-factor, and observability checks that apply.
- [x] At the design step, open `toby-swd-campfire`, answer its "Before the first edit" list, and put each refactor in the design lines. Run that refactor before the feature code. After each slice's proof, run its "After the tests pass" section. Put both in the order of work at both sizes.
- [x] Keep every other skill `toby-build` opens today: `toby-swd-testing`, `toby-swd-docs`, `toby-swd-environment`, and `toby-swd-clarity`.
- [x] Open `toby-swd-e2e` at the criteria step, before the Check lines of strategic work are written. In tactical work, open it when no test drives the entry point the change alters. For work with more than one slice, add the whole-feature test and its two runs to the final response.
- [x] Narrow the skip rule in the description. A one-file edit that copies a pattern skips the skill, unless it adds a case to a branch on a type, kind, or status, or adds a money or permissions rule. Change the description's "in the smallest step" to "in slices the user can review one at a time".
- [x] In `references/checks.md`, narrow the wrapper entry to an interface or adapter with one implementation whose methods only forward calls. Say that moving a rule into the module that owns its data is allowed. Let the uninvited-migration entry allow a refactor that campfire's first step allows. Rewrite "Two exceptions pass this entry" in plain words.
- [x] Rewrite the opening of `references/ambiguity.md` in plain words.
- [x] Create `skills/toby-swd-plan/SKILL.md`, a hidden method skill of about 600 words, with `agents/openai.yaml`. It covers:
  - cutting work into slices
  - the plan folder for a multi-session plan, with `overview.md` and one `NN-<slice-name>.md` per group, and what each file holds
  - one check per group that runs the slice where a user reaches it, with the result that means it failed
  - checks that pass whether or not the work is right, with two examples
  - the last group running one test through the whole feature
- [x] Move the slicing and plan-document sections of `references/strategic.md` into `toby-swd-plan`, and leave one pointer. Drop the rule that every step says what proves it. A step gets its own check only when that check can fail on its own.
- [x] Move the example plan from `skills/toby-build/references/examples.md` to `skills/toby-swd-plan/references/example.md`, and rewrite it as an `overview.md` and the first group file. Fold the migration and route steps into the step whose test fails without them. Add the end-to-end test for the slice. Write the flag step to the rules in `toby-swd-flags`.
- [x] Open `toby-swd-plan` from `toby-build` at stop 2. In the Plan Format section of `base/toby.md`, change the save path so a multi-session plan is a folder, `docs/plans/<feature-group>/<plan-name>/`, and replace the earlier pass's overview rule with the folder rule. Add that a feature plan ends with one test through the whole feature. Run `bash scripts/sync.sh`.
- [x] Replace the guide's line that let a behavior-keeping refactor be its own plan group. The refactor is now the first step of the slice that needs it, because a group whose only check is the existing tests cannot fail before the work. Run `bash scripts/sync.sh` again.
- [x] Add a yes to an entry skill's offer to the guide's list of requests that allow a plan. At stop 1 of strategic work, `toby-build` gives the plan's path and says that a yes means the plan gets written there.
- [x] Make stop 3 in `references/strategic.md` match the guide. The build stops at the end of each plan group. That stop asks for any decision the next group depends on.

- [x] Narrow the strategic list so a migration that only adds a table or a nullable column, an endpoint that reuses an existing ownership check, and the first control of its kind stay tactical. Open `toby-swd-flags` only for a release flag, kill switch, or experiment, and open `toby-swd-e2e` in tactical work only for a new entry point. A one-group plan's end-to-end test counts as its whole-feature test.

## Removed on purpose

- "The running order" and the method-skill list, because each step now says what it opens.
- "Each step says what proves it", because it produced checks that pass whatever the code does, such as a migration "proved" when the table lists its columns.
- The separate experiment step, because the description sends a throwaway to `toby-swd-experiment`, and that skill's Finish section moves the chosen behavior into the project. The body keeps the rule to open it for one question that reading the code cannot answer.
- "Re-read a file before editing it a second time", because it is a general habit for any edit and says nothing about building.
- "Commit a refactor separately, before the feature code", because the "Before the first edit" section of `toby-swd-campfire` takes the refactor-first rule, with its own commit, from `toby-swd-strategy`.
- The skip rule in the body, because the body is read only after the skill loads. The description holds the routing rule.
- The sizing table in `references/strategic.md`, because the sections below it and `references/criteria.md` state every row.
- "Build an item on that list only when a criterion whose Source quotes the user or the ticket requires it", because "Don't build" in `references/checks.md` opens with that rule.
- "Record whether you found one" at the second-reading step, because no later step reads that record.
- "A feature can match every word of a request and leave the problem unsolved" in `references/ambiguity.md`, because the sentence before it states the rule.
- "A person who can reach half-built behavior has found a defect" in `toby-swd-plan`, because the sentence before it states the rule.
- "This step serves criterion 1" after each step of the example plan. One line under the group heading says it once.
- "When that needs an approval-gated command, write out the command and ask for approval", because `toby-swd-environment` and the operating guide already require that ask. The body opens `toby-swd-environment` before any such command.
- The `toby-swd-modules` triggers "moves code" and "gives a module a new job", and the rule to fix its red flags before the plan. `toby-swd-architecture` now opens for a moved rule, entry point, write, or outbound call, and its "Default structure" says where each part goes.

## Verification

- Run `wc -w skills/toby-build/SKILL.md`. More than 1,300 words fails this group.
- List the backticked `toby-*` names in `skills/toby-build/SKILL.md` at HEAD and now. A name that is gone with no stated reason fails this group.
- Give an Opus subagent the new `toby-build` and ask it to quote, for each request below, the sentence that opens each skill. The check fails when a quote is missing or wrong.
  - "add a fifth status to the shipment tracker" must reach `toby-build` and `toby-swd-extensibility`.
  - "add a nightly job that uploads a CSV to S3" must open `toby-swd-twelve-factor` and `toby-swd-hardening`.
  - "add an optional `limit` argument to `list_orders`" must open neither of those skills.
- Give a second subagent `toby-swd-plan` and the guide's Plan Format, and ask it to quote any sentence that allows one long file, a group named for a layer, or a check that passes whatever the code does, for "add CSV export to the reports page, over three sessions". A quoted sentence that holds up fails this group.
- Run `bash scripts/sync.sh --check` and `python3 tests/test-voice-hook.py`. A failure in either fails this group.
- Run `python3 scripts/validate-skills.py`. An error in an owned file fails this group.
