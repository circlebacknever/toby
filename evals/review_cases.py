#!/usr/bin/env python3
"""Prepare blinded reviews, verify seeded regressions, and score independent findings."""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
import difflib
import importlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "evals" / "review_cases"


def load_fixture():
    """Load fixture source without importing the application under review."""
    spec = importlib.util.spec_from_file_location("review_fixture", CASES / "fixture.py")
    fixture = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(fixture)
    return fixture


def write_tree(destination: Path, files: dict[str, str]) -> None:
    """Write a fixture tree below an inspected empty destination."""
    destination.mkdir(parents=True)
    for relative, content in files.items():
        path = destination / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)


def prepare(destination: Path, skills_source: Path = ROOT, clean: bool = False) -> None:
    """Copy the review inputs while excluding gold, private probes, and prior outputs."""
    if destination.exists():
        raise ValueError(f"Destination already exists: {destination}")
    fixture = load_fixture()
    before = fixture.BASE
    after = fixture.changed_files()
    if clean:
        gold = json.loads((CASES / "gold.json").read_text())
        guarded = {item["path"] for item in gold["guarded_changes"]}
        after = {path: after[path] if path in guarded else content
                 for path, content in before.items()}
        after["CHANGE.md"] = (
            "# Parcel changes\n\n"
            "This change simplifies the allowlisted admin expressions and adds optional receipt metadata.\n"
            "Existing behavior and the contracts in README.md stay unchanged.\n"
        )
    destination.mkdir(parents=True)
    write_tree(destination / "before", before)
    write_tree(destination / "after", after)
    changes = []
    for path in sorted(set(before) | set(after)):
        changes.extend(difflib.unified_diff(
            before.get(path, "").splitlines(True), after.get(path, "").splitlines(True),
            fromfile="a/" + path, tofile="b/" + path,
        ))
    (destination / "change.diff").write_text("".join(changes))
    for path in sorted((skills_source / "skills").glob("toby-*/**/*.md")):
        target = destination / path.relative_to(skills_source)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, target)
    shutil.copyfile(skills_source / "base" / "toby.md", destination / "GUIDE.md")
    (destination / "TASK.md").write_text(REVIEW_TASK)


REVIEW_TASK = """# Parcel review

Review the proposed change for defects. Don't edit the application.

Read GUIDE.md and skills/toby-code-review/SKILL.md, and follow the skill.
The proposed change is change.diff. Read after/CHANGE.md and after/README.md
for intent and contracts. The runnable proposed repository is after/, and
before/ contains its previous version. Refer to the other copied skills when needed.
Use only this directory, local standard-library tools, and temporary files.
Don't inspect the authoring checkout, gold, private probes, or another review.

Run focused local checks when they can establish a finding. No dependency
installation, server, or external service is required. Store your report in
review.json. Each finding must describe the trigger, actual consequence, and
smallest repair in plain prose. Cite the root cause in the proposed version.
Don't guess expected findings or pad the report to a count.

Use this JSON shape:

```json
{
  "findings": [
    {"path": "parcel/example.py", "line": 12,
     "body": "The concrete failure, the input that reaches it, and its repair."}
  ],
  "checks": [{"command": "the command you ran", "result": "what it proved"}],
  "limitations": []
}
```

Use an empty findings array when you found no defects. Return the report path.
"""


@contextmanager
def application(tree: Path):
    """Load each application version in isolation and restore imported modules afterward."""
    saved = {key: value for key, value in sys.modules.items()
             if key == "parcel" or key.startswith("parcel.")}
    for key in saved:
        del sys.modules[key]
    sys.path.insert(0, str(tree))
    try:
        importlib.invalidate_caches()
        yield lambda module: importlib.import_module("parcel." + module)
    finally:
        sys.path.remove(str(tree))
        for key in list(sys.modules):
            if key == "parcel" or key.startswith("parcel."):
                del sys.modules[key]
        sys.modules.update(saved)


def seeded_connection(module, path=":memory:"):
    """Create the same local data for each independent probe."""
    connection = module.connect(path)
    module.initialize(connection)
    return connection


def probe_invoice_cents(load):
    actual = load("billing").invoice_total(199, 20)
    return actual == 239, f"invoice_total(199, 20)={actual}, expected 239"


