#!/usr/bin/env python3
"""Count how many gold-labelled sentences scripts/voice-check.py catches.

Each row in each evals/gold/*.jsonl file is one sentence with a label. A row with a
`context` field puts the sentence inside that markdown, such as `# {text}` for a
heading, because some rules apply only to headings or list items.

The test prints the result for every bad and good row, so a reader can see which
sentences get a FIX finding, which get only DECIDE, and which get no finding. It fails
when a good row gets a FIX finding. A miss on a bad row does not fail the run,
because the misses are the gap this test measures.

Run: python3 tests/test-voice-recall.py [file.jsonl ...]
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "voice-check.py"
LABEL_FILES = [Path(a) for a in sys.argv[1:]] or sorted((REPO_ROOT / "evals" / "gold").glob("*.jsonl"))


def result_for(row: dict) -> str:
    """Return FIX, DECIDE, or none for one row, as the checker reports it on stdin."""
    body = row.get("context", "{text}").replace("{text}", row["text"]) + "\n"
    run = subprocess.run([sys.executable, str(CHECKER), "-"], input=body, capture_output=True, text=True)
    if run.returncode not in (0, 1):
        raise SystemExit(f"checker crashed on {row['id']}:\n{run.stderr}")
    if run.returncode == 1:
        return "FIX"
    return "DECIDE" if "DECIDE  (" in run.stdout else "none"


false_positives: list[str] = []
for labels in LABEL_FILES:
    rows = [json.loads(line) for line in labels.read_text().splitlines() if line.strip()]
    counts: dict[str, Counter] = {"bad": Counter(), "good": Counter(), "unknown": Counter()}
    print(f"=== {labels.name}")
    for row in rows:
        label = row["label"] if row["label"] in counts else "unknown"
        result = result_for(row)
        counts[label][result] += 1
        if label != "unknown":
            print(f"{result:<6} {label:<4} {row['id']}  {row['text'][:70]}  ({row.get('why', '')})")
        # The held-out file measures precision and never gates, so no pattern
        # gets tuned to pass it.
        if label == "good" and result == "FIX" and row.get("split") != "heldout":
            false_positives.append(f"{labels.name}:{row['id']}")
    for label, tally in counts.items():
        total = sum(tally.values())
        print(f"{label}: {total} rows, {tally['FIX']} FIX, {tally['DECIDE']} DECIDE only, {tally['none']} with no finding")
    fix_total = counts["good"]["FIX"] + counts["bad"]["FIX"]
    if fix_total:
        print(f"FIX precision: {counts['bad']['FIX']} of {fix_total} FIX findings are on bad rows")
    print()

if false_positives:
    print(f"FAIL good rows with a FIX finding: {', '.join(false_positives)}")
    raise SystemExit(1)
print("ok   no good row has a FIX finding")
