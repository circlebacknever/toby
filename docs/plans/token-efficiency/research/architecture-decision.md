# Toby skills by coding decision

This proposal replaces the 18 Toby skills with 20. Twelve of them each cover one kind of request, such as a bug or a review. The other eight are `toby-swd-*` skills that each make one design decision inside coding work. The descriptions that load on every turn drop from 2,649 to 2,311 tokens. The Claude Code skill listing drops from about 9,900 to about 7,500 characters. Body sizes below are projections from measured sections plus estimated edits. I drafted and measured two pieces, the `toby-bug-fix` body and the guide's routing section.

## Changes

| Change | Skills | Reason |
|---|---|---|
| Split | `toby-swd-complexity` into `toby-swd-errors` and `toby-swd-performance` | The skill answers two questions, each with its own user words, references, and red flags. |
| New | `toby-bug-fix` | Strategy, testing, and feature-dev each claim a bug fix in their descriptions, yet each body omits a step that finds the cause. |
| Rename | `toby-swd-experiment` to `toby-experiment`, and `toby-swd-environment` to `toby-environment` | Both cover a kind of request, so after the rename the `swd` prefix marks only the eight design decisions. |
| Merge text | the design pass, the parameter rule, the interface comment, the test deferral, and the two-run proof | Each of these rules has two or three copies today. The proposal keeps one copy, in the skill that makes the decision. |
| Narrow | the descriptions of strategy, testing, docs, voice, clarity, simplify-code, and interfaces | Each loses the trigger words for requests that another skill answers, and gains a skip clause that names that skill. |
| Hide | `toby-learning`, `toby-squall`, and `toby-game` | `disable-model-invocation: true` takes their descriptions out of the Claude Code listing and stops model invocation on Copilot. |

I checked four other skills for a second decision and kept each one whole.

- `toby-swd-modules` keeps placement, splitting, the conditional ladder, and inheritance, because all four answer which module holds a piece of knowledge.
- `toby-swd-testing` keeps writing tests and classifying failing tests, because both answer what a test protects.
- `toby-swd-clarity` keeps names and comments, because both answer whether the next reader can guess the meaning.
- `toby-feature-dev` keeps its whole workflow, because a `toby-swd-*` skill already makes every design decision its steps need.

## Routing rules

A request skill is a Toby skill whose name has no `swd`. Each one covers one kind of request, such as a review, a bug, or a command. A decision skill is a `toby-swd-*` skill. Each one makes one design decision, such as where code goes. Each skill body lists the other skills it loads, with the step at which each one loads. This proposal calls that list the chain.

1. Toby first loads the one skill whose description matches what the user asked for.
2. A decision skill loads first only when the request asks for that one decision, such as a rename or a module split.
3. In every other case, the first skill's chain says when a decision skill loads.
4. The word throwaway sends the request to `toby-experiment`, whatever else the request names.
5. `toby-voice` loads last on every turn that writes prose, under the guide's voice line, because it is the one skill that checks sentences.

The `swd` prefix puts the role in the name. Claude Code lists a skill by name alone when the listing runs over its budget. In that case the prefix still tells the model which kind of skill it is.

### Guide text

This text replaces the Skill Routing section of `base/toby.md`. The Work Modes line that lists experiment triggers goes, because `toby-experiment`'s description now lists them. The section measures 634 tokens against 624 today. The whole guide drops from 4,744 to 4,705 tokens.

```markdown
## Skill Routing
- These routes stay active whenever the matching skill is installed, including late in a long chat. The skill descriptions are the trigger surface, so this section states only the rules a description cannot state.
- For each request, load the one Toby skill whose description matches what the user asked for. When two descriptions match, state in one sentence the decision the user asked for, and load the skill for that decision. Then load each skill that its body names, at the step that names it.
- Load a `toby-swd-*` skill first only when the request asks for that one decision, such as a rename, a module split, or a new test. In every other case, the first skill's body says when to load it.
- When the user calls the work throwaway, load `toby-experiment`, whatever else the request names. When a description says to skip it for this kind of task, skip it, even when a word in the request matches.
- `toby-voice` stays in force for the rest of the session once it loads. Its rules apply to every reply from that point, in chat and in files, until the user says otherwise. A skill that has to be re-invoked each turn stops being applied around turn six.
- Load `toby-voice` last on every turn that writes a substantive reply, code findings, a commit message, a PR description, docs, comments, a plan, or a generated artifact, before that prose is final. Load its `references/plain-language.md` with it. Load its `references/toby.md` only when the operating guide is absent from context. Do not wait to be asked.
- Treat `voice`, `toby voice`, `check the voice`, `voice pass`, `voice standards`, or a request for a rewrite, banned-phrasing help, tone repair, or wording help as a direct instruction to reload `toby-voice` with `references/plain-language.md`, apply those rules to the recent output, and keep applying them for the rest of the session. Load `references/toby.md` instead only when the operating guide is absent from context.
- Use `toby-learning` only when the user invokes it by name or `/toby-learning`. When a question asks for an answer, use `toby-explain`, however much learning is in the question.
- Use `toby-squall` only when the user invokes it by name or `/toby-squall`.
- Use `toby-game` only when the user invokes it by name or `/toby-game`. A request to make a game, a sim, a toy, or a visualizer does not trigger it.
- When the user names one of those three skills and the host does not let you load it, ask the user to type its slash command.
- State active skills in one short line.
```

