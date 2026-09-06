#!/usr/bin/env python3
"""The regression suite for this repo. One entry point, two kinds of check.

**Gates** run with no model and decide pass or fail. Every number they compare
against lives in `baselines/gates.json`. A gate that gets worse fails the run,
and a gate that gets better is recorded by `record` on purpose.

**Model suites** need a subagent to write something, so they cannot gate. They
carry their prompts here so a later run is the same run, and they record a
distribution rather than a score. Five samples of the voice suite on identical
inputs scored 1, 1, 4, 4, and 11, so a single number from one of them means
nothing. `compare` refuses to call a difference real when the ranges overlap.

Commands:
  run.py gates              every deterministic check, exits 1 on regression
  run.py gates --slow       adds the install smoke test
  run.py record             rewrite baselines/gates.json from the current tree
  run.py prompt <suite>     print the prompt to hand a subagent
  run.py compare <suite> <files...>   score outputs against the recorded run
  run.py list               what suites exist
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import statistics
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
EVALS = REPO_ROOT / "evals"
BASELINES = EVALS / "baselines"
GATES_FILE = BASELINES / "gates.json"


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate = load("validate_skills", REPO_ROOT / "scripts" / "validate-skills.py")


# ---------------------------------------------------------------- measurements

def warning_classes() -> dict[str, int]:
    """Validator warnings, counted by kind. The kind is what regresses."""
    errors: list[str] = []
    warnings: list[str] = []
    validate.check_voice_compliance(errors, warnings)
    validate.check_ste_conformance(warnings)
    validate.check_cross_skill_collisions(warnings)
    validate.check_anti_triggers(warnings)
    validate.check_buried_leads(warnings)
    reference_warnings: list[str] = []
    validate.check_reference_reachability([], reference_warnings)
    warnings.extend(reference_warnings)

    kinds = {
        "banned word": r"^banned word",
        "sense-scoped word": r"^check sense of",
        "invented foil": r"^possible invented foil",
        "over-length sentence": r"^sentence runs",
        "over-long paragraph": r"^paragraph runs",
        "latin abbreviation": r"^Latin abbreviation",
        "cross-skill collision": r"^sentence duplicated",
        "missing skip clause": r"carries no skip clause",
        "buried lead": r"opens on a thesis",
        "unreferenced file": r"^reference file nothing points at",
    }
    counts = {name: 0 for name in kinds}
    for warning in warnings:
        for name, pattern in kinds.items():
            if re.search(pattern, warning):
                counts[name] += 1
                break
    return counts


def skill_tokens() -> dict[str, int]:
    return {
        d.name: validate.tokens(validate.body_of((d / "SKILL.md").read_text()))
        for d in validate.skill_dirs()
    }


def coload_tokens() -> dict[str, int]:
    sizes = skill_tokens()
    return {
        group: sum(sizes.get(name, 0) for name in members)
        for group, members in validate.ROUTING_GROUPS.items()
    }


def lost_rules() -> list[str]:
    """Sentences in the recorded inventory with no relative in the tree today.

    The list is the baseline, and not its length. A deletion that lands the same
    week a rewording arrives keeps the count still and swaps the contents.
    """
    inventory = load("rule_inventory", REPO_ROOT / "scripts" / "rule-inventory.py")
    current = set()
    for path in inventory.paths():
        current.update(inventory.sentences(path))
    before = set(BASELINES.joinpath("rules.txt").read_text().splitlines())

    diff = load("rule_diff", REPO_ROOT / "scripts" / "rule-diff.py")
    # Pair each gone sentence against surviving ones only. `rule-diff.py` also
    # asks whether the words survive anywhere in the repo, which reads well in a
    # report and gates nothing: common words always survive somewhere. Deleting
    # "Mock external dependencies at the system boundary" passed that fallback
    # while the rule was gone.
    survivors = [(line, diff.content(line)) for line in current]

    lost = []
    for line in sorted(before - current):
        words = diff.content(line)
        best = max((diff.overlap(words, cand) for _, cand in survivors), default=0.0)
        # A short sentence has few content words, and three common ones landing
        # in some unrelated sentence clears 0.6 on their own. "Mock external
        # dependencies at the system boundary" survived that way while the rule
        # was deleted, so a short sentence has to match a survivor completely.
        needed = 1.0 if len(words) < 8 else diff.THRESHOLD
        if best < needed:
            lost.append(line)
    return lost


def snapshot() -> dict:
    return {
        "warning_classes": warning_classes(),
        "skill_tokens": skill_tokens(),
        "coload_tokens": coload_tokens(),
        "accepted_lost_rules": lost_rules(),
    }


# ---------------------------------------------------------------------- gates

def run_script(label: str, command: list[str], failures: list[str]) -> None:
    result = subprocess.run(command, cwd=REPO_ROOT, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"ok   {label}")
    else:
        print(f"FAIL {label}")
        print("     " + (result.stdout + result.stderr).strip().splitlines()[-1][:160])
        failures.append(label)


def gates(slow: bool) -> int:
    if not GATES_FILE.exists():
        sys.exit("no baselines/gates.json. Run: evals/run.py record")
    base = json.loads(GATES_FILE.read_text())
    now = snapshot()
    failures: list[str] = []

    errors: list[str] = []
    validate.check_skills(REPO_ROOT / "skills", errors)
    validate.check_instruction_sync(errors)
    validate.check_stale_references(errors)
    validate.check_review_skill(errors)
    validate.check_operating_guide_refs(errors)
    validate.check_voice_compliance(errors, [])
    validate.check_single_source(errors)
    validate.check_token_budget(errors, [])
    validate.check_reference_reachability(errors, [])
    validate.check_description_backticks(errors)
    if errors:
        print(f"FAIL validator, {len(errors)} error(s)")
        for error in errors[:5]:
            print(f"     {error}")
        failures.append("validator errors")
    else:
        print("ok   validator errors: none")

    for kind, before in sorted(base["warning_classes"].items()):
        after = now["warning_classes"].get(kind, 0)
        if after > before:
            print(f"FAIL {kind}: {before} -> {after}")
            failures.append(kind)
        else:
            arrow = f"{before} -> {after}" if after != before else str(after)
            print(f"ok   {kind}: {arrow}")

    for name, before in sorted(base["skill_tokens"].items()):
        after = now["skill_tokens"].get(name)
        if after is None:
            print(f"FAIL {name} has no SKILL.md any more")
            failures.append(name)
        elif after > before * 1.10:
            print(f"FAIL {name} body grew past 10 percent: {before} -> {after}")
            failures.append(name)

    for group, before in sorted(base["coload_tokens"].items()):
        after = now["coload_tokens"].get(group, 0)
        if after > before * 1.05:
            print(f"FAIL co-load {group} grew past 5 percent: {before} -> {after}")
            failures.append(group)
        else:
            print(f"ok   co-load {group}: {before} -> {after}")

    accepted = set(base["accepted_lost_rules"])
    new_losses = [line for line in now["accepted_lost_rules"] if line not in accepted]
    if new_losses:
        print(f"FAIL {len(new_losses)} rule(s) left the repo with no reworded survivor")
        for line in new_losses[:5]:
            print(f"     {line[:120]}")
        failures.append("lost rules")
    else:
        print(f"ok   lost rules: none beyond the {len(accepted)} accepted")

    run_script("validator fixtures", [sys.executable, "tests/test-validator-checks.py"], failures)
    run_script("stop hook fixtures", [sys.executable, "tests/test-voice-hook.py"], failures)
    run_script("instruction sync", ["bash", "scripts/sync.sh", "--check"], failures)
    if slow:
        run_script("install smoke test", ["bash", "scripts/test-install.sh"], failures)

    print()
    if failures:
        print(f"{len(failures)} gate(s) regressed: {', '.join(failures)}")
        print("If the change is intended, run: evals/run.py record")
        return 1
    print("All gates hold.")
    return 0


def record() -> int:
    GATES_FILE.write_text(json.dumps(snapshot(), indent=2, sort_keys=True) + "\n")
    data = json.loads(GATES_FILE.read_text())
    print(f"wrote {GATES_FILE.relative_to(REPO_ROOT)}")
    print(f"  {sum(data['warning_classes'].values())} warnings across {len(data['warning_classes'])} classes")
    print(f"  {len(data['skill_tokens'])} skills, {sum(data['skill_tokens'].values())} body tokens")
    print(f"  {len(data['accepted_lost_rules'])} accepted rule deletions")
    return 0


# --------------------------------------------------------------- model suites

SUITES = {
    "voice": {
        "file": "suites/voice.md",
        "scorer": "score-voice",
        "min_samples": 5,
        "prompt": """Write four short pieces of prose in Toby's voice.

