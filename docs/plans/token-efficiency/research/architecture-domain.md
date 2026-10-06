# Domain split proposal

This proposal grows the Toby set from 18 to 23 skills and lowers the resident cost from 7,393 to 7,172 tokens. The 15 domain reference files move out of `toby-swd-modules`, `toby-swd-interfaces`, and `toby-swd-complexity` into five new domain skills. Every other skill gets a new description, so each request matches one entry skill. The agent loads a domain skill only when a loaded skill's body names it. No recorded run has tested that path yet.

I built the proposed tree in `scratchpad/proto/skills` with `scratchpad/proto/build.py` and measured it with the repo's scripts. The validator's skill, skip-clause, budget, reference, and duplicate-sentence checks report 0 errors and 0 warnings on that tree. I changed no repo file.

## Terms

An entry skill is the one skill whose description matches the user's request. A chain is the list of skills that an entry skill's body tells the agent to load next. A method skill is one of the seven toby-swd design skills, which are strategy, modules, interfaces, complexity, clarity, testing, and docs. A domain skill contains the worked examples for one kind of code, such as React front ends or caches.

## Loading

The agent loads skills in three steps.

1. The agent reads the 23 descriptions and loads the one entry skill whose description matches the request.
2. The agent loads each method skill that the entry skill's body names for this task.
3. When the agent uses `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-complexity`, or `toby-code-review` on one of five kinds of code, that skill's body names the matching domain skill. The agent loads that domain skill as well.

The agent reads the one section of the domain skill written for the method skill whose body named it. The agent opens that section's example file only when the section's table does not settle the decision. Today each method skill tells the agent to open one domain file every time.

The guide's Skill Routing section still contains the voice lines, the three invoke-only lines, and the throwaway rule. This proposal changes its first line and its tie-break line. The first line now says that the 23 descriptions and the skills each body names are the whole trigger surface. The proposal replaces the four-decision tie-break line with this line.

> Load the one skill whose description matches the request, then load each skill its body names for this task. When two descriptions still match, state the decision in one sentence and load the skill written for that decision.

The guide line that routes `toby-voice` to every reply stays, so the guide is the one place that states the `toby-voice` chain.

## Skills

The descriptions below are the exact text I measured. Each one is 591 characters or fewer. Every sentence in them has 25 words or fewer. The proposal edits 7 of the 18 existing bodies. The 11 unchanged bodies are explain, experiment, environment, voice, artifact-style, strategy, clarity, docs, learning, squall, and game.

| Group | Skills | Fires from |
|---|---|---|
| Entry | feature-dev, code-review, simplify-code, explain, experiment, environment, voice, artifact-style | the user's words |
| Method | strategy, modules, interfaces, complexity, clarity, testing, docs | the user's words for their one question, or a parent body |
| Invoke-only | learning, squall, game | the skill name or slash command |
| Domain | web, mobile, backend-apis, databases, caching | a parent body, or the skill name |

### toby-feature-dev

> Build a feature or fix a bug as the smallest change that leaves the design no worse, with evidence that it works. Use it when the user asks to build, add, implement, wire up, finish, or fix a behavior they intend to keep. Examples are a ticket, an endpoint, a screen, a job, and a flag. Skip it for a one-file edit that copies a pattern already in that file, and for a throwaway, which toby-swd-experiment covers. Skip it for a review, which toby-code-review covers, and for a cleanup of working code, which toby-simplify-code covers.

Its question asks what done means for a change and in which slices the change ships. Its body still contains today's mode, sizing, criteria, slices, stops, plan, and handoff. The proposal adds one line to its body. That line names `toby-swd-complexity` for an error path, retry, cache, or optimization, and `toby-swd-docs` for a structure or public API change. The agent opens `references/checks.md` before the plan's out-of-scope line and before the handoff. It opens `references/examples.md` to cut slices or write plan steps. The chain is strategy and testing for every durable change, plus modules, interfaces, complexity, and docs when the design needs them.

### toby-code-review

> Report the real risks in a change and edit nothing. Use it for code review, PR review, diff review, commit review, or working-tree review, covering bugs, regressions, missing tests, security issues, and repo-rule breaks. Skip it when the user wants the code changed, which toby-simplify-code or toby-feature-dev covers.

