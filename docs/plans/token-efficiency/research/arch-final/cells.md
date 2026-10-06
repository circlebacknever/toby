Changes what code does in the smallest step that leaves the design at least as good as before. It proves each change with one check run before the edit and again after it. Use it when the user asks to add, build, implement, wire up, or finish a behavior. The behavior can be a feature, a ticket, an endpoint, a method, a screen, a job, or a flag. Skip it for wrong output, which toby-bug-fix covers, and for slow code, which toby-optimize covers. Skip it when behavior stays the same, which toby-refactor covers, and for a throwaway, which toby-swd-experiment covers. Skip it for a one-file edit that copies a pattern already in that file.

before the out-of-scope line or the first edit, and again before the handoff

the work needs a slice cut or a plan step

before the design pass, unless the surrounding code already settles the structure

the design adds or changes a signature

the design adds a module, moves code, or gives a module a new job

a criterion has a failure case, a retry, a timeout, or validation

a criterion states a time or memory budget, or the design adds a cache, a batch, or a queue for speed

before the first edit of each behavior change

module structure or a public API changes

before any command beyond safe inspection

before the handoff, when the diff adds a public name or an interface comment

Fixes behavior that is wrong today. It reproduces the failure, finds the cause at a file and line, fixes that cause, and proves the fix with a run before and after. Use it when the user reports a bug, a crash, an error message, a regression, or wrong output and wants it fixed. Use it when the user pastes a stack trace, or says a build or a test started failing. Skip it for a question about why something fails with no fix asked for, which toby-explain covers. Skip it for a flaky test, which toby-swd-testing covers, and for slow code, which toby-optimize covers.

at the reproduce step, for a failing test's four classes, and at the prove step

the fix would patch around a design problem

the cause is in an error path, a retry, or a validation step

before any command beyond a narrow test

the repair needs new behavior in more than one file, with the reproduction as its first criterion

Makes working code faster or lighter from a measured baseline, with one change per measurement. It covers whether a cache, a batch, a queue, or parallel work is worth what it adds. Use it when the user says code is slow, or asks to speed it up or to cut latency, memory, or query count. Use it when the user asks to add a cache to code that already works. Skip it for new behavior that includes a cache, which toby-build covers, and for wrong output, which toby-bug-fix covers. Skip it for a speed question with no change asked for, which toby-explain covers, and for a throwaway sweep, which toby-swd-experiment covers.

one stack file, from `backend-apis.md` (about 1,210), `databases.md` (about 2,310), `web.md` (about 2,060), and `mobile.md` (about 1,690)

a new cache's get-or-load contract needs a design

at the prove step, for the two-run form

before a benchmark, a profiler, or a heavy suite

Changes how code is arranged or reads and keeps its behavior and tests the same. Use it when the user asks to simplify, tidy, refactor, de-duplicate, extract, split, merge, move, or rename code. Use it to add, fix, or delete comments and docstrings. Skip it when behavior should change, which toby-build, toby-bug-fix, or toby-optimize covers. Skip it when the user wants findings with no edit, which toby-code-review covers.

only names, comments, or docstrings change

the scope is a local cleanup inside changed code

the scope is a split, merge, move, or extraction across files

the scope is an error check for a condition that cannot occur

Keeps tests an executable specification of behavior, and classifies a failing test before anyone edits it. Use it when the user asks to write, rewrite, delete, or weaken a test, raise coverage, update snapshots, or fix a flaky test. Skip it when production code changes too, which toby-build or toby-bug-fix covers. Skip it for a throwaway spike, which toby-swd-experiment covers, and for a run of the suite alone, which toby-swd-environment covers.

Reports the proven risks in a change and edits nothing. Use it when the user asks to review, check, or audit a diff, a PR, a commit, a branch, or the working tree. Use it when the user asks what is wrong with a change. Skip it when the user wants the code changed, which toby-refactor or toby-bug-fix covers. Skip it for a question about how code works, which toby-explain covers.

the diff changes a SKILL.md, a guide, a hook, or an agent config

a finding's fix depends on that method

before any run beyond safe inspection

