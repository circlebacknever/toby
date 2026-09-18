# Hooks

Three mechanisms, because each one reaches a surface the others cannot.

| Mechanism | Reads | Catches |
|---|---|---|
| `scripts/voice-check.py` | any file, a directory, or stdin | every pattern, on demand, followed by the rules the patterns do not check |
| `voice-write-check.py` | a file the agent just wrote | prose in files, as each file is written |
| `voice-stop-check.py` | the reply the agent just sent | prose in chat, which no file check sees |

## Run the checker by hand

```sh
scripts/voice-check.py draft.md --review
scripts/voice-check.py skills/
some-command | scripts/voice-check.py -
```

`--review` prints every prose sentence with its findings under it, for the
sentence-by-sentence read the READ rules need.

It prints three groups. **FIX** holds rules with no judgement in them, and a
FIX finding makes the run exit 1. **DECIDE** holds rules a machine cannot
settle. The checker prints each DECIDE sentence, and a DECIDE finding never
fails the run. Most DECIDE findings are real, so read each one.
**READ** lists the rules the patterns do not check. Every run prints it. The
patterns miss 7 of the 49 bad sentences in `evals/gold/labels.jsonl`, so
after you handle the findings, read every sentence against the READ list.

Ask for a voice pass and this is the tool to run. Improvising a grep each time
finds a different subset each time.

## Wire up the hooks

Run `scripts/install.sh --hooks --tool claude` and it prints this block with the
paths filled in. To write it by hand, add this to `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          { "type": "command", "command": "python3 /abs/path/to/toby/hooks/voice-write-check.py" }
        ]
      }
    ],
    "Stop": [
      {
        "hooks": [
          { "type": "command", "command": "python3 /abs/path/to/toby/hooks/voice-stop-check.py" }
        ]
      }
    ]
  }
}
```

Both exit 2 on a break, which puts the findings in front of the agent. The
write hook fires after the write, so the agent gets the findings while it is
still working on the file. The Stop hook fires after the reply, so the agent
gets one pass to repair it.

The write hook needs `scripts/voice-check.py`. It looks in `TOBY_ROOT`, then in
a checkout that holds the hook, then in the installed skill at
`~/.claude/skills/toby-voice`. Installing with `--tool claude` puts the checker
there, so nothing needs setting. With none of those it exits 0 and says nothing,
because a hook that fails loudly on a machine that never asked for it gets
deleted.

## What each one costs you

The stop hook fires on literal strings and a 40-word sentence. The ceiling is
25, and it fires at 40 on purpose, because a hook that argues about a 27-word
sentence gets switched off. Its fixtures hold 24 ordinary replies that must pass
silently, and that half matters more than the seeded breaks.

The write hook reports FIX and DECIDE findings. It exits 2 on either
group. It runs the checker with `--no-read`, because printing the READ list
after every write repeats 15 rules the agent already has.

## Testing them

```sh
python3 tests/test-voice-hook.py
```

Seeded breaks must be caught, and ordinary replies must pass untouched. A false positive
fails the run.
