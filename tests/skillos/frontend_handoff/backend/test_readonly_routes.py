"""Test: all declared GET endpoints return 200 with valid JSON."""

import json

import pytest

from skillos.frontend_handoff.backend.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# ── all GET endpoints that must return 200 ──────────────────────────────────

GET_ENDPOINTS = [
    "/api/health",
    "/api/version",
    "/api/dashboard/summary",
    "/api/capabilities",
    "/api/factor-library/summary",
    "/api/composition-graph/summary",
    "/api/research-report/summary",
    "/api/z9-review/summary",
    "/api/evidence-chain",
    "/api/run-state",
    "/api/gate-state",
    "/api/audit-trail",
    "/api/frontend/routes",
    "/api/frontend/contracts",
]


@pytest.mark.parametrize("endpoint", GET_ENDPOINTS)
def test_get_endpoint_returns_200(client, endpoint):
    resp = client.get(endpoint)
    assert resp.status_code == 200, f"{endpoint} returned {resp.status_code}"
    data = resp.get_json()
    assert isinstance(data, dict), f"{endpoint} response body is not JSON object"


def test_health_has_required_keys(client):
    resp = client.get("/api/health")
    data = resp.get_json()
    assert "status" in data
    assert "version" in data
    assert data["status"] == "ok"
    assert data["version"] == "v0.1.0-rc"


def test_version_has_required_keys(client):
    resp = client.get("/api/version")
    data = resp.get_json()
    assert "version" in data
    assert "build" in data
    assert "timestamp" in data


def test_dashboard_summary_has_modules(client):
    resp = client.get("/api/dashboard/summary")
    data = resp.get_json()
    assert "modules" in data
    assert isinstance(data["modules"], list)


def test_capabilities_has_frontend_backend(client):
    resp = client.get("/api/capabilities")
    data = resp.get_json()
    assert "frontend" in data
    assert "backend" in data


def test_factor_library_has_factors(client):
    resp = client.get("/api/factor-library/summary")
    data = resp.get_json()
    assert "factors" in data
    assert isinstance(data["factors"], list)


def test_composition_graph_has_nodes_edges(client):
    resp = client.get("/api/composition-graph/summary")
    data = resp.get_json()
    assert "nodes" in data
    assert "edges" in data


def test_research_report_has_keys(client):
    resp = client.get("/api/research-report/summary")
    data = resp.get_json()
    assert "report_id" in data
    assert "title" in data


def test_z9_review_has_keys(client):
    resp = client.get("/api/z9-review/summary")
    data = resp.get_json()
    assert "review_id" in data
    assert "status" in data


def test_evidence_chain_has_keys(client):
    resp = client.get("/api/evidence-chain")
    data = resp.get_json()
    assert "chain_id" in data
    assert "links" in data


def test_frontend_routes_has_routes(client):
    resp = client.get("/api/frontend/routes")
    data = resp.get_json()
    assert "routes" in data
    assert isinstance(data["routes"], list)


def test_frontend_contracts_has_contracts(client):
    resp = client.get("/api/frontend/contracts")
    data = resp.get_json()
    assert "contracts" in data
    assert "version" in data
