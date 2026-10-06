# Testing and agentic research proposals

This file proposes 35 changes to six Toby skills, two complexity references, and `base/toby.md`. The 33 changes that edit text save 1,263 tokens net. The proposals come from comparing 31 published practices with the skills' current text.

Each token change is the proposed text's characters minus the current text's characters, divided by 4 and rounded. The script `proposals.py` in this scratchpad folder computes the numbers from each proposal's full current text. It also checks that each current text appears once in the repo. No source measured model behavior without these rules, so each gap ships only after its eval shows the current skill failing. A proposal with no risk line weakens no Toby rule that I found.

| Heading | Proposals | Net tokens |
|---|---|---|
| Gaps | 6 | +245 |
| Conflicts | 6 | -190 |
| Rewrites | 9 | -301 |
| Cuts | 14 | -1,017 |
| Total | 35 | -1,263 |

The `base/toby.md` edits save 85 tokens in each of the five instruction files built from it.

## Gaps

I left four missing practices out. Fowler's 2021 article traces the pyramid and trophy dispute to two definitions of a unit test, so the skills keep stating no test ratio. Mutation-testing tools need a dependency the user approves. Feature-dev's before run already checks each criterion against the unchanged code, which tests the test the way one seeded fault would. Server-side idempotency-key rules, such as a 422 for a reused key with a different payload, wait for an eval that shows a model missing them. I left out circuit-breaker states because `backend-apis.md` example 4 already lists them.

### G1. Expected value copied from the output

- Target: `skills/toby-swd-testing/SKILL.md`, Red flags.
- Current text: the list has no entry for this failure.
- Proposed text:

  ```text
  - **Expected value copied from the output.** The assertion checks for whatever the code returned, so it passes with the bug in place. Work out the expected value from the spec or by hand.
  ```

- Reason: Kent Beck's Canon TDD warns against pasting computed values into expected values to force a pass. The skill's failing-test classification covers existing tests. The skill has no rule for a new test whose expected value came from running the code.
- Source: https://newsletter.kentbeck.com/p/canon-tdd
- Tokens: +47.

### G2. Flaky tests and fixed sleeps

- Target: `skills/toby-swd-testing/SKILL.md`, Red flags.
- Current text:

  ```text
  - **Flaky test.** Passes on retry, fails at random. Fix the nondeterminism, and never loop it until it goes green.
  ```

- Proposed text:

  ```text
  - **Flaky test.** It passes and fails on the same code. Look for the cause in async waits first, then concurrency, then test order. Replace a fixed sleep with a wait on the event, or a poll with a timeout. Check the code under test for a race. Do not rerun the test until it happens to pass, because a green rerun hides the cause.
  ```

- Reason: Luo et al. studied 201 flaky-test fixes and found async waits behind 45%, concurrency behind 20%, and test order behind 12%. In 24% of the fixes the code under test changed, and 94% of those changes fixed a real bug. The current entry bans retry loops and says nothing about fixed sleeps.
- Source: https://mir.cs.illinois.edu/marinov/publications/LuoETAL14FlakyTestsAnalysis.pdf and https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html
- Tokens: +54.

### G3. Which dependencies get a mock

- Target: `skills/toby-swd-testing/SKILL.md`, Mocks and test doubles, item 3.
- Current text:

  ```text
  3. **Mock** only at system boundaries: external APIs, payment, email, time, randomness, file systems, and failure modes hard to trigger otherwise.
  ```

- Proposed text:

  ```text
  3. **Mock** only a dependency whose calls another system sees, such as a third-party API, payment, email, or a message bus. Mock or fake time, randomness, and failures that are hard to trigger. Put each mock on your own adapter class around that client. Test against the application's own database with the real implementation or a fake.
  ```

- Reason: Khorikov mocks only dependencies whose calls other systems observe, and he treats calls to the application's own database as implementation details. Khorikov and the London-school authors agree on one rule, which is to mock only types you own through an adapter over the third-party client. The current item allows a mock placed directly on the HTTP library. It does not say where the application's own database goes.
- Source: https://enterprisecraftsmanship.com/posts/when-to-mock/, https://khorikov.org/posts/2020-06-15-mocking-types-that-you-own/, https://abseil.io/resources/swe-book/html/ch13.html, and http://jmock.org/oopsla2004.pdf
- Tokens: +48.
- Toby practice at risk: `evals/README.md` records that the rule "Mock external dependencies at the system boundary" was lost once. The lost-rules gate must show item 3 as its survivor. The proposed item also drops "file systems" from the mock list.