Its question asks what a change breaks. Its body still contains the four passes and the evidence lines. In the design pass, a new line names the domain skill for the changed code. The agent loads that skill only when a finding depends on how that kind of code is built. The agent opens `references/smells.md` when a design finding matches a smell entry.

### toby-simplify-code

> Make working code simpler and keep its behavior and tests the same. Use it when the user asks to simplify, tidy, tighten, de-duplicate, or refactor code inside its current files. It also covers confusing control flow and catch blocks that can never run. Skip it for findings with no edit, which toby-code-review covers, and for moving code between files, which toby-swd-modules covers.

Its question asks which simpler code keeps the same behavior. The proposal adds one line to its body, which names `toby-swd-clarity` for a rename or a comment edit. The agent opens `references/smells.md` when a candidate matches a design smell.

### toby-explain

> Answer a question in plain words and stop. Use it when the user asks why or how something works, what the difference is, or for a walkthrough, a rationale, or a trade-off. Use it whenever the user asks for a clear, concise, short, simple, or direct explanation. Use it for any subject, including code, math, science, language, literature, and medicine. When the question asks for a diagram, load toby-artifact-style as well. Skip it for names and comments inside code, which toby-swd-clarity covers. Skip it for a decision to change the user's code, which the matching toby-swd skill covers.

It covers the question the user asked. The agent opens `references/examples.md` when an explanation needs a worked model, and `toby-voice`'s `references/plain-language.md` every time. Its body names no domain skill, because a two-sentence answer does not need a 900-token table.

### toby-swd-experiment

> Run a loop of small reversible changes while the behavior is still undecided. Use it for a spike, a proof of concept, a throwaway version, a parameter sweep, comparing options, or tweaking settings while the user tests. When the request says throwaway, use it whatever other nouns the request contains, including retries, timeouts, and tests. Skip it for work the user intends to keep, which toby-feature-dev covers, and for starting a server to try a finished change, which toby-swd-environment covers.

Its question asks which candidate behavior the user picks. It has no reference files, and its body already names `toby-swd-environment` for commands.

### toby-swd-environment

> Treat the machine and everything on it as the user's. Use it when a task runs a command, starts or stops a process, takes a port, or installs a dependency. Use it as well for a migration, a seed script, a cache clear, or a settings or credential edit, whichever Toby skill named it. Skip it for a code edit with nothing to run, and for choosing which snapshots to accept, which toby-swd-testing covers.

Its question asks whether a command may run and how narrowly. It has no reference files.

### toby-voice

> Apply Toby's writing rules to prose. Use it when the user says voice, toby voice, check the voice, voice pass, or voice standards. Use it for a rewrite, tone repair, or wording help. Load it before finalizing any reply, finding, commit message, PR description, doc, plan, or artifact. Skip it for names and comments inside code, which toby-swd-clarity covers.

Its question asks how prose is worded. The agent opens `references/plain-language.md` every time, `references/toby.md` when the operating guide is absent, and `references/plain-language-examples.md` when a rewrite fails. It also opens the file in `references/examples/` that matches the output type. The new description has no skip for explanations, because that skip conflicted with the guide line that routes voice to every reply.

### toby-artifact-style

> Apply Toby's design system to a visual artifact and the copy inside it. A visual artifact is an HTML or React page or widget, an SVG, an image, a diagram, a chart, or a dashboard. It can also be a slide deck, a mockup, or a printable card. Use it when the user asks to draw, show, sketch, chart, or build a visual, and when toby-explain or toby-learning draws one. Skip it as the first skill for a question, even one that asks for a diagram, which toby-explain covers. Skip it for a browser game, which toby-feature-dev covers.

Its question asks how a visual looks. The agent opens `references/copy.md` for copy, `references/charts.md` for a chart, `references/decks.md` for a deck, and `references/components.md` for a component. It opens `references/layout.md` to place boxes and arrows, `references/geometry.md` for a geometric mark, and `references/sample-content.md` for placeholder data.

### toby-swd-strategy

