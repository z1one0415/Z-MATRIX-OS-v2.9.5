"""Stage A: Build V13.F5.5.1.2 Data Access Authorization Contract."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
OUT.mkdir(parents=True, exist_ok=True)

PRICE_BARS = Path("data/price_bars")

# Check if price_bars directory has actual data
data_files = list(PRICE_BARS.glob("*.csv"))
access_available = len(data_files) > 0 and any(f.stat().st_size > 100 for f in data_files)

contract = {
    "pipeline_signature": "Z2-V13-F5-5-1-2-DATA-ACCESS-AUTHORIZATION-CONTRACT",
    "status": "V13_F5_5_1_2_DATA_ACCESS_AUTHORIZATION_CONTRACT_BUILT",
    "base_commit": "db190ff",
    "read_only_price_data_access_requested": True,
    "read_only_price_data_access_allowed": access_available,
    "allowed_source": "data/price_bars",
    "allowed_label_month": "2026-05",
    "allowed_horizons": ["5D", "20D"],
    "blocked_horizons": ["60D"],
    "feature_store_write_allowed": False,
    "monitoring_execution_allowed": False,
    "candidate_decision_update_allowed": False,
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

out_path = OUT / "v13_f5_5_1_2_data_access_authorization_contract.json"
out_path.write_text(json.dumps(contract, indent=2) + "\n")
print(f"Written: {out_path}")
print(f"Access allowed: {access_available}")
