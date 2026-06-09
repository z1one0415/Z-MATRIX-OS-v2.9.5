#!/usr/bin/env python3
"""V13.F6.2.1 — Generate closeout JSON."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_2_1_fundamental_signal_canonicalization")

def main():
    closeout = {
        "pipeline_signature": "Z2-V13-F6-2-1-FUNDAMENTAL-SIGNAL-CANONICALIZATION-CLOSEOUT",
        "timestamp": datetime.now(TZ).isoformat(),
        "status": "V13_F6_2_1_FUNDAMENTAL_SIGNAL_CANONICALIZATION_PASS",
        "base_commit": "3df60ce",
        "fundamental_signal_rows": 28,
        "fundamental_ticker_count": 4,
        "price_label_ticker_count": 5,
        "excluded_tickers": ["588000"],
        "exclusion_reason": {
            "588000": "ETF_NO_CORPORATE_FUNDAMENTALS"
        },
        "materialized_factors": ["F06","F07","F08","F12","F13","F14","F15"],
        "informative_factors": ["F06","F07","F08","F12","F14","F15"],
        "non_informative_factors": ["F13"],
        "f13_status": "MATERIALIZED_NON_INFORMATIVE",
        "f13_reason": "all_equal_zero_shareholder_yield",
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
        "recommended_next_action": "PREPARE_V13_F6_3_REMAINING_DIMENSION_LANE_COMPLETION"
    }
    
    (OUT / "v13_f6_2_1_closeout.json").write_text(
        json.dumps(closeout, indent=2, ensure_ascii=False))
    print(f"✅ {OUT / 'v13_f6_2_1_closeout.json'}")

if __name__ == "__main__":
    main()
