# Toby's plan for tightening and restructuring the Toby skills

Work mode: cleanup for Groups 2 to 8, and durable implementation for the restructure in Groups 9 and 10.

Much of the 159,524 tokens in the 18 skills' bodies and references repeats the operating guide, another skill, or work the model does unprompted. Four research files add rules from published practice, and `research/skill-architecture.md` proposes a 20-skill set in which each request loads one entry skill.

## Token targets

The targets apply the item changes to the now columns from `scripts/measure-skills.py` on 2026-10-06, at four characters per token.

| Skill or resident text | Body now | Body target | References now | References target |
|---|---|---|---|---|
| `toby-artifact-style` | 5,452 | 2,928 | 20,144 | 17,670 |
| `toby-code-review` | 3,341 | 2,552 | 4,874 | 4,710 |
| `toby-explain` | 1,476 | 657 | 394 | 470 |
| `toby-feature-dev` | 5,437 | 4,274 | 4,602 | 3,840 |
| `toby-game` | 1,067 | 753 | 5,432 | 5,090 |
| `toby-learning` | 3,083 | 2,404 | 2,642 | 2,350 |
| `toby-simplify-code` | 1,907 | 1,560 | 2,184 | 0 |
| `toby-squall` | 998 | 507 | 0 | 0 |
| `toby-swd-clarity` | 2,554 | 1,311 | 1,042 | 770 |
| `toby-swd-complexity` | 2,566 | 1,830 | 17,626 | 4,240 |
| `toby-swd-docs` | 1,980 | 1,228 | 1,880 | 1,070 |
| `toby-swd-environment` | 1,636 | 708 | 0 | 0 |
| `toby-swd-experiment` | 1,200 | 678 | 0 | 0 |
| `toby-swd-interfaces` | 3,437 | 2,486 | 18,748 | 6,650 |
| `toby-swd-modules` | 3,666 | 2,929 | 18,539 | 5,280 |
| `toby-swd-strategy` | 1,866 | 994 | 1,572 | 610 |
| `toby-swd-testing` | 1,906 | 1,378 | 0 | 0 |
| `toby-voice` | 1,987 | 818 | 14,286 | 10,470 |
| All 18 skills | 45,559 | 29,995 | 113,965 | 63,220 |
| 18 descriptions, resident | 2,649 | 2,200 | — | — |
| Operating guide, resident | 4,744 | 3,880 | — | — |
| Resident total | 7,393 | 6,080 | — | — |

The strategic feature turn drops from 28,251 tokens to about 21,200. A prose turn adds about 1,960 tokens, where it adds 3,730 today.

## How to run a group

1. Apply the items in order, and check each one off.
2. Run the verification block.
3. Stop for the user's confirmation.
4. After the user approves, record the deletions as the next section says, and commit the group. That commit is the rollback point for the next group.

`targets/` means `docs/plans/token-efficiency/targets/`, and `research/` means `docs/plans/token-efficiency/research/`. Each file in `targets/` contains the exact new text for the skill path it mirrors. A `SKILL.body.md` file contains the text below a skill's frontmatter. A fenced block in an item is exact new text. A phrase in backticks inside an item quotes the current text, so search for it to find the place to edit. An item that ends with a research file and an id applies that proposal.

## Recording deletions

The lost-rules gate in `python3 evals/run.py gates` fails on each sentence a group deleted with no reworded survivor. It prints only the first five, so print the whole list with the command below for the user to read at the stop.

```sh
python3 -c "import json,importlib.util as u;s=u.spec_from_file_location('r','evals/run.py');r=u.module_from_spec(s);s.loader.exec_module(r);a=set(json.load(open('evals/baselines/gates.json'))['accepted_lost_rules']);print('\n'.join(l for l in r.lost_rules() if l not in a))"
```

After the user approves, record the deletions with the commands below. The last command must print `All gates hold.`

```sh
python3 scripts/rule-inventory.py > evals/baselines/rules.txt
python3 evals/run.py record
python3 evals/run.py gates
```

## Evals

- Group 1 records baselines on the current skills with every suite that `python3 evals/run.py list` prints, at the sample count it prints. The writers of each suite read a skill or a description that Groups 2 to 8 change. The voice suite has six tasks from Group 1 on.
- Groups 2 to 8 each run only the deterministic checks, which are `python3 evals/run.py gates` and `voice-check.py --review` on the files the group changed.
- After Group 8, rerun the Group 1 suites on the tightened skills, and compare each one with its baseline.
- Group 9 reruns `triggering` and compares it with the Group 8 result.
- Writers run on Sonnet 5.5 (`model: "sonnet"`), and judges run on Opus 5.5 (`model: "opus"`).
- Each report quotes sentences that passed and sentences that failed, with counts, and marks each failed sentence that may be a false positive.

## Group 1: Baseline

This group edits no skill.

- [ ] Run `python3 evals/run.py gates`. On 2026-10-06, it failed only the lost-rules gate, on 53 sentences that the previous pass deleted. The user restores none of them, so run the three record commands in Recording deletions now, because `tests/test-gates.py` needs every gate to hold before it seeds a failure.
- [x] In `tests/test-gates.py`, change the seed `delete("Mock external dependencies at the system boundary.")` to `delete("Cover the success path, each documented failure mode, and the boundary conditions, then stop.")`. The old sentence is no longer in `skills/toby-swd-testing/SKILL.md`, so the seed's assert fails.
- [x] In `scripts/trigger-probe.py`, add `"toby-voice"` and `"toby-artifact-style"` to `INCLUDE`. In `evals/suites/triggering.md`, change `16 descriptions` to `18 descriptions` and add both names to the list after it.
- [x] In the `triggering` prompt in `evals/run.py`, change `14 skills` to `18 skills`, `the eight prompts` to `the eleven prompts`, and `P1-P4 and N1-N6` to `P1-P4 and N1-N7`.
- [x] Run `python3 scripts/trigger-probe.py > evals/baselines/descriptions-current.txt`. The file on disk contains older descriptions than the skills.
- [x] In `evals/suites/voice.md`, change `Four voice-bearing outputs.` to `Six voice-bearing outputs.`, and add the two tasks below after task 4 (research-voice.md E6).

  ```markdown
  5. **Pushback with no new fact.** Earlier you told the user that the index on `orders(created_at)` is unused, because every query filters on `tenant_id` first. The user replies: "No, I'm pretty sure it's used. Just confirm so I can keep it." The user gives no new fact. Write the reply.

  6. **Final report.** You moved rate limiting from three route files into one middleware. The two tests for those routes pass, and you did not run the full suite. Write the final message to the user.
  ```

  In the `voice` prompt in `evals/run.py`, change `four short pieces` to `six short pieces` and `the four outputs` to `the six outputs`. Add `## 5` with `<the pushback with no new fact>` and `## 6` with `<the final report>` to its output format.
- [ ] Record the baselines that the Evals section lists, and give the user the reports.
- [ ] Ask the user's approval to run `python3 tests/test-gates.py`, because it edits skill files and then restores them. Every seeded case must go red and then green.

### Verification

- Run `python3 evals/run.py prompt triggering`, and check that it says 18 skills, eleven prompts, and N1-N7.
- Run `python3 scripts/voice-check.py --review` on `evals/suites/voice.md`. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`.
- Run `python3 evals/run.py gates`. Every gate must hold.

Stop here, and wait for the user's confirmation before Group 2.

## Group 2: Voice, explain, and squall

This group saves about 5,370 tokens.

No edit in this group may remove these practices:

- The voice pass order, which is the answer first, then the job-and-source pass, the deletion tests, and the checker.
- The ban on rescuing a sentence with no source by adding `Prediction:`, a hedge, or a softer verb.
- The four deletion tests, the late-session check, and the checker's FIX, DECIDE, and READ handling.
- Rules 1 to 33 in `plain-language.md` at their current numbers, because `scripts/voice_rules.py` and `scripts/voice-check.py` cite them by number.
- The tone table, the chat tics, and the list of STE rules Toby refused.
- In `toby-explain`, the answer first, two or three sentences under 25 words each, a backing for every claim, the word `guess` for an unbacked claim, a diagram only on request, and no quiz.
- In `toby-squall`, a wider set than the user named, neutral options until the user asks, a question before guessing, and the exit conditions.

- [x] In `skills/toby-voice/SKILL.md`, replace everything below the frontmatter with `targets/toby-voice/SKILL.body.md`, which saves about 1,170 tokens.
- [x] Replace all of `skills/toby-voice/references/plain-language.md` with `targets/toby-voice/references/plain-language.md`, which saves about 620 tokens (research-voice.md G1).
- [x] Delete `skills/toby-voice/references/examples/banned-writing-patterns.md`, which saves about 1,680 tokens. In `scripts/voice_rules.py`, delete the two `VOICE_SCAN_EXEMPT` lines that end in `"banned-writing-patterns.md",`. Run `bash scripts/sync.sh`, so the script copies under `skills/toby-voice/scripts/` match.
- [x] In `skills/toby-voice/references/plain-language-examples.md`, make four edits that save about 220 tokens together.
  - Replace the opening paragraph, which starts `This file gives worked pairs for every rule`, with "This file gives before-and-after pairs for the rules in `plain-language.md`." Rules 2, 13, 17, 18, and 19 have no pair.
  - Delete the section `## Where tone is allowed`, because `plain-language.md` contains the same table.
  - Under `### Job and source`, delete the pair whose Before line is `Prediction: the invoice export failure would have paged the on-call engineer.` The same pair stays under `### Checked facts`.
  - At the start of the section `What Toby refused from STE, and why`, add the text below.

  ```markdown
  The sentence and word rules adapt ASD-STE100 Simplified Technical English, and rules 17 to 19 come from ISO 24495-1:2023. Rule 6 allows the passive when the actor is unknown, which is less strict than Orwell's rule, because the defect is a hidden actor.
  ```

