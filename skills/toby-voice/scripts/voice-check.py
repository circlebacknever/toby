#!/usr/bin/env python3
"""Find the voice breaks that patterns can find, then list the rules the patterns do not check.

Run this on a file, a directory, or stdin. Do not write your own grep for these
rules, because a fresh grep finds a different subset each time. The checker
prints each sentence at fault and the rule it breaks.

    scripts/voice-check.py draft.md
    scripts/voice-check.py draft.md --review
    pr-description | scripts/voice-check.py -

--review prints every prose sentence in order with its findings under it, after
the READ list. Use it for the sentence-by-sentence read the READ rules need.

On 2026-09-17, tests/test-voice-recall.py gave 17 of 49 bad gold sentences a
FIX finding and 25 more a DECIDE finding. The other 7 got no finding. Many of
the patterns were written from those sentences, and nobody has measured the
patterns on new text. So a run with no findings
means the patterns matched nothing, and the draft still needs the READ pass.

Output comes in three groups, because each one needs different handling.

FIX     A rule with no judgement in it. A banned word is banned. A dash welding
        two clauses is a weld. Do not argue with these, and do not call them
        false positives. Rewrite the sentence.

DECIDE  A rule a machine cannot settle. `shape` is banned when it only says something matters
        and fine as a noun for an actual shape. The check prints the sentence so
        you can answer for that sentence. Most of these are real. Read each one
        and say which it is, and never dismiss the group.

READ    The rules the patterns do not check. After you fix the findings, read every
        sentence of the draft against each rule in this list, and rewrite each
        sentence that fails. Every run prints this list, even a run with no
        findings.

Exit 1 when anything is in FIX. DECIDE and READ never fail the run.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple

# The rules are in voice_rules.py beside this file. The checker needs that file
# and the guide, and nothing else from the repo. The import writes no __pycache__,
# so a run leaves an installed skill folder unchanged.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import voice_rules as v  # noqa: E402

WELD_RE = re.compile(r"\w\s+—\s+\w|\w;\s+\w")
LABEL_DASH_RE = re.compile(r"^(?:[-*]\s+)?\**[A-Z][\w-]*(?:\s[\w-]+)?\**\s+—$")
BARE_PRONOUN_RE = re.compile(r"\b(This|That)\s+(is|was|means|makes|leaves|gets|costs|holds)\b")
CLOSING_OFFER_RE = re.compile(
    r"\b(hope this helps|let me know if|feel free|don'?t hesitate|happy to help|reach out)\b", re.I
)

# What to do about each slogan form, with the plain-language rule behind it.
SLOGAN_NOTES = {
    "heading written as a claim": "use a one- or two-word label, or a phrase saying what the section covers, rule 23",
    "noun phrase with no verb": "write a sentence that names the thing and says what it does, rule 22",
    "chained pair": "the second sentence restarts on the last word of the first, so join them, rule 24",
    "one-word definition": "say what the thing does, rule 24",
    "label with a period": "give it a subject and a verb, rule 29",
    "label with no value": "write a sentence that names what is missing and where you looked, rule 29",
    "setup sentence before the fact": "name the file, the cause, or the change in this sentence, rule 30",
    "sentence about the document": "delete it and give the content, rule 21",
    "litotes": "state it in positive form: not uncommon is common, rule 28",
    "abstract noun as actor": "name the person or program that acts, or describe the state, rule 27",
    "setup question": "delete the question and state the result, rule 30",
    "noun doing a verb's job": "use the verb: provides the ability to is can, rule 11",
    "meeting jargon": "say the plain thing: the ask is the request, rule 15",
    "rhythm device": "state the claim once, without the balanced frame, rule 24",
    "vague intensifier": "delete the intensifier, or give the number, rule 3",
    "code given feelings": "say what the tool printed or did, rule 27",
    "hedge stack": "keep one hedge and name the unknown, or none, rule 3",
    "would-have stated as fact": "delete it, even with a Prediction label, and state what the system does now, rule 31",
    "claim about the user": "say only what the user said or did, rule 31",
    "what a thing never does": "leave it out unless this document's reader would assume it, rule 25",
    "program given a judgment": "state the fact about the thing, such as providers are swappable, rule 27",
    "bullet restates its heading": "give the bullet a fact the heading does not state, or delete it, rule 23",
    "empty qualifier": "delete the adjective when the noun has no other kind, Banned Constructions",
    "opening phrase that frames the evidence": "delete the phrase and state the claim, Banned Constructions",
    "relation word with its other half missing": "say what the trade is for, or delete the relation word, Banned Constructions",
    "negated actor": "make the thing that acts the subject, as in `purgeable` does not return the row, Banned Constructions",
    "two facts joined by and": "check that both facts belong to one process, and write two sentences when they do not, rule 24",
    "bare `that` as an object": "say the noun after `that`, rule 9",
    "rider after a complete claim": "delete the clause, because the sentence before it already said this, Banned Constructions",
    "heading joins two clauses": "write a one- or two-word label, or a phrase that says what the section covers, rule 23",
    "grade before the answer": "delete the grade and open with the answer, unless the word is the answer, rule 30",
    "count before the items": "delete the count and give the items, rule 30",
    "dramatic word": "delete the word, or state the consequence in numbers, Banned Constructions",
    "cleft for emphasis": "drop `is what` and let the subject act: the rule forces, rule 24",
    "reflexive for emphasis": "delete `itself` unless it marks a contrast someone made, rule 3",
    "deferred antecedent": "put the noun where `this:` is, Banned Constructions",
    "punchline closer": "delete it, the reply ends at the last fact, rule 30",
    "code given senses": "say what the program reads or matches, rule 27",
    "sentence that announces the next one": "say what the reader should look for in the code, rule 32",
    "coined name": "use the name the source skill uses, such as the step number, rule 10",
    "importance flag": "delete the flag and state the fact, Banned Constructions",
    "picture word": "say where it is: is in, is loaded from, rule 26",
    "fragment": "give the sentence a subject and a verb, rule 29",
    "doubled verb": "delete one of the two verbs, rule 29",
    "intensifier with no contrast": "delete the word, or state the contrast it implies, Banned Constructions",
    "either with no or": "give the other half after `or`, or delete `either`, rule 29",
    "closing offer": "end at the last fact, and ask only for a decision you need, Five Tests 5",
}

# READ_RULES lists the rules that the patterns in voice_rules.py do not check, in the
# order the READ group prints them. Each entry ends with its rule number in
# references/plain-language.md, or with the guide section that states it.
# tests/test-voice-recall.py marks with `none` each gold sentence that the
# patterns miss.
READ_RULES = [
    "Each fact comes from the user, a file you read, or a command you ran, and it keeps its qualifier. (rules 31 and 32)",
    "Each sentence gives an answer, a reason, a step, a risk, or a decision. Delete a sentence that introduces, repeats, or reacts. (rule 32)",
    "The first sentence states the answer, each condition that changes it comes right after, and nothing follows the last fact. (rules 17 and 30)",
    "Each verb has its dictionary meaning, so code runs, reads, writes, calls, returns, or stores. Rewrite every metaphor. (rules 26 and 27)",
    "A reader could look up each word and find your meaning. Rewrite each coined term and each piece of jargon, and explain each internal label such as an eval id or a rule number. (rules 10, 13, 14, and 15)",
    "A sentence says what a thing is or does. Cut every contrast with something nobody said, whatever words it uses. (rules 25 and 28)",
    "Cut an adjective on a noun that has no other kind, such as actual output or a named audit. (Banned Constructions section)",
    "Every join between two clauses has a word that states the true relation, so `because` marks only a cause and `so` only a result. A colon only introduces a list of three or more items. (rules 7 and 24)",
    "A relation word has both halves, so `in exchange` says for what. Put `only` before a small number. (Banned Constructions section)",
    "Two facts joined by `and` belong to one process, or they become two sentences. In a negated sentence, make the thing that acts the subject. (Banned Constructions section)",
    "Put a noun after `this` and `that`, and open a sentence with a bare `It` only when one earlier noun could be its target. Give each thing one name from first mention to last. (rules 9 and 10)",
    "Name the actor when a passive hides who acted. (rule 6)",
    "Cut an opening phrase that frames the evidence, a method told before its finding, an aphorism, and a withheld answer. (Banned Constructions section)",
    "When the user must decide something, the first sentence asks, with at most three options and one recommended. (Replies section)",
    "Put each modifier next to the word it modifies. When a trailing phrase could attach to more than one verb, move it to the front. Give an opening phrase a subject. (rule 33)",
]


# Sense-scoped words whose legal meaning is narrower than "fine as a plain noun".
CARRY_NOTE = "legal only for moving an object or an arithmetic carry. Write contains, has, includes, or states, rule 26"
SENSE_NOTES = {word: CARRY_NOTE for word in ("carry", "carries", "carried", "carrying")}


def sentence_at(text: str, offset: int) -> str:
    """The sentence containing an offset, for showing the writer what to rewrite."""
    start = max(text.rfind(". ", 0, offset), text.rfind("\n", 0, offset)) + 1
    end = min(
        [x for x in (text.find(". ", offset), text.find("\n", offset)) if x != -1] or [len(text)]
    )
    return " ".join(text[start : end + 1].split())[:200]


def defines_the_rules(path: str) -> bool:
    """True for a file that states the banned words rather than obeying them.

    The operating guide lists every banned word, so scanning it for them returns 107
    findings and teaches the reader that the tool is noise. The validator has
    always known this; the checker did not, until it was pointed at the guide.
    """
    try:
        resolved = Path(path).resolve()
    except OSError:
        return False
    return resolved in {p.resolve() for p in v.VOICE_SCAN_EXEMPT if p.exists()}


class Finding(NamedTuple):
    """One finding, with the line it came from, so --review can place it."""

    source: str
    bucket: str
    line: int
    rule: str
    sentence: str
    note: str

    def text(self) -> str:
        return f"{self.source}:{self.line}  {self.rule}\n      {self.sentence}\n      -> {self.note}"


NUMBER_WORDS = {w: i for i, w in enumerate(
    "zero one two three four five six seven eight nine ten eleven twelve".split())}
SENTENCE_CLAIM_RE = re.compile(
    r"\b(?:comment|docstring|contract)\s+(?:has|is)\s+(" + "|".join(NUMBER_WORDS) + r"|\d+)\s+sentences?\b", re.I)
COMMENT_LINE_RE = re.compile(r"^\s*(?:/\*\*?|\*/?|//+|#+)\s?(.*)$")
CODE_SPAN_RE = re.compile(r"`[^`\n]+`")
BLOCKQUOTE_RUN_RE = re.compile(r"(?:^>.*(?:\n|$))+", re.M)


def comment_groups(block: str) -> list[str]:
    """Return the text of each run of comment lines or docstring in a code block."""
    groups: list[list[str]] = []
    current: list[str] = []
    in_doc = False
    for line in block.splitlines()[1:-1]:
        stripped = line.strip()
        quotes = stripped.count('"""')
        if in_doc or quotes:
            current.append(stripped.replace('"""', "").strip())
            in_doc = in_doc != (quotes % 2 == 1)
            continue
        match = COMMENT_LINE_RE.match(line)
        if match and not stripped.startswith("#!"):
            current.append(match.group(1).strip().rstrip("*/").strip())
        elif current:
            groups.append(current)
            current = []
    if current:
        groups.append(current)
    return [" ".join(part for part in group if part) for group in groups]


