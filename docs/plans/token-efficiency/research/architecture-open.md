# Toby skill architecture, open proposal

I propose 18 skills in three groups. On Claude Code, Codex, and Copilot, the model picks from 9 of them, which are the entry skills. Six method skills contain the engineering practice. An entry skill opens each method skill by file path, at the step its body lists. Three skills load only when the user types their name or slash command.

The numbers below use the len/4 ruler of `scripts/token-budget.py`, which by its own docstring runs 5 to 15 percent low on prose dense with backticks.

- Resident cost falls from 7,393 to 6,263 tokens. Resident cost counts the guide and every skill's frontmatter, which the host sends on every turn.
- The Toby part of the listing on Claude Code falls from 9,920 to 3,878 characters. The listing is the list of skill names and descriptions that a host includes in the model's context. In the installed Claude Code 2.1.283, the default listing budget at a 200K context is 8,000 characters.
- Loaded bodies across the 11 scenarios rise from 64,230 to 65,056 tokens, which is 1.3 percent. The single-method scenario rises by 3,370 tokens, while the tactical feature falls by 1,856.
- The largest scenario falls from 20,858 to 20,176 tokens.
- Seven of the eight scored false fires in the recorded runs were method skills. The proposal takes method skills off the listing on three of the four hosts.

No number here comes from a rewritten file, because none exists yet. Each body size is a sum of current sections plus drafted text measured with the same ruler. The script that computes them is `scratchpad/arch-open/model.py`.

## Terms

- An entry skill is a skill the model picks from its description. Each user request maps to one entry skill or to none.
- A method skill is a skill that loads only when an entry skill's body opens it.
- "The body opens X" means the skill body tells the agent to read file X at that step.
- A chain is an entry skill plus the method skills its body opens for the request.
- An invoke-only skill loads only when the user types its name or its slash command.
- A false fire is a skill that loads on a request whose eval directive forbids it.

## Design

Each entry skill covers one kind of output, so the model picks an entry skill by what the user wants back.

| The user wants | Entry skill |
| --- | --- |
| a change to what the code does | `toby-build` |
| a change to how code is arranged or reads, with behavior unchanged | `toby-refactor` |
| a change to the tests alone | `toby-swd-testing` |
| a report on a change, with no edits | `toby-code-review` |
| an answer to a question, with no edits | `toby-explain` |
| a throwaway trial | `toby-swd-experiment` |
| a command run on the machine | `toby-swd-environment` |
| prose such as a commit message, a README, or a rewrite | `toby-voice` |
| a visual | `toby-artifact-style` |

The nine rows name nine different outputs. For each trigger word that two descriptions share, at least one of the two has a skip clause that names the other skill.

I kept the listed group at nine for three reasons from the research.

1. Overlapping descriptions explained up to 68 percent of the selection drop in arXiv 2605.24050. Each listed skill adds one more description that others can overlap.
2. In a two-skill Claude Code test, distinct names or distinct descriptions gave 8 correct picks of 8. Misses and double loads came only when both fields overlapped.
3. Claude Code drops the descriptions of the least-used skills when the listing passes 8,000 characters at a 200K context. Today's 18 Toby descriptions use 9,920 characters.

A method skill stays off the listing on Claude Code, Codex, and Copilot, so it adds no listing cost there. The method group can therefore split further, such as `toby-swd-complexity` into an errors skill and a performance skill.

### Host fields

| Field | Hosts that read it | Use here |
| --- | --- | --- |
| `disable-model-invocation: true` in SKILL.md frontmatter | Claude Code, Copilot | Set on the 6 method skills and the 3 invoke-only skills. Claude Code then removes the description from the listing and still accepts the slash command. |
| `policy.allow_implicit_invocation: false` in `agents/openai.yaml` | Codex | Set on the same 9 skills. Codex then leaves the skill out of the model context and still accepts `$skill`. |
| `paths` globs | Claude Code only | Unused. The field can only narrow loading, and Anthropic's skill-creator reports that Claude loads too few skills more often than too many. |
| `when_to_use` | Claude Code only | Unused, because Codex, Copilot, and Kiro would lose any trigger written there. |
| UserPromptSubmit hook | Claude Code only | Optional, described under Hook. |

