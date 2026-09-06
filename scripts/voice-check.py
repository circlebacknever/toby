#!/usr/bin/env python3
"""Find voice problems in any text, and say what to do about each one.

Run this instead of inventing a grep. It runs every check the repo has, against
a file, a directory, or stdin, and prints the sentence at fault with the rule it
breaks.

    scripts/voice-check.py draft.md
    scripts/voice-check.py skills/toby-explain/SKILL.md
    pr-description | scripts/voice-check.py -

Findings come in two groups, because the two need different handling.

FIX     A rule with no judgement in it. A banned word is banned. A dash welding
        two clauses is a weld. Do not argue with these, and do not call them
        false positives. Rewrite the sentence.

DECIDE  A rule a machine cannot settle. `shape` is banned as a significance flag
        and fine as a noun for an actual shape. The check prints the sentence so
        you can answer for that sentence. Most of these are real. Read each one
        and say which it is, and never dismiss the group.

Exit 1 when anything lands in FIX. DECIDE never fails the run.
"""
from __future__ import annotations

import argparse
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
CLOSING_OFFER_RE = re.compile(
    r"\b(hope this helps|let me know if|feel free|don'?t hesitate|happy to help|reach out)\b", re.I
)


def sentence_at(text: str, offset: int) -> str:
    """The sentence containing an offset, for showing the writer what to rewrite."""
    start = max(text.rfind(". ", 0, offset), text.rfind("\n", 0, offset)) + 1
    end = min(
        [x for x in (text.find(". ", offset), text.find("\n", offset)) if x != -1] or [len(text)]
    )
    return " ".join(text[start : end + 1].split())[:200]


def defines_the_rules(path: str) -> bool:
    """True for a file that states the banned words rather than obeying them.

    base/toby.md lists every banned word, so scanning it for them returns 107
    findings and teaches the reader that the tool is noise. The validator has
    always known this; the checker did not, until it was pointed at the guide.
    """
    try:
        resolved = Path(path).resolve()
    except OSError:
        return False
    return resolved in {p.resolve() for p in v.VOICE_SCAN_EXEMPT if p.exists()}


def findings(raw: str, label: str, defining: bool = False) -> tuple[list[str], list[str]]:
    text = v.prose_only(raw)
    tiers = v.load_banned_words()
    fix: list[str] = []
    decide: list[str] = []

    def add(bucket, rule, offset, note):
        line = v.line_for_offset(text, offset)
        bucket.append(f"{label}:{line}  {rule}\n      {sentence_at(text, offset)}\n      -> {note}")

    if not defining:
        for word in tiers["hard"]:
            for m in re.finditer(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", text, re.I):
                add(fix, f"banned word {m.group(0)!r}", m.start(), "cut it, or rewrite the sentence around it")
        for pattern in v.CONTRAST_PATTERNS:
            for m in pattern.finditer(text):
                add(fix, f"invented foil {m.group(0)!r}", m.start(), "state the thing directly, rule 12")
        for term, pattern in v.COINED_RE:
            for m in pattern.finditer(text):
                add(fix, f"coined term {m.group(0)!r}", m.start(), f"{v.COINED_TERMS[term]}, rule 14")
        for frame, pattern in v.FIGURATIVE_RE:
            for m in pattern.finditer(text):
                add(fix, f"figurative frame {m.group(0)!r}", m.start(), "say what the thing is, no metaphor")
        for m in CLOSING_OFFER_RE.finditer(text):
            add(fix, f"closing offer {m.group(0)!r}", m.start(), "delete it, the reply ends at the answer")
    for m in WELD_RE.finditer(text):
        if v.is_prose_line(text[text.rfind("\n", 0, m.start()) + 1 : text.find("\n", m.start())]):
            add(fix, "clause weld", m.start(), "name the relation: because, so, after, rule 7")

    if not defining:
        for word in tiers["sense"]:
            for m in re.finditer(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", text, re.I):
                add(decide, f"sense-scoped {m.group(0)!r}", m.start(),
                    "banned as a significance flag, fine as a plain noun. Which is it here?")
    for m in BARE_PRONOUN_RE.finditer(text):
        add(decide, f"bare {m.group(1).lower()!r}", m.start(),
            "say the noun after it unless the reference is unmistakable, rule 9")

    for number, line in enumerate(text.splitlines(), 1):
        if not v.is_prose_line(line):
            continue
        for sentence in v.sentences_in(line.strip()):
            count = len(sentence.split())
            if count > 35:
                fix.append(f"{label}:{number}  sentence runs {count} words\n"
                           f"      {' '.join(sentence.split())[:200]}\n"
                           f"      -> split it, the ceiling is 25, rule 1")
            elif count > 25:
                decide.append(f"{label}:{number}  sentence runs {count} words\n"
                              f"      {' '.join(sentence.split())[:200]}\n"
                              f"      -> over the 25 ceiling. Cut a clause, or say why it earns the length")
    return fix, decide


def targets(args: list[str]) -> list[tuple[str, str]]:
    if args == ["-"]:
        return [("stdin", sys.stdin.read())]
    out = []
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            out.extend((str(p), p.read_text()) for p in sorted(path.rglob("*.md")))
        else:
            out.append((str(path), path.read_text()))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="files, directories, or - for stdin")
    parser.add_argument("--fix-only", action="store_true", help="print the FIX group and nothing else")
    args = parser.parse_args()

    all_fix: list[str] = []
    all_decide: list[str] = []
    for label, raw in targets(args.paths):
        defining = defines_the_rules(label)
        if defining:
            print(f"note: {label} states the banned words, so word checks are off for it.\n")
        fix, decide = findings(raw, label, defining)
        all_fix.extend(fix)
        all_decide.extend(decide)

    if all_fix:
        print(f"FIX  ({len(all_fix)}) — no judgement in these, rewrite them\n")
        for entry in all_fix:
            print(f"  {entry}\n")
    if all_decide and not args.fix_only:
        print(f"DECIDE  ({len(all_decide)}) — read each sentence and answer for that sentence\n")
        for entry in all_decide:
            print(f"  {entry}\n")
        print("  Most of these are real. Do not dismiss the group.\n")
    if not all_fix and (args.fix_only or not all_decide):
        print("Clean.")
    return 1 if all_fix else 0


if __name__ == "__main__":
    raise SystemExit(main())
