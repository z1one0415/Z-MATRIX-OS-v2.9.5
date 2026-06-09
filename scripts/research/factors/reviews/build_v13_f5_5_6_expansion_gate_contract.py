"""Stage A: V13.F5.5.6 Expansion Gate Contract."""
import json
from pathlib import Path
OUT = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
OUT.mkdir(parents=True, exist_ok=True)
c = {
    "pipeline_signature": "Z2-V13-F5-5-6-MONITORING-SAMPLE-EXPANSION-GATE-CONTRACT",
    "status": "V13_F5_5_6_EXPANSION_GATE_CONTRACT_BUILT",
    "base_commit": "7cc8a76",
    "planning_only": True,
    "current_sample_scope": "MICRO_SAMPLE_5_TICKERS_1_MONTH",
    "current_signal_ready_factors": ["F04","F10","F11","F21","F24","F30","F31"],
    "blocked_factors": ["F14","F15","F16"],
    "minimum_formal_ticker_count": 475,
    "minimum_formal_oos_months": 6,
    "preferred_formal_oos_months": 12,
    "formal_oos_validation_allowed": False,
    "sample_expansion_execution_allowed": False,
    "new_label_generation_allowed": False,
    "new_signal_generation_allowed": False,
    "monitoring_execution_allowed": False,
    "candidate_state_update_allowed": False,
    "promotion_allowed": False,
    "alpha_claim_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}
(OUT / "v13_f5_5_6_expansion_gate_contract.json").write_text(json.dumps(c, indent=2) + "\n")
print("Written: expansion gate contract")
