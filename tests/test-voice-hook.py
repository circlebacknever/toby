#!/usr/bin/env python3
"""The hooks block seeded hard breaks and stay silent on clean text.

The second half is the half that matters. A hook that fires on a reply with
nothing wrong gets turned off, and then nothing is checking anything.

Run: python3 tests/test-voice-hook.py
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOK = REPO / "hooks" / "voice-stop-check.py"
WRITE_HOOK = REPO / "hooks" / "voice-write-check.py"
CHECKER = REPO / "scripts" / "voice-check.py"

BREAKS = [
    "This is a real tension — not a free addition.",
    "Fixed the off-by-one in the pager. Hope this helps.",
    "The retry wrapper is at line 88 and the two call sites that reach it are both in the same file, which means removing it changes nothing outside that module, though the test suite has not run yet so that is still open.",
    "Very close. The score has to be 0 at the center.",
    "Here's why. The constant score never rises under any rule.",
    "Your sentence, repaired: the rule never raises the score.",
    "Short answer: the cache is stale.",
    "Two fixes, and both matter. The rule is fixed.",
    "Good. Now write the guard for the empty case.",
    "Great! The derivative is the slope at one point.",
    "Noted. I'll use specify from now on.",
    "Got it. The plan now covers the hook tests.",
    "Understood. I'll keep the old rubric wording.",
    "We can leverage the existing retry queue for the webhook failures.",
    "The new importer gives users a seamless upgrade path from version 3.",
    "The build passed; the deploy failed on the health check.",
    "The test is flaky — it depends on wall-clock time.",
    "Based on the diff, the handler drops the last write.",
    "You asked whether the timeout is per request, and it applies per connection, not per request.",
    "You're right, and I had the cause wrong.",
    "I won't propose a fix in this reply.",
    "That's the whole trick.",
    "We are leveraging the existing retry queue for the webhook failures.",
    "It is worth noting that the cache is stale.",
    "Additionally, the tests pass.",
    "The takeaway is that retries drop writes.",
    "The key insight is the timeout value.",
    "The new importer gives a seamlessly upgrade path.",
    "This section delves into the retry logic.",
    "Utilizing the map speeds up the lookup.",
    "The change is empowering for users.",
    "To summarize, the migration adds the column.",
    "To be clear, the timeout is per connection.",
    "Remaining limit, stated plainly: the hooks catch the hard markers.",
    "The cache is stale, honestly:",
    "In other words: delete the row.",
    "In other words, the row is gone.",
    "I'm happy to help with the migration.",
    "I should note that the cache is stale.",
    "Put simply, the timeout is per connection.",
    "One honest caveat: the hooks need a model to run.",
    "Three things to know: the cache, the queue, and the timeout.",
    "Two fixes: the pager and the retry.",
    "Let me take a look at the handler.",
    "I'll start by reading the diff.",
    "Here's what I found: the cache is stale.",
    "Note that the cache is stale.",
    "You're absolutely right. The handler drops the write.",
    "That sounds frustrating. The handler returns early.",
    "I understand your frustration. The migration ran.",
    "Great point. The cache is stale.",
    "Fair enough. The cache is stale.",
    "Does that make sense?",
    "To recap, the cache is stale.",
    "Here's a breakdown:",
    "Let me check the logs.",
    "Looking at the code, the handler returns early.",
    "That said, the second run passed.",
    "That's a great question.",
    "I apologize for the confusion.",
    "The code is robust.",
    "In short, the migration is safe.",
    "What this means is the cache is stale.",
    "The real issue is the missing index.",
    "The key is to move the insert.",
    "This is a classic race condition.",
    "Nice work on the fix.",
    "Overall, the change is safe.",
    "This might potentially cause a problem.",
    "Let's dive in.",
    "The answer is that the cache is stale.",
    "Here's a quick summary: the cache is stale.",
    "The problem: the cache is stale.",
    "The card named process narration.",
    "The report names the cause.",
    "I'd be happy to walk you through it.",
    "Let's look at the second issue.",
    "The good news is the cache is stale.",
    "Here's the plan:",
    "The migration is extremely slow.",
    "Basically, the cache is stale.",
]

# Style preferences the hooks deliberately leave to the on-demand checker:
# contrastive foils, litotes, and similar forms are a person's call, and a hook
# that blocks them gets switched off.
LETS_THROUGH = [
    "The cache is a correctness fix, not a speed one.",
    "It's not a nit, it's a bug in the retry path.",
    "The failure is not just slow, it drops writes.",
    "Use a lookup map rather than a switch statement.",
    "The migration ran. It has not been verified, though.",
    "Two libraries carry the framework.",
    "The fixture for that fix is built, not run.",
    "That's not a slip in word choice, it's the failure the guide describes.",
    "Use a lookup map instead of a switch statement.",
    "The one that matters: the retry count.",
    "A stampede under peak load isn't uncommon.",
    "Complexity creeps into the handler when retries stay inline.",
]

# Ordinary replies, and borderline forms the hooks deliberately leave to the
# on-demand checker, must pass silently.
CLEAN = [
    "The retry loop drops the last write. api/sync.ts:88.",
    "Reproduce: run `make test` twice.\nFix: the pager clamps negative offsets to zero.",
    "One thing is clear: the row is gone.",
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
    "The plan is at docs/plans/export.md. Step 3 ran differently and the file says how.",
    "The parser reads the header, then the body. Both are UTF-8.",
    "I renamed the flag and updated its four call sites. Suite is green.",
    "The index does not match the query, so the planner reads the table instead.",
    "Two entry points changed: the export route and the CLI subcommand.",
    'You flagged "The rule lives in AGENTS.md." I rewrote it as "The rule is in AGENTS.md."',
    "Almost. Two tables are left to migrate.",
    "Here is the stack trace from the failing run.",
    "Two tests failed, and both are in auth.test.ts.",
    "The parser calls itself on each child node.",
    "Exactly 12 rows differ from the ledger by more than $1.",
    "Correct. The index covers both columns.",
    "Yes, the migration ran on all four tables.",
    "Got it working on staging after the second deploy.",
    "I noted the port number in the plan, so the next run uses 5174.",
    "Understood messages get archived after a day.",
    "The rule lives in AGENTS.md, so read it first.",
    "A five-bullet list is five sentences wearing a hat.",
    "When the cache is down, the request falls through to load().",
    "make clean removes the build folder.",
    "I read the diff and saw no new allocations.",
    "I'll check the pager after the migration.",
    "Let me know when the deploy finishes.",
    "Overall latency fell 40 percent.",
    "The file is named `robust.py`.",
    "The problem is the missing index.",
    "The file is named `config.yml`.",
    "A named export has a fixed name.",
    "Name the function after its job.",
    "The user named one skill in the sentence.",
    "The plan is at docs/plan.md.",
    "The news is bad.",
    "We're happy to report 41 passing tests.",
]

failures = 0


def run_hook(reply: str, stop_hook_active: bool = False) -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
        handle.write(json.dumps({"message": {"role": "assistant", "content": [{"type": "text", "text": reply}]}}) + "\n")
        transcript = handle.name
    payload = json.dumps({"transcript_path": transcript, "stop_hook_active": stop_hook_active})
    result = subprocess.run([sys.executable, str(HOOK)], input=payload, capture_output=True, text=True)
    Path(transcript).unlink()
    return result


def expect(label: str, got, want) -> None:
    global failures
    if got == want:
        print(f"ok   {label}")
    else:
        print(f"FAIL {label} (got {got!r}, wanted {want!r})")
        failures += 1


for reply in BREAKS:
    if run_hook(reply).returncode == 2:
        print(f"ok   blocks: {reply[:56]}")
    else:
        print(f"FAIL allowed a break: {reply}")
        failures += 1

false_positives = 0
for reply in CLEAN:
    if run_hook(reply).returncode == 0:
        print(f"ok   allows: {reply[:56]}")
    else:
        print(f"FAIL false positive: {reply}")
        false_positives += 1
        failures += 1

for reply in LETS_THROUGH:
    if run_hook(reply).returncode == 0:
        print(f"ok   lets through: {reply[:56]}")
    else:
        print(f"FAIL blocked a checker-only form: {reply}")
        failures += 1

print()
print(f"{len(BREAKS)} seeded breaks, {len(BREAKS) - failures + false_positives} caught.")
print(f"{len(CLEAN)} ordinary replies, {false_positives} false positives.")

# --- reprompt shape ----------------------------------------------------------

blocked = run_hook("Short answer: the cache is stale.")
expect("a block prints nothing on stdout", blocked.stdout, "")
expect("the reprompt asks for a Revised reply heading", "`## Revised reply`" in blocked.stderr, True)
expect("the reprompt stays short and does not demand a whole-reply rewrite",
       "rewrite the whole reply" in blocked.stderr.lower(), False)
expect("the reprompt lists the matched line", "Short answer:" in blocked.stderr, True)

# --- length ceilings and splitting -------------------------------------------

LONG = " ".join(["word"] * 45) + "."
LONG_TOO = " ".join(["other"] * 45) + "."
two_hits = run_hook(f"Hope this helps with the first part. {LONG} Feel free to ask. {LONG_TOO}").stderr
expect("both long sentences are listed", two_hits.count("-word sentence"), 2)
expect("both closing offers are listed", "'Hope this helps'" in two_hits and "'Feel free'" in two_hits, True)

bullets = "The test missed the conditions where the failure happens, for these reasons:\n" + "\n".join(
    f"- **Item {n}.** Each writer read the style as its first step, with only the draft to fix." for n in range(3))
expect("a label line and its bullets are separate sentences", "-word sentence" in run_hook(bullets).stderr, False)

table = "The new message did best.\n\n| Measure | A | B | C |\n|---|---|---|---|\n" + "\n".join(
    f"| Unnamed problem types fixed in round {n} | 11 of 13 | 11 of 13 | 12 of 13 |" for n in range(6))
expect("table rows are not counted as one long sentence", "-word sentence" in run_hook(table).stderr, False)

expect("a four-sentence paragraph is blocked",
       "over 3 sentences" in run_hook("The cache is stale. The job runs hourly. The job skips weekends. The fix moves it to a queue.").stderr, True)
expect("a three-sentence paragraph passes",
       run_hook("The cache is stale. The job runs hourly. The fix moves it.").returncode, 0)

# --- the two-pass revision guard ----------------------------------------------

with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
    handle.write(json.dumps({"message": {"role": "assistant", "content": [{"type": "text", "text": "Short answer: stale."}]}}) + "\n")
    handle.write(json.dumps({"message": {"role": "assistant", "content": [{"type": "text", "text": "## Revised reply\n\nWe can leverage the cache."}]}}) + "\n")
    retry_transcript = handle.name
retry_res = subprocess.run([sys.executable, str(HOOK)],
                           input=json.dumps({"transcript_path": retry_transcript, "stop_hook_active": True}),
                           capture_output=True, text=True)
Path(retry_transcript).unlink()
expect("a first revised reply that still has a hard break is blocked", retry_res.returncode, 2)

with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as handle:
    for text in ("Short answer: stale.", "## Revised reply\n\nWe leverage the cache.",
                 "## Revised reply\n\nThe cache is stale. We use the queue."):
        handle.write(json.dumps({"message": {"role": "assistant", "content": [{"type": "text", "text": text}]}}) + "\n")
    twice_transcript = handle.name
twice_res = subprocess.run([sys.executable, str(HOOK)],
                           input=json.dumps({"transcript_path": twice_transcript, "stop_hook_active": True}),
                           capture_output=True, text=True)
Path(twice_transcript).unlink()
expect("the hook allows after two revisions", twice_res.returncode, 0)

# --- the write hook ------------------------------------------------------------


def run_write_hook(body: str, suffix: str = ".md") -> subprocess.CompletedProcess:
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False) as handle:
        handle.write(body)
        written = handle.name
    payload = json.dumps({
        "hook_event_name": "PostToolUse", "tool_name": "Write",
        "tool_input": {"file_path": written},
    })
    result = subprocess.run([sys.executable, str(WRITE_HOOK)], input=payload, capture_output=True, text=True)
    Path(written).unlink()
    return result


print()
expect("write hook flags a banned word in a written file",
       run_write_hook("This uses a robust approach.\n").returncode, 2)
expect("write hook flags a clause weld in a written file",
       run_write_hook("The build passed; the deploy failed.\n").returncode, 2)
expect("write hook flags a sentence over 40 words",
       run_write_hook("The retry wrapper is at line 88 and the two call sites that reach it are both in the same file, "
                      "which means removing it changes nothing outside that module, though the test suite has not run "
                      "yet so that is still open.\n").returncode, 2)
expect("write hook flags a four-sentence paragraph",
       run_write_hook("The cache is stale. The job runs hourly. The job skips weekends. The fix moves it.\n").returncode, 2)
expect("write hook flags a bullet over 40 words",
       run_write_hook("- The retry wrapper is at line 88 and the two call sites that reach it are both in the same file, "
                      "which means removing it changes nothing outside that module, though the test suite has not run "
                      "yet so that is still open.\n").returncode, 2)
expect("write hook flags a label in a written file",
       run_write_hook("Short answer: the cache is stale.\n").returncode, 2)
expect("write hook stays quiet on ordinary prose",
       run_write_hook("The parser reads the header, then the body. Both are UTF-8.\n").returncode, 0)
expect("write hook honors a quoted sentence",
       run_write_hook('The user wrote "This is a robust approach." and asked for a fix.\n').returncode, 0)
expect("write hook ignores a non-prose file",
       run_write_hook("This uses a robust approach.\n", suffix=".py").returncode, 0)
expect("write hook prints findings on stderr, not stdout",
       (run_write_hook("This uses a robust approach.\n").stdout, "banned word" in run_write_hook("This uses a robust approach.\n").stderr),
       ("", True))

# --- the on-demand checker still runs ------------------------------------------

check = subprocess.run([sys.executable, str(CHECKER), "-"], input="The parser reads the header.\n",
                       capture_output=True, text=True)
expect("voice-check.py still runs on stdin", check.returncode, 0)

print()
if failures:
    raise SystemExit(1)
print("Voice hook fixtures passed.")
