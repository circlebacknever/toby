#!/usr/bin/env bash
# Install the whole package into a throwaway HOME and check that what it installed is right.
# Touches only temp dirs, which it removes on exit. Proves the package installs
# on a fresh machine without trusting prose.
#
# Counting files only proves something arrived. These checks compare content, so
# a truncated copy or a stale instruction block fails here instead of on a user's
# machine.

# `sh scripts/test-install.sh` runs this file under a shell that lacks [[ and
# process substitution, so start again under bash.
# On macOS, sh is bash in POSIX mode, which sets BASH_VERSION too.
case "${BASH_VERSION:-}:${SHELLOPTS:-}" in
  :*|*posix*) exec bash "$0" "$@" ;;
esac
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
# installed instruction file must contain verbatim.
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
  # The installer strips .DS_Store, so a Finder copy in the repo is not a difference.
  if [[ -d "$dir" ]] && diff -r -x .DS_Store -x __pycache__ "$ROOT/skills" "$dir" >/dev/null 2>&1; then
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

# Each tool runs the checker from its own installed toby-voice skill, from a
# directory outside the repo, with no TOBY_ROOT. A skill that tells the agent to
# run scripts/voice-check.py fails when the skill folder has no such file.
PROBE="$TMP_ROOT/probe.md"
CLEAN="$TMP_ROOT/clean.md"
printf 'This uses a robust approach.\n' > "$PROBE"
printf 'The job retries twice.\n' > "$CLEAN"

while IFS='|' read -r label skills_rel instr_rel; do
  checker="$FRESH/$skills_rel/toby-voice/scripts/voice-check.py"
  if [[ ! -f "$checker" ]]; then
    flunk "$label" "the toby-voice skill has no scripts/voice-check.py"
  elif ! (cd "$TMP_ROOT" && env -u TOBY_ROOT python3 "$checker" "$CLEAN" --fix-only >/dev/null 2>&1); then
    flunk "$label" "the installed checker fails on a clean file"
  # The checker exits 1 when it finds a problem, and pipefail would carry that
  # exit through a pipe into grep, so read the output first.
  elif checker_out="$(cd "$TMP_ROOT" && env -u TOBY_ROOT python3 "$checker" "$PROBE" --fix-only 2>&1)"; [[ "$checker_out" == *"banned word 'robust'"* ]]; then
    pass "$label" "checker runs from the skill folder and catches a banned word"
  else
    flunk "$label" "the installed checker missed a banned word"
  fi
done < <(tool_rows)

if find "$FRESH" -name __pycache__ | grep -q .; then
  flunk total "running the checker left __pycache__ in an installed skill"
else
  pass total "running the checker left the skill folders unchanged"
fi

# --- 2. re-install without --force must refuse -------------------------------
# README promises an existing toby-* stays put unless forced. Untested, that
# promise is the one that quietly overwrites someone's work.

if install_into "$FRESH" --tool claude >/dev/null 2>&1; then
  flunk safety "re-install without --force overwrote existing skills"
else
  pass safety "re-install without --force refuses"
fi

# A conflict in one tool must stop the install for every tool before anything is
# written, and the message must list every conflicting file.
PARTIAL="$TMP_ROOT/partial"
mkdir -p "$PARTIAL/.claude/skills/toby-voice" "$PARTIAL/.codex"
printf 'hand edit\n' > "$PARTIAL/.claude/skills/toby-voice/SKILL.md"
printf 'user notes, no toby marker\n' > "$PARTIAL/.codex/AGENTS.md"

status=0
out="$(install_into "$PARTIAL" --tool all 2>&1)" || status=$?
if [[ "$status" -eq 0 ]]; then
  flunk safety "install with conflicts exited 0"
elif [[ -e "$PARTIAL/.codex/skills" || -e "$PARTIAL/.copilot" || -e "$PARTIAL/.kiro" ]]; then
  flunk safety "install with conflicts wrote files before it stopped"
elif [[ "$(cat "$PARTIAL/.claude/skills/toby-voice/SKILL.md")" != "hand edit" ]]; then
  flunk safety "install with conflicts replaced an existing skill"
elif ! grep -q "skills/toby-voice" <<<"$out" || ! grep -q ".codex/AGENTS.md" <<<"$out"; then
  flunk safety "the refusal did not list every conflicting file"
