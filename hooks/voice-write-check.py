#!/usr/bin/env python3
"""Claude Code PostToolUse hook: check prose the agent just wrote.

The Stop hook reads the reply. This one reads the file. Between them, every
word Toby produces passes the same rules, which is what the operating guide
claims and what nothing enforced before.

It fires after Write and Edit on a markdown file, runs the FIX group from
scripts/voice-check.py, and exits 2 with the findings. The write already
happened, so this is feedback rather than a block, and the agent gets it while
the file is still the thing it is working on.

Wire it up in settings.json, alongside the Stop hook:

    {"hooks": {
      "PostToolUse": [{"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "python3 /abs/path/hooks/voice-write-check.py"}]}],
      "Stop": [{"hooks": [
        {"type": "command", "command": "python3 /abs/path/hooks/voice-stop-check.py"}]}]}}

It needs the repo to find scripts/voice-check.py. Set TOBY_ROOT, or leave the
hook inside a checkout. Without either it exits 0 and says nothing, because a
hook that fails loudly on a machine that never asked for it gets deleted.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

PROSE_SUFFIXES = {".md", ".markdown", ".mdx", ".txt"}


def find_repo() -> Path | None:
    named = os.environ.get("TOBY_ROOT")
    if named and (Path(named) / "scripts" / "voice-check.py").exists():
        return Path(named)
    for parent in Path(__file__).resolve().parents:
        if (parent / "scripts" / "voice-check.py").exists():
            return parent
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

    repo = find_repo()
    if repo is None:
        return 0

    result = subprocess.run(
        [sys.executable, str(repo / "scripts" / "voice-check.py"), str(target), "--fix-only"],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return 0

    print(f"Voice rules broken in {target.name}. Fix these before moving on.", file=sys.stderr)
    print(result.stdout.strip(), file=sys.stderr)
    print("Every one of these is a rule with no judgement in it.", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
