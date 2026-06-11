"""Error and degraded-response helpers for the readonly backend shell."""

from flask import jsonify


def blocked_response(method: str):
    """Return a 405 BLOCKED payload for any mutation method."""
    return jsonify({
        "status": "BLOCKED",
        "reason": "readonly_disabled_default",
        "method": method.upper(),
    }), 405


def degraded_response(endpoint: str, reason: str = "service_unavailable"):
    """Return a 200 with a degraded flag (dummy data from fixtures)."""
    return jsonify({
        "status": "degraded",
        "endpoint": endpoint,
        "reason": reason,
        "data": None,
    }), 200


def degraded_data_response(data: dict, endpoint: str):
    """Return 200 with degraded flag plus fixture data."""
    payload = {"status": "degraded", "endpoint": endpoint}
    payload.update(data)
    return jsonify(payload), 200
