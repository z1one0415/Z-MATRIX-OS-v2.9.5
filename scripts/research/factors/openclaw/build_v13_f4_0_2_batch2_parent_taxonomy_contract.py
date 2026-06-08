#!/usr/bin/env python3
"""V13.F4.0.2 — Stage A: taxonomy contract."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
(B2 / "v13_f4_0_2_batch2_parent_taxonomy_contract.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-2-BATCH2-PARENT-TAXONOMY-CONTRACT",
    "status": "V13_F4_0_2_BATCH2_PARENT_TAXONOMY_CONTRACT_BUILT",
    "base_commit": "90958a2b", "canonicalization_only": True,
    "expected_lanes_from_contract": 7,
    "frozen_candidates_preserved": ["F04","F10","F11"],
    "f3_5_1_monitoring_execution_allowed": False,
    "f3_6_true_oos_validation_allowed": False,
    "source_audit_group_taxonomy_fix_required": True,
    "lane_count_consistency_required": True,
    "f17_f20_group_must_not_be_coverage_blocked": True,
    "multi_factor_composite_built": False, "alpha_claim_allowed": False,
    "production": "BLOCKED", "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print("[F4.0.2-A] Taxonomy contract built")
sys.exit(0)
