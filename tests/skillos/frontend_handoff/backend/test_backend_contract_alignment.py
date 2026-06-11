"""Test: response schemas match declared API schema contracts.

Every GET endpoint response must contain all keys declared in its schema
and the value types must be compatible.
"""

import json

import pytest

from skillos.frontend_handoff.backend.app import app
from skillos.frontend_handoff.backend.schemas import ENDPOINT_SCHEMAS


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


# Map endpoint key → URL path
SCHEMA_TO_PATH = {
    "health": "/api/health",
    "version": "/api/version",
    "dashboard/summary": "/api/dashboard/summary",
    "capabilities": "/api/capabilities",
    "factor-library/summary": "/api/factor-library/summary",
    "composition-graph/summary": "/api/composition-graph/summary",
    "research-report/summary": "/api/research-report/summary",
    "z9-review/summary": "/api/z9-review/summary",
    "evidence-chain": "/api/evidence-chain",
    "run-state": "/api/run-state",
    "gate-state": "/api/gate-state",
    "audit-trail": "/api/audit-trail",
    "frontend/routes": "/api/frontend/routes",
    "frontend/contracts": "/api/frontend/contracts",
}


def _type_matches(value, expected_type) -> bool:
    """Check if value is compatible with expected_type."""
    if expected_type is list:
        return isinstance(value, list)
    if expected_type is dict:
        return isinstance(value, dict)
    return isinstance(value, expected_type)


@pytest.mark.parametrize("schema_key", sorted(ENDPOINT_SCHEMAS.keys()))
def test_endpoint_matches_schema(client, schema_key):
    """Every endpoint's response must contain all schema keys with compatible types."""
    path = SCHEMA_TO_PATH[schema_key]
    schema_fn = ENDPOINT_SCHEMAS[schema_key]
    expected_schema = schema_fn()

    resp = client.get(path)
    assert resp.status_code == 200, f"{path} → {resp.status_code}"
    data = resp.get_json()

    for key, expected_type in expected_schema.items():
        assert key in data, f"{path} missing key '{key}' in response"
        assert _type_matches(data[key], expected_type), (
            f"{path} key '{key}': expected {expected_type.__name__}, "
            f"got {type(data[key]).__name__} (value={data[key]!r})"
        )


def test_all_schema_keys_have_paths():
    """Ensure every schema key in ENDPOINT_SCHEMAS maps to a URL."""
    for key in ENDPOINT_SCHEMAS:
        assert key in SCHEMA_TO_PATH, f"Schema key '{key}' has no mapped URL path"


def test_contract_count():
    """Frontend contracts must list all 12 endpoints."""
    with app.test_client() as c:
        resp = c.get("/api/frontend/contracts")
    data = resp.get_json()
    contracts = data["contracts"]
    # 12 backend API endpoints
    assert len(contracts) == 12, f"Expected 12 contracts, got {len(contracts)}"


def test_frontend_routes_count():
    """Frontend routes must list 7 pages."""
    with app.test_client() as c:
        resp = c.get("/api/frontend/routes")
    data = resp.get_json()
    routes = data["routes"]
    assert len(routes) == 7, f"Expected 7 frontend routes, got {len(routes)}"
