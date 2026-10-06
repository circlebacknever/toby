# Code review research proposals

This file proposes edits to `toby-code-review` and `toby-simplify-code` from the code-review research. It lists one gap, six conflicts, two rewrites, and one cut. If the implementer applies every proposal, the two skills grow by about 10 tokens. Three of the six conflicts need no edit, because the current Toby rule wins.

Token changes are characters divided by 4, measured against the current files. The token-efficiency plan rewrites both skills in Groups 4 and 8, so each proposal also states where to apply it in the plan's target text. The research does not cover the simplify smell catalog, so it gives no reason to change the plan's Group 4 deletion of that file. The one-day response target and reviewer selection apply to human teams, so they get no proposal.

## Gaps

### G1. Hardening findings with no attack path

**Target.** `skills/toby-code-review/SKILL.md`, `## Don't flag`, as a new last bullet.

**Current.** The section has no such rule.

**Proposed.**

> - A missing hardening measure, such as a rate limit or an audit log, unless the diff removed it. Treat environment variables and CLI flags as trusted input.

**Evidence.** `/security-review` excludes denial of service, rate limiting, missing hardening, and missing audit logs. It treats environment variables and CLI flags as trusted. A request to a real route meets the Fires-when requirement, so the current skill text permits these findings.

**Sources.** https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/.claude/commands/security-review.md and https://code.claude.com/docs/en/code-review.

**Tokens.** +39.

**At risk.** A reviewer could mistake a resource bug for missing hardening and drop it. An example is an uncapped page size that the diff passes to a query, which eval E1 tests.

**Plan.** Add the bullet to `## Don't flag` in the Group 8 target body.

## Conflicts

### C1. When to recheck findings

**Target.** `skills/toby-code-review/SKILL.md`, line 56 in `## Evidence for each finding`, and line 67 in `## Four passes, each run to completion`.

**Current.** Line 56 says "More than a handful of findings means the list includes unproven suspicions." Line 67 says "The three-finding limit above applies to each pass on its own."

**Evidence.** The Claude Code review plugin starts one validation subagent per flagged bug and drops each bug the subagent does not validate. `/security-review` runs one false-positive filter per finding. Anthropic reports 7.5 findings on average for PRs over 1,000 lines. Engineers marked under 1% of its findings incorrect. ByteDance's filter raised precision from 54.50% to 67.12% in one configuration.

**Dispute.** Atlassian found its correctness judge had little effect. Cursor found its tool-calling reviewer too cautious.

**Recommendation.** The research wins. The current rule rechecks only a pass with more than three findings. Anthropic's figures contradict its claim that a long list contains unproven suspicions.

**Proposed.** Replace line 56 with the text below, and delete line 67.

> Before the report, recheck every finding. When you can start a subagent, give it one finding and the changed files, and ask it for the guard that makes the finding wrong. Report only the findings the recheck confirms.

**Sources.** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md, https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/.claude/commands/security-review.md, https://claude.com/blog/code-review, https://arxiv.org/html/2501.15134v1, https://arxiv.org/html/2601.01129v1, and https://cursor.com/blog/building-bugbot.

**Tokens.** −31.

**At risk.** A subagent with less context could reject a real finding, which lowers recall. The skill's precision rule accepts that cost. Line 60 still tells the reviewer to keep each pass's findings separate.

**Plan.** In the target body, replace "When one pass has more than three findings, recheck each against the three evidence lines." with the proposed text, and delete "The recheck counts each pass separately."

### C2. Small fixes as code blocks

**Target.** `skills/toby-code-review/SKILL.md`, `## Evidence for each finding`, line 50.

**Current.** "When the fix isn't plain, add one sentence that says how to fix it. Don't restate the code, because the author has the diff."

**Evidence.** In a study of 22,326 comments from 16 AI review GitHub Actions, short comments with code blocks led to more code changes. The Claude Code review plugin attaches a suggestion only when it fixes the whole issue. It describes a fix of six or more lines in words. The repo's design-review eval already counts findings with a concrete fix, in `evals/results/design-review-2026-09-25.md`.

