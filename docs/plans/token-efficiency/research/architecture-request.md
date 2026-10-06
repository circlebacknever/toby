# Skill set by request kind

This proposal replaces the 18 Toby skills with 16 skills, so that each user request loads one of them. That one skill is the entry skill for the request. It opens reference files for the method it needs. When it hands work to another skill, it names that skill, which this document calls a chain.

The set has 13 skills the model can load on its own and 3 that load only when the user invokes them. Four skills are new: `toby-fix-bug`, `toby-refactor`, `toby-design`, and `toby-optimize`. Four skills lose the `swd-` prefix, because each now covers a request kind of its own. Six skills retire, so their text moves into reference files: `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-complexity`, `toby-swd-clarity`, and `toby-simplify-code`.

Resident cost falls from 7,393 to about 6,513 tokens. The largest modelled scenario falls from 20,858 to about 20,430 loaded tokens. One scenario costs more, because a request to add a repository method now loads the `toby-feature-dev` workflow. Every new body size below is an estimate, because no new text has been written.

## How the set is cut

Each skill covers one kind of request, stated in the words a user types. I sorted the requests with these four questions.

1. Does the user want code changed, or an answer? Answers go to `toby-explain`, `toby-design`, or `toby-code-review`.
2. If code changes, does its behavior change? Same behavior goes to `toby-refactor`. New behavior goes to `toby-feature-dev`, and broken behavior goes to `toby-fix-bug`.
3. Is the work throwaway? Throwaway work goes to `toby-experiment`, whatever else the request names.
4. Is the request about tests, docs, commands, speed, prose, or a visual? Each of those six has one skill.

The six retired skills held method with no request kind of their own. None of the 11 prompts in `triggering.md` asks for interfaces or strategy by name. In the current set those skills loaded beside the skill the request was about. The recorded runs show them loading where nobody asked for them. Strategy fired on P1 in 4 of 5 runs, and interfaces fired on P3 in two runs.

## Skill list

Each entry gives the draft description, the contents of the body, and a table of the reference files. A path written as `toby-design: references/modules.md` is a file in another skill's folder. `toby-learning` already uses that form to point at `toby-voice: references/plain-language.md`, as does `toby-explain`.

Every entry skill except the three invoke-only skills ends its final-response section with one line that loads `toby-voice` before prose is sent. That line states the voice chain inside the entry skill, as well as in the operating guide.

### toby-feature-dev

> Gives the steps to build new behavior in slices the user can review, with acceptance criteria and a before-and-after check for each one. Use when the user asks to build, add, implement, wire up, or finish something the code does not do yet. That covers a feature, ticket, endpoint, screen, job, flag, or method. Skip a one-file edit that copies a pattern already in that file. Skip broken behavior (toby-fix-bug), same-behavior changes (toby-refactor), and throwaway work (toby-experiment).

The body keeps every section that applies at both sizes, from the mode pick to the final response. Slicing beyond one slice, stops 2 and 3, and the plan document move to `references/strategic.md`. The body shrinks from 5,437 to about 4,440 tokens.

| Reference | When the body opens it |
|---|---|
| `references/strategic.md` | The sizing step picks strategic. |
| `references/checks.md` | Before the plan's out-of-scope line, and before the handoff. |
| `references/examples.md` | Greenfield work, or a slice cut the body does not settle. |
| `toby-design: references/strategy.md` | Strategic size, or a tactical change that adds a special case, a flag, or a hidden dependency. |
| `toby-design: references/modules.md` | The design adds a module or gives one a new job. |
| `toby-design: references/interfaces.md` | The design adds or changes a signature. |
| `toby-design: references/errors.md` | The change adds or alters an error path, a retry, or validation. |
| `toby-design: references/performance.md` | The path has a stated budget, or the change adds a cache. |
| `toby-write-tests: references/testing.md` | Every slice, before its first test. |
| `toby-docs: references/module-docs.md` | The change makes an AGENTS.md or a README wrong. |
| `toby-environment: references/commands.md` | Before any command beyond inspection or a narrow test. |

It hands the work to `toby-experiment` when the user says throwaway or when one value needs a trial.

### toby-fix-bug (new)

> Gives the steps to fix broken behavior: reproduce it in a failing test, fix the cause, and keep the test as a regression test. Use when the user reports a bug, error, crash, wrong result, regression, flaky test, or failing build and wants it working. Use it also when the user only pastes an error or a stack trace. Skip a question about why it fails with no fix wanted (toby-explain), slow code (toby-optimize), and throwaway trials (toby-experiment).

The body holds about 1,420 tokens of new text built from current rules.

1. Reproduce the failure first, and state the input that causes it.
2. Find the cause at a path and line. Quote the guard that should have stopped it, as the Guard line in `toby-code-review` does.
3. Classify a failing test with the four classes in `testing.md` before editing it.
4. Fix the cause with no special case for one input, which comes from the After writing section of strategy.
5. Prove the fix with the before-and-after form from `toby-feature-dev`.

