#!/usr/bin/env python3
"""Count how many gold-labelled sentences scripts/voice-check.py catches.

Each row in evals/gold/labels.jsonl is one sentence with a label. A row with a
`context` field puts the sentence inside that markdown, such as `# {text}` for a
heading, because some rules apply only to headings or list items.

The test prints the result for every bad and good row, so a reader can see which
sentences get a FIX finding, which get only DECIDE, and which get no finding. It fails
when a good row gets a FIX finding. A miss on a bad row does not fail the run,
because the misses are the gap this test measures.

Run: python3 tests/test-voice-recall.py [labels.jsonl]
"""
from __future__ import annotations

import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
CHECKER = REPO_ROOT / "scripts" / "voice-check.py"
LABELS = Path(sys.argv[1]) if len(sys.argv) > 1 else REPO_ROOT / "evals" / "gold" / "labels.jsonl"


def result_for(row: dict) -> str:
    """Return FIX, DECIDE, or none for one row, as the checker reports it on stdin."""
    body = row.get("context", "{text}").replace("{text}", row["text"]) + "\n"
    run = subprocess.run([sys.executable, str(CHECKER), "-"], input=body, capture_output=True, text=True)
    if run.returncode not in (0, 1):
        raise SystemExit(f"checker crashed on {row['id']}:\n{run.stderr}")
    if run.returncode == 1:
        return "FIX"
    return "DECIDE" if "DECIDE  (" in run.stdout else "none"


rows = [json.loads(line) for line in LABELS.read_text().splitlines() if line.strip()]
counts: dict[str, Counter] = {"bad": Counter(), "good": Counter(), "unknown": Counter()}
false_positives: list[str] = []

for label in ("bad", "good"):
    print(f"--- {label} rows")
    for row in (r for r in rows if r["label"] == label):
        result = result_for(row)
        counts[label][result] += 1
        print(f"{result:<6} {row['id']}  {row['text'][:70]}  ({row['why']})")
        if label == "good" and result == "FIX":
            false_positives.append(row["id"])
    print()

for row in (r for r in rows if r["label"] == "unknown"):
    counts["unknown"][result_for(row)] += 1

for label, tally in counts.items():
    total = sum(tally.values())
    print(f"{label}: {total} rows, {tally['FIX']} FIX, {tally['DECIDE']} DECIDE only, {tally['none']} with no finding")

if false_positives:
    print(f"\nFAIL good rows with a FIX finding: {', '.join(false_positives)}")
    raise SystemExit(1)
print("\nok   no good row has a FIX finding")
