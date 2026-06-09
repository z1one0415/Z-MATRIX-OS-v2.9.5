"""Stage A: V13.F5.5.2.2 Seven-Factor Partial Monitoring Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-2-2-SEVEN-FACTOR-PARTIAL-MONITORING-CONTRACT",
    "status": "V13_F5_5_2_2_SEVEN_FACTOR_PARTIAL_MONITORING_CONTRACT_BUILT",
    "base_commit": "ac96790",
    "monitoring_scope": ["F04", "F10", "F11", "F21", "F24", "F30", "F31"],
    "blocked_factors": ["F14", "F15", "F16"],
    "ticker_count": 5,
    "label_rows": 10,
    "expected_signal_rows": 35,
    "label_month": "2026-05",
    "rebalance_date": "2026-05-06",
    "allowed_horizons": ["5D", "20D"],
    "blocked_horizons": ["60D"],
    "sample_scope": "MICRO_SAMPLE_5_TICKERS",
    "formal_oos_validation_allowed": False,
    "formal_statistical_inference_allowed": False,
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

(OUT / "v13_f5_5_2_2_seven_factor_partial_monitoring_contract.json").write_text(
    json.dumps(contract, indent=2) + "\n")
print("Written: contract")
