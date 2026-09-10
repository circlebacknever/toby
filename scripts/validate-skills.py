#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
INSTRUCTION_BLOCK_RE = re.compile(
    r"<!-- BEGIN TOBY INSTRUCTIONS -->\n(.*?)\n<!-- END TOBY INSTRUCTIONS -->\n?", re.S
)

OLD_REFERENCES = [
    re.compile(r"\bcc-[a-z-]+\b"),
    re.compile(r"\bopenspec-[a-z-]+\b"),
    re.compile(r"\$cc-[a-z-]+"),
    re.compile(r"\$swd-[a-z-]+"),
    re.compile(r"\$" + "as" + "tro" + r"\b"),
    re.compile(r"\b" + "Ar" + "thur" + r"\b"),
    re.compile(r"\b" + "As" + "tro" + r"\b"),
    re.compile(r"\b" + "as" + "tro" + r"\b"),
]

REVIEW_TOOL_NAMES = re.compile(r"\b(Codex|Claude|Kiro|Copilot)\b")

# The repo path for the operating guide. Nothing installs under this name, so a
# skill that cites it sends the reader to a file that is not there.
#
# The other half of this bug is a skill calling the guide `AGENTS.md`, and that
# one is not checked here. `AGENTS.md` is also what toby-swd-docs calls the
# module doc in the user's own repo, so the same string is right in one skill
# and wrong in another, and only the sentence around it tells them apart.
OPERATING_GUIDE_PATHS = [
    re.compile(r"base/toby\.md"),
]

# Kept byte-identical to base/toby.md by sync.sh, so it is scanned as the guide
# rather than as a skill file.
#
# Measured, not assumed. Deleting it scored 8 voice defects against 1 for the
# full re-read, and a writing-sections-only extract scored 4.5. The duplicate
# costs 6,800 tokens a prose turn and buys the voice. evals/README.md has the
# runs.
VOICE_REFERENCE_COPY = REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md"


# Ceiling every current CLI target accepts (agentskills/Kiro allow up to 1024;
# Claude Code allows more). Stay under this and the skill loads everywhere.
DESCRIPTION_MAX = 1024

BASE_TOBY = REPO_ROOT / "base" / "toby.md"

# The banned-word lists live in base/toby.md under "## Banned Words" and are read
# from there. Keeping a second copy here is how the two lists drifted apart the
# last time: base carried 33 words the artifact-style copy never had.
BANNED_SECTION_RE = re.compile(r"^## Banned Words\n(.*?)(?=^## )", re.M | re.S)
BANNED_TIER_RE = re.compile(r"^### (.+?)\n(.*?)(?=^### |\Z)", re.M | re.S)


def _split_words(block: str) -> list[str]:
    """Pull the comma-separated word list out of a tier body.

    A tier body is one explanatory sentence followed by the list. The list is
    recognized by form: every comma-separated item is at most four words and
    carries no backtick, quote, or terminal punctuation of its own.
    """
    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith(("|", "-", "*", "#", ">")):
            continue
        if "," not in line or "`" in line or '"' in line:
            continue
        items = [item.strip().lower() for item in line.rstrip(".").split(",")]
        if all(item and len(item.split()) <= 4 and "." not in item for item in items):
            return items
    return []


def load_banned_words() -> dict[str, list[str]]:
    """Read the hard-ban and sense-scoped tiers out of base/toby.md.

    Returns {"hard": [...], "sense": [...]}. "hard" gates the build. "sense"
    only warns, because a regex cannot tell `cache key` from "the key insight".
    """
    section = BANNED_SECTION_RE.search(BASE_TOBY.read_text())
    if not section:
        return {"hard": [], "sense": []}
    tiers: dict[str, list[str]] = {"hard": [], "sense": []}
    for heading, body in BANNED_TIER_RE.findall(section.group(1)):
        heading = heading.strip().lower()
        if heading.startswith("hard ban"):
            tiers["hard"] = _split_words(body)
        elif heading.startswith("banned as"):
            tiers["sense"] = _split_words(body)
    return tiers


CONTRAST_PATTERNS = [
    re.compile(r"\bnot\s+[^.\n]{0,80}\bbut\b", re.I),
    re.compile(r"\brather than\b", re.I),
    re.compile(r"\binstead of\b", re.I),
    re.compile(r"\bnot just\b", re.I),
    re.compile(r"\bit'?s not\b", re.I),
]


def frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    result: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        result[key.strip()] = value.strip().strip("\"'")
    return result


def description_text(text: str) -> str:
    """Render the full description, including folded/literal multi-line scalars.

    The frontmatter() parser only keeps the inline value, so a folded
    ``description: >-`` collapses to ``>-``. This reads the real string so the
    length guard measures what the tools actually load.
    """
    if not text.startswith("---\n"):
        return ""
    end = text.find("\n---", 4)
    if end < 0:
        return ""
    lines = text[4:end].splitlines()
    for index, line in enumerate(lines):
        stripped = line.lstrip()
        if not stripped.startswith("description:"):
            continue
        indent = len(line) - len(stripped)
        inline = stripped[len("description:") :].strip()
        if inline and inline[:1] not in {">", "|"}:
            return inline.strip("\"'")
        parts: list[str] = []
        for cont in lines[index + 1 :]:
            cont_stripped = cont.strip()
            if cont_stripped == "":
                parts.append("")
                continue
            if len(cont) - len(cont.lstrip()) <= indent:
                break
            parts.append(cont_stripped)
        if inline.startswith("|"):
            return "\n".join(parts).strip()
        return " ".join(part for part in parts if part).strip()
    return ""