### G4. Retry layering, jitter, idempotency, and timeouts

- Target: `skills/toby-swd-complexity/SKILL.md`, Red flags, plus four calls in `references/backend-apis.md` (lines 54, 62, and 128) and `references/mobile.md` (line 48).
- Current text: SKILL.md has no entry for these four failures. The four reference calls read `backoff(attempt)`.
- Proposed text for SKILL.md:

  ```text
  - A remote call with no timeout.
  - A retry added above a client or SDK that already retries.
  - Retry backoff with no jitter.
  - A retried write with no idempotency key that the server dedupes on.
  ```

- Proposed text for the references: rename each `backoff(attempt)` call to `jitteredBackoff(attempt)`, which `references/databases.md` already uses.
- Reason: Amazon's Builders' Library shows three tries at each of five layers multiplying database load 243 times. Brooker's simulation found that full jitter cut calls by more than half. Stripe, Amazon, and the IETF draft make a retried write safe only with an idempotency key. Amazon and the SRE book set a timeout on every remote call. SKILL.md states none of these rules. The references `backend-apis.md`, `databases.md`, and `mobile.md` state the timeout, jitter, and idempotency rules. SKILL.md tells the model to open those references only for a matching stack.
- Source: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter, https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/, https://docs.stripe.com/api/idempotent_requests, and https://sre.google/sre-book/addressing-cascading-failures/
- Tokens: +57, which is +49 in SKILL.md and +8 in the references.
- Toby practice at risk: the timeout entry asks for a timeout before any measurement. A reader could take the rule "Add complexity only on evidence" to forbid that. Example 3 in `backend-apis.md` already describes a timeout as a design-time step, so the two rules agree.

### G5. A deletion test for AGENTS.md lines

- Target: `skills/toby-swd-docs/SKILL.md`, AGENTS.md red flags.
- Current text: the list has no deletion test.
- Proposed text:

  ```text
  - The file has a line whose removal would cause no agent mistake, so delete that line.
  ```

- Reason: Gloaguen et al. found that context files written by a model had a small negative effect on task success and raised inference cost by over 20%. Anthropic's pruning test asks whether removing each line would cause a mistake. The docs skill lists what to include and gives no test for what to delete.
- Source: https://arxiv.org/abs/2602.11988 and https://code.claude.com/docs/en/best-practices
- Tokens: +22.

### G6. A failing test fails on the bug

- Target: `skills/toby-swd-testing/SKILL.md`, Test-first, item 1.
- Current text:

  ```text
  The failing test proves it catches the bug, then proves the fix, then guards against return.
  ```

- Proposed text:

  ```text
  Read the failure and confirm it shows the bug's wrong result. A failure from an import error, a missing fixture, or a typo proves only that the test is broken.
  ```

- Reason: Khorikov says that watching a test fail for the right reason validates the test. The current item counts any failure as proof, including a failure in setup. Feature-dev's example `FAIL expected 409, got 200` already fails on the assertion, so feature-dev needs no edit.
- Source: https://khorikov.org/posts/2022-01-24-test-first-vs-test-last-approaches/ and https://martinfowler.com/bliki/TestPyramid.html
- Tokens: +17.

## Conflicts

### C1. The Files section in AGENTS.md

- Target: `skills/toby-swd-docs/SKILL.md`, Sections in order, item 2 and the heading list above it.
- Toby's rule:

  ```text
  2. **Files.** List only the files a new agent must understand to work here.
  ```

- The research: Gloaguen et al. found repository overviews unhelpful and advise listing only practices that differ from the default. Anthropic says to leave out what the agent can read from the code. OpenAI's Codex guide and Anthropic both say to list the build, test, and lint commands. The section list has no place for them.
- Recommendation: the research wins, so replace `Files` with `Commands` in item 2 and in the heading list.
- Proposed text:

  ```text
  2. **Commands.** Give the narrowest command that builds, tests, or lints this module, such as `pnpm test --filter notify`. Cite a file in a later section only when its job does not show in its name or code.
  ```