## Skill list

Token counts use the repo's ruler, which is characters divided by 4. Body sizes are projections unless marked measured.

### Request skills

#### toby-feature-dev

> Build a new behavior across more than one file, with acceptance criteria, an approved plan, slices, and proof for each slice. Use it when the user asks to build, add, implement, wire up, or finish a feature. The feature can be a ticket, an endpoint, a screen, a job, or a flag. Skip it for a one-file edit that copies a pattern in that file. Skip it for a bug, which `toby-bug-fix` is for, and for a throwaway, which `toby-experiment` is for.

- Body: The body keeps today's running order of mode, size, discovery, criteria, ambiguity, slices, three stops, plan, build, proof, resume, red flags, and the final response. "Design before the plan" shrinks to the design lines the plan records, and tells Toby to run the design pass in `toby-swd-strategy`. "Prove the slice" keeps the per-criterion report and cites the two-run proof in `toby-swd-testing`. A new section lists the chain. The projected body is 5,342 tokens, against 5,437 today.
- References: `references/checks.md` (1,265) opens before the plan's out-of-scope line and again before the handoff. `references/examples.md` (3,360) opens when Toby cuts slices, writes a plan step, or starts greenfield work.
- Chain: `toby-swd-strategy` loads at the design pass. `toby-swd-modules` loads when the design adds a module or gives one a new job, and `toby-swd-interfaces` loads when it adds or changes a signature. `toby-swd-errors` loads when a criterion has a failure case, and `toby-swd-performance` loads when a criterion states a time or memory budget. `toby-swd-testing` loads for each criterion at the build step. `toby-swd-docs` loads at handoff when a module's AGENTS.md or README.md is now wrong. `toby-environment` loads before an ask-list command, and `toby-experiment` loads for one value that reading the code cannot settle.

#### toby-bug-fix (new)

> Fix behavior that is wrong today. Reproduce it in a failing test, find the cause at a file and line, fix it, and prove the fix. Use it when the user reports a bug, a crash, an error message, a regression, or wrong output. Use it when a test started failing, or when the user asks why something is broken. Skip it when the repair is new behavior across files, which `toby-feature-dev` is for, and for a flaky test, which `toby-swd-testing` is for.

- Body: The body has six steps, which are reproduce, classify a failing test, find the cause, stop when the user asked only why, choose the fix, and prove it. A scope rule says the diff holds only the cause and its test. When the fix is in shared code, the rule asks for the callers Toby checked. Five red flags cover a fix with no reproduction, a branch for the one reported input, and a test changed to pass. The other two are a catch block that hides the error and an install or a cache clear before any cause was found. The final response leads with the cause at a file and line. The drafted body measures 629 tokens.
- References: The body opens no reference file. It cites three rules in `toby-swd-testing`, which are the bug-fix test, the four-way classification of a failing test, and the two-run proof.
- Chain: `toby-swd-testing` loads at the reproduce and prove steps. `toby-swd-strategy` loads when the fix would patch around a design problem. `toby-swd-errors` loads when the cause is in an error path, a retry, or a validation step. `toby-feature-dev` takes over when the repair needs new behavior in more than one file, with the reproduction as its first criterion. `toby-environment` loads before an ask-list command.

#### toby-code-review

> Report the risks in a change and stop, with no edits to the code. Use it when the user asks for a code review or a PR review. Use it for a review of a diff, a commit, a branch, or the working tree. Skip it when the user asks for the code to be changed, which `toby-simplify-code` or `toby-bug-fix` is for.

- Body: The body is unchanged except for one pointer, which names `toby-swd-errors` and `toby-swd-performance` in place of `toby-swd-complexity`. The projected body is 3,351 tokens.
- References: `references/smells.md` (4,908) opens during the design pass, for a smell finding.
- Chain: `toby-environment` loads before any run beyond safe inspection. A decision skill loads only when a finding needs that skill's fix wording.

#### toby-simplify-code

> Make working code simpler while its behavior and tests stay the same, and count what each edit removes. Use it when the user asks to simplify, tidy, tighten, de-duplicate, or refactor code inside one module. Skip it when the change moves code between files or modules, which `toby-swd-modules` is for. Skip it when the user wants findings only, which `toby-code-review` is for.

- Body: The body is unchanged except that its pointer to the error ladder names `toby-swd-errors`. The projected body is 1,912 tokens.
- References: `references/smells.md` (2,183) opens for a Fix here or a Flag entry. The full entry for a flagged smell is in `toby-code-review`'s `references/smells.md`.
- Chain: `toby-swd-clarity` loads when the fix is a name or a comment. `toby-environment` loads before a test run wider than one file.

#### toby-experiment (renamed from toby-swd-experiment)

