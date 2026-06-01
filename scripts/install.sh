#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="all"
DRY_RUN=0
FORCE=0

usage() {
  printf 'Usage: %s [--tool codex|claude|copilot|github|kiro|all] [--dry-run] [--force]\n' "$0"
  printf '       github is an alias for copilot (GitHub Copilot CLI, ~/.copilot).\n'
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --tool)
      TOOL="${2:-}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      usage >&2
      exit 2
      ;;
  esac
done

case "$TOOL" in
  github)
    TOOL="copilot"
    ;;
  codex|claude|copilot|kiro|all) ;;
  *)
    usage >&2
    exit 2
    ;;
esac

run() {
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] %q' "$1"
    shift
    for arg in "$@"; do
      printf ' %q' "$arg"
    done
    printf '\n'
  else
    "$@"
  fi
}

install_skills() {
  local dest="$1"
  run mkdir -p "$dest"

  local skill
  for skill in "$ROOT"/skills/toby-*; do
    [[ -d "$skill" ]] || continue
    local name
    name="$(basename "$skill")"
    local target="$dest/$name"

    if [[ -e "$target" && "$FORCE" -ne 1 ]]; then
      printf 'Refusing to replace existing skill directory: %s\n' "$target" >&2
      printf 'Pass --force to replace Toby skill directories.\n' >&2
      exit 1
    fi

    if [[ -e "$target" ]]; then
      run rm -rf "$target"
    fi
    run cp -R "$skill" "$target"
  done
}

install_instruction_file() {
  local source="$1"
  local target="$2"
  local mode="${3:-merge}"

  run mkdir -p "$(dirname "$target")"

  if [[ "$DRY_RUN" -eq 1 ]]; then
    if [[ -f "$target" ]]; then
      printf '[dry-run] merge Toby instructions into %s\n' "$target"
    else
      printf '[dry-run] install Toby instructions to %s\n' "$target"
    fi
    return
  fi

  python3 - "$source" "$target" "$FORCE" "$mode" <<'PY'
from pathlib import Path
import re
import sys

source = Path(sys.argv[1])
target = Path(sys.argv[2])
force = sys.argv[3] == "1"
mode = sys.argv[4]

if mode not in {"merge", "dedicated"}:
    raise SystemExit(f"Unknown voice install mode: {mode}")

source_text = source.read_text()
block_re = re.compile(
    r"<!-- BEGIN TOBY INSTRUCTIONS -->\n?(.*?)\n?<!-- END TOBY INSTRUCTIONS -->",
    re.S,
)
match = block_re.search(source_text)
if not match:
    raise SystemExit(f"{source} has no Toby instruction marker block")
source_block = (
    "<!-- BEGIN TOBY INSTRUCTIONS -->\n"
    + match.group(1).strip()
    + "\n<!-- END TOBY INSTRUCTIONS -->"
)

if not target.exists():
    target.write_text(source_text)
    raise SystemExit(0)

target_text = target.read_text()
target_match = block_re.search(target_text)
if target_match:
    updated = target_text[: target_match.start()] + source_block + target_text[target_match.end() :]
    target.write_text(updated)
    raise SystemExit(0)

if not force:
    raise SystemExit(
        f"Refusing to change {target}; no Toby marker block found. Pass --force to append the Toby block."
    )

if mode == "dedicated":
    target.write_text(source_text)
else:
    sep = "" if target_text.endswith("\n") else "\n"
    target.write_text(target_text + sep + "\n" + source_block + "\n")
PY
}

install_codex() {
  local home="${CODEX_HOME:-$HOME/.codex}"
  install_skills "$home/skills"
  install_instruction_file "$ROOT/AGENTS.md" "$home/AGENTS.md" merge
}

install_claude() {
  install_skills "$HOME/.claude/skills"
  install_instruction_file "$ROOT/instructions/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md" merge
}

install_copilot() {
  install_skills "$HOME/.copilot/skills"
  install_instruction_file "$ROOT/instructions/copilot/copilot-instructions.md" "$HOME/.copilot/copilot-instructions.md" merge
}

install_kiro() {
  install_skills "$HOME/.kiro/skills"
  install_instruction_file "$ROOT/instructions/kiro/toby-instructions.md" "$HOME/.kiro/steering/toby-instructions.md" dedicated
}

if [[ "$TOOL" == "all" || "$TOOL" == "codex" ]]; then
  install_codex
fi
if [[ "$TOOL" == "all" || "$TOOL" == "claude" ]]; then
  install_claude
fi
if [[ "$TOOL" == "all" || "$TOOL" == "copilot" ]]; then
  install_copilot
fi
if [[ "$TOOL" == "all" || "$TOOL" == "kiro" ]]; then
  install_kiro
fi

printf 'Toby package install complete for --tool %s\n' "$TOOL"
