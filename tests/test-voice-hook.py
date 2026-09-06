#!/usr/bin/env python3
"""The Stop hook blocks seeded breaks and stays silent on clean replies.

The second half is the half that matters. A hook that fires on a reply with
nothing wrong gets turned off, and then nothing is checking anything.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

HOOK = Path(__file__).resolve().parents[1] / "hooks" / "voice-stop-check.py"

BREAKS = [
    "The cache is a correctness fix, not a speed one.",
    "This is a real tension — not a free addition.",
    "It's not a nit, it's a bug in the retry path.",
    "The failure is not just slow, it drops writes.",
    "Use a lookup map rather than a switch statement.",
    "The migration ran. It has not been verified, though.",
    "That said, the second run passed.",
    "Fixed the off-by-one in the pager. Hope this helps.",
]

CLEAN = [
    "The retry loop drops the last write. api/sync.ts:88.",
    "Three days. Okay, it's personal now. Send me the stack trace.",
    "I don't know why memory climbed. Nothing in the diff allocates, and I have no profiler data.",
    "Renamed `usr` to `user` across session.ts. Tests pass: 41 passed, 0 failed.",
    "The suite is green. One test was already skipped before this change, at auth.test.ts:203.",
    "Moved rate limiting into one middleware. The limit is now per-account.",
    "Adding a retry wrapper double-writes. The sync job is not idempotent, so a partial run plus a retry writes the rows twice.",
    "Port 3000 is taken by a `pnpm dev` you started at 09:14. Reuse it, pick another, or stop it?",
    "`validateInput` returns `true` on every branch. It validates that the function still runs.",
    "Two files changed, both under src/billing. No behavior moved.",
    "The flag is named `temporary_dispatch`. It shipped in 2019.",
    "Done: the export writes a CSV for the picked range. Verified with the 500-row fixture.",
    "The test asserts on a local-timezone timestamp and CI runs in UTC. That is the flake.",
    "Nothing to report. The diff matches the scope and the suite is green.",
    "I stopped at the migration. It is on the ask-list and I need a yes first.",
    "Four callers. Three updated, one deliberately out of scope at reports/legacy.py:12.",
    "The comment says the buffer is bounded. It is not. cache.go:41.",
    "Skipped the full suite and ran the two files the change touches instead.",
    "The plan lives at docs/plans/export.md. Step 3 ran differently and the file says how.",
    "Yes. The behavior record has no entry for this, so I wrote one.",
]


def run(reply: str) -> int:
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
        handle.write(json.dumps({"message": {"role": "assistant", "content": [{"type": "text", "text": reply}]}}) + "\n")
        transcript = handle.name
    payload = json.dumps({"transcript_path": transcript, "stop_hook_active": False})
    result = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True)
    Path(transcript).unlink()
    return result.returncode


failures = 0
for reply in BREAKS:
    code = run(reply)
    if code == 2:
        print(f"ok   blocks: {reply[:56]}")
    else:
        print(f"FAIL allowed a break: {reply}")
        failures += 1

false_positives = 0
for reply in CLEAN:
    code = run(reply)
    if code == 0:
        print(f"ok   allows: {reply[:56]}")
    else:
        print(f"FAIL false positive: {reply}")
        false_positives += 1
        failures += 1

print()
print(f"{len(BREAKS)} seeded breaks, {len(BREAKS) - failures + false_positives} caught.")
print(f"{len(CLEAN)} clean replies, {false_positives} false positives.")
if failures:
    raise SystemExit(1)
print("Stop hook fixtures passed.")