def probe_account_scope(load):
    with seeded_connection(load("database")) as connection:
        connection.execute("INSERT INTO orders VALUES ('private', 'other', 'paid', 0)")
        result = load("routes").dispatch("/orders/get", {
            "connection": connection, "account_id": "caller", "order_id": "private"})
    return result[0] == 404, f"foreign-account lookup status={result[0]}, expected 404"


def probe_shipment_wire(load):
    events = load("events")
    try:
        actual = events.read_order(events.encode_order("o1"))
    except KeyError as error:
        return False, f"new message raises {error!r} in existing consumer"
    return actual == "o1", f"consumer decoded order={actual!r}"


class BarrierCursor:
    """Pause each stock read after SQLite returns its result to expose the race."""
    def __init__(self, cursor, barrier):
        self.cursor = cursor
        self.barrier = barrier

    def fetchone(self):
        result = self.cursor.fetchone()
        self.barrier.wait(timeout=5)
        return result


class BarrierConnection:
    """Keep SQLite transactions intact while coordinating only the vulnerable read."""
    def __init__(self, connection, barrier):
        self.connection = connection
        self.barrier = barrier

    def __enter__(self):
        self.connection.__enter__()
        return self

    def __exit__(self, *args):
        return self.connection.__exit__(*args)

    def execute(self, statement, parameters=()):
        cursor = self.connection.execute(statement, parameters)
        if statement.startswith("SELECT available FROM inventory"):
            return BarrierCursor(cursor, self.barrier)
        return cursor


def probe_stock_race(load):
    database = load("database")
    inventory = load("inventory")
    with tempfile.TemporaryDirectory(prefix="parcel-stock-") as directory:
        path = str(Path(directory) / "inventory.sqlite")
        with seeded_connection(database, path) as connection:
            connection.execute("INSERT INTO inventory VALUES ('last', 1)")
        barrier = threading.Barrier(2)

        def request(_):
            connection = database.connect(path)
            try:
                return inventory.reserve(BarrierConnection(connection, barrier), "last", 1)
            finally:
                connection.close()

        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(request, range(2)))
        with database.connect(path) as connection:
            reserved = connection.execute("SELECT SUM(quantity) FROM reservations").fetchone()[0]
    return sum(outcomes) == 1 and reserved == 1, f"successes={sum(outcomes)}, units reserved={reserved}, expected 1 each"


class Gateway:
    """Simulate a provider that commits the first charge before losing its response."""
    def __init__(self):
        self.charges = {}
        self.drop_response = True

    def charge(self, amount_cents, *, idempotency_key):
        if idempotency_key not in self.charges:
            self.charges[idempotency_key] = amount_cents
            if self.drop_response:
                self.drop_response = False
                raise TimeoutError("Response lost after charge")
        return {"charge_id": idempotency_key}


def probe_charge_retry(load):
    gateway = Gateway()
    load("payments").collect_charge(gateway, "o1", 1200)
    count = len(gateway.charges)
    return count == 1, f"provider accepted {count} charges, expected 1"


class Publisher:
    """Fail the first publish before accepting any event, then deduplicate by event id."""
    def __init__(self):
        self.events = {}
        self.fail_next = True

    def publish(self, payload, *, event_id):
        if self.fail_next:
            self.fail_next = False
            raise ConnectionError("Publisher unavailable")
        self.events.setdefault(event_id, payload)


def probe_paid_event(load):
    dispatch = load("dispatch")
    publisher = Publisher()
    with seeded_connection(load("database")) as connection:
        connection.execute("INSERT INTO orders VALUES ('o1', 'a1', 'open', 0)")
        connection.commit()
        try:
            dispatch.mark_paid(connection, publisher, "o1")
            dispatch.flush_outbox(connection, publisher)
        except ConnectionError:
            pass
        dispatch.mark_paid(connection, publisher, "o1")
        dispatch.flush_outbox(connection, publisher)
        status = connection.execute("SELECT status FROM orders").fetchone()[0]
    count = len(publisher.events)
    return status == "paid" and count == 1, f"persisted status={status}, published events={count}, expected paid and 1"