> Decide whether a change leaves the design better or worse before it is written. Use it when the user asks which of two designs to take or whether to refactor before a change. Use it as well when toby-feature-dev or toby-swd-modules names it. Skip it for where code goes, which toby-swd-modules covers, and for what a signature exposes, which toby-swd-interfaces covers. Skip it for a rename, a formatting pass, or a throwaway spike.

Its question asks whether the design gets better or worse. The current body already names modules and interfaces for the decisions it reaches. The agent opens `references/examples.md` for the tactical and strategic versions side by side.

### toby-swd-modules

> Decide which module code goes in and which module defines each piece of knowledge. Use it when the user asks to split, merge, move, or place code, or to refactor so one rule is defined in one place. Skip it for what one signature exposes, which toby-swd-interfaces covers, and for a cleanup inside the current files, which toby-simplify-code covers. Skip it as the first skill for a feature, which toby-feature-dev covers.

Its question asks where code goes. The proposal removes the five domain lines from its body and adds a last section. That section names `toby-swd-strategy` when a boundary that other code calls moves, and `toby-swd-docs` when module structure changes. It also names the domain skill for the code being placed. The agent opens `references/examples.md` first, `references/replace-the-conditional.md` for a conditional that grows per case, and `references/solid.md` for a SOLID question. It opens the domain skill's `references/placement.md` when the Placement table does not settle the placement.

### toby-swd-interfaces

> Design a callable surface before its body is written. Use it when the user asks to add or change one function, method, class, hook, component's props, endpoint contract, or message format. Skip it for where code goes, which toby-swd-modules covers, and for a field added beside an identical one. Skip it as the first skill for a whole feature, which toby-feature-dev covers.

Its question asks what a signature exposes. The proposal removes the five domain lines from its body and adds a last section. That section names `toby-swd-complexity` for an error path, fallback, retry, or cache, and `toby-swd-testing` for a behavior change. It also names `toby-swd-docs` for a public API change and the domain skill for the contract. The agent opens `references/examples.md`, and `references/runtime-config.md` for deploy config. It opens the domain skill's `references/contracts.md` when the Contracts table does not settle the design.

### toby-swd-complexity

> Decide whether an error path, a retry, a cache, or an optimization is worth what it costs. Use it when the user asks whether to add or remove one of those, or to fix a slow path. Skip it as the first skill when a new method or feature contains one, which toby-swd-interfaces or toby-feature-dev covers. Skip it for a throwaway sweep, which toby-swd-experiment covers, and for deleting catch blocks that can never run, which toby-simplify-code covers.

Its question asks whether added code is worth its cost. The proposal removes the five domain lines from its body and adds a last section. That section names `toby-swd-testing` for a behavior change and the domain skill for the code. The agent opens `references/examples.md`, and the domain skill's `references/cost.md` when the Cost table does not settle the decision.

### toby-swd-clarity

> Make names, comments, and docstrings in code readable to the next maintainer. Use it when the user asks to rename an identifier, or to add, fix, or remove code comments and docstrings. Skip it for restructuring control flow, which toby-simplify-code covers, and for an explanation in chat, which toby-explain covers. Skip it for a README or AGENTS.md, which toby-swd-docs covers.

Its question asks what a thing is called and what its comment says. The agent opens `references/examples.md` for worked cases.

### toby-swd-testing

> Keep tests an executable specification of behavior. Use it when the user asks to write, fix, delete, weaken, or snapshot a test. Use it as well when another loaded Toby skill names it for a behavior change. Skip it for a change that leaves behavior the same, such as a rename or a formatting pass. Skip it for a throwaway spike, which toby-swd-experiment covers.

Its question asks which test specifies a behavior. The proposal adds one line to its body, which names `toby-swd-environment` before a snapshot update or any test command wider than one file. It has no reference files.

### toby-swd-docs

> Keep a module's AGENTS.md, for agents, and README.md, for people, accurate. Use it when the user asks to write or update one of those files. Use it as well when another loaded Toby skill names it after a change to module structure or a public API. Skip it for code comments and docstrings, which toby-swd-clarity covers.

Its question asks what a module's README.md or AGENTS.md says. The agent opens `references/examples.md` for backend and frontend examples of both files.

### toby-learning

> Teach a subject by working through it with the learner at the keyboard. Trigger only when the user explicitly invokes this skill by name or with /toby-learning. Do not trigger on a question that asks for an answer, such as why is this slow, walk me through, or help me understand. Use toby-explain for those questions.