> Run a discovery loop while the behavior is undecided, with one reversible change per round and the state shown to the user. Use it for a spike, a proof of concept, a throwaway version, or a parameter sweep. Use it to compare options, to tweak while the user tests, or to iterate on the user's feedback. The word throwaway takes priority over every other noun in the request. Skip it for work the user intends to keep.

- Body: The body keeps the mode contract, the experiment surface, the disposable markings, the iteration loop, the finish phase, and the failure modes. Its Testing Boundary section gains the experiment-loop rules from `toby-swd-testing`. The projected body is 1,240 tokens.
- References: The skill has no reference files.
- Chain: `toby-environment` loads before a command. `toby-swd-testing` loads after the user chooses a behavior. `toby-swd-docs` loads in the finish phase when the chosen behavior becomes durable inside a module.

#### toby-environment (renamed from toby-swd-environment)

> Sort each command into run freely, run narrowly, or ask first, and track every process Toby starts. Use it when the request is to run a command, start or stop a server, or free a port. Use it to install a dependency, run a migration or a seed script, or clear a cache. Skip it for a code edit with nothing to run, and for a test snapshot update, which `toby-swd-testing` is for.

- Body: The body keeps the command classes, the port rules, long-running processes, heavy repo commands, reporting, and the red flags. One added line points to `toby-swd-testing` for the decision about a snapshot's diff. The projected body is 1,646 tokens.
- References: The skill has no reference files.
- Chain: The body loads no other skill.

#### toby-explain

> Answer a question in plain words in two or three sentences, then stop. Use it when the user asks why something works the way it does, how it works, or what the difference is. Use it for a walkthrough, a trade-off, or a clear, short, or simple explanation on any subject. Skip it when the user asks why something is broken, which `toby-bug-fix` is for. Skip it for names or comments in code, which `toby-swd-clarity` is for.

- Body: The body keeps the answer rules, the subjects, the audience rules, and the no-teaching rule. The Form bullet that restates four plain-language rules becomes a pointer to rules 2, 7, 9, and 10. The citation of the error ladder names `toby-swd-errors`. The projected body is 1,426 tokens.
- References: `references/examples.md` (397) opens when Toby starts cold or answers an interpretation question. `toby-voice`'s `references/plain-language.md` (1,742) always opens.
- Chain: `toby-artifact-style` loads when the user asks for a diagram, an image, or a chart.

#### toby-voice

> Write and check prose in Toby's voice, and run the voice checker on each prose file. Use it when the user asks for a commit message, a PR description, release notes, a plan, or a status update. Use it when the user says voice, toby voice, voice pass, or check the voice, or asks for a rewrite or wording help. Every other Toby skill that writes prose loads it as its last step. Skip it for names and comments in code, which `toby-swd-clarity` is for.

- Body: The body stays as it is, at 1,987 tokens.
- References: `references/plain-language.md` (1,742) always opens. `references/toby.md` (4,751) opens only when the guide is absent from context. `references/plain-language-examples.md` (3,316) opens when a rewrite is not working. `references/examples/banned-writing-patterns.md` (1,684) opens before Toby sends prose. `chat.md` (1,281), `code.md` (1,093), and `artifacts.md` (443) open for the matching kind of output.
- Chain: The body loads no other skill.

#### toby-artifact-style

> Apply Toby's artifact design system to a visual the user asked for, and to the copy inside it. The visual can be an HTML page, an SVG, a diagram, a chart, a dashboard, a slide deck, a mockup, or a reference card. Use it when the user says draw, show, diagram, chart, graph, deck, slides, or mockup. Skip it for a plain answer in chat, which `toby-explain` is for, and for a game or a screen in the user's app.

- Body: The body stays as it is, at 5,452 tokens.
- References: `copy.md` (2,331) opens for copy, `charts.md` (969) for a chart, and `decks.md` (6,010) for a deck. `components.md` (5,404) opens for a component, `layout.md` (2,936) for placing boxes and arrows, `geometry.md` (1,324) for a geometric mark, and `sample-content.md` (1,281) for placeholder data.
- Chain: The body loads no other skill, and the guide's voice line loads `toby-voice` after it.

#### toby-learning, toby-squall, and toby-game

> Teach a subject one step at a time, with a guess from the learner before each answer. Trigger only when the user explicitly invokes this skill by name or with the `/toby-learning` slash command. Skip it for a question that asks for an answer, which `toby-explain` is for.

> Brainstorm by widening one example into the set it belongs to, then offer labelled options. Trigger only when the user explicitly invokes this skill by name or with the `/toby-squall` slash command. Do not trigger on a general request to brainstorm or explore.

> Build a single-file HTML simulation game or toy in Toby's style with the creator. Trigger only when the creator explicitly invokes this skill by name or with the `/toby-game` slash command. Do not trigger on a general request to make a game, a sim, a toy, or a visualizer.