def sentence_count_findings(raw: str, label: str) -> list[Finding]:
    """Check "The comment has N sentences" against the code block above it.

    The repo review on 2026-10-02 found four of these claims wrong in one
    skill, and the count is a fact the checker can read off the page.
    """
    found = []
    # The comment is in a fenced code block or quoted in a blockquote. The
    # nearest one above the claim that holds a real comment is the one meant,
    # and a placeholder such as `// ...` does not count.
    sources = [(b.end(), comment_groups(b.group(0))) for b in v.FENCE_RE.finditer(raw)]
    sources += [(q.end(), [" ".join(line.lstrip("> ").strip() for line in q.group(0).splitlines())])
                for q in BLOCKQUOTE_RUN_RE.finditer(raw)]
    sources.sort()
    for match in SENTENCE_CLAIM_RE.finditer(v.prose_only(raw)):
        word = match.group(1).lower()
        claimed = NUMBER_WORDS.get(word, int(word) if word.isdigit() else -1)
        counts = []
        for end, groups in reversed([s for s in sources if s[0] <= match.start()]):
            counts = [len(v.sentences_in(g)) for g in groups if len(v.WORD_RE.findall(g)) >= 3]
            if counts:
                break
        if counts and claimed not in counts:
            line = v.line_for_offset(raw, match.start())
            found.append(Finding(label, "decide", line, "sentence count does not match the comment",
                                 sentence_at(v.prose_only(raw), match.start()),
                                 f"the comment above has {' or '.join(map(str, sorted(set(counts))))} sentences, "
                                 "so correct the number, rule 31"))
    return found


