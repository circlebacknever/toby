#!/usr/bin/env python3
"""Score a written reply against the voice checks in validate-skills.py.

Same rules, pointed at an output file instead of the skill tree. Reports banned
words, invented foils, over-length sentences, and clause welds.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")
v = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v)

WELD_RE = re.compile(r"\w\s+—\s+\w|\w;\s+\w")
BARE_PRONOUN_RE = re.compile(r"\b(This|That)\s+(is|was|means|makes|leaves|gets|costs|holds)\b")


def score(path: Path) -> dict:
    raw = path.read_text()
    text = v.prose_only(raw)
    tiers = v.load_banned_words()
    banned, foils, long_sentences, welds, pronouns = [], [], [], [], []

    for word in tiers["hard"]:
        pattern = re.compile(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", re.I)
        for match in pattern.finditer(text):
            banned.append(f"{match.group(0)!r}:{v.line_for_offset(text, match.start())}")
    for pattern in v.CONTRAST_PATTERNS:
        for match in pattern.finditer(text):
            foils.append(f"{match.group(0)!r}:{v.line_for_offset(text, match.start())}")
    for number, line in enumerate(text.splitlines(), 1):
        if not v.is_prose_line(line):
            continue
        for sentence in v.sentences_in(line.strip()):
            count = len(sentence.split())
            if count > v.SENTENCE_CEILING:
                long_sentences.append(f"{count}w:{number}")
        for _ in WELD_RE.finditer(line):
            welds.append(str(number))
        for _ in BARE_PRONOUN_RE.finditer(line):
            pronouns.append(str(number))

    words = len(text.split())
    return {
        "file": path.name,
        "words": words,
        "banned": banned,
        "foils": foils,
        "long": long_sentences,
        "welds": welds,
        "pronouns": pronouns,
        "defects": len(banned) * 3 + len(foils) * 2 + len(long_sentences) + len(welds) + len(pronouns),
    }


def main() -> int:
    for arg in sys.argv[1:]:
        r = score(Path(arg))
        print(f"{r['file']}: {r['words']} words, defect score {r['defects']}")
        for key in ("banned", "foils", "long", "welds", "pronouns"):
            if r[key]:
                print(f"  {key}: {', '.join(r[key])}")
        if not r["defects"]:
            print("  clear")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
