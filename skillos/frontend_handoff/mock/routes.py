"""
routes.py — Mock API routes matching A1 API schema for SkillOS Frontend Handoff RC.

All endpoints serve fixture JSON from skillos/frontend_handoff/fixtures/.
No real computation, no state mutation, no trade/order/position content.
"""

import json
import os
from flask import jsonify, Response


def _load_fixture(filename):
    """Load a JSON fixture file from the fixtures directory."""
    fixture_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "fixtures", filename)
    with open(fixture_path, "r", encoding="utf-8") as f:
        return json.load(f)


def _json_response(data, status=200):
    """Return a Flask JSON response with proper headers."""
    return Response(
        json.dumps(data, ensure_ascii=False, indent=2),
        status=status,
        mimetype="application/json",
        headers={"X-Mock-Server": "A5-SkillOS-Frontend-Handoff-RC"}
    )


def register_routes(app):
    """Register all mock API routes on the Flask app."""

    @app.route("/api/v1/health")
    def health():
        return _json_response({
            "status": "OK",
            "timestamp_utc": "2026-06-12T04:03:00Z",
            "uptime_sec": 86400
        })

    @app.route("/api/v1/version")
    def version():
        return _json_response({
            "version": "v2.9.6-draft",
            "branch": "agent/a5-frontend-mock-fixtures",
            "build_utc": "2026-06-12T03:00:00Z"
        })

    @app.route("/api/v1/dashboard/summary")
    def dashboard_summary():
        return _json_response(_load_fixture("dashboard_summary.json"))

    @app.route("/api/v1/capabilities")
    def capability_list():
        return _json_response(_load_fixture("capability_list.json"))

    @app.route("/api/v1/factors/summary")
    def factor_library_summary():
        return _json_response(_load_fixture("factor_library_summary.json"))

    @app.route("/api/v1/composition-graph/summary")
    def composition_graph_summary():
        return _json_response(_load_fixture("composition_graph_summary.json"))

    @app.route("/api/v1/research/report-summary")
    def research_report_summary():
        return _json_response(_load_fixture("research_report_summary.json"))

    @app.route("/api/v1/z9/review-summary")
    def z9_review_summary():
        return _json_response(_load_fixture("z9_review_summary.json"))

    @app.route("/api/v1/evidence/chain-demo")
    def evidence_chain_demo():
        return _json_response(_load_fixture("evidence_chain_demo.json"))

    @app.route("/api/v1/pipeline/run-state")
    def run_state_demo():
        return _json_response(_load_fixture("run_state_demo.json"))

    @app.route("/api/v1/gates/state")
    def gate_state_demo():
        return _json_response(_load_fixture("gate_state_demo.json"))

    @app.route("/api/v1/audit/trail")
    def audit_trail_demo():
        return _json_response(_load_fixture("audit_trail_demo.json"))

    @app.route("/api/v1/demo/error-abort-degraded")
    def error_abort_degraded_demo():
        return _json_response(_load_fixture("error_abort_degraded_demo.json"))

    # 404 handler for non-existent endpoints
    @app.errorhandler(404)
    def not_found(e):
        return _json_response({
            "error": "NOT_FOUND",
            "message": "Endpoint not implemented in mock server",
            "available_endpoints": [
                "/api/v1/health",
                "/api/v1/version",
                "/api/v1/dashboard/summary",
                "/api/v1/capabilities",
                "/api/v1/factors/summary",
                "/api/v1/composition-graph/summary",
                "/api/v1/research/report-summary",
                "/api/v1/z9/review-summary",
                "/api/v1/evidence/chain-demo",
                "/api/v1/pipeline/run-state",
                "/api/v1/gates/state",
                "/api/v1/audit/trail",
                "/api/v1/demo/error-abort-degraded",
            ]
        }, status=404)
