"""
V13 F5.1.20 Human Acceptance & F5.2 Candidate Review Decision Prep — Comprehensive Test
========================================================================================
Covers Steps 1-4 of V13.F5.1.20 implementation:
  Step 1: f5_1_20_human_acceptance (contract, post-merge audit, decision)
  Step 2: f5_1_19_1_registry_post_merge_canonicalization (closeout)
  Step 3: f5_1_20_human_acceptance (acceptance seal, boundary audit)
  Step 4: f5_2_candidate_review_decision (contract, input audit, prep closeout)
  Registry: updated state
"""
import json
import os
import sys
from pathlib import Path

# Resolve repo root
REPO_ROOT = Path(__file__).resolve().parents[4]
REVIEWS_BASE = REPO_ROOT / "research" / "factor_library" / "reviews" / "batch_003"
REGISTRY_PATH = REPO_ROOT / "research" / "factor_library" / "registry.json"

# --- File existence catalog ---
EXPECTED_FILES = [
    # Step 1
    REVIEWS_BASE / "f5_1_20_human_acceptance" / "v13_f5_1_20_human_review_contract.json",
    REVIEWS_BASE / "f5_1_20_human_acceptance" / "v13_f5_1_20_clean_target_post_merge_audit.json",
    REVIEWS_BASE / "f5_1_20_human_acceptance" / "v13_f5_1_20_human_review_decision.json",
    # Step 2
    REVIEWS_BASE / "f5_1_19_1_registry_post_merge_canonicalization" / "v13_f5_1_19_1_registry_canonicalization_closeout.json",
    # Step 3
    REVIEWS_BASE / "f5_1_20_human_acceptance" / "v13_f5_1_20_clean_target_human_acceptance_seal.json",
    REVIEWS_BASE / "f5_1_20_human_acceptance" / "v13_f5_1_20_acceptance_boundary_audit.json",
    # Step 4
    REVIEWS_BASE / "f5_2_candidate_review_decision" / "v13_f5_2_batch3_candidate_review_decision_contract.json",
    REVIEWS_BASE / "f5_2_candidate_review_decision" / "v13_f5_2_batch3_candidate_review_input_audit.json",
    REVIEWS_BASE / "f5_2_candidate_review_decision" / "v13_f5_2_batch3_candidate_review_decision_prep_closeout.json",
    # Registry
    REGISTRY_PATH,
]


def load_json(path: Path) -> dict:
    with open(path) as f:
        return json.load(f)


def test_all_files_exist():
    """All expected output files must exist."""
    missing = [str(p) for p in EXPECTED_FILES if not p.exists()]
    assert not missing, f"Missing files: {missing}"


def test_all_json_valid():
    """Every file must be valid JSON."""
    for p in EXPECTED_FILES:
        try:
            load_json(p)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            raise AssertionError(f"Invalid JSON or missing: {p} — {e}")


# ─── Step 1 assertions ────────────────────────────────────────────────────────

def test_step1_human_review_contract():
    data = load_json(EXPECTED_FILES[0])
    assert data["pipeline_signature"] == "Z2-V13-F5-1-20-HUMAN-REVIEW-CLEAN-TARGET-CONTRACT"
    assert data["status"] == "V13_F5_1_20_HUMAN_REVIEW_CONTRACT_BUILT"
    assert data["base_clean_target_head"] == "b9dd7b5"
    assert data["runner_enabled"] is False
    assert data["execution_allowed"] is False
    assert data["production"] == "BLOCKED"
    assert data["broker_runtime"] == "BLOCKED"
    assert data["real_trade"] == "BLOCKED"
    assert data["human_review_required"] is True
    assert "0c2e655" in data["invalid_commits_excluded"]


def test_step1_post_merge_audit():
    data = load_json(EXPECTED_FILES[1])
    assert data["status"] == "V13_F5_1_20_CLEAN_TARGET_POST_MERGE_AUDIT_PASS"
    assert data["violation_count"] == 0
    checks = data["checks"]
    assert checks["head_is_b9dd7b5"] is True
    assert checks["no_pycache"] is True
    assert checks["no_broker"] is True
    assert checks["runner_enabled_false"] is True
    assert checks["production_blocked"] is True


def test_step1_human_review_decision():
    data = load_json(EXPECTED_FILES[2])
    assert data["status"] == "V13_F5_1_20_HUMAN_REVIEW_CLEAN_TARGET_ACCEPTED"
    assert data["clean_target_accepted"] is True
    assert data["accepted_clean_target_head"] == "b9dd7b5"
    assert data["production"] == "BLOCKED"
    assert data["broker_runtime"] == "BLOCKED"
    assert data["real_trade"] == "BLOCKED"


# ─── Step 2 assertions ────────────────────────────────────────────────────────

def test_step2_registry_canonicalization():
    data = load_json(EXPECTED_FILES[3])
    assert data["status"] == "V13_F5_1_19_1_REGISTRY_POST_MERGE_CANONICALIZATION_PASS"
    assert data["canonicalization_executed"] is True
    assert data["registry_merge_executed"] is True
    assert data["registry_clean_target_head"] == "b9dd7b5"
    assert set(data["frozen_candidates_preserved"]) == {"F04", "F10", "F11", "F14", "F15", "F16"}
    assert set(data["rejected_factors_preserved"]) == {"F02", "F03", "F05"}
    assert data["production"] == "BLOCKED"
    assert data["runner_enabled"] is False


# ─── Step 3 assertions ────────────────────────────────────────────────────────

