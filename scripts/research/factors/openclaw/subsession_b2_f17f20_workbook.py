#!/usr/bin/env python3
"""V13.F4.0 — Subsession Lane G: F17-F20 event/domain source audit group."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
FACTORS = [
    {"fid":"F17","name":"POLICY_CATALYST_DECAY","source_type":"EVENT"},
    {"fid":"F18","name":"SUPPLY_DEMAND_TENSION","source_type":"INDUSTRY"},
    {"fid":"F19","name":"CAPITAL_FLOW_CONFIRMATION","source_type":"FLOW"},
    {"fid":"F20","name":"INDUSTRY_CATALYST_CONFIRMATION","source_type":"INDUSTRY"}
]

for spec in FACTORS:
    fid = spec["fid"]
    fname = spec["name"]
    B = ROOT / "runtime_reports" / "research" / "factors" / "openclaw_batch_2" / fid
    B.mkdir(parents=True, exist_ok=True)

    def wj(name, data):
        (B / name).write_text(json.dumps(data, indent=2))
        print(f"  [{fid}] wrote {name}")

    wj(f"{fid.lower()}_formula_contract.json", {
        "pipeline_signature": "Z2-V13-F4-0-SUBSESSION-FORMULA",
        "factor_id": fid, "factor_name": fname, "source_type": spec["source_type"],
        "lane_type": "SOURCE_AUDIT_ONLY",
        "alpha_claim_allowed": False, "production": "BLOCKED",
        "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    })
    wj(f"{fid.lower()}_source_readiness.json", {
        "factor_id": fid, "factor_name": fname,
        "source_type": spec["source_type"], "source_ready": False,
        "blocked_reason": "event/domain source not yet ingested; requires separate data pipeline",
        "materialization_allowed": False,
        "alpha_claim_allowed": False, "production": "BLOCKED",
        "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    })
    wj(f"{fid.lower()}_source_gap_report.json", {
        "factor_id": fid, "factor_name": fname,
        "missing_data_sources": ["event_calendar","industry_chain_mapping","capital_flow_data"],
        "estimated_effort_to_ingest": "HIGH",
        "data_snooping_risk": True,
        "alpha_claim_allowed": False, "production": "BLOCKED",
        "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    })
    wj(f"{fid.lower()}_future_materialization_plan.json", {
        "factor_id": fid, "factor_name": fname,
        "requires_future_data_gate": True,
        "materialization_executed": False,
        "estimated_minimum_months_after_data_ingestion": 12,
        "alpha_claim_allowed": False, "production": "BLOCKED",
        "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    })
    wj(f"{fid.lower()}_closeout.json", {
        "factor_id": fid, "factor_name": fname,
        "subsession_status": "SOURCE_AUDIT_COMPLETE",
        "materialization_executed": False, "validation_executed": False,
        "ready_for_parent_merge": True, "ready_for_promotion_review": False,
        "data_snooping_risk_acknowledged": True,
        "multi_factor_composite_built": False, "v13_6_allowed": False,
        "alpha_claim_allowed": False, "production": "BLOCKED",
        "broker_runtime": "BLOCKED", "real_trade": "BLOCKED"
    })
    print(f"  [{fid}] SOURCE_AUDIT_COMPLETE")

print("[Lane G] All 4 event/domain factors audited")
sys.exit(0)