Its question asks how the learner works through a subject. The agent opens `references/interpretation.md` for a subject with no single right answer and `references/retention.md` for recall and language practice.

### toby-squall

> Brainstorm by widening one example into the larger set it belongs to. Trigger only when the user explicitly invokes this skill by name or with /toby-squall. Do not trigger on help me think through this, let's explore, brainstorm with me, or other general brainstorming requests.

Its question asks which larger set one example belongs to. It has no reference files.

### toby-game

> Build a single-file HTML simulation game or toy in Toby's style with the creator. Trigger only when the creator explicitly invokes this skill by name or with /toby-game. Do not trigger on a general request to make a game, sim, toy, visualizer, or simulation, or on a game mentioned in passing.

Its question asks how an invoked game gets built. The agent opens the reference file that the "What this prevents" list names for the feedback, such as `references/gameplay.md` for an unfair game.

### toby-web

> This skill contains the React, Solid, and Svelte examples for the toby-swd design skills. Trigger only when a loaded Toby skill names it for that code, or when the user invokes it by name. Skip it for React Native, which toby-mobile covers.

Its 920-token body has three sections. The Placement section contains the framework idiom table from today's `toby-swd-modules/references/web.md`. The Contracts section contains the six-row table from `toby-swd-interfaces/references/web.md`. The Cost section contains the five-row table from `toby-swd-complexity/references/web.md`. The agent opens `references/placement.md`, `references/contracts.md`, or `references/cost.md` when that section's table does not settle the decision. Those three files are today's three `web.md` files without their last sections. Together they contain 13 worked examples.

### toby-mobile

> This skill contains the React Native examples, with iOS, Android, and Flutter notes, for the toby-swd design skills. Trigger only when a loaded Toby skill names it for that code, or when the user invokes it by name. Skip it for web React, which toby-web covers.

Its 837-token body contains the platform notes from today's modules and interfaces `mobile.md` files and the seven-row cost table from complexity. The agent opens its three example files, which contain 13 worked examples, under the same rule as `toby-web`.

### toby-backend-apis

> This skill contains the HTTP, gRPC, and service examples in Java, Kotlin, Go, and TypeScript for the toby-swd design skills. Trigger only when a loaded Toby skill names it for that code, or when the user invokes it by name. Skip it for queries and transactions, which toby-databases covers.

Its 872-token body contains the three-stack pattern table from modules, the six-row comment-test table from interfaces, and the seven-row cost table from complexity. The agent opens its three example files, which contain 14 worked examples, under the same rule as `toby-web`. `toby-swd-interfaces` also names it for the interface-segregation rule on a backend service.

### toby-databases

> This skill contains the repository, query, schema, migration, and transaction examples for the toby-swd design skills. Trigger only when a loaded Toby skill names it for that code, or when the user invokes it by name. Skip it for running a migration, which toby-swd-environment covers.

Its 828-token body contains the cross-cutting notes from modules, the six-row data-layer table from interfaces, and the seven-row cost table from complexity. The agent opens its three example files, which contain 15 worked examples, under the same rule as `toby-web`.

### toby-caching

> This skill contains the cache examples for the toby-swd design skills, covering whether to add a cache, where it goes, its contract, and stampedes. Trigger only when a loaded Toby skill names it for that code, or when the user invokes it by name.

Its 828-token body contains the five-layer placement table from modules, the six-row contract table from interfaces, and the six-row cost table from complexity. The agent opens its three example files, which contain 13 worked examples, under the same rule as `toby-web`.

## Request map

Each request below matches one entry skill's description. That entry skill's body names the rest of the chain. Rows 1 to 11 are the 11 prompts in `evals/suites/triggering.md`. Rows 12 to 22 are the collision cases from the description audit in the task. Rows 23 to 27 are new cases for the domain skills and for bug fixes.