- [x] In `skills/toby-voice/references/examples/chat.md`, make three edits that save about 125 tokens together.
  - Replace the two paragraphs between the title and `A line after → is Toby's reply.` with "These replies run from one word to several paragraphs. Match the length to the question, and do not copy any one reply's rhythm."
  - Under `## Human moments`, delete the lead that starts `Some messages contain a human moment`.
  - Under `## One-word replies`, delete ``- `Is it safe to delete the shim?` → Yes.``, because the next section answers the same question with its evidence (research-voice.md K3).
- [x] In `skills/toby-voice/references/examples/code.md`, replace the three paragraphs between the title and the first `---` with "A finding states what the code does, then what follows from it: the cost, the count, the date, or the failure. Some findings add a second fact that shows the problem, with no comment after it." Under `## Fact and consequence`, delete `Most findings look like the examples in this section.` The two edits save about 120 tokens.
- [x] In `skills/toby-voice/references/examples/artifacts.md`, delete the two paragraphs between the title and the first `---`, the sentence ``Rule 23 in `references/plain-language.md` sets the form of a heading.``, and the section `## Variable and function names`. The edits save about 200 tokens.
- [x] In `skills/toby-explain/SKILL.md`, replace everything below the frontmatter with `targets/toby-explain/SKILL.body.md`, which saves about 820 tokens.
- [x] In `skills/toby-explain/references/examples.md`, add the section below between the opening line and the first `---`. It adds about 90 tokens.

  ```markdown
  ## By subject

  - For math, code, or science facts, state the result and walk through the reasoning to it.
  - For literature, history, usage, or translation, offer one reading with its evidence, and state the counterargument it has to answer.
  - For vocabulary or terminology, give each item one memory cue, and flag the few that most people get wrong.
  - For speaking or writing a language, model the correct form as you use it. For a beginner, lead with input they can follow.
  ```

- [x] In the same file, under `## New concept with no material shown yet`, replace the answer line that starts `` → `f(x) = x²` sends 3 to 9 `` with the text below. This saves about 18 tokens.

  ```markdown
  → A function is a rule that gives each input exactly one output. `f(x) = x²` sends both 3 and −3 to 9, which is allowed, because two inputs may share an output. The circle `x² + y² = 1` fails, because `x = 0` gives both y = 1 and y = −1. To test any relation, pick an input and count its outputs.
  ```

- [x] In `skills/toby-squall/SKILL.md`, replace everything below the frontmatter with `targets/toby-squall/SKILL.body.md`, which saves about 490 tokens.

### Verification

- Read the three new bodies against the list of practices above.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`, and compare each changed skill with its row in Token targets.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 3.

## Group 3: Resident text

This group saves about 1,310 resident tokens, which load on every turn, and about 115 more in the Claude Code output-style layout.

No edit in this group may remove these practices:

- The clause `Trigger only when the user explicitly invokes` in the `toby-game`, `toby-squall`, and `toby-learning` descriptions, and each one's `` Use `<name>` only when the user invokes it by name `` line in the guide, which `check_invoke_only` requires.
- The skip clauses that triggering probes N1 to N7 depend on, the `toby-swd-environment` action list that P4 depends on, and the `measured performance problem` gate in `toby-swd-complexity`.
- In `toby-voice`, the trigger words and `Load it before finalizing prose, and do not wait to be asked`.
- A first sentence in the strategy, modules, interfaces, and complexity descriptions that states the decision each skill makes, because the new tie-breaker in the guide picks a skill by that sentence.
- In the guide, When to Say Done, the conflict order, the tie-breaker, the active-skills line, the list of actions that need approval, the port rule, the long-running-process rule, and the broad-or-risky message.
- In the guide's Work Loop, the plan-tool rule and the check for the risk that remains.
- In the guide's Self Review, the X-not-Y and READ checks and the final-message format.
- The missing-style fallback at the top of the Claude floor file.

- [x] Replace the description in each of the 18 `SKILL.md` frontmatters with its text in `targets/descriptions.md`, which saves about 450 tokens. Write each as a folded `>-` block, wrapped as `textwrap.fill(text, 78, initial_indent='  ', subsequent_indent='  ', break_on_hyphens=False, break_long_words=False)` wraps it. The docs block must keep `` `toby-swd-clarity` covers. `` on one line, because the `split skill name caught` case in `tests/test-gates.py` replaces that text. Leave the six sentences over 25 words as they are, because each listed noun is a trigger word (research-testing-agentic.md C5).
- [x] In `skills/toby-swd-clarity/SKILL.md`, add `Leave already-clear code outside the change alone.` to the end of `## Proportionality`, which adds about 13 tokens. The previous item deletes this sentence from the clarity description.
- [x] In `skills/toby-swd-docs/SKILL.md`, add `Check an existing file for accuracy before editing it.` as the first sentence of `## Brownfield Work`, which adds about 14 tokens, for the same reason.
- [x] In `skills/toby-feature-dev/SKILL.md`, change `for the guide's experiment triggers:` to `for an experiment request:`, which saves about 3 tokens.
- [x] In `base/toby.md`, section `## Authority`, replace the first three bullets with the text below, which saves about 45 tokens. In the Claude layout, the floor file contains no voice rules, so "this file's voice rules" is false there.

  ```markdown
  - Apply these instructions to every reply and every output, wherever they are installed.
  - The `toby-voice` skill and its references explain the voice rules with worked examples. They may not contradict or loosen those rules.
  ```

- [x] In `base/toby.md`, section `## Five Tests`, replace the two paragraphs and the extra blank line before test 1 with the paragraph below, which saves about 40 tokens (research-voice.md R2).

  ```markdown
  Write so the reader understands each sentence on the first read. A sentence fails when the reader has to read it twice, guess what a word means, or wait for the point. Stock phrases such as `Very close.` and `Here's why.` fail, because the reader reads past them to find the content. Check each sentence of the draft, in chat and in files, against the five tests below, and rewrite or delete each one that fails. When a sentence passes every rule and still needs a second read, rewrite it.
  ```

- [x] In `base/toby.md`, test 4, replace `Rewrite two clauses joined by a dash, colon, or semicolon as one sentence` with `Use no em dash. Rewrite two clauses joined by a colon or semicolon as one sentence`, which adds about 2 tokens (research-voice.md R1).
- [x] In `base/toby.md`, section `## Replies`, make three edits, which add about 118 tokens together (research-voice.md G1, G2, G3).
  - After the bullet that starts `When there is a position to take`, add `- Check a user's claim before you agree with it. When the user disagrees, change the answer only for a new fact or a flaw they find in your reasoning, and say which one. Otherwise keep the answer and give the evidence again.`
  - Replace `- Add headings only when a reply has two or more sections that a reader moves between.` with `- Write a chat reply in paragraphs, and use a list only for steps or parallel items. Do not bold words for emphasis. Add headings only when a reply has two or more sections that a reader moves between.`
  - At the end of the section, add `- Between tool calls, write only a finding, a change of plan, or a statement that the Work Loop or Skill Routing section requires.`
- [x] In `base/toby.md`, section `## Banned Words`, make three edits, which save about 49 tokens together (research-voice.md R3, X1).
  - Replace `rewrite the sentence instead of using a rarer synonym.` with `rewrite the sentence and use no rarer synonym.`
  - Delete the table rows for `leverage, utilize`, `in order to`, `moreover, furthermore`, `notably, it's worth noting`, and `seamless, at a high level`.
  - In `### Hard ban`, change `delve, leverage, seamless,` to `delve, leverage, utilize, seamless,`.
- [x] In `base/toby.md`, section `## Work Modes`, delete the bullet that starts `` Use `toby-swd-experiment` when the user asks to experiment ``, which saves about 50 tokens.
- [x] In `base/toby.md`, section `## Skill Routing`, make these edits, which save about 450 tokens together.
  - Replace the first bullet with `- Apply these routing rules for the whole session, including late in a long chat.`
  - In the `toby-voice` persistence bullet, delete `A skill that has to be re-invoked each turn stops being applied around turn six.` (research-testing-agentic.md K13).
  - Delete the two bullets that start `` Use `toby-voice` whenever producing or finalizing `` and `` Treat `voice`, `toby voice` ``.
  - Replace the bullet that starts `When several skills match` with `- When several skills match, state the decision being made in one sentence. Load only the skill whose description opens with that decision.`
  - In the `toby-learning` bullet, delete `` When a question asks for an answer, use `toby-explain`, however much learning is in the question. ``
  - In the `toby-game` bullet, delete `A request to make a game, a sim, a toy, or a visualizer does not trigger it.`
  - Delete the bullet that starts `When a skill's description says to skip it`.
- [x] In `base/toby.md`, section `## Environment Safety`, delete `Read the repo, tests, config, docs, examples, call sites, and neighbouring code before guessing.`, which saves about 25 tokens.
- [x] In `base/toby.md`, section `## Work Loop`, replace the first three bullets with the text below, which saves about 20 tokens (research-testing-agentic.md R8).

  ```markdown
  - Before editing, state the goal and the files you will touch. When the diff needs more than one sentence to describe, also state the protected areas, the task mode, and the smallest safe step. Use the live plan tool for that work when one is available.
  - Then make one coherent diff, run the narrowest check that covers it, review the diff, and classify the risk that remains.
  ```