def text_files(root: Path) -> list[Path]:
    suffixes = {".md", ".yaml", ".yml", ".sh", ".py"}
    return [
        path
        for path in root.rglob("*")
        if path.is_file() and path.suffix in suffixes and ".git" not in path.parts
    ]


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def extract_instruction_block(path: Path) -> str:
    text = path.read_text()
    match = INSTRUCTION_BLOCK_RE.search(text)
    if not match:
        raise ValueError(f"{path} has no Toby instruction marker block")
    return match.group(1).strip() + "\n"


def check_instruction_sync(errors: list[str]) -> None:
    instructions = (REPO_ROOT / "base" / "toby.md").read_text().strip() + "\n"
    targets = [
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "instructions" / "claude" / "CLAUDE.md",
        REPO_ROOT / "instructions" / "copilot" / "copilot-instructions.md",
        REPO_ROOT / "instructions" / "kiro" / "toby-instructions.md",
    ]
    for target in targets:
        try:
            block = extract_instruction_block(target)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if block != instructions:
            errors.append(f"{target} is out of sync with base/toby.md")

    ref = REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md"
    if ref.read_text().strip() + "\n" != instructions:
        errors.append(f"{ref} is out of sync with base/toby.md")

    kiro = (REPO_ROOT / "instructions" / "kiro" / "toby-instructions.md").read_text()
    if "inclusion: always" not in kiro.split("---", 2)[1]:
        errors.append("instructions/kiro/toby-instructions.md must use inclusion: always")


OUTPUT_STYLE = REPO_ROOT / "output-styles" / "toby.md"

# The writing sections scripts/sync.sh writes into the output style. Kept here so
# a section dropped from sync.sh fails the build instead of going quiet.
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


def sections_of(text: str) -> dict[str, str]:
    """Split a guide-shaped file into {heading: body} at its `## ` headings."""
    parts = re.split(r"^(## .+)$", text, flags=re.M)
    return dict(zip((h[3:].strip() for h in parts[1::2]), parts[2::2]))


def check_output_style(errors: list[str]) -> None:
    """The output style carries guide sections verbatim, and nothing else.

    It lands in Claude Code's system prompt, which is a stronger position than
    any instruction file. A section that drifts there is a rule that applies in
    chat and nowhere else, or the reverse.
    """
    if not OUTPUT_STYLE.exists():
        errors.append("output-styles/toby.md is missing, run scripts/sync.sh")
        return
    style = sections_of(OUTPUT_STYLE.read_text())
    base = sections_of(BASE_TOBY.read_text())
    for name, body in style.items():
        if name not in base:
            errors.append(f"output style has a section base/toby.md lacks: {name!r}")
        elif body.strip() != base[name].strip():
            errors.append(f"output style section {name!r} has drifted from base/toby.md")
    for name in OUTPUT_STYLE_SECTIONS:
        if name not in style:
            errors.append(f"output style is missing the {name!r} section, run scripts/sync.sh")
    head = OUTPUT_STYLE.read_text()[:400]
    if "keep-coding-instructions: true" not in head:
        errors.append("output style must set keep-coding-instructions: true, or Toby stops engineering")


CLAUDE_FLOOR = REPO_ROOT / "instructions" / "claude" / "CLAUDE-floor.md"


def check_floor_complements_style(errors: list[str]) -> None:
    """The floor file and the output style together are the whole guide.

    They ship as a pair: the style holds the writing sections, CLAUDE-floor.md
    holds the rest, and installing the full guide alongside the style would put
    the same 4,900 tokens in front of every turn twice. A section in both, or in
    neither, is a rule that fires twice or not at all.
    """
    if not CLAUDE_FLOOR.exists():
        errors.append("instructions/claude/CLAUDE-floor.md is missing, run scripts/sync.sh")
        return
    base = sections_of(BASE_TOBY.read_text())
    # Read the marked block, or the last section picks up the closing marker and
    # reads as drift on every run.
    try:
        floor_block = extract_instruction_block(CLAUDE_FLOOR)
    except ValueError as exc:
        errors.append(str(exc))
        return
    floor = sections_of(floor_block)
    style = sections_of(OUTPUT_STYLE.read_text()) if OUTPUT_STYLE.exists() else {}

    for name in base:
        in_floor, in_style = name in floor, name in style
        if in_floor and in_style:
            errors.append(f"section {name!r} is in both CLAUDE-floor.md and the output style")
        elif not in_floor and not in_style:
            errors.append(f"section {name!r} is in neither CLAUDE-floor.md nor the output style")
    for name, body in floor.items():
        if name not in base:
            errors.append(f"CLAUDE-floor.md has a section base/toby.md lacks: {name!r}")
        elif body.strip() != base[name].strip():
            errors.append(f"CLAUDE-floor.md section {name!r} has drifted from base/toby.md")
    if "output style" not in floor_block[:600]:
        errors.append("CLAUDE-floor.md must say the writing rules come from the output style")