Answers a question in plain words, then stops, and edits no files. Use it when the user asks why, how, what the difference is, which option fits, or where code should go, on any subject. Use it for "walk me through", "help me understand", and any request for a clear, short, or simple explanation. Skip it when the user asks for a diagram, a chart, or a deck, which toby-artifact-style covers. Skip it when the user wants a fix, which toby-bug-fix covers.

a cold start or an interpretation question

a placement question, answered with its placement note

a question about an error path

a question about a cache or a speed-up

Runs a short, reversible discovery loop while the behavior is still undecided. Use it when the user says spike, prototype, proof of concept, throwaway, try a few values, compare options, tweak settings, or let me test. The word throwaway decides the route even when the request also names retries, timeouts, or tests. Skip it for work the user intends to keep, which toby-build covers. Skip it for starting or stopping a server alone, which toby-swd-environment covers.

after the user picks a behavior

Classifies each command before it runs and asks before any command that changes the user's machine. Use it when the user asks to run a migration or a seed script, or to install a dependency. Use it to start or stop a server, free a port, clear a cache, or run the full test suite. Skip it for a code edit with nothing to run, and for a snapshot update, which toby-swd-testing covers.

Applies Toby's writing rules to prose and runs the voice checker on it. Use it for a commit message, a PR description, a README, an AGENTS.md, a doc, a plan, or a rewrite of any text. Use it when the user says voice, toby voice, check the voice, voice pass, or voice standards, or asks for wording or tone help. Skip it as the first skill for names and comments inside code, which toby-refactor covers.

only when the operating guide is absent from context

`chat.md` (1,282), `code.md` (1,094), or `artifacts.md` (443)

the prose is a module README.md or AGENTS.md

Applies Toby's visual design system to a visual and to the copy inside it. The visual can be a diagram, chart, dashboard, slide deck, HTML or React page, SVG, mockup, or reference card. Use it when the user asks to draw, show, chart, diagram, or build a visual, including a visual that explains something. Skip it for a text answer in chat, which toby-explain covers, and for a game, which only /toby-game starts.

Contains Toby's design pass, run before a change. Entry skills open this file by path. Do not load it from a user request alone.

1,487 tokens. The design pass gains feature-dev's rule that the second approach is the strongest option a competent engineer would pick. "While writing" becomes a pointer to modules checks 3 and 8.

`references/design-note.md` (211) opens for a design note in chat. `references/examples.md` (1,575) opens for a worked case.

Contains Toby's checks for where code goes and when to split or merge modules. Entry skills open this file by path. Do not load it from a user request alone.

3,706 tokens. Checks 3 and 8 gain the text from strategy that puts complexity in the right place.

`references/examples.md` (1,265) opens first. Then one stack file opens to match the code, from `web.md` (4,365), `mobile.md` (2,772), `backend-apis.md` (2,608), `databases.md` (2,756), and `caching.md` (2,410). `replace-the-conditional.md` (1,976) opens for a growing conditional, and `solid.md` (415) opens for a SOLID question.

Contains Toby's procedure for designing a callable surface before its body. Entry skills open this file by path. Do not load it from a user request alone.

2,879 tokens. Step 1 points to modules check 1, and the design-it-twice loop moves to a reference file.

`references/examples.md` (1,090) opens first. `references/design-it-twice.md` (578) opens for a consequential interface or a failed first comment. One stack file opens to match the code, from `web.md` (3,395), `mobile.md` (3,266), `backend-apis.md` (3,817), `databases.md` (3,294), and `caching.md` (2,791). `runtime-config.md` (1,117) opens when code reads deploy config.

Contains Toby's error ladder for deciding how code handles a failure. Entry skills open this file by path. Do not load it from a user request alone.

1,530 tokens. It keeps the intro on special cases and shared state, and Error design with its ladder, limit, hard rules, and degraded path. It also keeps five red flags and the error half of Brownfield Work.

`references/examples.md` (about 700) opens first. Then one stack file opens to match the code, from `backend-apis.md` (about 2,560), `databases.md` (about 1,380), `web.md` (about 1,450), and `mobile.md` (about 1,520).

Contains Toby's rules for names, comments, and docstrings inside code. Entry skills open this file by path. Do not load it from a user request alone.