Its red flags are a fix with no regression test and an assertion edited to go green. Two more are a special case for one input and a caught error that hides the symptom.

| Reference | When the body opens it |
|---|---|
| `toby-write-tests: references/testing.md` | Always, for the regression test and the failing-test classes. |
| `toby-design: references/errors.md` | The fix touches error handling, retries, or validation. |
| `toby-design: references/strategy.md` | The fix needs a design change, or the quick fix adds a special case. |
| `toby-design: references/interfaces.md` | The fix changes a signature, so the callers need a sweep. |
| `toby-environment: references/commands.md` | Before any command beyond a narrow test. |

It hands the work to `toby-feature-dev` when the repair is new behavior, and to `toby-optimize` when the cause is speed.

### toby-refactor (new)

This skill replaces `toby-simplify-code` and takes over the rename and comment requests that loaded `toby-swd-clarity`.

> Covers changes to the structure or wording of working code that keep its behavior the same. That includes names, comments, docstrings, simpler logic, less duplication, and split, moved, or merged files and modules. Use when the user asks to refactor, simplify, tidy, "clean up", rename, comment, de-duplicate, split, extract, or move code. Skip a request for findings with no edit (toby-code-review) and any change to what the code does (toby-feature-dev or toby-fix-bug).

The body holds about 1,330 tokens. It keeps the Disposition, Behavior drift, Process, and Final response sections of `toby-simplify-code`. It adds a scope table and a scope rule, which says to stay at the scope the user asked for. The edit for a simplify or tidy request stays inside the changed code, while a split, move, or extract request may change module boundaries. The tests must pass before and after with no edit to them. A bug found on the way gets reported and left alone. The refactor goes in its own commit.

| Reference | When the body opens it |
|---|---|
| `references/naming.md` | The request renames anything. |
| `references/comments.md` | The request adds or fixes comments or docstrings, or unclear control flow. |
| `references/simplify.md` | The request simplifies, tidies, or de-duplicates code inside its current files. |
| `references/simplify-smells.md` | `simplify.md` sends the pass there for a design smell. |
| `references/clarity-examples.md` | A naming or comment case needs a worked example. |
| `toby-design: references/strategy.md` and `references/modules.md` | The request splits, moves, merges, or extracts code. |
| `toby-design: references/interfaces.md` | A signature or an export changes, so the callers need a sweep. |
| `toby-design: references/errors.md` | The request simplifies error handling. |
| `toby-write-tests: references/testing.md` | Coverage of the touched path is thin, so a characterization test comes first. |
| `toby-docs: references/module-docs.md` | A structural change leaves an AGENTS.md or a README wrong. |

### toby-write-tests (renamed from toby-swd-testing)

> Covers writing and improving tests for behavior that already works. That includes new tests, more coverage, a regression test for an earlier fix, rewritten brittle tests, and snapshot updates read line by line. Use when the request is about tests and nothing is broken. Skip a failing or flaky test (toby-fix-bug) and a request only to run the suite (toby-environment).

The body holds about 450 tokens. It says to read the existing tests for the behavior first and then open `testing.md`. A snapshot update runs only after every line of its diff has been read. Its report names each test by behavior, quotes the run, and lists any test deleted or weakened. The current body moves unchanged to `references/testing.md`, because `toby-feature-dev`, `toby-fix-bug`, `toby-refactor`, `toby-code-review`, and `toby-experiment` open it too.

| Reference | When the body opens it |
|---|---|
| `references/testing.md` | Always. |
| `toby-environment: references/commands.md` | A snapshot update, or a run wider than one test file. |

### toby-optimize (new)

> Gives the steps to make working code faster or smaller, from a measured baseline with one change per measurement. Use when the user asks to optimize, speed up, or cut latency or memory, or to fix a slow page or query. Use it also for a cache added for speed. Skip a question about why something is slow with no change wanted (toby-explain), wrong output (toby-fix-bug), and a throwaway sweep (toby-experiment).

The body holds about 1,000 tokens of procedure drawn from the performance rules in `toby-swd-complexity`. The steps are to record a baseline, look for a cache or a better algorithm before code-level tuning, and change one thing. Then the code is measured again, and a change with no measured effect is reverted unless it also simplified the code. A path with a stated budget gets measured at its worst case under load. The report gives the baseline, the result, the command, and what stays unmeasured, such as production load.

| Reference | When the body opens it |
|---|---|
| `toby-design: references/performance.md` | Always. |
| `toby-design: references/complexity/<stack>.md` | The stack file that matches the code. |
| `toby-design: references/interfaces.md` and `references/interfaces/caching.md` | The change adds a cache, so its get-or-load contract needs a design. |
| `toby-environment: references/commands.md` | A benchmark, a profiler, or a heavy suite. |

