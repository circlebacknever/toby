#!/usr/bin/env python3
"""Diff two rule inventories, separating rewordings from real deletions.

`comm` on the raw inventories reports every reworded sentence as a deletion,
which buries the one that matters. This pairs each deleted sentence with its
closest surviving relative by word overlap. Anything under the threshold has no
relative, and that is a rule that left the repo.

Usage: scripts/rule-diff.py before.txt after.txt [--threshold 0.55]
"""
from __future__ import annotations

import sys
from pathlib import Path

THRESHOLD = 0.6


# Containment, not Jaccard. Splitting one long sentence into two short ones
# halves a Jaccard score while losing no rule, and that is the commonest edit in
# this pass. What matters is whether the old sentence's words still sit together
# somewhere in the new text.
STOPWORDS = set(
    "a an and are as at be but by for from has have in is it its of on or that "
    "the their them they this to was what when where which who with you your not "
    "no do does don t so if then than there here every each one two all any".split()
)


def content(line: str) -> set[str]:
    return {w for w in line.split() if w not in STOPWORDS and len(w) > 2}


def overlap(a: set[str], b: set[str]) -> float:
    if not a:
        return 1.0
    return len(a & b) / len(a)


def main() -> int:
    before = set(Path(sys.argv[1]).read_text().splitlines())
    after = set(Path(sys.argv[2]).read_text().splitlines())
    threshold = THRESHOLD
    if "--threshold" in sys.argv:
        threshold = float(sys.argv[sys.argv.index("--threshold") + 1])

    gone = sorted(before - after)
    new = sorted(after - before)
    new_sets = [(line, content(line)) for line in new]
    survivors = set()
    for line in after:
        survivors |= content(line)

    reworded, scattered, lost = [], [], []
    for line in gone:
        words = content(line)
        best, score = "", 0.0
        for candidate, candidate_words in new_sets:
            value = overlap(words, candidate_words)
            if value > score:
                best, score = candidate, value
        if score >= threshold:
            reworded.append((line, best, score))
        elif words <= survivors:
            scattered.append((line, best, score))
        else:
            lost.append((line, best, score, sorted(words - survivors)))

    print(f"{len(gone)} sentences gone, {len(new)} new.")
    print(f"{len(reworded)} paired with a reworded survivor above {threshold}.")
    print(f"{len(scattered)} split across new sentences, every content word still present.")
    print(f"{len(lost)} carrying words that left the repo. Read every one.\n")
    for line, best, score, missing in lost:
        print(f"LOST  {line}")
        print(f"      words gone: {', '.join(missing)}")
        if best:
            print(f"      nearest ({score:.2f}): {best}")
    return 1 if lost else 0


if __name__ == "__main__":
    raise SystemExit(main())