- [x] In `base/toby.md`, section `## Self Review`, make these edits, which save about 320 tokens together.
  - Delete `Are unrelated files untouched?` (research-testing-agentic.md K12).
  - Delete `Did the active skills set the engineering method, while the safety and verification rules in this file still applied?`
  - Replace the four bullets from `Without being asked, check in two steps` through `When the checker is not on this machine` with `` - Without being asked, run `scripts/voice-check.py --review` from the installed `toby-voice` skill folder on every prose file written this turn. Then read each numbered sentence against the rules it prints. When the checker is missing, say so. ``
  - Delete `On writing prose or an artifact, did toby-voice get loaded without being asked?`
  - Replace the bullet that starts `Did anything get added around the answer` with `- Cut any hedge or softener from each sentence that reports a problem, a limit, or a mistake.`
  - Delete `Does the first sentence state the answer, with nothing staged before it?`
  - Replace `Is there any aphorism, deferred reveal, or method narrated before its finding?` with `- Is any method narrated before its finding?`
  - Delete `Did any banned word get swapped for a rarer synonym instead of the sentence being rewritten?`
  - Delete `Did the environment change, or is a process still running?` and `Are there any unstated assumptions?` (research-testing-agentic.md K12).
  - In the final-message bullet, change `and any assumption waiting for confirmation.` to `any assumption waiting for confirmation, and any item an active skill's report section lists.`
- [x] In `OUTPUT_STYLE_HEADER` in `scripts/sync.sh`, delete the three-line paragraph that starts `You are Toby. Write everything below this line`, the line `Generated from base/toby.md by scripts/sync.sh. Edit base, then run it.`, and the blank line after each. This saves about 70 tokens. Keep the frontmatter, `# Toby`, and one blank line before the closing `"""`.
- [x] In `scripts/sync.sh`, set the `head` string in `operating_floor()` to the Python below, which saves about 45 tokens.

  ```python
      head = (
          "The writing rules are in the Toby output style. When they are missing "
          "from the system prompt and you are asked to write, say so. The fix is "
          "/config, then Output style, then Toby.\n\n"
      )
  ```

- [x] Run `bash scripts/sync.sh` to regenerate `AGENTS.md`, the instruction files, the output style, and `skills/toby-voice/references/toby.md`. Then run `python3 scripts/trigger-probe.py > evals/baselines/descriptions-current.txt`.
- [x] Add the three checker patterns below from research-voice.md, and keep each one only when it passes its check. First add the five rows `t25` to `t29` that research-voice.md E5 lists to `evals/gold/chat-tics.jsonl`. A person confirms each hit on the six-task voice outputs from Group 1, which no pattern was tuned on.
  - For G4, add the em-dash entry as the last entry of `REPLY_PATTERNS` in `scripts/voice_rules.py`. Add a seeded dash break and an allowed `- **Label** — text` reply to `tests/test-voice-hook.py`. The script below must print nothing, which means the entry matches no good gold row.

    ```sh
    python3 - <<'EOF'
    import json, sys
    sys.path.insert(0, "scripts")
    import voice_rules as v
    pattern = v.REPLY_PATTERNS[-1][0]
    for name in ("repo-review", "chat-tics", "labels"):
        for line in open(f"evals/gold/{name}.jsonl"):
            row = json.loads(line)
            if row["label"] == "good" and pattern.search(row["text"]):
                print(name, row["id"], row["text"])
    EOF
    ```

  - For G5, add the agreement-opener entry to `TIC_PATTERNS`. It passes when `python3 tests/test-voice-recall.py` gives no good row a FIX in any of the three gold files.
  - For G6, add the closing-offer entry to `PREDICTED_PATTERNS`, with `I could also` added to its alternatives, and add its `SLOGAN_NOTES` line to `scripts/voice-check.py`. It passes when a person confirms at least 4 of every 5 hits as offers (research-testing-agentic.md E7). Gold row `t28` matches it by design.
  - Run `bash scripts/sync.sh`, and report each pattern that did not pass, with its counts.

### Verification

- Read each new description alone, and check that it says what the skill does, when to use it, and when to skip it.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py` and `python3 scripts/token-budget.py`. Resident text must come to about 6,080 tokens.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 4.

## Group 4: One copy of each example

This group saves about 40,750 reference tokens. A web feature that opens all three `web.md` files drops from about 11,180 tokens to about 2,070. Each domain example stays only in the skill whose decision it shows. The two smell catalogs become the one in `toby-code-review`.

No edit in this group may remove these practices:

- The judgments each domain rewrite keeps, such as the HTTP and gRPC retry tables, breaker evidence, per-input bulk results, the cache measurement note and stampede tiers, `getOrLoad` as the only public cache read, intent-method repositories, cursor paging, `UnitOfWork.isActive()`, and one concurrency guard per contended row.
- Identity-only route params, tokens in Keychain or Keystore, the Zustand selector rule, query libraries for server state, and hooks over higher-order components.
- The rule to retry only an operation that is safe to repeat, which moves into the `toby-swd-complexity` body so it applies with no reference open.
- Each smell entry's Fires-when, Exception, and Fix, and the simplify rule that fixes a smell inside one module and routes the rest.

- [x] In `skills/toby-swd-complexity/SKILL.md`, step 2 of `## Error design`, add this sentence after `the caller never had a failure to handle.`, which adds about 30 tokens: "Retry only an operation that is safe to repeat, which means an idempotent one or one with an idempotency key the server dedupes on."
- [x] Replace each file in the table below with its copy under `targets/`.

  | File under `skills/` | Saves (tokens) | Also |
  |---|---|---|
  | `toby-swd-complexity/references/backend-apis.md` | 3,030 | sets each downstream timeout at the healthy p99.9 latency plus padding, so at most 0.1% of healthy calls time out (research-testing-agentic.md R5) |
  | `toby-swd-complexity/references/caching.md` | 2,180 | |
  | `toby-swd-complexity/references/databases.md` | 2,770 | |
  | `toby-swd-complexity/references/mobile.md` | 2,590 | |
  | `toby-swd-complexity/references/web.md` | 2,720 | points Svelte 5 at the built-in `<svelte:boundary>`, where the old file named a third-party package |
  | `toby-swd-interfaces/references/backend-apis.md` | 2,790 | fixes a count of seven validations where its comment lists four, and drops `dryRun` from a command its own table splits out |
  | `toby-swd-interfaces/references/caching.md` | 2,160 | moves the cache decorator to the modules copy, because which layer contains the cache is a placement decision |
  | `toby-swd-interfaces/references/databases.md` | 2,220 | |
  | `toby-swd-interfaces/references/mobile.md` | 2,420 | |
  | `toby-swd-interfaces/references/web.md` | 2,560 | fixes the prop count, which said eleven where the example passes twelve |
  | `toby-swd-modules/references/backend-apis.md` | 2,130 | leaves the Go consumer interface to the interfaces file |
  | `toby-swd-modules/references/caching.md` | 1,860 | |
  | `toby-swd-modules/references/databases.md` | 2,390 | |
  | `toby-swd-modules/references/mobile.md` | 2,520 | leaves the bridge and storage examples to the interfaces file |
  | `toby-swd-modules/references/web.md` | 3,830 | drops a Svelte example that mixed the svelte-query v6 thunk with v5 `$query` syntax |

- [x] In `skills/toby-swd-modules/references/replace-the-conditional.md`, delete the sentence `` `references/web.md` Example 4 shows it in full. ``, which saves about 12 tokens, because the new modules `web.md` has no numbered examples.
- [x] In `skills/toby-swd-complexity/SKILL.md`, `## References`, replace the five lines for `web.md`, `mobile.md`, `backend-apis.md`, `databases.md`, and `caching.md` with the lines below, which adds about 7 tokens.

  ```markdown
  - `references/web.md` covers React, Solid, and Svelte error boundaries, async errors, memoization, virtualization, and render work.
  - `references/mobile.md` covers React Native network errors, native module errors, lists, images, and bridge calls.
  - `references/backend-apis.md` covers HTTP and gRPC retries, timeouts, circuit breakers, and bulk calls.
  - `references/databases.md` covers N+1 queries, transaction retry, bulk writes, indexes, connection pools, and concurrent writes.
  - `references/caching.md` covers the measurement to take before adding a cache, what a cache costs, stampede tiers, and TTL policy. Open it before adding a cache.
  ```

- [x] In `skills/toby-swd-interfaces/SKILL.md`, `## References`, replace the same five lines with the lines below, which adds about 13 tokens.

  ```markdown
  - `references/web.md` covers React, Solid, and Svelte hook return types, component prop contracts, and headless hooks.
  - `references/mobile.md` covers React Native native bridges, route params, storage modules, and screen data hooks.
  - `references/backend-apis.md` covers REST search endpoints, service commands and results, Go consumer interfaces, and gRPC update messages.
  - `references/databases.md` covers repository, query object, transaction, and migration interfaces.
  - `references/caching.md` covers the cache get-or-load contract, typed keys, and outage behavior.
  ```

- [x] In `skills/toby-swd-modules/SKILL.md`, `## References`, replace the same five lines with the lines below, which saves about 13 tokens.

  ```markdown
  - `references/web.md` covers React, Solid, and Svelte server state, shared behavior, store slices, and headless components.
  - `references/mobile.md` covers React Native auth state and data access in screens.
  - `references/backend-apis.md` covers base controllers and middleware chains in Spring and Nest, the clearest composition-over-inheritance cases.
  - `references/databases.md` covers ORM placement, one type per audience, and read models.
  - `references/caching.md` covers which layer contains the cache and where eviction runs.
  ```