### toby-design (new)

> Covers design advice given before code is written: where new code goes, what a function or API exposes, whether to split or merge a module, and which approach to take. It also covers whether an error path, retry, or cache is worth its cost. Use when the user asks how to structure, organize, design, or architect something, or asks for a design note. Skip a request to build it (toby-feature-dev), options tried by running them (toby-experiment), and how existing code works (toby-explain).

The body holds about 900 tokens. It says to put the recommendation and its main reason in the first sentence. A table maps each decision to the reference file that covers it. The body also merges "Writing a design note" from strategy with "Writing a placement note" from modules. Every design reference file is in this folder, so other skills point here.

| Reference | When the body opens it |
|---|---|
| `references/strategy.md`, `references/strategy-examples.md` | The question is whether the design changes, or which approach to take. |
| `references/modules.md`, `references/modules/<stack>.md` | The question is where code goes, or whether to split or merge. |
| `references/replace-the-conditional.md` | A conditional gains a branch per domain case. |
| `references/solid.md` | The user asks about a SOLID principle. |
| `references/interfaces.md`, `references/interfaces/<stack>.md` | The question is what a signature, endpoint, or contract exposes. |
| `references/interfaces/runtime-config.md` | The question is where deploy-varying config enters. |
| `references/errors.md` | The question is whether an error path, retry, or validation is worth its cost. |
| `references/performance.md`, `references/complexity/<stack>.md` | The question is whether a cache or an optimization is worth its cost. |

### toby-code-review (kept)

> Covers a review that reports proven risks in a change and leaves the code unedited: bugs, regressions, security holes, missing tests, design smells, and repo-rule breaks. Use when the user asks to review, check, or audit a diff, PR, commit, branch, or working tree. Skip any request to change the code, which toby-refactor or toby-fix-bug covers.

The body stays at about 3,360 tokens. The paragraph that cites five swd skills for contract, placement, error, coverage, and naming questions now cites reference files.

| Reference | When the body opens it |
|---|---|
| `references/smells.md` | The design pass. |
| `toby-design: references/modules.md`, `interfaces.md`, `errors.md`, `strategy.md` | A design finding needs its fix stated. |
| `toby-write-tests: references/testing.md` | A coverage finding. |
| `toby-refactor: references/naming.md` or `comments.md` | A name or comment finding. |
| `toby-environment: references/commands.md` | Before any run beyond narrow verification. |

### toby-explain (kept)

> Covers answering a question in plain words and stopping, with a file and line or a source behind each claim. Use when the user asks why or how something works, where it happens, or what the difference is. Use it also for a walkthrough or a clear, short explanation of code or any other subject. Skip a choice the user still has to make about their own code (toby-design) and step-by-step teaching (toby-learning, which loads only when invoked by name).

The body stays at about 1,480 tokens. Its "When the topic is code" list cites the reference file behind each principle in place of a skill name. It already loads `toby-voice: references/plain-language.md`, and it already names `toby-artifact-style` when the user asks for a visual.

| Reference | When the body opens it |
|---|---|
| `references/examples.md` | A cold start or an interpretation question. |
| One of `strategy.md`, `modules.md`, `interfaces.md`, `errors.md`, or `testing.md` | The answer applies that principle to code. |

### toby-docs (renamed from toby-swd-docs)

> Covers writing and updating documentation files in the user's repo: README.md for people who call a module, AGENTS.md for agents who change it, and other Markdown docs. Use when the user asks to write, update, or fix a README, an AGENTS.md, or a docs page. Skip comments and docstrings inside code (toby-refactor) and prose outside the repo (toby-voice).

The body holds about 450 tokens. It says to check the existing file against the code before an edit. A docs page other than the two module files gets the facts-only, no-duplication, and maintenance rules. The current body moves to `references/module-docs.md`, because `toby-feature-dev` and `toby-refactor` open it after a structural change.

| Reference | When the body opens it |
|---|---|
| `references/module-docs.md` | Always for a README or an AGENTS.md. |
| `references/examples.md` | The file is new. |

### toby-environment (renamed from toby-swd-environment)

> Covers running commands and changing machine state with the user's approval: migrations, seed scripts, installs, processes, ports, caches, settings, credentials, and git pushes. Use when the user asks to run, start, stop, install, migrate, seed, clear, commit, or push something. Skip test and snapshot edits (toby-write-tests) and an experiment loop where code changes between tries (toby-experiment).

The body holds about 500 tokens. It keeps the opening rule to inspect, report, and ask. It also keeps the Reporting back section. A new line says to hand a build broken by an install or a migration to `toby-fix-bug`. The command classes, ports, long-running processes, heavy repo commands, and red flags move to `references/commands.md`, which five other skills open.

| Reference | When the body opens it |
|---|---|
| `references/commands.md` | Always. |

