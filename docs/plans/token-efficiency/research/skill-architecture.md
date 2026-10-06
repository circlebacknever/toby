# Toby skill architecture

This document recommends a set of 20 Toby skills, in which each user request loads one entry skill or none. The tags in Rejected ideas point to the four proposals it came from: `architecture-open.md`, `architecture-decision.md`, `architecture-request.md`, and `architecture-domain.md`.

- The model picks from 11 entry skills. Host fields hide six method skills and three invoke-only skills on Claude Code, Codex, and Copilot.
- Resident cost falls from 7,393 to 6,833 tokens. The Toby part of the Claude Code skill listing falls from 9,920 to 5,710 characters.
- The strategic feature, the largest of the 11 modelled scenarios, falls from 20,858 to 19,062 loaded tokens.
- No rewritten file exists yet, so every body size is a projection from measured sections plus drafted text. The scripts `scratchpad/arch-final/model.py` and `scratchpad/arch-final/descs.py` compute the numbers with the len/4 ruler of `scripts/token-budget.py`. The Tokens section lists where this review's numbers differ from the scripts' output.

## Terms

- An entry skill is a skill the model picks from its description.
- A method skill is a skill that loads only when an entry skill's body opens it.
- "Opens X" means the body lists a step at which the agent reads the file X. When X is a skill, the file is that skill's SKILL.md, in a folder beside the entry skill's folder.
- No research fact shows an agent reading a sibling skill folder by path on any of the four hosts. Step 2 of the migration tests that read on each host before anything is built.
- A chain is an entry skill plus the method skills its body opens for one request.
- An invoke-only skill loads only when the user invokes it with the host's skill command, such as `/toby-game` in Claude Code.
- A hidden skill has `disable-model-invocation: true` in its frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Claude Code and Copilot read the first field, while Codex reads the second. The research names the Codex field but does not show which section of `openai.yaml` holds it, so step 4 checks the Codex docs before writing it.

## Skill list

### Entry skills

#### toby-build, renamed from toby-feature-dev

> Changes what code does in the smallest step that leaves the design at least as good as before. It proves each change with one check run before the edit and again after it. Use it when the user asks to add, build, implement, wire up, or finish a behavior. The behavior can be a feature, a ticket, an endpoint, a method, a screen, a job, or a flag. Skip it for wrong output, which toby-bug-fix covers, and for slow code, which toby-optimize covers. Skip it when behavior stays the same, which toby-refactor covers, and for a throwaway, which toby-swd-experiment covers. Skip it for a one-file edit that copies a pattern already in that file.

The body holds 4,065 tokens. It keeps the running order, the mode choice, the size gate, tactical discovery, criteria, ambiguity, and stop 1. It also keeps the build loop, Don't build, the red flags, and the final response. It keeps the tactical design line, which states the structure chosen, the alternative rejected, and any new signature in chat before the first edit. The strategic parts move to `references/strategic.md`. They are sibling-feature and call-site discovery, greenfield rules, the slice cut, and stops 2 and 3. They also include the design lines, the plan document, and resuming half-built work. A method table replaces the "Load `toby-swd-modules` when" bullets. The two-run proof moves to `toby-swd-testing`, so the "Prove the slice" section cites that skill.

| The body opens | When |
| --- | --- |
| `references/strategic.md` (1,436) | a strategic trigger fires |
| `references/checks.md` (1,264) | before the out-of-scope line or the first edit, and again before the handoff |
| `references/examples.md` (3,338) | the work needs a slice cut or a plan step |
| `toby-swd-strategy` | before the design pass, unless the surrounding code already settles the structure |
| `toby-swd-interfaces` | the design adds or changes a signature |
| `toby-swd-modules` | the design adds a module, moves code, or gives a module a new job |
| `toby-swd-errors` | a criterion has a failure case, a retry, a timeout, validation, or state shared between concurrent tasks |
| `toby-optimize` | a criterion states a time or memory budget, or the design adds a cache, a batch, or a queue for speed |
| `toby-swd-testing` | before the first edit of each behavior change |
| `toby-swd-docs` | module structure, a public API, a cross-module decision, an extension rule, or how a person uses the module changes |
| `toby-swd-environment` | before any command beyond safe inspection |
| `toby-swd-clarity` | before the handoff, when the diff adds a public name or an interface comment |

#### toby-bug-fix, new

> Fixes behavior that is wrong today. It reproduces the failure, finds the cause at a file and line, fixes that cause, and proves the fix with a run before and after. Use it when the user reports a bug, a crash, an error message, a regression, or wrong output and wants it fixed. Use it when the user pastes a stack trace, or says a build or a test started failing. Skip it for a question about why something fails with no fix asked for, which toby-explain covers. Skip it for a flaky test, which toby-swd-testing covers, and for slow code, which toby-optimize covers. Skip it for a throwaway trial, which toby-swd-experiment covers.

The body holds 616 tokens. It is the decision proposal's draft in `scratchpad/ad-bugfix-draft.md` minus step 4, which stops after a why answer, because `toby-explain` answers that question. It adds a line that opens `toby-swd-environment` and changes the draft's handover target from `toby-feature-dev` to `toby-build`. Its five steps are reproduce, classify a failing test, find the cause at a file and line, choose the fix, and prove it. A scope rule keeps the diff to the cause and its test. When the fix is in shared code, the rule asks which callers were checked. Three red flags cover a fix with no reproduction, a branch for the one reported input, and a test changed to pass. The other two cover a catch block that hides the error and an install or a cache clear before any cause was found. The final response leads with the cause at a file and line.

| The body opens | When |
| --- | --- |
| `toby-swd-testing` | at the reproduce step, for a failing test's four classes, and at the prove step |
| `toby-swd-strategy` | the fix would patch around a design problem |
| `toby-swd-errors` | the cause is in an error path, a retry, or a validation step |
| `toby-swd-environment` | before any command beyond a narrow test |
| `toby-build`, as a handover | the repair needs new behavior in more than one file, with the reproduction as its first criterion |

