#!/usr/bin/env python3
"""V13.F6.3 — Remaining dimension lane completion contract."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUTDIR = Path("research/factor_library/reviews/batch_004/f6_3_remaining_dimension_completion")
OUTDIR.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F6-3-REMAINING-DIMENSION-LANE-COMPLETION-CONTRACT",
    "status": "V13_F6_3_CONTRACT_BUILT",
    "timestamp": datetime.now(TZ).isoformat(),
    "base_commit": "9e7c083",
    "completed_upstream": ["F6.2","F6.2.1","F6.2.2"],
    "excluded_from_scope": ["F06","F07","F08","F12","F14","F15"],
    "target_lanes": {
        "E": {"factor": "F13", "goal": "shareholder_yield_variance_repair"},
        "F": {"factor": "F09", "goal": "earnings_revision_or_proxy"},
        "G": {"factor": "F41,F42", "goal": "industry_chain_evidence"},
        "H": {"factor": "F43-F46", "goal": "operating_cycle"},
        "I": {"factor": "F47-F49", "goal": "event_catalyst_decay"},
        "J": {"factor": "F50-F52", "goal": "policy_macro_risk"},
        "K": {"factor": "F16,F53-F55", "goal": "sentiment_attention_crowding"},
        "L": {"factor": "F56-F60", "goal": "money_flow_microstructure"}
    },
    "allowed_outcomes": ["MATERIALIZED","SOURCE_CONTRACT_ONLY","BLOCKED_BY_SOURCE_DATA","TAXONOMY_REVIEW_REQUIRED"],
    "formal_oos_validation_allowed": False,
    "candidate_state_update_allowed": False,
    "promotion_allowed": False,
    "alpha_claim_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

outfile = OUTDIR / "v13_f6_3_remaining_dimension_contract.json"
outfile.write_text(json.dumps(contract, indent=2, ensure_ascii=False))
print(f"✅ F6.3 contract: {outfile}")
