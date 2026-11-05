"""Reproduce the failed archive that reports success and prevents retry."""

import unittest

from app.provider import ArchiveProvider, ProviderUnavailable
from app.reports import Report
from app.routes import handle


class ArchiveChecks(unittest.TestCase):
    def test_failed_archive_is_retryable(self):
        report = Report("report-7")
        provider = ArchiveProvider([ProviderUnavailable("provider timed out")])
        result = handle("archive", report, provider, "request-7")
        self.assertEqual(result["status"], 503)
        self.assertEqual(report.state, "ready")
        self.assertIsNone(report.archive_id)


if __name__ == "__main__":
    unittest.main()
