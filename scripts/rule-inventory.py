#!/usr/bin/env python3
"""Every prose sentence in the skill tree, normalized and sorted, filename dropped.

Diff two runs and a moved rule shows as no change. A deleted rule shows as a
missing line. That is the only guard the plan has against a consolidation pass
quietly losing a sentence nobody reads for six months.
"""
from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")
validate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validate)

WHITESPACE_RE = re.compile(r"\s+")
LEADING_MARKER_RE = re.compile(r"^(?:[-*>]|\d+[.)])\s+")
PUNCT_RE = re.compile(r"[^a-z0-9 ]")


def normalize(sentence: str) -> str:
    """Lowercase, strip punctuation and list markers, collapse whitespace.

    Reflowing a paragraph or turning a bullet into a table cell must not read as
    a deleted rule, so the normal form keeps words and drops everything else.
    """
    text = LEADING_MARKER_RE.sub("", sentence.strip()).lower()
    text = PUNCT_RE.sub(" ", text)
    return WHITESPACE_RE.sub(" ", text).strip()


def paths() -> list[Path]:
    files = sorted((REPO_ROOT / "skills").rglob("*.md"))
    # The voice reference is a byte copy of the operating guide. Counting it
    # would report every guide rule twice and hide a real deletion in the noise.
    copy = REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md"
    return [p for p in files if p != copy]


def sentences(path: Path) -> list[str]:
    text = path.read_text()
    out: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "```")):
            continue
        if stripped.startswith("|"):
            # A paragraph rewritten as a table keeps its rules. Read the cells,
            # or every table rewrite reports as a pile of deletions.
            cells = [c.strip() for c in stripped.strip("|").split("|")]
            if all(set(c) <= set("-: ") for c in cells):
                continue
            stripped = ". ".join(c for c in cells if c)
        for sentence in validate.sentences_in(stripped):
            norm = normalize(sentence)
            if len(norm.split()) >= 4:
                out.append(norm)
    return out


def main() -> int:
    targets = paths()
    if len(sys.argv) > 1 and not sys.argv[1].startswith("-"):
        targets = [Path(a).resolve() for a in sys.argv[1:]]
    rules: list[str] = []
    for path in targets:
        rules.extend(sentences(path))
    for rule in sorted(rules):
        print(rule)
    print(f"# {len(rules)} sentences, {len(set(rules))} distinct", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