### toby-experiment (renamed from toby-swd-experiment)

> Gives the steps for a short, reversible discovery loop while the behavior is undecided, such as a spike, prototype, proof of concept, parameter sweep, or debug panel. Use when the user says throwaway, spike, prototype, experiment, try a few values, or tweak it while I test. The word throwaway outranks every other noun in the request. Skip work the user means to keep (toby-feature-dev) and a bare command (toby-environment).

The body stays at 1,200 tokens, with skill names updated. The trigger words in the guide's Work Modes line move into this description, so the guide line goes.

| Reference | When the body opens it |
|---|---|
| `toby-environment: references/commands.md` | Before a command. |
| `toby-write-tests: references/testing.md` | After the user picks a behavior to keep. |

It hands the chosen behavior to `toby-feature-dev` in the finish phase.

### toby-voice (kept)

> Gives the steps to apply Toby's writing rules to prose before it is sent: the five tests, the banned lists, the deletion tests, and the voice checker. Use when the user asks for a rewrite, a voice pass, or wording or tone help, or for prose with no code task, such as an email or a commit message. Every other Toby skill loads it as its last step. Skip choosing the content, which the task skill does first.

The body stays at about 2,000 tokens, and its references do not change. The description drops the clause that skipped comments inside code, which contradicted its own use clause.

### toby-artifact-style (kept)

> Covers Toby's visual design system for an artifact: color and type tokens, layout, chart rules, deck patterns, and artifact copy. Use when the user asks for a visual, such as an HTML page, chart, diagram, dashboard, slide deck, mockup, or reference card, including one that teaches. Skip a plain answer in chat with no visual asked for (toby-explain), and skip a game or a screen in an app's codebase (toby-feature-dev).

The body and its seven references do not change.

### Invoke-only skills (kept)

These three descriptions belong to `toby-learning`, `toby-squall`, and `toby-game`, in that order.

> Covers teaching a subject step by step with the learner doing the work: a guess before each step, the answer right after it, then a new case. Trigger only when the user explicitly invokes this skill by name or with /toby-learning. Skip every question that asks for an answer, such as why, how, or walk me through, which toby-explain covers.

> Covers brainstorming that widens one example the user gives into the wider set it belongs to, with labeled options and no pick. Trigger only when the user explicitly invokes this skill by name or with /toby-squall. Skip general requests such as "help me think through this" or "brainstorm with me".

> Covers building a single-file HTML simulation game or toy with the creator, in Toby's style: a real system underneath, deadpan comedy, and a paper-and-ink look. Trigger only when the creator explicitly invokes this skill by name or with /toby-game. Skip a plain request to make a game, sim, toy, or visualizer.

The bodies and references do not change. Each frontmatter gets `disable-model-invocation: true` for Claude Code and Copilot. For Codex, the matching `agents/openai.yaml` gets `allow_implicit_invocation: false`. On Claude Code that flag takes the description out of the model's listing, so a false load becomes impossible. The cost is that typing the skill's name in a sentence stops loading it on Claude Code, and only the slash command works. The phrase "Trigger only when the user explicitly invokes" stays, because `validate-skills.py` checks for it and hosts that ignore the flag still read it.

## Request map

All 11 prompts in `evals/suites/triggering.md` appear below, with 18 more. R1 to R13 are the colliding requests the research found between current skills. R14 to R18 test the new request kinds.

