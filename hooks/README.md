# Hooks

Three mechanisms, because each one reaches a surface the others cannot.

| Mechanism | Reads | Catches |
|---|---|---|
| `scripts/voice-check.py` | any file, a directory, or stdin | everything, on demand |
| `voice-write-check.py` | a file the agent just wrote | prose in files, as it lands |
| `voice-stop-check.py` | the reply the agent just sent | prose in chat, which no file check sees |

## Run the checker by hand

```sh
scripts/voice-check.py draft.md
scripts/voice-check.py skills/
some-command | scripts/voice-check.py -
```

It prints two groups. **FIX** holds rules with no judgement in them, and exits
1. **DECIDE** holds rules a machine cannot settle, prints the sentence, and
never fails the run. Most DECIDE findings are real, so read each one.

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

Both exit 2 on a break, which puts the findings in front of the agent. Neither
blocks: `PostToolUse` fires after the write, and `Stop` fires after the reply.
Feedback while the work is still in hand is what they buy.

The write hook needs to find `scripts/voice-check.py`. Installed by `--hooks` it
finds it next door in `~/.claude/toby`, so nothing needs setting. Running from a
checkout works the same way. Anywhere else, set `TOBY_ROOT`. With none of those
it exits 0 and says nothing, because a hook that fails loudly on a machine that
never asked for it gets deleted.

## What each one costs you

The stop hook fires on literal strings and a 40-word sentence. The ceiling is
25, and it fires at 40 on purpose, because a hook that argues about a 27-word
sentence gets switched off. Its fixtures hold 24 ordinary replies that must pass
silently, and that half matters more than the seeded breaks.

The write hook runs the FIX group only. DECIDE findings need a person, and a
hook cannot ask.

## Testing them

```sh
python3 tests/test-voice-hook.py
```

Seeded breaks must be caught, and ordinary replies must pass untouched. A false positive
fails the run.
