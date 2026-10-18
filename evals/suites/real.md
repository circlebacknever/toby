# Real tasks

This suite has eight tasks taken from the user's own sessions in this repo. We froze these tasks on 2026-09-14 before changing the rules they test. Each task gives all the facts the output needs, and a writer that invents a fact fails the task. Task 1 also allows standard school mathematics.

## 1. Explanation for a self-learner

The user writes: "Can you explain what a function is in mathematics? I'm teaching myself and I get overwhelmed by walls of text."

Facts:

- A function takes an input and gives exactly one output for each input.
- `f(x) = 2x` gives 6 for the input 3.
- A rule that sends the input 4 to both 2 and -2 isn't a function.
- The set of allowed inputs is called the domain.

## 2. Status report with bad news

The user asked for the results of the third verification round on the code review skill. Write the chat report.

Facts:

- Reviewers found the magic number in 0 of 5 runs in round 1, 1 of 3 in round 2, and 3 of 3 in round 3, and none of them flagged the named constant `MS_PER_DAY`.
- A row with a future timestamp gets 91 days remaining against a 90-day maximum. Two of three reviewers computed 91 and dropped the finding because they couldn't name a caller that writes a future timestamp, while the third reviewer called 91 correct.
- An earlier edit told reviewers to check the exception list before flagging. All three reviewers then turned a soft note into a hard finding, because the rule from `toby-swd-clarity:51` was missing from that list.
- You added the rule to the exception list and built a test fixture for it, and you haven't run the fixture yet.

## 3. Trade-off before approval

The user is about to approve a plan item. Write the chat reply that states its token cost before they approve it.

Facts:

- The plan item makes code review check whether a changed rule in `skills/` contradicts a rule in another skill.
- That check loads two skills at the same time.
- Group 2 of the same plan reduces how often skills load together.
- The check runs only when the diff touches `skills/`, so ordinary code reviews don't load extra skills.

## 4. README install section

Write the `Install` section of the README: one short paragraph followed by the commands.

Facts:

- `scripts/install.sh --tool claude` installs the full `CLAUDE.md` (7,443 tokens) without an output style.
- `scripts/install.sh --tool claude --output-style` installs the Toby output style (5,042 tokens) and a shorter `CLAUDE.md` (2,601 tokens), totaling 7,643 tokens.
- Installing the full `CLAUDE.md` and the output style together loads 12,485 tokens.
- Claude Code puts the output style in the system prompt and repeats it during long sessions.
- To turn the style on, open `/config`, choose Output style, then choose Toby.
- The installer doesn't edit `~/.claude/settings.json`. To enable the Stop hook, add `python3 /absolute/path/hooks/voice-stop-check.py` under `hooks.Stop` in `~/.claude/settings.json`.

## 5. Review finding

The diff adds this code to `src/retention.ts`:

```ts
52  daysRemaining(row: AuditRow, nowMs: number): number {
53    const ageDays = Math.floor((nowMs - row.atMs) / MS_PER_DAY);
54    return 90 - ageDays;
55  }
...
63  purgeable(nowMs: number): AuditRow[] {
64    return this.store.all().filter((r) => this.daysRemaining(r, nowMs) < 0);
65  }
...
68  utilizationPct(nowMs: number): number {
69    const rows = this.store.all();
70    const consumed = rows.filter((r) => this.daysRemaining(r, nowMs) <= 0).length;
71    return Math.round((consumed / rows.length) * 100);
72  }
```

Write the review finding for the day-90 boundary. A reviewer ran both methods on a row exactly 90 days old: `purgeable` returned `false`, and `utilizationPct` counted the row as consumed.

## 6. Commit message

Write the commit message.

Facts:

- You rebuilt all 18 zips in `dist/` from `skills/`.
- Passing `zip -x '*.DS_Store'` excluded `.DS_Store` files from the zips.
- When unzipped together, the archives match `skills/` byte for byte.

## 7. Naming complaint

The user writes: "All the names are so bizarre and confusing. BoundFlags (the heck does that mean). Oh it means request flags related to the incoming request."

Facts:

- `BoundFlags` is a type that holds the feature flags read from the incoming request.
- You haven't renamed `BoundFlags` yet.

Write the chat reply.

## 8. Six replies in one session

Reply to each message in order, as six chat turns in the same session, using the facts below each message.

1. "One last thing to double check. Will we still generate plans as \"Toby's plan for [...]\"? That's also important to me to maintain the comedy"
   The Plan Format section of `base/toby.md` requires the title `Toby's plan for [task]`, and this session didn't change that line.
2. "what is CLAUDE-floor.md"
   `scripts/sync.sh` generates `instructions/claude/CLAUDE-floor.md` with the operating sections that the output style omits (authority, plans, skill routing, environment safety, work loop, and self review). The `--output-style` install copies it to `~/.claude/CLAUDE.md`.
3. "I think it's strange that the voice checker depends on a different python file?"
   Both `scripts/voice-check.py` and `scripts/validate-skills.py` import `scripts/voice_rules.py`.
4. "Oh sorry, it looks like the app restarted to pick up an update. validate-skills is like an internal tool meant to test whether the skills are up to snuff. voice-check.py is like for other stuff outside"
   If each script kept its own copy of the rules, editing one copy would leave the other out of sync. You haven't changed either file.
5. "Hmm Maybe we should gitignore those or something? .DS_Store is always gonna be there"
   `.gitignore` already lists `.DS_Store`, and the validator fails on any tracked `.DS_Store` file.
6. "Thanks Toby!"
   No facts.