| Request | Entry skill | Chain and references |
|---|---|---|
| P1. Add a `getAccountBalance(userId)` method to `AccountRepository`, reading Redis first and Postgres on a miss. | `toby-feature-dev` (tactical) | `interfaces.md`, `interfaces/caching.md`, `errors.md`, `testing.md`, then `toby-voice` |
| P2. `invoice.ts` is 1,400 lines and does three jobs. Split it. | `toby-refactor` (boundary scope) | `strategy.md`, `modules.md`, `module-docs.md`, and `interfaces.md` if exports change |
| P3. Build the CSV export for the reports page. | `toby-feature-dev` | `testing.md`, plus `modules.md` or `interfaces.md` as the design needs |
| P4. Run the pending migration and re-seed. | `toby-environment` | `commands.md` |
| N1. Rename `usr` to `user` in `session.ts`. | `toby-refactor` | `naming.md` |
| N2. Review my changes. | `toby-code-review` | `smells.md` in the design pass |
| N3. Try a few retry backoff values, throwaway. | `toby-experiment` | none |
| N4. Add a `phone` field the way `email` is done. | none | `toby-feature-dev` skips it by its first skip clause |
| N5. Build me a browser traffic game in one HTML file. | `toby-feature-dev`, or none | `toby-game` is out of the listing on Claude Code |
| N6. Help me brainstorm names for this service. | none | `toby-squall` is out of the listing on Claude Code |
| N7. In one or two sentences, mutex or semaphore? | `toby-explain` | none |
| R1. Tidy the confusing control flow in `parseArgs` and rename its variables. | `toby-refactor` | `comments.md`, `naming.md` |
| R2. Refactor the checkout service so the discount rules are in one function. | `toby-refactor` | `strategy.md`, `modules.md` |
| R3. De-duplicate the two date helpers into one shared module. | `toby-refactor` | `modules.md` |
| R4. Simplify the error handling in `upload.ts`, because half the catch blocks never run. | `toby-refactor` | `errors.md`, `simplify.md` |
| R5. Update the Jest snapshots for `Header`. | `toby-write-tests` | `testing.md`, `commands.md` |
| R6. Update the billing module README after the split. | `toby-docs` | `module-docs.md`, then `toby-voice` |
| R7. Add an optional timeout parameter to the public `fetchReport()`. | `toby-feature-dev` (tactical) | `interfaces.md`, `module-docs.md` |
| R8. Add a POST /invites endpoint that emails the invitee. | `toby-feature-dev` | `interfaces.md`, `interfaces/backend-apis.md`, `testing.md` |
| R9. Start the dev server so I can try the new button by hand. | `toby-environment` | `commands.md` |
| R10. Make a five-slide deck on the Q3 outage. | `toby-artifact-style` | `decks.md`, then `toby-voice` |
| R11. Explain how a TCP handshake works, with a diagram. | `toby-explain` | `toby-artifact-style` for the diagram, named in the explain body |
| R12. Walk me through how B-tree indexes work. | `toby-explain` | none |
| R13. Move the date helpers into a shared package and export `formatDate`. | `toby-refactor` | `modules.md`, `interfaces.md` |
| R14. The login page returns a 500 when the email has a plus sign. Fix it. | `toby-fix-bug` | `testing.md`, `errors.md` |
| R15. The orders query takes 4 seconds. Make it faster. | `toby-optimize` | `performance.md`, `complexity/databases.md` |
| R16. Should the retry logic go in the HTTP client or in each service? | `toby-design` | `modules.md`, `errors.md` |
| R17. Write tests for the discount calculator. | `toby-write-tests` | `testing.md` |
| R18a. Why does this test fail on CI and pass locally? | `toby-explain` | none |
| R18b. This test fails on CI. Fix it. | `toby-fix-bug` | `testing.md`, `commands.md` |

## Boundaries

A pair of skills needs skip clauses in both directions when both descriptions contain words from the same request. A pair whose trigger words do not overlap needs a skip clause on one side at most. The table lists every pair whose words overlap in the drafts above.

| Pair | Dividing question | Who names whom |
|---|---|---|
| `feature-dev` and `fix-bug` | Is the behavior new, or broken? | Both |
| `feature-dev` and `refactor` | Does the behavior change? | Both |
| `feature-dev` and `experiment` | Will the user keep it? | Both |
| `feature-dev` and `design` | Did the user ask for code, or advice? | `design` names `feature-dev`, and `feature-dev` uses no design words |
| `fix-bug` and `explain` | Does the user want a fix, or an answer? | `fix-bug` names `explain`, and `explain` uses no fix words |
| `fix-bug` and `optimize` | Is the output wrong, or slow? | Both |
| `fix-bug` and `write-tests` | Is a test failing or flaky? | Both |
| `refactor` and `code-review` | Did the user ask for an edit, or findings? | Both |
| `refactor` and `docs` | Is the text inside code, or in a doc file? | `docs` names `refactor` |
| `write-tests` and `environment` | Does the request edit tests, or only run them? | Both |
| `environment` and `experiment` | Does code change between tries? | Both |
| `optimize` and `experiment` | Is the sweep throwaway? | `optimize` names `experiment` |
| `design` and `explain` | Is the choice still open, or is the code already written? | Both |
| `design` and `experiment` | Are the options compared on paper, or run? | `design` names `experiment` |
| `explain` and `learning` | Did the user invoke `toby-learning`? | Both |
| `explain` and `artifact-style` | Did the user ask for a visual? | `artifact-style` names `explain`, and `explain` names `artifact-style` as a chain step |
| `artifact-style` and `feature-dev` | Is it a game or an app screen? | `artifact-style` names `feature-dev` |
| `voice` and every entry skill | None, because `toby-voice` runs after the entry skill | The guide and each entry body state the chain |

Three overlaps from the research stay in this set as chains that a skill states, which the criterion allows. `toby-voice` runs after `toby-code-review`, `toby-docs`, and `toby-artifact-style`, because it checks the prose those skills write. When the user asks for a diagram, `toby-explain` hands it to `toby-artifact-style`. A commit request goes to `toby-environment`, which loads `toby-voice` for the message.

## Firing

Each description follows the research on what makes a skill load.

