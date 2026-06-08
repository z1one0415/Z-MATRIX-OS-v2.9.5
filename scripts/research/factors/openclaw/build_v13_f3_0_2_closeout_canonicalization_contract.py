#!/usr/bin/env python3
"""V13.F3.0.2 — Stage A: canonicalization contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
BATCH = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch"
(BATCH / "v13_f3_0_2_closeout_canonicalization_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F3-0-2-CLOSEOUT-CANONICALIZATION-CONTRACT",
    "status": "V13_F3_0_2_CLOSEOUT_CANONICALIZATION_CONTRACT_BUILT",
    "base_commit": "6b80553", "canonicalization_only": True,
    "materialization_rerun_allowed": False, "single_factor_validation_rerun_allowed": False,
    "target_parent_artifacts": [
        "v13_f3_0_child_evidence_consistency_audit.json",
        "v13_f3_0_1_parallel_batch_merge_report.json",
        "v13_f3_0_1_parallel_batch_safety_audit.json",
        "v13_f3_0_1_parallel_batch_repair_closeout.json"
    ],
    "canonical_after_repair_source": "recomputed_child_closeouts",
    "pre_repair_audit_must_not_drive_after_repair_status": True,
    "multi_factor_composite_built": False, "v13_6_allowed": False,
    "paper_trading_allowed": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F3.0.2-A] Canonicalization contract built")
sys.exit(0)
