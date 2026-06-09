"""Stage A: Build V13.F5.5.4.1 Batch1/Batch2 Signal Materialization Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_1_batch1_batch2_signal_materialization")
OUT.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-4-1-BATCH1-BATCH2-SIGNAL-MATERIALIZATION-CONTRACT",
    "status": "V13_F5_5_4_1_SIGNAL_MATERIALIZATION_CONTRACT_BUILT",
    "base_commit": "7384266",
    "materialization_scope": "MINIMAL_LABEL_TICKERS_ONLY",
    "target_factors": ["F04", "F10", "F11", "F14", "F15", "F16"],
    "already_signal_ready": ["F21", "F24", "F30", "F31"],
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

(OUT / "v13_f5_5_4_1_signal_materialization_contract.json").write_text(
    json.dumps(contract, indent=2) + "\n")
print("Written: contract")
