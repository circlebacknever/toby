# Raw-material tasks

Eight outputs built from raw material: code, command output, a diff, and eval
results. The writer forms every sentence. No task hands over a finished
sentence to copy. Frozen on 2026-09-14 before any writer ran.

Use only what the material shows, plus arithmetic on it. Tasks 1 and 6 also
allow standard knowledge of the tools they name.

## 1. Explanation for a self-learner

The user writes: "what does an index on a database column actually do? I get
overwhelmed by walls of text"

Material, from Postgres on an `orders` table with 1,000,000 rows:

```
=> EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 4412;
 Seq Scan on orders  (cost=0.00..18334.00 rows=52 width=64) (actual time=0.412..96.301 rows=48 loops=1)
   Filter: (customer_id = 4412)
   Rows Removed by Filter: 999952
 Execution Time: 96.337 ms

=> CREATE INDEX orders_customer_id_idx ON orders (customer_id);
=> EXPLAIN ANALYZE SELECT * FROM orders WHERE customer_id = 4412;
 Index Scan using orders_customer_id_idx on orders  (cost=0.42..191.33 rows=52 width=64) (actual time=0.031..0.118 rows=48 loops=1)
   Index Cond: (customer_id = 4412)
 Execution Time: 0.141 ms
```

Write the chat reply.

## 2. Status report

The user writes: "how did round 3 go?"

Material, the eval harness output:

```json
{
  "round": 3,
  "magic_number_found": {"round_1": "0/5", "round_2": "1/3", "round_3": "3/3"},
  "flagged_MS_PER_DAY": 0,
  "future_timestamp_row": {
    "days_remaining": 91, "max_days": 90,
    "reviewer_1": "computed 91; not reported; note: 'cannot name what writes a future timestamp'",
    "reviewer_2": "computed 91; not reported; note: 'no caller writes a future atMs'",
    "reviewer_3": "reported the 91 as correct behavior"
  },
  "exception_list_edit": {
    "result": "3/3 reviewers raised a soft note to a hard finding",
    "cause": "rule toby-swd-clarity:51 absent from the review exception list",
    "change_since": "rule added to the exception list",
    "fixture_built": true,
    "fixture_run": false
  }
}
```

Write the chat reply.

## 3. Review finding

The diff adds this to `src/retention.ts`:

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

The reviewer ran a scratch script:

```
$ npx tsx scratch/boundary.ts
age 89d  daysRemaining=1   purgeable=false  consumed=false
age 90d  daysRemaining=0   purgeable=false  consumed=true
age 91d  daysRemaining=-1  purgeable=true   consumed=true
```

Write the review finding.

## 4. Commit message

Write the commit message for this staged diff:

```diff
--- a/scripts/install.sh
+++ b/scripts/install.sh
@@ -235,7 +235,7 @@ install_claude() {
   if [[ "$OUTPUT_STYLE" -eq 1 ]]; then
     # The style contains the writing rules, so CLAUDE.md leaves them out. Both
-    # together would put the same 6,400 tokens in front of every turn twice.
+    # together would put the same 6,900 tokens in front of every turn twice.
--- a/scripts/sync.sh
+++ b/scripts/sync.sh
@@ -97,7 +97,7 @@ def output_style(text: str) -> str:
 # The operating floor: everything the output style does not contain. Installing
 # the style and the full guide together pays for the writing sections twice, at
-# about 6,400 tokens a turn, so this is the half to pair with the style.
+# about 6,900 tokens a turn, so this is the half to pair with the style.
--- a/README.md
+++ b/README.md
@@ -74,7 +74,7 @@ nothing depends on remembering.
 The writing rules go in `CLAUDE.md`, or in an output style. Never both: that
-puts the same 6,400 tokens in front of every turn twice, which is what the flag
+puts the same 6,900 tokens in front of every turn twice, which is what the flag
@@ -110,7 +110,7 @@ write something before the style is on.
-| Resident tokens per turn | 9,124 | 9,312 (6,531 style, 2,781 `CLAUDE.md`) |
+| Resident tokens per turn | 9,555 | 9,744 (6,963 style, 2,781 `CLAUDE.md`) |
```

## 5. README install section