#### toby-optimize, new

> Makes working code faster or lighter from a measured baseline, with one change per measurement. It covers whether a cache, a batch, a queue, or parallel work is worth what it adds. Use it when the user says code is slow, or asks to speed it up or to cut latency, memory, or query count. Use it when the user asks to add a cache to code that already works. Skip it for new behavior that includes a cache, which toby-build covers, and for wrong output, which toby-bug-fix covers. Skip it for a speed question with no change asked for, which toby-explain covers, and for a throwaway sweep, which toby-swd-experiment covers.

The body holds 1,181 tokens. It holds the performance half of `toby-swd-complexity`, which is Performance design, Proportionality, the four performance red flags, and half of Brownfield Work. It adds five steps from the request proposal. First the agent records a baseline and looks for a better algorithm, an index, or a cache before any code-level tuning. Then it changes one thing and measures again. It reverts a change with no measured effect unless that change also made the code simpler. When the path has a stated budget, it measures the worst case under load. The report gives the baseline, the result, the command, and what stays unmeasured. Other entry skills also open this file, the way they open `toby-swd-testing`.

| The body opens | When |
| --- | --- |
| `references/examples.md` (about 260) | first |
| one stack file, from `backend-apis.md` (about 1,210), `databases.md` (about 2,310), `web.md` (about 2,060), and `mobile.md` (about 1,690) | the file matches the code |
| `references/caching.md` (2,844), moved from complexity | a cache is the question |
| `toby-swd-interfaces` | a new cache's get-or-load contract needs a design |
| `toby-swd-testing` | at the prove step, for the two-run form |
| `toby-swd-environment` | before a benchmark, a profiler, or a heavy suite |

#### toby-refactor, renamed from toby-simplify-code

> Changes how code is arranged or reads and keeps its behavior and tests the same. Use it when the user asks to simplify, tidy, refactor, de-duplicate, extract, split, merge, move, or rename code, or to make it easier to read. Use it to add, fix, or delete comments and docstrings. Skip it when behavior should change, which toby-build, toby-bug-fix, or toby-optimize covers. Skip it when the user wants findings with no edit, which toby-code-review covers.

The body holds 1,231 tokens. It keeps the disposition, the behavior-drift rules, Keep, Out of scope, the process, and the final response. The disposition keeps the countable win, precision over recall, and "nothing worth simplifying" as a valid result. Out of scope names `toby-swd-errors` and `toby-optimize` where it names `toby-swd-complexity` today. In a new scope picker, the agent states the scope in one line and opens only the files in that scope's row below.

| The body opens | When |
| --- | --- |
| `toby-swd-clarity` | only names, comments, or docstrings change |
| `references/cleanup.md` (843) and `references/smells.md` (2,184) | the scope is a local cleanup inside changed code |
| `toby-swd-strategy`, then `toby-swd-modules` | the scope is a split, merge, move, or extraction across files |
| `toby-swd-interfaces` | a signature changes |
| `toby-swd-docs` | module structure changes |
| `toby-swd-errors` | the scope is an error check for a condition that cannot occur |
| `toby-swd-testing` | before any test changes |

#### toby-swd-testing

> Keeps tests an executable specification of behavior, and classifies a failing test before anyone edits it. Use it when the user asks to write, rewrite, delete, or weaken a test, raise coverage, update snapshots, or fix a flaky test. Skip it when production code changes too, which toby-build or toby-bug-fix covers. Skip it for a throwaway spike, which toby-swd-experiment covers, and for a run of the suite alone, which toby-swd-environment covers. Skip it for a question about why a test fails, which toby-explain covers.

The body holds 1,979 tokens. It keeps every current section, including Brownfield Work. A new section, "Prove a change", holds the two-run proof from feature-dev, so build, bug-fix, and optimize cite one copy. The "Experiment loops" subsection moves to `toby-swd-experiment`, because that skill opens testing only after the user picks a behavior. The skill has no reference files. It opens `toby-swd-environment` before a snapshot update or a full-suite run.

#### toby-code-review

> Reports the proven risks in a change and edits nothing. Use it when the user asks to review, check, or audit a diff, a PR, a commit, a branch, or the working tree. Use it when the user asks what is wrong with a change. Skip it when the user wants the code changed, which toby-refactor or toby-bug-fix covers. Skip it for a question about how code works, which toby-explain covers.

The body holds 3,138 tokens, because the section on reviewing a skills or config diff moves to a reference file. The four passes and the evidence rules stay. The intro already maps each kind of fix to a method skill. The body now opens that skill when a finding depends on it.

| The body opens | When |
| --- | --- |
| `references/smells.md` (4,874) | the design pass |
| `references/skills-diff.md` (245) | the diff changes a SKILL.md, a guide, a hook, or an agent config |
| one method skill | a finding's fix depends on that method |
| `toby-swd-environment` | before any run beyond safe inspection |

#### toby-explain

> Answers a question in plain words, then stops, and edits no files. Use it when the user asks why, how, what the difference is, which option fits, or where code should go, on any subject. Use it for "walk me through", "help me understand", and any request for a clear, short, or simple explanation. Skip it when the user asks for a diagram, a chart, or a deck, which toby-artifact-style covers. Skip it when the user wants a fix, which toby-bug-fix covers.

The body holds 1,544 tokens, which is the current body plus one chain line. That line tells the agent to open the method file that answers a question about the user's code.

| The body opens | When |
| --- | --- |
| `references/examples.md` (394) | a cold start or an interpretation question |
| `toby-voice`'s `references/plain-language.md` (1,743) | every time, as today |
| `toby-swd-modules` | a placement question, answered with its placement note |
| `toby-swd-strategy/references/design-note.md` (211) | a design choice |
| `toby-swd-errors` | a question about an error path |
| `toby-optimize` | a question about a cache or a speed-up |

#### toby-swd-experiment

