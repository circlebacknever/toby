#!/usr/bin/env python3
"""Every gate in evals/run.py fails on a seeded regression and passes when it is undone.

A gate proved once by hand rots the first time someone refactors the checker.
Each case here edits a real file, runs the gate, restores the file, and checks
the gate went red and then green.

Run: python3 tests/test-gates.py
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RUNNER = REPO_ROOT / "evals" / "run.py"
GATES = REPO_ROOT / "evals" / "baselines" / "gates.json"

spec = importlib.util.spec_from_file_location("run", RUNNER)
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

failures: list[str] = []


def gates_output() -> tuple[int, str]:
    result = subprocess.run(
        [sys.executable, str(RUNNER), "gates"], cwd=REPO_ROOT, capture_output=True, text=True
    )
    return result.returncode, result.stdout + result.stderr


def seeded(label: str, path: Path, mutate, expect: str) -> None:
    """Apply mutate() to path, expect the gates to go red naming `expect`."""
    original = path.read_text()
    try:
        path.write_text(mutate(original))
        code, output = gates_output()
        if code == 0:
            print(f"FAIL {label}: gates stayed green on a seeded regression")
            failures.append(label)
        elif expect not in output:
            print(f"FAIL {label}: gates went red without naming {expect!r}")
            failures.append(label)
        else:
            print(f"ok   {label}")
    finally:
        path.write_text(original)


def add_after(marker: str, addition: str):
    def mutate(text: str) -> str:
        assert marker in text, marker
        return text.replace(marker, marker + addition, 1)
    return mutate


def delete(sentence: str):
    def mutate(text: str) -> str:
        assert sentence in text, sentence
        return text.replace(sentence, "", 1)
    return mutate


code, output = gates_output()
if code != 0:
    print("The tree is already red. Fix that before running this file.")
    print(output)
    raise SystemExit(1)
print("ok   baseline is green\n")

CLARITY = REPO_ROOT / "skills" / "toby-swd-clarity" / "SKILL.md"
TESTING = REPO_ROOT / "skills" / "toby-swd-testing" / "SKILL.md"
DOCS = REPO_ROOT / "skills" / "toby-swd-docs" / "SKILL.md"

seeded("banned word caught", CLARITY,
       add_after("## Consistency\n", "\nUse a robust approach here.\n"),
       "validator errors")

seeded("invented foil caught", CLARITY,
       add_after("## Consistency\n", "\nRename the field rather than widening it.\n"),
       "invented foil")

seeded("over-length sentence caught", CLARITY,
       add_after("## Consistency\n",
                 "\nPick the name that a reader who has never opened this file before "
                 "would guess correctly on their very first attempt without any help at all.\n"),
       "over-length sentence")

seeded("buried lead caught", CLARITY,
       add_after("## Consistency\n",
                 "\nConsistency in a codebase is one of those qualities that reveals itself "
                 "slowly over the lifetime of the project and its many maintainers.\n"),
       "buried lead")

seeded("deleted rule caught", TESTING,
       delete("Mock external dependencies at the system boundary."),
       "left the repo with no reworded survivor")

seeded("body growth caught", DOCS,
       add_after("# Toby SWD Docs\n",
                 "\n" + "Filler sentence that carries no rule whatsoever. " * 90 + "\n"),
       "grew past 10 percent")

seeded("co-load growth caught", DOCS,
       add_after("# Toby SWD Docs\n",
                 "\n" + "Filler sentence that carries no rule whatsoever. " * 90 + "\n"),
       "co-load feature-change")

# A skill name broken across a folded-scalar line wrap points at nothing.
seeded("split skill name caught", DOCS,
       lambda t: t.replace("`toby-swd-clarity` owns.", "`toby-swd-\n  clarity` owns.", 1),
       "broken across a line wrap")

STYLE = REPO_ROOT / "output-styles" / "toby.md"

seeded("output style drift caught", STYLE,
       lambda t: t.replace("Plain words. Concrete verbs.", "Plain words."),
       "drifted from base/toby.md")

seeded("output style losing the coding flag caught", STYLE,
       lambda t: t.replace("keep-coding-instructions: true", "keep-coding-instructions: false"),
       "keep-coding-instructions")

code, output = gates_output()
if code != 0:
    print("\nFAIL the tree did not come back green after the seeded edits")
    print(output)
    failures.append("restore")
else:
    print("ok   tree green again after every restore")

print()
if failures:
    print(f"{len(failures)} gate(s) cannot fail: {', '.join(failures)}")
    raise SystemExit(1)
print("Every gate fails on a seeded regression.")