Setup, follow it exactly:
1. Read {repo}/skills/toby-voice/SKILL.md
2. Read {repo}/skills/toby-voice/references/toby.md — the rules file. Load it in full.
3. Read {repo}/evals/suites/voice.md

Write the four outputs to {repo}/evals/results/voice-<run>.md, in this format and
nothing else:

## 1
<the status update>

## 2
<the pushback>

## 3
<the PR description>

## 4
<the I-don't-know reply>

No preamble, no summary, no notes. Reply with just the word "done".""",
    },
    "triggering": {
        "file": "suites/triggering.md",
        "scorer": "triggering",
        "min_samples": 2,
        "prompt": """You are simulating a coding agent's skill-routing decision. Do no engineering work.

Read {repo}/evals/baselines/descriptions-current.txt — 14 skills, each with a name
and description. That is the entire routing surface a host tool sees.

Read {repo}/evals/suites/triggering.md for the eight prompts. Read ONLY each
scenario's blockquoted user prompt. Do NOT read the "Should load" lines before
deciding.

For each of P1-P4 and N1-N6, decide which skills you would load, receiving that
prompt cold with only the descriptions in front of you. Be realistic and slightly
generous: if a description's trigger nouns match, that skill fires.

Write to {repo}/evals/results/triggering-<run>.txt, one line per scenario:
P1 fired: <comma-separated names>

