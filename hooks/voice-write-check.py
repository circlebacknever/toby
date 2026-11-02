#!/usr/bin/env python3
"""Claude Code PostToolUse hook: flag hard voice breaks in a file just written.

It fires after Write and Edit on a markdown or text file and runs
hook_patterns() from voice_rules.py over the prose in the file. Exit 2 prints
the findings. The write has already happened when the hook runs, so the hook
undoes nothing; the agent gets the findings while it is still working on the
file.

The hook blocks only what is wrong on every reading, never a judgement call,
so a valid rewrite never traps the agent in a repeat-edit loop. The full
pattern list stays available on demand as scripts/voice-check.py --review.

Wire it up in settings.json, alongside the Stop hook:

    {"hooks": {
      "PostToolUse": [{"matcher": "Write|Edit", "hooks": [
        {"type": "command", "command": "python3 /abs/path/hooks/voice-write-check.py"}]}],
      "Stop": [{"hooks": [
        {"type": "command", "command": "python3 /abs/path/hooks/voice-stop-check.py"}]}]}}

It looks for voice_rules.py in TOBY_ROOT/scripts, then in a checkout that holds
this hook, then in the installed skill at ~/.claude/skills/toby-voice/scripts.
Without any of those it exits 0 and says nothing, because a hook that fails
loudly on a machine that never asked for it gets deleted.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.dont_write_bytecode = True

PROSE_SUFFIXES = {".md", ".markdown", ".mdx", ".txt"}
CLI_CLEAN_RE_STR = r"\b(?:make|git|cargo|npm|yarn|pnpm|gradle|mvn|go|brew)\s+clean\b"


def find_rules_dir() -> Path | None:
    """Return the first scripts folder that holds voice_rules.py, or None."""
    roots = []
    named = os.environ.get("TOBY_ROOT")
    if named:
        roots.append(Path(named))
    roots.extend(Path(__file__).resolve().parents)
    roots.append(Path.home() / ".claude" / "skills" / "toby-voice")
    for root in roots:
        if (root / "scripts" / "voice_rules.py").exists():
            return root / "scripts"
    return None


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if payload.get("hook_event_name") != "PostToolUse":
        return 0

    tool_input = payload.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("path")
    if not path or Path(path).suffix.lower() not in PROSE_SUFFIXES:
        return 0
    target = Path(path)
    if not target.exists():
        return 0

    rules_dir = find_rules_dir()
    if rules_dir is None:
        return 0
    sys.path.insert(0, str(rules_dir))
    import re

    import voice_rules as v

    text = v.prose_only(target.read_text(errors="ignore"))
    hits = []
    cli_clean = re.compile(CLI_CLEAN_RE_STR, re.I)
    for pattern, label in v.hook_patterns():
        for match in pattern.finditer(text):
            if label == "banned word" and match.group(0).lower() == "clean" and cli_clean.search(
                text[max(0, match.start() - 10) : match.end() + 2]
            ):
                continue
            hits.append(f"{match.group(0).strip()!r}: {label}")
    for match in v.WELD_RE.finditer(text):
        line_end = text.find("\n", match.start())
        line_text = text[text.rfind("\n", 0, match.start()) + 1 : len(text) if line_end == -1 else line_end]
        if v.is_prose_line(line_text) or (v.LIST_ITEM_RE.match(line_text) and ";" in match.group(0)):
            hits.append(f"{match.group(0).strip()!r}: clause weld")

    # The same two ceilings the Stop hook applies to a reply. A file with
    # a 45-word sentence is the tedium the write hook exists to catch.
    for line, paragraph in v.prose_paragraphs(text):
        sentences = v.sentences_in(paragraph)
        for sentence in sentences:
            words = sentence.split()
            if len(words) > v.HOOK_SENTENCE_LIMIT:
                hits.append(
                    f"the {len(words)}-word sentence starting {' '.join(words[:6])!r}: over {v.HOOK_SENTENCE_LIMIT} words"
                )
        if len(sentences) > v.HOOK_PARAGRAPH_LIMIT:
            hits.append(
                f"the {len(sentences)}-sentence paragraph at line {line} starting "
                f"{' '.join(paragraph.split()[:6])!r}: over {v.HOOK_PARAGRAPH_LIMIT} sentences"
            )

    # A long bullet buries its point too, and prose_paragraphs skips list items.
    for number, line in enumerate(text.splitlines(), 1):
        item = v.LIST_ITEM_RE.match(line)
        if not item:
            continue
        for sentence in v.sentences_in(item.group(1)):
            words = sentence.split()
            if len(words) > v.HOOK_SENTENCE_LIMIT:
                hits.append(
                    f"the {len(words)}-word bullet at line {number} starting "
                    f"{' '.join(words[:6])!r}: over {v.HOOK_SENTENCE_LIMIT} words"
                )

    if not hits:
        return 0

    print(f"voice hook found {len(set(hits))} hard break(s) in {target.name}. Fix them in one edit:", file=sys.stderr)
    for hit in dict.fromkeys(hits):
        print(f"  - {hit}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
