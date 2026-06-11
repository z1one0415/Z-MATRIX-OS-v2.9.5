"""Response schemas for all readonly backend endpoints.

Each function returns a typed dict describing the expected structure.
Used by tests to validate contract alignment.
"""


def health_schema() -> dict:
    return {
        "status": str,
        "version": str,
    }


def version_schema() -> dict:
    return {
        "version": str,
        "build": str,
        "timestamp": str,
    }


def dashboard_summary_schema() -> dict:
    return {
        "modules": list,
        "pipeline_state": str,
        "last_updated": str,
    }


def capabilities_schema() -> dict:
    return {
        "frontend": dict,
        "backend": dict,
    }


def factor_library_summary_schema() -> dict:
    return {
        "factors": list,
        "total_factors": int,
        "last_calibrated": str,
    }


def composition_graph_summary_schema() -> dict:
    return {
        "nodes": list,
        "edges": list,
        "pipeline": str,
    }


def research_report_summary_schema() -> dict:
    return {
        "report_id": str,
        "title": str,
        "sections": list,
        "generated_at": str,
    }


def z9_review_summary_schema() -> dict:
    return {
        "review_id": str,
        "status": str,
        "items_reviewed": int,
        "findings": list,
        "timestamp": str,
    }


def evidence_chain_schema() -> dict:
    return {
        "chain_id": str,
        "links": list,
        "timestamp": str,
    }


def run_state_schema() -> dict:
    return {
        "pipeline": str,
        "state": str,
        # last_run / next_scheduled may be None
    }


def gate_state_schema() -> dict:
    return {
        "truth_gate": str,
        "confirmation_gate": str,
        "active_flows": list,
    }


def audit_trail_schema() -> dict:
    return {
        "entries": list,
        "total_entries": int,
        "since": str,
    }


def frontend_routes_schema() -> dict:
    return {
        "routes": list,
    }


def frontend_contracts_schema() -> dict:
    return {
        "contracts": list,
        "version": str,
    }


# Map endpoint → schema function
ENDPOINT_SCHEMAS = {
    "health": health_schema,
    "version": version_schema,
    "dashboard/summary": dashboard_summary_schema,
    "capabilities": capabilities_schema,
    "factor-library/summary": factor_library_summary_schema,
    "composition-graph/summary": composition_graph_summary_schema,
    "research-report/summary": research_report_summary_schema,
    "z9-review/summary": z9_review_summary_schema,
    "evidence-chain": evidence_chain_schema,
    "run-state": run_state_schema,
    "gate-state": gate_state_schema,
    "audit-trail": audit_trail_schema,
    "frontend/routes": frontend_routes_schema,
    "frontend/contracts": frontend_contracts_schema,
}
