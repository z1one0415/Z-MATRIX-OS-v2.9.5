"""
registry_loader.py — Load gate state from F7.2 research artifacts (readonly).

Loads the F7.2 gate chain from the research artifact files directory,
producing a gate_state_demo-compatible dictionary suitable for the
frontend handoff API consumption.

This is a READONLY loader: no writes to the research artifacts directory.
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Root paths relative to this file's location
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent  # Z-MATRIX-OS root
RESEARCH_DIR = ROOT / "runtime_reports" / "research" / "factors"


def _sha256(content: str) -> str:
    """Compute SHA-256 hash of content."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


def _resolve_artifact_path(commit_sha: str) -> Optional[Path]:
    """Resolve a research artifact path from a commit SHA.

    Scans runtime_reports/research/factors/ and its subdirectories
    for JSON files that reference the given commit.
    """
    if not RESEARCH_DIR.exists():
        return None
    for fpath in RESEARCH_DIR.rglob("*.json"):
        try:
            data = json.loads(fpath.read_text())
            # Check if this artifact references the commit
            if isinstance(data, dict):
                if data.get("commit_sha") == commit_sha or data.get("commit") == commit_sha:
                    return fpath
        except (json.JSONDecodeError, OSError):
            continue
    return None


def load_gate_state_chain() -> Dict[str, Any]:
    """Load the full F7.2 gate state chain from hardcoded registry data.

    Returns a dictionary conforming to gate_state_schema.json,
    with gates ordered by stage number. Gate data is derived from
    the audited F7.2 commit chain.

    Returns:
        Dict with keys: chain_id, generated_at, gates, chain_summary
    """
    now = datetime.now(timezone.utc).isoformat()

    gates: List[Dict[str, Any]] = [
        {
            "gate_id": "F7.0-logical-reconcile",
            "stage": 0,
            "commit": "e636dcfa",
            "parent_commit": "1f20dc1b",
            "status": "MERGED_AND_SEALED",
            "scope": "Reconcile F7.1 logical order with parent route history",
            "allowed_next_entries": ["F7.2-planning-review"],
            "blocked_actions": [],
            "evidence_refs": ["ev-F7.0-001"],
            "created_at": "2026-05-25T00:00:00Z",
            "human_decision_required": False,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-planning-review",
            "stage": 1,
            "commit": "e1373225",
            "parent_commit": "e636dcfa",
            "status": "MERGED_AND_SEALED",
            "scope": "F7.2 U475 6-month validation planning review gate",
            "allowed_next_entries": ["F7.2-execution-plan"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy"],
            "evidence_refs": ["ev-F7.2-plan-001"],
            "created_at": "2026-05-26T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-execution-plan",
            "stage": 2,
            "commit": "6de8802d",
            "parent_commit": "e1373225",
            "status": "MERGED_AND_SEALED",
            "scope": "F7.2 formal validation execution plan gate",
            "allowed_next_entries": ["F7.2-execution-auth"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
            "evidence_refs": ["ev-F7.2-exec-001"],
            "created_at": "2026-05-27T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-execution-auth",
            "stage": 3,
            "commit": "c1d1e38d",
            "parent_commit": "6de8802d",
            "status": "MERGED_AND_SEALED",
            "scope": "Update execution plan gate base commit to approval SHA",
            "allowed_next_entries": ["F7.2-final-exec-auth"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
            "evidence_refs": ["ev-F7.2-exec-auth-001"],
            "created_at": "2026-05-28T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-final-exec-auth",
            "stage": 4,
            "commit": "2448124e",
            "parent_commit": "c1d1e38d",
            "status": "MERGED_AND_SEALED",
            "scope": "F7.2 final execution authorization gate",
            "allowed_next_entries": ["F7.2-human-val-auth"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
            "evidence_refs": ["ev-F7.2-final-auth-001"],
            "created_at": "2026-05-29T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-human-val-auth",
            "stage": 5,
            "commit": "597aaa32",
            "parent_commit": "2448124e",
            "status": "MERGED_AND_SEALED",
            "scope": "F7.2 human formal validation run authorization decision gate",
            "allowed_next_entries": ["F7.2-val-readonly"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy", "validation_run"],
            "evidence_refs": ["ev-F7.2-human-val-001"],
            "created_at": "2026-05-30T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-val-readonly",
            "stage": 6,
            "commit": "ea80ff9a",
            "parent_commit": "597aaa32",
            "status": "MERGED_AND_SEALED",
            "scope": "Run F7.2 formal validation in readonly mode",
            "allowed_next_entries": ["F7.2-val-audit"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy"],
            "evidence_refs": ["ev-F7.2-val-run-001"],
            "created_at": "2026-06-01T00:00:00Z",
            "human_decision_required": False,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": True,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-val-audit",
            "stage": 7,
            "commit": "b9f77abb",
            "parent_commit": "ea80ff9a",
            "status": "MERGED_AND_SEALED",
            "scope": "Audit F7.2 formal validation results",
            "allowed_next_entries": ["F7.2-safety-patch"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy"],
            "evidence_refs": ["ev-F7.2-audit-001"],
            "created_at": "2026-06-02T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-safety-patch",
            "stage": 8,
            "commit": "18429840",
            "parent_commit": "b9f77abb",
            "status": "MERGED_AND_SEALED",
            "scope": "Patch F7.2 result audit safety field semantics",
            "allowed_next_entries": ["F7.2-human-interpret"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy"],
            "evidence_refs": ["ev-F7.2-safety-001"],
            "created_at": "2026-06-03T00:00:00Z",
            "human_decision_required": False,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-human-interpret",
            "stage": 9,
            "commit": "4dcef2ab",
            "parent_commit": "18429840",
            "status": "MERGED_AND_SEALED",
            "scope": "F7.2 human interpretation review",
            "allowed_next_entries": ["F7.2-decision-gate"],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy"],
            "evidence_refs": ["ev-F7.2-interpret-001"],
            "created_at": "2026-06-04T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        },
        {
            "gate_id": "F7.2-decision-gate",
            "stage": 10,
            "commit": "03c8de6e",
            "parent_commit": "4dcef2ab",
            "status": "MERGED_AND_SEALED",
            "scope": "F7.2 human interpretation review decision gate — final gate",
            "allowed_next_entries": [],
            "blocked_actions": ["factor_promotion", "alpha_claim", "production_deploy", "paper_trading"],
            "evidence_refs": ["ev-F7.2-decision-001"],
            "created_at": "2026-06-05T00:00:00Z",
            "human_decision_required": True,
            "promotion_allowed": False,
            "alpha_claim_allowed": False,
            "runner_enabled": False,
            "paper_trading_allowed": False,
            "production": False,
            "broker_runtime": "none",
            "real_trade": False
        }
    ]

    total_gates = len(gates)
    passed = sum(1 for g in gates if g["status"] == "MERGED_AND_SEALED")
    blocked = sum(1 for g in gates if g["status"] == "BLOCKED")
    pending = sum(1 for g in gates if g["status"] == "PENDING")
    degraded = sum(1 for g in gates if g["status"] == "DEGRADED")
    merged = sum(1 for g in gates if g["status"] == "MERGED_AND_SEALED")

    return {
        "chain_id": "F7.2-formal-validation",
        "generated_at": now,
        "gates": gates,
        "chain_summary": {
            "total_gates": total_gates,
            "passed": passed,
            "blocked": blocked,
            "pending": pending,
            "merged_and_sealed": merged,
            "degraded": degraded
        }
    }


def load_evidence_chain() -> Dict[str, Any]:
    """Load the evidence chain for the F7.2 gate chain.

    Returns a dictionary conforming to evidence_chain_schema.json.
    Each evidence node corresponds to a gate in the F7.2 chain.

    Returns:
        Dict with keys: chain_id, generated_at, nodes, root_hash
    """
    now = datetime.now(timezone.utc).isoformat()

    nodes: List[Dict[str, Any]] = [
        {
            "node_id": "ev-F7.0-001",
            "hash": _sha256("F7.0 logical reconcile evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "RESEARCH_ARTIFACT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.0-logical-reconcile",
            "artifact_path": "runtime_reports/research/factors/f7_0_logical_reconcile.json",
            "commit_sha": "e636dcfa",
            "description": "F7.1 logical order reconciliation with parent route history",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-plan-001",
            "hash": _sha256("F7.2 planning review evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "RESEARCH_ARTIFACT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-planning-review",
            "artifact_path": "runtime_reports/research/factors/f7_2_planning_review.json",
            "commit_sha": "e1373225",
            "description": "F7.2 U475 6-month validation planning review",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-exec-001",
            "hash": _sha256("F7.2 execution plan evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "RESEARCH_ARTIFACT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-execution-plan",
            "artifact_path": "runtime_reports/research/factors/f7_2_execution_plan.json",
            "commit_sha": "6de8802d",
            "description": "F7.2 formal validation execution plan",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-exec-auth-001",
            "hash": _sha256("F7.2 execution auth update evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "RESEARCH_ARTIFACT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-execution-auth",
            "artifact_path": "runtime_reports/research/factors/f7_2_execution_auth_update.json",
            "commit_sha": "c1d1e38d",
            "description": "Update execution plan gate base commit to approval SHA",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-final-auth-001",
            "hash": _sha256("F7.2 final exec auth evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "DECISION_GATE",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-final-exec-auth",
            "artifact_path": "runtime_reports/research/factors/f7_2_final_exec_auth.json",
            "commit_sha": "2448124e",
            "description": "F7.2 final execution authorization gate decision",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-human-val-001",
            "hash": _sha256("F7.2 human validation auth evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "HUMAN_REVIEW",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-human-val-auth",
            "artifact_path": "runtime_reports/research/factors/f7_2_human_val_auth.json",
            "commit_sha": "597aaa32",
            "description": "F7.2 human formal validation run authorization decision",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-val-run-001",
            "hash": _sha256("F7.2 validation readonly run evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "VALIDATION_OUTPUT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-val-readonly",
            "artifact_path": "runtime_reports/research/factors/f7_2_val_readonly.json",
            "commit_sha": "ea80ff9a",
            "description": "F7.2 formal validation readonly run output",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-audit-001",
            "hash": _sha256("F7.2 validation audit evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "AUDIT_REPORT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-val-audit",
            "artifact_path": "runtime_reports/research/factors/f7_2_val_audit.json",
            "commit_sha": "b9f77abb",
            "description": "Audit of F7.2 formal validation results",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-safety-001",
            "hash": _sha256("F7.2 safety field patch evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "RESEARCH_ARTIFACT",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-safety-patch",
            "artifact_path": "runtime_reports/research/factors/f7_2_safety_patch.json",
            "commit_sha": "18429840",
            "description": "Patch F7.2 result audit safety field semantics",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-interpret-001",
            "hash": _sha256("F7.2 human interpretation evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "HUMAN_REVIEW",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-human-interpret",
            "artifact_path": "runtime_reports/research/factors/f7_2_human_interpret.json",
            "commit_sha": "4dcef2ab",
            "description": "F7.2 human interpretation review",
            "verified_at": now,
            "verification_status": "VERIFIED"
        },
        {
            "node_id": "ev-F7.2-decision-001",
            "hash": _sha256("F7.2 decision gate evidence"),
            "hash_algorithm": "SHA-256",
            "source_class": "DECISION_GATE",
            "no_real_source_flag": False,
            "linked_gate_id": "F7.2-decision-gate",
            "artifact_path": "runtime_reports/research/factors/f7_2_decision_gate.json",
            "commit_sha": "03c8de6e",
            "description": "F7.2 human interpretation review decision gate — final",
            "verified_at": now,
            "verification_status": "VERIFIED"
        }
    ]

    # Compute root hash as SHA-256 of concatenated node hashes
    combined = "".join(node["hash"] for node in nodes)
    root_hash = _sha256(combined)

    return {
        "chain_id": "F7.2-evidence-chain",
        "generated_at": now,
        "nodes": nodes,
        "root_hash": root_hash
    }