def code_only_findings(written: str, label: str) -> list[Finding]:
    """Flag a sentence that is only code spans, such as "`a.md` and `b.md`."."""
    found = []
    # Read joined paragraphs, because a wrapped line such as "`userId`." is
    # the end of a sentence that started on the line above.
    for number, paragraph in v.prose_paragraphs(written):
        for sentence in v.sentences_in(paragraph):
            if not sentence.endswith(".") or not CODE_SPAN_RE.search(sentence):
                continue
            rest = CODE_SPAN_RE.sub(" ", sentence)
            if not [w for w in v.WORD_RE.findall(rest) if w.lower() not in ("and", "or")]:
                found.append(Finding(label, "decide", number, "fragment", sentence[:200],
                                     "give the sentence a subject and a verb, rule 29"))
    return found


# A term such as "the outcome laws" or "the one-decision loop" in a reference
# file names something the skill never defines. The reader of the reference
# came from SKILL.md and has to guess what it means.
# The head nouns are the ones the review found coined. "case" and "problem"
# were tried and dropped, because "the deep-link case" describes rather than names.
TERM_RE = re.compile(r"\bthe\s+((?:[a-z]+-)+[a-z]+\s+(?:loop|laws?|ladder|smell|principle)|"
                     r"[a-z]+\s+(?:laws|ladder|smell))\b", re.I)