- Source: https://arxiv.org/abs/2602.11988, https://code.claude.com/docs/en/best-practices, https://developers.openai.com/codex/guides/agents-md, and https://agents.md/
- Tokens: +3.
- Toby practice at risk: both AGENTS.md examples in `references/examples.md` have a `Files` section, so they change too.

### C2. Offers to write more docs and tests

- Target: four Brownfield or finish paragraphs in `toby-swd-docs`, `toby-swd-experiment`, `toby-swd-complexity`, and `toby-swd-testing`.
- Toby's rule, from the docs skill:

  ```text
  If it does not, offer to create one with only the facts learned from the current change.
  ```

  The experiment skill says "Offer to create or update it". The complexity skill says "offer to record it in the nearest meaningful AGENTS.md". The testing skill says "offer a focused regression test".
- The other side: the last Self Review bullet in `base/toby.md` lists five report items and ends with "Report nothing else". An offer to write a file is none of the five. Gloaguen et al. found that model-written context files gave no average gain. The r1 judge on 2026-09-14 marked "I can also check whether that deploy changed a dependency version" as a closing offer (`evals/baselines/runs/2026-09-14-judge-r1.md`, line 103).
- Recommendation: the guide wins, so turn each offer into a risk line or delete it.
- Proposed text for the docs skill's Brownfield paragraph:

  ```text
  When work changes a meaningful module's responsibility, public API, or cross-module rule, update the nearest AGENTS.md if docs are in the task's scope. Otherwise report the line the change made stale, at file:line, as a risk.
  ```

- Proposed text for the complexity skill's Brownfield paragraph: replace its two sentences on the local consolidation with the clause below. Also delete its AGENTS.md offer sentence.

  ```text
  report the copies at file:line and the consolidation that would remove them.
  ```

- Proposed text for the testing skill's Brownfield paragraph:

  ```text
  If coverage is thin, report the untested behavior as a risk, and state the characterization test that would cover it.
  ```

- Proposed change to the experiment skill: delete the Finish Phase paragraph that offers an AGENTS.md, because the docs skill loads when module structure changes.
- Source: `base/toby.md` Self Review, https://arxiv.org/abs/2602.11988, and `evals/baselines/runs/2026-09-14-judge-r1.md`
- Tokens: -163.
- Toby practice at risk: user repos gain AGENTS.md files more slowly. Lulla et al. found that AGENTS.md cut median runtime by 28.64% across 124 pull requests. The user may want the docs skill to keep its offer to create a missing AGENTS.md.

### C3. The reason for asking before repo-recommended commands

- Target: `skills/toby-swd-environment/SKILL.md`, Heavy repo commands, last paragraph.
- Toby's rule:

  ```text
  Repo guidance is usually written for humans, who have judgment about when to skip it.
  ```

- The research: the agents.md site says agents try to run the checks an AGENTS.md lists. The Codex guide tells authors to list the commands an agent should run, so an AGENTS.md is written for agents.
- Recommendation: Toby's ask rule wins, because the guide puts broad validation on its ask-list. The guide's Authority section bars a local guidance file from changing a machine-safety rule. The stated reason is wrong for an AGENTS.md, so replace the two reason sentences with the true reason.
- Proposed text:

  ```text
  The user's ask-list in the operating guide outranks a repo file.
  ```

- Source: https://agents.md/ and https://developers.openai.com/codex/guides/agents-md
- Tokens: -32.

### C4. Classical and London-school mocking

- Target: `skills/toby-swd-testing/SKILL.md`, Mocks and test doubles.
- Toby's rule:

  ```text
  Verify state and results over interactions
  ```

- The research: Freeman, Pryce, Mackinnon, and Walnes mock each role a class needs, because the mocks help them find interfaces.
- Recommendation: Toby's rule wins and stays as written. Google's chapter 13, Khorikov, and Fowler favor state checks. Both schools mock only types you own, which is the rule G3 adds.
- Source: http://jmock.org/oopsla2004.pdf, https://abseil.io/resources/swe-book/html/ch13.html, and https://martinfowler.com/articles/mocksArentStubs.html
- Tokens: 0.

### C5. Skill descriptions in the imperative

