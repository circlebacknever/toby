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

# Raw copies hold the body verbatim; marker copies hold it between the markers.
raw_targets = [root / "skills" / "toby-voice" / "references" / "toby.md"]
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

for target in marker_targets:
    text = target.read_text()
    if not block_re.search(text):
        sys.exit(f"  ERROR: no Toby marker block in {target.relative_to(root)}")
    apply(target, block_re.sub(lambda m: m.group(1) + body_stripped + m.group(2), text, count=1))

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
