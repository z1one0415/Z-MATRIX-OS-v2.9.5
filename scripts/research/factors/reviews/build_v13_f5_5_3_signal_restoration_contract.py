"""Stage A: Build V13.F5.5.3 Signal Restoration Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")
OUT.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-3-SIGNAL-SCORE-RESTORATION-CONTRACT",
    "status": "V13_F5_5_3_SIGNAL_RESTORATION_CONTRACT_BUILT",
    "base_commit": "bfb48a7",
    "planning_only": True,
    "frozen_candidates": ["F04", "F10", "F11", "F14", "F15", "F16",
                          "F21", "F24", "F30", "F31"],
    "label_month": "2026-05",
    "label_ticker_count": 5,
    "current_signal_available_count": 0,
    "current_signal_blocked_count": 10,
    "factor_recalculation_allowed": False,
    "signal_materialization_allowed": False,
    "monitoring_rerun_allowed": False,
    "candidate_state_update_allowed": False,
    "promotion_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "v13_6_allowed": False,
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

out_path = OUT / "v13_f5_5_3_signal_restoration_contract.json"
out_path.write_text(json.dumps(contract, indent=2) + "\n")
print(f"Written: {out_path}")
