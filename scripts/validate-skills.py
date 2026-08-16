#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
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


def check_skills(skills_root: Path, errors: list[str]) -> None:
    if not skills_root.exists():
        errors.append(f"{skills_root} does not exist")
        return

    forbidden_dirs = [skills_root / ".system"] + list(skills_root.glob("openspec-*"))
    for path in forbidden_dirs:
        if path.exists():
            errors.append(f"forbidden package path exists: {path}")

    for path in REPO_ROOT.rglob(".DS_Store"):
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


# These files quote the rules in order to state them, so scanning them for the
# words they define would fail by design.
VOICE_SCAN_EXEMPT = {
    REPO_ROOT / "base" / "toby.md",
    REPO_ROOT / "AGENTS.md",
    REPO_ROOT / "instructions" / "claude" / "CLAUDE.md",
    REPO_ROOT / "instructions" / "copilot" / "copilot-instructions.md",
    REPO_ROOT / "instructions" / "kiro" / "toby-instructions.md",
    REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md",
    REPO_ROOT / "skills" / "toby-voice" / "references" / "ste-floor.md",
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
    paths.append(REPO_ROOT / "README.md")
    paths.append(REPO_ROOT / "base" / "toby.md")
    # AGENTS.md and instructions/** are generated from base/toby.md by sync.sh,
    # so scanning them would report every finding five times over.
    generated = {
        REPO_ROOT / "skills" / "toby-voice" / "references" / "toby.md",
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_root", nargs="?", default="skills")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail the run on warnings too. Heuristic checks warn by default so they never gate CI.",
    )
    args = parser.parse_args()

    skills_root = (REPO_ROOT / args.skills_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    check_skills(skills_root, errors)
    check_instruction_sync(errors)
    check_stale_references(errors)
    check_review_skill(errors)
    check_voice_compliance(errors, warnings)
    check_single_source(errors)
    check_ste_conformance(warnings)

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