- It opens in the third person with what the skill covers. Then "Use when" lists the verbs a user types, and "Skip" names the skill that covers each skipped case. Anthropic's guide asks for the third person, and the open standard asks for the boundary with adjacent skills.
- Each new or renamed skill's name states its request kind, such as fix-bug, refactor, and optimize. A dev.to test routed 8 of 8 requests correctly when either the name or the description told two jobs apart.
- No description says "ALWAYS invoke". The 650-trial study behind that wording reports no false-fire rate, so its effect on 13 skills that each claim priority is untested.
- The descriptions run from 298 to 490 characters, under the 1,024 limit in `validate-skills.py` and the 1,536-character listing cap in Claude Code.
- The 16 descriptions and names total 6,649 characters, against 9,830 today by the same count. Without the three invoke-only skills, the Claude Code listing holds 5,668 characters. Claude Code 2.1.283 gives all skills together 8,000 characters at a 200K context, and skills past that budget show only their names.

Two firing risks come from outside this set. First, this session lists every Toby skill twice, once as `anthropic-skills:toby-*` from claude.ai, which doubles the listing. Removing those copies is an account change for the user to make. Second, this session also lists skills named `simplify`, `code-review`, and `run` that Toby does not ship. Each of the three overlaps the Toby skill for the same request, which is `toby-refactor`, `toby-code-review`, or `toby-environment`. Today the `simplify` skill already overlaps `toby-simplify-code` in the same way.

The guide's Skill Routing section changes in two places. The tie-break line becomes the text below.

> Load one entry skill per request, meaning the skill whose description matches the kind of request. When two descriptions match, load the one whose skip clause does not name the other. The entry skill opens the method references it lists and names any skill it hands work to.

The Work Modes line that lists experiment triggers goes, because the `toby-experiment` description now holds those words. The voice lines, the three invoke-only lines, the skip-precedence line, and the active-skills line stay, with `toby-swd-experiment` renamed.

## Tokens

The numbers use `len(text)/4`, the ruler in `scripts/token-budget.py`. Resident cost is the operating guide plus every description frontmatter.

| Resident | Today | Proposed |
|---|---|---|
| Operating guide | 4,744 | about 4,663 |
| Description frontmatter | 2,649 (18 skills) | about 1,850 (16 skills) |
| Total | 7,393 | about 6,513 |
| Model listing on Claude Code, with the invoke-only flag | 7,393 | about 6,215 |

The loaded cost counts each body plus the method references the body opens for that scenario. Stack files such as `modules/web.md` stay out of both columns, because they were reference files before as well. The proposed bodies of `toby-fix-bug`, `toby-refactor`, `toby-design`, `toby-optimize`, `toby-write-tests`, `toby-docs`, and `toby-environment` are estimates, and so is the split of `toby-feature-dev`.

| Scenario in `token-budget.py` | Today | Proposed | Change |
|---|---|---|---|
| a question, answered | 1,476 | 1,480 | +4 |
| a rename | 2,554 | 2,300 | -254 |
| a command or migration | 1,636 | 1,790 | +154 |
| review my changes | 3,341 | 3,360 | +19 |
| a throwaway spike | 1,200 | 1,200 | 0 |
| one method on a repository | 7,909 | 11,297 | +3,388 |
| split a module | 7,512 | 8,280 | +768 |
| a feature, tactical | 9,209 | 6,346 | -2,863 |
| a feature, strategic | 20,858 | 20,430 | -428 |
| learning, invoked | 3,083 | 3,083 | 0 |
| a visual artifact | 5,452 | 5,452 | 0 |

The repository method costs 3,388 more tokens, because it now loads the 4,440-token `toby-feature-dev` body with its criteria and before-and-after proof. The current P1 loads no workflow skill, although the blind run fired `toby-feature-dev` on P1 anyway. A tactical feature costs 8,018 tokens when the change adds a special case, because `strategy.md` opens then. Splitting a module costs 11,717 tokens when its exports change.

The largest modelled turn falls from 28,251 to about 26,943 tokens before a stack file opens. A prose turn still adds 3,730 tokens for `toby-voice` and `plain-language.md` on both sides.

The new request kinds cost between 2,113 and 4,840 loaded tokens.

| New scenario | Loaded |
|---|---|
| fix a bug | 3,326, or 4,840 with an error path |
| make it faster | 2,113 |
| a placement question | 4,318 |
| write tests | 2,356 |
| update a README | 2,310 |

`token-budget.py` models bodies only. Its SCENARIOS table needs the new names and a reference layer. Without that layer it prints 4,440 for the strategic feature, which leaves out 15,990 tokens of method.

## Practices that move

Every section of the six retired skills moves, and parts of four others move. Each row below is one section of a current SKILL.md body whose text changes file. The count is 65 sections, plus each skill's opening paragraph. `scripts/rule-inventory.py`, run before and after, would show any sentence that gets lost.