def undefined_term_findings(text: str, label: str) -> list[Finding]:
    """Flag a named concept that its skill's SKILL.md and other files never use."""
    path = Path(label).resolve()
    if path.parent.name != "references" or not (path.parent.parent / "SKILL.md").exists():
        return []
    skill = path.parent.parent
    others = " ".join(p.read_text().lower() for p in skill.rglob("*.md") if p.resolve() != path)
    others = " ".join(others.replace("-", " ").split())
    found = []
    for match in TERM_RE.finditer(text):
        term = " ".join(match.group(1).lower().replace("-", " ").split())
        if term not in others:
            found.append(Finding(label, "decide", v.line_for_offset(text, match.start()),
                                 f"term the skill never defines {match.group(1)!r}",
                                 sentence_at(text, match.start()),
                                 "use the name SKILL.md uses, or define the term where it first appears, rule 10"))
    return found


def findings(raw: str, label: str, defining: bool = False) -> list[Finding]:
    text = v.prose_only(raw)
    tiers = v.load_banned_words()
    fix: list[Finding] = []
    decide: list[Finding] = []

    def add(bucket, rule, offset, note):
        line = v.line_for_offset(text, offset)
        name = "fix" if bucket is fix else "decide"
        bucket.append(Finding(label, name, line, rule, sentence_at(text, offset), note))

    if not defining:
        for word in tiers["hard"]:
            for m in re.finditer(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", text, re.I):
                add(fix, f"banned word {m.group(0)!r}", m.start(), "cut it, or rewrite the sentence around it")
        # One foil finding per line, because the older CONTRAST_PATTERNS and
        # FOIL_PATTERNS both match a sentence such as "a real tension, not a free
        # addition", and it needs one rewrite.
        foil_lines: set[int] = set()
        foils = [(p, "invented foil") for p in v.CONTRAST_PATTERNS] + [(p, r) for p, r in v.FOIL_PATTERNS]
        for pattern, rule in foils:
            for m in pattern.finditer(text):
                line = v.line_for_offset(text, m.start())
                if line not in foil_lines:
                    foil_lines.add(line)
                    add(fix, f"{rule} {m.group(0).strip()!r}", m.start(), "state the thing directly, rule 25")
        for term, pattern in v.COINED_RE:
            for m in pattern.finditer(text):
                add(fix, f"coined term {m.group(0)!r}", m.start(), f"{v.COINED_TERMS[term]}, rule 14")
        for frame, pattern in v.FIGURATIVE_RE:
            for m in pattern.finditer(text):
                add(fix, f"figurative frame {m.group(0)!r}", m.start(), "say what the thing is, no metaphor")
        for m in CLOSING_OFFER_RE.finditer(text):
            add(fix, f"closing offer {m.group(0)!r}", m.start(), "delete it, the reply ends at the answer")
        for pattern, reason in v.TIC_PATTERNS:
            for m in pattern.finditer(text):
                add(fix, f"chat tic {m.group(0).strip()!r}", m.start(), f"{reason}, rule 32")
        # The mechanical checks read the line as written. prose_only blanks
        # inline code, which would make "`a.json`. Set" look like a stray period.
        written = raw
        for block in (v.FRONTMATTER_RE, v.FENCE_RE):
            written = block.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), written)
        for pattern, reason in v.MECHANICAL_PATTERNS:
            for m in pattern.finditer(written):
                add(fix, reason, m.start(), "repair the line, it is wrong on every reading")
        decide.extend(code_only_findings(written, label))
        decide.extend(sentence_count_findings(raw, label))
        decide.extend(undefined_term_findings(text, label))
    for m in WELD_RE.finditer(text):
        # A dash after a one- or two-word label at the start of a sentence, as in
        # "Source — the user said", separates a field name from its value.
        before = text[max(text.rfind("\n", 0, m.start()), text.rfind(". ", 0, m.start())) + 1 : m.start() + 1]
        if LABEL_DASH_RE.match(before.strip() + " —") and "—" in m.group(0):
            continue
        # A list item is checked for semicolons only. The skills write bullets as
        # "label — description" on purpose, and a dash there separates a label.
        line_text = text[text.rfind("\n", 0, m.start()) + 1 : text.find("\n", m.start())]
        # A weld inside double quotes is a quoted example, and the rules exempt quotes.
        line_start = text.rfind("\n", 0, m.start()) + 1
        if text.count('"', line_start, m.start()) % 2 == 1:
            continue
        if v.is_prose_line(line_text) or (v.LIST_ITEM_RE.match(line_text) and ";" in m.group(0)):
            add(fix, "clause weld", m.start(), "name the relation: because, so, after, rule 7")

    if not defining:
        for word in tiers["sense"]:
            for m in re.finditer(rf"(?<![A-Za-z]){re.escape(word)}(?![A-Za-z])", text, re.I):
                note = SENSE_NOTES.get(m.group(0).lower(),
                                       "banned when it only says something matters, fine as a plain noun. Which is it here?")
                add(decide, f"sense-scoped {m.group(0)!r}", m.start(), note)
    for m in v.INTENSIFIER_RE.finditer(text):
        sentence = sentence_at(text, m.start())
        if not v.CONTRAST_RE.search(sentence):
            decide.append(Finding(label, "decide", v.line_for_offset(text, m.start()), "intensifier with no contrast",
                                  sentence, SLOGAN_NOTES["intensifier with no contrast"]))
    for m in BARE_PRONOUN_RE.finditer(text):
        add(decide, f"bare {m.group(1).lower()!r}", m.start(),
            "say the noun after it unless the reference is unmistakable, rule 9")
    for number, form, excerpt in v.slogan_findings(text):
        # The guide lists the dramatic words to ban them, like the banned words.
        if defining and form == "dramatic word":
            continue
        decide.append(Finding(label, "decide", number, form, excerpt[:200], SLOGAN_NOTES[form]))

    for number, line in enumerate(text.splitlines(), 1):
        if not v.is_prose_line(line):
            continue
        for sentence in v.sentences_in(line.strip()):
            count = len(sentence.split())
            trimmed = " ".join(sentence.split())[:200]
            if count > 35:
                fix.append(Finding(label, "fix", number, f"sentence runs {count} words", trimmed,
                                   "cut a clause, or split it into two sentences that each state their own subject. The ceiling is 25, rule 1"))
            elif count > 25:
                decide.append(Finding(label, "decide", number, f"sentence runs {count} words", trimmed,
                                      "over the 25 ceiling. Cut a clause, or say why it earns the length"))
    return fix + decide