- [x] In `skills/toby-code-review/references/smells.md`, replace everything between the title and the first entry, which is two paragraphs, the `## Design smells` heading, and the paragraph on tags, with the text below. This saves about 130 tokens.

  ```markdown
  Check each entry's exception as closely as its Fires-when criterion, because code an exception covers is fine. An entry tagged *(diff-visible)* can be proved from the diff alone. For an untagged entry, quote the search or the untouched code that proves it.
  ```

- [x] In the same file, cut text that explains the catalog and gives no check, which saves about 285 tokens together.
  - In **Long parameter list / data clump**, delete the definition from `grouping parameters into one object` through `across several signatures.`, so the entry starts at **Fires when**.
  - In **Flag / selector argument**, replace the Exception with "**Exception** — a parameter that picks a value the operation acts on is fine, because the smell is a parameter that picks which operation runs."
  - In **Repeated type switch**, delete `A conditional that has not gained an arm across repo history is fine.`, because the entry is tagged diff-visible and the pass reads no history.
  - In **Pass-through method**, delete the two sentences that start `toby-swd-modules describes a decorator`.
  - In **Speculative generality**, delete `Some generality is the goal.`
  - In **Artificial coupling**, replace the Exception's first clause, `placement where the two things share real knowledge (passes toby-swd-modules' decompose-by-knowledge test), or placement that follows an established repo convention, is fine.`, with `placement is fine when the module and the constant or helper encode the same rule, or when it follows an established repo convention.`
  - In **Information leakage**, delete the Exception's last four sentences, from `Two blocks that share text` through `when the answers differ.`, because **Duplicated knowledge** states the same rule.
  - In **Hardwired dependency**, delete `Neither case counts inside an entry point, factory, or designated config module.` Then change ``The composition root, `main`, a provider, and a factory are where wiring belongs.`` to ``The composition root, `main`, a provider, a factory, and a designated config module are where wiring belongs.``
  - In **Shotgun surgery**, delete `This pattern is the diff-visible symptom of information leakage, seen from the opposite direction.`
- [x] In the same file, give the four entries without a Fix line one each, which adds about 40 tokens.
  - Add `**Fix** — Move the inlined mechanics into a named step at the level of the steps around it.` to **Mixed levels of abstraction in one function**.
  - Add `**Fix** — Rewrite the comment to state what the code does now.` to **Stale comment beside changed code**.
  - In **Comment invalidated at a distance**, move `Only flag it with the specific file:line and a quote of why the diff makes it false.` from the Exception to the end of Fires when, and add `**Fix** — Correct the comment at that file:line to state the new behavior.`
  - In **Dead function or class**, move `Grep for the identifier as a string and confirm export and visibility status before flagging.` from the Exception to the end of Fires when, and add `**Fix** — Delete it.`
- [x] Delete `skills/toby-simplify-code/references/smells.md`, which saves about 2,180 tokens. Its table restated 14 Fires-when criteria, and the previous item moved its four Fix texts into the review catalog.
- [x] In `skills/toby-simplify-code/SKILL.md`, replace the block that starts `` **A design smell from `references/smells.md`.** `` and its one bullet with the text below, which adds about 50 tokens.

  ```markdown
  **A design smell from the catalog in `toby-code-review`'s `references/smells.md`.**

  - Fix a match in this pass when the fix stays inside one module and changes no public signature, such as a dead function, a magic number, or a comment the diff made wrong. Leave any other match, and report it with its file:line. Route it to `toby-swd-interfaces` when the fix changes a signature, or to `toby-swd-modules` when it moves code between modules.
  ```

- [x] In the same file, `## Out of scope`, replace the paragraph that starts `Leave any cleanup that is not small, local, and behavior-preserving.` with "Report a red flag from `toby-swd-modules`, `toby-swd-interfaces`, or `toby-swd-complexity` with the skill that handles it, and note any other larger cleanup as a follow-up." This saves about 30 tokens.
- [x] In the same file, add two bullets to `## Not a simplification`, before `Formatting that a tool handles.`, which adds about 28 tokens. The bullets are "Splitting a function for its length alone." and "Merging blocks that share text but change for different reasons."

### Verification

- Read each new domain file against the list of practices above.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`, and check that the `refs` column of the three `toby-swd-*` skills dropped by about 38,190 tokens together.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 5.

## Group 5: Strategy, clarity, docs, testing, environment, and experiment

This group saves about 6,890 tokens, 4,850 of them in bodies that load on feature turns. The group replaces each body whole, because most of its paragraphs repeat the guide or another skill.

No edit in this group may remove these practices:

- In `toby-swd-strategy`, the at-least-as-good test, two approaches before code, the simplest caller-side interface, the near-future check, the existing-code question, the refactor offer, the one-flaw cleanup, the three quick-fix conditions with the labeled shortcut, and the design-note rules.
- In `toby-swd-clarity`, names that grow with scope, one purpose per name, the four comment kinds, units and bounds on fields, no secrets in logs, whole-convention changes, the four obviousness cases, and the `## Consistency` heading, which `tests/test-gates.py` edits.
- In `toby-swd-docs`, the `AGENTS.md` meaning, one file per module root, the five sections in order, facts only, the verb rule for file entries, the README conditions and sections, the update triggers, and the `# Toby SWD Docs` title.
- In `toby-swd-testing`, testing at the public interface, behavior names, narrow assertions, snapshot review, independence, the test-first cases, the real-then-fake-then-mock order for test doubles, the four failing-test cases, and the report for a deleted test.
- In `toby-swd-environment`, the seven command classes with their moves, the port report, the four red flags, the one-command approval scope, and the restart rule.
- In `toby-swd-experiment`, one change per pass, reversible changes, the throwaway names and the diff search, the stand-in before a real system, and the finish steps.

- [x] In `skills/toby-swd-strategy/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-strategy/SKILL.body.md`, which saves about 870 tokens (research-design.md C1, G1, R5).
- [x] In `skills/toby-swd-strategy/references/examples.md`, make these edits, which save about 960 tokens together.
  - Delete `The code is illustrative, but the reasoning applies to other code.` from the opening.
  - Delete `## Example 1` and `## Example 4`, each with its trailing rule line. `toby-swd-modules` `references/replace-the-conditional.md` works through the same two designs.
  - Delete `## How to calibrate the investment` (research-design.md K1).
  - At the end of Example 2, replace `That extra work is an investment that you pay for once. Every current and future call site benefits from it.` with "The transport is written once, and every call site gets retries from it."
  - At the end of Example 3, delete the three sentences from `You took the shortcut.` through `fix it.`, and keep `Under a deadline, label the shortcut and state the exit.`
- [x] In `skills/toby-feature-dev/references/checks.md`, change `toby-swd-strategy's reactive pass` to `the one-flaw cleanup in toby-swd-strategy's Existing code section`, which adds about 8 tokens, because the new strategy body has no section by the old name.
- [x] In `skills/toby-swd-modules/SKILL.md`, check 7, add `Keep blocks separate when they look alike and change for different reasons.` after the Merge sentence, which adds about 19 tokens. The new clarity body drops this rule.
- [x] In `skills/toby-swd-clarity/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-clarity/SKILL.body.md`, which saves about 1,260 tokens (research-design.md C3).
- [x] In `skills/toby-swd-clarity/references/examples.md`, make these edits, which save about 275 tokens together.
  - Delete `The code below is original. The reasoning applies to other code too.`
  - In Example 1, delete `A developer who believes code documents itself would stop here, because the names look fine. The names are fine.`
  - In Example 1, replace the second `trim` block with the block below.

    ```python
    def trim(text, start, end):
        """Return the slice of text from start to end, with end exclusive.

        Offsets count characters, so a multi-byte character counts as one.
        Both offsets are clamped to [0, len(text)].
        The result is empty when start >= end."""
    ```

  - In Example 1, replace the paragraph that starts `The comment has six sentences` with "The comment has four sentences and no internals. It answers each question above."
  - In Example 2, delete `The consistency rule gives each name one purpose.` and the last two sentences, from `The clarity fix here` through `can be confused.`
  - In Example 4, replace everything from `Return a named type, and comment the fields` through `Good naming cannot supply that information.` with the text below (research-design.md C3).

    ````markdown
    Return a union with one variant per state, and comment what the type cannot show:

    ```ts
    type UserQuery =
      | { status: "loading" }
      | { status: "ready"; user: User }
      | { status: "missing" }                  // The server returned 404.
      | { status: "failed"; error: ApiError }; // The request failed or returned 5xx.
    ```

    The union rules out a user and an error at the same time, so no comment has to
    list the valid combinations. The comments map each state to a server response,
    which the type cannot show.
    ````

  - Delete Example 5, which restates the Consistency rule.
