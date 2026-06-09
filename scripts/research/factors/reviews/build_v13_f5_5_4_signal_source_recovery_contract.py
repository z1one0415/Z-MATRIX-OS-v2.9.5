"""Stage A: Build V13.F5.5.4 Signal Source Recovery Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")
OUT.mkdir(parents=True, exist_ok=True)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-4-SIGNAL-SOURCE-RECOVERY-CONTRACT",
    "status": "V13_F5_5_4_SIGNAL_SOURCE_RECOVERY_CONTRACT_BUILT",
    "base_commit": "3f9f5ca",
    "planning_and_restoration_only": True,
    "target_factors": ["F04", "F10", "F11", "F14", "F15", "F16"],
    "already_signal_ready": ["F21", "F24", "F30", "F31"],
    "signal_score_generation_allowed": False,
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

out_path = OUT / "v13_f5_5_4_signal_source_recovery_contract.json"
out_path.write_text(json.dumps(contract, indent=2) + "\n")
print(f"Written: {out_path}")