> Runs a short, reversible discovery loop while the behavior is still undecided. Use it when the user says experiment, spike, prototype, proof of concept, throwaway, try a few values, compare options, tweak settings, or let me test. Use it to iterate on code from the user's feedback. The word throwaway decides the route even when the request also names retries, timeouts, or tests. Skip it for work the user intends to keep, which toby-build covers. Skip it for starting or stopping a server alone, which toby-swd-environment covers.

The body holds 1,238 tokens. It keeps the mode contract, the experiment surface, the disposable markings, the iteration loop, the finish phase, and the failure modes. Its Testing Boundary section gains the experiment-loop rules from testing, because the loop runs before testing opens. The merged section keeps today's rule that automated tests, browser automation, and screenshots run only when the user asks or the experiment surface needs them. The skill has no reference files.

| The body opens | When |
| --- | --- |
| `toby-swd-environment` | before a command |
| `toby-swd-testing` | after the user picks a behavior |

#### toby-swd-environment

> Classifies each command before it runs and asks before any command that changes the user's machine. Use it when the user asks to run a migration or a seed script, or to install a dependency. Use it to start or stop a server, free a port, clear a cache, or run the full test suite. Skip it for a code edit with nothing to run, and for a snapshot update, which toby-swd-testing covers.

The body is unchanged at 1,636 tokens. It has no reference files and opens no other skill.

#### toby-voice

> Applies Toby's writing rules to prose and runs the voice checker on it. Use it for a commit message, a PR description, a README, an AGENTS.md, a doc, a plan, or a rewrite of any text. Use it when the user says voice, toby voice, check the voice, voice pass, or voice standards. Use it when the user asks for help with banned phrasing or with the wording or tone of a text. Skip it as the first skill for names and comments inside code, which toby-refactor covers.

The body holds 2,007 tokens, which is the current body plus one line that opens `toby-swd-docs` for a module README.md or AGENTS.md. With the words "as the first skill", `toby-refactor` loads first for a comment request. The guide's voice line still loads voice before the comment is final.

| The body opens | When |
| --- | --- |
| `references/plain-language.md` (1,743) | every time |
| `references/toby.md` (4,508, synced from the new guide) | only when the operating guide is absent from context |
| `references/plain-language-examples.md` (3,313) | a rewrite is not working |
| `references/examples/banned-writing-patterns.md` (1,681) | before prose is sent |
| `chat.md` (1,268), `code.md` (1,094), or `artifacts.md` (443) | the output is that kind |
| `toby-swd-docs` | the prose is a module README.md or AGENTS.md |

#### toby-artifact-style

> Applies Toby's visual design system to a visual and to the copy inside it. The visual can be a diagram, chart, dashboard, slide deck, HTML or React page, SVG, mockup, or reference card. Use it when the user asks to draw, show, chart, diagram, or build a visual, including a visual that explains something. Skip it for a text answer in chat, which toby-explain covers, and for a game, which only /toby-game starts.

The body is unchanged at 5,452 tokens. It opens `copy.md` (2,327) for copy, `charts.md` (967) for a chart, and `decks.md` (5,987) for a deck. It opens `components.md` (5,356) for a component, `layout.md` (2,934) to place boxes and arrows, `geometry.md` (1,321) for a geometric mark, and `sample-content.md` (1,252) for placeholder data.

### Method skills

Each method skill is hidden on Claude Code, Codex, and Copilot. Kiro lists its description, because the research found no Kiro field that hides a skill. Each method skill keeps its own Brownfield Work section.

| Skill | Description | Body | The body opens |
| --- | --- | --- | --- |
| `toby-swd-strategy` | Contains Toby's design pass, run before a change. Entry skills open this file by path. Do not load it from a user request alone. | 1,487 tokens. The design pass gains feature-dev's rule that the second approach is the strongest option a competent engineer would pick. "While writing" becomes a pointer to modules checks 3 and 8. | `references/design-note.md` (211) opens for a design note in chat. `references/examples.md` (1,572) opens for a worked case. |
| `toby-swd-modules` | Contains Toby's checks for where code goes and when to split or merge modules. Entry skills open this file by path. Do not load it from a user request alone. | 3,706 tokens. Checks 3 and 8 gain the text from strategy that puts complexity in the right place. | `references/examples.md` (1,259) opens first. Then one stack file opens to match the code, from `web.md` (4,361), `mobile.md` (2,769), `backend-apis.md` (2,605), `databases.md` (2,752), and `caching.md` (2,408). `replace-the-conditional.md` (1,970) opens for a growing conditional, and `solid.md` (415) opens for a SOLID question. |
| `toby-swd-interfaces` | Contains Toby's procedure for designing a callable surface before its body. Entry skills open this file by path. Do not load it from a user request alone. | 2,879 tokens. Step 1 points to modules check 1, and the design-it-twice loop moves to a reference file. | `references/examples.md` (1,088) opens first. `references/design-it-twice.md` (578) opens for a consequential interface or a failed first comment. One stack file opens to match the code, from `web.md` (3,392), `mobile.md` (3,264), `backend-apis.md` (3,810), `databases.md` (3,291), and `caching.md` (2,787). `runtime-config.md` (1,116) opens when code reads deploy config. |
| `toby-swd-errors`, renamed from complexity | Contains Toby's error ladder for deciding how code handles a failure. Entry skills open this file by path. Do not load it from a user request alone. | 1,530 tokens. It keeps the intro on special cases and shared state, and Error design with its ladder, limit, hard rules, and degraded path. It also keeps five red flags and the error half of Brownfield Work. | `references/examples.md` (about 700) opens first. Then one stack file opens to match the code, from `backend-apis.md` (about 2,560), `databases.md` (about 1,380), `web.md` (about 1,450), and `mobile.md` (about 1,520). |
| `toby-swd-clarity` | Contains Toby's rules for names, comments, and docstrings inside code. Entry skills open this file by path. Do not load it from a user request alone. | 1,398 tokens. It keeps naming, consistency, proportionality, Brownfield Work, and the red flags. | `references/comments.md` (1,199) opens when the change adds or edits a comment, a docstring, or control flow a reader could misread. `references/examples.md` (1,042) opens for a worked case. |
| `toby-swd-docs` | Contains Toby's rules for a module's README.md and AGENTS.md. Entry skills open this file by path. Do not load it from a user request alone. | 1,980 tokens, unchanged. | `references/examples.md` (1,880) opens for backend and frontend examples of both files. |

