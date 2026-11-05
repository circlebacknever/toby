#!/usr/bin/env python3
"""Check candidate report actions through domain, API, command, and emitted logs."""

from __future__ import annotations

import contextlib
import importlib
import io
import json
from pathlib import Path
import sys
import unittest


SECRET = "fixture-credential-should-never-be-emitted"
LOG_OUTPUT = io.StringIO()
STDOUT = io.StringIO()


class ArchiveContract(unittest.TestCase):
    def setUp(self):
        LOG_OUTPUT.seek(0)
        LOG_OUTPUT.truncate()
        STDOUT.seek(0)
        STDOUT.truncate()
        self.report = reports.Report("report-delta")
        self.request_id = "request-delta"

    def provider(self, outcomes=()):
        return providers.ArchiveProvider(outcomes)

    def route(self, provider=None):
        return routes.handle("archive", self.report,
                             provider if provider is not None else self.provider(),
                             self.request_id)

    def emitted_event(self, outcome):
        events = []
        for line in LOG_OUTPUT.getvalue().splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        matches = [event for event in events
                   if event.get("report_id") == self.report.id
                   and event.get("request_id") == self.request_id
                   and event.get("outcome") == outcome]
        self.assertTrue(matches, f"missing emitted {outcome} event with report and request context")
        event = matches[-1]
        self.assertIsInstance(event.get("event"), str)
        self.assertTrue(event["event"].strip())
        self.assertIsInstance(event.get("duration_ms"), (int, float))
        self.assertGreaterEqual(event["duration_ms"], 0)
        self.assertEqual(STDOUT.getvalue(), "", "service diagnostics must use stderr")
        return event

    def test_route_archives_a_ready_report(self):
        provider = self.provider([{"receipt": "receipt-unusual"}])
        result = self.route(provider)
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"], {
            "report_id": self.report.id, "state": "archived", "archive_id": "receipt-unusual",
        })
        self.assertEqual(self.report.state, "archived")
        self.assertEqual(self.report.archive_id, "receipt-unusual")
        self.assertEqual(provider.calls, [self.report.id])

    def test_command_exposes_the_same_archive_action(self):
        result = commands.run_command("archive", self.report, self.provider(), self.request_id)
        self.assertEqual(result["status"], 200)
        self.assertEqual(result["body"]["state"], "archived")

    def test_domain_operation_enforces_state_without_the_route(self):
        self.report.state = "draft"
        provider = self.provider()
        with self.assertRaises(reports.InvalidState):
            reports.archive_report(self.report, provider, self.request_id)
        self.assertEqual(self.report.state, "draft")
        self.assertIsNone(self.report.archive_id)
        self.assertEqual(provider.calls, [])
        self.assertEqual(self.route(provider)["status"], 409)

    def test_repeating_an_archive_reuses_the_receipt(self):
        provider = self.provider([{"receipt": "receipt-stable"}])
        first = self.route(provider)
        second = self.route(provider)
        self.assertEqual(first, second)
        self.assertEqual(provider.calls, [self.report.id])

    def test_provider_failure_preserves_state_and_allows_retry(self):
        provider = self.provider([providers.ProviderUnavailable("controlled timeout"),
                                  {"receipt": "receipt-retry"}])
        result = self.route(provider)
        self.assertEqual(result["status"], 503)
        self.assertEqual(self.report.state, "ready")
        self.assertIsNone(self.report.archive_id)
        retry = self.route(provider)
        self.assertEqual(retry["status"], 200)
        self.assertEqual(retry["body"]["archive_id"], "receipt-retry")
        self.assertEqual(provider.calls, [self.report.id, self.report.id])

    def test_domain_failure_preserves_the_original_cause(self):
        failure = providers.ProviderUnavailable("controlled timeout")
        with self.assertRaises(reports.ArchiveUnavailable) as caught:
            reports.archive_report(self.report, self.provider([failure]), self.request_id)
        self.assertIs(caught.exception.__cause__, failure)

    def test_success_diagnostics_are_emitted(self):
        self.route()
        self.emitted_event("success")

    def test_failure_diagnostics_are_emitted_safely(self):
        provider = self.provider([providers.ProviderUnavailable(f"provider token={SECRET}")])
        result = self.route(provider)
        event = self.emitted_event("failure")
        self.assertEqual(event.get("error_type"), "ProviderUnavailable")
        self.assertNotIn(SECRET, LOG_OUTPUT.getvalue())
        self.assertNotIn(SECRET, STDOUT.getvalue())
        self.assertNotIn(SECRET, json.dumps(result))

    def test_existing_publish_and_unknown_action_stay_available(self):
        result = routes.handle("publish", self.report, self.provider(), self.request_id)
        self.assertEqual(result["status"], 200)
        self.assertEqual(self.report.state, "published")
        self.assertEqual(routes.handle("unknown", self.report, self.provider(), self.request_id)["status"], 404)


def main() -> int:
    global reports, providers, routes, commands
    workspace = Path(sys.argv[1]).resolve()
    sys.path.insert(0, str(workspace))
    with contextlib.redirect_stderr(LOG_OUTPUT), contextlib.redirect_stdout(STDOUT):
        try:
            reports = importlib.import_module("app.reports")
            providers = importlib.import_module("app.provider")
            routes = importlib.import_module("app.routes")
            commands = importlib.import_module("app.cli")
        except Exception as exc:
            print(f"candidate import failed: {type(exc).__name__}: {exc}", file=sys.__stderr__)
            return 1
        suite = unittest.defaultTestLoader.loadTestsFromTestCase(ArchiveContract)
        result = unittest.TextTestRunner(stream=sys.__stderr__, verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
