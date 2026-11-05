"""Map report actions and domain failures to API responses."""

from . import reports


def handle(action, report, provider, request_id):
    """Run a report action and return its public status and response body."""
    operations = {
        "publish": reports.publish_report,
        "archive": reports.archive_report,
    }
    if action not in operations:
        return {"status": 404, "body": {"error": "unknown action"}}
    try:
        result = operations[action](report, provider, request_id)
    except reports.InvalidState:
        return {"status": 409, "body": {"error": "report must be ready"}}
    except reports.ArchiveUnavailable:
        return {"status": 503, "body": {"error": "archive unavailable"}}
    return {"status": 200, "body": {
        "report_id": result.id, "state": result.state, "archive_id": result.archive_id,
    }}