| Source | Sections | Destination |
|---|---|---|
| `toby-swd-strategy` (10) | Before writing, While writing, After writing, The test for modifying existing code, Brownfield Work, When the quick fix is the correct choice, What to report back, Anti-patterns, Worked examples | `toby-design: references/strategy.md` |
| | Writing a design note | `toby-design/SKILL.md` |
| `toby-swd-modules` (7) | Make modules somewhat general-purpose, The checks, Replace the growing conditional, Brownfield Work, Red flags, References | `toby-design: references/modules.md` |
| | Writing a placement note | `toby-design/SKILL.md` |
| `toby-swd-interfaces` (5) | Bias toward somewhat general-purpose, The procedure, Brownfield Work, Red flags, References | `toby-design: references/interfaces.md` |
| `toby-swd-complexity` (6) | Error design, with half of Brownfield Work, Red flags, and References | `toby-design: references/errors.md` |
| | Performance design, Proportionality, with the other half of those three | `toby-design: references/performance.md` |
| `toby-swd-clarity` (7) | Naming, Consistency, with the naming red flags | `toby-refactor: references/naming.md` |
| | Comments, Obviousness, Proportionality, Brownfield Work, with the other red flags | `toby-refactor: references/comments.md` |
| `toby-simplify-code` (9) | Disposition, Behavior drift, Process, Final response | `toby-refactor/SKILL.md` |
| | What to look for, Not a simplification, Idiom or local style, Keep | `toby-refactor: references/simplify.md` |
| | Out of scope | Rewritten as the scope rule in `toby-refactor/SKILL.md` |
| `toby-swd-testing` (10) | All ten sections | `toby-write-tests: references/testing.md` |
| `toby-swd-docs` (3) | AGENTS.md, README.md, Brownfield Work | `toby-docs: references/module-docs.md` |
| `toby-swd-environment` (5) | Classify every command, Ports, Long-running processes, Heavy repo commands, Red flags | `toby-environment: references/commands.md` |
| `toby-feature-dev` (3) | Cut the work into slices, Checkpoints for stops 2 and 3, The plan document | `toby-feature-dev: references/strategic.md` |

Five rules move out of the retired descriptions, because a retired skill has no description left to hold them.

- Strategy skipped renames, formatting passes, read-only work, spikes, and changes whose structure the surrounding code already sets. That list goes to the top of `strategy.md`.
- Interfaces skipped a field added beside an identical one, which the first skip clause of `toby-feature-dev` already covers.
- Modules skipped an edit inside one module that adds no boundary, which goes into the scope table of `toby-refactor`.
- Testing refused to make a failing test green by editing its assertion. That rule goes to the red flags of `toby-fix-bug` and stays in `testing.md`.
- Complexity said that removing a needless error is cheap and that heavier performance work waits for a measurement. Both sentences already appear in the body and move with it.

Six practices change meaning as well as place, so each one needs the user's agreement.

1. The Out of scope rule of `toby-simplify-code` banned module moves and signature changes. Under `toby-refactor`, those changes happen when the user asks for a split, move, or extract, while a simplify request stays local.
2. `toby-feature-dev` loaded strategy for every durable feature. It now opens `strategy.md` at strategic size, and at tactical size when the change adds a special case, a flag, or a hidden dependency. The design pass in its own body still runs at both sizes.
3. `toby-swd-testing` loaded on every behavior change. Now `toby-feature-dev` and `toby-fix-bug` open `testing.md` on every slice and every fix. `toby-refactor` runs the existing tests before and after its edit.
4. `toby-voice` skipped comments inside code. Comments now get the voice pass through the chain, which matches the guide's rule that comments are prose.
5. `toby-docs` covers other Markdown docs in the repo, beyond README.md and AGENTS.md.
6. `toby-environment` loads on commit and push requests, which no current description names.

## Hosts

`scripts/install.sh` copies every `skills/toby-*` folder to four hosts as sibling folders, so a path into another skill's folder exists on each host.

| Host | Install path | What this set needs | Not verified |
|---|---|---|---|
| Claude Code | `~/.claude/skills`, `~/.claude/CLAUDE.md` | Names and descriptions inside the limits above. `disable-model-invocation: true` on the three invoke-only skills. | The installed `~/.claude/CLAUDE.md` predates commit 8f238da and still routes to the six retired skills, so it needs a reinstall. Whether the `anthropic-skills:toby-*` copies keep their sibling folders is unknown. |
| Codex | `~/.codex/skills`, `~/.codex/AGENTS.md` | An `agents/openai.yaml` for each new skill, with its `$toby-*` default prompt. `allow_implicit_invocation: false` for the three invoke-only skills. | Whether Codex ignores the `disable-model-invocation` key. Whether Codex reads a file in a sibling skill folder. |
| GitHub Copilot | `~/.copilot/skills`, `~/.copilot/copilot-instructions.md` | Lowercase hyphenated names of 64 characters or fewer, and descriptions of 1,024 characters or fewer. All 16 qualify. | Whether a skill flagged `disable-model-invocation` still loads when its name appears in a sentence. |
| Kiro | `~/.kiro/skills`, `~/.kiro/steering/toby-instructions.md` | Name and description. A custom agent lists each skill by `skill://` URI, so the 8 new names need adding there. | Kiro's description limit, its handling of unknown frontmatter keys, and reads across skill folders. |

