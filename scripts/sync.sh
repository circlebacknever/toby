#!/usr/bin/env bash
# Propagate base/toby.md — the source of truth — into the five in-repo copies:
# the toby-voice reference and the four tool instruction files. Editors that
# fuzzy-find "toby.md" happily open the wrong one, so edit base and run this to
# make base win everywhere. install.sh ships these copies to $HOME; this only
# touches the repo.
#
# Usage:
#   scripts/sync.sh            write the copies from base
#   scripts/sync.sh --check    exit 1 if any copy is stale, write nothing (CI gate)
#   scripts/sync.sh --dry-run  show what would change, write nothing
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
MODE="write"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --check)   MODE="check"; shift ;;
    --dry-run) MODE="dry";   shift ;;
    -h|--help)
      printf 'Usage: %s [--check|--dry-run]\n' "$0"
      exit 0 ;;
    *)
      printf 'Usage: %s [--check|--dry-run]\n' "$0" >&2
      exit 2 ;;
  esac
done

python3 - "$ROOT" "$MODE" <<'PY'
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
mode = sys.argv[2]

body = (root / "base" / "toby.md").read_text()
body_stripped = body.strip()

# The output style is generated from the writing sections of base/toby.md. It
# sits in Claude Code's system prompt, one level above CLAUDE.md, and the tool
# re-states it during the conversation. That is the strongest position the
# voice rules can hold, and it is the only one that survives turn ten.
#
# It carries the writing sections only. The operating floor, skill routing, and
# machine safety stay in the instruction files, which every tool already loads.
OUTPUT_STYLE_SECTIONS = [
    "No Performance Around the Answer",
    "Role",
    "Prose",
    "Register",
    "Reply Architecture",
    "Register Range",
    "Banned Writing Patterns",
    "Writing in Files and Artifacts",
    "Disagreement",
    "Uncertainty",
    "Banned Words",
]

OUTPUT_STYLE_HEADER = """---
name: Toby
description: Toby's voice. Plain words, the answer first, no padding, in chat and in every file.
keep-coding-instructions: true
---

# Toby

You are Toby. Write everything below this line in Toby's voice: chat replies, code comments,
docstrings, commit messages, docs, diagrams, chart labels, and every generated
artifact. No surface is exempt.

Generated from base/toby.md by scripts/sync.sh. Edit base, then run it.

"""


def sections_of(text):
    parts = re.split(r"^(## .+)$", text, flags=re.M)
    return dict(zip((h[3:].strip() for h in parts[1::2]), parts[2::2]))


def output_style(text: str) -> str:
    found = sections_of(text)
    missing = [n for n in OUTPUT_STYLE_SECTIONS if n not in found]
    if missing:
        sys.exit(f"  ERROR: base/toby.md has no section(s): {', '.join(missing)}")
    out = [OUTPUT_STYLE_HEADER]
    for name in OUTPUT_STYLE_SECTIONS:
        out.append(f"## {name}{found[name].rstrip()}\n\n")
    return "".join(out).rstrip() + "\n"


# Raw copies hold the body verbatim; marker copies hold it between the markers.
raw_targets = [root / "skills" / "toby-voice" / "references" / "toby.md"]
# The operating floor: everything the output style does not carry. Installing
# the style and the full guide together pays for the writing sections twice, at
# about 4,900 tokens a turn, so this is the half to pair with the style.
def operating_floor(text: str) -> str:
    found = sections_of(text)
    keep = [n for n in found if n not in OUTPUT_STYLE_SECTIONS]
    head = (
        "This file carries Toby's operating floor. The writing rules live in the "
        "Toby output style, which Claude Code loads into the system prompt.\n\n"
        "If the Toby output style is not selected, the voice rules are not loaded "
        "at all. Turn it on with /config, then Output style, then Toby. Say so "
        "plainly if you are asked to write and these rules are missing.\n\n"
    )
    return head + "".join(f"## {n}{found[n].rstrip()}\n\n" for n in keep).rstrip() + "\n"


generated_targets = [
    (root / "output-styles" / "toby.md", output_style(body)),
]
floor_target = root / "instructions" / "claude" / "CLAUDE-floor.md"
floor_body = operating_floor(body)
marker_targets = [
    root / "AGENTS.md",
    root / "instructions" / "claude" / "CLAUDE.md",
    root / "instructions" / "copilot" / "copilot-instructions.md",
    root / "instructions" / "kiro" / "toby-instructions.md",
]

block_re = re.compile(
    r"(<!-- BEGIN TOBY INSTRUCTIONS -->\n).*?(\n<!-- END TOBY INSTRUCTIONS -->)",
    re.S,
)

changed = 0


def label(stale: bool) -> str:
    if not stale:
        return "in sync"
    return {"write": "synced", "check": "STALE", "dry": "would update"}[mode]


def apply(target: Path, new_text: str) -> None:
    global changed
    rel = target.relative_to(root)
    stale = target.read_text() != new_text
    changed += stale
    if stale and mode == "write":
        target.write_text(new_text)
    print(f"  {label(stale):>12}  {rel}")


for target in raw_targets:
    apply(target, body)

for target, text in generated_targets:
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text("")
    apply(target, text)

for target in marker_targets:
    text = target.read_text()
    if not block_re.search(text):
        sys.exit(f"  ERROR: no Toby marker block in {target.relative_to(root)}")
    apply(target, block_re.sub(lambda m: m.group(1) + body_stripped + m.group(2), text, count=1))

if not floor_target.exists():
    floor_target.write_text(
        "<!-- BEGIN TOBY INSTRUCTIONS -->\n\n<!-- END TOBY INSTRUCTIONS -->\n"
    )
text = floor_target.read_text()
apply(floor_target, block_re.sub(lambda m: m.group(1) + floor_body.strip() + m.group(2), text, count=1))

print()
if mode == "check" and changed:
    sys.exit(f"{changed} copy(ies) stale. Run scripts/sync.sh to fix.")
if mode == "dry":
    print(f"{changed} copy(ies) would change.")
elif mode == "check":
    print("All copies in sync with base/toby.md.")
else:
    print("done." if changed else "already in sync; nothing to write.")
PY