def probe_page_bound(load):
    with seeded_connection(load("database")) as connection:
        connection.executemany("INSERT INTO orders VALUES (?, 'a1', 'paid', 0)",
                               [(str(index),) for index in range(150)])
        status, rows = load("routes").dispatch("/orders/list", {
            "connection": connection, "account_id": "a1", "limit": 1000000})
    return status == 200 and len(rows) <= 100, f"client limit=1000000 returned {len(rows)} rows, maximum 100"


def probe_tracking_timeout(load):
    class Client:
        def get(self, path, **options):
            return options
    options = load("tracking").track(Client(), "s1")
    return options.get("timeout") == 3, f"outbound timeout={options.get('timeout')!r}, expected 3 seconds"


def probe_sync_context(load):
    class Client:
        def sync(self, record_id):
            raise TimeoutError("Provider did not respond")
    stream = io.StringIO()
    logger = load("runtime").configure_logger(stream)
    result = load("worker").sync_record(Client(), "record-17", "request-23", logger)
    output = stream.getvalue()
    required = ["record-17", "request-23", "TimeoutError", "Provider did not respond"]
    missing = [value for value in required if value not in output]
    return result is False and not missing, f"rendered failure log missing={missing!r}"


def probe_required_key(load):
    accepted = []
    for environment in [{}, {"BILLING_API_KEY": "   "}]:
        try:
            load("config").load_config(environment)
        except ValueError:
            continue
        accepted.append(environment)
    return not accepted, f"startup accepted {len(accepted)} missing or blank credentials, expected 0"


def probe_returns_route(load):
    status, _ = load("routes").dispatch("/returns", {})
    return status == 200, f"dispatch('/returns') status={status}, expected 200"


def probe_refund_policy(load):
    order = {"status": "shipped", "created_day": 1}
    support_allows = load("support").refund_allowed(dict(order), 10)
    status, _ = load("routes").dispatch("/orders/refund", {"order": dict(order), "today": 10})
    return not support_allows and status == 409, f"shipped order: support allows={support_allows}, HTTP status={status}, expected False and 409"


PROBES = {name.removeprefix("probe_"): value for name, value in list(globals().items())
          if name.startswith("probe_") and callable(value)}


def verify() -> int:
    """Require each private contract probe to pass before and fail after the proposed change."""
    fixture = load_fixture()
    gold = json.loads((CASES / "gold.json").read_text())
    if set(PROBES) != {case["probe"] for case in gold["cases"]}:
        raise ValueError("Gold and probe inventory differ")
    failures = []
    with tempfile.TemporaryDirectory(prefix="parcel-review-verify-") as directory:
        for label, files in [("before", fixture.BASE), ("after", fixture.changed_files())]:
            tree = Path(directory) / label
            write_tree(tree, files)
            smoke = subprocess.run([sys.executable, "-B", "-m", "unittest", "discover", "-s", "tests"],
                                   cwd=tree, capture_output=True, text=True, timeout=15)
            print(f"{label} smoke: {'PASS' if smoke.returncode == 0 else 'FAIL'}")
            if smoke.returncode:
                failures.append(label + " smoke")
                print(smoke.stdout + smoke.stderr)
            with application(tree) as load:
                for case in gold["cases"]:
                    passed, evidence = PROBES[case["probe"]](load)
                    print(f"{label} {case['id']}: {'PASS' if passed else 'FAIL'} | {evidence}")
                    if passed != (label == "before"):
                        failures.append(label + " " + case["id"])
    return 1 if failures else 0