- Frontmatter: Each one adds `disable-model-invocation: true`. Each `agents/openai.yaml` adds `policy: allow_implicit_invocation: false` for Codex.
- Bodies: Squall (998) and game (1,067) are unchanged. Learning's Explanation Form paragraph that restates four plain-language rules becomes a pointer, so learning projects to 3,018 tokens.
- References: Learning opens `interpretation.md` (1,263) in interpretation mode and `retention.md` (1,389) in recall or production mode. Game opens its six references one at a time after the first loop runs. The largest of them is `architecture.md` (1,111). Squall has none.
- Chain: Learning loads `toby-artifact-style` when the learner asks for a diagram. Squall and game load no other skill.

### Decision skills

#### toby-swd-strategy

> Decide before writing whether a change leaves the design better or worse, by sketching two structures and checking both against the next likely change. Use it when the user asks how to structure a change, or asks for a design note that compares two approaches. Use it when the user asks whether to refactor first. `toby-feature-dev` and `toby-bug-fix` load it for their design pass. Skip it for a rename, a formatting pass, a throwaway, and a change whose structure the surrounding code already determines.

- Body: The body keeps the design pass, reactive investment, the test for modifying code, brownfield work, the quick-fix exceptions, the design note, the report, and the anti-patterns. The design pass gains feature-dev's rule that the second approach is the strongest option a competent engineer would pick. "While writing" keeps its first paragraph and points to modules and interfaces for the rest. The projected body is 1,755 tokens.
- References: `references/examples.md` (1,575) opens for side-by-side tactical and strategic versions of one change.
- Chain: `toby-swd-modules` and `toby-swd-interfaces` load for the decisions the design pass produces, as today.

#### toby-swd-modules

> Decide which module holds each piece of code and knowledge, and when to split or merge modules. Use it when the user asks to split, merge, move, or extract code, or to de-duplicate code across files. Use it to choose where new code goes, or to replace a conditional that gains a branch for every new case. Skip it when the question is about one signature, which `toby-swd-interfaces` is for. Skip it for a tidy-up inside one module, which `toby-simplify-code` is for.

- Body: The body keeps the eight checks, the growing-conditional ladder, the placement note, brownfield work, and the red flags. It gains the deploy-config paragraphs from interfaces, because those paragraphs say which module reads the environment. Check 3 points to interfaces for the parameter rule. The projected body is 3,861 tokens.
- References: `references/examples.md` (1,265) opens first. One stack file opens to match the code, from `web.md` (4,364), `mobile.md` (2,771), `backend-apis.md` (2,607), `databases.md` (2,755), and `caching.md` (2,410). `replace-the-conditional.md` (1,976) opens for a growing conditional. `runtime-config.md` (1,116, moved in) opens when code reads deploy config. `solid.md` (415) opens when a finding cites a SOLID principle.
- Chain: `toby-swd-interfaces` loads when an export changes. `toby-swd-docs` loads when a split or a move changes a module root.

#### toby-swd-interfaces

> Design a callable surface before its body, with the interface comment written first and each parameter justified. Use it when the user asks to add or change one function, method, class, hook, repository, or message type. Use it for a component's props, an endpoint contract, or the docstring on a function. Skip it when the question is where code goes, which `toby-swd-modules` is for. Skip it when a new field copies an identical one beside it, and for a feature across files, which `toby-feature-dev` is for.

- Body: The body keeps the general-purpose bias, the eight-step procedure, the brownfield caller sweep, and the red flags. It holds the one copy of the rule to compute a value inside the module before exporting a parameter. The comment test gains clarity's list of what an interface comment states. The deploy-config paragraphs move out to modules. A new section lists the chain. The projected body is 3,347 tokens.
- References: `references/examples.md` (1,089) opens first. One stack file opens to match the code, from `web.md` (3,394), `mobile.md` (3,266), `backend-apis.md` (3,816), `databases.md` (3,294), and `caching.md` (2,791).
- Chain: `toby-swd-testing` loads for the behavior behind the signature. `toby-swd-errors` loads when the contract has a failure case. `toby-swd-performance` loads when the contract adds a cache, a batch, or a queue that the user has not already chosen. `toby-swd-docs` loads when the surface is public.

#### toby-swd-errors (new, from toby-swd-complexity)

> Decide how code handles a failure, trying four options in order, from defining the error away to stopping in a safe state. Use it when the user asks about error handling, retries, timeouts, validation, fallbacks, recovery, or conflicting concurrent writes. Skip it for a throwaway sweep, which `toby-experiment` is for. Skip it for deleting a catch block that can never run, which `toby-simplify-code` is for.

- Body: The body holds the opening paragraphs on special cases and shared mutable state, and the four-step error ladder with its limit, hard rules, and degraded path. It also holds the error half of brownfield work and five red flags. The projected body is 1,485 tokens.
- References: `references/examples.md` (about 700) opens first. One stack file opens to match the code. `backend-apis.md` (about 2,560) covers HTTP categories, gRPC codes, circuit breakers, and shared state. `databases.md` (about 1,380) covers deadlock retry and concurrency control. `web.md` (about 1,450) covers error boundaries and async results, and `mobile.md` (about 1,520) covers offline state and native module errors.
- Chain: The body loads no other skill.