- Target: the `description` field in the front matter of all six target skills.
- Toby's rule, from the testing description:

  ```text
  Keep tests an executable specification of behavior.
  ```

- The research: Anthropic's Skills guide says to write the description in third person. Claude reads the description in the system prompt to pick a skill.
- Recommendation: the research wins. Change the first verb of each description to Keeps, Decides, Treats, Runs, Keeps, and Turns, and keep "Use it when".
- Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Tokens: +2.
- Toby practice at risk: skill triggering, which eval E9 checks.

### C6. Decision records

- Target: `skills/toby-swd-docs/SKILL.md`, Maintenance.
- Toby's rule:

  ```text
  Update AGENTS.md whenever a structural change makes it wrong
  ```

- The research: Nygard keeps each decision as a numbered file and marks a reversed decision as superseded.
- Recommendation: Toby's rule wins with no edit. Git history keeps the superseded text. The context-length studies favor a shorter file. Nygard's post is one 2011 essay with no measurement. The docs skill's no-duplication rule already links an outside record.
- Source: https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions and https://arxiv.org/abs/2402.14848
- Tokens: 0.

## Rewrites

### R1. Testing skill opening

- Target: `skills/toby-swd-testing/SKILL.md`, the two paragraphs under the title (149 tokens).
- Current text, opening only:

  ```text
  Record what the system does in tests, so callers rely on it and regressions get caught. Tests make refactoring safe.
  ```

- Proposed text:

  ```text
  Tests record the behavior callers rely on, checked through the public interface. A refactor, a new feature, or a bug fix leaves existing tests unchanged. Only a change to required behavior edits an existing test, so a test that needs an edit during a refactor checks internals.
  ```

- Reason: Google's chapter 12 gives this four-way rule, so a model can check its own diff against it.
- Source: https://abseil.io/resources/swe-book/html/ch12.html
- Tokens: -80.
- Toby practice at risk: the lost-rules gate flags the sentence that lists call order and private signatures. Its survivor is "Do not import private modules, assert private state, or verify call order" in the next section.

### R2. Example tests and property tests

- Target: `skills/toby-swd-testing/SKILL.md`, How much to test.
- Current text:

  ```text
  Check a behavioral outcome by example (one named scenario) or by property (an invariant that holds over a range of generated inputs). Prefer whichever states the contract directly.
  ```

- Proposed text:

  ```text
  Default to named examples. Add a property test when the contract is a round trip, agreement with a simpler reference version, or an invariant.
  ```

- Reason: the Hypothesis tutorial suggests these three kinds of property, and a check that the code does not crash on valid input. Anthropic's Skills guide prefers one default with an exception over a choice between options.
- Source: https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html and https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Tokens: -10.

### R3. Snapshot review

- Target: `skills/toby-swd-testing/SKILL.md`, Narrow assertions.
- Current text:

  ```text
  An unread snapshot protects no behavior. Read the diff before accepting a snapshot update and confirm every change is intended, because an unread update is the same as deleting the test.
  ```

- Proposed text:

  ```text
  Read the diff before accepting a snapshot update, and confirm every change is intended, because accepting an unread update deletes the test.
  ```

- Reason: Jest's documentation asks reviewers to read snapshots like code. The first current sentence repeats the clause after "because".
- Source: https://jestjs.io/docs/snapshot-testing
- Tokens: -12.

### R4. Foil in the internal-mock red flag

- Target: `skills/toby-swd-testing/SKILL.md`, the fifth entry in Red flags.
- Current text:

  ```text
  - **Mock of an internal collaborator.** Verifies call sequence, not what the system produces.
  ```

- Proposed text:

  ```text
  - **Mock of an internal collaborator.** The test checks call order, so a refactor breaks it.
  ```

- Reason: Google's chapter 13 says interaction checks make tests brittle. The current entry is an "X, not Y" sentence, which the operating guide bans.
- Source: https://abseil.io/resources/swe-book/html/ch13.html and `base/toby.md` Banned Constructions
- Tokens: 0.

### R5. Timeout from a false-timeout rate

- Target: `skills/toby-swd-complexity/references/backend-apis.md`, example 3. The task did not list this file as a target.
- Current text:

  ```text
  A typical timeout is a few multiples of the downstream's P99 latency when it is healthy. If the healthy P99 is 50ms, 200ms is generous.
  ```