**Dispute.** Google says the fix is the author's job. Meta found that reviewers took over 5% longer when shown AI patches. Both concern a human reviewer, while line 17 tells the reviewer to write each finding for the author.

**Recommendation.** The research wins for small fixes.

**Proposed.**

> State the fix in one sentence, or as a code block when five lines or fewer at one site fix the whole issue. Do not quote the current code back, because the author has the diff.

**Sources.** https://arxiv.org/html/2508.18771v1, https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md, https://google.github.io/eng-practices/review/reviewer/comments.html, and https://arxiv.org/abs/2507.13499v1.

**Tokens.** +13.

**At risk.** "Report problems and do not fix them" still holds, because a code block in the report changes no file.

**Plan.** In the target body, replace "End each finding with one sentence that states the fix, unless the Guard line already makes it plain, and do not restate the code." with the proposed text.

### C3. Severity labels

**Target.** `skills/toby-code-review/SKILL.md`, line 52.

**Current.** "Leave off P1/P2 labels, because a severity label is a claim about impact."

**Evidence.** Google labels comments `Nit`, `Optional`, or `FYI`. Claude Code Code Review labels findings `Important`, `Nit`, or `Pre-existing`. `/security-review` rates findings HIGH, MEDIUM, or LOW.

**Recommendation.** The skill rule wins, with no edit beyond the plan. Google's and Anthropic's labels tell the author whether a comment blocks merge. The plan's report sections give the author the same split. Those sections are findings, residual risk for pre-existing problems, and at most two cleanup candidates.

**Sources.** https://google.github.io/eng-practices/review/reviewer/comments.html, https://code.claude.com/docs/en/code-review, and https://raw.githubusercontent.com/anthropics/claude-code-security-review/main/.claude/commands/security-review.md.

**Tokens.** 0.

**At risk.** This edit removes no Toby practice.

**Plan.** The target body keeps this rule and adds the Residual risk and Cleanup candidates sections. This recommendation depends on both sections.

### C4. Missing-coverage findings

**Target.** `skills/toby-code-review/SKILL.md`, `## What to catch`, line 98.

**Current.** "Missing coverage: new behavior or a regression path with no useful test, including a bug fix that ships without a regression test."

**Evidence.** Claude Code Code Review skips missing test coverage by default. The Claude Code review plugin treats a lack of test coverage as a false positive unless CLAUDE.md requires tests. In Graphite's analysis of 10,000 comments, developers ignored requests to add tests.

**Dispute.** Google's checklist asks whether each test would fail when the code breaks.

**Recommendation.** The research wins in a narrow form. Keep the bug-fix case, and report other untested behavior only where the repo requires tests. The word "asserts" takes the place of "useful" and states Google's test.

**Proposed.**

> - Report a bug fix with no regression test. Report other new behavior that no test asserts only when the repo's guidance requires tests.

**Sources.** https://code.claude.com/docs/en/code-review, https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md, https://ai.engineer/talks/TswQeKftnaw-ai-powered-entomology-lessons-from-millions-ai, and https://google.github.io/eng-practices/review/reviewer/looking-for.html.

**Tokens.** +1.

**At risk.** In a repo with no test rule, the review stops enforcing the `toby-swd-testing` rule that a behavior change gets a test. The compliance pass still reports a criterion whose named check test is missing, so a review of the `review` suite's fixture still reports criteria 2 and 3.

**Plan.** Apply it to pass 1 in the target body, which reads "new behavior or a regression path with no useful test, and a bug fix without a regression test."

### C5. The design pass

**Target.** `skills/toby-code-review/SKILL.md`, `## Four passes, each run to completion`, line 65.

**Current.** "Ask what the change cost the next person to touch this code, and which document it left wrong."

**Evidence.** Claude Code Code Review, the Claude Code review plugin, and OpenAI's reviewer look for bugs and security problems by default. Graphite found that developers ignored requests to extract functions or add comments.