1,398 tokens. It keeps naming, consistency, proportionality, Brownfield Work, and the red flags.

`references/comments.md` (1,199) opens when the change adds or edits a comment, a docstring, or control flow a reader could misread. `references/examples.md` (1,044) opens for a worked case.

Contains Toby's rules for a module's README.md and AGENTS.md. Entry skills open this file by path. Do not load it from a user request alone.

`references/examples.md` (1,886) opens for backend and frontend examples of both files.

What is the smallest change that delivers this new behavior, and what proves it?

What causes this wrong behavior, and which fix removes the cause?

Which measured change makes this working code fast enough, and is a cache or batch worth its cost?

Which edit improves how this code is arranged or reads, with behavior unchanged?

Which test states this behavior, and what does a failing test mean?

What in this change can break?

What is the answer to this question?

What does the next reversible trial show the user?

Can this command run without asking the user?

Does each sentence of this prose pass the voice rules?

How does this visual look and read under Toby's design system?

Does this change leave the design better or worse?

Which module holds this code and knowledge?

What does this signature expose to callers?

How does this code handle this failure?

Can the next reader guess what this name or comment means?

What do this module's README.md and AGENTS.md need to say now?

The clause that keeps the nearest neighbour out

P1. Add `getAccountBalance(userId)` to `AccountRepository`, reading Redis first, falling back to Postgres, and returning null when the account is missing.

`toby-optimize` skips new behavior that includes a cache.

P2. `invoice.ts` is 1,400 lines and does three jobs. Split it.

`toby-build` skips work where behavior stays the same.

P3. Build the CSV export for the reports page.

strategy, testing, and modules or interfaces when the design adds them

`toby-swd-testing` skips work that changes production code.

P4. Run the pending migration against my local database and re-seed it.

No other entry description lists a migration.

N1. Rename `usr` to `user` in `session.ts`. No other change.

`toby-build` skips work where behavior stays the same.

a method skill when a finding depends on it

`toby-refactor` skips a request for findings.

N3. Try a few values for the retry backoff. Throwaway.

`toby-swd-errors` is hidden, and `toby-optimize` skips a throwaway sweep.

N4. Add a `phone` field the way `email` is done two lines up.

`toby-build` skips a one-file pattern copy.

N5. Build me a browser traffic game in one HTML file.

`toby-game` is hidden, and `toby-artifact-style` skips a game.

N6. Help me brainstorm names for this service.

N7. Clearly and concisely, what is the difference between a mutex and a semaphore?

Tidy the confusing control flow in `parseArgs` and rename its variables.

`toby-code-review` skips a request to change code.

Refactor the checkout service so the discount rules are in one function.

`toby-build` skips work where behavior stays the same.

De-duplicate the two date-formatting helpers into one shared module.

No other entry description lists de-duplicate.

Simplify the error handling in `upload.ts`, because half the catch blocks can never run.

Update the Jest snapshots for the `Header` component.

Update the billing module README after the split.

Add an optional `timeout` parameter to the public `fetchReport()` in the SDK.

Add a `POST /invites` endpoint that emails the invitee.

Start the dev server so I can try the new button by hand.

`toby-swd-experiment` skips starting a server alone.

Make a five-slide deck on the Q3 outage.

none, and the guide's voice line loads `toby-voice`

Explain how a TCP handshake works, with a diagram.

Walk me through how B-tree indexes work.

Move the date helpers into a shared package and export `formatDate`.

Should the retry helper go in `http/client.ts` or in each sync job?

`toby-refactor` needs a request to change code.

Write the commit message for this change.

No other entry description lists a commit message.

The checkout total is one cent off for discounted orders. Fix it.

testing, and strategy when the fix would patch around a design problem

The login page returns a 500 when the email has a plus sign. Fix it.

Why does the orders test fail since yesterday's merge?

`toby-bug-fix` skips a why question with no fix asked for.

The orders page takes 4 seconds to load. Make it faster.

`toby-build` and `toby-bug-fix` skip slow code.

Should we put Redis in front of the product lookup?

`toby-optimize` skips a speed question with no change asked for.

build, `strategic.md`, strategy, modules, interfaces, errors, testing, docs

a bug fix in an error path