Report only what fired. `evals/run.py compare triggering <file>` does the
scoring, so do not total anything yourself and do not read the expected sets.""",
    },
    "feature-dev": {
        "file": "suites/feature-dev.md",
        "scorer": "manual",
        "min_samples": 1,
        "prompt": """Follow a skill and report what it tells you to produce. Write no code and
edit no file except the output named below.

1. Read {repo}/skills/toby-feature-dev/SKILL.md in full.
2. Read the two requests in {repo}/evals/suites/feature-dev.md, and read only
   the blockquoted request text. Do not read the Expected lines.

For each request work out, from the skill alone: the mode, the size and which
trigger fired, exactly which gates you owe at that size, and one blunt line on
whether that much process fits the request.

Write it to {repo}/evals/results/feature-dev-<run>.md, quoting the line from the
skill that decided the size.""",
    },
    "review": {
        "file": "suites/review.md",
        "scorer": "manual",
        "min_samples": 1,
        "prompt": """Review a diff. Follow the review skill exactly.

1. Read {repo}/skills/toby-code-review/SKILL.md and its references/smells.md.
2. The change under review is {repo}/evals/fixtures/export.diff.
3. The agreed acceptance criteria are {repo}/evals/fixtures/criteria.md. No plan
   file and no behavior record exist for this work.

The code is not runnable here — there is only the diff and the criteria. Say so
where the skill asks you to run something.

Write the review to {repo}/evals/results/review-<run>.md, in the format the
skill's Final report section specifies. Nothing else in the file.""",
    },
}


SCENARIO_RE = re.compile(r"^### ((?:P|N)\d+) .*?$(.*?)(?=^### |\Z)", re.M | re.S)
DIRECTIVE_RE = re.compile(r"^(Required|Forbidden|Optional|Exactly one of): (.+)$", re.M)
SKILL_NAME_RE = re.compile(r"toby-[a-z-]+")


def expected_sets() -> dict[str, dict[str, set[str]]]:
    """Read each scenario's fenced directive block.

    The prose under it is for a person. Parsing that prose read "nothing, or
    `toby-swd-clarity` at most" as a requirement and reported three misses that
    were not misses, so the directives are their own lines.
    """
    text = (EVALS / "suites" / "triggering.md").read_text()
    out: dict[str, dict[str, set[str]]] = {}
    for name, body in SCENARIO_RE.findall(text):
        directives: dict[str, set[str]] = {}
        for kind, value in DIRECTIVE_RE.findall(body):
            directives[kind] = set(SKILL_NAME_RE.findall(value))
        out[name] = directives
    return out


FIRED_RE = re.compile(r"^((?:P|N)\d+) fired: (.*)$", re.M)