- Proposed text:

  ```text
  Set the timeout at the downstream's healthy p99.9 latency plus padding, so at most 0.1% of healthy calls time out.
  ```

- Reason: Amazon picks an acceptable false-timeout rate and sets the timeout from the matching latency percentile, which gives a model a number to compute.
- Source: https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter
- Tokens: -5.

### R6. One default experiment surface

- Target: `skills/toby-swd-experiment/SKILL.md`, Experiment Surface (110 tokens).
- Current text, opening only:

  ```text
  Make the experiment easy to run and read. Prefer a small surface that shows the values under test and the result they produce.
  ```

- Proposed text:

  ```text
  Default to a local script, or a labeled block in the nearest file, that prints the inputs, the candidate values, and the result. When the user tests in a running app, use a dev-only state panel or debug route.
  ```

- Reason: Anthropic's Skills guide recommends one default with an exception over a list of six options.
- Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Tokens: -58.
- Toby practice at risk: a fixture and a local flag leave this list, but Disposable Markings still lists both.

### R7. One experiment loop

- Target: `skills/toby-swd-experiment/SKILL.md`, Mode Contract and Iteration Loop.
- Current text, Mode Contract steps 1 to 3:

  ```text
  1. Inspect the current behavior and the smallest safe edit point.
  2. Pick one candidate change.
  3. Make the change reversible.
  ```

- Proposed change: delete the Mode Contract steps, and replace the Iteration Loop list with these steps.

  ```text
  1. Inspect the current behavior and the smallest safe edit point.
  2. Write down one candidate, then make one reversible change to a behavior, parameter, path, or surface.
  3. Report the changed value and what the user should observe.
  4. Ask the user to test, or run the smallest useful check.
  5. Record the result in the chat, then wait for feedback before the next candidate.
  ```

- Reason: the two six-step lists give the same loop twice. IFScale and Harada et al. found that models follow fewer of their instructions as the count rises.
- Source: https://arxiv.org/abs/2507.11538 and https://arxiv.org/abs/2509.21051
- Tokens: -66.

### R8. Pre-edit statement scaled to the diff

- Target: `base/toby.md`, Work Loop, bullets 2 and 3.
- Current text:

  ```text
  Use the live plan tool for non-trivial work when one is available. For tiny edits, an in-chat inspect/edit/verify list is enough.
  ```

- Proposed text, which replaces both bullets:

  ```text
  - Before editing, state the goal and the files you will touch. When the diff needs more than one sentence to describe, also state protected areas, task mode, and the smallest safe step. Use the live plan tool for that work when one is available.
  ```

- Reason: Anthropic's Claude Code guide says planning adds overhead and can be skipped when the diff fits in one sentence. The one-sentence test gives a model a threshold to check, which "tiny edits" lacks.
- Source: https://code.claude.com/docs/en/best-practices
- Tokens: -2.
- Toby practice at risk: a one-sentence edit no longer gets a stated protected area or task mode. The Work Modes bullet still classifies every task.

### R9. Inspecting an occupied port

- Target: `skills/toby-swd-environment/SKILL.md`, Ports (98 tokens).
- Current text, opening only:

  ```text
  If a port is occupied, a process is using it, so don't take the port. Inspect what's there
  ```

- Proposed text:

  ```text
  To inspect an occupied port, report the process ID, its command, and its start time, such as from `lsof -nP -i :PORT`.
  ```

- Reason: the Environment Safety section of `base/toby.md` already says to inspect, report, and ask before taking a port. The skill's red flag covers killing the process. The new sentence adds the fields to report.
- Source: `base/toby.md` Environment Safety, and https://code.claude.com/docs/en/best-practices on pruning lines
- Tokens: -68.
- Toby practice at risk: `lsof` runs on macOS and Linux only.

## Cuts

Every cut sentence below needs a survivor in the lost-rules gate, or a deletion recorded with `evals/run.py record` after someone reads the gate's report. Each cut follows Anthropic's advice to keep only what the model lacks, and the IFScale finding that compliance falls as instructions rise.

### K1. Repeated boundary sentences in the testing skill

