"""
test_mock_server_routes.py

Verify all mock server endpoints return 200.
Tests the Flask app directly (no live server needed).
"""

import json
import pytest
import sys
import os

# Resolve project root (go up 4 levels from tests/skillos/frontend_handoff/mock/)
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
MOCK_DIR = os.path.join(_PROJECT_ROOT, "skillos", "frontend_handoff", "mock")
sys.path.insert(0, MOCK_DIR)

from server import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# List of all expected endpoints that should return 200
ENDPOINTS = [
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


class TestAllEndpointsReturn200:
    @pytest.mark.parametrize("endpoint", ENDPOINTS)
    def test_endpoint_returns_200(self, client, endpoint):
        response = client.get(endpoint)
        assert response.status_code == 200, f"{endpoint} returned {response.status_code}"

    @pytest.mark.parametrize("endpoint", ENDPOINTS)
    def test_endpoint_returns_json(self, client, endpoint):
        response = client.get(endpoint)
        assert response.content_type == "application/json"
        data = json.loads(response.data)
        assert isinstance(data, dict)


class TestHealthEndpoint:
    def test_health_has_status(self, client):
        response = client.get("/api/v1/health")
        data = json.loads(response.data)
        assert data["status"] == "OK"


class TestVersionEndpoint:
    def test_version_has_fields(self, client):
        response = client.get("/api/v1/version")
        data = json.loads(response.data)
        assert "version" in data
        assert "branch" in data


class Test404Handling:
    def test_nonexistent_endpoint_returns_404(self, client):
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404

    def test_nonexistent_endpoint_lists_endpoints(self, client):
        response = client.get("/api/v1/nonexistent")
        data = json.loads(response.data)
        assert "available_endpoints" in data
        assert len(data["available_endpoints"]) >= len(ENDPOINTS)


class TestMockHeader:
    def test_mock_server_header(self, client):
        response = client.get("/api/v1/health")
        assert response.headers.get("X-Mock-Server") == "A5-SkillOS-Frontend-Handoff-RC"
