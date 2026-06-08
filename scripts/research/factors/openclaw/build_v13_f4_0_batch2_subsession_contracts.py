#!/usr/bin/env python3
"""V13.F4.0 — Stage D: batch 2 subsession contracts for 7 lanes.
Generates one JSON contract per lane and a combined registry."""
import json, csv, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
B2 = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2"
B2.mkdir(parents=True, exist_ok=True)

ALLOWED = ["formula_contract","source_readiness","materialization","pit_leakage_validation","coverage_validation","single_factor_validation","evidence_scorecard","closeout"]
FORBIDDEN = ["alpha_claim","promotion_review","multi_factor_composite","weight_optimization","v13_6","paper_trading","production","broker_runtime","real_trade"]
AUDIT_ONLY_ALLOWED = ["formula_contract","source_readiness","source_gap_report","future_materialization_plan","closeout"]

lanes_data = {
    "A": {"fid":"F05","name":"TURNOVER_STABILITY","type":"MATERIALIZATION_AND_VALIDATION"},
    "B": {"fid":"F02","name":"DOWNSIDE_VOL_ADJUSTED_STRENGTH","type":"MATERIALIZATION_AND_VALIDATION"},
    "C": {"fid":"F09","name":"EARNINGS_REVISION","type":"SOURCE_AUDIT_ONLY"},
    "D": {"fid":"F14","name":"ASSET_GROWTH_DISCIPLINE","type":"MATERIALIZATION_AND_VALIDATION"},
    "E": {"fid":"F15","name":"ACCRUALS_QUALITY","type":"MATERIALIZATION_AND_VALIDATION"},
    "F": {"fid":"F16","name":"SENTIMENT_ATTENTION","type":"MATERIALIZATION_AND_VALIDATION"},
    "G": {"fid":"F17_F20_GROUP","name":"EVENT_DOMAIN_SOURCE_AUDIT_GROUP","type":"SOURCE_AUDIT_ONLY"}
}

per_lane = []
for lid, spec in sorted(lanes_data.items()):
    is_audit = spec["type"] == "SOURCE_AUDIT_ONLY"
    contract = {
        "lane_id": lid, "factor_id": spec["fid"], "factor_name": spec["name"],
        "lane_type": spec["type"],
        "output_path": f"runtime_reports/research/factors/openclaw_batch_2/{spec['fid']}/",
        "allowed_actions": AUDIT_ONLY_ALLOWED if is_audit else ALLOWED,
        "forbidden_actions": FORBIDDEN + (["materialization","validation"] if is_audit else [])
    }
    per_lane.append(contract)
    # Create output dir
    (B2 / spec["fid"]).mkdir(parents=True, exist_ok=True)

(B2 / "v13_f4_0_batch2_subsession_contracts.json").write_text(json.dumps({
    "pipeline_signature": "Z2-V13-F4-0-BATCH2-SUBSESSION-CONTRACTS",
    "status": "V13_F4_0_BATCH2_SUBSESSION_CONTRACTS_BUILT",
    "batch2_subsession_count": len(per_lane),
    "subsession_contracts": per_lane,
    "alpha_claim_allowed": False, "production": "BLOCKED",
    "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
}, indent=2))
print(f"[F4.0-D] {len(per_lane)} subsession contracts built")
for c in per_lane:
    print(f"  Lane {c['lane_id']}: {c['factor_id']} {c['factor_name']} ({c['lane_type']})")
sys.exit(0)