def score_triggering(path: Path) -> dict:
    """Score a run against the suite, here rather than in the agent that wrote it.

    The runner used to ask the subagent for its own totals while telling it not
    to read the expected sets, so it had to guess them. One run reported a false
    fire on N1 for loading exactly the skill N1 calls for.
    """
    expected = expected_sets()
    fired = {name: set(SKILL_NAME_RE.findall(rest)) for name, rest in FIRED_RE.findall(path.read_text())}
    false_fires, missed = [], []
    for name, directives in expected.items():
        got = fired.get(name, set())
        for skill in sorted(got & directives.get("Forbidden", set())):
            false_fires.append(f"{name} {skill}")
        for skill in sorted(directives.get("Required", set()) - got):
            missed.append(f"{name} {skill}")
        one_of = directives.get("Exactly one of")
        if one_of and len(got & one_of) != 1:
            picked = ", ".join(sorted(got & one_of)) or "nothing"
            false_fires.append(f"{name} picked {picked} where exactly one was needed")
    return {"fired": fired, "false_fires": false_fires, "missed": missed,
            "scenarios_answered": len(fired), "scenarios_expected": len(expected)}


def score_voice(paths: list[Path]) -> list[int]:
    scorer = load("score_voice", REPO_ROOT / "scripts" / "score-voice.py")
    return [scorer.score(path)["defects"] for path in paths]


def compare(suite: str, paths: list[Path]) -> int:
    spec = SUITES[suite]
    if spec["scorer"] == "triggering":
        recorded = json.loads((BASELINES / "triggering.json").read_text())
        print(f"before Group 2: {recorded['before']['false_fires_N1_N4']} false fires, "
              f"{recorded['before']['missed_P1_P4']} missed")
        worst = 0
        for path in paths:
            result = score_triggering(path)
            missing = result["scenarios_expected"] - result["scenarios_answered"]
            print(f"\n{path.name}: {len(result['false_fires'])} false fires, {len(result['missed'])} missed"
                  + (f", {missing} scenario(s) unanswered" if missing else ""))
            for entry in result["false_fires"]:
                print(f"  false fire  {entry}")
            for entry in result["missed"]:
                print(f"  missed      {entry}")
            worst = max(worst, len(result["false_fires"]) + len(result["missed"]))
        print()
        print("Clean." if worst == 0 else f"{worst} defect(s) in the worst run.")
        return 0
    if spec["scorer"] != "score-voice":
        sys.exit(f"suite {suite!r} is read by a person. evals/README.md says what to look for.")

    scores = score_voice(paths)
    recorded = json.loads((BASELINES / f"{suite}.json").read_text())
    before = recorded["scores"]

    def line(label: str, values: list[int]) -> str:
        return (
            f"{label:22} n={len(values):<3} scores={values}  "
            f"mean={statistics.mean(values):.1f}  range={min(values)}-{max(values)}"
        )

    print(line(recorded["label"], before))
    print(line("this run", scores))
    print()

    if len(scores) < spec["min_samples"]:
        print(f"{len(scores)} samples. This suite needs {spec['min_samples']} before the numbers say anything.")
        return 0

    overlap = min(before) <= max(scores) and min(scores) <= max(before)
    if overlap:
        print("Ranges overlap. No difference to report, whatever the means do.")
        print("Two samples an arm read as a clean win here once, and five samples took it back.")
        return 0
    verdict = "better" if statistics.mean(scores) < statistics.mean(before) else "worse"
    print(f"Ranges are disjoint. This run is {verdict}.")
    return 0


def prompt(suite: str) -> int:
    print(SUITES[suite]["prompt"].format(repo=REPO_ROOT))
    return 0


def list_suites() -> int:
    print("Gates run with no model and decide pass or fail:")
    print("  evals/run.py gates\n")
    print("Model suites need a subagent, and record a distribution:")
    for name, spec in SUITES.items():
        recorded = BASELINES / f"{name}.json"
        mark = "recorded" if recorded.exists() else "no baseline yet"
        print(f"  {name:12} {spec['min_samples']} samples minimum, {mark}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    gate = sub.add_parser("gates")
    gate.add_argument("--slow", action="store_true", help="add the install smoke test")
    sub.add_parser("record")
    sub.add_parser("list")
    p = sub.add_parser("prompt")
    p.add_argument("suite", choices=sorted(SUITES))
    c = sub.add_parser("compare")
    c.add_argument("suite", choices=sorted(SUITES))
    c.add_argument("files", nargs="+")
    args = parser.parse_args()

    if args.command == "gates":
        return gates(args.slow)
    if args.command == "record":
        return record()
    if args.command == "list":
        return list_suites()
    if args.command == "prompt":
        return prompt(args.suite)
    return compare(args.suite, [Path(f) for f in args.files])


if __name__ == "__main__":
    raise SystemExit(main())