The Codex field and its meaning come from the Codex skill-creator reference in `~/.codex/sessions/2026/05/31/rollout-2026-05-31T19-15-59-*.jsonl`. Codex's own migration table, `~/.codex/vendor_imports/skills/skills/.curated/migrate-to-codex/references/differences.md`, lists `disable-model-invocation` as unsupported. No source states a Kiro field that hides a skill from the listing, so Kiro still lists all 18 skills.

### Opening a method skill

Each entry body lists the method skills it opens, with the condition and the step. The body names the sibling folder, such as `toby-swd-modules/SKILL.md` in the skills folder that holds the entry skill. It also lists the four install roots, the way the `toby-voice` body already lists them for its checker. Those roots are `~/.claude/skills`, `~/.codex/skills`, `~/.copilot/skills`, and `~/.kiro/skills`.

Claude Code prints each skill's base directory when the skill loads, so the sibling path resolves there. A Codex session log from 2026-09-27 lists each skill with its file path, such as `r0/toby-swd-testing/SKILL.md`. The sibling path is not verified on Copilot or Kiro.

### Hook

An optional Claude Code hook adds 71 tokens to each prompt. Its text lists the nine entry skills and asks the model to state, before the first tool call, which one the request needs or none. A forced-evaluation hook of this kind reached 100 percent activation with 0 percent false positives on Sonnet 4.5. It reached 84 percent on Haiku 4.5. Both tests used only 4 skills, so the result is not verified for this set.

`scripts/install.sh --hooks` would install the file and print the settings block, as it does now for the voice hooks. Every host must pick the right entry skill without the hook, so I would add the hook only after an A/B run shows a gain.

### Guide changes

The Skill Routing section of `base/toby.md` falls from 624 to 370 tokens with the text below.

```
## Skill Routing
- These routes stay active whenever the matching skill is installed, including late in a long chat. Each request loads one entry skill, picked by its description. The entry skill opens the method skills it lists, at the step that needs them.
- Open `toby-swd-strategy`, `toby-swd-modules`, `toby-swd-interfaces`, `toby-swd-complexity`, `toby-swd-clarity`, and `toby-swd-docs` only when an entry skill lists them, because no request starts one of them alone.
- When a Toby skill and a skill from another source match the same request, load the Toby skill.
- `toby-voice` stays in force for the rest of the session once it loads. Its rules apply to every reply from that point, in chat and in files, until the user says otherwise. A skill that has to be re-invoked each turn stops being applied around turn six.
- Load `toby-voice` before finalizing voice-bearing output: a substantive reply, code findings, a commit message, a PR description, docs, comments, a plan, or any generated artifact. Load its `references/plain-language.md` with it, and load its `references/toby.md` only when the operating guide is absent from context. Do not wait to be asked.
- When a skill's description says to skip it for this kind of task, skip it, even when a word in the request matches. When the user calls the work throwaway, use `toby-swd-experiment`, whatever else the request names.
- State active skills in one short line, including each method skill an entry skill opened.
```

Work Modes falls from 82 to 32 tokens, because its experiment triggers move to the `toby-swd-experiment` description.

The source-precedence line exists because Claude Code ships its own `code-review` and `simplify` skills. Those two match the same requests as `toby-code-review` and `toby-refactor`. No description can name a skill that exists on one host only, so the guide states the precedence.

The `toby-voice` line stays as it is. It loads the writing rules for any prose output. The voice rules cover the wording of the output, while each entry skill covers the task.

## Skills

### Entry skills

**1. `toby-build`**, renamed from `toby-feature-dev`

> Changes what code does in the smallest step that keeps the design at least as good as before. It proves the change with one check run before the edit and again after it. Use it when the user asks to add, build, implement, wire up, finish, fix, or speed up a behavior. The behavior can be a feature, a ticket, an endpoint, a method, a screen, a job, a flag, or a bug. Skip it for a throwaway spike, which toby-swd-experiment covers. Skip it when behavior stays the same, which toby-refactor covers, and for work on tests alone, which toby-swd-testing covers. Skip it for a one-file edit that copies a pattern already in that file.

The body holds 4,134 tokens. It covers the running order, the mode choice, the size gate, tactical discovery, the criteria lines, ambiguity, the four ship conditions, and stop 1. It also covers the tactical design lines, the method table, the build loop, the before-and-after proof, Don't build, Red flags, and the final response.

