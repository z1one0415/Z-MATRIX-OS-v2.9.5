"""Static fixture data for the readonly backend shell.

All data is hard-coded placeholder content matching the frontend contracts.
No file I/O, no database — pure in-memory dicts.
"""

from datetime import datetime, timezone


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# ---------------------------------------------------------------------------
# /api/health
# ---------------------------------------------------------------------------
HEALTH = {
    "status": "ok",
    "version": "v0.1.0-rc",
}

# ---------------------------------------------------------------------------
# /api/version
# ---------------------------------------------------------------------------
VERSION_INFO = {
    "version": "v0.1.0-rc",
    "build": "a2-backend-readonly-shell",
    "timestamp": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/dashboard/summary
# ---------------------------------------------------------------------------
DASHBOARD_SUMMARY = {
    "modules": [
        {"id": "factor-library", "label": "Factor Library", "status": "ready"},
        {"id": "composition-graph", "label": "Composition Graph", "status": "ready"},
        {"id": "research-report", "label": "Research Report", "status": "ready"},
        {"id": "z9-review", "label": "Z9 Review", "status": "ready"},
        {"id": "evidence-chain", "label": "Evidence Chain", "status": "ready"},
    ],
    "pipeline_state": "idle",
    "last_updated": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/capabilities
# ---------------------------------------------------------------------------
CAPABILITIES = {
    "frontend": {
        "routes": ["/", "/dashboard", "/factor-library", "/composition-graph",
                   "/research-report", "/z9-review", "/evidence-chain"],
        "framework": "React",
    },
    "backend": {
        "mode": "readonly",
        "mutations_blocked": True,
    },
}

# ---------------------------------------------------------------------------
# /api/factor-library/summary
# ---------------------------------------------------------------------------
FACTOR_LIBRARY_SUMMARY = {
    "factors": [
        {"name": "momentum", "weight": 0.20, "status": "active"},
        {"name": "quality", "weight": 0.18, "status": "active"},
        {"name": "value", "weight": 0.15, "status": "active"},
        {"name": "growth", "weight": 0.12, "status": "active"},
        {"name": "volatility", "weight": 0.10, "status": "active"},
        {"name": "sentiment", "weight": 0.10, "status": "active"},
        {"name": "liquidity", "weight": 0.08, "status": "active"},
        {"name": "size", "weight": 0.07, "status": "active"},
    ],
    "total_factors": 8,
    "last_calibrated": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/composition-graph/summary
# ---------------------------------------------------------------------------
COMPOSITION_GRAPH_SUMMARY = {
    "nodes": [
        {"id": "N1", "label": "Data Ingest"},
        {"id": "N2", "label": "Factor Calculation"},
        {"id": "N3", "label": "Score Aggregation"},
        {"id": "N4", "label": "Ranking"},
        {"id": "N5", "label": "Output"},
    ],
    "edges": [
        {"from": "N1", "to": "N2"},
        {"from": "N2", "to": "N3"},
        {"from": "N3", "to": "N4"},
        {"from": "N4", "to": "N5"},
    ],
    "pipeline": "default",
}

# ---------------------------------------------------------------------------
# /api/research-report/summary
# ---------------------------------------------------------------------------
RESEARCH_REPORT_SUMMARY = {
    "report_id": "RR-0000-EXAMPLE",
    "title": "Placeholder Research Report",
    "sections": ["macro", "sector", "candidates", "risk"],
    "generated_at": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/z9-review/summary
# ---------------------------------------------------------------------------
Z9_REVIEW_SUMMARY = {
    "review_id": "Z9-0000-EXAMPLE",
    "status": "pending",
    "items_reviewed": 0,
    "findings": [],
    "timestamp": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/evidence-chain
# ---------------------------------------------------------------------------
EVIDENCE_CHAIN = {
    "chain_id": "EC-0000-EXAMPLE",
    "links": [
        {"level": "A", "label": "Hard Financial Data", "status": "placeholder"},
        {"level": "B", "label": "Sector Positioning", "status": "placeholder"},
        {"level": "C", "label": "Thematic Alignment", "status": "placeholder"},
        {"level": "D", "label": "Market Narrative", "status": "placeholder"},
    ],
    "timestamp": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/run-state
# ---------------------------------------------------------------------------
RUN_STATE = {
    "pipeline": "z-skillos-frontend-handoff",
    "state": "idle",
    "last_run": None,
    "next_scheduled": None,
}

# ---------------------------------------------------------------------------
# /api/gate-state
# ---------------------------------------------------------------------------
GATE_STATE = {
    "truth_gate": "closed",
    "confirmation_gate": "closed",
    "active_flows": [],
}

# ---------------------------------------------------------------------------
# /api/audit-trail
# ---------------------------------------------------------------------------
AUDIT_TRAIL = {
    "entries": [],
    "total_entries": 0,
    "since": now_iso(),
}

# ---------------------------------------------------------------------------
# /api/frontend/routes
# ---------------------------------------------------------------------------
FRONTEND_ROUTES = {
    "routes": [
        {"path": "/", "component": "Dashboard"},
        {"path": "/dashboard", "component": "Dashboard"},
        {"path": "/factor-library", "component": "FactorLibrary"},
        {"path": "/composition-graph", "component": "CompositionGraph"},
        {"path": "/research-report", "component": "ResearchReport"},
        {"path": "/z9-review", "component": "Z9Review"},
        {"path": "/evidence-chain", "component": "EvidenceChain"},
    ],
}

# ---------------------------------------------------------------------------
# /api/frontend/contracts
# ---------------------------------------------------------------------------
FRONTEND_CONTRACTS = {
    "contracts": [
        {"endpoint": "/api/dashboard/summary", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/capabilities", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/factor-library/summary", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/composition-graph/summary", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/research-report/summary", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/z9-review/summary", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/evidence-chain", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/run-state", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/gate-state", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/audit-trail", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/frontend/routes", "method": "GET", "schema_version": "v0.1.0-rc"},
        {"endpoint": "/api/frontend/contracts", "method": "GET", "schema_version": "v0.1.0-rc"},
    ],
    "version": "v0.1.0-rc",
}
