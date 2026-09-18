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
    "Teaching prose is a first-read surface, so keep it plain.",
    "A five-bullet list is five sentences wearing a hat.",
    "That decorator is a shallow pass-through in disguise.",
    "Narrow the blast radius before you start guessing at the cause.",
    "Two libraries carry the framework.",
    "The rule lives in AGENTS.md, so read it first.",
    "This finding rests on reading the diff.",
    "When the cache is down, the request falls through to load().",
    "Every lever feeds a formula.",
    "The fixture for that fix is built, not run.",
    "That's not a slip in word choice, it's the failure the guide describes.",
    "Checkpoints and caches sit in the stores.",
    "The retry wrapper is at line 88 and the two call sites that reach it are both "
    "in the same file, which means removing it changes nothing outside that "
    "module, though the test suite has not run yet so that is still open.",
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
    "The plan is at docs/plans/export.md. Step 3 ran differently and the file says how.",
    "Yes. The behavior record has no entry for this, so I wrote one.",
    "The parser reads the header, then the body. Both are UTF-8.",
    "I renamed the flag and updated its four call sites. Suite is green.",
    "The index does not match the query, so the planner reads the table instead.",
    "Two entry points changed: the export route and the CLI subcommand.",
    'You flagged "The rule lives in AGENTS.md." I rewrote it as "The rule is in AGENTS.md."',
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
print(f"{len(CLEAN)} ordinary replies, {false_positives} false positives.")

# --- the write hook, and the FIX/DECIDE split ---------------------------------
import tempfile as _tf

WRITE_HOOK = Path(__file__).resolve().parents[1] / "hooks" / "voice-write-check.py"
CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "voice-check.py"
notes: list[str] = []


def run_write_hook(body: str, suffix: str = ".md") -> int:
    with _tf.NamedTemporaryFile("w", suffix=suffix, delete=False) as handle:
        handle.write(body)
        written = handle.name
    payload = json.dumps({
        "hook_event_name": "PostToolUse", "tool_name": "Write",
        "tool_input": {"file_path": written},
    })
    result = subprocess.run([sys.executable, str(WRITE_HOOK)], input=payload,
                            capture_output=True, text=True)
    Path(written).unlink()
    return result.returncode


def expect(label: str, got: int, want: int) -> None:
    if got == want:
        print(f"ok   {label}")
    else:
        print(f"FAIL {label} (exit {got}, wanted {want})")
        notes.append(label)


print()
expect("write hook flags a banned word in a written file",
       run_write_hook("This uses a robust approach.\n"), 2)
expect("write hook reports a DECIDE finding in a written file",
       run_write_hook("The hook return shape is fine here.\n"), 2)
expect("write hook stays quiet on ordinary prose",
       run_write_hook("The parser reads the header, then the body. Both are UTF-8.\n"), 0)
expect("write hook ignores a non-prose file",
       run_write_hook("This uses a robust approach.\n", suffix=".py"), 0)

# A judgement call must never gate anything, or the group gets waved away.
with _tf.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
    handle.write("The hook return shape is fine here.\n")
    decide_file = handle.name
out = subprocess.run([sys.executable, str(CHECKER), decide_file], capture_output=True, text=True)
Path(decide_file).unlink()
expect("a DECIDE finding does not fail the run", out.returncode, 0)

# The guide lists every banned word. Scanning it for them returned 107 findings
# once, which is how a tool teaches its reader to ignore it.
GUIDE = Path(__file__).resolve().parents[1] / "base" / "toby.md"
guide_out = subprocess.run([sys.executable, str(CHECKER), str(GUIDE), "--fix-only"],
                           capture_output=True, text=True)
expect("the guide is not scanned for the words it defines", guide_out.returncode, 0)
if "states the banned words" not in guide_out.stdout:
    print("FAIL the checker did not say why the word checks were off")
    notes.append("defining note")
if "DECIDE" not in out.stdout:
    print("FAIL the DECIDE group was not printed")
    notes.append("decide printed")

# A run with no findings still prints the rules the patterns do not check, because an
# agent that sees no findings stops reading.
read_out = subprocess.run([sys.executable, str(CHECKER), "-"], input="The parser reads the header.\n",
                          capture_output=True, text=True)
if "READ  (" in read_out.stdout:
    print("ok   a run with no findings prints the READ list")
else:
    print("FAIL a run with no findings left out the READ list")
    notes.append("read list printed")
no_read_out = subprocess.run([sys.executable, str(CHECKER), "-", "--no-read"],
                             input="The parser reads the header.\n", capture_output=True, text=True)
if "READ  (" in no_read_out.stdout:
    print("FAIL --no-read printed the READ list")
    notes.append("no-read flag")
else:
    print("ok   --no-read leaves out the READ list")