| The body opens | When |
| --- | --- |
| `references/strategic.md` (1,458 tokens), which holds sibling-feature and call-site discovery, greenfield rules, the slice cut, stops 2 and 3, the design lines, the plan document, and resuming half-built work | a strategic trigger fires |
| `references/checks.md` | before the out-of-scope line or the first edit, and again before the handoff |
| `references/examples.md` | the work needs a slice cut or a plan step |
| `toby-swd-strategy` | before the design pass, unless the surrounding code already settles the structure |
| `toby-swd-interfaces` | the design adds or changes a signature |
| `toby-swd-modules` | the design adds a module, moves code, or gives a module a new job |
| `toby-swd-complexity` | the change touches an error path, a retry, validation, a cache, concurrency, batching, or speed |
| `toby-swd-testing` | before the first edit of every behavior change |
| `toby-swd-docs` | module structure or a public API changes |
| `toby-swd-environment` | before any command beyond safe inspection |
| `toby-swd-clarity` | before the handoff, when the diff adds a public name or an interface comment |

**2. `toby-refactor`**, renamed from `toby-simplify-code`

> Changes how code is arranged or reads and keeps its behavior and tests the same. Use it when the user asks to simplify, tidy, "clean up", refactor, de-duplicate, extract, split, merge, move, or rename code. Use it to add or fix comments and docstrings. Skip it when behavior should change, which toby-build covers, and when the user wants findings with no edit, which toby-code-review covers.

The body holds 1,305 tokens. It covers the disposition, a scope picker, the behavior-drift rules, Keep, the shared brownfield rule, the process, and the final response. The disposition keeps the countable win, precision over recall, and "nothing worth simplifying" as a valid result.

| The body opens | When |
| --- | --- |
| `toby-swd-clarity` | only names, comments, or docstrings change |
| `references/cleanup.md` (843 tokens) and the current `references/smells.md` | the scope is a local cleanup inside changed code |
| `toby-swd-strategy`, then `toby-swd-modules` | the scope is a split, merge, move, or extraction across files |
| `toby-swd-interfaces` | a signature changes |
| `toby-swd-docs` | module structure changes |
| `toby-swd-complexity` | the scope is an error check for a condition that cannot occur |
| `toby-swd-testing` | before any test changes |

**3. `toby-swd-testing`**, an entry skill that other entry skills also open

> Keeps tests an executable specification of behavior. Use it when the user asks to write, fix, update, delete, or weaken a test. Use it to fix a flaky test, raise coverage, or update snapshots. Skip it when production code changes as well, which toby-build covers, and for a throwaway spike, which toby-swd-experiment covers.

The body holds 1,863 tokens with its current sections. Its Brownfield section shrinks to the characterization-test line. The body opens `toby-swd-environment` before a snapshot update or a full-suite run.

**4. `toby-code-review`**

> Reports the proven risks in a change and edits nothing. Use it when the user asks to review a diff, a PR, a commit, a branch, or the working tree. Use it when the user asks what is wrong with a change. Skip it when the user wants the code changed, which toby-refactor or toby-build covers. Skip it for a question about how code works, which toby-explain covers.

The body holds 3,138 tokens, because the skills-and-config section moves to a reference file. The body opens `references/smells.md` for the design pass. It opens `references/skills-diff.md`, at 245 tokens, when the diff changes a SKILL.md, a guide, a hook, or an agent config. The intro already maps each kind of fix to a method skill. The body now opens that method skill when a finding depends on it.

**5. `toby-explain`**

> Answers a question in plain words, then stops, and edits no files. Use it when the user asks why, how, what the difference is, which option fits, or where code should go, on any subject. Use it for "walk me through", "help me understand", and any request for a clear, short, or simple explanation. Skip it when the user asks for a diagram, a chart, or a deck, which toby-artifact-style covers.

The body holds 1,516 tokens, which is the current body plus one chain line. The body opens `references/examples.md` as it does now. For a placement question, it opens `toby-swd-modules` and writes the placement note that skill describes. For a design question, it opens `toby-swd-strategy/references/design-note.md`.

**6. `toby-swd-experiment`**

> Runs a short, reversible discovery loop while the behavior is still undecided. Use it when the user says spike, proof of concept, throwaway, try a few values, compare options, tweak settings, or let me test. The word throwaway decides the route even when the request also names retries, timeouts, or tests. Skip it for work the user intends to keep, and for starting or stopping a server alone, which toby-swd-environment covers.