Each complexity stack file splits by example, with the title and half the cheat sheet in each half. `toby-swd-errors` gets examples 1, 2, 4, and 6 of `backend-apis.md`, examples 2 and 6 of `databases.md`, and examples 1 and 2 of `web.md` and `mobile.md`. It also gets examples 1, 2, and 4 of `examples.md`. `toby-optimize` gets the other examples. The sizes marked "about" come from that split.

### Invoke-only skills

`toby-learning`, `toby-squall`, and `toby-game` keep their bodies, references, and descriptions. The two host fields hide all three on Claude Code, Codex, and Copilot. Kiro still reads the description, so the clause "Trigger only when the user explicitly invokes" stays. Learning opens `interpretation.md` (1,257) for a subject with no single right answer, or `retention.md` (1,385) for recall or language practice. Game opens its six references one at a time after the first loop runs. The largest of them is `architecture.md` (1,110). Squall has no references.

### Guide text

This text replaces the Skill Routing section of `base/toby.md`, which falls from 624 to 437 tokens. The Work Modes section falls from 82 to 33 tokens, because its experiment triggers move into the `toby-swd-experiment` description. The whole guide falls from 4,744 to 4,508 tokens.

```markdown
## Skill Routing
- These routes stay active whenever the matching skill is installed, including late in a long chat. Each request loads one entry skill, picked by its description. The entry skill opens the method skills it lists, at the step that needs them.
- Open `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-errors`, `toby-swd-clarity`, and `toby-swd-docs` only when an entry skill lists them, because no request starts one of them alone.
- When a Toby skill and a skill from another source match the same request, load the Toby skill.
- `toby-voice` stays in force for the rest of the session once it loads. Its rules apply to every reply from that point, in chat and in files, until the user says otherwise. A skill that has to be re-invoked each turn stops being applied around turn six.
- Load `toby-voice` before finalizing voice-bearing output: a substantive reply, code findings, a commit message, a PR description, docs, comments, a plan, or any generated artifact. Load its `references/plain-language.md` with it, and load its `references/toby.md` only when the operating guide is absent from context. Do not wait to be asked.
- When a skill's description says to skip it for this kind of task, skip it, even when a word in the request matches. When the user calls the work throwaway, use `toby-swd-experiment`, whatever else the request names.
- `toby-learning`, `toby-squall`, and `toby-game` load only when the user invokes them with the host's skill command, such as `/toby-squall` in Claude Code. When the user names one of them in a sentence and the host does not load it, ask the user to type that command.
- State active skills in one short line, including each method skill an entry skill opened.
```

Claude Code ships its own `code-review`, `simplify`, and `run` skills, which match the same requests as `toby-code-review`, `toby-refactor`, and `toby-swd-environment`. The guide line that prefers a Toby skill covers them, because a description cannot name a skill that exists on one host only.

## Request map

The 11 entry skills answer 11 different questions, while each method skill answers one question inside a chain.

| Skill | Question it answers |
| --- | --- |
| `toby-build` | What is the smallest change that delivers this new behavior, and what proves it? |
| `toby-bug-fix` | What causes this wrong behavior, and which fix removes the cause? |
| `toby-optimize` | Which measured change makes this working code fast enough, and is a cache or batch worth its cost? |
| `toby-refactor` | Which edit improves how this code is arranged or reads, with behavior unchanged? |
| `toby-swd-testing` | Which test states this behavior, and what does a failing test mean? |
| `toby-code-review` | What in this change can break? |
| `toby-explain` | What is the answer to this question? |
| `toby-swd-experiment` | What does the next reversible trial show the user? |
| `toby-swd-environment` | Can this command run without asking the user? |
| `toby-voice` | Does each sentence of this prose pass the voice rules? |
| `toby-artifact-style` | How does this visual look and read under Toby's design system? |
| `toby-swd-strategy` | Does this change leave the design better or worse? |
| `toby-swd-modules` | Which module holds this code and knowledge? |
| `toby-swd-interfaces` | What does this signature expose to callers? |
| `toby-swd-errors` | How does this code handle this failure? |
| `toby-swd-clarity` | Can the next reader guess what this name or comment means? |
| `toby-swd-docs` | What do this module's README.md and AGENTS.md need to say now? |

Rows 1 to 11 are every prompt in `evals/suites/triggering.md`. Rows 12 to 24 are the collisions the research found between today's descriptions. Rows 25 to 32 test the new boundaries.