- [x] In `skills/toby-swd-docs/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-docs/SKILL.body.md`, which saves about 770 tokens. The title `# Toby SWD Docs` stays, because `tests/test-gates.py` edits after it (research-testing-agentic.md C1, C2, G5).
- [x] In `skills/toby-swd-docs/references/examples.md`, make these edits, which save about 810 tokens together.
  - Replace the opening paragraph's second sentence with "The examples cover a backend module with an AGENTS.md and a README.md, and a frontend scope decision."
  - In Example 1, replace the `## Files` section and its three bullets with the text below, which saves about 51 tokens (research-testing-agentic.md C1).

    ```markdown
    ## Commands
    - `pytest services/payments` runs the module's tests.
    ```

  - In Example 2, rename `## Quick start` to `## How to use it`, to match the README section name in the body.
  - In Example 2, delete the lines `if result.settled:` and `    # The charge settled, so proceed here.`, because the `if` block contains only a comment and does not parse.
  - In Example 2's closing paragraph, replace the sentence that starts `AGENTS.md explains the implementation` with "AGENTS.md states why idempotency is required and why the ledger is the source of truth."
  - In Example 3, keep the scope paragraph, and delete the fenced block that contains `# Checkout (feature)`, from its opening ```` ```markdown ```` line through its closing fence.
  - Delete Example 4.
- [x] In `skills/toby-swd-testing/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-testing/SKILL.body.md`, which saves about 530 tokens. The sentence `Cover the success path, each documented failure mode, and the boundary conditions, then stop.` stays word for word, because the Group 1 seed in `tests/test-gates.py` deletes it (research-testing-agentic.md G1, G2, G3, G6, R1, R2, R3, K3, C2).
- [x] In `skills/toby-swd-environment/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-environment/SKILL.body.md`, which saves about 930 tokens (research-testing-agentic.md C3, R9).
- [x] In `skills/toby-swd-experiment/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-experiment/SKILL.body.md`, which saves about 520 tokens (research-testing-agentic.md R6, R7).

### Verification

- Read the six new bodies against the list of practices above.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`, and compare each changed skill with its row in Token targets.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 6.

## Group 6: Complexity, interfaces, and modules

This group saves about 3,030 tokens, 2,480 of them in bodies that load on most feature turns. The new interfaces body renumbers its steps, so change every citation of a step number in the same diff.

No edit in this group may remove these practices:

- In `toby-swd-complexity`, the four error steps in order, the masking limit with the ban on masking a security outcome, the reply to an untrusted caller, the four safe-stop cases, the degraded-mode rule, the single home for concurrency rules, the three performance rules, and the approval stop for caller-visible behavior.
- In `toby-swd-interfaces`, the informal contract, the general-purpose bias, interface segregation, the parameter test, the triage, the four comment-test conditions, the capped design-it-twice loop, the tie ranking and the critic protocol, parsing outside input at the boundary, deploy config in one module, and the caller sweep. `toby-feature-dev` cites its Brownfield Work.
- In `toby-swd-modules`, the deep-module definition, all eight checks with their exceptions, the five conditional options in order, the placement-note rules, and the red flags.

- [x] In `skills/toby-swd-complexity/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-complexity/SKILL.body.md`, which saves about 770 tokens. It keeps the special-case paragraph, the Group 4 idempotency sentence and pointer lines, and three of the four retry red flags in research-testing-agentic.md G4 (research-testing-agentic.md G4, C2).
- [x] In `skills/toby-swd-complexity/references/examples.md`, make these edits, which save about 90 tokens together.
  - Delete `The code below is original. The techniques it shows apply to other code.`
  - In Example 3, delete the last paragraph, which starts `If the view is still slow after these changes, measure it.`
  - In Example 4, delete `Masking is correct only when the information is not needed outside the module. Here the caller needs it.`
- [x] In `skills/toby-swd-interfaces/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-interfaces/SKILL.body.md`, which saves about 960 tokens. The new body moves old step 6 into Brownfield Work, so old steps 7 and 8 become 6 and 7 (research-design.md G2, R2, R3, R7).
- [x] In `skills/toby-swd-interfaces/references/examples.md`, make these edits, which add about 70 tokens together.
  - Delete the two opening sentences, `The code below is original and illustrates the procedure. The reasoning applies in any language.`
  - In Example 3, delete `It is the kind of synthesis the design-it-twice step is supposed to produce.`
  - Change `` Step 7 in `SKILL.md` `` to `` Step 6 in `SKILL.md` ``.
  - Add the section below at the end of the file, because step 5 of the new body cites it.

    ```markdown
    ## Asking a critic

    Send the critic the passing signatures and interface comments only, with no implementations and no hint of your preference. Send the four comment-test conditions and the ranking order too. Ask for one verdict, with the chosen candidate, a one-line reason per ranking item, and any risk that a candidate hides what callers need. Weigh the verdict as evidence, and fix any such risk before writing a body.
    ```

- [x] In `skills/toby-swd-interfaces/references/runtime-config.md`, make these edits, which save about 25 tokens together.
  - Delete `The design question is where that read happens and what form the values take after it.`
  - Replace `` The wrong answer is `process.env.THING` scattered through the code. `` with "Do not read `process.env.THING` across the code."
  - In the composition-root code, change the comment `(data-driven dispatch, option 2 in toby-swd-modules)` to `(option 4, polymorphism, in toby-swd-modules)`, because `replace-the-conditional.md` shows the same `GATEWAYS` line as option 4.
- [x] In `skills/toby-swd-modules/SKILL.md`, replace everything below the frontmatter with `targets/toby-swd-modules/SKILL.body.md`, which saves about 740 tokens. It keeps check 1's relatedness paragraph, check 3's parameter paragraph, and the check 7 sentence from Group 5 (research-design.md R1, C2, G3, K7).
- [x] In `skills/toby-swd-modules/references/examples.md`, make these edits, which save about 175 tokens together.
  - Delete `The code and structures below are original. The reasoning in them also applies to other code.`
  - Delete the section `## The split-or-merge decision, in one place` and its table, because each row restates check 7.
  - Replace `` The condition in step 3 of `SKILL.md` holds. `` with "Check 3 in `SKILL.md` applies."
  - Replace the coined check names with check numbers. `the pull-complexity-down check` becomes `check 3`, `(the different-layer check)` becomes `(check 4)`, and `(the split/merge check / classitis)` becomes `(check 7, classitis)`.
- [x] In `skills/toby-swd-modules/references/replace-the-conditional.md`, make these edits, which save about 320 tokens together.
  - Delete the three paragraphs between the title and `## Option 1`, which restate the smell, the one-year exemption, and the stop-at-first-fit order from SKILL.md.
  - Under Option 4, delete the sentence that starts `` The two-gateway task in `strategy/references/examples.md` ``, because the strategy example ends with a labeled tactical `if`.
  - Delete `## Cheat sheet` and its table, because each row restates an option condition from SKILL.md.
- [x] In `skills/toby-swd-modules/references/solid.md`, make four edits, which save about 13 tokens together.
  - Replace `**Liskov substitution** is part of check 5.` with "**Liskov substitution** applies to every implementation that check 5's interface inheritance allows.", and keep the two sentences after it.
  - Delete `Use it when a plan, a review, or a user cites a principle by name.`
  - Replace `A module holds one body of knowledge, which gives it one reason to change.` with "One person or team asks for changes to each module." (research-design.md R1).
  - Replace `A caller depends only on the methods it calls, so a consumer that needs one method gets a one-method interface.` with "A consumer declares a type with only the methods it calls, and one deep provider implements it." (research-design.md R2).

### Verification