#### toby-swd-performance (new, from toby-swd-complexity)

> Decide whether a speed-up, a cache, a batch, or parallel work is worth the complexity it adds. Measure before and after each optimization. Use it when the user reports that something is slow or asks to make code faster. Use it when the user asks to add a cache, batching, a queue, or concurrency. Skip it for a throwaway parameter sweep, which `toby-experiment` is for, and for the cache's interface, which `toby-swd-interfaces` is for.

- Body: The body holds the three performance rules, the critical-path redesign, proportionality, the performance half of brownfield work, and four red flags. The projected body is 1,148 tokens.
- References: `references/examples.md` (about 260) opens first. One stack file opens to match the code. `backend-apis.md` (about 1,210) covers timeouts and bulk calls, and `databases.md` (about 2,310) covers N+1 queries, bulk writes, indexes, and pooling. `web.md` (about 2,060) covers memoization, virtualization, and rendering, and `mobile.md` (about 1,690) covers lists, images, and bridge batching. `caching.md` (2,844, moved in) opens when a cache is the question.
- Chain: `toby-environment` loads before a benchmark or a profiler run.

#### toby-swd-clarity

> Make names and comments tell the next reader what the code holds and why. Use it when the user asks to rename something, or to add, fix, or delete comments on fields or inside function bodies. Skip it for a docstring on a function's interface, which `toby-swd-interfaces` is for. Skip it for restructuring code, which `toby-simplify-code` is for, and for a clear explanation in chat, which `toby-explain` is for.

- Body: The body keeps naming, comments, consistency, obviousness, proportionality, brownfield work, and the red flags. The interface row of the comment table points to `toby-swd-interfaces`. The projected body is 2,484 tokens.
- References: `references/examples.md` (1,044) opens for worked backend and frontend cases.
- Chain: The body loads no other skill.

#### toby-swd-testing

> Write tests that state behavior at the public interface, and classify a failing test before changing it. Use it when the user asks to write, rewrite, delete, or weaken a test, update a snapshot, or fix a flaky test. `toby-feature-dev`, `toby-bug-fix`, and `toby-swd-interfaces` load it for each behavior they change. Skip it for a rename, a formatting pass, a comment edit, and a throwaway, which `toby-experiment` is for.

- Body: The body keeps every section it has today. A new section, "Prove a change", holds the two-run proof from feature-dev. "Experiment loops" becomes a one-line pointer to `toby-experiment`. The projected body is 1,971 tokens.
- References: The skill has no reference files.
- Chain: `toby-environment` loads before a snapshot update or a full suite run.

#### toby-swd-docs

> Keep two files accurate in each module, AGENTS.md for agents writing code there and README.md for people calling it. Use it when the user asks to write or update a module's README.md or AGENTS.md. Use it when a module split or a public API change makes one of those files wrong. Skip it for comments and docstrings in code, which `toby-swd-clarity` and `toby-swd-interfaces` are for.

- Body: The body stays as it is, at 1,980 tokens.
- References: `references/examples.md` (1,885) opens for backend and frontend examples of both files.
- Chain: The body loads no other skill, and the guide's voice line loads `toby-voice` after it.

## Exclusivity

The 20 skills answer 20 different questions.

| Skill | Question it answers |
|---|---|
| `toby-feature-dev` | What is the smallest multi-file change that delivers this behavior, and what proves it? |
| `toby-bug-fix` | What causes this wrong behavior, and which fix removes the cause? |
| `toby-code-review` | What in this change can break, and for whom? |
| `toby-simplify-code` | Which edit inside this module removes a countable thing with no change in behavior? |
| `toby-experiment` | What does the next reversible trial show the user? |
| `toby-environment` | Can this command run without asking the user? |
| `toby-explain` | What is the answer to this question, in two or three sentences? |
| `toby-voice` | Does each sentence of this prose pass the voice rules? |
| `toby-artifact-style` | How does this visual look and read under Toby's design system? |
| `toby-learning` | What does the learner guess before the next step? |
| `toby-squall` | What wider set does the user's one example belong to? |
| `toby-game` | How does this game's system, comedy, and look follow Toby's style? |
| `toby-swd-strategy` | Does this change leave the design better or worse, and does a refactor come first? |
| `toby-swd-modules` | Which module holds this code and knowledge? |
| `toby-swd-interfaces` | What does this signature and its comment expose to callers? |
| `toby-swd-errors` | How does this code handle this failure? |
| `toby-swd-performance` | Is this speed-up, cache, or batch worth its complexity, by measurement? |
| `toby-swd-clarity` | Can the next reader guess what this name or comment means? |
| `toby-swd-testing` | Which test states this behavior, and what does a failing test mean? |
| `toby-swd-docs` | What do this module's AGENTS.md and README.md need to say now? |

The first eleven rows of the next table are the eleven prompts in `evals/suites/triggering.md`. The suite has only eleven, so the other thirteen rows come from the collisions the research found, plus requests for the new skills. The Today column gives what fired in the recorded runs or what the current descriptions claim. Every proposed row loads one first skill, plus the chain that skill's body states.