The body is unchanged at 1,199 tokens. The body opens `toby-swd-environment` before commands, as its Environment Boundary section already says. It opens `toby-swd-testing` once the user picks a behavior.

**7. `toby-swd-environment`**

> Classifies each command before it runs and asks before any command that changes the user's machine. Use it when the user asks to run a migration or a seed script, or to install a dependency. Use it to start or stop a server, free a port, clear a cache, or run the full test suite. Skip it for a code edit with nothing to run, and for a snapshot update, which toby-swd-testing covers.

The body is unchanged at 1,637 tokens.

**8. `toby-voice`**

> Applies Toby's writing rules to prose and runs the voice checker on it. Use it for a commit message, a PR description, a README, an AGENTS.md, a doc, or a rewrite of any text. Use it when the user says voice, toby voice, check the voice, voice pass, or voice standards. Use it for wording or tone help. Skip it for names and comments inside code, which toby-refactor covers.

The body holds 2,007 tokens, which is the current body plus one line. The body opens `references/plain-language.md` every time, and `references/toby.md` only when the guide is absent from context. The body opens the examples and runs the checker as it does now. It opens `toby-swd-docs` when the prose is a module README.md or AGENTS.md.

**9. `toby-artifact-style`**

> Applies Toby's visual design system to a visual and to the copy inside it. The visual can be a diagram, chart, dashboard, slide deck, HTML or React page, SVG, mockup, or reference card. Use it when the user asks to draw, show, chart, diagram, or build a visual, including a visual that explains something. Skip it for a text answer in chat, which toby-explain covers, and for a game, which only /toby-game starts.

The body is unchanged at 5,452 tokens. The body opens its references by task, as its load table already says.

### Method skills

Each method skill gets `disable-model-invocation: true` in its frontmatter and `policy.allow_implicit_invocation: false` in `agents/openai.yaml`. Its description matters only on Kiro, where the skill stays listed.

| Skill | Description | Body (tokens) | The body opens |
| --- | --- | --- | --- |
| `toby-swd-strategy` | Runs Toby's design pass before a change. toby-build, toby-refactor, and toby-explain open this file by path. Do not load it from a user request alone. | 1,356 | `references/design-note.md` (211 tokens) for a design note in chat, and `references/examples.md` for a worked case |
| `toby-swd-modules` | Contains Toby's checks for where code goes and when to split or merge. Entry skills open this file by path. Do not load it from a user request alone. | 3,595 | one stack file and one subject file, as now |
| `toby-swd-interfaces` | Contains Toby's procedure for designing a callable surface before its body. Entry skills open this file by path. Do not load it from a user request alone. | 2,747 | `references/design-it-twice.md` (578 tokens) for a consequential interface or a failed first comment, and one stack file |
| `toby-swd-complexity` | Contains Toby's error ladder and performance rules. Entry skills open this file by path. Do not load it from a user request alone. | 1,819 | `references/performance.md` (716 tokens) for a cache, batching, a stated budget, or a measured slow path, and one stack file |
| `toby-swd-clarity` | Contains Toby's rules for names, comments, and docstrings inside code. Entry skills open this file by path. Do not load it from a user request alone. | 1,330 | `references/comments.md` (1,199 tokens) when the change adds or edits a comment, a docstring, or control flow a reader could misread |
| `toby-swd-docs` | Contains Toby's rules for a module's README.md and AGENTS.md. toby-voice, toby-build, and toby-refactor open this file by path. Do not load it from a user request alone. | 1,910 | `references/examples.md` |

### Invoke-only skills

`toby-learning`, `toby-squall`, and `toby-game` keep their bodies and their descriptions. Each gets the same two host fields as a method skill. Kiro still reads the description, so the clause "Trigger only when the user explicitly invokes" stays.

## Request map

Each row gives a request with its one entry skill and the method skills that entry body opens. Rows 1 to 11 come from `evals/suites/triggering.md`, rows 12 to 24 from collisions in the research, and rows 25 to 28 from new boundaries.