| # | Request | Entry skill | Opens | The clause that keeps the nearest neighbour out |
| --- | --- | --- | --- | --- |
| 1 | P1. Add `getAccountBalance(userId)` to `AccountRepository`, reading Redis first, falling back to Postgres, and returning null when the account is missing. | `toby-build` | interfaces, errors, testing | `toby-optimize` skips new behavior that includes a cache. |
| 2 | P2. `invoice.ts` is 1,400 lines and does three jobs. Split it. | `toby-refactor` | strategy, modules, docs | `toby-build` skips work where behavior stays the same. |
| 3 | P3. Build the CSV export for the reports page. | `toby-build` | strategy, testing, and modules or interfaces when the design adds them | `toby-swd-testing` skips work that changes production code. |
| 4 | P4. Run the pending migration against my local database and re-seed it. | `toby-swd-environment` | none | No other entry description lists a migration. |
| 5 | N1. Rename `usr` to `user` in `session.ts`. No other change. | `toby-refactor` | clarity | `toby-build` skips work where behavior stays the same. |
| 6 | N2. Review my changes. | `toby-code-review` | a method skill when a finding depends on it | `toby-refactor` skips a request for findings. |
| 7 | N3. Try a few values for the retry backoff. Throwaway. | `toby-swd-experiment` | environment before a run | `toby-swd-errors` is hidden, and `toby-optimize` and `toby-bug-fix` skip a throwaway. |
| 8 | N4. Add a `phone` field the way `email` is done two lines up. | none | none | `toby-build` skips a one-file pattern copy. |
| 9 | N5. Build me a browser traffic game in one HTML file. | `toby-build`, or none | as the design needs | `toby-game` is hidden, and `toby-artifact-style` skips a game. |
| 10 | N6. Help me brainstorm names for this service. | none | none | `toby-squall` is hidden, and `toby-voice` takes wording help only for a text. |
| 11 | N7. Clearly and concisely, what is the difference between a mutex and a semaphore? | `toby-explain` | none | `toby-swd-clarity` is hidden. |
| 12 | Tidy the confusing control flow in `parseArgs` and rename its variables. | `toby-refactor` | clarity with `comments.md` | `toby-code-review` skips a request to change code. |
| 13 | Refactor the checkout service so the discount rules are in one function. | `toby-refactor` | strategy, modules | `toby-build` skips work where behavior stays the same. |
| 14 | De-duplicate the two date-formatting helpers into one shared module. | `toby-refactor` | strategy, modules | No other entry description lists de-duplicate. |
| 15 | Simplify the error handling in `upload.ts`, because half the catch blocks can never run. | `toby-refactor` | errors | `toby-swd-errors` is hidden. |
| 16 | Update the Jest snapshots for the `Header` component. | `toby-swd-testing` | environment before the update | `toby-swd-environment` skips a snapshot update. |
| 17 | Update the billing module README after the split. | `toby-voice` | docs | `toby-swd-docs` is hidden. |
| 18 | Add an optional `timeout` parameter to the public `fetchReport()` in the SDK. | `toby-build` | interfaces, errors, testing, docs | `toby-swd-interfaces` is hidden. |
| 19 | Add a `POST /invites` endpoint that emails the invitee. | `toby-build` | strategy, interfaces, errors, testing | `toby-swd-interfaces` is hidden. |
| 20 | Start the dev server so I can try the new button by hand. | `toby-swd-environment` | none | `toby-swd-experiment` skips starting a server alone. |
| 21 | Make a five-slide deck on the Q3 outage. | `toby-artifact-style` | none, and the guide's voice line loads `toby-voice` | `toby-explain` skips a deck. |
| 22 | Explain how a TCP handshake works, with a diagram. | `toby-artifact-style` | none | `toby-explain` skips a diagram. |
| 23 | Walk me through how B-tree indexes work. | `toby-explain` | none | `toby-learning` is hidden. |
| 24 | Move the date helpers into a shared package and export `formatDate`. | `toby-refactor` | strategy, modules, interfaces | `toby-swd-modules` and `toby-swd-interfaces` are hidden. |
| 25 | Should the retry helper go in `http/client.ts` or in each sync job? | `toby-explain` | modules, for the placement note | `toby-refactor` needs a request to change code. |
| 26 | Write the commit message for this change. | `toby-voice` | none | No other entry description lists a commit message. |
| 27 | The checkout total is one cent off for discounted orders. Fix it. | `toby-bug-fix` | testing, and strategy when the fix would patch around a design problem | `toby-build` skips wrong output. |
| 28 | The login page returns a 500 when the email has a plus sign. Fix it. | `toby-bug-fix` | testing, errors | `toby-build` skips wrong output. |
| 29 | Why does the orders test fail since yesterday's merge? | `toby-explain` | none | `toby-bug-fix` and `toby-swd-testing` skip a why question about a failing test. |
| 30 | Fix the flaky checkout test. | `toby-swd-testing` | environment before a full-suite run | `toby-bug-fix` skips a flaky test. |
| 31 | The orders page takes 4 seconds to load. Make it faster. | `toby-optimize` | environment for the benchmark | `toby-build` and `toby-bug-fix` skip slow code. |
| 32 | Should we put Redis in front of the product lookup? | `toby-explain` | `toby-optimize`, for the cost question | `toby-optimize` skips a speed question with no change asked for. |

Four requests depend on a judgement the model makes from the request text.

- Row 1 sends a single repository method to `toby-build`, which costs 2,544 more loaded tokens than today. The build body adds 4,065 tokens, while the smaller interfaces, errors, and testing bodies save 1,521. In the 5 recorded runs, P1 loaded `toby-feature-dev`, which holds the before-and-after proof, only once.
- Row 30 needs the model to tell a flaky test, which goes to `toby-swd-testing`, from a test that started failing, which goes to `toby-bug-fix`.
- Rows 21 and 22 send a visual to `toby-artifact-style` even when it explains something, because the output is a visual.
- `toby-build` opens `toby-optimize` when a new feature has a time budget, so a request that mixes new behavior and speed still enters through `toby-build`.

## Tokens

The ruler is len/4 on characters, the one `scripts/token-budget.py` uses. Its docstring says the ruler runs 5 to 15 percent low on prose with many backticks. The numbers below differ from the earlier draft's numbers for these reasons.

- It measured current reference files by characters, where the earlier draft divided bytes by 4.
- It measured the unchanged environment and docs bodies whole, at 1,636 and 1,980.
- It added the description and body text this review restored, which are listed under Practices that move.
- It wrapped each projected description at 80 columns, as today's frontmatter is wrapped. It also kept each invoke-only skill's current frontmatter and added the hide field.

### Resident

Resident cost counts the guide and every skill's frontmatter, as `token-budget.py` does.

| Part | Today | Recommended |
| --- | --- | --- |
| Operating guide | 4,744 | 4,508 |
| Frontmatter, all skills | 2,649 for 18 | 2,325 for 20 |
| Total | 7,393 | 6,833 |

The listing is the list of names and descriptions a host puts in the model's context. Each entry here counts as the name plus the description plus 5 characters. By default, Claude Code 2.1.283 gives all installed skills together 8,000 characters at a 200K context, and 40,000 at a 1M context. The research found no listing budget for Codex, Copilot, or Kiro.