| # | Request | Entry skill | Chain the entry names | Must not load first |
|---|---|---|---|---|
| 1 | P1. Add `getAccountBalance(userId)` to `AccountRepository`, reading Redis first, falling back to Postgres, and returning null when the account is missing. | toby-swd-interfaces | toby-swd-complexity, toby-swd-testing, toby-databases, toby-caching | toby-swd-complexity, toby-swd-testing, toby-feature-dev |
| 2 | P2. Split the 1,400-line `src/billing/invoice.ts`. | toby-swd-modules | toby-swd-strategy, toby-swd-docs, toby-backend-apis | toby-simplify-code, toby-swd-clarity |
| 3 | P3. Build the CSV export for the reports page. | toby-feature-dev | toby-swd-strategy, toby-swd-testing, then toby-swd-interfaces for the export endpoint, which names toby-web and toby-backend-apis | toby-simplify-code, toby-code-review |
| 4 | P4. Run the pending migration against my local database and re-seed it. | toby-swd-environment | none | toby-databases, toby-swd-strategy |
| 5 | N1. Rename `usr` to `user` in `src/auth/session.ts`. | toby-swd-clarity | none | toby-swd-strategy, toby-swd-testing |
| 6 | N2. Review my changes. | toby-code-review | the domain skill for the diff, in the design pass only | toby-simplify-code |
| 7 | N3. Try a few retry backoff values. Throwaway. | toby-swd-experiment | toby-swd-environment to run the sweep | toby-swd-complexity, toby-swd-testing |
| 8 | N4. Add a `phone` field to `ContactForm` the way `email` is done. | none | none | toby-feature-dev, toby-swd-interfaces, toby-web |
| 9 | N5. Build me a browser traffic game in one HTML file. | toby-feature-dev, or none | toby-swd-strategy, toby-swd-testing | toby-game, toby-artifact-style, toby-swd-experiment |
| 10 | N6. Help me brainstorm names for this service. | none | none | toby-squall |
| 11 | N7. Clearly and concisely, what is the difference between a mutex and a semaphore? | toby-explain | none | toby-swd-clarity, toby-learning |
| 12 | Tidy the confusing control flow in `parseArgs` and rename its variables. | toby-simplify-code | toby-swd-clarity for the renames | toby-swd-clarity, toby-code-review |
| 13 | Update the Jest snapshots for the Header component. | toby-swd-testing | toby-swd-environment to run the update | toby-swd-environment |
| 14 | Update the billing module README after the split. | toby-swd-docs | toby-voice, through the guide | toby-voice |
| 15 | Add an optional timeout parameter to the public `fetchReport()` in the SDK. | toby-swd-interfaces | toby-swd-complexity, toby-swd-testing, toby-swd-docs | toby-swd-strategy |
| 16 | Add a POST /invites endpoint that emails the invitee. | toby-feature-dev | toby-swd-strategy, toby-swd-testing, toby-swd-interfaces, then toby-backend-apis | toby-swd-interfaces |
| 17 | Start the dev server so I can try the new button by hand. | toby-swd-environment | none | toby-swd-experiment |
| 18 | Make a five-slide deck on the Q3 outage. | toby-artifact-style | toby-voice, through the guide | toby-explain |
| 19 | Explain how a TCP handshake works, with a diagram. | toby-explain | toby-artifact-style | toby-artifact-style, toby-learning |
| 20 | De-duplicate the two date-formatting helpers into one shared module. | toby-swd-modules | toby-swd-strategy | toby-simplify-code |
| 21 | Simplify the error handling in `upload.ts`, because half the catch blocks can never run. | toby-simplify-code | none | toby-swd-complexity |
| 22 | Walk me through how B-tree indexes work. | toby-explain | none | toby-learning, toby-databases |
| 23 | The React Native orders screen stutters when it scrolls 2,000 rows. | toby-swd-complexity | toby-mobile | toby-web, toby-feature-dev |
| 24 | Should we put Redis in front of the product lookup? | toby-swd-complexity | toby-caching | toby-explain, toby-swd-interfaces |
| 25 | Add a `useCart` hook that returns the items and an `addItem` function. | toby-swd-interfaces | toby-swd-testing, toby-web | toby-feature-dev |
| 26 | Why does this `useEffect` run twice in development? | toby-explain | none | toby-web |
| 27 | Fix the crash when the cart is empty. | toby-feature-dev | toby-swd-strategy, toby-swd-testing | toby-swd-strategy, toby-swd-testing |