**Dispute.** In the RevMate study, reviewers accepted about 18% of refactoring comments and about 5% of functional ones. Atlassian's readability comments were among those resolved most often. Google's checklist covers design.

**Recommendation.** The skill rule wins, with no edit. The sources disagree. Graphite's ignored requests asked authors to extract functions or add comments, while each smell finding quotes a catalog criterion against the code. Eval E5 would show whether authors act on design findings.

**Sources.** https://code.claude.com/docs/en/code-review, https://alignment.openai.com/scaling-code-verification/, https://ai.engineer/talks/TswQeKftnaw-ai-powered-entomology-lessons-from-millions-ai, https://arxiv.org/html/2411.07091v1, https://arxiv.org/html/2601.01129v1, and https://google.github.io/eng-practices/review/reviewer/looking-for.html.

**Tokens.** 0.

**At risk.** This edit removes no Toby practice.

### C6. Praise for the author

**Target.** `AGENTS.md`, `## Five Tests`, test 2.

**Current.** "Delete a sentence that only introduces the next one, repeats an earlier one, or reacts to the reader's mood."

**Evidence.** Google asks reviewers to say what the author did well.

**Recommendation.** The guide's rule wins, with no edit. The research gives no data that praise changes what authors fix. The user's request says a reply that reads like default Claude is a failure.

**Sources.** https://google.github.io/eng-practices/review/reviewer/looking-for.html.

**Tokens.** 0.

**At risk.** This edit removes no Toby practice.

## Rewrites

### R1. A test that asserts the touched behavior

**Target.** `skills/toby-simplify-code/SKILL.md`, `## Behavior drift`, line 68.

**Current.** "Ship a change only when a test covers the touched path and passes."

**Proposed.**

> Ship a change only when a passing test asserts the touched behavior.

**Evidence.** Google's guide asks reviewers to confirm that each test would fail when the code breaks. Under the current wording, a test that runs the line and checks nothing counts as cover.

**Sources.** https://google.github.io/eng-practices/review/reviewer/looking-for.html.

**Tokens.** +1.

**At risk.** This edit removes no Toby practice.

**Plan.** The target body keeps the current sentence, so apply the rewrite there.

### R2. The PR description

**Target.** `skills/toby-code-review/SKILL.md`, `## Scope`, line 30.

**Current.** "For a PR, inspect the PR metadata and diff with the tools available."

**Proposed.**

> - For a PR, read its title and description before the diff.

**Evidence.** The Claude Code review plugin gives every review agent the PR title and description, so each agent has the author's stated intent. Bacchelli and Bird found that understanding the reason for a change was the hardest part of review. Google's guide tells reviewers to read the description first.

**Sources.** https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/code-review/commands/code-review.md, https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf, and https://google.github.io/eng-practices/review/reviewer/navigate.html.

**Tokens.** −3.

**At risk.** This edit removes no Toby practice.

**Plan.** The target body cuts this line. Keep the rewritten line there, because the research supports it.

## Cuts

### K1. One finding on a trivial diff

**Target.** `skills/toby-code-review/SKILL.md`, `## Final report`, line 123.

**Current.** "A trivial diff gets at most one finding."

**Evidence.** The research caps only nits, such as the cap of about five per review that Anthropic's REVIEW.md docs suggest. The skill already caps cleanup candidates at two. A trivial diff with two real bugs would lose one of them under this cap.

**Sources.** https://code.claude.com/docs/en/code-review.

**Tokens.** −10.

**At risk.** This cut removes no Toby practice, because the precision rules already keep a trivial diff's report short.

**Plan.** The target body keeps this sentence, so cut it there.

## Aligned

### toby-code-review

