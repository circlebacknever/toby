# Content tasks

This suite has six tasks: a platform overview, slide copy, contributor rules, a commit message, a review finding, and six chat replies in a row. Each task gives all the facts the output needs, so a writer that invents a fact fails the task. `scripts/voice-check.py` and the `content-judge` prompt both evaluate the outputs, because regex patterns don't catch every unnatural or slogan-like sentence.

## 1. Platform overview

Write the top of the README for Relay: a title, an opening paragraph of at most 80 words, then two sections (`Install` and one about writing a plugin) with one short paragraph each.

Facts:

- Relay is a platform for building multi-agent apps.
- It ships two packages: `@relay/ui` provides shared generative UI components, and `@relay/agents` provides the runtime for tool calling, memory, and human approval before destructive actions.
- Users give agents instructions, and agents read documents, call tools, and wait for a person to approve any destructive action.
- Developers add new agents as plugins. Each plugin is a JSON manifest plus handler functions, and Relay compiles the manifest at build time.
- Model providers are swappable, and plugin handlers call the active provider through `ctx.engine`.
- Install with `npm install @relay/ui @relay/agents` on Node 20 or later.

## 2. Deck

Write five slides for engineering leadership proposing to move scheduled jobs from cron scripts to a queue service. For each slide write a title sentence, a subtitle only when it adds new information, and two or three bullets.

Facts:

- 43 cron scripts run today on two hosts that don't have an assigned owner.
- 6 cron scripts failed silently last quarter, including the invoice export, which stopped running for 9 days before a customer reported it.
- The queue service retries a failed job 3 times and pages the on-call engineer when the third retry fails.
- The migration runs in 3 phases over 6 weeks, starting with the highest-risk jobs.
- The queue service costs $400 a month.

## 3. Contributor rules

Write the "Adding a plugin" section of `AGENTS.md` in Relay's `plugins/` directory for an agent adding a new plugin.

Facts:

- Each plugin is a directory, `plugins/<name>/`, that contains `manifest.json` and `handlers.ts`.
- A plugin must not import from `engines/`. The build rejects direct engine imports with `E_ENGINE_IMPORT`, because direct imports broke every plugin the last time a provider changed its SDK.
- Handlers call the model provider through `ctx.engine`.
- Run `npm run plugins:check` before opening a PR to validate every manifest.

## 4. Commit message

Phase 1 of the queue migration from task 2 is complete. You moved the 8 highest-risk cron jobs (including invoice export) to the queue service, deleted their crontab entries, and added a test asserting that the invoice export pages on-call after its third failed attempt. Write the commit message.

## 5. Review finding

The diff adds this code to `api/webhooks.ts` at line 41:

```ts
try {
  await processEvent(req.body);
} catch (err) {
  logger.warn(err);
}
res.status(200).send();
```

The payment provider stops retrying a webhook as soon as it receives HTTP 200. Write the review finding.

## 6. Six replies in one session

Reply to each message in order, as six chat turns in the same session, using only the facts below each message.

1. "what does the `--dry-run` flag on the installer do?"
   It prints every file copy and merge the installer would perform, without writing any files.
2. "ok ran it. it wants to overwrite my CLAUDE.md, is that safe?"
   The file already contains the Toby marker block, so the installer replaces only the text between the markers and leaves the rest untouched.
3. "lol my CLAUDE.md is 900 lines, it's basically a novel. which parts are mine?"
   Lines 1 to 610 are the user's text, and lines 611 to 900 are the Toby block.
4. "tests are failing again and I've been at this for two hours"
   `scripts/test-install.sh` fails with `installed skill differs: toby-voice/SKILL.md`, because `~/.claude/skills/toby-voice/SKILL.md` has a local edit that isn't in the repo.
5. "is it fixed?"
   You ran `scripts/install.sh --force` and reran `scripts/test-install.sh`, which passed. You haven't run `evals/run.py gates` yet.
6. "I think we should just delete the validator, it's slowing me down"
   The validator runs in 1.9 seconds, and last week the gates that run it caught 3 regressions before merge.
