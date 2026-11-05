"""Expose report actions to the local command caller."""

from .routes import handle


def run_command(action, report, provider, request_id):
    """Return the same result as the API for the requested report action."""
    return handle(action, report, provider, request_id)
