# Toby's plan for making the voice rules produce replies a person can follow

Work mode: durable implementation, with an eval loop before and after the rule changes.

Some voice rules and checks push agents into sentences that pass every check, and the user still cannot follow them. `evidence.md` in this folder quotes the real cases.

## Constraints

- Each current rule exists because Claude's default writing annoyed the user. A change may loosen a rule only where `evidence.md` shows the rule producing a sentence that is hard to read. Every change must keep failing the Claude defaults quoted at the top of `evidence.md`.
- The user picked four rule groups: the punctuation ban and the length cap, the forced connectors, the way the checks count, and internal labels in replies. The user also picked four places to change: the eval judge, the conflict order, the rubric and gold set, and the skill files. The contrast ban, the literal-verb rule, the banned-word list, the negated-actor rule, and the condition-first rule stay as they are.
- The user's past rulings stay, such as `lives in` failing as figurative and the status-change pair failing as choppy. When this work finds a ruling that conflicts with the evidence, the final report asks the user about it, and the ruling does not change.
- `hooks/voice-stop-check.py` and `hooks/voice-write-check.py` run from this checkout in every session the user has open, and `scripts/voice_rules.py` reads `base/toby.md` on every hook run. A broken edit to either file blocks those sessions right away, so `python3 tests/test-voice-hook.py` runs after every edit to them. `scripts/sync.sh` rewrites the repo's `AGENTS.md`, which sessions opened in this repo load.
- Installed copies under `~/.claude` stay untouched, because `scripts/install.sh` writes outside the repo and needs the user's approval. Every eval below reads from the repo.
- Nothing gets committed. Each group saves its diff to the scratchpad as `group-N.patch`, so a group can be reverted on its own.
- The user asked for the plan to be reviewed by a second agent, then run, with the most relevant evals rerun, and said they will check the result at the end. Each verification block still runs, and a group whose block fails gets reverted and reported.

## Group 1: Judges, test sets, and the before arm

The judges and decision rules get fixed and tested here, before any writer runs.

- [ ] Create a git worktree of `HEAD` in the scratchpad as the before arm. Before-arm writers read their rules from it.
- [ ] Add a `defaults-judge` prompt to `SUITES` in `evals/run.py`, and freeze it for the whole run. It reads no Toby rules. It fails only Claude's default habits: slogans and clipped runs, mirrored pairs, figurative verbs, `X, not Y` foils, hedges and sincerity words, deferred answers and setup sentences, stock openers such as "Great" or "Noted", closing offers, recaps and restated context, dashes, semicolons, and a colon before a reveal or a labelled answer.
- [ ] Add a `readability-judge` prompt to `SUITES`. It reads each output cold, with no task facts and no rules. First it writes what it understood from each output in plain words. Then it quotes every sentence it had to read twice or could not follow, and every sentence a colleague would not say out loud, each with a one-line reason. Last, it reads the task facts and marks each place where its understanding was wrong.
- [ ] Change `prompt()` in `evals/run.py` so a judge prompt can take a `{folder}` value, and give both judge prompts the folder of blinded files to read.
- [ ] Test both judges before either arm runs, each on its own shuffled file.
  - The defaults judge reads the user-flagged and user-ruled bad rows from `evals/gold/labels.jsonl` and `evals/gold/chat-tics.jsonl`, the defaults at the top of `evidence.md`, and the user-written good rows.
  - The readability judge reads the sentences the user said they could not follow, from `evidence.md`, and the same user-written good rows.
  - Leave out good row g08, because it is a labelled answer, and fix the stray capital in g02 only in the test file.
  - A judge passes when it fails at least 80 percent of its bad rows and passes at least 80 percent of the good rows.
  - Half of each set stays held out. A judge that misses gets one prompt revision and is retested on the held-out half. A judge that misses again gets reported and dropped.