a strategic feature with a time budget

a strategic feature with a new public API

Sibling-feature and call-site discovery, greenfield rules, the slice cut, stops 2 and 3, the design lines, the plan document, and resuming half-built work

The "Load `toby-swd-modules` when" and "Load `toby-swd-interfaces` when" bullets

What to look for, Not a simplification, and Idiom or local style

The rule against moving code or changing a signature during cleanup

the local-cleanup scope of `toby-refactor`, while the across-files scope makes those moves after the modules checks

Put complexity in the right place while writing

checks 3 and 8 of `toby-swd-modules`, with a pointer in strategy

The second approach is the strongest option a competent engineer would pick

Decompose by knowledge, step 1 of the interface procedure

a pointer to check 1 of `toby-swd-modules`

The design-it-twice loop, tie resolution, and the redesign step

Error design, five red flags, the error half of Brownfield Work, and the error examples of each stack file

Performance design, Proportionality, four red flags, the performance half of Brownfield Work, the performance examples of each stack file, and `caching.md`

`toby-optimize`, which adds five entry steps

How to review a skills or config diff

a "Prove a change" section in `toby-swd-testing`

the Testing Boundary section of `toby-swd-experiment`

the strategy, testing, and feature-dev descriptions

the `toby-bug-fix` description, whose body adds a cause-finding step

The trigger for any behavior change in production code

the method tables of build, bug-fix, refactor, and optimize

The feature, refactor, and public API triggers

the method tables of build, bug-fix, and refactor

The four tie-break decisions for strategy, modules, interfaces, and complexity

the method tables in the entry bodies

The invoke-only rule for learning, squall, and game

the host fields, the descriptions Kiro reads, and one guide line that asks for the slash command

"walk me through" and "help me understand"

`check the voice` and `voice standards`

the voice description, while the reapply steps stay in the voice body

Tweak settings, compare options, and let me test

A diagram that a question asks for

the explain body, which applied artifact-style

`toby-artifact-style` as the entry skill, with an explain skip clause

`toby-bug-fix` SKILL.md and `openai.yaml`, `toby-optimize` SKILL.md, `openai.yaml`, and 5 reference files, 6 reference files split from bodies, `evals/suites/chains.md`, and `evals/suites/bug-fix.md`

4 files to `toby-build`, 3 to `toby-refactor`, 7 to `toby-swd-errors`, and `caching.md` to `toby-optimize`

into strategy, modules, testing, and experiment

The 3 retired folder names stay on each of the 4 hosts until `install.sh` removes them, which is 12 folders

18 SKILL.md files, 11 `agents/openai.yaml` files, `base/toby.md` and its 6 synced copies, 6 scripts, 4 eval documents, 7 eval suites, and `README.md`

new directives for P1, P2, N1, N2, N3, and N7, and one case for each of rows 12 to 32

three requests per entry skill, each checking which files the agent opens

at least three bug reports, one with a failing test, one with a stack trace, and one whose repair is new behavior

a single-method request, and a strategic request that must open `strategic.md`

a placement question that must open modules, and a diagram request that must not load explain

a SKILL.md diff that must open `skills-diff.md`

task 4 pointed at `toby-swd-errors`, and one optimization task

Arm 1 shows today's 18 descriptions, including `toby-voice` and `toby-artifact-style`. Arm 2 shows the 11 entry descriptions that Claude Code, Codex, and Copilot list. Arm 3 shows all 20 descriptions, as Kiro lists them.

The 32 rows of the request map, plus enough new prompts that each entry skill has 3 should-fire prompts and 2 near-miss prompts. That comes to about 60 prompts.

A second writer drafts 40 percent of the new prompts after the descriptions are frozen. Nobody edits a description to pass a held-out prompt, because the open standard warns that this overfits.

Sonnet 5.5 subagents. Each sees one arm's listing and one prompt, and returns the skills it would load.

3 per prompt per arm, against the 2 that `evals/run.py` sets as the triggering minimum.

`python3 evals/run.py compare triggering` scores each sample against the Required, Forbidden, Exactly one of, and Optional directives.

Each `chains.md` case gives a Sonnet 5.5 writer one entry body and one request, and asks which files it would open. The scorer compares that list with the row's expected files.