def print_read_list() -> None:
    print(f"READ  ({len(READ_RULES)}) — the patterns do not check these rules. "
          "Read every sentence against each one.\n")
    for number, rule in enumerate(READ_RULES, 1):
        print(f"  {number:>2}. {rule}")
    print()


def review(sources: list[tuple[str, str]], found: list[Finding]) -> None:
    """Print every prose sentence in order, with its findings under it.

    The FIX and DECIDE groups show the sentences a pattern matched. This mode
    shows all of them, because rules 1 to 15 in the READ list need a person to
    read each sentence and answer for it.
    """
    print_read_list()
    print("REVIEW — read each sentence below against those 15 rules, and rewrite each one that fails.\n")
    by_line: dict[tuple[str, int], list[Finding]] = {}
    for finding in found:
        by_line.setdefault((finding.source, finding.line), []).append(finding)
    for label, raw in sources:
        text = v.prose_only(raw)
        count = 0
        for number, line in enumerate(text.splitlines(), 1):
            item = v.LIST_ITEM_RE.match(line)
            heading = v.HEADING_RE.match(line.strip())
            body = item.group(1) if item else (heading.group(1) if heading else line.strip())
            # Headings are read too, because rule 23 applies to them.
            if not body or not (v.is_prose_line(line) or item or heading):
                continue
            for sentence in v.sentences_in(body):
                count += 1
                print(f"  {label}:{number}  {count:>3}. {' '.join(sentence.split())[:300]}")
            for finding in by_line.pop((label, number), []):
                print(f"        {finding.bucket.upper()}  {finding.rule} -> {finding.note}")
        print()