def test_step3_acceptance_seal():
    data = load_json(EXPECTED_FILES[4])
    assert data["status"] == "V13_F5_1_20_CLEAN_TARGET_HUMAN_ACCEPTANCE_SEALED"
    assert data["accepted_clean_target_head"] == "b9dd7b5"
    assert data["accepted_merge_commit"] == "9d63225"
    assert data["clean_target_human_accepted"] is True
    assert data["registry_post_merge_canonicalized"] is True
    assert data["runner_enabled"] is False
    assert data["execution_allowed"] is False
    assert data["production"] == "BLOCKED"
    assert data["broker_runtime"] == "BLOCKED"
    assert data["real_trade"] == "BLOCKED"
    assert data["next_legal_entry"] == "PREPARE_V13_F5_2_BATCH3_CANDIDATE_REVIEW_DECISION"


def test_step3_boundary_audit():
    data = load_json(EXPECTED_FILES[5])
    assert data["status"] == "V13_F5_1_20_ACCEPTANCE_BOUNDARY_AUDIT_PASS"
    assert data["violation_count"] == 0
    checks = data["checks"]
    assert checks["no_runner_enabled"] is True
    assert checks["no_execution_allowed"] is True
    assert checks["no_broker_trading_execution_real_trade"] is True
    assert checks["no_skillos_adapter"] is True


# ─── Step 4 assertions ────────────────────────────────────────────────────────

def test_step4_candidate_review_contract():
    data = load_json(EXPECTED_FILES[6])
    assert data["status"] == "V13_F5_2_BATCH3_CANDIDATE_REVIEW_DECISION_CONTRACT_BUILT"
    assert data["base_clean_target_head"] == "b9dd7b5"
    assert set(data["candidate_review_scope"]) == {"F21", "F22", "F24", "F26", "F27", "F30", "F31", "F34"}
    assert data["candidate_review_execution_allowed_next"] is True
    assert data["current_step_executes_candidate_review"] is False
    assert data["runner_enabled"] is False
    assert data["production"] == "BLOCKED"


def test_step4_input_audit():
    data = load_json(EXPECTED_FILES[7])
    assert data["status"] == "V13_F5_2_BATCH3_CANDIDATE_REVIEW_INPUT_AUDIT_PASS"
    assert data["violation_count"] == 0
    checks = data["checks"]
    assert checks["f5_1_20_acceptance_seal_exists"] is True
    assert checks["f5_1_20_acceptance_seal_status"] == "V13_F5_1_20_CLEAN_TARGET_HUMAN_ACCEPTANCE_SEALED"
    assert checks["no_promotion"] is True
    assert checks["no_skillos_adapter"] is True


def test_step4_prep_closeout():
    data = load_json(EXPECTED_FILES[8])
    assert data["status"] == "V13_F5_2_BATCH3_CANDIDATE_REVIEW_DECISION_PREP_PASS"
    assert data["human_acceptance_seal_verified"] is True
    assert data["ready_to_execute_f5_2_candidate_review"] is True
    assert data["candidate_review_executed"] is False
    assert data["runner_enabled"] is False
    assert data["execution_allowed"] is False
    assert data["production"] == "BLOCKED"
    assert data["broker_runtime"] == "BLOCKED"
    assert data["real_trade"] == "BLOCKED"


# ─── Registry assertions ──────────────────────────────────────────────────────

def test_registry_state():
    reg = load_json(REGISTRY_PATH)
    assert reg["next_legal_entry"] == "PREPARE_V13_F5_2_BATCH3_CANDIDATE_REVIEW_DECISION"
    assert reg["merge_executed"] is True
    assert reg["merge_verification_passed"] is True
    assert reg["clean_target_head"] == "b9dd7b5"
    assert reg["merge_commit"] == "9d63225"
    assert reg["post_merge_seal_commit"] == "b9dd7b5"
    assert reg["clean_target_post_merge_sealed"] is True
    assert reg["human_review_required"] is True
    assert reg["production"] == "BLOCKED"
    assert reg["broker_runtime"] == "BLOCKED"
    assert reg["real_trade"] == "BLOCKED"
    assert reg["runner_enabled"] is False
    assert reg["execution_allowed"] is False
    assert reg["alpha_claim_allowed"] is False


# ─── Boundary checks ─────────────────────────────────────────────────────────

def test_boundary_no_blocked_field_missing():
    """Every output file that has production/broker_runtime/real_trade must be BLOCKED."""
    blocked_fields = {"production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"}
    for p in EXPECTED_FILES:
        data = load_json(p)
        for field, expected in blocked_fields.items():
            if field in data:
                assert data[field] == expected, f"{p.name}: {field} should be {expected}, got {data[field]}"


def test_boundary_runner_and_execution_disabled():
    """Every file with runner_enabled/execution_allowed must have them False."""
    for p in EXPECTED_FILES:
        data = load_json(p)
        if "runner_enabled" in data:
            assert data["runner_enabled"] is False, f"{p.name}: runner_enabled must be False"
        if "execution_allowed" in data:
            assert data["execution_allowed"] is False, f"{p.name}: execution_allowed must be False"


def test_boundary_no_pycache_or_pyc():
    """No __pycache__ or .pyc files should exist in the reviews output directories."""
    for d in [
        REVIEWS_BASE / "f5_1_20_human_acceptance",
        REVIEWS_BASE / "f5_1_19_1_registry_post_merge_canonicalization",
        REVIEWS_BASE / "f5_2_candidate_review_decision",
    ]:
        for root, dirs, files in os.walk(d):
            assert "__pycache__" not in dirs, f"__pycache__ found in {root}"
            for f in files:
                assert not f.endswith(".pyc"), f".pyc file found: {os.path.join(root, f)}"


if __name__ == "__main__":
    import pytest
    sys.exit(pytest.main([__file__, "-v"]))
