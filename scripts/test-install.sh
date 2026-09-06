#!/usr/bin/env bash
# Install the whole package into a throwaway HOME and check what landed is right.
# Touches only temp dirs, which it removes on exit. Proves the package installs
# on a fresh machine without trusting prose.
#
# Counting files only proves something arrived. These checks compare content, so
# a truncated copy or a stale instruction block fails here instead of on a user's
# machine.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# One table, read by every check below. A new tool goes here and nowhere else.
# Fields: label | skills dir | instruction file. Both paths are relative to HOME.
TOOLS="
codex|.codex/skills|.codex/AGENTS.md
claude|.claude/skills|.claude/CLAUDE.md
copilot|.copilot/skills|.copilot/copilot-instructions.md
kiro|.kiro/skills|.kiro/steering/toby-instructions.md
"

tool_rows() { printf '%s\n' "$TOOLS" | grep -v '^[[:space:]]*$'; }

EXPECTED_PER_TOOL="$(find "$ROOT/skills" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
TOOL_COUNT="$(tool_rows | wc -l | tr -d ' ')"
EXPECTED_TOTAL=$(( EXPECTED_PER_TOOL * TOOL_COUNT ))

TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/toby-install-test.XXXXXX")"
trap 'rm -rf "$TMP_ROOT"' EXIT

fail=0

pass() { printf 'ok   %-9s %s\n' "$1" "$2"; }
flunk() { printf 'FAIL %-9s %s\n' "$1" "$2"; fail=1; }

install_into() {
  local home="$1"
  shift
  mkdir -p "$home"
  HOME="$home" CODEX_HOME="$home/.codex" "$ROOT/scripts/install.sh" "$@"
}

# The instruction block as base/toby.md defines it, which is what every
# installed instruction file must carry verbatim.
base_block() { cat "$ROOT/base/toby.md"; }

installed_block() {
  python3 - "$1" <<'PY'
import re, sys
from pathlib import Path
text = Path(sys.argv[1]).read_text()
match = re.search(
    r"<!-- BEGIN TOBY INSTRUCTIONS -->\n?(.*?)\n?<!-- END TOBY INSTRUCTIONS -->", text, re.S
)
if not match:
    raise SystemExit(1)
print(match.group(1).strip())
PY
}

# --- 1. fresh install ---------------------------------------------------------

FRESH="$TMP_ROOT/fresh"
install_into "$FRESH" --tool all --force >/dev/null

while IFS='|' read -r label skills_rel instr_rel; do
  dir="$FRESH/$skills_rel"
  instr="$FRESH/$instr_rel"

  count=0
  [[ -d "$dir" ]] && count="$(find "$dir" -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
  if [[ "$count" -ne "$EXPECTED_PER_TOOL" ]]; then
    flunk "$label" "$count skills installed, want $EXPECTED_PER_TOOL"
  else
    pass "$label" "$count skills"
  fi

  # Every installed skill must be byte-identical to the repo copy.
  if [[ -d "$dir" ]] && diff -r "$ROOT/skills" "$dir" >/dev/null 2>&1; then
    pass "$label" "skill contents match the repo"
  else
    flunk "$label" "installed skills differ from $ROOT/skills"
  fi

  if [[ ! -f "$instr" ]]; then
    flunk "$label" "missing instruction file $instr_rel"
  elif ! grep -q '<!-- BEGIN TOBY INSTRUCTIONS -->' "$instr"; then
    flunk "$label" "instruction marker missing in $instr_rel"
  elif ! diff <(installed_block "$instr") <(base_block) >/dev/null 2>&1; then
    flunk "$label" "instruction block in $instr_rel is out of sync with base/toby.md"
  else
    pass "$label" "instruction block matches base/toby.md"
  fi

done < <(tool_rows)

kiro_steering="$FRESH/.kiro/steering/toby-instructions.md"
if [[ -f "$kiro_steering" ]] && grep -q '^inclusion: always$' "$kiro_steering"; then
  pass kiro "steering uses inclusion: always"
else
  flunk kiro "steering missing inclusion: always"
fi

total="$(find "$FRESH" -path '*/skills/toby-*/SKILL.md' | wc -l | tr -d ' ')"
if [[ "$total" -ne "$EXPECTED_TOTAL" ]]; then
  flunk total "$total skill files across all tools, want $EXPECTED_TOTAL"
else
  pass total "$EXPECTED_TOTAL skill files across $TOOL_COUNT tools"
fi

# --- 2. re-install without --force must refuse -------------------------------
# README promises an existing toby-* stays put unless forced. Untested, that
# promise is the one that quietly overwrites someone's work.

if install_into "$FRESH" --tool claude >/dev/null 2>&1; then
  flunk safety "re-install without --force overwrote existing skills"
else
  pass safety "re-install without --force refuses"
fi

# --- 3. surrounding text in an instruction file survives ----------------------

MERGE="$TMP_ROOT/merge"
mkdir -p "$MERGE/.claude"
cat >"$MERGE/.claude/CLAUDE.md" <<'EOF'
# My own notes

Keep this line.

<!-- BEGIN TOBY INSTRUCTIONS -->
stale content that must be replaced
<!-- END TOBY INSTRUCTIONS -->

Keep this trailing line too.
EOF

install_into "$MERGE" --tool claude --force >/dev/null

merged="$MERGE/.claude/CLAUDE.md"
if grep -q 'Keep this line.' "$merged" && grep -q 'Keep this trailing line too.' "$merged"; then
  pass merge "text around the marker block survives"
else
  flunk merge "install destroyed text outside the marker block"
fi

if grep -q 'stale content that must be replaced' "$merged"; then
  flunk merge "stale block content was left in place"
elif diff <(installed_block "$merged") <(base_block) >/dev/null 2>&1; then
  pass merge "marker block updated to base/toby.md"
else
  flunk merge "marker block does not match base/toby.md"
fi

# --- 4. a file with no marker block is not touched without --force ------------

NOMARK="$TMP_ROOT/nomark"
mkdir -p "$NOMARK/.claude"
printf 'user content, no toby marker\n' >"$NOMARK/.claude/CLAUDE.md"

if install_into "$NOMARK" --tool claude >/dev/null 2>&1; then
  flunk safety "install appended to an unmarked file without --force"
elif [[ "$(cat "$NOMARK/.claude/CLAUDE.md")" == "user content, no toby marker" ]]; then
  pass safety "unmarked instruction file left untouched"
else
  flunk safety "unmarked instruction file was modified"
fi

# The output style lands in Claude Code's system prompt, so a truncated or stale
# copy changes how every reply reads. Compare content, not existence.
STYLE_HOME="$TMP_ROOT/style"
install_into "$STYLE_HOME" --tool claude >/dev/null 2>&1
STYLE="$STYLE_HOME/.claude/output-styles/toby.md"
if [[ ! -f "$STYLE" ]]; then
  flunk claude "output style did not install"
elif ! diff -q "$ROOT/output-styles/toby.md" "$STYLE" >/dev/null; then
  flunk claude "installed output style differs from the repo"
elif ! grep -q '^keep-coding-instructions: true$' "$STYLE"; then
  flunk claude "installed output style would switch off the coding instructions"
else
  pass claude "output style matches the repo"
fi

if [[ "$fail" -ne 0 ]]; then
  printf '\nInstall smoke test failed.\n' >&2
  exit 1
fi
printf '\nInstall smoke test passed.\n'