- Target: `skills/toby-swd-testing/SKILL.md`, Test through public interfaces.
- Current text:

  ```text
  Test at the boundary. Those tests survive refactors, while internal tests break. … Mock external dependencies at the boundary, and keep internal collaborators real.
  ```

- Reason: R1 and Mocks item 3 state both rules.
- Tokens: -40.
- Toby practice at risk: the mock sentence was lost once before, so the gate must show item 3 as its survivor.

### K2. Experiment loops in the testing skill

- Target: `skills/toby-swd-testing/SKILL.md`, Experiment loops subsection.
- Current text:

  ```text
  Defer tests while the behavior is still being discovered, which covers `toby-swd-experiment`, feedback, proofs of concept, spikes, tuning, and exploration.
  ```

- Reason: the testing description skips throwaway spikes. The experiment skill's Testing Boundary gives the same rule. Khorikov supports test-last for exploratory work, so the rule stays in the experiment skill.
- Source: https://khorikov.org/posts/2022-01-24-test-first-vs-test-last-approaches/
- Tokens: -104.

### K3. Repeated internal-mock ban

- Target: `skills/toby-swd-testing/SKILL.md`, Mocks and test doubles.
- Current text:

  ```text
  Do not mock internal collaborators, because it couples tests to call sequences, so a refactor breaks them.
  ```

- Reason: item 3 limits mocks to outside systems. R4's red flag states the failure.
- Tokens: -27.

### K4. Complexity skill opening paragraph

- Target: `skills/toby-swd-complexity/SKILL.md`, the first paragraph.
- Current text:

  ```text
  Exception handling and performance optimization are two of the largest sources of complexity in any codebase.
  ```

- Reason: the research contains no measurement of that ranking. The paragraph gives no step, so the next paragraph, which states the rule, can open the skill.
- Tokens: -81.

### K5. Proportionality section

- Target: `skills/toby-swd-complexity/SKILL.md`, Proportionality.
- Current text:

  ```text
  The design-time steps are cheap and apply on every edit. Build a measurement harness, record baselines, and rebuild the critical path only for a stated performance requirement or a measured problem.
  ```

- Reason: "Add complexity only on evidence" and "When something is slow, measure" state the same rules. Knuth and Pike support those rules, which stay.
- Tokens: -89.

### K6. Environment skill opening paragraphs

- Target: `skills/toby-swd-environment/SKILL.md`, paragraphs 1 and 3.
- Current text:

  ```text
  The machine running this code is not yours. … An agent that ignores that discipline is useful only in a sandbox, so follow it in a real codebase.
  ```

- Reason: the first Environment Safety bullet in `base/toby.md` states the ownership rule. The sandbox claim has no source. The bold default in paragraph 2 stays.
- Tokens: -145.
- Toby practice at risk: the cut deletes the `pnpm dev` example in paragraph 3.

### K7. Duplicate process rules

- Target: `skills/toby-swd-environment/SKILL.md`, Long-running processes.
- Current text:

  ```text
  1. Say why you're starting it before you do.
  2. Track the command so you can stop the specific process later.
  3. Stop only what you started.
  ```

- Reason: the last Environment Safety bullet in `base/toby.md` gives the same four steps in one sentence.
- Tokens: -114.

### K8. Duplicate report list

- Target: `skills/toby-swd-environment/SKILL.md`, Reporting back.
- Current text:

  ```text
  After the task, report each of these that applies:
  ```

- Reason: the last Self Review bullet in `base/toby.md` lists the same report items. Its "anything incomplete or risky" covers the two items it lacks, tests skipped for safety and state changed outside scope.
- Tokens: -95.

### K9. Repeated approval scope

- Target: `skills/toby-swd-environment/SKILL.md`, Heavy repo commands.
- Current text:

  ```text
  Approval for the heavy command applies to that command in this task only. The next task needs a new approval.
  ```

- Reason: paragraph 2 of the same skill states the rule.
- Tokens: -28.

### K10. Trigger text in the experiment skill body

- Target: `skills/toby-swd-experiment/SKILL.md`, the opening sentence and the list of example prompts.
- Current text:

  ```text
  Use this skill when the work is exploratory and the user expects fast learning before durable implementation.
  ```