- [ ] Add `evals/gold/readability.jsonl`. It holds one bad row for each rule-bent sentence in `evidence.md`, with its source and cause, and one good row per bad row with a plain rewrite. Mark the good rows `"strength": "proposed"`, because the user has not approved them. These rows measure the change and play no part in judge tests.
- [ ] Add rows to `evals/gold/chat-tics.jsonl` for "Noted.", "Got it.", and "Understood." as reply openers, with `"strength": "user-flagged"`.
- [ ] Add the suite `evals/suites/report.md` and a matching writer entry in `SUITES`. It has three chat tasks drawn from the user's complaints: a final report after a long change, a code review summary, and a reply to "what does that mean?". Each task gives facts that contain internal labels, file paths, and eval ids. This suite was written for this change, so the final report states that its results are weaker evidence than `holdout`.
- [ ] Run the before arm on Sonnet 5.5, with 12 writers each for `holdout` and `report`, 6 for `voice`, and 3 for `explain`. Save the outputs under `evals/results/readable/before/`.
- [ ] Run a no-rules arm on Sonnet 5.5, with 3 writers each for `holdout` and `report`. These writers get the task and no Toby files. The defaults judge should fail this arm at a much higher rate than the before arm. If it does not, the defaults judge gets reported as unable to see the defaults.
- [ ] Record the current checker on the gold sets with `python3 tests/test-voice-recall.py` on `labels.jsonl`, `chat-tics.jsonl`, `repo-review.jsonl`, and `readability.jsonl`. Save the counts to the scratchpad.

Verification:
- `python3 evals/run.py gates` prints `All gates hold.`
- Both judges pass their test, or the report says which one was dropped.
- The before folder holds 33 output files and the no-rules folder holds 6, each in its suite's format.

## Group 2: Guide and voice skill

Each item edits `base/toby.md` first, and `scripts/sync.sh` copies the change into the generated files.

- [ ] Add one item to the conflict order in Authority, between scope control and brevity: "a reader understands each sentence on the first read, in the fewest sentences that achieve it". Add that this item never permits a recap or restated context, and that the Job test still applies.
- [ ] Extend the Literal test's rule on terms. In a reply, explain in plain words or leave out each internal label the user has not used: an eval or row id, a rule number, a gate, check, or group name, and a mode name. When a standard term exists, use it, as with "borderline" and "unreachable code". File paths and code identifiers keep their current rules.
- [ ] Allow a colon in one case: after a whole sentence with no count in it, before a list of three or more items, whether the list is vertical or inline. Keep the dash ban, the semicolon ban, and the ban on a colon before a reveal or a labelled answer.
- [ ] Keep the length limit at 25 words or fewer, the same as the checker and the validator use today. Add how to meet it. Cut a clause, or split the sentence into two sentences that each state their own subject. A sentence may open with a bare `It` only when the sentence before it holds one noun that `It` could mean. Rule 9 stays, so `This` and `That` still take a noun. Write three or more parallel items as a list.
- [ ] Change the connector rule. A connector states the true relation between two clauses. Use `because` only for a cause, and `so` only for a result. Two facts about one process may be joined with `and`. A sentence holds at most one `which` clause, and no clause gets joined after it.
- [ ] Mirror these changes in `skills/toby-voice/references/plain-language.md`, in rules 1, 7, 9, 10, 14, and 24, and in the READ list that `scripts/voice-check.py` prints. Change READ rule 10, which says to split two facts joined by `and`, so it says to check that the relation is clear.
- [ ] Change `skills/toby-explain/SKILL.md:17`, which says to join clauses with "because, so, or which", to match the connector rule.
- [ ] Remove "cite the rule by its number" from `skills/toby-voice/SKILL.md`, because rule numbers are internal labels.
- [ ] Run `scripts/sync.sh`, then `scripts/sync.sh --check`, then `python3 tests/test-voice-hook.py`.

Verification:
- `python3 evals/run.py gates` holds. Each lost rule it reports gets read against the new wording and listed in `evals/results/readable/report.md`.
- `python3 scripts/validate-skills.py` passes with no new warning class.
- Every prose file changed in this group passes `scripts/voice-check.py --review`, and each sentence gets read against the READ list.

## Group 3: Checker, validator, hooks, and rubric

Each check change gets a fixture on each side in `tests/test-validator-checks.py` or `tests/test-voice-hook.py` before it is recorded.

