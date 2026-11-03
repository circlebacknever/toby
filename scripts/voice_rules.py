"""The voice rules, as code: the banned words, the patterns, and prose splitting.

validate-skills.py imports them to check the skills in this repo, and
score-voice.py imports them to score eval outputs.
"""
from __future__ import annotations

import re
from pathlib import Path

# The operating guide is in the base folder beside scripts.
REPO_ROOT = Path(__file__).resolve().parents[1]
BASE_TOBY = REPO_ROOT / "base" / "toby.md"


# The banned-word lists are in the operating guide under "## Banned Words" and are read
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
    """Read the hard-ban and sense-scoped tiers out of the operating guide.

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


# FOIL_PATTERNS matches a contrast whose rejected half follows a comma or a dash.
# It also matches "That's not X, it's Y" with any pronoun as the subject.
FOIL_PATTERNS = [
    (re.compile(r",\s+not\s+(?:a|an|the|just|only|because|to|for|from|in|on|by|per|with|at|as|under|over|without|through|across|between|after|before|its|his|her|their|my|your)\b"),
     "invented foil"),
    (re.compile(r"—\s*not\s"), "invented foil"),
    # "The fixture is built, not run." The rejected half is one word before the
    # end of the sentence.
    (re.compile(r",\s+not\s+[\w-]+\s*(?=[.;]|$)", re.M), "invented foil"),
    (re.compile(r"\b(?:it|that|this|which|they|these|those)(?:'s|'re| is| was| are| were) not\s+[^.,\n]{1,60},"
                r"\s*(?:it|that|this|they)(?:'s|'re| is| was| are| were)\b", re.I),
     "invented foil"),
]


# TIC_PATTERNS matches chat tics. Four forms are whole sentences that grade the
# user, announce the next sentence, or label the answer. The fifth is a tail
# that flags importance. They came from a lesson reply the user rejected on
# 2026-10-02, which opened "Very close. Two fixes, and both matter." Each one
# fails the Job test, because it gives no answer, reason, step, risk, or
# decision. Each form matches a whole sentence or a fixed tail, so "Almost. Two
# tables are left." passes.
# A sentence also starts after an opening quote, because skills quote the reply
# they want, as in `"Good. You write the guard."`, and an agent copies it.
SENTENCE_START = r"(?:^|(?<=[.!?]\s)|(?<=[.!?]\s\s)|(?<=\")|(?<=“))"
TIC_PATTERNS = [
    # "Good." and "Great!" praise the user and say nothing about the subject.
    # "Right." and "Correct." are left out, because each one can be the answer.
    (re.compile(SENTENCE_START + r"(?:Good|Great|Nice|Perfect|Excellent|Awesome|Wonderful|Lovely)"
                r"(?: (?:work|job|thinking|question|point|idea|catch|observation|call))?[.!]", re.M),
     "praise for the user"),
    (re.compile(SENTENCE_START + r"That(?:'s| is) a (?:great|good|excellent|fair) "
                r"(?:question|point|idea|catch|observation)[.!]", re.M),
     "praise for the user"),
    # "right — what happens when the input is empty?" grades the answer, then
    # welds the next clause on with a dash.
    (re.compile(SENTENCE_START + r"(?:[Rr]ight|[Cc]orrect|[Ee]xactly|[Yy]es|[Gg]ood|[Gg]reat|[Nn]ice)\s+—", re.M),
     "grade and a dash"),
    (re.compile(SENTENCE_START + r"(?:Very close|So close|Spot on|Bingo|(?:You )?[Nn]ailed it|"
                r"You(?:'ve| have)? got it|Good (?:instinct|intuition|eye|thinking)|"
                r"(?:Good|Nice|Great) catch|Right (?:idea|instinct|track)|"
                r"(?:Partly|Half|Mostly|Exactly) right|You(?:'re| are) (?:close|almost there|on the right track)|"
                r"Almost there|Close,? but not quite)[.!]", re.M),
     "grade on the user's attempt"),
    (re.compile(SENTENCE_START + r"(?:Here(?:'s| is) (?:why|how|the thing|the catch|the deal|the kicker|"
                r"the trick|the twist|what happens|what's going on|what's happening|"
                r"what I (?:found|changed|did|saw)|what we (?:found|changed|did|saw)|the idea|"
                r"a breakdown|the breakdown|a quick summary|the quick summary|the plan|the steps)|Let me explain|"
                r"Let me break (?:it|this|that) down|Think (?:about|of) it (?:this|like this) way|Consider this|"
                r"Put another way|To put it (?:simply|another way)|In other words|To be clear|"
                r"To recap|Key points|Main points|(?:a |the )?[Qq]uick summary)\s*[.:]", re.M),
     "sentence that announces the next one"),
    (re.compile(SENTENCE_START + r"(?:To recap|In short|Overall|All told|To sum up)\s*,", re.M),
     "sentence that announces the next one"),
    (re.compile(SENTENCE_START + r"(?:What this means is|The answer is|The point is|What matters is|"
                r"The bottom line is|The key is|The real (?:issue|problem|bug|cause|question) is)\b", re.M),
     "labelled answer"),
    (re.compile(SENTENCE_START + r"(?:This|That|It) is (?:a|the) classic\b", re.M),
     "stock phrasing"),
    (re.compile(SENTENCE_START + r"(?:Nice|Great|Good|Excellent) (?:work|job) (?:on|with)\b", re.M),
     "praise for the user"),
    # "The card named process narration" uses `named` for `described`. The verb
    # takes an actual name: a file named `config.yml`, or a named export.
    (re.compile(r"\b(?:names?|named|naming)\s+(?:the |this |that |these |those |its |their |your |our )?"
                r"(?:problem|problems|issue|issues|process|narration|behavior|behaviour|"
                r"cause|reason|risk|risks|change|changes|point|points|finding|findings|"
                r"failure|failures|gap|gaps)\b", re.I),
     "named for described"),
    # "Let me take a look at the handler." and "I'll start by reading the diff."
    # announce the writer's next action and hold the finding back. "I read the
    # diff and saw no new allocations" stays legal, because it reports a result.
    # "Let me know when the deploy finishes" stays legal too, because that asks
    # the user for something.
    (re.compile(SENTENCE_START + r"(?:Let me\s+(?:take a look|look|check|read|open|examine|review|walk|dig|"
                r"think|start|begin|explain|show|see|verify|confirm|run|search|find|inspect|analy[sz]e|help)|"
                r"Allow me to|I'm going to\s+(?:take a look|look|check|read|open|review|walk|start)|"
                r"I(?:'ve| have) (?:reviewed|taken a look at|gone through|looked through) (?:the|your)\b|"
                r"I'll go ahead|I'll take a look|I'll start by|First,? I'll|First,? let's|First things first|"
                r"Now,? let's|Alright,? let's|Okay,? let's|Let's get started|"
                r"Let's\s+(?:look|check|walk|go|start|begin|dive|dig|see|examine|review)|Note that)\b", re.M),
     "process preamble"),
    # "Remaining limit, stated plainly:" describes the next sentence instead of
    # stating it. The part after the comma is a meta word (an adverb or a
    # participle), not content, and a bare "Fix:" label has no comma and stays
    # legal, because a required format may ask for one.
    (re.compile(SENTENCE_START + r"[A-Z][\w'&/-]{1,30}(?: [\w'&/-]+){0,4}, (?:[a-z]+ ){0,2}"
                r"(?:plainly|simply|briefly|honestly|clearly|tersely|short|clear|stated|put|said|"
                r"written|noted|rephrased|reworded|summarized|recap)\s*:", re.M),
     "meta label"),
    (re.compile(SENTENCE_START + r"(?:The problem|The issue)\s*:", re.M),
     "labelled answer"),
    (re.compile(SENTENCE_START + r"(?:The good news is|The bad news is)\b", re.M),
     "labelled answer"),
    (re.compile(SENTENCE_START + r"(?:(?:The )?(?:[Ss]hort|[Ll]ong|[Qq]uick|[Ss]imple|[Dd]irect) (?:answer|version)|"
                r"(?:The )?[Bb]ottom line|In short|In a nutshell|Put simply|Simply put|"
                r"The gist|The upshot|The verdict|Spoiler)\s*:", re.M),
     "labelled answer"),
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:Your|The|My)\s+(?:[\w-]+\s+){0,2}[\w-]+,\s+"
                r"(?:repaired|corrected|rewritten|revised|tightened|cleaned up|reworded|improved|simplified)\s*:", re.M),
     "labelled answer"),
    (re.compile(r",\s+and\s+(?:both|all(?: three| four| of them)?|each(?: one)?)\s+"
                r"(?:matters?|counts?|(?:is|are) important)\b", re.I),
     "importance flag"),
    # "You're absolutely right!" and "Of course!" agree before checking.
    # "You're right." with no adverb passes, because it can be the answer.
    (re.compile(SENTENCE_START + r"(?:You(?:'re| are) (?:absolutely |totally |completely |so )right|"
                r"Of course|Certainly|Absolutely|Sure thing)[.!]", re.M),
     "agreement before checking"),
    # "Noted." and "Got it." acknowledge a correction and say nothing. The user
    # flagged "Noted" on 2026-10-08, so a reply opens with the change itself.
    (re.compile(SENTENCE_START + r"(?:Noted|Got it|Understood|Fair enough|Makes sense)[.!]", re.M),
     "stock acknowledgement"),
    # "I'm taking your message as approval" claims a decision the user didn't make.
    (re.compile(r"\b(?:I'm |I am |I'll )?(?:taking|take|treating|treat) (?:that|this|your (?:message|reply|answer|note)) as "
                r"(?:a yes|approval|a go|permission)\b", re.I),
     "taking a message as approval"),
    # "This relates to problem 2." points back to a label and adds nothing.
    (re.compile(SENTENCE_START + r"This (?:relates|maps|corresponds|ties|applies) to (?:problem|item|rule|step|group|criterion|finding)s? "
                r"\d+(?: and \d+)?\.", re.M),
     "tag sentence"),
    (re.compile(SENTENCE_START + r"(?:You(?:'re| are) asking (?:whether|if|how|why|what|about)|"
                r"You asked (?:whether|if|how|why|what|about)|"
                r"So you (?:want|need) to know|"
                r"Your question (?:was|is) (?:whether|if|how|why|what))\b", re.M),
     "restating the question"),
    # "I understand your frustration." and "That sounds frustrating." perform
    # sympathy and give the reader no fact or next step.
    (re.compile(SENTENCE_START + r"(?:I (?:understand|know) (?:your|this|that) (?:is |can be )?"
                r"(?:frustration|concern|situation)|"
                r"That (?:sounds|must be|is) (?:frustrating|annoying|tough|rough|hard)|"
                r"I'm sorry (?:to hear|you|that you)|"
                r"I apolog(?:ize|ise)|My apologies|"
                r"Sorry (?:about (?:that|the confusion)|for the confusion))", re.M),
     "performed empathy"),
]


# Editing leftovers that are wrong on every reading: a period alone at the
# start of a line, and a list number with no text. The repo review on
# 2026-10-02 found one of each in the skills. An unfilled `path:line` was found
# too, but eight skill lines use that phrase to name the citation format, so no
# pattern checks it.
MECHANICAL_PATTERNS = [
    (re.compile(r"^[ \t]*\.(?!\.)(?:[ \t]+\S|[ \t]*$)", re.M), "stray period at the start of a line"),
    (re.compile(r"^[ \t]*\d+\.[ \t]*$", re.M), "list number with no text"),
]


# Each form here matches a fixed phrase, so it doesn't flag correct replies.
REPLY_PATTERNS = FOIL_PATTERNS + TIC_PATTERNS + [
    (re.compile(r"\bnot just\b"), "invented foil"),
    (re.compile(r"\brather than\b"), "invented foil"),
    (re.compile(r",\s*though\.?\s*$", re.M), "trailing though"),
    (re.compile(r"\bthat said,", re.I), "that said"),
    # `carry` is legal only for moving an object or an arithmetic carry, and a
    # reply about code almost never means either one.
    (re.compile(r"\bcarr(?:y|ies|ied|ying)\b", re.I), "carry as a metaphor"),
    (re.compile(r"\b(?:hope this helps|feel free|let me know if|don't hesitate)\b", re.I),
     "closing offer"),
    (re.compile(r"\b(?:[Dd]oes (?:that|this) make sense|(?:I'd be |I'm )?[Hh]appy to (?:help|walk|show|explain|dig|go|answer|talk|look|share)|[Gg]lad I could help)\b"),
     "closing offer"),
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
    # A compressed copy of the guide that one eval arm loads in place of it.
    REPO_ROOT / "evals" / "arms" / "core.md",
}


FENCE_RE = re.compile(r"^```.*?^```", re.M | re.S)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
TABLE_ROW_RE = re.compile(r"^\|.*$", re.M)


# A blockquote is quoted material, which the Banned Words exemption covers. The
# worked examples quote bad copy on purpose so the reader can see it.
BLOCKQUOTE_RE = re.compile(r"^>.*$", re.M)


# A double-quoted span is a quote too, and the same exemption covers it, so
# quoting a user's sentence never fails the scan.
DOUBLE_QUOTE_RE = re.compile(r'"[^"\n]{1,300}"|“[^”\n]{1,300}”')


# A footnote definition is a citation, and cited titles are exempt. Its
# indented continuation lines belong to the same footnote.
FOOTNOTE_RE = re.compile(r"^\[\^[^\]]+\]:.*(?:\n[ \t]+\S.*)*", re.M)


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

    for pattern in (FRONTMATTER_RE, FENCE_RE, FOOTNOTE_RE, INLINE_CODE_RE, TABLE_ROW_RE, BLOCKQUOTE_RE,
                    DOUBLE_QUOTE_RE, EMPHASIS_RE):
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
    "wears a", "dressed as", "dressed up as", "in disguise",
    "masquerading as", "pretending to be", "with a new hat", "with a hat on",
    "under the hood", "in a trench coat", "puts on a", "wrapped in a costume",
    # From the repo review on 2026-10-02: "five runs took back" a result, "it
    # moved nothing", a check a metaphor "walks past", and a stranger "wearing"
    # Toby's clothes.
    "wearing", "took back", "moved nothing", "walks past", "walk past", "handed straight back",
    "without being buried", "death by a thousand cuts", "death-by-a-thousand-cuts",
    # Verbs of place and motion used for code, rules, and findings. A rule is in
    # a file, and a finding depends on the diff. The eval writers and this repo
    # both wrote each of these, and the reader stopped on every one.
    "lives in", "lives at", "lives on", "lives inside", "lives next to", "living in",
    "live inside", "sits in", "sits on", "sits at", "sits above", "sits below",
    "sits outside", "sits inside", "sits next to", "sits beside", "sitting in",
    "sit in", "sit on", "sit at", "sit inside", "sit outside", "sit next to",
    "sitting outside", "land", "lands", "landed", "landing in", "land on", "not land",
    "falls through", "fall through", "rests on", "rest on", "feeds", "fed into",
    "glides over", "bites hardest", "racks up interest", "embarrass", "embarrasses", "embarrassed",
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


# Habits predicted from what this reader has rejected so far. None of them is
# in the skills today, and agents write all of them, so each hit is a question.
PREDICTED_PATTERNS = [
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:The (?:result|catch|fix|problem|answer|twist|upshot|kicker|good news|bad news|reason)|Why does (?:this|that|it) matter|So what does (?:this|that) mean|What does (?:this|that) mean|The short version|(?:And )?[Ww]hy|How)\?", re.M),
     "setup question"),
    # "Almost." and "Exactly." grade the user's attempt before the answer. Each
    # one is also a correct reply to "is it done?", so a person decides.
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:Close|Almost|Nearly|Not quite|Exactly|Precisely|Sort of|Kind of|Partially)[.!]", re.M),
     "grade before the answer"),
    # "One honest caveat:" and "Three things to know:" give a count and hold the
    # items back. "One thing is clear:" passes, because the noun phrase is
    # followed by a verb, not a colon.
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:One|Two|Three|Four|Five|A few|A couple of|Several|\d+)\s+(?:[a-z-]+\s+)?"
                r"(?:fix(?:es)?|corrections?|things?|issues?|problems?|points?|caveats?|catch(?:es)?|notes?|differences?|"
                r"reasons?|tweaks?|mistakes?|gaps?|ideas?|parts?|pieces?|changes?)(?:\s+to\s+(?:know|fix|note|check))?"
                r"(?:\s+here)?(?:[.:](?=\s|$)|,\s+and\s+(?:both|all|each)\b)", re.M),
     "count before the items"),
    # "The theorem would be worthless" and "every system on Earth" add drama to a
    # claim that needs none. The guide bans dramatic words used for emphasis.
    # "The worst time to find them" comes from the repo review on 2026-10-02.
    # `worst-case` is a term, so it passes.
    (re.compile(r"\b(?:worthless|pointless|catastroph\w+|damning|dire|disastrous|devastating|"
                r"theater|on Earth|in the world|of all time|lives or dies|make or break|"
                r"worst(?![- ]case)|pure (?:complexity|overhead|waste)|"
                r"everything (?:hinges|rests|depends) on)\b", re.I),
     "dramatic word"),
    # "Widening the set is the whole job" and "The entire rule is". The form
    # needs the copula, because "a retry runs the whole job again" is literal.
    (re.compile(r"\b(?:is|are|was) the (?:whole|entire) (?:point|game|trick|story|job|rule|test|idea|purpose|fix)\b|"
                r"(?:^|(?<=[.!?]\s))(?:The|Its|Their) (?:whole|entire) (?:point|rule|test|idea|trick|job) is\b", re.I | re.M),
     "dramatic word"),
    # "The bitmaps are what exhaust memory" says "The bitmaps exhaust memory"
    # with extra words. A noun clause such as "what the field holds" passes,
    # because a determiner or pronoun follows `what`.
    (re.compile(r"\b(?:is|was|are|were|that's|that is) what (?!(?:the|a|an|it|its|they|their|you|your|we|our|"
                r"I|my|this|that|these|those|he|she|his|her|people|users?|callers?)\b)[a-z]+", re.I),
     "cleft for emphasis"),
    # "Per-call-site retry logic is where this design goes wrong."
    (re.compile(r"\b(?:is|are|was|were) where\b[^.:;]{0,80}?\b(?:happens?|goes wrong|go wrong|breaks?|fails?|starts?)\b", re.I),
     "cleft for emphasis"),
    # "This is the tool to run" and "is the one who can tell" put a filler noun
    # between the subject and the verb that does the work.
    (re.compile(r"\b(?:is|are) the (?:one|ones|thing|step|tool|part|error|piece|place|complexity|person) "
                r"(?:who|that|to|the)\b", re.I),
     "cleft for emphasis"),
    # ", which is why writers use these tests" and "That last one is why".
    (re.compile(r"\b(?:which|that|this|one) is why\b", re.I), "cleft for emphasis"),
    # "Performance work has three layers." and "The voice rules ship three
    # ways" give a count of a vague noun and hold the items back. A count
    # followed by a colon passes, because its list follows at once, and the
    # repo review could not tell those apart from cited counts by pattern.
    (re.compile(r"\b(?:two|three|four|five|six|seven|eight|nine|ten)\s+(?:[a-z-]+\s+)?(?:things|ways|problems|"
                r"categories|layers|mechanisms)\b(?![^.:\n]*:)", re.I),
     "count before the items"),
    (re.compile(r"\b(?:has|have|checks|runs?)\s+(?:two|three|four|five|six)\s+(?:more\s+)?(?:[a-z-]+\s+){0,2}"
                r"(?:things|lines|forms|verbs|tests|choices|rules|limits|steps)\s*:"
                r"|(?:^|(?<=[.!?]\s))(?:\*\*)?(?:Two|Three|Four|Five)\s+(?:[a-z-]+\s+){0,2}"
                r"(?:things|limits|choices|changes)\s+(?:your\b|apply\b|prevent\b)"
                r"|\bin\s+(?:two|three|four)\s+forms\."
                r"|\bthere are (?:two|three|four),", re.I | re.M),
     "count before the items"),
    # "This file adds two sections, and both always appear:" flags the count.
    (re.compile(r"\band (?:both|all (?:three|four|five)|each) (?:always )?(?:appear|apply|matter|count)\b", re.I),
     "importance flag"),
    # "Descriptions are all a host tool sees" and "the checker cannot see"
    # give a program a person's senses.
    (re.compile(r"\b(?:checker|script|linter|hook|tool|compiler|regex|patterns?)\s+(?:(?:cannot|can't|does not|"
                r"doesn't|never|can)\s+)?(?:sees?|notices?|knows?|wants?|decides?)\b", re.I),
     "code given senses"),
    # "Consider this service code:" announces the code and says nothing about it.
    (re.compile(r"(?:^|(?<=[.!?]\s))Consider (?:this|the following)\b[^.:]{1,40}:", re.M),
     "sentence that announces the next one"),
    # "The guardrail question" names a step of toby-swd-interfaces with a word
    # its SKILL.md never uses. Twelve skill lines used it on 2026-10-02.
    (re.compile(r"\bguardrails?\b", re.I), "coined name"),
    # "The number that matters" flags importance without stating it.
    (re.compile(r"\bthe (?:number|thing|part|metric|question) that (?:matters|counts)\b", re.I), "importance flag"),
    # "is either plainly right (...)." keeps half of an either-or pair.
    (re.compile(r"\b(?:is|are|was|were|be)\s+either\b(?![^.!?]*\bor\b)", re.I), "either with no or"),
    # "Bound orbits are ellipses, and everything else about them is detail."
    (re.compile(r"\b(?:everything else|the rest)\b[^.]{0,20}\bis (?:detail|noise|commentary|history)\b", re.I),
     "punchline closer"),
    # "Where the writing rules sit" places a rule as if it had a seat.
    (re.compile(r"\bwhere\b[^.,]{1,30}?\b(?:should |would |now )?(?:sits?|lives?)\b(?!\s+(?:in|on|at|inside|next))", re.I),
     "picture word"),
    # Fragments that open a note: "Frozen on 2026-09-14 before any writer ran.",
    # "Same diff, same criteria.", and "Not context, not a restatement."
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:Frozen|Scored|Recorded|Answered|Taken|Graded|Measured)\s+"
                r"(?:on|by|in|from|before|after|twice|at|with)\b", re.M),
     "fragment"),
    (re.compile(r"(?:^|(?<=[.!?]\s))Same\s+[\w-]+(?:\s+[\w-]+)?,", re.M), "fragment"),
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:Not|No)\s+[^,.!?]{1,40},\s+(?:not|no)\b", re.M), "fragment"),
    # "an optimization has is worth its cost" keeps two verbs from two drafts.
    (re.compile(r"\b(?:an?|the)\s+[\w-]+\s+has\s+is\b|\bhave\s+are\b", re.I), "doubled verb"),
    # "The rule is the system itself" stresses a noun that needs no stress.
    (re.compile(r"\bthe\s+[a-z][\w-]*\s+itself\b", re.I),
     "reflexive for emphasis"),
    # "Rule C tests this: the spin" and "the one that matters:" hold the noun
    # back past a colon. The noun has to follow on the same line, because "like
    # this:" before a code block or a list is how the docs introduce an example.
    (re.compile(r"\b(?<!like )(?:(?:exactly|precisely)\s+)?(?:this|that)\s*:[ \t]+\S|"
                r"\bthe (?:one|part|bit|thing|piece|question|step|rule|line) that (?:matters|counts)\s*:|"
                r"\bwhat matters\s*:", re.I),
     "deferred antecedent"),
    # "That's the whole trick." ends a reply on a punchline.
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:And )?(?:That's|That is|This is|Which is) "
                r"(?:it|the (?:whole|entire) [\w-]+|the (?:point|trick|idea|secret|magic)|all there is(?: to it)?)\.", re.M),
     "punchline closer"),
    (re.compile(r"\b(?:provides? the ability to|enables? the creation of|the implementation of|facilitates?|utilization|in terms of|with regard to|with respect to)\b", re.I),
     "noun doing a verb's job"),
    (re.compile(r"\b(?:the ask(?![-a-z])|bandwidth|action items?|learnings|net-new|quick win|big lift|touch base|level set|align on|alignment on|double down)\b", re.I),
     "meeting jargon"),
    (re.compile(r"\b(?:not only\b[^.]{0,60}\bbut also|less \w+, more \w+)\b", re.I), "rhythm device"),
    (re.compile(r"\b(?:super|incredibly|extremely|hugely|massively|insanely|ridiculously)\s+\w+", re.I), "vague intensifier"),
    # "tests exactly that surface" says the same as "tests that surface".
    (re.compile(r"\b(?:exactly|precisely)\s+(?:that|this|the|what)\b", re.I), "vague intensifier"),
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
    # "check that." and "keep that true" leave the reader to work out what `that` is.
    (re.compile(r"\b(?:keeps?|makes?|leaves?|checks?|shows?|proves?|covers?|handles?|fixes?|says?|does)\s+that"
                r"\s*(?:[.,;!?]|$|true\b|false\b|so\b|right\b|work\b|clear\b)", re.I | re.M),
     "bare `that` as an object"),
    # "A failed demo has one trace to open, and that is the property that makes it
    # checkable." The clause after the comma restates the claim before it.
    (re.compile(r",\s+and\s+(?:that|this|it)\s+is\s+(?:the|what|why|how|where)\b", re.I),
     "rider after a complete claim"),
    # "actual output" and "a named audit". The noun has no other kind, so the
    # adjective adds nothing. `true` and `existing` are left out, because "true
    # positive" and "the existing tests" each name a distinction.
    # `real` and `specific` are left out too. "A real caller" beside a
    # hypothetical caller draws a distinction, and a pattern cannot tell that use
    # from an empty one.
    (re.compile(r"\b(?:the|a|an|your|my|our|its|their|this|that|each|every|\w+'s)\s+(?:actual|named|given)\s+"
                r"(?!time\b|number\b)[a-z][\w-]*", re.I),
     "empty qualifier"),
    # "With the code shown, this test fails." The phrase frames the evidence
    # before the claim.
    (re.compile(r"(?:^|(?<=[.!?]\s))(?:With the (?:code|context|information|files?|evidence|output) "
                r"(?:shown|given|provided|available)|From what (?:is|I can see|I see|was) (?:here|shown)|"
                r"Based on (?:the|what|this|my)|Looking at (?:the|this)|Given the (?:code|context|evidence|output))\b", re.M),
     "opening phrase that frames the evidence"),
    # "The index uses disk space in exchange." The sentence never says for what.
    (re.compile(r"\bin (?:exchange|return)\b(?! for\b)", re.I), "relation word with its other half missing"),
    # "no purge removes it" hides the thing that acts.
    # The verb needs an object after it, because "no API calls" is a noun phrase.
    (re.compile(r"\bno\s+(?!longer\b|matter\b|more\b|less\b)[a-z][\w-]*\s+(?:removes|deletes|reads|writes|calls|"
                r"checks|catches|imports|uses|changes|touches|sees|runs|clears|updates|returns|names|"
                r"fires|sets|stores|owns)\s+(?:it|them|the|a|an|this|that|these|those|any|its|their)\b", re.I),
     "negated actor"),
    # "Text holds only what no widget shows better." The form above needs an
    # object, so it missed this one. After a clause word, "no" plus a noun and
    # a verb is the actor of that clause, as in "hosts that no team owns".
    (re.compile(r"\b(?:what|that|which|who|where|when|while|unless|until|than|if|because|since)\s+no\s+"
                r"(?!longer\b|matter\b|more\b|less\b|doubt\b)[a-z][\w-]*\s+"
                r"(?:can(?:not|'t)?|could|will|would|should|must|may|might|does|did|has|had|is|was|"
                r"[a-z]{2,}(?:s|ed))\b", re.I),
     "negated actor"),
    # "Nothing calls `UserHandler`" makes a negative pronoun the actor, the same
    # problem as "no purge removes it". The retest on 2026-10-12 found it in 5
    # of 10 notes.
    (re.compile(r"(?:^|(?<=[.!?]\s)|(?<=^- )|\b(?:what|that|which|where|when|while|unless|until|if|because|since|so|and|but)\s+)"
                r"(?:Nothing|Nobody|No one)\s+(?:else\s+)?(?:(?:in|on|from|outside|inside)\s+(?:the\s+|this\s+)?[\w-]+\s+)?(?:can(?:not|'t)?|could|will|would|should|does|did|"
                r"[a-z]{2,}(?:s|ed))\b", re.I | re.M),
     "negated actor"),
    (re.compile(r"\b(?:Nothing|Nobody|No one)\s+(?:from\s+[^.\n]{1,40}\s+)?(?:is|was|are|were|has|had)\s+[a-z]+(?:ed|en)\b"
                r"|\bNone of the\s+[a-z][\w-]*\s+(?:is|are|was|were|has|have|had|can|will|does|did|[a-z]{2,}(?:s|ed))\b"
                r"|\b[A-Za-z][\w-]*\s+nothing\s+[a-z]{2,}s\b"
                r"|\b(?:so|and|but)\s+no\s+(?:other\s+)?[a-z][\w-]*(?:\s+(?:in|on|outside|inside)\s+(?:the\s+|this\s+)?[a-z][\w-]*)?\s+"
                r"(?:depends|uses|calls|reads|writes|touches|reaches)\b", re.I),
     "negated actor"),
    # "Text holds the answer" and "The line holds the event name" give text a
    # container verb. A database table holds rows, so "table" is left out.
    (re.compile(r"\b(?:text|sentence|paragraph|reply|message|doc|document|page|section|heading|list|"
                r"comment|prose|copy|line|bullet|title|caption|answer|summary)s?\s+(?:holds?|held)\b", re.I),
     "container verb"),
    # "`tests/orders/` has no test for `cancelOrder`" puts the negation on the
    # noun. The user wants "doesn't have a test", which puts it on the verb.
    (re.compile(r"\b(?:has|have|had|find|finds|found|need|needs|needed|get|gets|got|see|sees|saw|"
                r"return|returns|returned|give|gives|gave|take|takes|took|make|makes|made|show|shows|"
                r"contain|contains|hold|holds|carry|carries|run|runs|ran|leave|leaves|left|"
                r"with|touches|takes|writes|proves|owns|says|does)\s+(?-i:no)\s+"
                r"(?!longer\b|more\b|less\b|matter\b|later\b|sooner\b|other\b|one\b|doubt\b)[a-z]"
                r"|\b(?:writes|proves|owns|says|does|means|adds|changes|fixes|solves|explains|checks|tests|covers)\s+nothing\b", re.I),
     "negation on a noun"),
    # "The repo does not have a rate limiter" reads stiff. The user asked on
    # 2026-10-12 for negations written the way people say them, as "doesn't".
    (re.compile(r"\b(?:does|do|did|is|are|was|were|has|have|had|could|would|should|will)\s+not\b(?!\s+NULL\b)|\bcannot\b", re.I),
     "uncontracted negation"),
    # "only what no widget shows" limits one clause twice.
    (re.compile(r"\bonly\s+(?:what|whatever|when|where|the\s+[\w-]+\s+(?:that|which))\s+"
                r"(?:no|nothing|none|nobody)\b", re.I),
     "double negation"),
    # "uses text only where a chart wouldn't show the data better" limits the
    # clause with "only" and negates its verb too. The retest found it in 9 of 10 notes.
    # "Load it only when the guide is not loaded" reads fine, so the form needs a
    # comparison after the negation, as in "wouldn't show the data better".
    (re.compile(r"\bonly\s+(?:what|whatever|when|where|if)\s+(?!no\b|nothing\b|none\b|nobody\b)[^.;:\n]{0,40}?(?:n't|\bnot\b|\bnever\b|\bno\b)"
                r"[^.;:\n]{0,40}?\b(?:better|worse|more|less|faster|slower|clearer|differently)\b", re.I),
     "double negation"),
    # A phrase such as "no longer" or a decision with its date records
    # history. A doc or plan states what is true now.
    (re.compile(r"\b(?:no longer|was removed|were removed|has been removed|decided against|used to be|previously|formerly)\b"
                r"|\b(?:decided|chose|agreed)\b[^.\n]{0,40}\b\d{4}-\d{2}-\d{2}\b", re.I),
     "history in a file"),
    # "I won't propose a fix in this reply" talks about the reply in place of
    # giving its content.
    (re.compile(r"\bin (?:this|my) (?:reply|message|answer|response)\b|\bmy replies here\b", re.I),
     "sentence about the reply"),
    # "You're right, and I had the cause wrong" is a stock admission. The
    # corrected fact is the useful part.
    (re.compile(r"\b(?:you'?re|you are) right,? and I\b|\bI had the cause wrong\b|\bI misread (?:you|your)\b", re.I),
     "stock admission"),
    # "That rule produces the same chopping" gives a rule a person's action.
    (re.compile(r"\b(?:the|that|this|each|a)\s+(?:[\w-]+\s+)?(?:rule|choice|decision|constraint|ban|plan|suite|skill|column|catalog)s?\s+"
                r"(?:produces?|decides?|wants?|pushes|forces?|insists?|cares?|says|trained|lists|owns|ships)\b"
                r"|\bwords\s+below\s+want\b"
                r"|\bforces\s+the\s+plan\s+to\b", re.I),
     "rule as the actor"),
    # "`checks.md:12` turns implied work into follow-ups" gives a file a
    # person's action. prose_only blanks the code span, so the sentence
    # starts with a run of spaces before the verb.
    (re.compile(r"(?:^|(?<=[.!?]\s)|(?<=^- ))\s{4,}(?:turns|decides|wants|owns|produces|forces|pushes|waits|knows|thinks|cares)\b", re.M),
     "file as the actor"),
    # "Want me to also check the logs?" ends on an offer. "Do you want me to
    # rebase instead?" can ask for a decision Toby needs, so a person decides.
    (re.compile(r"\b(?:[Ww]ant me to|[Ww]ould you like me to|[Ss]hould I also|[Ii]f you(?:'d)? like, I can|I can also)\b"),
     "closing offer"),
]


# Litotes denies the opposite of what the writer means: "not uncommon" is "common".
LITOTES_RE = re.compile(
    r"(?:\bnot|n't) (?:uncommon|unusual|unlike|unreasonable|unimportant|unhelpful|unknown|unfamiliar|"
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

REPLY_EXTRA_FORMS = {
    "opening phrase that frames the evidence",
    "relation word with its other half missing",
    "double negation",
    "sentence about the reply",
    "stock admission",
    "deferred antecedent",
    "punchline closer",
    "code given senses",
    "code given feelings",
    "sentence that announces the next one",
    "count before the items",
    "doubled verb",
    "either with no or",
    "hedge stack",
    "rhythm device",
    "closing offer",
    "vague intensifier",
}

REPLY_PATTERNS.extend([(p, "invented foil") for p in CONTRAST_PATTERNS])
REPLY_PATTERNS.extend(MECHANICAL_PATTERNS)
REPLY_PATTERNS.append((LITOTES_RE, "litotes"))
REPLY_PATTERNS.append((ABSTRACT_ACTOR_RE, "abstract noun as actor"))
REPLY_PATTERNS.extend([(p, f) for p, f in PREDICTED_PATTERNS if f in REPLY_EXTRA_FORMS])


