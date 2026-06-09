#!/usr/bin/env python3
"""V13.F6.2.1 — Build universe join policy: 4 fundamental ∩ 5 price = 4 inner join."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_004/f6_2_1_fundamental_signal_canonicalization")

def main():
    policy = {
        "pipeline_signature": "Z2-V13-F6-2-1-FUNDAMENTAL-UNIVERSE-JOIN-POLICY",
        "fundamental_tickers": ["000977","002050","002472","601899"],
        "price_label_tickers": ["000977","002050","002472","588000","601899"],
        "excluded_from_fundamental": {
            "588000": {
                "reason": "ETF",
                "detail": "tracked in price universe only; no corporate fundamentals exist"
            }
        },
        "join_key": "ticker",
        "inner_join_tickers": ["000977","002050","002472","601899"],
        "join_rules": {
            "fundamental_only": "ignored (no price signal to compare)",
            "price_only": "fundamental factors BLOCKED, price factors continue",
            "both": "full factor signal available"
        },
        "rebalance_date": "2026-05-06",
        "real_trade": "BLOCKED"
    }
    
    (OUT / "v13_f6_2_1_fundamental_universe_join_policy.json").write_text(
        json.dumps(policy, indent=2, ensure_ascii=False))
    print(f"✅ {OUT / 'v13_f6_2_1_fundamental_universe_join_policy.json'}")
    print(f"   inner_join={len(policy['inner_join_tickers'])} tickers | excluded={list(policy['excluded_from_fundamental'].keys())}")

if __name__ == "__main__":
    main()
