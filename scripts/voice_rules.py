"""The voice rules, as code: the banned words, the patterns, and prose splitting.

voice-check.py runs these against any text. validate-skills.py imports them to
check the skills in this repo. The rules are in their own file so the checker
runs with this file and base/toby.md alone, which is all the installed kit holds.
"""
from __future__ import annotations

import re
from pathlib import Path

# The repo root, or ~/.claude/toby in the installed kit. Both keep base/toby.md
# one level above this file.
REPO_ROOT = Path(__file__).resolve().parents[1]


BASE_TOBY = REPO_ROOT / "base" / "toby.md"


# The banned-word lists are in base/toby.md under "## Banned Words" and are read
# from there. Keeping a second copy here is how the two lists drifted apart the
# last time: base had 33 words the artifact-style copy never had.
BANNED_SECTION_RE = re.compile(r"^## Banned Words\n(.*?)(?=^## )", re.M | re.S)
BANNED_TIER_RE = re.compile(r"^### (.+?)\n(.*?)(?=^### |\Z)", re.M | re.S)


def _split_words(block: str) -> list[str]:
    """Pull the comma-separated word list out of a tier body.

    A tier body is one explanatory sentence followed by the list. The list is
    recognized by form: every comma-separated item is at most four words and
    contains no backtick, quote, or terminal punctuation of its own.
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


# Emphasis spans mark cited titles, which the same exemption covers. README
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
    # Verbs of place and motion used for code, rules, and findings. A rule is in
    # a file, and a finding depends on the diff. The eval writers and this repo
    # both wrote each of these, and the reader stopped on every one.
    "lives in", "lives at", "lives on", "lives inside", "lives next to", "living in",
    "live inside", "sits in", "sits on", "sits at", "sits above", "sits below",
    "sits outside", "sits inside", "sits next to", "sits beside", "sitting in",
    "sitting outside", "land", "lands", "landed", "landing in", "land on", "not land",
    "falls through", "fall through", "rests on", "rest on", "feeds", "fed into",
    "glides over", "bites hardest", "racks up interest",
    # Idioms. Each asks the reader to translate before they can read on.
    "earns its keep", "earn their keep", "earns its place", "earn their place",
    "earns its complexity", "boils down to", "at the end of the day",
    "low-hanging fruit", "silver bullet", "rabbit hole", "table stakes",
    "move the needle", "heavy lifting", "in the weeds", "band-aid", "footgun",
    "smoking gun", "red herring", "sweet spot", "deep dive", "game changer",
    "pain point", "double-edged",
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
    """A run of short items split by commas or middle dots is a list, so it has no sentences."""
    separator = " · " if line.count(" · ") >= 4 else ","
    items = [item.strip() for item in line.rstrip(".").split(separator)]
    return len(items) >= 5 if separator == " · " else (
        len(items) >= 8 and all(item and len(item.split()) <= 4 for item in items))


def is_prose_line(line: str) -> bool:
    stripped = line.strip()
    if not stripped or LIST_MARKER_RE.match(stripped):
        return False
    return not is_word_list(stripped)


def sentences_in(body: str) -> list[str]:
    """Split into sentences, keeping abbreviations from faking a boundary."""
    guarded = LATIN_ABBREV_RE.sub(lambda m: m.group(0).replace(".", "\0"), body)
    return [s.replace("\0", ".") for s in SENTENCE_SPLIT_RE.split(guarded) if s.strip()]


# Slogans. Every form below came from agent-written docs and decks that passed
# every other check in this file, because each word was plain and each sentence
# short. A short sentence is often right, so no check here can settle one of
# these. Each hit is a question for the writer.
SHORT_SENTENCE = 6
MIRROR_LIMIT = 10
# Opening words that repeat in ordinary prose without making a mirrored pair.
MIRROR_EXEMPT = {"the", "a", "an", "it", "this", "i", "then", "if", "when"}
WORD_RE = re.compile(r"[A-Za-z0-9][\w'-]*")
# "A plugin is data." and "Plugins are data." define a thing by one bare word.
DEFINITION_RE = re.compile(
    r"^(?:(?:A|An|Every|Each)\s+[\w-]+\s+is|[A-Z][\w-]*s\s+are)\s+(?:an?\s+)?[\w-]+\.$"
)
FRAGMENT_RE = re.compile(r"^(?:A|An|The)\s")
# Setup sentences name a count or a category and hold the thing back for the
# next sentence, as in "One file causes this failure." Every writer in the
# content eval opened its reply to a frustrated user this way.
SETUP_SENTENCE_RES = [
    re.compile(r"^(?:One|Two|Three|A single|Only one)\s+[\w-]+\s+(?:causes?|changes?|matters?|remains?|explains?|breaks?|fails?)\b[^.?!]*\.$"),
    re.compile(r"^(?:This|That|The)\s+[\w-]+\s+(?:has|comes from|traces back to|traces to|comes down to)\s+(?:one|a single|two|three)\s+[\w-]+\.$"),
    re.compile(r"^There (?:is|are) (?:one|a single|two|three|only one) [\w-]+(?: left)?\.$"),
]
# "Guard: none." and "Wiring: none new." put a label where a sentence belongs.
LABEL_NONE_RE = re.compile(r"^\s*(?:[-*]\s+)?\**[A-Z][\w -]{1,30}[:.]\**\s*\**(?:None|none)\b[^.]{0,20}\.")
# A sentence about the document itself, where the content should be.
NARRATION_RE = re.compile(
    r"^(?:Follow these steps|The following steps|Here are the steps|"
    r"This (?:deck|proposal|document|section|slide|README|guide) (?:proposes|asks|describes|covers|explains|shows|walks))\b"
)
# A sentence that opens like a noun phrase and never reaches a verb is a label
# with a period, as in "Phase 1 of 3 in the queue migration."
PHRASE_OPENER_RE = re.compile(r"^(?:A|An|The|This|That|These|Those|Phase|Step|Part|Stage|One|Two|Three|Four|Five|Six|\d+)\b")
IRREGULAR_VERB_RE = re.compile(
    r"^(?:\w+n't|must|should|would|could|may|might|shall|let|get|got|make|made|take|took|"
    r"give|gave|go|went|come|came|see|saw|say|said|keep|kept|run|ran|put|set|cut|hit|hold|"
    r"held|find|found|know|knew|show|shown|become|became|pay|paid|ship|stay|stop|start)$", re.I
)
# Habits predicted from what this reader has rejected so far. None of them is
# in the skills today, and agents write all of them, so each hit is a question.
PREDICTED_PATTERNS = [
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:The (?:result|catch|fix|problem|answer|twist|upshot|kicker|good news|bad news)|Why does (?:this|that|it) matter|So what does (?:this|that) mean|What does (?:this|that) mean|The short version)\?", re.M),
     "setup question"),
    (re.compile(r"\b(?:provides? the ability to|enables? the creation of|the implementation of|facilitates?|utilization|in terms of|with regard to|with respect to)\b", re.I),
     "noun doing a verb's job"),
    (re.compile(r"\b(?:the ask|bandwidth|action items?|learnings|net-new|quick win|big lift|touch base|level set|align on|alignment on|double down)\b", re.I),
     "meeting jargon"),
    (re.compile(r"\b(?:not only\b[^.]{0,60}\bbut also|less \w+, more \w+)\b", re.I), "rhythm device"),
    (re.compile(r"\b(?:super|incredibly|extremely|hugely|massively|insanely|ridiculously)\s+\w+", re.I), "vague intensifier"),
    (re.compile(r"\b(?:compiler|linter|test|tests|build|code|function|type checker|CI)\s+(?:complains?|is (?:happy|unhappy|angry|sad|upset)|gets (?:angry|upset|confused)|yells|screams|hates|loves|is not a fan)\b", re.I),
     "code given feelings"),
    (re.compile(r"\b(?:may|might|could) (?:potentially|possibly|perhaps|conceivably)\b", re.I), "hedge stack"),
    # What would have happened, stated as a result: "that failure would have paged
    # the on-call engineer". It is a prediction, and the reader takes it as fact.
    (re.compile(r"\bwould(?:n't| not)? have (?:been |either |also |still )?\w+(?:ed|en|ne|id|ot|aid|ught)\b", re.I),
     "would-have stated as fact"),
    # A claim about what the user did or is doing that the user never said.
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:Stop|Quit) \w+ing\b|\byou(?:'ve| have) been \w+ing\b|\byou(?:'re| are) (?:searching|looking|trying|chasing|stuck)\b", re.I | re.M),
     "claim about the user"),
    # "A plugin never imports an engine" in a document whose reader never assumed it did.
    (re.compile(r"\b(?:a|an|the|each|every)\s+[a-z]+s? never (?:imports?|calls?|touches|reads|writes|depends|uses|sends|returns|knows|sees)\b", re.I),
     "what a thing never does"),
    # "Relay treats model providers as swappable engines" gives a program a judgment.
    (re.compile(r"\b(?!Treat)\w+ treats \w+(?: \w+){0,3} as\b"), "program given a judgment"),
]
# Words too common to show that a bullet repeats its heading.
RESTATE_STOPWORDS = set(
    "a an the of to in on at by for from with and or but so is are was were be been it its this "
    "that these those there their they them as than then into onto over under which who what when "
    "where how all any each every no not do does did has have had can will would should may might "
    "must more most other same one two three four five six".split()
)
HEADING_LINE_RE = re.compile(r"^(?:#{1,6}\s+(.+)|\*\*(.+?)\*\*)$")


def content_words(text: str) -> set[str]:
    """The words that carry meaning, lowercased with a plural -s removed."""
    return {w.lower().rstrip("s") for w in WORD_RE.findall(text) if w.lower() not in RESTATE_STOPWORDS}


LIST_ITEM_RE = re.compile(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$")
# Litotes denies the opposite of what the writer means: "not uncommon" is "common".
LITOTES_RE = re.compile(
    r"\bnot (?:uncommon|unusual|unlike|unreasonable|unimportant|unhelpful|unknown|unfamiliar|"
    r"unlikely|unclear|unsafe|unwise|infrequent|insignificant|inconsiderable|inexpensive|"
    r"impossible|trivial|a small|bad|terrible|without (?:risk|merit|cost|reason|precedent))\b"
    r"|\bno (?:small|mean) (?:feat|amount|task|thing|part)\b",
    re.I,
)
# An abstract noun given a person's action: "complexity creeps in", "the design
# wants a cache". A reader has to work out who really acts.
ABSTRACT_ACTOR_RE = re.compile(
    r"\b(?:complexity|design|architecture|abstraction|decision|knowledge|logic|pattern|approach|"
    r"strategy|process|system|codebase|data|context|problem|code|interface|module)\s+"
    r"(?:wants?|knows?|thinks|believes|creeps?|screams?|tells?|cares?|fights?|resists?|resisting|"
    r"punish(?:es)?|rewards?|expects?|lies|hopes?|refuses?|insists?|begs?|demands?|invites?|"
    r"deserves?|forgives?|hates?|loves?|whispers?|shouts?|complains?|remembers?|forgets?)\b",
    re.I,
)
# A line with one of these is a sentence missing its period, such as the slide
# title "The queue service costs $400 a month", and is no fragment. The last word
# is left out of the test, because a plural noun there ends in -s too.
VERB_HINT_RE = re.compile(
    r"^(?:is|are|was|were|has|have|had|can|will|does|do|did|runs?|needs?|\w+(?:s|ed))$", re.I
)
HEADING_RE = re.compile(r"^#{1,6}\s+(?:\d+[.)]\s+)?(.+?)\s*$")
# A heading longer than this reads as a plain description, such as "Toby is
# careful to avoid breaking things". A short claim is the slogan: "Uniformity
# is the failure".
CLAIM_HEADING_LIMIT = 6
# A heading that opens on one of these words names a topic or asks a question,
# so it describes the section even when it holds a verb: "When the topic is code".
DESCRIPTIVE_OPENERS = {"when", "where", "what", "how", "why", "which", "who", "example", "step", "not"}
CLAIM_VERB_RE = re.compile(
    r"\b(?:is|are|was|were|never|always|carr(?:y|ies)|fails?|wins|beats|lives|sits|lands|holds)\b", re.I
)


def prose_paragraphs(text: str) -> list[tuple[int, str]]:
    """Join consecutive prose lines into paragraphs, with each one's first line number."""
    paragraphs: list[tuple[int, str]] = []
    lines: list[str] = []
    start = 0
    for number, line in enumerate(text.splitlines() + [""], 1):
        if is_prose_line(line):
            if not lines:
                start = number
            lines.append(line.strip())
        elif lines:
            paragraphs.append((start, " ".join(lines)))
            lines = []
    return paragraphs