def grade(review: dict, judgment: dict, gold: dict | None = None) -> dict:
    """Score each independently judged finding once and penalize unmatched or duplicate findings."""
    gold = gold or json.loads((CASES / "gold.json").read_text())
    cases = {case["id"]: case for case in gold["cases"]}
    findings = review["findings"]
    decisions = judgment["decisions"]
    indexes = [decision["finding"] for decision in decisions]
    if sorted(indexes) != list(range(1, len(findings) + 1)):
        raise ValueError("Judgment must cover each finding exactly once, using 1-based indexes")
    matched = set()
    rejected = []
    for decision in decisions:
        index = decision["finding"]
        finding = findings[index - 1]
        quote = decision.get("quote", "")
        if not quote or quote not in finding["body"] or not decision.get("reason", "").strip():
            raise ValueError(f"Decision {index} requires an exact finding quote and a reason")
        case_id = decision.get("match")
        if case_id is None:
            rejected.append({"finding": index, "reason": decision["reason"]})
            continue
        if case_id not in cases:
            raise ValueError(f"Unknown case id: {case_id}")
        evidence = decision.get("evidence", {})
        for part in ["trigger", "mechanism", "consequence", "repair"]:
            excerpt = evidence.get(part, "")
            if not excerpt or excerpt not in finding["body"]:
                raise ValueError(f"Matched finding {index} requires its own {part} evidence")
        if len(set(evidence.values())) < 4:
            raise ValueError(f"Matched finding {index} needs distinct evidence for its four claims")
        if finding["path"] != cases[case_id]["path"]:
            raise ValueError(f"Finding {index} cites a different root-cause file for {case_id}")
        if not isinstance(finding["line"], int) or isinstance(finding["line"], bool) or finding["line"] < 1:
            raise ValueError(f"Finding {index} requires a positive source line")
        source = load_fixture().changed_files()[finding["path"]]
        if finding["line"] > len(source.splitlines()):
            raise ValueError(f"Finding {index} cites a line outside the reviewed file")
        if case_id in matched:
            rejected.append({"finding": index, "reason": "Duplicate root cause"})
        else:
            matched.add(case_id)
    true_positives = len(matched)
    false_positives = len(rejected)
    missing = sorted(set(cases) - matched)
    return {
        "true_positives": true_positives,
        "false_positives": false_positives,
        "false_negatives": len(missing),
        "precision": true_positives / len(findings) if findings else 0.0,
        "recall": true_positives / len(cases) if cases else None,
        "score": true_positives - 2 * false_positives,
        "matched": sorted(matched), "missing": missing, "rejected": rejected,
        "pass": not missing and not rejected,
    }


def judge_prompt(directory: Path) -> str:
    """Give a separate reader the submitted findings and private matching criteria."""
    return f"""Independently grade {directory / 'review.json'} against {CASES / 'gold.json'}.
Read the exact reviewed source in {directory / 'after'} and its change.diff.
You didn't write this review. Don't add findings or improve their wording.
Read the gold matching rule. For each finding, decide whether its own words
identify a gold failure's trigger, mechanism, and consequence, and propose a
repair that actually preserves the contract. A suggestion, category name,
or cited line alone doesn't match. Check the existing guards.
Reject unsupported findings, unrelated mechanisms, and findings on unchanged
defects. A finding earns at most one match. Report any real unseeded defect
separately for human verification before this score is accepted.
Write {directory / 'judgment.json'} as JSON with a decisions array:
{{"decisions": [{{"finding": 1, "match": "a_gold_id_or_null", "quote": "exact words from this finding", "reason": "why it matches or fails", "evidence": {{"trigger": "exact excerpt", "mechanism": "exact excerpt", "consequence": "exact excerpt", "repair": "exact excerpt"}}}}]}}
Use JSON null for an unmatched finding. Cover every finding once, using its
1-based index. Matched findings need four distinct exact excerpts. Don't infer
a mechanism the writer didn't state. You supply the semantic judgment. The
scorer validates coverage, excerpts, citations, and arithmetic, not meaning.
Return the path.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    create = commands.add_parser("prepare")
    create.add_argument("directory", type=Path)
    create.add_argument("--skills-source", type=Path, default=ROOT)
    create.add_argument("--clean", action="store_true", help="prepare only the guarded changes")
    commands.add_parser("verify")
    prompt = commands.add_parser("judge-prompt")
    prompt.add_argument("directory", type=Path)
    scoring = commands.add_parser("grade")
    scoring.add_argument("review", type=Path)
    scoring.add_argument("judgment", type=Path)
    scoring.add_argument("--clean", action="store_true", help="expect zero seeded defects")
    args = parser.parse_args()
    if args.command == "prepare":
        prepare(args.directory.resolve(), args.skills_source.resolve(), args.clean)
        print(args.directory.resolve() / "TASK.md")
        return 0
    if args.command == "verify":
        return verify()
    if args.command == "judge-prompt":
        print(judge_prompt(args.directory.resolve()))
        return 0
    gold = {"cases": []} if args.clean else None
    result = grade(json.loads(args.review.read_text()), json.loads(args.judgment.read_text()), gold)
    print(json.dumps(result, indent=2))
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
