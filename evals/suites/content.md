# Content tasks

Six outputs that invite the slogan register: a platform overview, deck titles,
contributor rules, a commit, a review finding, and six chat replies in a row.
Each task gives every fact the output needs, so a writer who invents a fact has
broken the task. `scripts/voice-check.py` and a judge agent both read the
results, because the checker cannot see a grating sentence made of legal words.

## 1. Platform overview

Write the top of the README for Relay: a title, an opening paragraph of at most
80 words, then two sections, `Install` and one about writing a plugin, with one
short paragraph each.

Facts:

- Relay is a platform for building multi-agent apps.
- It ships two packages. `@relay/ui` holds shared generative UI components.
  `@relay/agents` holds the runtime: tool calling, memory, and pauses for human
  approval before a destructive action.
- Users give agents instructions. Agents read documents, call tools, and wait
  for a person to approve anything destructive.
- A new agent is a plugin. A plugin is a JSON manifest plus handler functions,
  and Relay compiles the manifest at build time.
- Model providers are swappable engines. Plugins never import an engine directly.
- Install with `npm install @relay/ui @relay/agents`. Node 20 or later.

## 2. Deck

Five slides for engineering leadership, proposing to move scheduled jobs from
cron scripts to a queue service. For each slide write a title, a subtitle only
if it adds information, and two or three bullets.

Facts:

- 43 cron scripts run today, on two hosts nobody owns.
- 6 of them failed silently last quarter. One was the invoice export, which was
  missing for 9 days before a customer noticed.
- The queue service retries a job 3 times and pages the on-call engineer on the
  final failure.
- Migration runs in 3 phases over 6 weeks, highest-risk jobs first.
- The service costs $400 a month.

## 3. Contributor rules

Write the "Adding a plugin" section of `AGENTS.md` in Relay's `plugins/`
directory, for an agent adding a new plugin.

Facts:

- Each plugin is a directory, `plugins/<name>/`, that contains `manifest.json` and `handlers.ts`.
- A plugin must not import from `engines/`. The build fails the plugin with
  `E_ENGINE_IMPORT`, because engine imports broke every plugin the last time a
  provider changed its SDK.
- Handlers receive the engine through `ctx.engine`.
- Run `npm run plugins:check` before opening a PR. It validates every manifest.

## 4. Commit message

Phase 1 of the queue migration from task 2 is done. You moved the 8
highest-risk cron jobs, invoice export included, to the queue service, deleted
their crontab entries, and added a test asserting that the invoice export pages
after its third failed attempt. Write the commit message.

## 5. Review finding

The diff adds this to `api/webhooks.ts` at line 41:

```ts
try {
  await processEvent(req.body);
} catch (err) {
  logger.warn(err);
}
res.status(200).send();
```

The payment provider stops retrying a webhook once it gets a 200. Write the
review finding.

## 6. Six replies in one session

Reply to each message in order, as six chat turns in the same session. Facts for
each turn follow the message.

1. "what does the `--dry-run` flag on the installer do?"
   It prints every copy and merge the install would make, and writes nothing.
2. "ok ran it. it wants to overwrite my CLAUDE.md, is that safe?"
   The file already has the Toby marker block, so only the text between the
   markers is replaced.
3. "lol my CLAUDE.md is 900 lines, it's basically a novel. which parts are mine?"
   Lines 1 to 610 are the user's, and lines 611 to 900 are the Toby block.
4. "tests are failing again and I've been at this for two hours"
   `scripts/test-install.sh` fails with `installed skill differs:
   toby-voice/SKILL.md`. The cause is a hand edit in
   `~/.claude/skills/toby-voice/SKILL.md` that the repo does not have.
5. "is it fixed?"
   You reinstalled with `--force` and reran `scripts/test-install.sh`, which
   passed. You did not run `evals/run.py gates`.
6. "I think we should just delete the validator, it's slowing me down"
   The validator takes 1.9 seconds, and last week the gates that read its
   output caught 3 regressions before they shipped.