| Host | Toby skills listed | Listing (characters) |
| --- | --- | --- |
| Claude Code | 11 | 5,710 |
| Codex and Copilot | 11 if their hide fields drop the description, else 20 | 5,710 or 8,286 |
| Kiro | 20 | 8,286 |
| Every host today | 18 | 9,920 |

The research shows that Claude Code drops a hidden skill's description from the listing. It does not show that for Codex or Copilot, so the trigger eval runs both listings.

The `anthropic-skills:toby-*` copies in the user's claude.ai account list 18 more skills with older descriptions. If those copies match today's 9,920 characters, the Toby listing on Claude Code comes to 15,630. Only the user can remove those copies.

### Loaded bodies

The 11 scenarios are the ones in `scripts/token-budget.py`. Both columns leave out reference files that exist today. A reference file split out of a current body counts when the scenario meets the condition that opens it.

| Scenario | Today's files | Today | Recommended files | Recommended | Change |
| --- | --- | --- | --- | --- | --- |
| a question, answered | explain | 1,476 | explain | 1,544 | +68 |
| a rename | clarity | 2,554 | refactor, clarity | 2,629 | +75 |
| a command or migration | environment | 1,636 | environment | 1,636 | 0 |
| review my changes | code-review | 3,341 | code-review | 3,138 | -203 |
| a throwaway spike | experiment | 1,200 | experiment | 1,238 | +38 |
| one method on a repository | interfaces, complexity, testing | 7,909 | build, interfaces, errors, testing | 10,453 | +2,544 |
| split a module | modules, strategy, docs | 7,512 | refactor, strategy, modules, docs | 8,404 | +892 |
| a feature, tactical | feature-dev, strategy, testing | 9,209 | build, strategy, testing | 7,531 | -1,678 |
| a feature, strategic | feature-dev and six swd skills | 20,858 | build, `strategic.md`, strategy, modules, interfaces, errors, testing, docs | 19,062 | -1,796 |
| learning, invoked | learning | 3,083 | learning | 3,083 | 0 |
| a visual artifact | artifact-style | 5,452 | artifact-style | 5,452 | 0 |
| Sum | | 64,230 | | 64,170 | -60 |

The largest modelled turn, resident plus loaded, falls from 28,251 to 25,895 tokens. A prose turn adds 3,730 tokens for the voice body and `plain-language.md` in both sets.

| Scenario outside the script | Recommended files | Loaded |
| --- | --- | --- |
| a bug fix | bug-fix, testing | 2,595 |
| a bug fix in an error path | bug-fix, testing, errors | 4,125 |
| make it faster | optimize, environment | 2,817 |
| a strategic feature with a time budget | the strategic set plus optimize | 20,243 |
| a strategic feature with a new public API | the strategic set plus `design-it-twice.md` | 19,640 |

Today a bug fix loads strategy and testing for 3,772 tokens. The largest body is artifact-style at 5,452, under the validator's 6,000 body ceiling. The eight skills that can co-load as methods total 16,140 tokens. The build body plus those eight bodies totals 20,205 tokens, over the validator's 19,000 co-load ceiling. Step 6 therefore lists the strategic build chain without optimize and clarity, at 17,626 tokens, or asks the user to raise the ceiling.

## Practices that move

Every practice in the current skills stays in some file of the new set. The table lists each practice that changes file or changes the trigger that loads it.

| # | Practice | From | To |
| --- | --- | --- | --- |
| 1 | The whole feature workflow | `toby-feature-dev` | `toby-build` |
| 2 | Behavior-preserving cleanup | `toby-simplify-code` | `toby-refactor` |
| 3 | Sibling-feature and call-site discovery, greenfield rules, the slice cut, stops 2 and 3, the design lines, the plan document, and resuming half-built work | `toby-feature-dev/SKILL.md` | `toby-build/references/strategic.md`, while the tactical design line stays in the build body |
| 4 | The "Load `toby-swd-modules` when" and "Load `toby-swd-interfaces` when" bullets | `toby-feature-dev/SKILL.md` | the method table in `toby-build` |
| 5 | What to look for, Not a simplification, and Idiom or local style | `toby-simplify-code/SKILL.md` | `toby-refactor/references/cleanup.md` |
| 6 | The rule against moving code or changing a signature during cleanup | Out of scope in `toby-simplify-code` | the local-cleanup scope of `toby-refactor`, while the across-files scope makes those moves after the modules checks |
| 7 | Put complexity in the right place while writing | `toby-swd-strategy` | checks 3 and 8 of `toby-swd-modules`, with a pointer in strategy |
| 8 | The second approach is the strongest option a competent engineer would pick | feature-dev's "Design before the plan" | the strategy design pass |
| 9 | Writing a design note | `toby-swd-strategy/SKILL.md` | `toby-swd-strategy/references/design-note.md` |
| 10 | Decompose by knowledge, step 1 of the interface procedure | `toby-swd-interfaces` | a pointer to check 1 of `toby-swd-modules` |
| 11 | The design-it-twice loop, tie resolution, and the redesign step | `toby-swd-interfaces/SKILL.md` | `toby-swd-interfaces/references/design-it-twice.md` |
| 12 | Error design, five red flags, the error half of Brownfield Work, and the error examples of each stack file | `toby-swd-complexity` | `toby-swd-errors` |
| 13 | Performance design, Proportionality, four red flags, the performance half of Brownfield Work, the performance examples of each stack file, and `caching.md` | `toby-swd-complexity` | `toby-optimize`, which adds five entry steps |
| 14 | Comments and Obviousness | `toby-swd-clarity/SKILL.md` | `toby-swd-clarity/references/comments.md` |
| 15 | How to review a skills or config diff | `toby-code-review/SKILL.md` | `toby-code-review/references/skills-diff.md` |
| 16 | The two-run proof | feature-dev's "Prove the slice" | a "Prove a change" section in `toby-swd-testing` |
| 17 | The experiment-loop test rules | testing's "Experiment loops" subsection | the Testing Boundary section of `toby-swd-experiment` |
| 18 | The bug-fix triggers | the strategy, testing, and feature-dev descriptions | the `toby-bug-fix` description, whose body adds a cause-finding step |
| 19 | The trigger for any behavior change in production code | the testing description | the method tables of build, bug-fix, refactor, and optimize |
| 20 | The feature, refactor, and public API triggers | the strategy description | the method tables of build, bug-fix, and refactor |
| 21 | The docstring and confusing-control-flow triggers | the clarity description | the refactor description, which lists docstrings and code that should be easier to read |
| 22 | The snapshot-update trigger | the environment description | the testing description |
| 23 | The four tie-break decisions for strategy, modules, interfaces, and complexity | the guide's Skill Routing section | the method tables in the entry bodies |
| 24 | The invoke-only rule for learning, squall, and game | three guide lines | the host fields, the descriptions Kiro reads, and one guide line that asks for the host's skill command |
| 25 | "walk me through" and "help me understand" | the guide's learning line | the explain description |
| 26 | `check the voice`, `voice standards`, and banned-phrasing help | the guide's voice line | the voice description, while the reapply steps stay in the voice body |
| 27 | Experiment, tweak settings, compare options, let me test, and iterate from feedback | the guide's Work Modes section | the experiment description |
| 28 | A diagram that a question asks for | the explain body, which applied artifact-style | `toby-artifact-style` as the entry skill, with an explain skip clause |
| 29 | The interfaces, modules, and docs triggers, including a cross-module decision, an extension rule, and human-facing usage for docs | those three descriptions | the method tables of build and refactor, and the voice body for docs |
| 30 | The trigger for shared state between concurrent tasks | the complexity description | the errors row of the build method table |

