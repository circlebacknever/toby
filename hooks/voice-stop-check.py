#!/usr/bin/env python3
"""Claude Code Stop hook: read the finished reply, block on the hard voice breaks.

The hook runs hook_patterns() from scripts/voice_rules.py, the small set that is
wrong on every reading: the hard banned words, the tic and label forms, clause
welds, and the two length ceilings. scripts/voice-check.py keeps the full
pattern list, including style preferences, for on-demand audits. This hook
fires on literal strings only, because a hook that blocks a clean reply gets
switched off inside a week.

Wire it up in settings.json:

    {"hooks": {"Stop": [{"hooks": [{"type": "command",
      "command": "python3 /absolute/path/hooks/voice-stop-check.py"}]}]}}

It looks for voice_rules.py in TOBY_ROOT/scripts, then in a checkout that holds
this hook, then in the installed skill at ~/.claude/skills/toby-voice/scripts.
Without any of those it exits 0 and says nothing.

Input: the Stop hook payload on stdin, containing transcript_path.
Output: exit 0 to allow. Exit 2 with a short reprompt on stderr to block, which
hands the reason back to the agent for one repair pass.
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

sys.dont_write_bytecode = True


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


# A sentence ends at terminal punctuation, even inside bold such as "fixed.**",
# and at a blank line or a new list item, so a label line ending in a colon is
# not joined to the bullet below it.
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\**\s+|\n\s*\n|\n(?=\s*(?:[-*]|\d+\.)\s)")

# The reprompt stays short on purpose. A long list of repair rules makes the
# rewrite longer, and a longer rewrite is the tedium this hook exists to cut.
REPROMPT = """Rewrite the reply and send it again under a `## Revised reply` heading on its own line. Fix the lines below, keep every fact, number, command, path, and URL, and change nothing else.
Lines to fix:"""

# Fenced code, inline code, and quoted text are not Toby's prose. A reply quotes
# a sentence to report on it, such as a sentence the user flagged, and the rules
# exempt exact quotes.
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_RE = re.compile(r"`[^`\n]*`")
DOUBLE_QUOTE_RE = re.compile(r'"[^"\n]{1,300}"|“[^”\n]{1,300}”')
QUOTE_RE = re.compile(r"^>.*$", re.M)
# A table row is cells, not a sentence, so it never counts toward the length check.
TABLE_RE = re.compile(r"^\s*\|.*$", re.M)
CLI_CLEAN_RE = re.compile(r"\b(?:make|git|cargo|npm|yarn|pnpm|gradle|mvn|go|brew)\s+clean\b", re.I)


def assistant_messages(transcript: Path) -> list[str]:
    """Return the text of each assistant message in the transcript."""
    messages: list[str] = []
    for line in transcript.read_text(errors="ignore").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        message = event.get("message") or {}
        if message.get("role") != "assistant":
            continue
        content = message.get("content")
        if isinstance(content, str) and content.strip():
            messages.append(content)
        elif isinstance(content, list):
            parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
            if any(parts):
                messages.append("\n".join(parts))
    return messages


def prose_only(text: str) -> str:
    for pattern in (FENCE_RE, INLINE_RE, QUOTE_RE, TABLE_RE, DOUBLE_QUOTE_RE):
        text = pattern.sub(" ", text)
    return text


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    path = payload.get("transcript_path")
    if not path or not Path(path).exists():
        return 0

    msgs = assistant_messages(Path(path))
    if not msgs:
        return 0
    # Allow at most two rewrite passes when stop_hook_active is set, so a first
    # "## Revised reply" that still has a hard break is caught once more without
    # risking an infinite loop.
    if payload.get("stop_hook_active"):
        revised_streak = 0
        for msg in reversed(msgs):
            if "## Revised reply" in msg:
                revised_streak += 1
            else:
                break
        if revised_streak >= 2:
            return 0

    reply = prose_only(msgs[-1])
    if not reply.strip():
        return 0

    rules_dir = find_rules_dir()
    if rules_dir is None:
        return 0
    sys.path.insert(0, str(rules_dir))
    import voice_rules as v

    # Every match is listed, because a list that stops at the first hit tells
    # the agent the fix is local and complete.
    hits = []
    for pattern, label in v.hook_patterns():
        for match in pattern.finditer(reply):
            if label == "banned word" and match.group(0).lower() == "clean" and CLI_CLEAN_RE.search(
                reply[max(0, match.start() - 10) : match.end() + 2]
            ):
                continue
            hits.append(f"{match.group(0).strip()!r}: {label}")

    for match in v.WELD_RE.finditer(reply):
        before = reply[max(reply.rfind("\n", 0, match.start()), reply.rfind(". ", 0, match.start())) + 1 : match.start() + 1]
        if v.LABEL_DASH_RE.match(before.strip() + " —") and "—" in match.group(0):
            continue
        line_end = reply.find("\n", match.start())
        line_text = reply[reply.rfind("\n", 0, match.start()) + 1 : len(reply) if line_end == -1 else line_end]
        if v.is_prose_line(line_text) or (v.LIST_ITEM_RE.match(line_text) and ";" in match.group(0)):
            hits.append(f"{match.group(0).strip()!r}: clause weld")

    for sentence in SENTENCE_SPLIT_RE.split(reply):
        words = sentence.split()
        if len(words) > v.HOOK_SENTENCE_LIMIT:
            hits.append(f"the {len(words)}-word sentence starting {' '.join(words[:6])!r}: over {v.HOOK_SENTENCE_LIMIT} words")

    # A paragraph past three sentences buries separate points, which a list
    # shows one at a time.
    for block in re.split(r"\n\s*\n", reply):
        lines = [line for line in block.splitlines() if line.strip()]
        if not lines or any(re.match(r"\s*(?:[-*]|\d+[.)]|#)", line) for line in lines):
            continue
        count = len([s for s in re.split(r"(?<=[.!?])\s+", " ".join(lines)) if s.strip()])
        if count > v.HOOK_PARAGRAPH_LIMIT:
            hits.append(f"the {count}-sentence paragraph starting {' '.join(block.split()[:6])!r}: over {v.HOOK_PARAGRAPH_LIMIT} sentences")

    if not hits:
        return 0

    print(REPROMPT, file=sys.stderr)
    for hit in dict.fromkeys(hits):
        print(f"  - {hit}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
