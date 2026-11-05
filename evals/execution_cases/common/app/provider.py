"""Provide a deterministic archive service for local checks."""

from __future__ import annotations


class ProviderUnavailable(RuntimeError):
    """Report that the archive service couldn't complete the request."""


class ArchiveProvider:
    """Return scripted receipts or failures without accessing a network."""

    def __init__(self, outcomes=()):
        self.outcomes = list(outcomes)
        self.calls = []

    def archive(self, report_id):
        """Return the provider receipt, or raise the next scripted exception."""
        self.calls.append(report_id)
        outcome = self.outcomes.pop(0) if self.outcomes else {"receipt": f"arc-{report_id}"}
        if isinstance(outcome, Exception):
            raise outcome
        return outcome