Four changes alter what a skill does, so each needs the user's decision before the migration.

1. Practice 6 lets `toby-refactor` move code between modules, which `toby-simplify-code` told the agent to leave alone. The modules checks and the behavior-drift rules apply to every such move.
2. The voice description drops its skip clause for an explanation. That clause conflicted with the guide line that loads voice for every substantive reply.
3. The open proposal's refactor description quoted a two-word tidying phrase whose first word is on the hard-ban list. This set leaves the phrase out, so a request worded that way relies on "tidy" and "refactor" until the user decides.
4. `toby-build` opens `toby-swd-clarity` only when the diff adds a public name or an interface comment. Today the clarity description matches any name or comment in the code being touched.

## Migration

| Kind | Count | Files |
| --- | --- | --- |
| Created | 17 | `toby-bug-fix` SKILL.md and `openai.yaml`, `toby-optimize` SKILL.md, `openai.yaml`, and 5 reference files, 6 reference files split from bodies, `evals/suites/chains.md`, and `evals/suites/bug-fix.md` |
| Moved | 15 | 4 files to `toby-build`, 3 to `toby-refactor`, 7 to `toby-swd-errors`, and `caching.md` to `toby-optimize` |
| Merged | 5 sections | into strategy, modules, testing, and experiment |
| Deleted | 0 in the repo | The 3 retired folder names stay on each of the 4 hosts until `install.sh` removes them, which is 12 folders |
| Edited | 53 | 18 SKILL.md files, 11 `agents/openai.yaml` files, `base/toby.md` and its 6 synced copies, 6 scripts, 4 eval documents, 6 eval suites, and `README.md` |

The six reference files split from bodies are `strategic.md`, `cleanup.md`, `design-note.md`, `design-it-twice.md`, `comments.md`, and `skills-diff.md`. The edits reach six scripts, which are `validate-skills.py`, `trigger-probe.py`, `token-budget.py`, `measure-skills.py`, `install.sh`, and `test-install.sh`. They also reach four eval documents, which are `evals/run.py`, `evals/README.md`, `evals/grading.md`, and `evals/boundaries.md`. The six edited eval suites are `triggering.md`, `feature-dev.md`, `explain.md`, `review.md`, `swd.md`, and `artifacts.md`, which names `toby-feature-dev`.

| Suite | New cases |
| --- | --- |
| `triggering.md` | new directives for P1, P2, N1, N2, N3, and N7, and one case for each of rows 12 to 32 |
| `chains.md`, new | three requests per entry skill, each checking which files the agent opens |
| `bug-fix.md`, new | at least three bug reports, one with a failing test, one with a stack trace, and one whose repair is new behavior |
| `feature-dev.md` | a single-method request, and a strategic request that must open `strategic.md` |
| `explain.md` | a placement question that must open modules, and a diagram request that must not load explain |
| `review.md` | a SKILL.md diff that must open `skills-diff.md` |
| `swd.md` | task 4 pointed at `toby-swd-errors`, and one optimization task |

### Steps in order

Each step ends with a check that must pass before the next step starts.

