#!/usr/bin/env python3
"""Claude Code Stop hook: read the finished reply, block on literal voice breaks.

Every other check in this repo reads a file. This one reads a reply, which is
the only surface the voice actually ships on. It greps for the forms the file
checker misses: an invented foil written as `X, not Y`, and a trailing rider.

It fires on literal strings only. A heuristic here would fire on clean replies,
and a hook that fires on clean replies gets disabled inside a week.

Wire it up in settings.json:

    {"hooks": {"Stop": [{"hooks": [{"type": "command",
      "command": "python3 /absolute/path/hooks/voice-stop-check.py"}]}]}}

Input: the Stop hook payload on stdin, carrying transcript_path.
Output: exit 0 to allow. Exit 2 with a reason on stderr to block, which hands
the reason back to the agent for one repair pass.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# Literal forms only. Each one is a break no wording rescues.
PATTERNS = [
    (re.compile(r",\s+not\s+(?:a|an|the|just|only|because|to|for|from|in|on|by|its|his|her|their|my|your)\b"),
     "invented foil `X, not Y` — state the thing directly"),
    (re.compile(r"—\s*not\s"), "invented foil after a dash — state the thing directly"),
    (re.compile(r"\bit'?s not\s+[^.,\n]{0,40},\s*it'?s\b", re.I), "`it's not X, it's Y` — state the thing directly"),
    (re.compile(r"\bnot just\b"), "`not just` — say what it is"),
    (re.compile(r"\brather than\b"), "`rather than` — name the thing you chose"),
    (re.compile(r",\s*though\.?\s*$", re.M), "trailing `though` — a rider on a sentence that landed"),
    (re.compile(r"\bthat said,", re.I), "`that said` — a rider on a sentence that landed"),
    (re.compile(r"\b(?:hope this helps|feel free|let me know if|don't hesitate)\b", re.I),
     "relational performance — cut the closing offer"),
]

# Words used outside their everyday meaning. Kept in step with COINED_TERMS in
# scripts/validate-skills.py, which checks the same rule against files. This one
# checks it against the reply, which is the only surface no file check reaches.
COINED = [
    "first-read", "blast radius", "surface area", "load-bearing", "north star",
    "forcing function", "cognitive surface", "affordance", "the shape of the work",
]

# Figurative frames, kept in step with FIGURATIVE_FRAMES in validate-skills.py.
# A sentence cannot wear a hat, and the file checks never see a reply.
FRAMES = [
    "wearing a", "wears a", "dressed as", "in disguise", "masquerading as",
    "with a new hat", "under the hood", "pretending to be",
]

# The prose ceiling is 25 words. The hook fires at 40, well past it, because a
# hook that argues about a 27-word sentence gets switched off.
SENTENCE_LIMIT = 40

# Fenced code, inline code, and quoted user text are not Toby's prose.
FENCE_RE = re.compile(r"```.*?```", re.S)
INLINE_RE = re.compile(r"`[^`\n]*`")
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
    for pattern in (FENCE_RE, INLINE_RE, QUOTE_RE):
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

    hits = []
    for pattern, reason in PATTERNS:
        match = pattern.search(reply)
        if match:
            hits.append(f"{match.group(0).strip()!r}: {reason}")

    for frame in FRAMES:
        match = re.search(rf"(?<![A-Za-z]){re.escape(frame)}(?![A-Za-z])", reply, re.I)
        if match:
            hits.append(f"{match.group(0)!r}: figurative frame, say what the thing is")

    for term in COINED:
        match = re.search(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", reply, re.I)
        if match:
            hits.append(f"{match.group(0)!r}: invented term, say it in everyday words")

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
