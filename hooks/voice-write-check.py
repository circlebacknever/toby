#!/usr/bin/env python3
"""Claude Code PostToolUse hook: check prose the agent just wrote.

The Stop hook reads the reply. This one reads the file.

It fires after Write and Edit on a markdown or text file, and it runs
scripts/voice-check.py with --no-read. When the checker reports a FIX or a
DECIDE finding, the hook exits 2 and prints the findings. The write has already
happened when the hook runs, so the hook undoes nothing. The agent gets the
findings while it is still working on the file.

The patterns miss 7 of the 49 bad sentences in evals/gold/labels.jsonl.
The hook leaves out the READ list, because the same 15 rules would print after
every write. The Self Review step in base/toby.md tells the agent to read the
file against that list before it finishes.

Wire it up in settings.json, alongside the Stop hook:

    {"hooks": {
      "PostToolUse": [{"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "python3 /abs/path/hooks/voice-write-check.py"}]}],
      "Stop": [{"hooks": [
        {"type": "command", "command": "python3 /abs/path/hooks/voice-stop-check.py"}]}]}}

It looks for scripts/voice-check.py in TOBY_ROOT, then in a checkout that holds
this hook, then in the installed skill at ~/.claude/skills/toby-voice. Without
any of those it exits 0 and says nothing, because a hook that fails loudly on a
machine that never asked for it gets deleted.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PROSE_SUFFIXES = {".md", ".markdown", ".mdx", ".txt"}


def find_checker() -> Path | None:
    """Return the first complete voice checker, or None.

    A checker counts only with voice_rules.py beside it. An old install left
    ~/.claude/toby/scripts/voice-check.py on its own, and that copy crashes.
    """
    roots = []
    named = os.environ.get("TOBY_ROOT")
    if named:
        roots.append(Path(named))
    roots.extend(Path(__file__).resolve().parents)
    roots.append(Path.home() / ".claude" / "skills" / "toby-voice")
    for root in roots:
        checker = root / "scripts" / "voice-check.py"
        if checker.exists() and (root / "scripts" / "voice_rules.py").exists():
            return checker
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if payload.get("hook_event_name") != "PostToolUse":
        return 0

    path = (payload.get("tool_input") or {}).get("file_path")
    if not path or Path(path).suffix.lower() not in PROSE_SUFFIXES:
        return 0
    target = Path(path)
    if not target.exists():
        return 0

    checker = find_checker()
    if checker is None:
        return 0

    result = subprocess.run(
        [sys.executable, str(checker), str(target), "--no-read"],
        capture_output=True,
        text=True,
    )
    # Exit 0 or 1 is a finished check. Any other code means the checker failed.
    # An older installed checker fails this way, because it has no --no-read
    # flag. A failed check says nothing about the file, so the hook stays silent.
    if result.returncode not in (0, 1):
        return 0
    if result.returncode == 0 and "DECIDE  (" not in result.stdout:
        return 0

    print(f"voice-check.py found voice breaks in {target.name}. Rewrite each FIX sentence, "
          "and answer each DECIDE sentence.",
          file=sys.stderr)
    print(result.stdout.strip(), file=sys.stderr)
    print("These patterns miss 7 of the 49 bad sentences in the gold set. Before you finish the task, run "
          "voice-check.py on the file and read every sentence against the READ list it prints.",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