| # | Request | Entry skill | Method skills opened | Neighbour that skips, and its clause |
| --- | --- | --- | --- | --- |
| 1 | P1. Add `getAccountBalance(userId)` to `AccountRepository`, read Redis first, fall back to Postgres, return null when missing. | `toby-build` | interfaces, complexity with `performance.md`, testing | `toby-refactor` skips a behavior change. |
| 2 | P2. `invoice.ts` is 1,400 lines and does three jobs. Split it. | `toby-refactor` | strategy, modules, docs | `toby-build` skips work where behavior stays the same. |
| 3 | P3. Build the CSV export for the reports page. | `toby-build` | strategy, testing, and modules or interfaces when the design adds them | `toby-swd-testing` skips work where production code changes too. |
| 4 | P4. Run the pending migration against my local database and re-seed it. | `toby-swd-environment` | none | `toby-build` sees no behavior to add. |
| 5 | N1. Rename `usr` to `user` in `session.ts`. No other change. | `toby-refactor` | clarity | `toby-build` skips work where behavior stays the same. |
| 6 | N2. Review my changes. | `toby-code-review` | as findings need | `toby-refactor` skips a request for findings. |
| 7 | N3. Try a few values for the retry backoff. Throwaway. | `toby-swd-experiment` | environment before a run | The guide's throwaway line and the `toby-build` skip clause. |
| 8 | N4. Add a `phone` field the same way `email` is done two lines up. | none | none | `toby-build` skips a one-file pattern copy. |
| 9 | N5. Build me a browser traffic game in one HTML file. | `toby-build`, or none | as the design needs | `toby-game` is off the listing. `toby-artifact-style` skips a game. |
| 10 | N6. Help me brainstorm names for this service. | none | none | `toby-squall` is off the listing. |
| 11 | N7. Clearly and concisely, what is the difference between a mutex and a semaphore? | `toby-explain` | none | `toby-swd-clarity` is off the listing. |
| 12 | Tidy the confusing control flow in `parseArgs` and rename its variables. | `toby-refactor` | clarity with `comments.md` | `toby-build` skips work where behavior stays the same. |
| 13 | Refactor the checkout service so the discount rules are in one function. | `toby-refactor` | strategy, modules | `toby-build` skips work where behavior stays the same. |
| 14 | De-duplicate the two date-formatting helpers into one shared module. | `toby-refactor` | strategy, modules | No other listed description contains de-duplicate. |
| 15 | Simplify the error handling in `upload.ts`, because half the catch blocks can never run. | `toby-refactor` | complexity | Complexity is off the listing. |
| 16 | Update the Jest snapshots for the `Header` component. | `toby-swd-testing` | environment before the update | `toby-swd-environment` skips a snapshot update. |
| 17 | Update the billing module README after the split. | `toby-voice` | docs | Docs is off the listing. |
| 18 | Add an optional `timeout` parameter to the public `fetchReport()` in the SDK. | `toby-build` | interfaces, complexity, testing, docs | Interfaces is off the listing. |
| 19 | Add a `POST /invites` endpoint that emails the invitee. | `toby-build` | strategy, interfaces, testing | Interfaces is off the listing. |
| 20 | Start the dev server so I can try the new button by hand. | `toby-swd-environment` | none | `toby-swd-experiment` skips starting a server alone. |
| 21 | Make a five-slide deck on the Q3 outage. | `toby-artifact-style` | none | `toby-voice` loads by the guide's voice line and covers the wording. |
| 22 | Explain how a TCP handshake works, with a diagram. | `toby-artifact-style` | none | `toby-explain` skips a request for a diagram. |
| 23 | Walk me through how B-tree indexes work. | `toby-explain` | none | `toby-learning` is off the listing. |
| 24 | Move the date helpers into a shared package and export `formatDate`. | `toby-refactor` | strategy, modules, interfaces | Modules and interfaces are off the listing. |
| 25 | Should the retry helper go in `http/client.ts` or in each sync job? | `toby-explain` | modules, for the placement note | `toby-refactor` needs a request to change code. |
| 26 | Write the commit message for this change. | `toby-voice` | none | No other description contains commit message. |
| 27 | The checkout page is slow. Make it faster. | `toby-build` | complexity with `performance.md`, testing | `toby-refactor` skips a behavior change, and speed counts as behavior here. |
| 28 | Fix the off-by-one in pagination. | `toby-build` | testing | `toby-refactor` skips a behavior change. |

Rows 1 and 27 depend on choices the user may reverse.

- Row 1 maps a single repository method to `toby-build`, where the other candidate is `toby-swd-interfaces`. The research found that the descriptions of `toby-swd-interfaces` and `toby-feature-dev` both match "Add a POST /invites endpoint". So I based the boundary on the output and left the request's size out of it.
- I count speed as behavior in row 27, because the before-and-after check in `toby-build` measures the slow path on both sides of the edit.

