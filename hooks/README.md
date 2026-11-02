# Hooks

The repo has three voice checks, because each one checks text that the other two don't see.

| Mechanism | Reads | Catches |
|---|---|---|
| `scripts/voice-check.py` | any file, a directory, or stdin | the full pattern list, on demand, plus the rules the patterns don't check |
| `voice-write-check.py` | a file the agent just wrote | the hard set, as each file is written |
| `voice-stop-check.py` | the reply the agent just sent | the hard set, in chat, which no file check sees |

## The hard set

Both hooks run `hook_patterns()` from `scripts/voice_rules.py`: the hard banned words, the tic and label forms, clause welds, and two length ceilings (40 words per sentence, 3 sentences per paragraph). That set is what is wrong on every reading. Style preferences (contrastive foils and litotes) stay in the on-demand checker, where a person decides them, because a hook that fires on a clean reply gets switched off inside a week.

The Stop hook's reprompt is one short paragraph: resend under a `## Revised reply` heading, fix the listed lines, keep every fact. It never asks for a rewrite of the whole reply, because a longer repair instruction produces a longer, more tedious reply.

## Run the checker by hand

```sh
scripts/voice-check.py draft.md --review
scripts/voice-check.py skills/
some-command | scripts/voice-check.py -
```

`--review` prints every prose sentence with its findings under it. Without it, the checker prints the findings and the READ list, the rules the patterns don't check.

## Wire up the hooks

Run `scripts/install.sh --hooks --write-settings` to copy the hooks to `~/.claude/toby/hooks`, back up `~/.claude/settings.json` to `settings.json.bak`, and merge the hook entries. Run `scripts/install.sh --hooks` without `--write-settings` to print this block with the paths filled in, or add it to `~/.claude/settings.json` by hand:

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

Both exit 2 on a hard break, which puts the findings in front of the agent. The write hook fires after the write, so the agent gets the findings while it is still working on the file. The Stop hook fires after the reply, so the agent gets one repair pass, and two at most when `stop_hook_active` is set.

The hooks look for `voice_rules.py` in `TOBY_ROOT/scripts`, then in a checkout that holds the hook, then in the installed skill at `~/.claude/skills/toby-voice/scripts`. Installing with `--tool claude` puts it there, so you don't need to set anything. With none of those the hooks exit 0 and say nothing.

## Testing them

```sh
python3 tests/test-voice-hook.py
```

Seeded breaks must be caught, and ordinary replies must pass untouched. A false positive fails the run.
