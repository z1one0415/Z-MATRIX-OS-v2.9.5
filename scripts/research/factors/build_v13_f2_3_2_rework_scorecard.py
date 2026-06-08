#!/usr/bin/env python3
"""V13.F2.3.2 — Stage G: rework scorecard."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"

def load_json(name):
    p = RUNTIME / name
    return json.loads(p.read_text()) if p.exists() else {}

readiness = load_json("f06_extended_sample_readiness_validation.json")
f03r = load_json("f03r_materialization_planning_contract.json")

f06_ready = readiness.get("ready_for_revalidation", False)
f06_sample = readiness.get("sample_month_count", 0)
f03r_planning = f03r.get("planning_only", False)

ready_for_validation = ["F06"] if f06_ready else []

scorecard = {
    "pipeline_signature": "Z2-V13-F2-3-2-REWORK-SCORECARD",
    "status": "V13_F2_3_2_REWORK_SCORECARD_BUILT",
    "f06_extension_attempted": True,
    "f06_ready_for_revalidation": f06_ready,
    "f06_sample_month_count_after_extension": f06_sample,
    "f03r_planning_built": f03r_planning,
    "f03r_materialized": False,
    "f03r_validated": False,
    "ready_for_next_validation": ready_for_validation,
    "ready_for_promotion_review": [],
    "multi_factor_composite_built": False,
    "oos_alpha_validation_executed": False,
    "v13_6_allowed": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "v13_f2_3_2_rework_scorecard.json"
dst.write_text(json.dumps(scorecard, indent=2))
print(f"[F2.3.2-G] Rework scorecard built -> {dst}")
sys.exit(0)