## Tokens

### Resident

| Part | Current (tokens) | Proposed (tokens) |
| --- | --- | --- |
| Operating guide | 4,744 | 4,440 |
| Frontmatter of all 18 skills | 2,649 | 1,823 |
| Total, by the `token-budget.py` ruler | 7,393 | 6,263 |

| Host | Toby skills listed | Listing (characters) | Listing (tokens) |
| --- | --- | --- | --- |
| Claude Code | 9 | 3,878 | about 970 |
| Copilot | 9 | 3,878 | about 970 |
| Codex | 9 | 3,878 | about 970 |
| Kiro | 18 | 6,483 | about 1,621 |
| Every host today | 18 | 9,920 | about 2,480 |

The optional hook adds 71 tokens to each Claude Code prompt.

### Loaded bodies per scenario

The scenarios are the 11 in `scripts/token-budget.py`. A reference file counts when the scenario meets the condition that opens it.

| Scenario | Current files | Current (tokens) | Proposed files | Proposed (tokens) | Change (tokens) |
| --- | --- | --- | --- | --- | --- |
| a question, answered | explain | 1,476 | explain | 1,516 | +40 |
| a rename | clarity | 2,554 | refactor, clarity | 2,635 | +81 |
| a command or migration | environment | 1,636 | environment | 1,637 | +1 |
| review my changes | code-review | 3,341 | code-review | 3,138 | -203 |
| a throwaway spike | experiment | 1,200 | experiment | 1,199 | -1 |
| one method on a repository | interfaces, complexity, testing | 7,909 | build, interfaces, complexity, `performance.md`, testing | 11,279 | +3,370 |
| split a module | modules, strategy, docs | 7,512 | refactor, strategy, modules, docs | 8,166 | +654 |
| a feature, tactical | feature-dev, strategy, testing | 9,209 | build, strategy, testing | 7,353 | -1,856 |
| a feature, strategic | 7 bodies | 20,858 | build, `strategic.md`, strategy, modules, interfaces, `design-it-twice.md`, complexity, `performance.md`, testing, docs | 20,176 | -682 |
| learning, invoked | learning | 3,083 | learning | 3,083 | 0 |
| a visual artifact | artifact-style | 5,452 | artifact-style | 5,452 | 0 |
| Sum | | 64,230 | | 65,056 | +826 |

The strategic row includes `design-it-twice.md` for a feature that changes a public API. Without that file, the row is 19,598 tokens.

The single-method row rises because the request now loads the `toby-build` procedure, which contains the criteria and the before-and-after proof. In the recorded runs, P1 loaded `toby-feature-dev` in 1 of 5 runs, so P1 usually got no proof step.

The recorded runs show what the current set loads in practice, though every run tested older descriptions and no run recorded its model. Each token figure below prices those loads at today's body sizes.

- `toby-swd-strategy` loaded on P1 in 4 of 5 runs, which made P1 cost 9,775 tokens in those runs.
- On P3, the run named `blind` loaded 16,312 tokens of bodies, while the run named `invokeonly` loaded 12,646.
- The before run's 7 false fires on N1 to N4 loaded 18,984 tokens. Of those, 13,547 tokens came from method skills, which the proposal takes off the listing.

### What the numbers leave out

- No body was rewritten. Shortening the `toby-build` body would lower the single-method row the most. These numbers include no such rewrite.
- The `toby-voice` layer costs 3,730 tokens on a prose turn in both designs, as `token-budget.py` reports separately.
- Stack references, such as `toby-swd-modules/references/web.md`, open on the same conditions in both designs, so I left them out of both columns.

## Practices that move

Every practice in the current skills stays in the repo. The table lists the 21 practices that change file or change the trigger that loads them.