# Slogans. The five sentences below each passed every check before the slogan
# forms existed, and each is an agent's doc copy the user rewrote. The checker
# has to raise every form on them and none on the rewrites.
SLOGANS = """# Backplane

A multi agent framework platform

Users talk to agents. Agents read, call tools, and pause for people.

No plugin imports an engine. No framework file names a plugin.

A plugin is data. The framework compiles it.

## Uniformity is the failure

Two libraries carry the framework.

One file causes this failure.

Phase 1 of 3 in the queue migration.

- Guard: none.

Follow these steps to add one.

- Approve the $400 monthly cost.
- Approve the 6-week migration.

A stampede under peak load is not uncommon, and complexity creeps into the handler.

The result? The build is incredibly slow, and the compiler complains about the types.

The wrapper provides the ability to retry, which may potentially help, and it is the ask from product.

The plan is less prose, more code.

Stop searching the repo, because the cause is outside it. That failure would have paged the engineer.

A plugin never imports an engine directly, and Relay treats model providers as engines.

## Toby is careful, Toby wants to live

The bigger gap is elsewhere. The conformance suite tests exactly that surface.

Five properties keep that true, and the runner checks the third.

A failed demo has one trace to open, and that is the property that makes it checkable.

### The migration moves the highest-risk jobs first

- Phase 1 moves the highest-risk jobs.
"""
REWRITES = """# Backplane

Backplane is an extensible multi-agent platform.

Users instruct agents, and agents perform complex actions and wait for human feedback.

New agents are created as plugins.

The queue service costs $400 a month

## Varied replies

The platform consists of a shared generative UI toolkit and features that make it easy to build agents.
"""
FORMS = ["noun phrase with no verb", "clipped run of short sentences", "mirrored pair",
         "chained pair", "one-word definition", "heading written as a claim", "sense-scoped 'carry'",
         "setup sentence before the fact", "label with a period", "label with no value",
         "sentence about the document", "mirrored bullets", "litotes", "abstract noun as actor",
         "setup question", "noun doing a verb's job", "meeting jargon", "rhythm device",
         "vague intensifier", "code given feelings", "hedge stack", "would-have stated as fact",
         "claim about the user", "what a thing never does", "program given a judgment",
         "bullet restates its heading", "bare `that` as an object", "rider after a complete claim",
         "heading joins two clauses"]


def check_text(body: str) -> subprocess.CompletedProcess:
    with _tf.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
        handle.write(body)
        name = handle.name
    result = subprocess.run([sys.executable, str(CHECKER), name], capture_output=True, text=True)
    Path(name).unlink()
    return result


slogan_out = check_text(SLOGANS)
for form in FORMS:
    if form in slogan_out.stdout:
        print(f"ok   checker raises {form}")
    else:
        print(f"FAIL checker missed {form}")
        notes.append(form)
expect("slogan findings do not fail the run", slogan_out.returncode, 0)
rewrite_out = check_text(REWRITES)
for form in FORMS:
    if form in rewrite_out.stdout:
        print(f"FAIL checker raised {form} on a plain rewrite")
        notes.append(f"rewrite {form}")
expect("the plain rewrites pass", rewrite_out.returncode, 0)

# Figurative verbs sit in FIX, so they fail the run. A plain sentence with the
# same facts passes.
verb_out = check_text("The rule lives in AGENTS.md.\n")
expect("a figurative verb fails the run", verb_out.returncode, 1)
plain_out = check_text("The rule is in AGENTS.md.\n")
expect("the literal version passes", plain_out.returncode, 0)

# A verb for a feeling, given to a system, is a metaphor, so it fails the run.
feeling_out = check_text("Stream resume is the one most likely to embarrass a demo.\n")
expect("a verb for a feeling fails the run", feeling_out.returncode, 1)

# --review prints every sentence, so the reader can answer for each one.
with _tf.NamedTemporaryFile("w", suffix=".md", delete=False) as handle:
    handle.write("# A heading\n\nThe parser reads the header. The rule lives in AGENTS.md.\n")
    review_file = handle.name
review_out = subprocess.run([sys.executable, str(CHECKER), review_file, "--review"],
                            capture_output=True, text=True)
Path(review_file).unlink()
expect("--review fails the run on a FIX finding", review_out.returncode, 1)
for wanted in ("READ  (", "1. A heading", "2. The parser reads the header.",
               "3. The rule lives in AGENTS.md.", "FIX  figurative frame"):
    if wanted in review_out.stdout:
        print(f"ok   --review prints {wanted!r}")
    else:
        print(f"FAIL --review left out {wanted!r}")
        notes.append(f"review {wanted}")

# A numbered step joins clauses with a semicolon as easily as a paragraph does.
list_weld_out = check_text("1. An agent starting from a plugin edits; one starting from nothing guesses.\n")
expect("a semicolon join inside a list item fails the run", list_weld_out.returncode, 1)
label_out = check_text("- Supported but vague — sharpen it before you evaluate anything.\n")
expect("a label and a dash in a list item pass", label_out.returncode, 0)

print()
if failures or notes:
    raise SystemExit(1)
print("Voice hook and checker fixtures passed.")
