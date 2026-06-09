#!/usr/bin/env python3
"""V13.F6.3 — Closeout: aggregate lane results."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUTDIR = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion")

lanes = {}
lane_dirs = [
    "lane_e_shareholder_yield_repair", "lane_f_earnings_revision",
    "lane_g_industry_chain_evidence", "lane_h_operating_cycle",
    "lane_i_event_catalyst_decay", "lane_j_policy_macro_risk",
    "lane_k_sentiment_attention_crowding", "lane_l_money_flow_microstructure"
]
for ld in lane_dirs:
    cp = OUTDIR / ld / "lane_closeout.json"
    if cp.exists():
        lanes[ld] = json.loads(cp.read_text())

def bucket(outcome):
    if outcome is None:
        return "unknown"
    if outcome.startswith("MATERIALIZED"):
        return "materialized"
    return outcome.lower()

materialized = [k for k,v in lanes.items() if v.get("outcome","").startswith("MATERIALIZED")]
source_only = [k for k,v in lanes.items() if v.get("outcome")=="SOURCE_CONTRACT_ONLY"]
blocked = [k for k,v in lanes.items() if v.get("outcome")=="BLOCKED_BY_SOURCE_DATA"]
taxonomy = [k for k,v in lanes.items() if v.get("outcome")=="TAXONOMY_REVIEW_REQUIRED"]

closeout = {
    "pipeline_signature": "Z2-V13-F6-3-REMAINING-DIMENSION-LANE-COMPLETION-CLOSEOUT",
    "status": "V13_F6_3_PARTIAL",
    "base_commit": "9e7c083",
    "timestamp": datetime.now(TZ).isoformat(),
    "lanes_executed": len(lanes),
    "excluded_completed_factors": ["F06","F07","F08","F12","F14","F15"],
    "materialized_lanes": materialized,
    "materialized_details": {k: lanes[k]["outcome"] for k in materialized},
    "source_contract_only": source_only,
    "blocked_lanes": blocked,
    "taxonomy_review_required": taxonomy,
    "monitoring_rerun_executed": False,
    "formal_oos_validation_executed": False,
    "candidate_state_update_executed": False,
    "promotion_allowed": False,
    "alpha_claim_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "recommended_next_action": "PREPARE_V13_F6_4_PARENT_MERGE_AND_STATUS_CANONICALIZATION"
}

outfile = OUTDIR / "v13_f6_3_remaining_dimension_closeout.json"
outfile.write_text(json.dumps(closeout, indent=2, ensure_ascii=False))
print(f"✅ F6.3 closeout: {outfile}")
print(f"   Materialized: {len(materialized)} ({materialized})")
print(f"   Source-only:  {len(source_only)} ({source_only})")
print(f"   Blocked:      {len(blocked)} ({blocked})")
print(f"   Taxonomy:     {len(taxonomy)} ({taxonomy})")
