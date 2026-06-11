#!/usr/bin/env python3
"""test_frontend_handoff_smoke.py — Import all modules, verify contracts parse, backend loads.

Phase: A6 QA/Release — E2E Smoke Test
"""

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SKILLOS = ROOT / "skillos" / "frontend_handoff"


def test_import_backend_app():
    """Flask app imports cleanly."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.backend.app import app
    assert app is not None


def test_import_backend_config():
    """Config module imports and has expected attributes."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.backend import config
    assert config.PORT == 5500
    assert config.DISABLED_DEFAULT is True
    assert config.READONLY_MODE is True


def test_import_backend_routes():
    """Routes blueprint imports cleanly."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.backend.routes import api
    assert api is not None


def test_import_backend_service():
    """Service module imports cleanly."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.backend.service import service
    assert service is not None


def test_import_backend_fixtures():
    """Fixtures module imports with all expected data dicts."""
    sys.path.insert(0, str(ROOT))
    import skillos.frontend_handoff.backend.fixtures as f
    expected = [
        "HEALTH", "VERSION_INFO", "DASHBOARD_SUMMARY", "CAPABILITIES",
        "FACTOR_LIBRARY_SUMMARY", "COMPOSITION_GRAPH_SUMMARY",
        "RESEARCH_REPORT_SUMMARY", "Z9_REVIEW_SUMMARY", "EVIDENCE_CHAIN",
        "RUN_STATE", "GATE_STATE", "AUDIT_TRAIL", "FRONTEND_ROUTES",
        "FRONTEND_CONTRACTS",
    ]
    for name in expected:
        assert hasattr(f, name), f"Fixtures missing {name}"
        val = getattr(f, name)
        assert isinstance(val, dict), f"Fixture {name} is not a dict"


def test_import_permission_guard():
    """Permission guard imports and has expected API."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.auth.permission_guard import (
        check_permission, list_roles, list_permissions, list_dangerous_permissions,
    )
    roles = list_roles()
    assert len(roles) == 6
    perms = list_permissions()
    assert len(perms) == 15
    dang = list_dangerous_permissions()
    assert len(dang) == 5


def test_import_state_registry_loader():
    """State registry loader imports cleanly."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.state_registry.registry_loader import (
        load_gate_state_chain, load_evidence_chain,
    )
    assert callable(load_gate_state_chain)
    assert callable(load_evidence_chain)


def test_import_release_version():
    """Version module imports with correct values."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.release.version import VERSION, BASE_COMMIT
    assert VERSION == "v0.1.0-rc"
    assert BASE_COMMIT == "1f20dc1b"


def test_all_contracts_valid_json():
    """Every JSON file in contracts/ parses as valid JSON."""
    contracts_dir = SKILLOS / "contracts"
    json_files = sorted(contracts_dir.glob("*.json"))
    assert len(json_files) >= 5, f"Expected >= 5 contracts, found {len(json_files)}"
    for fpath in json_files:
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name} is not valid JSON object/array"


def test_all_auth_files_valid_json():
    """Every JSON file in auth/ parses as valid JSON."""
    auth_dir = SKILLOS / "auth"
    json_files = sorted(auth_dir.glob("*.json"))
    assert len(json_files) >= 2, f"Expected >= 2 auth json files, found {len(json_files)}"
    for fpath in json_files:
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name} is not valid JSON object/array"


def test_all_fixtures_valid_json():
    """Every JSON file in fixtures/ parses as valid JSON."""
    fixtures_dir = SKILLOS / "fixtures"
    json_files = sorted(fixtures_dir.glob("*.json"))
    assert len(json_files) >= 5, f"Expected >= 5 fixture files, found {len(json_files)}"
    for fpath in json_files:
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name} is not valid JSON object/array"


def test_observability_schemas_valid_json():
    """Every JSON file in observability/ parses as valid JSON."""
    obs_dir = SKILLOS / "observability"
    json_files = sorted(obs_dir.glob("*.json"))
    assert len(json_files) >= 3, f"Expected >= 3 observability schemas, found {len(json_files)}"
    for fpath in json_files:
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name} is not valid JSON object/array"


def test_state_registry_schemas_valid_json():
    """Every JSON file in state_registry/ parses as valid JSON."""
    sr_dir = SKILLOS / "state_registry"
    json_files = sorted(sr_dir.glob("*.json"))
    assert len(json_files) >= 3, f"Expected >= 3 state registry schemas, found {len(json_files)}"
    for fpath in json_files:
        with open(fpath, "r") as f:
            data = json.load(f)
        assert isinstance(data, (dict, list)), f"{fpath.name} is not valid JSON object/array"


def test_flask_app_test_client_works():
    """Flask test client returns health check."""
    sys.path.insert(0, str(ROOT))
    from skillos.frontend_handoff.backend.app import app
    app.config["TESTING"] = True
    with app.test_client() as client:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"
        assert data["version"] == "v0.1.0-rc"