No two skill entries above state the same question. A domain skill has no question of its own, because it contains the examples that a method skill applies to one kind of code. `toby-caching` and `toby-swd-complexity` both mention whether to add a cache. The rule for that decision is in `toby-swd-complexity`. The Cost table in `toby-caching` gives examples of that rule for caches.

Two requests have more than one correct result. In row 9, the agent may load `toby-feature-dev` or no skill, as the suite allows today. The request "Refactor the checkout service so the discount rules are in one function" goes to `toby-swd-modules` when the rules are in several files. It goes to `toby-simplify-code` when they are in one file.

## Firing

Each description opens with an imperative that states the job. Its "Use it when" sentences give triggers in the words a user types. Its skip sentences follow the pattern "Skip it for X, which Y covers". Anthropic's authoring guide asks for what the skill does and when to use it, within 1,024 characters. The agentskills.io guide asks each description to state its boundary with adjacent skills. In a dev.to test of two overlapping date skills, routing was 8 of 8 correct when the names or the descriptions differed.

A method skill's skip clause says "Skip it as the first skill" for a request that its parent covers. That wording tells the agent to skip the skill when only its own trigger words match. The agent can still load it when the parent's body names it. In the recorded runs, the agent loaded strategy on P1 in 4 of 5 runs. In two runs, it loaded strategy and testing on P3.

The domain descriptions copy the invoke-only wording, "Trigger only when". With that wording, `toby-game` and `toby-squall` had 0 recorded false fires on N5 and N6. Those runs used older descriptions and a model that no run file records. The domain wording names a loaded skill as the trigger, which no run has tested.

The agent loads a domain skill by the name in a body line, so the agent can still load it from a name-only listing. Claude Code 2.1.283 caps the description listing at 8,000 characters for a 200K context. Past that cap, it lists the least-used skills by name only. The Toby listing falls from 9,920 to 9,026 characters. That cap also covers every other installed skill.

In tests with 4 Svelte skills, a UserPromptSubmit forced-eval hook raised activation to 84 percent on Haiku 4.5 and to 100 percent on Sonnet 4.5. This proposal leaves the hook out, because it runs only on Claude Code and no test has used it with 23 skills. The hook also added about 2 seconds per prompt on Sonnet 4.5.

`scripts/validate-skills.py` gets two new checks. One check fails when no other SKILL.md body names a domain skill, because the agent then loads that skill only when the user names it. The other check fails when a "which X covers" clause names a skill that does not exist.

## Tokens

The ruler is `len(text)/4`, which `scripts/token-budget.py` also uses. That script's docstring says the ruler runs 5 to 15 percent low on this prose.

| Resident part | Today | Proposed |
|---|---|---|
| Operating guide, `base/toby.md` | 4,744 | 4,709 |
| Skill Routing section inside the guide | 624 | 589 |
| Skill descriptions | 2,649 for 18 | 2,463 for 23 |
| Resident total | 7,393 | 7,172 |
| Claude Code listing text, in characters | 9,920 | 9,026 |

The table below counts loaded bodies, which is the measure `token-budget.py` prints. In a scenario on domain code, the proposed column includes one domain body for each kind of code.

| Scenario | Proposed skills | Today | Proposed |
|---|---|---|---|
| a question, answered | explain | 1,476 | 1,476 |
| a rename | clarity | 2,554 | 2,554 |
| a command or migration | environment | 1,636 | 1,636 |
| review my changes | code-review | 3,341 | 3,406 |
| a throwaway spike | experiment | 1,200 | 1,200 |
| one method on a repository | interfaces, complexity, testing, databases, caching | 7,909 | 9,450 |
| split a module | modules, strategy, docs, backend-apis | 7,512 | 8,294 |
| a feature, tactical | feature-dev, strategy, testing | 9,209 | 9,276 |
| a feature, strategic | today's seven plus backend-apis | 20,858 | 21,568 |
| learning, invoked | learning | 3,083 | 3,083 |
| a visual artifact | artifact-style | 5,452 | 5,452 |

The bodies-only numbers leave out the domain files that today's method skills tell the agent to open. The next table adds them for the three scenarios on domain code. Today the agent opens `toby-swd-interfaces/references/databases.md` and `toby-swd-complexity/references/caching.md` on P1. It opens the modules `backend-apis.md` on P2, and all three `backend-apis.md` files on the strategic feature.