def targets(args: list[str]) -> list[tuple[str, str]]:
    if args == ["-"]:
        return [("stdin", sys.stdin.read())]
    out = []
    for arg in args:
        path = Path(arg)
        if path.is_dir():
            out.extend((str(p), p.read_text()) for p in sorted(path.rglob("*.md")))
        else:
            out.append((str(path), path.read_text()))
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("paths", nargs="+", help="files, directories, or - for stdin")
    parser.add_argument("--fix-only", action="store_true", help="print the FIX group and nothing else")
    parser.add_argument("--no-read", action="store_true",
                        help="print FIX and DECIDE, and leave out the READ list")
    parser.add_argument("--review", action="store_true",
                        help="print every prose sentence with its findings under it")
    args = parser.parse_args()

    sources = targets(args.paths)
    found: list[Finding] = []
    for label, raw in sources:
        defining = defines_the_rules(label)
        if defining:
            print(f"note: {label} states the banned words, so word checks are off for it.\n")
        found.extend(findings(raw, label, defining))

    all_fix = [f for f in found if f.bucket == "fix"]
    all_decide = [f for f in found if f.bucket == "decide"]

    if args.review:
        review(sources, found)
        return 1 if all_fix else 0

    if all_fix:
        print(f"FIX  ({len(all_fix)}) — no judgement in these, rewrite them\n")
        for finding in all_fix:
            print(f"  {finding.text()}\n")
    if args.fix_only:
        if not all_fix:
            print("No FIX findings.")
        return 1 if all_fix else 0
    if all_decide:
        print(f"DECIDE  ({len(all_decide)}) — read each sentence and answer for that sentence\n")
        for finding in all_decide:
            print(f"  {finding.text()}\n")
        print("  Most of these are real. Do not dismiss the group.\n")
    if not all_fix and not all_decide:
        print("The patterns matched nothing. The rules below still need a read.\n")
    if not args.no_read:
        print_read_list()
    return 1 if all_fix else 0

if __name__ == "__main__":
    raise SystemExit(main())
