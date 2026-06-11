"""
registry_fixtures.py — Static fixture data for all gate states.

Provides fixture generators for gate state, evidence chain, run state,
and event log data suitable for schema validation and frontend demo.

All fixtures are read-only — consumed by the frontend handoff API layer.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent  # Z-MATRIX-OS root

FIXTURE_DIR = ROOT / "tests" / "skillos" / "frontend_handoff" / "state_registry"


def load_fixture(filename: str) -> Dict[str, Any]:
    """Load a fixture JSON file from the test fixtures directory."""
    path = FIXTURE_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"Fixture not found: {path}")
    return json.loads(path.read_text())


def fixture_gate_state_demo() -> Dict[str, Any]:
    """Load the gate_state_demo.json fixture (F7.2 gate chain).

    This fixture contains the complete F7.2 decision gate chain
    with correct statuses derived from audited commits.
    """
    return load_fixture("gate_state_demo.json")


def fixture_evidence_chain_demo() -> Dict[str, Any]:
    """Generate a minimal evidence chain fixture for testing."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "chain_id": "F7.2-evidence-chain",
        "generated_at": now,
        "nodes": [
            {
                "node_id": "ev-F7.2-decision-001",
                "hash": "a" * 64,
                "hash_algorithm": "SHA-256",
                "source_class": "DECISION_GATE",
                "no_real_source_flag": False,
                "linked_gate_id": "F7.2-decision-gate",
                "artifact_path": "runtime_reports/research/factors/f7_2_decision_gate.json",
                "commit_sha": "03c8de6e",
                "description": "F7.2 final decision gate",
                "verified_at": now,
                "verification_status": "VERIFIED"
            }
        ],
        "root_hash": "b" * 64
    }


def fixture_run_state_demo() -> Dict[str, Any]:
    """Generate a minimal run state fixture for testing."""
    return {
        "run_id": "RUN-20260612-001",
        "pipeline_name": "F7.2-formal-validation",
        "status": "COMPLETED",
        "created_at": "2026-06-12T00:00:00Z",
        "started_at": "2026-06-12T00:01:00Z",
        "completed_at": "2026-06-12T00:05:00Z",
        "duration_seconds": 240.0,
        "stages": [],
        "runtime_enabled": False,
        "runner_enabled": False,
        "commit_sha": "03c8de6e",
        "tags": ["F7.2", "validation", "readonly"]
    }


def fixture_event_log_demo() -> Dict[str, Any]:
    """Generate a minimal event log fixture for testing."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "generated_at": now,
        "events": [
            {
                "event_id": "EVT-001",
                "timestamp": "2026-06-05T00:00:00Z",
                "action": "gate_passed",
                "source": "A3-state-evidence-registry",
                "result": "MERGED_AND_SEALED",
                "gate_id": "F7.2-decision-gate",
                "commit_sha": "03c8de6e",
                "details": "F7.2 decision gate passed and sealed",
                "evidence_refs": ["ev-F7.2-decision-001"],
                "user_triggered": True
            }
        ],
        "total_events": 1
    }


def blocked_actions_matrix() -> Dict[str, List[str]]:
    """Return a gate_id -> blocked_actions mapping for all F7.2 gates.

    This is used by the blocked_actions test to verify that all
    blocked_actions lists are non-empty and promotion is disabled
    everywhere in the chain.
    """
    return {
        "F7.0-logical-reconcile": [],
        "F7.2-planning-review": ["factor_promotion", "alpha_claim", "production_deploy"],
        "F7.2-execution-plan": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
        "F7.2-execution-auth": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
        "F7.2-final-exec-auth": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
        "F7.2-human-val-auth": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
        "F7.2-val-readonly": ["factor_promotion", "alpha_claim", "production_deploy"],
        "F7.2-val-audit": ["factor_promotion", "alpha_claim", "production_deploy"],
        "F7.2-safety-patch": ["factor_promotion", "alpha_claim", "production_deploy"],
        "F7.2-human-interpret": ["factor_promotion", "alpha_claim", "production_deploy"],
        "F7.2-decision-gate": ["factor_promotion", "alpha_claim", "production_deploy", "paper_trading"],
    }
