"""Stage A: Build V13.F5.5.2 First Partial Monitoring Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-2-FIRST-PARTIAL-MONITORING-CONTRACT",
    "status": "V13_F5_5_2_FIRST_PARTIAL_MONITORING_CONTRACT_BUILT",
    "base_commit": "e7d7b1f",
    "monitoring_execution_scope": "MICRO_SAMPLE_PARTIAL_DIAGNOSTIC_ONLY",
    "label_month": "2026-05",
    "rebalance_date": "2026-05-06",
    "allowed_horizons": ["5D", "20D"],
    "blocked_horizons": ["60D"],
    "monitoring_scope": ["F04", "F10", "F11", "F14", "F15", "F16",
                         "F21", "F24", "F30", "F31"],
    "minimum_label_rows_required": 1,
    "formal_oos_validation_allowed": False,
    "candidate_state_update_allowed": False,
    "suspension_decision_allowed": False,
    "rejection_decision_allowed": False,
    "promotion_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "v13_6_allowed": False,
    "paper_trading_allowed": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

out_path = OUT / "v13_f5_5_2_first_partial_monitoring_contract.json"
out_path.write_text(json.dumps(contract, indent=2) + "\n")
print(f"Written: {out_path}")