| Scenario | Today, with domain files | Proposed, tables settle it | Proposed, example files opened |
|---|---|---|---|
| one method on a repository | 14,044 | 9,450 | 15,132 |
| split a module | 10,117 | 8,294 | 10,711 |
| a feature, strategic | 30,961 | 21,568 | 31,065 |

The largest modelled turn, resident plus bodies, rises from 28,251 to 28,740 tokens. With every example file opened, the largest turn falls from 38,354 to 38,237 tokens. When the domain tables settle the decision, the largest turn is 28,740 tokens, which is 9,614 below today's 38,354.

`toby-swd-complexity` loses 104 tokens, `toby-swd-modules` loses 90, and `toby-swd-interfaces` loses 35, because the proposal removes their domain lists. `toby-code-review` gains 65 tokens, `toby-feature-dev` gains 43, `toby-swd-testing` gains 24, and `toby-simplify-code` gains 21, because the proposal adds a chain line to each. The five domain bodies are 828 to 920 tokens each. Every body stays under the validator's 6,000-token ceiling.

On disk, the 15 domain files contain 48,125 tokens today. After the move, the moved files contain 45,099 tokens of examples. The five bodies contain another 4,285 tokens, so the total is 49,384. The section headings and the lists of example titles add those 1,259 tokens. Twelve pairs of examples cover the same code, such as the stampede example in both the modules and the complexity caching files. A later merge of those pairs could remove up to 7,239 tokens, which is the total size of the smaller example in each pair. I matched those pairs by title and read two of them.

## Practices that move

Every coding practice moves with its file or table. I ran `scripts/rule-diff.py` on the rule inventories of today's tree and the prototype. It found 93 reworded sentences, 84 split sentences, and 13 sentences whose content words left the repo. All 13 are description text or the old domain lists in the method skills. Each rule in them still appears in a body. For example, the complexity red flags still cover speculative optimization, and the testing body still says to classify a failing test before weakening it.

These practices move.

1. The 82 cheat-sheet rules at the end of the 15 domain files move into the five domain bodies with their wording unchanged. By domain, the counts are web 19, mobile 13, backend APIs 17, databases 16, and caching 17.
2. The 68 worked examples move with their files. By domain, the counts are web 13, mobile 13, backend APIs 14, databases 15, and caching 13.
3. The rule "Open one reference file" in three method skills becomes one line in each, which tells the agent to load the domain skill and read one section. The example file becomes optional, so this rule changes what the agent reads.
4. The interface-segregation pointer in `toby-swd-interfaces` now names `toby-backend-apis`. Today it names `references/backend-apis.md`.
5. Seventeen pointers inside the moved files now name the method skill they point to, such as "Step 7 in `toby-swd-interfaces`". Without that edit, the validator reports 10 broken references on the prototype.

These triggers move between descriptions. They are routing rules, so the coding practices stay the same.

1. A plain bug fix goes to `toby-feature-dev`, which names strategy and testing. Today the strategy description lists a bug fix with behavioral risk, and the testing description lists every behavior change.
2. A snapshot update goes to `toby-swd-testing`, which names environment.
3. Confusing control flow goes to `toby-simplify-code`, which names clarity for renames.
4. A public API change in one signature goes to `toby-swd-interfaces`, which names docs.
5. A cache, retry, or error path inside a new method goes to `toby-swd-interfaces`, which names complexity.
6. `check the voice` and `voice standards` join the `toby-voice` description. "Tweaking settings" and "comparing options" join the experiment description. The guide keeps its copies of those triggers.
7. The guide's four-decision tie-break gets shorter, because each method description now states its decision and its skip targets.

## Hosts

The proposal uses the same host features as the current 18 skills on the four hosts that `scripts/install.sh` installs to. Those hosts are `~/.codex`, `~/.claude`, `~/.copilot`, and `~/.kiro`.

