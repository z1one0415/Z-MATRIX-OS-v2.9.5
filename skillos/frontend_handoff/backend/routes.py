"""Routes — ALL endpoints are GET-only.

POST / PUT / PATCH / DELETE return a 405 BLOCKED payload.
"""

from flask import Blueprint, jsonify, request

from . import config
from .errors import blocked_response
from .service import service

api = Blueprint("api", __name__, url_prefix="/api")

# ── helper: mutation catches ────────────────────────────────────────────────

_READONLY_MSG = "readonly_disabled_default"


def _blocked():
    return blocked_response(request.method)


# ── mutation blocker for every route (decorator pattern) ────────────────────

def _ensure_get():
    """If the current request is NOT a GET, immediately return BLOCKED."""
    if request.method != "GET":
        return blocked_response(request.method)
    return None  # proceed


# ── GET endpoints ───────────────────────────────────────────────────────────

@api.route("/health", methods=["GET"])
def health():
    return jsonify(service.get_health())


@api.route("/version", methods=["GET"])
def version():
    return jsonify(service.get_version())


@api.route("/dashboard/summary", methods=["GET"])
def dashboard_summary():
    return jsonify(service.get_dashboard_summary())


@api.route("/capabilities", methods=["GET"])
def capabilities():
    return jsonify(service.get_capabilities())


@api.route("/factor-library/summary", methods=["GET"])
def factor_library_summary():
    return jsonify(service.get_factor_library_summary())


@api.route("/composition-graph/summary", methods=["GET"])
def composition_graph_summary():
    return jsonify(service.get_composition_graph_summary())


@api.route("/research-report/summary", methods=["GET"])
def research_report_summary():
    return jsonify(service.get_research_report_summary())


@api.route("/z9-review/summary", methods=["GET"])
def z9_review_summary():
    return jsonify(service.get_z9_review_summary())


@api.route("/evidence-chain", methods=["GET"])
def evidence_chain():
    return jsonify(service.get_evidence_chain())


@api.route("/run-state", methods=["GET"])
def run_state():
    return jsonify(service.get_run_state())


@api.route("/gate-state", methods=["GET"])
def gate_state():
    return jsonify(service.get_gate_state())


@api.route("/audit-trail", methods=["GET"])
def audit_trail():
    return jsonify(service.get_audit_trail())


@api.route("/frontend/routes", methods=["GET"])
def frontend_routes():
    return jsonify(service.get_frontend_routes())


@api.route("/frontend/contracts", methods=["GET"])
def frontend_contracts():
    return jsonify(service.get_frontend_contracts())


# ── mutation catchers: POST / PUT / PATCH / DELETE → 405 BLOCKED ──────────

_MUTATION_METHODS = ["POST", "PUT", "PATCH", "DELETE"]
_ALL_GET_PATHS = [
    "/health", "/version", "/dashboard/summary", "/capabilities",
    "/factor-library/summary", "/composition-graph/summary",
    "/research-report/summary", "/z9-review/summary",
    "/evidence-chain", "/run-state", "/gate-state",
    "/audit-trail", "/frontend/routes", "/frontend/contracts",
]


def _register_mutation_blockers():
    """Register POST/PUT/PATCH/DELETE handlers for every GET path to return BLOCKED."""
    for path in _ALL_GET_PATHS:
        for method in _MUTATION_METHODS:
            # Build unique endpoint name
            safe = path.lstrip("/").replace("/", "_").replace("-", "_")
            ep_name = f"blocked_{safe}_{method.lower()}"
            # Register via add_url_rule to avoid clashing function names
            api.add_url_rule(
                path,
                endpoint=ep_name,
                methods=[method],
                view_func=lambda m=method: blocked_response(m),
            )


_register_mutation_blockers()