The install script needs one change. It replaces only the folders it installs, so the 10 old folder names would stay on every host and keep loading beside the new set. A list of retired names in `install.sh` would remove them. That removal deletes up to 40 folders across four hosts, so it needs the user's approval each time. `scripts/test-install.sh` should check that every cross-folder reference resolves in each installed tree.

If any host fails that check, `scripts/sync.sh` can copy each method file from one source folder into every entry skill that cites it. `sync.sh` already copies the voice checker into `toby-voice` that way.

## Migration

| Change | Count |
|---|---|
| Skill folders created | 4 (`toby-fix-bug`, `toby-refactor`, `toby-design`, `toby-optimize`) |
| Skill folders renamed | 4 (`toby-write-tests`, `toby-docs`, `toby-environment`, `toby-experiment`) |
| Skill folders retired | 6 |
| Skill folders kept under the same name | 8 |
| Files created under `skills/` | 15. These are 5 SKILL.md files, 4 `openai.yaml` files, and 6 reference files split from bodies. |
| Files merged under `skills/` | 2 (`toby-refactor/SKILL.md`, `toby-design/SKILL.md`) |
| Files moved under `skills/` | 36. These are 6 SKILL.md bodies that become references, 25 reference files, 1 renamed SKILL.md, and 4 `openai.yaml` files. |
| Files deleted under `skills/` | 9 (3 split SKILL.md sources and 6 `openai.yaml` files) |
| Files edited in place under `skills/` | 18 |
| Files edited outside `skills/` | 34 |
| Installed folders to remove | up to 40, with approval |

The 34 outside files start with `base/toby.md`, its 5 synced copies including `AGENTS.md` and `CLAUDE-floor.md`, and `README.md`. They also include 6 scripts: `validate-skills.py`, `trigger-probe.py`, `token-budget.py`, `measure-skills.py`, `voice_rules.py`, and `install.sh`. Next come `evals/run.py`, `evals/boundaries.md`, `evals/README.md`, `evals/grading.md`, and `evals/rubric/pass-fail.md`, plus 2 test files and up to 6 regenerated baselines. The last 8 are the suite files that name a retired skill. The run records in `evals/baselines/runs/` stay as history.

`validate-skills.py` needs four changes.

- `ROUTING_GROUPS` lists skills only, so it has to add the references each entry opens.
- The strategic group comes to about 20,430 tokens, over the 19,000 co-load ceiling, so the ceiling or the group needs a decision.
- `check_reference_reachability` skips every cross-folder reference today. This layout depends on those references, so the check has to confirm each one exists.
- `INVOKE_ONLY_SKILLS` stays, with a new check for the flag in each invoke-only frontmatter.

Five eval suites need new cases.

| Suite | New cases |
|---|---|
| `triggering.md` | R1 to R13 as collision probes, plus two probes for each new skill, which takes it from 11 to 32 scenarios. The expected sets for P1, P2, N1, N3, N4, and N6 change. |
| `swd.md` | A bug-fix report task and an optimization report task. |
| `swd-notes.md` | Its design and placement notes, routed to `toby-design`. |
| `explain.md` | A request on the line between `toby-design` and `toby-explain`. |
| `feature-dev.md` | A tactical request that must leave `strategic.md` closed. |

`trigger-probe.py` needs all 16 skills, since it leaves out `toby-voice` and `toby-artifact-style` today. The `run.py` prompt still says 14 skills and eight prompts.

Four suites need only name edits: `review.md`, `artifacts.md`, `raw.md`, and `real.md`. The `content` and `holdout` prompts in `run.py` need the same edit.

Nobody has run the proposed triggering eval. The user's memory rule says to agree on the eval design before any run. The skill-creator loop uses 20 queries per skill, with 8 to 10 near-miss negatives, a 60/40 split, and 3 runs per query. `run.py` asks for 2 samples per suite, and no run file records its model today.

## Unverified

- No triggering run has measured these descriptions or the current ones.
- The new body sizes are estimates, so every proposed token number except the descriptions and the guide line can move.
- Reads across skill folders are untested on Codex, Copilot, and Kiro.
- How Codex and Kiro treat the `disable-model-invocation` key is unknown.
- A forced-eval hook reached 100 percent activation with 4 skills on Sonnet 4.5. Nobody has measured it with 13, so this proposal leaves it out.
