#!/usr/bin/env python3
"""Claude Code Stop hook: read the finished reply, block on literal voice breaks.

Every other check in this repo reads a file. This one reads the reply the agent
just sent. It runs REPLY_PATTERNS, FIGURATIVE_FRAMES, and COINED_TERMS from
scripts/voice_rules.py, so this hook and voice-check.py both use a pattern
added there.

It fires on literal strings only. A heuristic here would fire on clean replies,
and a hook that fires on clean replies gets disabled inside a week.

Wire it up in settings.json:

    {"hooks": {"Stop": [{"hooks": [{"type": "command",
      "command": "python3 /absolute/path/hooks/voice-stop-check.py"}]}]}}

It looks for voice_rules.py in TOBY_ROOT/scripts, then in a checkout that holds
this hook, then in the installed skill at ~/.claude/skills/toby-voice/scripts.
Without any of those it exits 0 and says nothing.

Input: the Stop hook payload on stdin, containing transcript_path.
Output: exit 0 to allow. Exit 2 with a reason on stderr to block, which hands
the reason back to the agent for one repair pass.
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


# The prose ceiling is 25 words. The hook fires at 40, well past it, because a
# hook that argues about a 27-word sentence gets switched off.
SENTENCE_LIMIT = 40

# Fenced code, inline code, and quoted text are not Toby's prose. A reply quotes
# a sentence to report on it, such as a sentence the user flagged, and the rules
# exempt exact quotes.
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_RE = re.compile(r"`[^`\n]*`")
DOUBLE_QUOTE_RE = re.compile(r'"[^"\n]{1,300}"|\u201c[^\u201d\n]{1,300}\u201d')
QUOTE_RE = re.compile(r"^>.*$", re.M)


def last_assistant_text(transcript: Path) -> str:
    """Return the text of the final assistant message in the transcript."""
    text = ""
    for line in transcript.read_text(errors="ignore").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        message = event.get("message") or {}
        if message.get("role") != "assistant":
            continue
        content = message.get("content")
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            parts = [b.get("text", "") for b in content if isinstance(b, dict) and b.get("type") == "text"]
            if any(parts):
                text = "\n".join(parts)
    return text


def prose_only(text: str) -> str:
    for pattern in (FENCE_RE, INLINE_RE, QUOTE_RE, DOUBLE_QUOTE_RE):
        text = pattern.sub(" ", text)
    return text


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except ValueError:
        return 0
    if payload.get("stop_hook_active"):
        return 0
    path = payload.get("transcript_path")
    if not path or not Path(path).exists():
        return 0

    reply = prose_only(last_assistant_text(Path(path)))
    if not reply.strip():
        return 0

    rules_dir = find_rules_dir()
    if rules_dir is None:
        return 0
    sys.path.insert(0, str(rules_dir))
    import voice_rules as v

    hits = []
    for pattern, reason in v.REPLY_PATTERNS:
        match = pattern.search(reply)
        if match:
            hits.append(f"{match.group(0).strip()!r}: {reason}")

    for frame, pattern in v.FIGURATIVE_RE:
        match = pattern.search(reply)
        if match:
            hits.append(f"{match.group(0)!r}: figurative frame, say what the thing is")

    for term, pattern in v.COINED_RE:
        match = pattern.search(reply)
        if match:
            hits.append(f"{match.group(0)!r}: invented term, {v.COINED_TERMS[term]}")

    for sentence in re.split(r"(?<=[.!?])\s+", reply):
        words = len(sentence.split())
        if words > SENTENCE_LIMIT:
            hits.append(f"a {words}-word sentence: the ceiling is 25, so split it")
            break

    if not hits:
        return 0

    print("Voice break in the reply just sent. Rewrite those sentences and send again:", file=sys.stderr)
    for hit in hits:
        print(f"  - {hit}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