- [ ] Change the advice text that tells writers to split a long sentence, in `hooks/voice-stop-check.py` and in the over-length note in `scripts/voice-check.py`. The new text says to cut a clause, or to split into two sentences that each state their own subject.
- [ ] Change the advice in the clipped-run finding in `scripts/voice-check.py`, which says to join with "which", so it matches the connector rule.
- [ ] Keep the "two facts joined by and" pattern, because it catches the user-flagged rows b06 and r07. Change its advice so it asks whether the relation between the two facts is clear.
- [ ] Exempt list items from "mirrored bullets" when the first word is "If" or "When", so a list of cases passes.
- [ ] Add "talk" and other common imperatives that the buried-lead check in `scripts/validate-skills.py` misses to its `IMPERATIVES` list.
- [ ] Check whether `scripts/voice-check.py` and `hooks/voice-write-check.py` count a table or a list as one sentence. Fix any that do.
- [ ] Add a pattern to `TIC_PATTERNS` for "Noted", "Got it", and "Understood" as reply openers. The stop hook reads `TIC_PATTERNS`, so the pattern blocks live replies that open this way. Add fixtures that must pass, such as "Got it working", a quoted "Understood.", and "Understood how the cache fails". Run it over every file in `evals/baselines/runs/` and `evals/results/`, and read each new hit.
- [ ] Change rubric category 8, Tangled, in `evals/rubric/pass-fail.md`, so two facts about one process joined by `and` pass. Change category 1, which recommends "which, so, or then", to match the connector rule. Change "under about 25 words" to "25 words or fewer". Add three fail categories:
  - a false link, where `because` or `so` joins clauses that are not cause and result
  - a vague back-reference, where `It`, `This`, or `That` has more than one possible target
  - an internal label that the reader was never told
- [ ] Rerun `tests/test-voice-recall.py` on all four gold files.
- [ ] Before each `python3 evals/run.py record`, save `evals/baselines/gates.json`. After it, diff the two and list every changed key in `report.md`.

Verification:
- On `labels.jsonl`, `chat-tics.jsonl`, and `repo-review.jsonl`, the count of bad rows with a FIX or DECIDE finding does not drop from the Group 1 count.
- No good row gets a FIX finding.
- `python3 tests/test-voice-hook.py`, `python3 tests/test-validator-checks.py`, and `python3 tests/test-gates.py` pass.
- `python3 evals/run.py gates` holds.

## Group 4: After-arm eval

- [ ] Run the after arm with the same writers, suites, sample counts, and model as the before arm. Save the outputs under `evals/results/readable/after/`.
- [ ] Copy the before, after, and no-rules files into `evals/results/readable/blind/` under random names. Keep the key in the scratchpad, where the judges do not read.
- [ ] Run the readability judge and the defaults judge on Opus 5.5, over chunks of at most 10 blinded files. Run each judge twice on `holdout` and `report`, with a different shuffle each time, and once on `voice` and `explain`. Report how often the two passes agree on a sentence.
- [ ] Run `scripts/score-voice.py` and `scripts/voice-check.py` on every file. Count dashes, semicolons, foils, banned words, and slogan DECIDE findings per file.
- [ ] Count words per output in each arm.
- [ ] Write `evals/results/readable/report.md`. For each suite and judge, give fails per file, per 100 words, and per 100 sentences for each arm, with the mean, the range, and a 90 percent bootstrap interval for the difference between arms. Quote ten failed and ten passed sentences per arm, and flag likely false positives.

Decision rules, fixed now:
- The readability result counts as better on a suite only when all three rates drop and the bootstrap interval for fails per file excludes zero. Otherwise the report says the eval showed no difference on that suite.
- Any rise in the after arm's mechanical counts of Claude defaults gets quoted in the report, sentence by sentence.
- The defaults judge result counts as a regression when its fails-per-file interval excludes zero, or when the after arm's quoted fails show a type of default that no before-arm file has.
- A rise above 10 percent in average words per output on any suite counts as a regression.
- A regression gets its cause found from the quoted sentences, and the change behind it gets reverted. The affected suite runs once more, and the report states the result of that one rerun.
- The user reads the report and the diff, and decides what stays.

## Group 5: Skill file read, after the eval

This group runs after Group 4, so its edits stay out of the measured change.

- [ ] Run the readability judge on `base/toby.md`, `skills/toby-voice/SKILL.md`, `skills/toby-explain/SKILL.md`, `skills/toby-code-review/SKILL.md`, and `skills/toby-plain/SKILL.md`.
- [ ] Rewrite only the sentences the judge flags, and keep every rule they state. Save the result as `group-5.patch` without applying it, so the user can review it and the tree keeps only measured changes.

Verification:
- The lost-rules gate reports no sentence that lacks a reworded survivor.
- `scripts/voice-check.py --review` passes on every changed file.

## Final message

The final message stays short and translates every id into plain words. It covers what changed and whether the eval showed better readability or a regression. It also covers anything that failed or did not run, and the user rulings this work questions. The detail goes in `evals/results/readable/report.md`.
