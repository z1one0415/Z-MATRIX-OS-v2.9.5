#!/usr/bin/env python3
"""V13.F2.3.2 — Stage H: rework closeout."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def load_json(name):
    p = RUNTIME / name
    return json.loads(p.read_text()) if p.exists() else {}

readiness = load_json("f06_extended_sample_readiness_validation.json")

f06_ready = readiness.get("ready_for_revalidation", False)
f06_sample = readiness.get("sample_month_count", 0)

if f06_ready:
    recommended_next_action = "PREPARE_V13_F2_3_3_F06_REVALIDATION_EXECUTION"
elif f06_sample >= 1:
    recommended_next_action = "PREPARE_F03R_SEPARATE_MATERIALIZATION_GATE_OR_FIX_F06_DATA_HISTORY"
else:
    recommended_next_action = "FIX_FACTOR_REWORK_BLOCKERS"

closeout = {
    "pipeline_signature": "Z2-V13-F2-3-2-REWORK-CLOSEOUT",
    "status": "V13_F2_3_2_REWORK_PASS" if f06_ready else "V13_F2_3_2_REWORK_BLOCKED",
    "v13_f2_3_2_executed": True,
    "f06_sample_extension_executed": True,
    "f06_ready_for_revalidation": f06_ready,
    "f06_sample_month_count_after_extension": f06_sample,
    "f03r_materialization_planning_built": True,
    "f03r_materialized": False,
    "f03r_validated": False,
    "ready_for_next_validation": ["F06"] if f06_ready else [],
    "ready_for_promotion_review": [],
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
    "recommended_next_action": recommended_next_action
}

dst = RUNTIME / "v13_f2_3_2_rework_closeout.json"
dst.write_text(json.dumps(closeout, indent=2))
print(f"[F2.3.2-H] Rework closeout built -> {dst}")
print(f"  F06 sample: {f06_sample}/12 months, ready: {f06_ready}")
print(f"  Next: {recommended_next_action}")
sys.exit(0)