1. The user approves the trigger eval design below and decides the four changes listed under Practices that move.
2. After the user approves the install, put a two-folder probe in each host's skills folder. One listed skill's body opens a hidden sibling's SKILL.md by path. Run one request per host, then remove the probe. On a host where the agent does not read the sibling file, use the copy fallback for that host. The fallback makes `scripts/sync.sh` copy each method folder into the `references/` of every entry skill that opens it. It copies the whole folder, because each method body opens its own reference files by relative path.
3. Run `scripts/rule-inventory.py` on today's tree and save the output as the baseline for step 5.
4. Build the new tree in a scratch copy of `skills/`. Before writing the Codex hide field, check in the Codex docs which section of `agents/openai.yaml` holds it. Create `toby-bug-fix` and `toby-optimize`, rename the three folders, split each complexity stack file by example, and move the sections in the practices table. Then write the 20 descriptions and add the host fields to the 9 hidden skills.
5. Run `scripts/rule-diff.py` against the step 3 baseline. The check fails when a rule that left a file appears in no other body or reference.
6. Extend `scripts/validate-skills.py` and run it on the scratch tree. Its `ROUTING_GROUPS` table lists the entry chains within the 19,000 ceiling, as the Tokens section says. Its invoke-only check reads the host fields, because the guide no longer has one line per invoke-only skill. One new check fails when a skip clause names a skill that does not exist. Another fails when no entry body opens a method skill.
7. Update `scripts/token-budget.py` with the new names and a layer for opened reference files, and confirm its numbers against the Tokens section.
8. Update `scripts/trigger-probe.py` to show what each host lists, which adds `toby-voice` and `toby-artifact-style` for the first time. Fix the `evals/run.py` triggering prompt, which still says 14 skills, eight prompts, and N1 to N6. Then write the new suite cases.
9. Run the trigger eval below on the scratch tree. The migration stops here if any pass condition fails.
10. Copy the scratch tree into `skills/`, replace the Skill Routing and Work Modes sections in `base/toby.md`, run `scripts/sync.sh`, and update `README.md`.
11. Add a retired-names list to `install.sh` for `toby-feature-dev`, `toby-simplify-code`, and `toby-swd-complexity`. Add a check to `scripts/test-install.sh` that every cross-folder path in each installed tree resolves.
12. Reinstall on the four hosts after the user approves. The reinstall rewrites the Toby block in `~/.claude/CLAUDE.md`, which predates commit 8f238da. Removing the 12 retired folders needs a separate approval.
13. Run one live request per host that should open a hidden method skill.
14. The user updates or removes the `anthropic-skills:toby-*` copies in the claude.ai account.

## Trigger eval

This design needs the user's approval before any run starts.

The eval asks whether each request loads its one entry skill or none, and whether the recommended set fires fewer wrong skills than today's set. Every recorded run measured older descriptions, with no record of the model that wrote it.

| Part | Design |
| --- | --- |
| Arms | Arm 1 shows today's 18 descriptions, including `toby-voice` and `toby-artifact-style`. Arm 2 shows the 11 entry descriptions that Claude Code lists. Arm 3 shows all 20 descriptions, as Kiro lists them and as Codex and Copilot may list them. |
| Guide | Each arm shows its own Skill Routing section above the listing, because hosts load the guide on every turn and no recorded run has measured its routing lines. |
| Prompts | The 32 rows of the request map, plus enough new prompts that each entry skill has 3 should-fire prompts and 2 near-miss prompts. That comes to about 60 prompts, each with its directives written before the run. |
| Held-out set | A second writer drafts 40 percent of the new prompts after the descriptions are frozen. Nobody edits a description to pass a held-out prompt, because the open standard warns that this overfits. |
| Writers | Sonnet 5.5 subagents. Each sees one arm's listing and one prompt, and returns the skills it would load. |
| Samples | 3 per prompt per arm, against the 2 that `evals/run.py` sets as the triggering minimum. |
| Scoring | `python3 evals/run.py compare triggering` scores each sample against the Required, Forbidden, Exactly one of, and Optional directives. |
| Chain mode | Each `chains.md` case gives a Sonnet 5.5 writer one entry body and one request, and asks which files it would open. The scorer compares that list with the row's expected files. |
| Run record | Each run file states the model, the arm, the date, and the description file it used. |
| Size | About 540 writer calls for the three arms, plus about 99 for chain mode. |

Both modes score against written expected sets, so no model judge reads the outputs. Any judge added later runs on Opus 5.5, as the user's eval-models note says.

The recommended set passes when all five conditions hold.

1. Each should-fire prompt loads its entry skill in at least 2 of 3 samples, which meets the open standard's pass rate of above 0.5.
2. At least 90 percent of should-fire prompts pass, which is the figure a third-party copy of Anthropic's guide to building skills gives.
3. No invoke-only skill and no hidden method skill fires in arm 3.
4. Arm 2 has fewer false fires per sample than arm 1 on the 11 shared prompts.
5. In arm 2, at least 90 percent of samples load exactly one entry skill or none, as the row expects.

Two A/B arms run after the main run passes, each with its own approval. The first compares the current "Use it when" wording with "ALWAYS invoke this skill when". It counts activation, false fires, and double fires. The second compares a forced-evaluation hook with no hook in live Claude Code sessions, because the probe script cannot run a hook. Its result applies to Claude Code only, because the research shows hooks for Claude Code alone.

## Rejected ideas

- Five domain skills (domain) lost because the domain set's listing stays at 9,026 characters with them, over Claude Code's 8,000 budget.
- The wording "Trigger only when a loaded Toby skill names it" (domain) lost because no run has tested a description that names another skill as its trigger.
- Retiring every method skill into reference files (request) lost because every method read would cross skill folders. The probe in step 2 tests that read for the method skills that stay.
- `toby-design` as an entry skill (request) lost because `toby-explain` answers the same design questions by opening the method file.
- A listed `toby-docs` skill (request, decision) lost because the `toby-voice` description already lists README and AGENTS.md requests.
- Eight listed decision skills (decision) lost because 7 of the 8 scored false fires in the recorded runs were method skills.
- Bug fixes and speed-ups inside `toby-build` (open) lost because the build body has no cause-finding step and costs over 4,000 tokens for a one-line fix.
- One shared Brownfield Work rule (open) lost because each method's section holds advice for that method alone.
- Dropping `swd` from the testing, experiment, and environment names (decision, request) lost because the rename would add 12 installed folders to retire.
- The bug-fix step that stops after a why answer (decision) lost because `toby-explain` answers that question.
- Shorter invoke-only descriptions (decision) lost because Kiro still reads them, and they quote the requests that must not fire the skill.
- A Haiku arm in the trigger eval (open) lost because the user's eval-models note rules Haiku out of every suite.
- "ALWAYS invoke this skill when" wording lost because its only evidence is secondhand and reports no false-fire rate, so it waits for an A/B arm.
- A forced-evaluation hook by default (research) lost because both published tests used only 4 skills. It also added about 2 seconds per prompt on Sonnet 4.5. The research shows hooks only for Claude Code.
- The `when_to_use` field lost because only Claude Code reads it, so the other three hosts would lose those triggers.
- `paths` globs lost because only Claude Code reads them, and they can only narrow loading for skills that already fire too rarely.