- `install_skills` copies every `skills/toby-*` folder, so the script installs the five new folders with no change.
- The new skills use only the `name` and `description` frontmatter fields, which all four hosts read. I left out `when_to_use`, `paths`, and `user-invocable`, because the research found no Kiro support for them.
- Each new skill has an `agents/openai.yaml` for Codex, which the validator requires. That file leaves implicit invocation at its default, because the agent must be able to load the skill from a chain.
- A chain line has the same form as the line in `toby-feature-dev` that says "Load `toby-swd-strategy`", so the proposal adds no host feature.
- The longest description is 591 characters, which is under Copilot's 1,024-character limit. Every name is under 64 lowercase characters.
- `scripts/sync.sh` copies the routing change from `base/toby.md` into `AGENTS.md` for Codex, both Claude Code instruction files, `copilot-instructions.md`, the Kiro steering file, and `toby-voice/references/toby.md`.
- A reinstall with `--force` removes each old skill folder before it copies the new one, so the reinstall also removes the old domain files from `~/.X/skills/toby-swd-*/references`.
- The research says a custom Kiro agent lists its skills through `skill://` URIs, so that list needs the five new skills. The Kiro page behind that claim did not load in full.
- The `anthropic-skills:toby-*` copies synced from claude.ai come from outside `install.sh`. They would keep the old 18 descriptions and the old domain paths.

## Migration

| Change | Count |
|---|---|
| Files created | 10, which are five SKILL.md files and five `agents/openai.yaml` files |
| Files moved | 15 domain reference files, renamed to `placement.md`, `contracts.md`, and `cost.md` |
| Files merged | 0 whole files, and 15 cheat-sheet sections merge into the five new bodies |
| Files deleted | 0 |
| SKILL.md files edited | 18 descriptions and 7 bodies |
| Other repo files edited | `replace-the-conditional.md`, `base/toby.md`, and four scripts |
| Generated copies rewritten by `sync.sh` | 6 |
| Eval suites | 3 need new cases, and 2 need one case edited |

The seven edited bodies are feature-dev, code-review, simplify-code, modules, interfaces, complexity, and testing. The four scripts change as follows.

- `scripts/validate-skills.py` gets the two checks in the Firing section, and its `feature-change` group in `ROUTING_GROUPS` gets a domain skill.
- `scripts/trigger-probe.py` shows all 23 descriptions. Today it shows 16 and leaves out `toby-voice` and `toby-artifact-style`.
- `scripts/token-budget.py` gets the domain skills in its scenarios and a column for the files each scenario opens.
- `evals/run.py` lines 530 to 537 still say 14 skills, eight prompts, and P1 to P4 with N1 to N6, so they change to 23 skills and the new probe list.

The eval suites change as follows.

- In `evals/suites/triggering.md`, the P1, P2, and P3 directives change so that the description probe requires the entry skill alone. The suite gets rows 12 to 27 of the request map as probes. It also gets a chain mode. In that mode, the probe shows the agent the entry skill's body, then asks which skills it would load next.
- `evals/suites/feature-dev.md` gets a plain bug fix, row 27. Its expected result is tactical sizing with strategy and testing loaded.
- `evals/suites/review.md` gets a diff on a React store slice where one design finding needs the Contracts table in `toby-web`.
- In `evals/suites/swd.md` and `evals/suites/swd-notes.md`, the exchange-rate cache placement task changes so the writer reads `toby-caching`.

`evals/gold/repo-review.jsonl` names the old domain paths in 46 rows. Each of those rows dates its path "before the fixes", so the rows need no edit. The three untracked files in `docs/plans/token-efficiency/targets/` also name the old paths. They are the user's untracked work, so the migration leaves them alone.

## Not verified

- I did not install the prototype on any host.
- No recorded run measures whether an agent loads a skill that a loaded skill's body names, on any host. The chain mode in `triggering.md` would measure it with at least two samples, which `evals/run.py` sets as the minimum for that suite.
- On P1 and P2, complexity, testing, strategy, and docs no longer fire from their own descriptions. When the agent fails to load the entry skill, it also skips every skill in that entry skill's chain.
- No eval covers plain bug fixes in `toby-feature-dev`.
- No run records which model produced the existing trigger results, so the 0 false fires for the invoke-only wording have no model attached.
- The guide's voice line still lists comments, while the `toby-voice` description skips comments inside code. That conflict exists today, so this proposal leaves it for the user to decide.