def slogan_findings(text: str) -> list[tuple[int, str, str]]:
    """Return (line, form, excerpt) for each slogan form in text from prose_only.

    The forms are a heading written as a claim, a noun phrase with no verb, a
    label with a period, a label with no value, a clipped run of short
    sentences, a mirrored pair, mirrored bullets, a chained pair, a one-word
    definition, a setup sentence, a sentence about the document, litotes, and an
    abstract noun given a person's action. voice-check.py maps each form to the
    rule to apply.
    """
    found: list[tuple[int, str, str]] = []
    lines = text.splitlines()
    for number, line in enumerate(lines, 1):
        if LABEL_NONE_RE.match(line):
            found.append((number, "label with no value", " ".join(line.split())))
    checks = [(LITOTES_RE, "litotes"), (ABSTRACT_ACTOR_RE, "abstract noun as actor"), *PREDICTED_PATTERNS]
    for pattern, form in checks:
        for match in pattern.finditer(text):
            number = line_for_offset(text, match.start())
            found.append((number, form, " ".join(lines[number - 1].split())))
    # A bullet whose content words mostly repeat the heading above it tells the
    # reader nothing new, as in "Phase 1 moves the highest-risk jobs" under a slide
    # titled "The migration moves the highest-risk jobs first".
    heading_words: set[str] = set()
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        heading = HEADING_LINE_RE.match(stripped)
        if heading:
            heading_words = content_words(heading.group(1) or heading.group(2))
            continue
        item = LIST_ITEM_RE.match(line)
        if item and len(heading_words) >= 3:
            body = content_words(item.group(1))
            if body and len(body & heading_words) / len(body) >= 0.6:
                found.append((number, "bullet restates its heading", " ".join(stripped.split())))
        elif stripped and not item:
            heading_words = set()
    previous: tuple[list[str], bool] | None = None
    for number, line in enumerate(lines, 1):
        item = LIST_ITEM_RE.match(line)
        if not item:
            previous = None
            continue
        body = " ".join(item.group(1).split())
        words = WORD_RE.findall(body)
        plain = (len(sentences_in(body)) == 1 and body.endswith(".") and ":" not in body
                 and "**" not in body and 2 <= len(words) <= 10)
        if (plain and previous and previous[1] and words[0].lower() not in ("a", "an", "the")
                and [w.lower() for w in words[:2]] == [w.lower() for w in previous[0][:2]]):
            found.append((number, "mirrored bullets", body))
        previous = (words, plain)
    for number, line in enumerate(text.splitlines(), 1):
        heading = HEADING_RE.match(line.strip())
        if not heading:
            continue
        title = " ".join(heading.group(1).split())
        words = WORD_RE.findall(title)
        if 3 <= len(words) <= CLAIM_HEADING_LIMIT and words[0].lower() not in DESCRIPTIVE_OPENERS and (
            title.endswith(".") or CLAIM_VERB_RE.search(title)
        ):
            found.append((number, "heading written as a claim", title))

    for number, paragraph in prose_paragraphs(text):
        paragraph = " ".join(paragraph.split())
        sentences = sentences_in(paragraph)
        if (
            len(sentences) == 1
            and FRAGMENT_RE.match(paragraph)
            and len(WORD_RE.findall(paragraph)) >= 3
            and not re.search(r"[.!?:;)\"'`]$", paragraph)
            and not any(VERB_HINT_RE.match(word) for word in WORD_RE.findall(paragraph)[1:-1])
        ):
            found.append((number, "noun phrase with no verb", paragraph))
        reported_run = False
        for first, second in zip(sentences, sentences[1:]):
            a, b = WORD_RE.findall(first), WORD_RE.findall(second)
            if not a or not b:
                continue
            pair = f"{first} {second}"
            # One report per paragraph, because a run of five short sentences
            # needs one rewrite and not four findings.
            if not reported_run and len(a) <= SHORT_SENTENCE and len(b) <= SHORT_SENTENCE:
                found.append((number, "clipped run of short sentences", pair))
                reported_run = True
            opener = a[0].lower()
            if opener == b[0].lower() and opener not in MIRROR_EXEMPT and len(a) <= MIRROR_LIMIT and len(b) <= MIRROR_LIMIT:
                found.append((number, "mirrored pair", pair))
            last, lead = a[-1].lower().rstrip("s"), b[0].lower().rstrip("s")
            if last == lead and len(last) > 3:
                found.append((number, "chained pair", pair))
        for sentence in sentences:
            sentence = sentence.strip()
            words = WORD_RE.findall(sentence)
            if DEFINITION_RE.match(sentence):
                found.append((number, "one-word definition", sentence))
            if any(pattern.match(sentence) for pattern in SETUP_SENTENCE_RES):
                found.append((number, "setup sentence before the fact", sentence))
            if NARRATION_RE.match(sentence):
                found.append((number, "sentence about the document", sentence))
            if (
                len(words) >= 3
                and sentence.endswith(".")
                and PHRASE_OPENER_RE.match(sentence)
                and not re.search(r"'(?:s|re)$", words[0])
                and not any(VERB_HINT_RE.match(w) or IRREGULAR_VERB_RE.match(w) for w in words[1:])
            ):
                found.append((number, "label with a period", sentence))
    return found