- **Precision over recall** (Disposition). GitHub's Copilot posts nothing on 29% of reviews. OpenAI says developers bypass a reviewer they see as noisy.
- **An empty review** (Disposition, line 22). The research supports the plan's wording, "a complete report". The current wording, "the normal result", is wrong for large diffs, because Anthropic's reviewer finds issues on 84% of PRs over 1,000 lines.
- **Callers outside the diff** (Scope). OpenAI reports that repo-wide context finds more critical issues with fewer false positives than diff-only review.
- **Pre-existing problems** (Scope). The skill reports a pre-existing problem only when it affects the change. Claude Code Code Review reports every one, while the Claude Code review plugin drops every one.
- **Consequence at file:line** (Evidence). In the GitHub Actions study, tools that commented on whole files led to fewer code changes than tools that commented on hunks.
- **Fires when** (Evidence). `/security-review` requires an exploit scenario for each finding.
- **Guard search** (Evidence). The Claude Code review plugin and `/security-review` run a similar check in a separate subagent for each finding. C1 adds that subagent step.
- **Four passes**. Claude Code Code Review runs several agents that each look for a different class of issue.
- **Quoted repo rule** (What to catch, line 100). The Claude Code review plugin reports a CLAUDE.md break only when the agent can quote the exact rule.
- **Linter nits** (Don't flag). The Claude Code review plugin and Anthropic's example REVIEW.md skip what a linter, formatter, or type checker reports.
- **Two cleanup candidates** (Don't flag). Anthropic's REVIEW.md docs suggest a cap such as five nits per review.
- **Report only** (line 15). Claude Code Code Review never approves or blocks a PR, because Anthropic leaves approval to a person.
- **Design no worse than before** (The design pass). Google's guide tells reviewers to approve a change once it improves the overall health of the code.
- **Speculative generality** (`references/smells.md`). Google asks reviewers to reject code written for problems the author only guesses might come later.

### toby-simplify-code

- **Formatting a tool handles** (Not a simplification). Bacchelli and Bird recommend that tools check conventions, so reviewers can look for deeper problems.
- **The edge and test for each change** (Final response). SmartBear says authors find their own errors while they annotate a change. Bacchelli and Bird found that reviewers respond faster when the author gives context.
- **A bug found while cleaning** (Out of scope). The rule asks for the trigger input and the missed guard, which matches the exploit scenario `/security-review` requires.

## Eval ideas

None of these evals runs before the user agrees the design. Review evals use the writer the user picks in the token-efficiency plan's question 10, because the user does not use Haiku for code review.

- **E1, for G1.** Write a fixture diff with three changes. It adds an endpoint with no rate limit and reads a file path from an environment variable. It also passes the request's page size to a query with no cap. A review passes when it reports the uncapped query and neither of the other two. Run three reviews per arm, and count the reviews that pass.
- **E2, for C1.** Write two fixtures. The first has code that looks like a bug, but middleware in an unchanged file guards it, so a passing review leaves it out. The second seeds five real bugs, so a passing review reports all five.
- **E3, for C2.** Run the `review` suite and the design-review fixture. A person then checks each code block against its finding. A review passes when every block fixes its finding in five lines or fewer, with no block for a fix at two sites.
- **E4, for C4.** Add a private helper with no test to `evals/fixtures/export.diff`. Pair the diff with a repo sketch whose guidance has no test rule. A review passes when it leaves the helper out and still reports criteria 2 and 3.
- **E5, for C5.** The user marks each finding from the `review` and design-review runs as fix or ignore. Group the marks by pass. ByteDance and Google remove checks that authors ignore, so a pass with mostly ignored findings would be a candidate to narrow.
- **E6, for R1.** Give `toby-simplify-code` a function whose only test asserts the HTTP status, where the likely cleanup changes the response body for an empty input. A run passes when the agent leaves that change or states the missing assertion.
- **E7, for review size.** Seed one bug in the last file of a diff with more than 600 changed lines. Count detections across runs. SmartBear found that human reviewers find fewer defects past 400 lines. The research has no recall figure by diff size for a model reviewer. A drop in detection would support a rule to review a large diff in file groups.
