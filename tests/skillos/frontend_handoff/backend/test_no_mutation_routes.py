"""Test: POST/PUT/PATCH/DELETE on every known path returns 405 or BLOCKED."""

import pytest

from skillos.frontend_handoff.backend.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


ALL_PATHS = [
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

MUTATION_METHODS = ["POST", "PUT", "PATCH", "DELETE"]


@pytest.mark.parametrize("path", ALL_PATHS)
@pytest.mark.parametrize("method", MUTATION_METHODS)
def test_mutation_returns_blocked(client, path, method):
    """Every mutation method on every path must be blocked."""
    caller = getattr(client, method.lower())
    resp = caller(path)
    # Accept 405 (method not allowed) or a custom BLOCKED status
    assert resp.status_code in (405, 200), (
        f"{method} {path} returned unexpected {resp.status_code}"
    )

    data = resp.get_json()
    assert data is not None, f"{method} {path} returned non-JSON"
    # If 405, check the BLOCKED reason
    if resp.status_code == 405 and "status" in data:
        assert data["status"] == "BLOCKED"
        assert "reason" in data


def test_post_to_health_returns_blocked(client):
    resp = client.post("/api/health")
    assert resp.status_code in (405, 200)
    data = resp.get_json()
    assert data is not None
    # Must contain blocked indicator
    has_blocked = (
        data.get("status") == "BLOCKED"
        or resp.status_code == 405
    )
    assert has_blocked, f"POST /api/health not blocked: {data}"


def test_put_to_dashboard_returns_blocked(client):
    resp = client.put("/api/dashboard/summary")
    assert resp.status_code in (405, 200)


def test_delete_to_capabilities_returns_blocked(client):
    resp = client.delete("/api/capabilities")
    assert resp.status_code in (405, 200)


def test_patch_to_factor_library_returns_blocked(client):
    resp = client.patch("/api/factor-library/summary")
    assert resp.status_code in (405, 200)


def test_mutated_routes_never_return_2xx_success(client):
    """All mutation requests on GET endpoints must not return 2xx without blocked flag."""
    for path in ALL_PATHS:
        for method in MUTATION_METHODS:
            caller = getattr(client, method.lower())
            resp = caller(path)
            if resp.status_code in (200, 201):
                data = resp.get_json() or {}
                # If 200, must have blocked/degraded status
                assert data.get("status") in ("BLOCKED",), (
                    f"{method} {path} returned 200 without BLOCKED: {data}"
                )
