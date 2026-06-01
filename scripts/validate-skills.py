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

BANNED_WORDS = [
    "delve",
    "leverage",
    "seamless",
    "robust",
    "tapestry",
    "comprehensive",
    "nuanced",
    "honestly",
    "genuinely",
    "clearly",
    "fair",
    "to be fair",
    "great question",
    "good point",
    "hope this helps",
    "let me know if",
    "feel free",
    "generally",
    "arguably",
    "in many cases",
    "it depends",
    "just a thought",
    "quite",
    "obviously",
    "indeed",
    "merely",
    "essentially",
    "deeply",
    "profoundly",
    "to be frank",
    "simply",
    "straightforward",
    "interestingly",
    "surprisingly",
    "ironically",
    "crucial",
    "vital",
    "essential",
    "important",
    "importantly",
    "particularly",
    "notably",
    "key",
    "load-bearing",
    "it's worth noting",
    "that's fair",
    "certainly",
    "absolutely",
    "definitely",
    "sorry",
    "apologies",
    "i hope",
    "you're welcome",
    "i'd be glad to",
    "here to help",
    "in order to",
    "the reason being",
    "in conclusion",
    "in summary",
    "moreover",
    "furthermore",
    "moving forward",
    "at a high level",
    "takeaway",
    "ecosystem",
    "journey",
    "landscape",
    "unlock",
    "empower",
    "best practices",
    "myriad",
    "plethora",
    "world-class",
    "cutting-edge",
    "innovative",
    "balanced",
    "perspective",
    "clean",
    "genuine",
]

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


def check_voice_compliance(errors: list[str]) -> None:
    paths = [
        REPO_ROOT / "skills" / "toby-code-review" / "SKILL.md",
        REPO_ROOT / "skills" / "toby-explain" / "SKILL.md",
        REPO_ROOT / "skills" / "toby-feature-dev" / "SKILL.md",
        REPO_ROOT / "skills" / "toby-learning" / "SKILL.md",
        REPO_ROOT / "skills" / "toby-simplify-code" / "SKILL.md",
    ]
    banned_re = [
        re.compile(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", re.I)
        for word in BANNED_WORDS
    ]
    for path in paths:
        text = path.read_text()
        for pattern in banned_re:
            match = pattern.search(text)
            if match:
                errors.append(f"banned word {match.group(0)!r}: {path}:{line_for_offset(text, match.start())}")
        for pattern in CONTRAST_PATTERNS:
            match = pattern.search(text)
            if match:
                errors.append(f"contrastive phrasing {match.group(0)!r}: {path}:{line_for_offset(text, match.start())}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("skills_root", nargs="?", default="skills")
    args = parser.parse_args()

    skills_root = (REPO_ROOT / args.skills_root).resolve()
    errors: list[str] = []

    check_skills(skills_root, errors)
    check_instruction_sync(errors)
    check_stale_references(errors)
    check_review_skill(errors)
    check_voice_compliance(errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print("Toby package validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