| # | Request | First skill | Chain for this request | Today |
|---|---|---|---|---|
| P1 | Add `getAccountBalance(userId)` to `AccountRepository`, reading Redis first and returning null when the account is missing. | `toby-swd-interfaces` | `toby-swd-errors`, `toby-swd-testing` | interfaces, complexity, and testing, and strategy also fired in 4 of 5 runs |
| P2 | Split the 1,400-line `src/billing/invoice.ts`. | `toby-swd-modules` | `toby-swd-docs` when a module root changes | modules, strategy, and docs, and clarity and simplify-code each fired once |
| P3 | Build the CSV export for the reports page. | `toby-feature-dev` | strategy, interfaces, testing | feature-dev, and interfaces, modules, strategy, and testing also fired in the blind run |
| P4 | Run the pending migration and re-seed the local database. | `toby-environment` | none | environment |
| N1 | Rename `usr` to `user` in `src/auth/session.ts`. | `toby-swd-clarity` | none | clarity, and testing also fired in the before run |
| N2 | Review my changes. | `toby-code-review` | none | one of code-review or simplify-code |
| N3 | Try a few retry backoff values. Throwaway. | `toby-experiment` | none | experiment, and complexity also fired in the explain run |
| N4 | Add a `phone` field the way `email` is done two lines up. | none, or `toby-swd-clarity` | none | feature-dev, interfaces, and strategy fired in the before run |
| N5 | Build me a browser traffic game in one HTML file. | `toby-feature-dev`, or none | per feature-dev | feature-dev or none |
| N6 | Help me brainstorm names for this service. | none | none | none |
| N7 | Clearly and concisely, what is the difference between a mutex and a semaphore? | `toby-explain` | none | explain |
| 12 | Tidy the confusing control flow in `parseArgs` and rename its variables. | `toby-simplify-code` | `toby-swd-clarity` for the names | clarity and simplify-code both claim it |
| 13 | De-duplicate the two date-formatting helpers into one shared module. | `toby-swd-modules` | `toby-swd-interfaces` | modules and simplify-code both claim it |
| 14 | Simplify the error handling in `upload.ts`, because half the catch blocks can never run. | `toby-simplify-code` | none | complexity and simplify-code both claim it |
| 15 | Update the Jest snapshots for the Header component. | `toby-swd-testing` | `toby-environment` for the command | environment and testing both claim it |
| 16 | Update the billing module README after the split. | `toby-swd-docs` | none | docs and voice both claim it |
| 17 | Add an optional `timeout` parameter to the public `fetchReport()` in the SDK. | `toby-swd-interfaces` | docs, testing | strategy, interfaces, and docs all claim it |
| 18 | Add a `POST /invites` endpoint that emails the invitee. | `toby-feature-dev` | interfaces, errors, testing | feature-dev and interfaces both claim it |
| 19 | Start the dev server so I can try the new button by hand. | `toby-environment` | none | environment and experiment both claim it |
| 20 | Explain how a TCP handshake works, with a diagram. | `toby-explain` | `toby-artifact-style` | explain and artifact-style both claim it |
| 21 | The checkout total is one cent off for discounted orders, so fix it. | `toby-bug-fix` | testing, and strategy when the fix patches around a design problem | strategy and testing claim it, and feature-dev claims a fix that needs new behavior |
| 22 | Why does the orders test fail since yesterday's merge? | `toby-bug-fix`, stopping after the cause | `toby-swd-testing` | explain and testing both claim it |
| 23 | The orders page takes 4 seconds to load, so make it faster. | `toby-swd-performance` | `toby-environment` for the benchmark | complexity |
| 24 | Write a commit message for the staged changes. | `toby-voice` | none | voice |

## Firing

Each description follows one form, which comes from Anthropic's authoring guide and the agentskills.io description guide.

1. The first sentence says what Toby does under the skill, with an imperative verb.
2. One or two "Use it" sentences list the words a user types for that request.
3. One or two "Skip it" sentences cite the request that the nearest other skill answers, by that skill's name.

The drafts run from 260 to 510 characters, under the 1,024-character limit in Copilot and the open standard. Every sentence passed the voice checker's 25-word ceiling. Five pairs name each other in their skip clauses. N2's pair used this pattern and had exactly one firing in all 5 recorded runs. The five are simplify-code and code-review, simplify-code and modules, modules and interfaces, explain and clarity, and feature-dev and bug-fix.

The set leaves three tactics out.

- The "ALWAYS invoke this skill" template reached 100 percent activation in a secondhand report, but that report gives no false-fire rate. Seventeen skills that must stay apart need that rate, so an eval arm should test the template first.
- A forced-eval hook reached 100 percent with 4 skills on Sonnet 4.5 and added about 2 seconds per prompt. Only Claude Code runs it, and both published tests used 4 skills, so it waits for a Claude Code trial with all 17.
- Only Claude Code documents the `when_to_use` field, so every trigger stays in `description`, which all four hosts read.

