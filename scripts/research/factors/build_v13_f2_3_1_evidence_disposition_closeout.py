#!/usr/bin/env python3
"""V13.F2.3.1 — Stage G: evidence disposition closeout."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

closeout = {
    "pipeline_signature": "Z2-V13-F2-3-1-DISPOSITION-CLOSEOUT",
    "status": "V13_F2_3_1_EVIDENCE_DISPOSITION_CLOSEOUT_PASS",
    "v13_f2_3_1_executed": True,
    "f03_disposition": "REJECTED_CURRENT_DIRECTION",
    "f03r_hypothesis_registered": True,
    "f03r_materialized": False,
    "f03r_validated": False,
    "f06_disposition": "BLOCKED_BY_INSUFFICIENT_SAMPLE",
    "f06_sample_extension_plan_built": True,
    "ready_for_f2_4_promotion_review": [],
    "promotion_review_allowed": False,
    "multi_factor_composite_built": False,
    "oos_alpha_validation_executed": False,
    "skillos_protocol_modified": False,
    "frontend_modified": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "ready_for_alpha_claim": False,
    "alpha_validated": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_F06_SAMPLE_EXTENSION_OR_F03R_HYPOTHESIS_MATERIALIZATION"
}

dst = RUNTIME / "v13_f2_3_1_evidence_disposition_closeout.json"
dst.write_text(json.dumps(closeout, indent=2))
print(f"[F2.3.1-G] Disposition closeout built -> {dst}")
sys.exit(0)