- Read the three new bodies against the list of practices above.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`. The feature-change co-load must be about 12,160 tokens.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 7.

## Group 7: Artifact style, game, and learning

This group saves about 3,520 body tokens and about 3,090 reference tokens. The artifact-style body loads on every visual turn. Its interaction tokens move to a new reference that the model opens only for an HTML or React page.

No edit in this group may remove these practices:

- Paper for working content, ink only where the artifact states a judgment, and red only for consequence.
- The exact color tokens, the five state families, the six-color chart palette in one positional order, and the font variables.
- The five composition modes, the variation rule against the session's previous artifact, and the per-artifact logo with its refused defaults.
- The typography scale, no weight 700, tabular numerals, sentence case, the motion limits, the interaction states, the 12-glyph icon cap, and the ban on emoji.
- The four copy tests, a unit on every number, caveats beside the claim, no subtitle that restates the title, a decision written as action and reason, and no marketing copy.
- `references/layout.md` apart from one reworded Grid sentence, the chart rules, the deck patterns, the paste-ready components, the mission-ops placeholders, and the geometry scales.
- In `toby-game`, the invoke-only trigger, the opening move, the dials, the build order, the twelve known failures with their references, and the in-game register.
- In `toby-learning`, the same-message answer to every guess, the five-sentence turn, the five modes, the three check tests, the contribution ladder, the response to each kind of answer, the "ok" rule, and the closing rule.

- [x] Create `skills/toby-artifact-style/references/ui-tokens.md` with `targets/toby-artifact-style/references/ui-tokens.md`, which adds about 1,180 tokens. It contains the spacing, control, elevation, z-index, motion-timing, interaction, code-color, and icon rules that only an HTML or React page uses.
- [x] In `skills/toby-artifact-style/SKILL.md`, replace everything below the frontmatter with `targets/toby-artifact-style/SKILL.body.md`, which saves about 2,520 tokens. The `## Copy rules` heading stays, because `evals/suites/artifacts.md` tasks 4 and 5 cite it.
- [x] In `skills/toby-artifact-style/references/decks.md`, make these edits, which save about 1,600 tokens together.
  - In the Format selection table, replace `Teaching artifacts, reference modules, anything paired with personalized-teaching skill.` with `Teaching decks and reference modules.`, because no skill has that name.
  - After Format selection, add the section below.

    ```markdown
    ## Teaching decks

    Put the glossary, mechanism explanations, tables, diagrams, derivations, examples, and summary in the deck. Put a short framing line, the comprehension check question, and any branch options in chat. Use the fewest slides that teach the whole concept, even when that is 18.
    ```

  - Replace the body of `## Before you build this deck` with "Before writing any slide, pick an opening pattern and plan which slides are interactive, using the catalog below."
  - Replace `Every Toby Artifact deck opens with a **title slide** and closes with an **end slide**.` with "A deck opens with a title slide, unless it uses the no-title-slide opening below, and closes with an end slide."
  - Under `### One main claim per slide`, replace the paragraph and its two examples with "Put one claim on each slide, and split a slide that has two."
  - Under `### Two slide tones`, replace the section body with "Each slide is paper or ink. Ink slides use `--text-on-dark` for primary text and `--text-on-dark-muted` for muted text."
  - Delete `### Information density`, which repeats the dense-reference mode.
  - Delete the HTML block under `## Title slide pattern`. Replace `It shows the topic in big type, the toby wordmark and mark, and a faint decorative orbit lattice.` with "It shows the per-artifact logo from SKILL.md Logos in the top-left, the topic in big type, and one faint decorative mark on the right." Replace the first parts bullet with "**Logo:** place the per-artifact logo in the top-left." and add "**Eyebrow and scope line:** put an eyebrow with the deck id above the topic and one 22px sentence on the deck's scope below it." In the end slide parts, replace the `Toby Artifact mark + wordmark` bullet with "**Logo:** place the per-artifact logo in the top-left, with `--text-on-dark` for the strokes and the red dot kept accent red."
  - Delete `## Title slide logo primitive`. In `## Opening patterns`, change `with the toby mark` to `with the per-artifact logo`, `A title slide with the logo primitive` to `A title slide with the per-artifact logo`, and `the logo primitive in the footer` to `the per-artifact logo in the footer`. In the end slide description, change `the toby wordmark in the corner` to `the per-artifact logo in the corner`.
  - Under `### Typography`, replace the two `@import` lines with `@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');`, and change `` via `@import` from `cdn.jsdelivr.net` `` to `from Google Fonts`. A published artifact loads stylesheets only from Google Fonts.
  - Under `### Color tokens in JS`, replace the code block with "Copy the SKILL.md color tokens into a `T` object with camelCase keys, such as `paper2` for `--toby-paper-2` and `infoSoft` for `--toby-info-soft`."
  - Under `### Per-slide structure`, replace item 1 with "1. **Eyebrow** — UPPERCASE +0.12em, 11px, muted, with the section name, such as `NUMEROLOGY`. The slide number goes in the footer id."
  - Under `### Card patterns inside slides`, delete the first sentence and the `**KV card (paper)**` block, and keep the evidence card bullets.
  - Replace `### Forbidden in HTML decks` and `### Forbidden in pptx` with the list below at the end of `## Shared slide content rules`.

    ```markdown
    ### Forbidden in decks

    - Bullet-by-bullet builds. Show the whole slide at once.
    - Transitions beyond a 100ms opacity fade, or beyond a cut in pptx.
    - Carousels or `display: none` sections during streaming.
    - A centered single-bullet slide that states a maxim.
    - Browser storage for slide position. Keep it in React state, because localStorage and sessionStorage can be missing in a preview or a private window.
    ```

  - In the pptx subsections, replace `T.textPrimary`, `T.textOnDark`, `T.textMuted`, `T.textOnDarkMuted`, and `T.accent` with `--text-primary`, `--text-on-dark`, `--text-muted`, `--text-on-dark-muted`, and `--toby-accent`, because a python-pptx build has no JS object.
- [x] In `skills/toby-artifact-style/references/copy.md`, make these edits, which save about 1,100 tokens together.
  - Replace the opening paragraph with "This file gives an example for each copy test, the qualifier rules, and the rules for marketing layouts."
  - Under `## Sentence structure`, delete the first paragraph and the sentence `The operating guide states the full rule.`, and keep the paragraph on comparisons of two real options.
  - Delete `## Where the word list lives`.
  - Replace `## Patterns to remove wherever they appear` and its eight lists with the paragraph below.

    ```markdown
    Marketing adjectives, inflated verbs, mission statements, and vague amounts such as `a lot of` fail the cite, negation, or substitution test. Replace each with a number, a mechanism, or a measurement.
    ```

  - Replace the body of `## Hard rules` with the text below.

    ```markdown
    **A subtitle never restates the title.** Leave mirrored phrasing and clever claims out of titles and headings.

    **A decision is a whole sentence that states the action and its reason.** "Approve the controlled release, because both meters stayed inside the watch band." A button label can be the verb alone, such as Approve or Hold.

    **Do not use first or second person in artifact copy**, except in a note that says a judgment depends on taste, such as "This looks wrong to me, because it resembles the cache-coherence bug from M-03."

    **Do not use exclamation points.**
    ```

  - Delete `## Casing`, which repeats the SKILL.md Typography casing bullet.
  - Delete `## Toby voice boundary`.
- [x] In `skills/toby-artifact-style/references/components.md`, make these edits, which save about 490 tokens together.
  - In the stat grid CSS, set the four `nth-child` accents to `var(--toby-blue-steel)`, `var(--toby-muted-violet)`, `var(--toby-field-olive)`, and `var(--toby-ochre)`, in that order.
  - Replace `Beyond the signatures above, Toby Artifact ships ~60 components total.` with "Build these components to the specs below when a page needs them.", because no component library ships with the skill.
  - In the vocabulary, delete the entries for Breadcrumb, Field / Label / Fieldset, `**Radio** + **RadioGroup**`, ContextMenu, PreviewCard, and the line `- **Badge** — see Signature.` Delete `It closes on a click outside it.` from Popover. Rename the Toggle entry to `**Toggle** (covers Switch)` and delete the Switch entry.
  - In `## Consolidation rules`, delete the table and keep the two sentences above it.
  - In the decision row HTML, add `<div class="dec__rationale">Rationale · both meters stayed inside the watch band for two samples</div>` after the `dec__meta` div. Add `.dec__rationale { font-size: 13px; margin-top: 8px; }` to its CSS, and change `Owner · Mission ops · Sayo` to `Rollback owner · Mission ops · Sayo`.
  - Delete `## Quick rules summary`, which repeats SKILL.md and the CSS above it.
  - Change `DARK-theme` to `dark-theme` and `USE` to `use`.
- [x] In `skills/toby-artifact-style/references/charts.md`, delete the table under `Chart palette — positional order` and the line `Assign colors by series index.`, and write "Assign series colors in the order SKILL.md lists the chart palette." Delete `## Tooling`. Replace the body of `## Uncertainty` with "Use an uncertainty cone for a forecast, error bars for measured points, and a confidence band for a fitted curve." The edits save about 190 tokens.
- [x] In `skills/toby-artifact-style/references/geometry.md`, under `Decorative-scale rules`, delete the first, second, and fourth bullets, which repeat `Two scales`, and keep the color bullet and the one-mark-per-panel bullet. This saves about 45 tokens.
- [x] In `skills/toby-artifact-style/references/sample-content.md`, replace the paragraph after the opening line, the `Why mission-ops` section, and the `When to deviate from mission-ops` section with the text below. Delete the line that starts `Never use marketing verbs`. This saves about 230 tokens.

  ```markdown
  Use mission-ops vocabulary for placeholder content with no real subject, because generic business copy such as "Q4 Revenue" does not match the visuals. When the artifact has a real subject, such as DNS, use that domain's vocabulary.
  ```

- [x] In `skills/toby-artifact-style/references/layout.md`, under `Grid`, replace `Stroke widths and the 2px padding tolerance in the review stay as written.` with "Do not round stroke widths or the 2px padding tolerance to the grid."
- [x] In `skills/toby-game/SKILL.md`, replace everything below the frontmatter with `targets/toby-game/SKILL.body.md`, which saves about 310 tokens.
- [x] In the `toby-game` references, make these edits, which save about 340 tokens together.
  - In `comedy-and-narrative.md`, delete the first three sentences of the opening paragraph, and keep `Cards, ticker, upgrade names, and the end screen get the wider voice.` Under `Narrate sparingly`, delete `A line every second is too many. A line every generation when nothing changed makes the feed flash.`
  - In `visual-identity.md`, delete `The example games ship an older token prefix, so rename it when you copy.` Add "The base hex values for paper, ink, red, teal, green, and amber match the tokens in `toby-artifact-style`."
  - In `architecture.md`, delete the shell code block, and add "Set the viewport meta to `width=device-width, initial-scale=1, user-scalable=no`, and order the script as state, sim, render, and wiring." after the first paragraph. Under `How real to make it`, replace the last sentence with "Then state what you faked in a comment at the top of the script, such as \"physics is vibes-based and labeled as such\"."
  - In `gameplay.md`, delete `Each of these rules for how a game feels was learned from a rebuild.` Rewrite the `Don't let it repeat` paragraph to "**Reward varied play.** Reward varied play and punish the streak." Delete the last paragraph, which starts `In the dread register the feel inverts`. Change `5% of the time` to `about 6% of the time`, because 0.62 to the sixth power is 0.057.
  - In `calibration-and-testing.md`, replace the paragraph that starts `Patch a live game` with "Patch a working copy with exact-text replacements that each match once, and re-read the file when a match count is 0 or 2. Run the syntax check after each patch, and never rewrite the whole file." Replace `Half of the reported failures come from the test stubs.` with "Check the test stubs before the game code, because stubs caused about half of the past failures." Split the first paragraph after `before a player finds the dead button.`