| # | Practice | From | To |
| --- | --- | --- | --- |
| 1 | The whole feature workflow | `skills/toby-feature-dev/` | `skills/toby-build/` |
| 2 | Behavior-preserving cleanup | `skills/toby-simplify-code/` | `skills/toby-refactor/` |
| 3 | Sibling-feature and call-site discovery, greenfield rules, the slice cut, stops 2 and 3, the design lines, the plan document, and resuming half-built work | `toby-feature-dev/SKILL.md` | `toby-build/references/strategic.md` |
| 4 | The "Load `toby-swd-modules` when" and "Load `toby-swd-interfaces` when" bullets | `toby-feature-dev/SKILL.md` | the method table in `toby-build/SKILL.md` |
| 5 | What to look for, Not a simplification, and Idiom or local style | `toby-simplify-code/SKILL.md` | `toby-refactor/references/cleanup.md` |
| 6 | The rule against moving code or changing a signature during cleanup | the Out of scope section of `toby-simplify-code` | the local-cleanup scope of `toby-refactor`, while the across-files scope makes those moves after the modules checks |
| 7 | Put complexity in the right place while writing | `toby-swd-strategy` | check 3 and check 8 of `toby-swd-modules`, with a pointer left in strategy |
| 8 | Writing a design note | `toby-swd-strategy/SKILL.md` | `toby-swd-strategy/references/design-note.md` |
| 9 | Seven Brownfield Work sections | strategy, modules, interfaces, complexity, clarity, docs, testing | one shared rule in `toby-build` and `toby-refactor`, plus the one line each method keeps for itself |
| 10 | Decompose by knowledge, as step 1 of the interface procedure | `toby-swd-interfaces` | a pointer to check 1 of `toby-swd-modules` |
| 11 | The design-it-twice loop, tie resolution, and the redesign step | `toby-swd-interfaces/SKILL.md` | `toby-swd-interfaces/references/design-it-twice.md` |
| 12 | Performance design | `toby-swd-complexity/SKILL.md` | `toby-swd-complexity/references/performance.md` |
| 13 | Comments and Obviousness | `toby-swd-clarity/SKILL.md` | `toby-swd-clarity/references/comments.md` |
| 14 | How to review a skills or config diff | `toby-code-review/SKILL.md` | `toby-code-review/references/skills-diff.md` |
| 15 | The snapshot-update trigger | the `toby-swd-environment` description | the `toby-swd-testing` description |
| 16 | The four tie-break decisions for strategy, modules, interfaces, and complexity | `base/toby.md` Skill Routing | the method tables in the entry bodies |
| 17 | The invoke-only rule for learning, squall, and game | three `base/toby.md` lines | the two host fields, plus the descriptions Kiro reads |
| 18 | Answer-seeking phrases such as "walk me through" and "help me understand" | the `toby-learning` guide line | the `toby-explain` description |
| 19 | The triggers `check the voice` and `voice standards` | `base/toby.md` | the `toby-voice` description, while the reapply procedure stays in the voice body |
| 20 | The experiment triggers tweak settings, compare options, and let me test | `base/toby.md` Work Modes | the `toby-swd-experiment` description |
| 21 | Building a diagram that a question asks for | the `toby-explain` body, which applied `toby-artifact-style` | `toby-artifact-style` as the entry skill, with an explain skip clause |

Practice 6 and the new `toby-voice` description change what a skill does, so each needs the user's decision.

- Practice 6 lets `toby-refactor` move code between modules, which the Out of scope section of `toby-simplify-code` tells the agent to leave alone. The modules checks and the behavior-drift rules apply to every such move.
- The `toby-voice` description no longer skips an explanation, which settles the conflict the research found with the guide. The guide's voice line loads voice for every substantive reply, so voice loads on an explanation too.

## Hosts

| Need | Claude Code | Codex | Copilot | Kiro |
| --- | --- | --- | --- | --- |
| Entry skills picked from descriptions | yes | yes | yes | yes |
| Descriptions under 1,024 characters | yes, longest 629 | yes | yes | yes |
| Method and invoke-only skills off the listing | yes, by frontmatter | yes, by `openai.yaml` | yes, by frontmatter | no, they stay listed with "do not load" text |
| Invoke-only skills start from a typed name | `/name` | `$name` | `/name` | by the description clause |
| Entry body finds a method by sibling path | yes, base directory printed | yes, skill paths listed | not verified | not verified |
| Unknown frontmatter field ignored | yes | the migration table calls it unsupported, and a live load is not verified | the field is native | not verified |
| Optional hook | yes | no | no | no |

Entry routing uses descriptions only, which all four hosts read. Method opening also needs the skill folder path, which I found on Claude Code and Codex only. The open items are the sibling path on Copilot and Kiro, and whether Kiro and Codex ignore `disable-model-invocation`. `scripts/test-install.sh` checks only the copied files, so each open item needs one live load per host.

## Migration