The listing budget limits how far the skill count can grow. Claude Code 2.1.283 gives the listing 8,000 characters on a 200K context and 40,000 on a 1M context. The proposed Toby set uses about 7,500 characters. The `anthropic-skills:toby-*` copies synced from claude.ai double that cost, so on a 200K context some Toby skills can lose their descriptions.

## Tokens

The resident cost is the guide plus every description, measured with `scripts/token-budget.py`'s ruler.

| Resident item | Today | Proposed |
|---|---|---|
| Operating guide | 4,744 | 4,705 |
| Descriptions, all skills | 2,649 (18 skills) | 2,311 (20 skills) |
| Total | 7,393 | 7,016 |
| Descriptions in the Claude Code listing | 2,649 | 2,050 (17 skills) |
| Claude Code listing characters, name plus description | about 9,900 | about 7,500 |

The loaded cost counts skill bodies only, as `scripts/token-budget.py` does. The voice body and `plain-language.md` add 3,730 tokens to any prose turn in both sets.

| Scenario | Skills today | Today | Skills proposed | Proposed |
|---|---|---|---|---|
| a question, answered | explain | 1,476 | explain | 1,426 |
| a rename | clarity | 2,554 | clarity | 2,484 |
| a command or migration | environment | 1,636 | environment | 1,646 |
| review my changes | code-review | 3,341 | code-review | 3,351 |
| a throwaway spike | experiment | 1,200 | experiment | 1,240 |
| one method on a repository | interfaces, complexity, testing | 7,909 | interfaces, errors, testing | 6,803 |
| split a module | modules, strategy, docs | 7,512 | modules, docs | 5,841 |
| a feature, tactical | feature-dev, strategy, testing | 9,209 | feature-dev, strategy, testing | 9,068 |
| a feature, strategic | feature-dev and six swd skills | 20,858 | feature-dev, strategy, modules, interfaces, errors, testing, docs | 19,741 |
| learning, invoked | learning | 3,083 | learning | 3,018 |
| a visual artifact | artifact-style | 5,452 | artifact-style | 5,452 |
| a bug fix, not in the script today | strategy, testing | 3,772 | bug-fix, testing | 2,600 |

The proposed range is 1,240 to 19,741 tokens. A strategic feature with a time or memory budget also loads performance, which makes 20,889 tokens. A bug fix that patches around a design problem also loads strategy, which makes 4,355 tokens. The largest body is artifact-style at 5,452, under the validator's 6,000 ceiling. If all eight decision skills load together, they total 18,031 tokens, under the validator's 19,000 co-load ceiling.

The split costs 67 tokens of repeated opening text, because errors (1,485) and performance (1,148) together exceed complexity (2,566). In the modelled scenarios only one half loads, so each of those turns loads fewer tokens than it did with complexity.

## Practices that move

Every practice in the current skills survives. The 20 practices below move to another file or to another part of the same skill.

1. The error ladder, its limit, its hard rules, the degraded-path rule, the shared-state paragraph, and five red flags move from `toby-swd-complexity` to `toby-swd-errors`.
2. The three performance rules, the critical-path redesign, proportionality, and four red flags move from `toby-swd-complexity` to `toby-swd-performance`.
3. The complexity references split by example. Errors gets examples 1, 2, and 4 of `examples.md`, and backend examples 1, 2, 4, and 6. It also gets database examples 2 and 6, and the first two web and mobile examples. Performance gets the rest and all of `caching.md`, and each cheat sheet splits by line.
4. The instruction to sketch two approaches, with the second as the strongest option a competent engineer would pick, moves from feature-dev's "Design before the plan" into the strategy design pass.
5. The rule to compute a value inside the module before exporting a parameter has copies in strategy, in modules check 3, and in interfaces. Interfaces keeps it, and the other two point to it.
6. Strategy's paragraph on deep modules and small functions repeats modules check 7, so modules keeps it and strategy points to it.
7. The deploy-config paragraphs and `references/runtime-config.md` move from interfaces to modules, and `solid.md` updates its pointer.
8. Clarity's paragraph on what an interface comment states, and on writing it before the body, moves into the interfaces comment test.
9. Testing's "Experiment loops" rules move into `toby-experiment`'s Testing Boundary section.
10. The two-run proof moves from feature-dev's "Prove the slice" into a new testing section, so feature-dev and bug-fix cite one rule.
11. The "bug fix whose repair is new behavior" trigger moves from feature-dev's description into bug-fix's handover step.
12. The experiment triggers in the guide's Work Modes line move into `toby-experiment`'s description.
13. The guide's tie-break line maps four decisions to four skills. That mapping moves into the opening sentence of each skill's description. The step that states the decision in one sentence stays in the guide.
14. The four plain-language rules that explain and learning restate leave both bodies, because rules 2, 7, 9, and 10 in `plain-language.md` already state them.
15. Voice's description drops code findings, a doc, a comment, and any generated artifact, because the guide's voice line already loads voice for each of them.
16. Learning's four quoted non-trigger questions and squall's three quoted phrases shrink to one clause in each description. The guide's learning line also sends answer-seeking questions to explain. Game's style summary leaves its description, because the game body states it.
17. Testing's trigger for any behavior change in production code moves from its description into the chains of feature-dev, bug-fix, and interfaces.
18. Strategy's triggers for a feature, a bug fix, a refactor, and a public API change leave its description. Feature-dev and bug-fix load strategy in their chains. A refactor request now matches simplify-code or modules, and a public API change matches interfaces and docs.
19. The snapshot-update trigger moves from environment's description to testing's description.
20. Clarity's description triggers for docstrings and for confusing control flow move to interfaces and simplify-code, and clarity's Obviousness section stays in its body.