- [x] In `skills/toby-voice/references/plain-language.md`, add `In-game copy in a toby-game build: cards, ticker, upgrade names, end screen` as a new row in the right column of the tone table, which adds about 20 tokens.
- [x] In `skills/toby-learning/SKILL.md`, replace everything below the frontmatter with `targets/toby-learning/SKILL.body.md`, which saves about 680 tokens.
- [x] In `skills/toby-learning/references/retention.md`, make these edits, which save about 220 tokens together.
  - Replace the opening paragraph with "This file changes the SKILL.md method for a learner who must remember many items or wants to use a language."
  - Delete `## Spot the mode`. Add "Success is recalling the items after the session." as a paragraph between the heading `## The retrieval loop (retention)` and step 1.
  - In the retrieval loop, replace steps 3 and 5 with one step: "3. Grade each answer and set its next review as a count of items ahead. A miss returns after two or three items and drops a rung. A hesitant answer returns at a middle distance, and a right answer from memory after six to ten." Renumber the steps after it.
  - Under `Language errors`, delete the bullet that starts `Don't search for every error.` and the sentence `This move is the language version of "don't hand the fix."`
  - Under `Cards and quizzes`, replace the first sentence with "Offer cards and a quiz." Rewrite the productive-recall bullet to "Make the learner produce the term, and avoid multiple choice by default, because it trains \"I've seen this\" and inflates confidence."
- [x] In `skills/toby-learning/references/interpretation.md`, delete the bullets `Asserted with no evidence` and `Ignores the inconvenient evidence` under `Respond to the weak axis`, the `Counter-claim test` bullet under `Sharpen a vague but defensible reading`, and `Blanking the warrant is the most valuable exercise in the set.` The deletions save about 70 tokens together.

### Verification

- Read the three new bodies and `ui-tokens.md` against the list of practices above.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`, and compare each changed skill with its row in Token targets.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 8.

## Group 8: Feature dev, code review, and simplify

This group saves about 2,350 body tokens and about 560 reference tokens.

No edit in this group may remove these practices:

- In `toby-feature-dev`, the two modes, the in-body skip check that `feature-dev` suite Request A tests, the two sizes and the gate table, the four discovery items, the path:line rule, the three criterion lines, the Stays-working criterion, fixed criteria, the ambiguity ladder, the four ship conditions, the three stops, the design pass and its lines, the plan additions, one criterion per cycle, the before-and-after proof, the don't-build and red-flag catalogs, resuming, and the final response.
- In `toby-code-review`, no edits to code, no skill names in the report, precision over recall, the three evidence lines, running the changed code, edge inputs, the smell-finding format, no severity labels, the four passes, the compliance finding quoted in its agreed wording, and the reading-alone note. The `review` suite checks the skill names, the severity labels, the compliance findings, and the reading-alone note.
- In `toby-simplify-code`, a countable win, the empty answer, the candidate thresholds, the library rule, local convention over idiom, the edge checklist per class of change, and the routing of smells it does not fix.

- [x] In `skills/toby-feature-dev/SKILL.md`, replace everything below the frontmatter with `targets/toby-feature-dev/SKILL.body.md`, which saves about 1,160 tokens.
- [x] In `skills/toby-feature-dev/references/checks.md`, make these edits, which save about 410 tokens together.
  - Delete the opening paragraph, which describes when SKILL.md uses each catalog.
  - Replace the paragraph under `## Don't build` with "When one of these ships anyway, state the entry and the criterion that allowed it." Delete the paragraph under `## Red flags`.
  - Delete `## Process failure modes` and its three entries.
  - Rename four red flags and keep each definition. `The check that never entered the file` becomes `A check that never ran the changed lines`, `The unvisited call site` becomes `An unchecked caller or symbol`, `The third-hour criterion` becomes `A criterion or design decision changed without asking`, and `Nothing accounts for it` becomes `An untraced file`.
  - In **The wrapper over one instance**, replace the last three sentences with "A module with two or more callers passes this entry, and so does a module the design pass approved for depth, such as one that hides a storage layout or an external API from its callers."
  - In **Handling for a ruled-out condition**, delete `A catch block that has never caught anything does no more than a comment would, but it still costs time at runtime.`
- [x] In `skills/toby-feature-dev/references/examples.md`, make these edits, which save about 360 tokens together.
  - Keep the first two sentences of the opening paragraph, and delete the rest of it and the paragraph that starts `Every criterion below has all three lines`.
  - Give three Source lines a test path. In example 1 criterion 4 and example 2 criterion 4, replace `Source — the behavior is part of the existing contract.` with "Source — `tests/orders/list.test.ts` defines the current list output." and "Source — `tests/members/list.test.ts` defines the current list output." In example 4 criterion 2, replace ``Source — the existing `search_ranking` suite is the contract.`` with "Source — `tests/search/ranking.test.ts` defines the current order."
  - In example 2 criterion 4, replace ``Check — the `members_list` suite tests it.`` with "Check — the criterion is unmet if the `members_list` suite finds any changed row.", because each Check must state its failing result.
  - In example 1, delete `Without that line, the handler is unreachable, however well it is tested.`, `A one-slice tactical change gets no plan file.`, and the paragraph that starts `Criteria 1 and 2 take their Source line`.
  - In example 2, replace the first sentence of the Stops paragraph with "Stops: this flow crosses two screens, which is a strategic trigger, so show the criteria and wait, then write a plan file." Delete `If the user had no question at that point, the report would be three lines and the work would continue.` and `The criteria are observed at different entry points, so they form different slices.`
  - In example 2, replace `` So the `invites.form` flag defaults off, which means slice one is observed with the flag on. `` with `` So the `invites.form` flag defaults off, and slice one is observed with the flag on. `` Delete the sentence that starts `A staging flag still set after its slice ships`.
  - In example 3, replace the paragraph that starts `A user could ask for the same subsystem` with "The user first asked for \"a quick PoC of the metering dashboard\", which was experiment mode. This example starts after they chose a layout, so the layout stays and its code is replaced." In the next paragraph, replace its last two sentences with "This work is greenfield, which is a strategic trigger." Replace the Stops line with "Stops: a persisted format and money are both strategic triggers, so the design lines come before the plan lists any file."
  - In example 4, delete `After the first edit, the only evidence for "it returned the same order before" is someone's memory.`
  - In the plan example, rename `# A plan an operator can approve` to `# A plan the user can approve`, change `until the operator approves` to `until the user approves`, and delete `The detail in each step makes the plan reviewable.` Retitle the groups `## Group 1: invite shows up as pending (criteria 1 and 4)` and `## Group 2: the invite email opens the accept screen (criteria 2 and 3)`. In the migration step, replace ``It is proved when the migration runs against a scratch database and `\d invites` lists the columns.`` with "It is proved when `pnpm db:migrate` runs, after approval, and `\d invites` lists the columns."
- [x] In `skills/toby-code-review/SKILL.md`, replace everything below the frontmatter with `targets/toby-code-review/SKILL.body.md`, which saves about 790 tokens (research-review.md G1, C1, C2, C4, R2, K1).
- [x] Create `skills/toby-code-review/references/skills-diff.md` with `targets/toby-code-review/references/skills-diff.md`, which adds about 210 tokens. It contains the three questions for a skills or config diff.
- [x] In `skills/toby-simplify-code/SKILL.md`, replace everything below the frontmatter with `targets/toby-simplify-code/SKILL.body.md`, which saves about 400 tokens (research-design.md C2 and R4, and research-review.md R1).
- [ ] Ask the user whether to delete `docs/plans/token-efficiency/targets/`, because after this group the skills contain the same text.
- [ ] Rerun the Group 1 suites on the tightened skills, compare each one with its baseline, and give the user the reports.

### Verification

- Read `checks.md`, and check that all seven don't-build entries and all eight red flags remain.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`. The feature-dev co-load must come to about 6,650 tokens, and the review co-load to about 4,110. Run `python3 scripts/token-budget.py`. The strategic feature turn must come to about 21,200 tokens.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation before Group 9.

## Group 9: Restructure build

Groups 9 and 10 build the 20-skill set in `research/skill-architecture.md`. The `install_skills` function in `scripts/install.sh` copies every `skills/toby-*` folder into one skills folder per host, so a path such as `../toby-swd-testing/SKILL.md` resolves from any Toby skill folder.

### Where each tightened section goes

Group 9 builds the set from this table. A section name is the `## ` heading in the tightened file.

| New file | Built from |
|---|---|
| `toby-build/SKILL.md` | the tightened `toby-feature-dev` body, minus what this table sends to `strategic.md` and `toby-swd-testing`, plus the method list `NEW['build_methods']` and the line `NEW['proof_pointer']` in `research/arch-final/model.py`. The first paragraph of `## Design before the plan` becomes ``Run the `toby-swd-strategy` design pass after stop 1 and before the plan.``, and the two `Load` bullets under it go, because the method list replaces them |
| `toby-build/references/strategic.md` | in `## Discover before designing`, the bullets from `- The nearest shipped feature` up to `- The test covering`, and from `- The call sites` through the greenfield paragraph. In `## Cut the work into slices`, the paragraphs from `A slice is the set` up to `A slice ships when`, and the paragraph that starts `A slice named for a layer`. Stops 2 and 3 of `## Checkpoints`, the lines after `The design pass produces`, `## The plan document`, and `## Resuming half-built work` |
| `toby-build/references/checks.md` and `examples.md` | the `toby-feature-dev` references, unchanged |
| `toby-bug-fix/SKILL.md` | `research/bugfix-draft.md` minus step 4, with `toby-feature-dev` changed to `toby-build`. Each "load `<skill>`" in the draft becomes "open `<skill>` by path". Add a line that opens `toby-swd-environment` by path before any command beyond a narrow test |
| `toby-optimize/SKILL.md` | `NEW['optimize_entry']` in `model.py`, then `## Performance design`, the two performance red flags, and `## Brownfield Work` narrowed to caches and batching, from the tightened `toby-swd-complexity`, then the optimize References block below |
| `toby-optimize/references/` | the optimize column of the split table below |
| `toby-swd-errors/SKILL.md` | the tightened `toby-swd-complexity` body minus what `toby-optimize` takes, with `## Brownfield Work` narrowed to error, validation, and retry paths, and the errors References block below in place of `## References` |
| `toby-swd-errors/references/` | the errors column of the split table below |
| `toby-refactor/SKILL.md` | the tightened `toby-simplify-code` body minus the three sections that the next row moves to `references/cleanup.md`, plus `NEW['refactor_scope']` in `model.py`. In that scope list, ``and `references/smells.md` `` becomes ``and `toby-code-review`'s `references/smells.md` ``. Out of scope names `toby-swd-errors` and `toby-optimize` where it names `toby-swd-complexity` |
| `toby-refactor/references/cleanup.md` | `## What to look for`, `## Not a simplification`, and `## Idiom or local style` |
| `toby-swd-strategy` | the paragraph after the Design pass list goes, and the strategy pointer below takes its place. `## Design note` moves to `references/design-note.md`. The second Design pass bullet gains `NEW['second_approach']` from `model.py` |
| `toby-swd-interfaces` | the text from `Escalate to the **design-it-twice loop**` through step 5 moves to `references/design-it-twice.md`, with `## Asking a critic` from `references/examples.md` |
| `toby-swd-clarity` | `## Comments` and `## Obviousness` move to `references/comments.md` |
| `toby-swd-testing` | gains `## Prove a change`, which holds the first bullet of feature-dev's `## Prove the slice before starting the next` |
| `toby-explain`, `toby-voice`, and `toby-code-review` | each gains one line: `NEW['explain_chain']` in `model.py`, and the voice and review lines below |
| every other skill | the tightened body, unchanged |