| Kind | Count | Files |
| --- | --- | --- |
| Created | 8 | `toby-build/references/strategic.md`, `toby-refactor/references/cleanup.md`, `toby-swd-strategy/references/design-note.md`, `toby-swd-interfaces/references/design-it-twice.md`, `toby-swd-complexity/references/performance.md`, `toby-swd-clarity/references/comments.md`, `toby-code-review/references/skills-diff.md`, `evals/suites/chains.md` |
| Created, optional | 1 | `hooks/toby-route.py` |
| Moved | 7 | the 4 files of `toby-feature-dev` to `toby-build`, and the 3 files of `toby-simplify-code` to `toby-refactor` |
| Merged | 0 whole files | 9 sections merge, which are practices 7, 9, and 10 |
| Deleted | 0 in the repo | The 2 retired folders stay on each of the 4 hosts until `install.sh` removes them, which is 8 folders |
| Edited | 54 | 18 SKILL.md files, 11 `agents/openai.yaml` files, `base/toby.md` and its 6 synced copies, 6 scripts, 4 eval docs, 7 eval suites, and `README.md` |

The 6 scripts are `validate-skills.py`, `trigger-probe.py`, `token-budget.py`, `measure-skills.py`, `install.sh`, and `test-install.sh`.

- `validate-skills.py` replaces `ROUTING_GROUPS` with the entry chains. It checks the two host fields where it now checks the guide's invoke-only lines. Its reference-reachability check accepts sibling paths.
- `trigger-probe.py` lists the 9 entry skills and the 3 invoke-only skills, plus a Kiro arm with all 18.
- `install.sh` needs a list of retired folder names. Without one, the old `toby-feature-dev` and `toby-simplify-code` folders keep loading on every host.

The 4 eval docs are `evals/run.py`, `evals/README.md`, `evals/grading.md`, and `evals/boundaries.md`. The `run.py` edit also fixes its triggering prompt, which still says 14 skills, P1 to P4, and N1 to N6.

Five eval suites need new cases. One of them, `chains.md`, is a new file.

| Suite | New cases |
| --- | --- |
| `triggering.md` | new directives for P1, P2, N1, N2, and N7, and one case for each of rows 12 to 28 |
| `chains.md`, new | one case per entry skill, each loading the entry body and checking which method files the agent opens |
| `feature-dev.md` | a single-method request, and a strategic request that must open `strategic.md` |
| `explain.md` | a placement question that must open modules, and a diagram request that must load no explain body |
| `review.md` | a SKILL.md diff that must open `skills-diff.md` |

Three suites need path edits only. `artifacts.md` points at the plan document and the clarity comments. `swd.md` and `swd-notes.md` point at the strategy design note.

## Before adoption

The user's memory note "Agree eval design first" requires agreement before any eval run, so I ran none. I propose the three runs below.

1. Rebuild the triggering run on the 9 entry skills and the 3 invoke-only skills, using the 28 requests above. Run at least 2 samples, record the model, and run Haiku and Sonnet, because Haiku lost more accuracy in the overlap studies. A pass means each request loads its one entry skill or none, and no invoke-only skill loads.
2. Run `chains.md` with each entry body loaded. A pass means the agent opens every method file the row lists and no other.
3. Run two A/B arms on the same requests. One compares the "Use it when" wording with the "ALWAYS invoke this skill when" template. The other compares the hook with no hook. The research reports no false-positive rate for either change on a mutually exclusive set.

## Risks

- The single-method scenario costs 3,370 tokens more than today's modelled cost. It costs 1,504 more than the 9,775 tokens P1 loaded when strategy also loaded.
- The sibling-path opening is not verified on Copilot or Kiro. If a host cannot resolve that path, every method skill on that host stops loading.
- Kiro still lists all 18 skills, so the method descriptions there rely on "do not load it from a user request alone".
- The source-precedence line for Claude Code's own `code-review` and `simplify` skills is not measured.
- The claude.ai copies named `anthropic-skills:toby-*` duplicate every Toby trigger with older text. Only the user can remove them.
- The installed `~/.claude/CLAUDE.md` predates commit 8f238da and still has 13 old route lines. A reinstall fixes it after the user approves the edit.
- The `toby-refactor` description quotes a two-word user phrase that contains a hard-banned word. The user decides whether a quoted trigger phrase counts as an exact user quote, which the guide exempts.
- Three entry skills keep the `toby-swd-` prefix to save migration. Renaming them later costs a second round of the same edits.