- Reason: Anthropic's Skills guide says Claude reads the description to choose a skill and loads the body afterward. Trigger text in the body therefore does nothing.
- Source: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices
- Tokens: -86.

### K11. Repeated abstraction rule and an unsupported claim in the docs skill

- Target: `skills/toby-swd-docs/SKILL.md`, Stay abstract on purpose, and one sentence in the AGENTS.md introduction.
- Current text:

  ```text
  An agent without an AGENTS.md has no record of these reasons, so it finds the gaps only when something breaks.
  ```

- Reason: the Maintenance section and the second red flag state the abstraction rule. Gloaguen et al. found no average task gain from context files, so the quoted claim has no support.
- Source: https://arxiv.org/abs/2602.11988
- Tokens: -111.

### K12. Duplicate review questions

- Target: `base/toby.md`, Self Review.
- Current text:

  ```text
  - Are unrelated files untouched?
  - Did the active skills set the engineering method, while the safety and verification rules in this file still applied?
  - Did the environment change, or is a process still running?
  - Are there any unstated assumptions?
  ```

- Reason: "Does the diff match the requested scope?" covers the first question. The Authority section covers the second. The final-message bullet asks for processes left running and assumptions waiting for confirmation, which covers the last two.
- Source: https://arxiv.org/abs/2507.11538 and https://arxiv.org/abs/2509.21051
- Tokens: -63.
- Toby practice at risk: the guide syncs to five instruction files, so the edit goes in `base/toby.md` and the instruction sync gate runs after it.

### K13. The turn-six claim

- Target: `base/toby.md`, Skill Routing, bullet 2.
- Current text:

  ```text
  A skill that has to be re-invoked each turn stops being applied around turn six.
  ```

- Reason: a repo search finds this sentence only in the guide and its copies. The `evals/` folder has no eval or run that measures it. The two sentences before it state the rule.
- Tokens: -20.
- Toby practice at risk: this cut assumes that no recorded run produced the number. If the user saw it in a session, cite that session in `evals/baselines` and keep the sentence.

### K14. Slogan in the feature-dev mode section

- Target: `skills/toby-feature-dev/SKILL.md`, Pick the mode first.
- Current text:

  ```text
  Two modes. Picking the wrong one is expensive either way.
  ```

- Reason: the bullets below list the two modes. The next sentence states the cost. The pair is a clipped run, which the operating guide bans.
- Tokens: -14.

## Aligned

- `toby-swd-testing`, Before deleting or weakening a test, the four-way classification, matches Google's chapter 12 and Beck's Canon TDD.
- `toby-swd-testing`, Test-first item 1, which reproduces a bug in a failing test first, matches Fowler's TestPyramid entry, Google's chapter 12, and Anthropic's guide.
- `toby-swd-testing`, "Skip test-first while the design is open", matches Khorikov's post on test-first and test-last.
- `toby-swd-testing`, Mocks items 1 and 2, real implementation first and a fake second, match Google's chapter 13.
- `toby-swd-testing`, "Verify state and results over interactions", matches Google's chapter 13 and Fowler's Mocks Aren't Stubs.
- `toby-swd-testing`, Each test is independent, matches Luo et al., who found test order behind 12% of flaky-test fixes.
- `toby-swd-testing`, "Reserve full-object equality and snapshots for when the whole structure is the contract", matches the Jest documentation and Dodds.
- `toby-swd-complexity`, "Never optimize on intuition" and "Record a baseline, change one thing, re-measure", match Knuth (1974) and Pike's rules.
- `toby-swd-complexity`, "At design time, always know what is expensive", matches Knuth's remark that an easy 12% speedup counts.
- `toby-swd-complexity`, the red flag on a circuit breaker for an unobserved problem, matches the Microsoft circuit breaker page and the Amazon Builders' Library.
- `references/backend-apis.md`, example 2, which passes the deadline in `ctx`, matches the SRE book.
- `references/caching.md`, examples 1 and 2, measurement before a cache and the cold-start cost, match Amazon's caching article.
- `toby-swd-environment`, the Narrow verification row, matches Anthropic's advice to give the agent a check that returns pass or fail.
- `toby-swd-environment`, the red flag "Updated snapshots wholesale", matches the Jest documentation.
- `toby-swd-experiment`, "run the loop with one change per result", matches Pike's measure-then-change rule.
- `toby-swd-experiment`, Testing Boundary, matches Khorikov's test-last advice for exploratory work.
- `toby-feature-dev`, the Check line with its failing result and the before-and-after runs, match Anthropic's Claude Code guide and Khorikov.
- `toby-feature-dev`, the tactical and strategic sizing and the Plan ceremony entry, match Anthropic's explore, plan, and code guidance.
- `toby-swd-docs`, the Constraints and Cross-module decisions sections, match Gloaguen et al. and Anthropic on recording only what the code cannot show.
- `toby-swd-docs`, "Leave out a section that has no fact to state", matches the Diataxis advice against empty sections.
- `toby-swd-docs`, one AGENTS.md per meaningful module root, matches the Codex guide's nested AGENTS.md files.
- `base/toby.md`, the Self Review voice-checker step, matches Anthropic's advice to put always-run steps in hooks. `hooks/voice-write-check.py` runs the checker on Claude Code, and the prose step covers hosts with no hook.
- `base/toby.md`, the voice sections placed before Work Loop, match the IFScale finding that models follow earlier instructions more often. Levy et al. and Anthropic found gains from putting the question last, so this evidence is mixed.