def stray_ds_store() -> list[Path]:
    """Return the .DS_Store files that can reach a commit or an install.

    Finder writes .DS_Store into every folder it opens, so one on disk is
    normal. .gitignore keeps it out of commits and install.sh strips it from
    copies, which leaves a tracked file as the only defect. Outside a git
    checkout nothing filters it, so every file on disk counts.
    """
    listed = subprocess.run(
        ["git", "ls-files"], cwd=REPO_ROOT, capture_output=True, text=True
    )
    if listed.returncode != 0:
        return list(REPO_ROOT.rglob(".DS_Store"))
    return [REPO_ROOT / rel for rel in listed.stdout.splitlines() if Path(rel).name == ".DS_Store"]


def check_skills(skills_root: Path, errors: list[str]) -> None:
    if not skills_root.exists():
        errors.append(f"{skills_root} does not exist")
        return

    forbidden_dirs = [skills_root / ".system"] + list(skills_root.glob("openspec-*"))
    for path in forbidden_dirs:
        if path.exists():
            errors.append(f"forbidden package path exists: {path}")

    for path in stray_ds_store():
        errors.append(f"remove .DS_Store: {path}")

    names: dict[str, Path] = {}
    for skill_dir in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        if not skill_dir.name.startswith("toby-"):
            errors.append(f"skill directory must start with toby-: {skill_dir}")
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", skill_dir.name):
            errors.append(f"invalid skill directory name: {skill_dir.name}")

        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            errors.append(f"missing SKILL.md: {skill_dir}")
            continue

        meta = frontmatter(skill_md.read_text())
        name = meta.get("name")
        desc = meta.get("description")
        if name != skill_dir.name:
            errors.append(f"{skill_md} frontmatter name must match directory")
        if not desc:
            errors.append(f"{skill_md} missing description")
        else:
            rendered = description_text(skill_md.read_text())
            if len(rendered) > DESCRIPTION_MAX:
                errors.append(
                    f"{skill_md} description is {len(rendered)} chars, over the {DESCRIPTION_MAX} ceiling"
                )
        if name:
            previous = names.get(name)
            if previous:
                errors.append(f"duplicate skill name {name}: {previous} and {skill_dir}")
            names[name] = skill_dir

        yaml_path = skill_dir / "agents" / "openai.yaml"
        if not yaml_path.exists():
            errors.append(f"missing agents/openai.yaml: {skill_dir}")
        elif name and f"${name}" not in yaml_path.read_text():
            errors.append(f"{yaml_path} default prompt should mention ${name}")

        for extra in ["README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"]:
            if (skill_dir / extra).exists():
                errors.append(f"remove extra skill doc: {skill_dir / extra}")


def check_stale_references(errors: list[str]) -> None:
    for path in text_files(REPO_ROOT):
        text = path.read_text(errors="ignore")
        if path.name == "validate-skills.py":
            continue
        if path == REPO_ROOT / "base" / "toby.md":
            continue
        for pattern in OLD_REFERENCES:
            for match in pattern.finditer(text):
                errors.append(f"stale reference {match.group(0)!r}: {path}:{line_for_offset(text, match.start())}")


def check_review_skill(errors: list[str]) -> None:
    review = REPO_ROOT / "skills" / "toby-code-review" / "SKILL.md"
    text = review.read_text()
    for match in REVIEW_TOOL_NAMES.finditer(text):
        errors.append(f"tool-specific review wording {match.group(0)!r}: {review}:{line_for_offset(text, match.start())}")


def check_operating_guide_refs(errors: list[str]) -> None:
    """A skill may not name the operating guide by any file path.

    Skills install standalone. The guide installs as a marked block inside
    whichever file the host tool already reads, so `base/toby.md` is a repo
    path that exists nowhere after install, and `AGENTS.md's ask-list` is only
    the right filename on one of the four targets. Say "the operating guide";
    it is always loaded, so no path is needed to reach it. Plain `AGENTS.md`
    stays legal because toby-swd-docs means the user's own module doc by it.
    """
    for path in text_files(REPO_ROOT / "skills"):
        if path == VOICE_REFERENCE_COPY:
            continue
        text = path.read_text(errors="ignore")
        rel = path.relative_to(REPO_ROOT)
        for pattern in OPERATING_GUIDE_PATHS:
            for match in pattern.finditer(text):
                errors.append(
                    f"operating guide named by path {match.group(0)!r}, "
                    f"write \"the operating guide\": {rel}:{line_for_offset(text, match.start())}"
                )


# These files quote the rules in order to state them, so scanning them for the
# words they define would fail by design.
VOICE_SCAN_EXEMPT = {
    REPO_ROOT / "base" / "toby.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "instructions" / "claude" / "CLAUDE.md",
    REPO_ROOT / "instructions" / "copilot" / "copilot-instructions.md",
    REPO_ROOT / "instructions" / "kiro" / "toby-instructions.md",
    REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md",
    REPO_ROOT / "skills" / "toby-voice" / "references" / "plain-language.md",
    REPO_ROOT / "skills" / "toby-voice" / "references" / "plain-language-examples.md",
    REPO_ROOT / "skills" / "toby-voice" / "references" / "examples" / "banned-writing-patterns.md",
}

