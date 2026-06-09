"""Stage A: Build V13.F5.5.3.1 Signal Materialization Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_1_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-3-1-SIGNAL-MATERIALIZATION-CONTRACT",
    "status": "V13_F5_5_3_1_SIGNAL_MATERIALIZATION_CONTRACT_BUILT",
    "base_commit": "d9895da",
    "materialization_scope": "MINIMAL_LABEL_TICKERS_ONLY",
    "eligible_factors": ["F21", "F24", "F30", "F31"],
    "blocked_factors": ["F04", "F10", "F11", "F14", "F15", "F16",
                        "F22", "F26", "F27", "F34"],
    "rebalance_date": "2026-05-06",
    "label_tickers_only": True,
    "full_universe_computation_allowed": False,
    "feature_store_write_allowed": False,
    "runtime_reports_write_allowed": False,
    "monitoring_rerun_allowed": False,
    "candidate_state_update_allowed": False,
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

out_path = OUT / "v13_f5_5_3_1_signal_materialization_contract.json"
out_path.write_text(json.dumps(contract, indent=2) + "\n")
print(f"Written: {out_path}")