else
  pass safety "conflicts stop every tool, are all listed, and nothing is written"
fi

status=0
out="$(install_into "$PARTIAL" --tool all --dry-run 2>&1)" || status=$?
if [[ "$status" -ne 0 ]]; then
  flunk dry-run "exits $status when there are conflicts, want 0"
elif ! grep -q "skill directory already exists: .*skills/toby-voice" <<<"$out"; then
  flunk dry-run "does not list the conflicting files"
else
  pass dry-run "lists the conflicting files and exits 0"
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

# Default install: the full guide, and no output style. Installing both would
# put the writing sections in front of every turn twice.
PLAIN_HOME="$TMP_ROOT/plain"
install_into "$PLAIN_HOME" --tool claude >/dev/null 2>&1
if [[ -f "$PLAIN_HOME/.claude/output-styles/toby.md" ]]; then
  flunk claude "default install shipped the output style, which duplicates the guide"
elif ! grep -q '^## Five Tests$' "$PLAIN_HOME/.claude/CLAUDE.md"; then
  flunk claude "default install left the writing rules out of CLAUDE.md"
else
  pass claude "default install contains the whole guide, no style"
fi

# --output-style: the style contains the writing rules and CLAUDE.md drops them.
STYLE_HOME="$TMP_ROOT/style"
install_into "$STYLE_HOME" --tool claude --output-style >/dev/null 2>&1
STYLE="$STYLE_HOME/.claude/output-styles/toby.md"
STYLE_MD="$STYLE_HOME/.claude/CLAUDE.md"
if grep -q '^## Five Tests$' "$STYLE_MD"; then
  flunk claude "--output-style left the writing rules in CLAUDE.md as well"
elif ! grep -q '^## Skill Routing$' "$STYLE_MD"; then
  flunk claude "--output-style dropped the operating floor from CLAUDE.md"
elif ! grep -q '^## Five Tests$' "$STYLE"; then
  flunk claude "--output-style did not put the writing rules in the style"
else
  pass claude "--output-style splits the guide, no section in both"
fi
if [[ ! -f "$STYLE" ]]; then
  flunk claude "output style did not install"
elif ! diff -q "$ROOT/output-styles/toby.md" "$STYLE" >/dev/null; then
  flunk claude "installed output style differs from the repo"
elif ! grep -q '^keep-coding-instructions: true$' "$STYLE"; then
  flunk claude "installed output style would switch off the coding instructions"
else
  pass claude "output style matches the repo"
fi

# --hooks ships both hooks. The write hook must find the checker in the installed
# toby-voice skill with no checkout and no TOBY_ROOT. An old install left a lone
# voice-check.py in ~/.claude/toby/scripts, and the hook must skip that copy.
HOOK_HOME="$TMP_ROOT/hooks"
mkdir -p "$HOOK_HOME/.claude/toby/scripts"
printf 'import validate_skills\n' > "$HOOK_HOME/.claude/toby/scripts/voice-check.py"
install_into "$HOOK_HOME" --tool claude --hooks >/dev/null 2>&1
KIT="$HOOK_HOME/.claude/toby"
if [[ -f "$KIT/hooks/voice-write-check.py" && -f "$KIT/hooks/voice-stop-check.py" ]]; then
  pass hooks "--hooks installed both hooks"
else
  flunk hooks "--hooks did not install both hooks"
fi

PAYLOAD="{\"hook_event_name\":\"PostToolUse\",\"tool_name\":\"Write\",\"tool_input\":{\"file_path\":\"$PROBE\"}}"
hook_out="$(cd "$TMP_ROOT" && printf '%s' "$PAYLOAD" | HOME="$HOOK_HOME" env -u TOBY_ROOT python3 "$KIT/hooks/voice-write-check.py" 2>&1)" || true
if grep -q "banned word 'robust'" <<<"$hook_out"; then
  pass hooks "write hook runs the skill's checker and skips the old lone copy"
else
  flunk hooks "the installed write hook did not flag a banned word"
fi

if [[ "$fail" -ne 0 ]]; then
  printf '\nInstall smoke test failed.\n' >&2
  exit 1
fi
printf '\nInstall smoke test passed.\n'