FENCE_RE = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
TABLE_ROW_RE = re.compile(r"^\|.*$", re.M)
# A blockquote is quoted material, which the Banned Words exemption covers. The
# worked examples quote bad copy on purpose so the reader can see it.
BLOCKQUOTE_RE = re.compile(r"^>.*$", re.M)
# Emphasis spans carry cited titles, which the same exemption covers. README
# names Robert C. Martin's *Clean Code*, and that is the book's name.
EMPHASIS_RE = re.compile(r"(?<!\*)\*(?!\*)[^*\n]+\*(?!\*)|(?<!_)_(?!_)[^_\n]+_(?!_)")


def prose_only(text: str) -> str:
    """Blank out everything that is not prose, keeping byte offsets intact.

    Line and column numbers stay usable because each stripped span is replaced
    with spaces of the same width. Without this the scan fires on `API_KEY`
    inside a fenced block and every new check inherits the false positive.
    """

    def blank(match: re.Match[str]) -> str:
        return "".join(" " if ch != "\n" else "\n" for ch in match.group(0))

    for pattern in (FRONTMATTER_RE, FENCE_RE, INLINE_CODE_RE, TABLE_ROW_RE, BLOCKQUOTE_RE, EMPHASIS_RE):
        text = pattern.sub(blank, text)
    return text


def prose_paths() -> list[Path]:
    """Every markdown file Toby's prose rules apply to."""
    paths = sorted(p for p in (REPO_ROOT / "skills").rglob("*.md"))
    # Repo-root markdown faces the same floor as a skill. A plan or a design note
    # that ships banned words is the same defect in a file nobody validated.
    paths.extend(sorted(REPO_ROOT.glob("*.md")))
    paths.extend(sorted((REPO_ROOT / "output-styles").glob("*.md")))
    paths.append(REPO_ROOT / "base" / "toby.md")
    # AGENTS.md and instructions/** are generated from base/toby.md by sync.sh,
    # so scanning them would report every finding five times over.
    generated = {
        REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md",
        REPO_ROOT / "AGENTS.md",
        REPO_ROOT / "output-styles" / "toby.md",
        REPO_ROOT / "instructions" / "claude" / "CLAUDE-floor.md",
    }
    return [p for p in paths if p not in generated]


def voice_scan_paths() -> list[Path]:
    """Files scanned for banned words. Files that define the list are exempt."""
    return [p for p in prose_paths() if p not in VOICE_SCAN_EXEMPT]


