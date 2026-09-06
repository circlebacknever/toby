#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TOOL="all"
DRY_RUN=0
FORCE=0
OUTPUT_STYLE=0
HOOKS=0

usage() {
  printf 'Usage: %s [--tool codex|claude|copilot|github|kiro|all] [--output-style] [--dry-run] [--force]\n' "$0"
  printf '       github is an alias for copilot (GitHub Copilot CLI, ~/.copilot).\n'
  printf '\n'
  printf '  --hooks         Install the voice checker and the two hooks to\n'
  printf '                  ~/.claude/toby, then print the settings.json block to\n'
  printf '                  paste. Does not edit settings.json itself.\n'
  printf '  --output-style  Claude Code only. Install the writing rules as an output\n'
  printf '                  style, and install the shorter CLAUDE.md that leaves them\n'
  printf '                  out. Costs about 200 tokens more than the default, and\n'
  printf '                  puts the rules in the system prompt. You must then turn\n'
  printf '                  the style on: /config, Output style, Toby. Without that\n'
  printf '                  step the voice rules are not loaded at all.\n'
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
    --output-style)
      OUTPUT_STYLE=1
      shift
      ;;
    --hooks)
      HOOKS=1
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

install_hooks() {
  # The checker and the two hooks, with the two files they read. Four scripts and
  # base/toby.md, which holds the banned-word list they check against.
  local kit="$HOME/.claude/toby"
  run mkdir -p "$kit/scripts" "$kit/base" "$kit/hooks"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] install the voice checker and hooks to %s\n' "$kit"
    return
  fi
  run cp "$ROOT/scripts/validate-skills.py" "$kit/scripts/"
  run cp "$ROOT/scripts/voice-check.py" "$kit/scripts/"
  run cp "$ROOT/base/toby.md" "$kit/base/"
  run cp "$ROOT/hooks/voice-stop-check.py" "$kit/hooks/"
  run cp "$ROOT/hooks/voice-write-check.py" "$kit/hooks/"

  printf '\nvoice checker installed:\n'
  printf '  %s/scripts/voice-check.py\n\n' "$kit"
  printf 'To run the hooks as well, add this to %s/.claude/settings.json:\n\n' "$HOME"
  cat <<JSON
{
  "hooks": {
    "PostToolUse": [
      { "matcher": "Write|Edit", "hooks": [
        { "type": "command", "command": "python3 $kit/hooks/voice-write-check.py" } ] }
    ],
    "Stop": [
      { "hooks": [
        { "type": "command", "command": "python3 $kit/hooks/voice-stop-check.py" } ] }
    ]
  }
}
JSON
  printf '\nThis installer does not edit settings.json. Paste the block yourself,\n'
  printf 'merging it with any hooks already there.\n\n'
}

install_output_style() {
  # Claude Code only. The style lands in the system prompt, which is why the
  # voice rules go here as well as in CLAUDE.md.
  local target="$HOME/.claude/output-styles/toby.md"
  run mkdir -p "$(dirname "$target")"
  if [[ "$DRY_RUN" -eq 1 ]]; then
    printf '[dry-run] install Toby output style to %s\n' "$target"
    return
  fi
  run cp "$ROOT/output-styles/toby.md" "$target"
  printf '\noutput style installed, and CLAUDE.md now leaves the writing rules out.\n'
  printf 'Turn the style on before you write anything:\n'
  printf '  /config, then Output style, then Toby\n'
  printf 'Until you do, the voice rules are not loaded.\n\n'
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
  if [[ "$OUTPUT_STYLE" -eq 1 ]]; then
    # The style carries the writing rules, so CLAUDE.md leaves them out. Both
    # together would put the same 4,900 tokens in front of every turn twice.
    install_instruction_file "$ROOT/instructions/claude/CLAUDE-floor.md" "$HOME/.claude/CLAUDE.md" merge
    install_output_style
  else
    install_instruction_file "$ROOT/instructions/claude/CLAUDE.md" "$HOME/.claude/CLAUDE.md" merge
  fi
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

if [[ "$HOOKS" -eq 1 ]]; then
  install_hooks
fi

printf 'Toby package install complete for --tool %s\n' "$TOOL"