## Hosts

`scripts/install.sh` copies every `skills/toby-*` folder into one folder per host, so the new and renamed folders install with no script change.

| Need | Codex | Claude Code | Copilot | Kiro |
|---|---|---|---|---|
| Reads `name` and `description` | yes | yes | yes | yes |
| Loads a chained skill | reads the sibling `SKILL.md` | Skill tool | reads the sibling `SKILL.md` | reads the sibling `SKILL.md` |
| Hides an invoke-only skill | `policy: allow_implicit_invocation: false` in `agents/openai.yaml` | `disable-model-invocation: true` | `disable-model-invocation: true` | not found, so the description sentence stays |
| Description limit | not found | 1,536 characters with `when_to_use` | 1,024 characters | not found |

The Codex field comes from the curated `migrate-to-codex` notes and from installed plugins under `~/.codex`. Those notes say Codex has no equivalent of `disable-model-invocation`. A Kiro custom agent loads only the skills it lists, so a chain to an unlisted skill fails there. No run has tested a chain on Codex, Copilot, or Kiro.

## Migration

| Kind | Count | Files |
|---|---|---|
| Created | 17 | `toby-bug-fix` (2), `toby-swd-errors` (7), `toby-swd-performance` (7), and `evals/suites/bug-fix.md` |
| Moved | 6 | `caching.md` to performance, `runtime-config.md` to modules, and the 2 files in each renamed folder |
| Merged into | 5 | the strategy, testing, experiment, modules, and interfaces SKILL.md files |
| Deleted | 7 | `toby-swd-complexity`'s SKILL.md, `agents/openai.yaml`, and 5 split references |
| Edited | 44 | 17 SKILL.md files, 5 `agents/openai.yaml` files, 2 references, 7 guide copies, 6 scripts, 6 eval files, and the repo README |

The five merge targets are among the 17 edited SKILL.md files. The 7 guide copies are `base/toby.md` and 6 of the 7 files that `scripts/sync.sh` writes. The output style has no routing section, so it stays the same. The edits reach six scripts, which are `validate-skills.py`, `token-budget.py`, `trigger-probe.py`, `measure-skills.py`, `install.sh`, and `test-install.sh`. They also reach six eval files, which are `suites/triggering.md`, `suites/swd.md`, `boundaries.md`, `README.md`, `grading.md`, and `run.py`. The baselines and the gold labels under `evals/` stay as dated records.

Three eval suites need new cases.

- `evals/suites/triggering.md` needs rows 12 to 24 above as new probes, with errors and performance forbidden on N3. P1's required set becomes interfaces, errors, and testing, and P2's becomes modules and docs.
- `evals/suites/swd.md` needs task 4 pointed at `toby-swd-errors`, and one new performance task.
- `evals/suites/bug-fix.md` is new and needs at least three cases, which is the minimum in Anthropic's authoring guide.

`scripts/trigger-probe.py` has to list all 20 skills, which adds voice and artifact-style for the first time. `evals/run.py` still says 14 skills and N1 to N6, so its prompt needs the new counts. Each run file needs the name of the model that wrote it. The suite needs 2 samples per prompt, which is the minimum that `run.py` sets.

`install.sh` never deletes a folder that the repo no longer has. The old `toby-swd-complexity`, `toby-swd-experiment`, and `toby-swd-environment` folders would stay on all four hosts with their old descriptions. The installer needs a list of retired names. Removing those 12 folders needs the user's approval. The `anthropic-skills:toby-*` copies in the claude.ai account need the same update, which only the user can make.

## Risks

- The word refactor goes to simplify-code inside one module and to modules across files. A request that names no files, such as "refactor the checkout service so the discount rules are in one function", leaves the model to guess.
- A test that started failing goes to bug-fix, and a flaky test goes to testing. The model has to judge flakiness from the request.
- Errors still matches "retry backoff" and "timeouts" in N3. The throwaway skip clause and the guide line guard it, as they do today. The explain run recorded one false fire there.
- "Tweak while the user tests" in experiment's description is close to row 19, which asks to start a server for a manual try.
- With `disable-model-invocation`, Claude Code and Copilot load the three invoke-only skills from the slash command only. A user who types the skill's name in a sentence gets the guide's request to type the slash command.
- Every body size except bug-fix is a projection from measured sections plus estimated edits. These descriptions still need a triggering run. The recorded runs also omit the model that wrote them.
