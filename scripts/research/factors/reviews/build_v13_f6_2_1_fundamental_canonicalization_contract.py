#!/usr/bin/env python3
"""V13.F6.2.1 — Generate fundamental canonicalization contract."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUTDIR = Path("research/factor_library/reviews/batch_004/f6_2_1_fundamental_signal_canonicalization")

def main():
    contract = {
        "pipeline_signature": "Z2-V13-F6-2-1-FUNDAMENTAL-CANONICALIZATION-CONTRACT",
        "timestamp": datetime.now(TZ).isoformat(),
        "base_commit": "3df60ce",
        "target_factors": ["F06","F07","F08","F12","F13","F14","F15"],
        "fundamental_ticker_universe": 4,
        "price_label_ticker_universe": 5,
        "etf_exclusion_rule": {
            "detection": "ticker_starts_with_5_or_is_etf",
            "588000": "ETF_NO_CORPORATE_FUNDAMENTALS",
            "action": "EXCLUDE_FROM_FUNDAMENTAL_UNIVERSE"
        },
        "universe_join_policy": {
            "inner_join": "fundamental ∩ price_label = 4 tickers (excludes 588000)",
            "join_key": "ticker",
            "rebalance_date": "2026-05-06",
            "missing_price_label": "skip_factor_for_that_ticker",
            "missing_fundamental": "mark_factor_BLOCKED_for_that_ticker"
        },
        "non_informative_factors": ["F13"],
        "f13_non_informative_reason": "all_tickers_zero_shareholder_yield_A_share_market",
        "real_trade": "BLOCKED",
    }
    outfile = OUTDIR / "v13_f6_2_1_fundamental_canonicalization_contract.json"
    outfile.parent.mkdir(parents=True, exist_ok=True)
    outfile.write_text(json.dumps(contract, indent=2, ensure_ascii=False))
    print(f"✅ {outfile}")

if __name__ == "__main__":
    main()