## Eval ideas

Each eval below waits for the user to agree to its design. Each one uses five samples per arm, because `evals/README.md` reports a two-run result that five runs reversed. Writers run on Haiku, except feature-dev tasks, which use Sonnet or Opus.

- **E1, for G1.** Give a `discount(total)` function with a seeded off-by-one bug and one spec sentence, and ask for pytest tests. Compare the current testing skill with the skill plus G1. Score the share of assertions whose expected value equals the buggy output. G1 ships if the current arm copies outputs in at least 2 of 5 runs and the G1 arm copies them less often.
- **E2, for G2.** Give a test that sleeps 50 ms before it reads a worker thread's result and fails about 1 run in 10. Ask for a fix. Score each fix as a longer sleep, a retry, or a wait on an event or a poll with a timeout. Record whether the writer read the code under test.
- **E3, for G4.** Give a payment client whose SDK config sets `max_network_retries=2`, with a POST that has no idempotency key. Ask for the call to survive brief outages. Score each run for a retry stacked on the SDK and for a POST retried with no idempotency key. Also score a call with no timeout and backoff with no jitter.
- **E4, for G6.** Give a bug-fix task whose first test run fails in a fixture before it reaches the bug. Score whether the writer reports that run as a reproduction of the bug.
- **E5, for G3.** Give a module that calls `requests.post` on a third-party API and reads its own Postgres through a repository. Ask for unit tests. Score whether the tests patch `requests` directly, mock the repository, or mock an adapter and use a real or fake database.
- **E6, for C1, G5, and K11.** Run swd suite task 1 before and after. Score whether the module's test command appears. Count the lines whose fact a file name or signature in the task already shows, and count total lines.
- **E7, for C2 and a new checker pattern.** Run feature-dev, swd, and real-suite tasks with and without the offer sentences. Count the replies that end in an offer. The candidate DECIDE pattern for `REPLY_PATTERNS` in `voice_rules.py` is `\b(want me to|would you like me to|I can also|I could also)\b`. It leaves out "should I", because the Environment Safety rules require questions such as "should I stop it?". Today it matches none of the 92 good rows and none of the 263 bad rows in `labels.jsonl`, `chat-tics.jsonl`, and `repo-review.jsonl`. In past runs it matches one sentence, the voice-s3 offer the r1 judge had marked. Before it ships, add that voice-s3 sentence to `chat-tics.jsonl` as a bad row. Then run the pattern on the next 10 voice-suite and real-suite samples that nobody has read. Label each match by hand. Ship it only with zero good-row matches and at least 4 of every 5 matches confirmed as offers.
- **E8, for all cuts.** Run the gates first, which include lost rules, body tokens, and co-load tokens. Then run the swd suite and the feature-dev sizing suite on both arms. The cuts ship when the scores from the current graders do not drop.
- **E9, for C5.** Run the triggering suite before and after the description change.
- **E10, for R8.** Run feature-dev sizing Request A, the copy change, and count the lines written before the first edit. The rewrite passes when a one-sentence diff gets only the goal and the files.