Each run file states the model, the arm, the date, and the description file it used.

About 540 writer calls for the three arms, plus about 99 for chain mode.

Part added to the open proposal

`toby-bug-fix` and its drafted body, minus the step that stops after a why answer

`toby-swd-complexity` split into a hidden `toby-swd-errors` and a listed `toby-optimize`

decision for the split, request for the `toby-optimize` entry

The experiment-loop test rules in `toby-swd-experiment`

The second-approach rule in the strategy design pass

A Brownfield Work section in each method skill

The guide line that asks the user to type a slash command

The cross-folder path check in `test-install.sh` and the `sync.sh` copy fallback

Validator checks for a skip clause that names a missing skill and for a method skill that no entry opens

A rule diff before and after the move

"as the first skill" in the voice skip clause

It maps 24 requests to 20 distinct questions, but its risk list says the model must guess where a bare refactor request goes.

Its skip clauses name each neighbour, but 17 listed skills use about 7,500 of the 8,000 listing characters before the claude.ai copies are added.

Every modelled scenario falls or rises by 40 tokens at most, and the strategic feature is 19,741, but resident cost falls only to 7,016.

It lists 20 moves, keeps one copy of each duplicated rule, and adds the cause-finding step that no current body has.

Its decision skills stay model-invocable, so each chain uses the host's normal skill load, and only Kiro keeps the invoke-only descriptions listed.

It creates 17 files, moves 6, merges 5, deletes 7, edits 44, and retires 3 folder names on 4 hosts.

Each of 13 listed skills covers one kind of request, but `toby-design` both answers questions and stores the method files of other skills.

Its third-person descriptions name each neighbour and use 5,668 listing characters, but it lists 13 skills, four more than the open proposal.

Resident cost falls to about 6,513, but the repository method rises by 3,388 and the strategic group passes the 19,000 co-load ceiling.

Sixty-five sections move into reference files in other folders, and six practices change meaning.

Every method read crosses skill folders, which nobody has tested on Codex, Copilot, or Kiro.

It creates 15 files, moves 36, deletes 9, edits 52, and removes up to 40 installed folders.

Entry and method skills both stay listed with an untested "skip it as the first skill" clause, and `toby-caching` repeats complexity's cache question.

The Toby listing stays at 9,026 characters, over the 8,000-character budget at a 200K context.

Resident cost falls to 7,172, but bodies-only loads rise to 9,450 on the repository method and 21,568 on the strategic feature.

Its author built a prototype tree that passed the validator, and a rule diff on that tree found every rule still in a body.

It uses only the name and description fields and today's chain-line form, so it needs no new host feature.

It creates 10 files, moves 15, deletes none, and retires no installed folder.

Nine listed entry skills each match one kind of output. Each of its 28 mapped requests has one entry skill or none.

Its listing is 3,878 characters, but `toby-build` lists feature, fix, and speed-up words in one 629-character description. Anthropic's skill-creator post links broad descriptions to false triggers.

Resident cost falls to 6,263, but the repository method rises by 3,370. Its table's rows add up to 65,634, while its stated sum is 65,056.

Every practice stays in the repo, but seven Brownfield Work sections collapse into one shared rule in two entry skills.

Hiding uses documented fields on three hosts, but opening a hidden skill by sibling path is confirmed only on Claude Code and Codex.

It creates 8 files, moves 7, merges 9 sections, edits 54, and retires 2 folder names on 4 hosts.

Eleven listed entry skills answer eleven questions. Each of the 32 mapped requests has one entry skill or none.

Each entry description states what it does, when to use it, and which named skill covers each skipped case, in a 5,416-character listing.

Resident cost falls to 6,705 and the 11-scenario sum to 64,014, but the repository method rises by 2,485.

Every practice stays in some file, each method keeps its Brownfield Work section, and `toby-bug-fix` adds the cause-finding step.

Hiding uses documented fields on three hosts, and the install path check plus the `sync.sh` copy fallback cover hosts where sibling reads fail.

It creates 17 files, moves 15, merges 5 sections, edits 54, deletes none in the repo, and retires 3 folder names on 4 hosts.