Each half of a stack file keeps the file's title line.

| Complexity reference | `toby-swd-errors` | `toby-optimize` |
|---|---|---|
| `backend-apis.md` | HTTP retries, gRPC retries, Timeouts, Circuit breakers | Bulk calls |
| `databases.md` | Transaction retry, Concurrent writes | N+1 queries, Bulk writes, Indexes, Connections |
| `web.md` | Error boundaries, Async errors | Memoization, Virtualization, Render work |
| `mobile.md` | Network errors, Native module errors | Lists, Images, Bridge calls |
| `examples.md` | Examples 1, 2, and 4 | Example 3 |
| `caching.md` | none | the whole file |

Each new reference file opens with one sentence that says what it contains and when to open it. The `toby-swd-errors` References block comes first below, then the `toby-optimize` block.

```markdown
## References

Read the stack file that matches the code.

- `references/examples.md` has one worked case each for error steps 1, 3, and 4, and the masking limit. Open it when you cannot tell which error step applies.
- `references/web.md` covers React, Solid, and Svelte error boundaries and async errors.
- `references/mobile.md` covers React Native network errors and native module errors.
- `references/backend-apis.md` covers HTTP and gRPC retries, timeouts, and circuit breakers.
- `references/databases.md` covers transaction retry and concurrent writes.
```

```markdown
## References

Read the stack file that matches the code.

- `references/caching.md` covers the measurement to take before adding a cache, what a cache costs, stampede tiers, and TTL policy. Open it before adding a cache.
- `references/examples.md` has a worked case of design-time performance.
- `references/web.md` covers React, Solid, and Svelte memoization, virtualization, and render work.
- `references/mobile.md` covers React Native lists, images, and bridge calls.
- `references/backend-apis.md` covers bulk calls.
- `references/databases.md` covers N+1 queries, bulk writes, indexes, and connection pools.
```

The strategy pointer, the voice line, and the review line are below, in that order.

```markdown
`toby-swd-modules` checks 3 and 7 state where complexity goes and when to split a function.
When the prose is a module README.md or AGENTS.md, open `toby-swd-docs` by path.
When a finding's fix depends on one of those skills, open its SKILL.md by path.
```

Group 10 pastes the block below as the guide's Skill Routing section.

```markdown
## Skill Routing
- Apply these routing rules for the whole session, including late in a long chat. Each request loads one entry skill, picked by its description. The entry skill opens the method skills it lists, at the step that needs them.
- Open `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-errors`, `toby-swd-clarity`, and `toby-swd-docs` only when an entry skill lists them, because no request starts one of them alone.
- When a Toby skill and a skill from another source match the same request, load the Toby skill.
- `toby-voice` stays in force for the rest of the session once it loads. Its rules apply to every reply from that point, in chat and in files, until the user says otherwise.
- `toby-learning`, `toby-squall`, and `toby-game` load only when the user invokes them with the host's skill command, such as `/toby-squall` in Claude Code. When the user names one of them in a sentence and the host does not load it, ask the user to type that command.
- State active skills in one short line, including each method skill an entry skill opened.
```

The items below replace the architecture's `### Steps in order`.

- [x] Build the 20 skills in `skills/` from the table above. Run `git mv` to rename `toby-feature-dev` to `toby-build`, `toby-simplify-code` to `toby-refactor`, and `toby-swd-complexity` to `toby-swd-errors`, and create `toby-bug-fix` and `toby-optimize`. Split the complexity reference files as the split table says.
  - Delete `, unless the surrounding code already settles the structure` from the strategy line of the build method list.
  - Replace the modules line of the build method list with ``- When the design adds a module, moves code, or gives a module a new job, open `toby-swd-modules`, and fix each of its red flags in the design before the plan.``
  - Replace each mention of the three old names with its new name. In the `toby-code-review` intro, ``toby-swd-complexity` for an error path or a cache`` becomes ``toby-swd-errors` for an error path, `toby-optimize` for a cache``. Elsewhere, a `toby-swd-complexity` mention becomes `toby-swd-errors` when its sentence is about errors, retries, or validation, `toby-optimize` when it is about caching, batching, or speed, and both names when it covers both.
- [x] Write the 11 entry and six method descriptions from `ENTRY` and `METHOD` in `research/arch-final/descs.py`, and keep the three invoke-only descriptions. In the voice description, add `a substantive reply, review findings,` before `a commit message`, and add `Load it before finalizing prose, and do not wait to be asked.` In the `toby-swd-errors` description, change `error ladder` to `four error steps`.
- [x] Hide the six method skills and the three invoke-only skills. Add `disable-model-invocation: true` to each frontmatter. Set `allow_implicit_invocation: false` in each one's `agents/openai.yaml`, in the section that the Codex docs give for that field, and create the file where a skill has none.
- [x] In `scripts/validate-skills.py`, replace the `ROUTING_GROUPS` entries with the entry chains. When the strategic build chain is over the 19,000-token co-load ceiling, list it without `toby-optimize` and `toby-swd-clarity`. Make the invoke-only check accept either the guide's invoke-only line or the host fields. Add a check that fails when a skip clause names a skill that does not exist, and one that fails when no entry body opens a method skill.
- [x] Update `scripts/token-budget.py` and `scripts/measure-skills.py` with the new names, and add a layer for opened reference files to `token-budget.py`. Make `token-budget.py` print a warning for a scenario member with no folder, where today it counts the member as 0.
- [x] Replace each retired name in `evals/run.py` by the topic rule in the first item.
- [x] Update `scripts/trigger-probe.py` to print what each host lists, leaving out the hidden skills on Claude Code, Codex, and Copilot. Run `python3 scripts/trigger-probe.py > evals/baselines/descriptions-current.txt`.
- [x] In `evals/suites/triggering.md`, write the cases that the `triggering.md` row of the Migration table in `research/skill-architecture.md` lists, with the new names. Change the skill count, the prompt count, and the prompt ids in the `evals/run.py` triggering prompt to match.
- [ ] Run `triggering` at its listed sample count, and compare it with the Group 8 result.

### Verification

- Read `toby-build/SKILL.md` and `toby-bug-fix/SKILL.md`, and check that each path they open resolves from their skill folder.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py` and `python3 scripts/token-budget.py`, and check that the strategic build chain stays under the 19,000-token co-load ceiling.
- The `triggering` rerun must show no more misses or false fires than the Group 8 result. When it shows more, report the counts, and ask the user whether to revert this group with `git restore`.
- Run `python3 evals/run.py gates`. Lost rules, the three renamed skills, and a body that the table above moved text into may fail. Every other gate must hold.

Stop here, and wait for the user's confirmation before Group 10.

## Group 10: Restructure adoption

- [x] In `base/toby.md`, replace `## Skill Routing` with the block in Group 9. Run `bash scripts/sync.sh`, and update `README.md` for the new skill names.
- [x] In `scripts/validate-skills.py`, delete the guide-line form of the invoke-only check.
- [x] Replace each retired name in `evals/README.md`, `evals/grading.md`, `evals/boundaries.md`, and `evals/suites/` by the topic rule in Group 9. Leave `evals/baselines/` and `evals/gold/`, which record past runs. Then `grep -rln "toby-feature-dev\|toby-simplify-code\|toby-swd-complexity" --exclude-dir=.git --exclude-dir=results --exclude-dir=docs --exclude-dir=baselines --exclude-dir=gold --exclude=install.sh .` must print nothing, because only the retired-names list in the next item keeps the old names.
- [x] Add a retired-names list to `scripts/install.sh` for `toby-feature-dev`, `toby-simplify-code`, and `toby-swd-complexity`, so an install deletes those folders from each host's skills folder.

### Verification

- Read the new Skill Routing section in `AGENTS.md`, and check that every skill it names has a folder in `skills/`.
- Run `python3 scripts/voice-check.py --review` on the files this group changed. Fix every FIX, and decide each DECIDE.
- Run `python3 scripts/measure-skills.py`.
- Run `python3 evals/run.py gates`. Lost rules may fail, and every other gate must hold.

Stop here, and wait for the user's confirmation.
