"""The voice rules, as code: the banned words, the patterns, and prose splitting.

voice-check.py runs these against any text. validate-skills.py imports them to
check the skills in this repo. The rules sit in their own file so the checker
runs with this file and base/toby.md alone, which is all the installed kit holds.
"""
from __future__ import annotations

import re
from pathlib import Path

# The repo root, or ~/.claude/toby in the installed kit. Both keep base/toby.md
# one level above this file.
REPO_ROOT = Path(__file__).resolve().parents[1]


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


def line_for_offset(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


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


LATIN_ABBREV_RE = re.compile(r"(?<![A-Za-z])(e\.g\.|i\.e\.|etc\.|viz\.|cf\.)", re.I)
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


# A sentence Toby writes runs to 25 words. validate-skills.py sets the hard limit.
SENTENCE_CEILING = 25
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