Write the `Install` section of the README: a short paragraph, then the commands.

Material:

```
$ scripts/install.sh --help
Usage: scripts/install.sh [--tool codex|claude|copilot|github|kiro|all] [--output-style] [--dry-run] [--force]
       github is an alias for copilot (GitHub Copilot CLI, ~/.copilot).

  --hooks         Install the voice checker and the two hooks to
                  ~/.claude/toby, then print the settings.json block to
                  paste. Does not edit settings.json itself.
  --output-style  Claude Code only. Install the writing rules as an output
                  style, and install the shorter CLAUDE.md that leaves them
                  out. Costs about 200 tokens more than the default, and
                  puts the rules in the system prompt. You must then turn
                  the style on: /config, Output style, Toby. Without that
                  step the voice rules are not loaded at all.

$ python3 scripts/token-budget.py | sed -n 6,9p
RESIDENT, every turn, before any skill fires
  operating guide                         9539
  18 skill descriptions                  2581
  default layout total                   12120
```

## 6. Failing test

The user writes: "tests fail on CI but pass on my machine??"

Material:

```
FAIL src/report/formatDate.test.ts
  ● formatDate › renders the statement date
    expect(received).toBe(expected)
    Expected: "2026-09-01"
    Received: "2026-08-31"
      12 |   const d = new Date("2026-09-01T00:30:00+02:00");
    > 13 |   expect(formatDate(d)).toBe("2026-09-01");

$ cat src/report/formatDate.ts
export const formatDate = (d: Date) => d.toISOString().slice(0, 10);

$ grep TZ .github/workflows/ci.yml
      TZ: UTC
$ echo $TZ
Europe/Berlin
```

Write the chat reply.

## 7. Naming complaint

The user writes: "All the names are so bizarre and confusing. BoundFlags (the
heck does that mean)"

Material:

```ts
// src/flags.ts
export type BoundFlags = { betaCheckout: boolean; newPricing: boolean };

export function bindFlags(req: Request): BoundFlags {
  return {
    betaCheckout: req.headers.get("x-beta-checkout") === "1",
    newPricing: req.headers.get("x-new-pricing") === "1",
  };
}

$ grep -rl BoundFlags src | wc -l
9
```

Write the chat reply.

## 8. Six replies in one session

Reply to each message in order, as six chat turns in the same session. The
material for each turn follows the message.

1. "One last thing to double check. Will we still generate plans as "Toby's plan
   for [...]"? That's also important to me to maintain the comedy"
   ```
   $ grep -n "Toby's plan for" base/toby.md
   247:- Write every plan as a markdown file. Title: `Toby's plan for [task]`, with a specific and plain task name.
   $ git log --oneline -S"Toby's plan for" -- base/toby.md
   33fa1cc toby adds skills
   ```
2. "what is CLAUDE-floor.md"
   ```
   $ ls instructions/claude
   CLAUDE-floor.md  CLAUDE.md
   $ sed -n 2p instructions/claude/CLAUDE-floor.md
   This file contains Toby's operating floor. The writing rules are in the Toby output style, which Claude Code loads into the system prompt.
   $ grep -n "floor" scripts/install.sh
   238:     install_instruction_file "$ROOT/instructions/claude/CLAUDE-floor.md" "$HOME/.claude/CLAUDE.md" merge
   ```
3. "I think it's strange that the voice checker depends on a different python
   file?"
   ```
   $ grep -n "voice_rules" scripts/voice-check.py scripts/validate-skills.py
   scripts/voice-check.py:35:import voice_rules as v  # noqa: E402
   scripts/validate-skills.py:14:from voice_rules import (  # noqa: E402
   ```
4. "Oh sorry, it looks like the app restarted to pick up an update.
   validate-skills is like an internal tool meant to test whether the skills are
   up to snuff. voice-check.py is like for other stuff outside"
   No new material.
5. "Hmm Maybe we should gitignore those or something? .DS_Store is always gonna
   be there"
   ```
   $ head -2 .gitignore
   # macOS clutter the validator hard-fails on
   .DS_Store
   $ sed -n 263p scripts/validate-skills.py
           return list(REPO_ROOT.rglob(".DS_Store"))
   ```
6. "Thanks Toby!"
   No material.