def check_voice_compliance(errors: list[str], warnings: list[str]) -> None:
    tiers = load_banned_words()
    hard_re = [
        (word, re.compile(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", re.I))
        for word in tiers["hard"]
    ]
    sense_re = [
        (word, re.compile(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", re.I))
        for word in tiers["sense"]
    ]
    for path in voice_scan_paths():
        text = prose_only(path.read_text())
        rel = path.relative_to(REPO_ROOT)
        for _word, pattern in hard_re:
            for match in pattern.finditer(text):
                errors.append(f"banned word {match.group(0)!r}: {rel}:{line_for_offset(text, match.start())}")
        for _word, pattern in sense_re:
            for match in pattern.finditer(text):
                warnings.append(
                    f"check sense of {match.group(0)!r} (banned as intensifier or significance flag): "
                    f"{rel}:{line_for_offset(text, match.start())}"
                )
        for pattern in CONTRAST_PATTERNS:
            for match in pattern.finditer(text):
                warnings.append(f"possible invented foil {match.group(0)!r}: {rel}:{line_for_offset(text, match.start())}")


# Words used outside their everyday meaning, every one found in this repo's own
# prose by a reader who had to stop and work out what was meant. A coined term
# costs the reader a guess, and no other check sees it: each of these is a real
# English word, so the banned list and the sense-scoped list both pass it.
#
# `shape` and `key` are handled by the sense-scoped tier already. `primitive`
# was tried and removed: it is a real term in graphics and in programming, and
# every hit was correct usage.
COINED_TERMS = {
    "first-read": "say when the reader reads it",
    "blast radius": "say what else the change touches",
    "surface area": "say what callers can reach",
    "load-bearing": "say what fails without it",
    "north star": "say the goal",
    "forcing function": "say what makes it happen",
    "cognitive surface": "say what the reader has to hold",
    "lens": "say whose view, or what it is being judged against",
    "seam": "say where, in plain words",
    "affordance": "say what it lets the reader do",
    "the shape of the work": "say what the work involves",
}
COINED_RE = [
    (term, re.compile(rf"(?<![A-Za-z]){re.escape(term)}(?![A-Za-z])", re.I))
    for term in COINED_TERMS
]


# Figurative frames that dress an abstract thing as a physical one. Every entry
# was written in this repo: "a performance problem dressed as an error", "rung 2
# wearing a prop", "leakage with a new hat", "two-way coupling masquerading as
# reuse". The guide bans invented metaphor, and nothing else here sees these,
# because every word in them is ordinary.
#
# The list is frames, not subjects, so it cannot catch a fresh metaphor built
# from a frame nobody has used yet. A reader is still the only check for that.
# "moving parts" was tried and left out: it is a dead metaphor, in the
# dictionary, and the guide keeps established terms of art.
FIGURATIVE_FRAMES = [
    "wearing a", "wears a", "dressed as", "dressed up as", "in disguise",
    "masquerading as", "pretending to be", "with a new hat", "with a hat on",
    "under the hood", "in a trench coat", "puts on a", "wrapped in a costume",
]
FIGURATIVE_RE = [
    (frame, re.compile(rf"(?<![A-Za-z]){re.escape(frame)}(?![A-Za-z])", re.I))
    for frame in FIGURATIVE_FRAMES
]


def check_figurative_frames(warnings: list[str]) -> None:
    """Flag an abstract thing described as wearing, dressing, or disguising itself.

    A sentence cannot wear a hat. The guide bans invented metaphor and this is
    the commonest form it takes here, because the words are all ordinary and no
    other check reads them.
    """
    for path in voice_scan_paths():
        text = prose_only(path.read_text())
        rel = path.relative_to(REPO_ROOT)
        for frame, pattern in FIGURATIVE_RE:
            for match in pattern.finditer(text):
                warnings.append(
                    f"figurative frame {match.group(0)!r}, say what the thing is: "
                    f"{rel}:{line_for_offset(text, match.start())}"
                )


def check_coined_terms(warnings: list[str]) -> None:
    """Flag a word doing a job its everyday meaning does not cover.

    Rule 14 in plain-language.md. Every term here was written in this repo and
    then flagged by a reader who could not tell what it meant. A reader who has
    to guess is the cost, and it is invisible to every other check.
    """
    for path in voice_scan_paths():
        text = prose_only(path.read_text())
        rel = path.relative_to(REPO_ROOT)
        for term, pattern in COINED_RE:
            for match in pattern.finditer(text):
                warnings.append(
                    f"coined term {match.group(0)!r}, {COINED_TERMS[term]}: "
                    f"{rel}:{line_for_offset(text, match.start())}"
                )


def check_single_source(errors: list[str]) -> None:
    """No file outside base/toby.md may carry its own banned-word list."""
    for path in voice_scan_paths():
        text = path.read_text()
        if re.search(r"^#+ Banned words?\s*$", text, re.M | re.I):
            rel = path.relative_to(REPO_ROOT)
            line = line_for_offset(text, re.search(r"^#+ Banned words?\s*$", text, re.M | re.I).start())
            errors.append(f"second banned-word list, base/toby.md owns the only one: {rel}:{line}")


LATIN_ABBREV_RE = re.compile(r"(?<![A-Za-z])(e\.g\.|i\.e\.|etc\.|viz\.|cf\.)", re.I)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")
# A sentence Toby writes runs to 25 words. The hard error sits at 35 so quoted
# material and inline lists cannot trip it; 25 to 35 warns instead.
SENTENCE_CEILING = 25
SENTENCE_HARD_LIMIT = 35
PARAGRAPH_SENTENCE_LIMIT = 6


LIST_MARKER_RE = re.compile(r"^(#|-|\*|\||>|\d+[.)]|[A-Za-z][.)]\s)")


def is_word_list(line: str) -> bool:
    """A comma-separated run of short items is a list, so it has no sentences."""
    items = [item.strip() for item in line.rstrip(".").split(",")]
    return len(items) >= 8 and all(item and len(item.split()) <= 4 for item in items)


def is_prose_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or LIST_MARKER_RE.match(stripped):
        return False
    return not is_word_list(stripped)


def sentences_in(body: str) -> list[str]:
    """Split into sentences, keeping abbreviations from faking a boundary."""
    guarded = LATIN_ABBREV_RE.sub(lambda m: m.group(0).replace(".", "\0"), body)
    return [s.replace("\0", ".") for s in SENTENCE_SPLIT_RE.split(guarded) if s.strip()]


def check_ste_conformance(warnings: list[str]) -> None:
    """The clarity floor, reported as warnings.

    Every check here is a heuristic on prose, so none of them gates the build.
    Pass --strict to fail on them. This runs over base/toby.md too: the file
    states the rules, so it obeys them.
    """
    for path in prose_paths():
        text = prose_only(path.read_text())
        rel = path.relative_to(REPO_ROOT)

        for number, line in enumerate(text.splitlines(), 1):
            if not is_prose_line(line):
                continue
            for sentence in sentences_in(line.strip()):
                count = len(sentence.split())
                if count > SENTENCE_HARD_LIMIT:
                    warnings.append(f"sentence runs {count} words, well over the {SENTENCE_CEILING} ceiling: {rel}:{number}")
                elif count > SENTENCE_CEILING:
                    warnings.append(f"sentence runs {count} words, over the {SENTENCE_CEILING} ceiling: {rel}:{number}")

        for match in LATIN_ABBREV_RE.finditer(text):
            warnings.append(f"Latin abbreviation {match.group(0)!r}, write it out: {rel}:{line_for_offset(text, match.start())}")

        for block in re.split(r"\n\s*\n", text):
            body = " ".join(line.strip() for line in block.splitlines() if is_prose_line(line))
            if not body:
                continue
            count = len(sentences_in(body))
            if count > PARAGRAPH_SENTENCE_LIMIT:
                offset = text.find(block)
                warnings.append(
                    f"paragraph runs {count} sentences, over the {PARAGRAPH_SENTENCE_LIMIT} limit: "
                    f"{rel}:{line_for_offset(text, offset)}"
                )


# A SKILL.md body over this loads more than any single task reads. The number is
# the largest body that measured useful, rounded up, and it fails rather than
# warns because a body creeps past it one paragraph at a time.
BODY_TOKEN_CEILING = 5600

# Skills that load together on one task. The total is what a turn actually pays.
ROUTING_GROUPS = {
    "feature-change": [
        "toby-swd-strategy", "toby-swd-modules", "toby-swd-interfaces",
        "toby-swd-complexity", "toby-swd-clarity", "toby-swd-testing",
        "toby-swd-docs",
    ],
    "feature-dev": ["toby-feature-dev", "toby-swd-strategy", "toby-swd-testing"],
    "review": ["toby-code-review", "toby-simplify-code"],
}
COLOAD_TOKEN_CEILING = 19000

# These two never fire on their own. A request to make a game, or to brainstorm,
# reaches them only when the user names the skill or types its slash command.
# The rule lives in two places that can drift apart, so both are checked: the
# description the host tool reads when deciding, and the routing line in the
# operating guide. toby-game had the clause in its description and no line in
# the guide at all, which left the rule stated once and enforced nowhere.
INVOKE_ONLY_SKILLS = ["toby-game", "toby-squall", "toby-learning"]
INVOKE_ONLY_DESCRIPTION_RE = re.compile(
    r"trigger only when the (?:user|creator) explicitly invokes", re.I
)


def check_invoke_only(errors: list[str]) -> None:
    guide = BASE_TOBY.read_text()
    for name in INVOKE_ONLY_SKILLS:
        skill_md = REPO_ROOT / "skills" / name / "SKILL.md"
        if not skill_md.exists():
            continue
        desc = description_text(skill_md.read_text())
        if not INVOKE_ONLY_DESCRIPTION_RE.search(desc):
            errors.append(
                f"{name} must fire only on explicit invocation, and its description "
                "does not say so. Write \"Trigger only when the user explicitly invokes\"."
            )
        if not re.search(rf"Use `{name}` only when the user invokes it by name", guide):
            errors.append(
                f"base/toby.md Skill Routing has no invoke-only line for {name}, "
                "so the routing block does not hold the rule its description states."
            )
        for pattern in (r"\bUse `" + name + r"` (?:for|when|whenever)\b",):
            if re.search(pattern, guide):
                errors.append(
                    f"base/toby.md routes {name} on conditions, and it fires only on "
                    "explicit invocation."
                )


# An anti-trigger is written two ways. Most skills say "skip it for X". The
# invoke-only skills say "trigger only when ... by name" and then name what must
# not fire them. Reading only the first form reported three skills as having no
# anti-trigger while they carried the strictest ones in the repo.
SKIP_CLAUSE_RE = re.compile(
    r"\bskip (?:it|this skill)\b|\bdo not trigger\b|\btrigger only when\b|\bonly when the user invokes\b",
    re.I,
)

# A section that opens on a declarative states a thesis and buries the rule under
# it. The reader pays for that in every skill, and no other check sees it.
IMPERATIVE_OPENERS = re.compile(
    r"^(?:\*\*)?(?:"
    r"[A-Z][a-z]+(?:e|t|d|k|p|n|y|w|x|r|l|m|g|h|s)?\b"
    r")"
)
# Verbs that actually open a rule. Kept explicit, because part-of-speech guessing
# on one word flags every noun that looks like a verb.
IMPERATIVES = {
    "add", "apply", "ask", "avoid", "build", "call", "cap", "check", "choose",
    "close", "collapse", "compare", "confirm", "cover", "cut", "declare",
    "decide", "default", "defer", "delete", "design", "do", "drop", "escalate",
    "establish", "explain", "find", "fix", "flag", "fold", "follow", "give",
    "handle", "hide", "hold", "inspect", "keep", "leave", "list", "load",
    "look", "make", "mark", "match", "measure", "merge", "move", "name",
    "never", "offer", "open", "order", "pick", "pin", "point", "prefer",
    "prove", "pull", "put", "raise", "read", "record", "reduce", "refuse",
    "reject", "remove", "rename", "replace", "report", "require", "reserve",
    "resist", "resolve", "return", "review", "rewrite", "run", "say", "scope",
    "send", "set", "show", "skip", "sketch", "split", "start", "state", "stay",
    "stop", "take", "tell", "test", "track", "treat", "trim", "turn", "use",
    "verify", "wait", "weigh", "widen", "write", "don't", "do not", "prefer",
    "create", "see", "spend", "treat", "cover", "note", "only", "start",
    "sketch", "assume", "count", "push", "reach", "carry", "own", "opt",
    "update", "document", "describe", "raise", "hunt", "quote", "collapse",
    "watch", "weigh", "gate", "trust", "batch", "cache", "log",
    "lead", "place", "recover", "collaborate", "ship", "reorder", "teach",
    "build", "cut", "sketch", "reduce", "turn", "pin", "brief",
}


def skill_dirs() -> list[Path]:
    root = REPO_ROOT / "skills"
    return sorted(d for d in root.iterdir() if d.is_dir() and (d / "SKILL.md").exists())


def body_of(text: str) -> str:
    if not text.startswith("---\n"):
        return text
    end = text.find("\n---", 4)
    return text if end < 0 else text[end + 4 :]


def tokens(text: str) -> int:
    return round(len(text) / 4)


def check_token_budget(errors: list[str], warnings: list[str]) -> None:
    """Bodies and co-load groups have a ceiling, so a gain cannot regress quietly."""
    sizes: dict[str, int] = {}
    for skill_dir in skill_dirs():
        size = tokens(body_of((skill_dir / "SKILL.md").read_text()))
        sizes[skill_dir.name] = size
        if size > BODY_TOKEN_CEILING:
            errors.append(
                f"{skill_dir.name} body is ~{size} tokens, over the {BODY_TOKEN_CEILING} ceiling"
            )
    for group, members in ROUTING_GROUPS.items():
        total = sum(sizes.get(name, 0) for name in members)
        if total > COLOAD_TOKEN_CEILING:
            errors.append(
                f"routing group {group!r} co-loads ~{total} tokens, over the {COLOAD_TOKEN_CEILING} ceiling"
            )


def check_cross_skill_collisions(warnings: list[str]) -> None:
    """One sentence in two SKILL.md bodies means two owners and a coming drift."""
    seen: dict[str, str] = {}
    for skill_dir in skill_dirs():
        text = prose_only((skill_dir / "SKILL.md").read_text())
        for line in text.splitlines():
            if not is_prose_line(line):
                continue
            for sentence in sentences_in(line.strip()):
                key = re.sub(r"[^a-z ]", " ", sentence.lower())
                key = re.sub(r"\s+", " ", key).strip()
                if len(key.split()) < 8:
                    continue
                if key in seen and seen[key] != skill_dir.name:
                    warnings.append(
                        f"sentence duplicated in {seen[key]} and {skill_dir.name}, "
                        f"pick one owner: {sentence.strip()[:70]}..."
                    )
                seen.setdefault(key, skill_dir.name)


# Two citation styles reach the same file. Every skill but one writes
# `references/foo.md`; toby-game wrote a bare `foo.md` in its References list.
# Matching only the prefixed form made this check blind to that whole file, and
# a pointer at a deleted `visual-identity.md` survived inside the blind spot.
REFERENCE_RE = re.compile(r"`references/([A-Za-z0-9_./-]+\.md)`")
BARE_REFERENCE_RE = re.compile(r"`([A-Za-z0-9_-]+\.md)`")

# Filenames a skill names because they exist in the user's repo or in this one,
# never because they sit under references/. Without this the bare-name pass
# reads every mention of AGENTS.md as a broken pointer.
NOT_A_REFERENCE = {
    "SKILL.md", "AGENTS.md", "README.md", "CLAUDE.md", "CHANGELOG.md",
    "plan.md", "intent.md", "spec.md", "REVIEW.md", "behavior.md",
    "copilot-instructions.md", "toby-instructions.md", "toby.md",
}


def check_reference_reachability(errors: list[str], warnings: list[str]) -> None:
    """Every named reference exists, and every reference file is named."""
    for skill_dir in skill_dirs():
        refs_dir = skill_dir / "references"
        named: set[str] = set()
        for path in [skill_dir / "SKILL.md"] + (sorted(refs_dir.rglob("*.md")) if refs_dir.exists() else []):
            text = path.read_text()
            matches = list(REFERENCE_RE.finditer(text))
            if refs_dir.exists():
                matches += [
                    m for m in BARE_REFERENCE_RE.finditer(text)
                    if m.group(1) not in NOT_A_REFERENCE
                ]
            for match in matches:
                # A skill may cite another skill's reference, and that path is
                # relative to the other skill. toby-learning points at
                # toby-voice's plain-language.md, which is correct and not a break.
                lead = text[max(0, match.start() - 60) : match.start()]
                if re.search(r"`toby-(?!" + skill_dir.name[5:] + r")[a-z-]+`", lead):
                    continue
                named.add(match.group(1))
                target = refs_dir / match.group(1)
                if not target.exists():
                    errors.append(
                        f"{path.relative_to(REPO_ROOT)} names references/{match.group(1)}, which does not exist"
                    )
        if not refs_dir.exists():
            continue
        for path in sorted(refs_dir.rglob("*.md")):
            rel = path.relative_to(refs_dir).as_posix()
            if rel not in named:
                warnings.append(f"reference file nothing points at: {path.relative_to(REPO_ROOT)}")


SPLIT_BACKTICK_RE = re.compile(r"`[^`\n]*\s[^`\n]*`")


def check_description_backticks(errors: list[str]) -> None:
    """A folded description wraps, and a wrap inside backticks renames a skill.

    `toby-swd-clarity` broke across two lines once and rendered as
    `toby-swd- clarity`, which points at nothing. The routing line reads that
    string, so the skip clause stopped naming a real skill.
    """
    for skill_dir in skill_dirs():
        desc = description_text((skill_dir / "SKILL.md").read_text())
        if desc.count("`") % 2:
            errors.append(f"{skill_dir.name} description has an unclosed backtick")
        for match in SPLIT_BACKTICK_RE.finditer(desc):
            if "toby-" in match.group(0):
                errors.append(
                    f"{skill_dir.name} description names {match.group(0)!r}, "
                    "which is a skill name broken across a line wrap"
                )


def check_anti_triggers(warnings: list[str]) -> None:
    """A description with no skip clause fires on every adjacent task."""
    for skill_dir in skill_dirs():
        desc = description_text((skill_dir / "SKILL.md").read_text())
        if not SKIP_CLAUSE_RE.search(desc):
            warnings.append(
                f"{skill_dir.name} description carries no skip clause, so nothing stops it over-firing"
            )


# A rule may open on its condition ("Before finishing, check ...") or state
# itself with a modal ("An assertion should fail when ..."). Both lead with the
# rule. Only a sentence that leads with neither is burying it.
LEADING_CONDITION_RE = re.compile(
    r"^(?:before|when|whenever|if|after|once|where|while|unless|until|for|on|in)\b[^,.]{0,90},\s*",
    re.I,
)
MODAL_RE = re.compile(r"\b(?:must|should|never|always|has to|have to|belongs?|stays?|goes?|wins?)\b", re.I)


def first_word(sentence: str) -> str:
    text = LEADING_CONDITION_RE.sub("", sentence.strip().lstrip("*"))
    match = re.match(r"\**([A-Za-z']+)", text)
    return match.group(1).lower() if match else ""


# A short opener is not a buried lead, whatever its grammar. "Four kinds, each
# with its own home." costs a reader nothing. The failure this check exists for
# is the long abstract preamble that pushes the rule into paragraph three, so
# the length floor is what keeps it from firing on prose readers find clear.
BURIED_LEAD_MIN_WORDS = 16


def leads_with_rule(sentence: str) -> bool:
    stripped = sentence.strip()
    if stripped.endswith(":"):
        return True
    if len(stripped.split()) < BURIED_LEAD_MIN_WORDS:
        return True
    if first_word(stripped) in IMPERATIVES:
        return True
    head = " ".join(stripped.split()[:12])
    return bool(MODAL_RE.search(head))


def check_buried_leads(warnings: list[str]) -> None:
    """A `##` section that opens on a declarative buries its rule under a thesis.

    Heuristic on prose, so it warns. It catches the failure that costs a reader
    the most and that sentence length and banned words never see: a file that
    passes every floor check while stating its point in paragraph three.
    """
    for skill_dir in skill_dirs():
        path = skill_dir / "SKILL.md"
        text = prose_only(path.read_text())
        rel = path.relative_to(REPO_ROOT)
        blocks = re.split(r"^(#{2,3} .+)$", text, flags=re.M)
        for heading, body in zip(blocks[1::2], blocks[2::2]):
            line_no = line_for_offset(text, text.index(heading))
            for line in body.splitlines():
                if not is_prose_line(line):
                    continue
                opening = sentences_in(line.strip())
                if not opening:
                    continue
                if not leads_with_rule(opening[0]):
                    warnings.append(
                        f"section opens on a thesis, lead with the rule: {rel}:{line_no} "
                        f"({heading.strip()[:40]})"
                    )
                break

        desc = description_text(path.read_text())
        opening = sentences_in(desc)
        if opening and not leads_with_rule(opening[0]):
            warnings.append(
                f"description opens on a thesis, lead with what the skill does: {rel}"
            )


INSTALL_TARGETS = [
    Path.home() / ".codex" / "skills",
    Path.home() / ".claude" / "skills",
    Path.home() / ".copilot" / "skills",
    Path.home() / ".kiro" / "skills",
]


def check_install_drift(warnings: list[str]) -> None:
    """The installed copies are what actually runs, so say when they differ.

    A warning, not an error. A machine with nothing installed is a valid state,
    and so is a machine mid-edit. A before-and-after measured against a stale
    install compares two unknown vintages, which is what this is here to say.
    """
    for root in INSTALL_TARGETS:
        if not root.exists():
            continue
        stale = []
        for skill_dir in skill_dirs():
            installed = root / skill_dir.name / "SKILL.md"
            if not installed.exists():
                stale.append(f"{skill_dir.name} (missing)")
            elif installed.read_text() != (skill_dir / "SKILL.md").read_text():
                stale.append(skill_dir.name)
        if stale:
            warnings.append(
                f"installed copy differs from the repo in {root}: {', '.join(stale[:6])}"
                + (f" and {len(stale) - 6} more" if len(stale) > 6 else "")
                + ". Run scripts/install.sh --force."
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_root", nargs="?", default="skills")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail the run on warnings too. Heuristic checks warn by default so they never gate CI.",
    )
    parser.add_argument(
        "--check-install",
        action="store_true",
        help="also compare the installed copies under $HOME against the repo.",
    )
    args = parser.parse_args()

    skills_root = (REPO_ROOT / args.skills_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    check_skills(skills_root, errors)
    check_instruction_sync(errors)
    check_output_style(errors)
    check_floor_complements_style(errors)
    check_stale_references(errors)
    check_review_skill(errors)
    check_operating_guide_refs(errors)
    check_voice_compliance(errors, warnings)
    check_single_source(errors)
    check_coined_terms(warnings)
    check_figurative_frames(warnings)
    check_ste_conformance(warnings)
    check_token_budget(errors, warnings)
    check_cross_skill_collisions(warnings)
    check_reference_reachability(errors, warnings)
    check_description_backticks(errors)
    check_invoke_only(errors)
    check_anti_triggers(warnings)
    check_buried_leads(warnings)
    if args.check_install:
        check_install_drift(warnings)

    for warning in warnings:
        print(f"warn: {warning}", file=sys.stderr)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    if warnings and args.strict:
        print(f"\n{len(warnings)} warnings, and --strict is on.", file=sys.stderr)
        return 1

    if warnings:
        print(f"Toby package validation passed with {len(warnings)} warnings.")
    else:
        print("Toby package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
