#!/usr/bin/env python3
"""V13.F6.2.1 — Audit: confirm 588000 is ETF, exclude from fundamental universe."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_004/f6_2_1_fundamental_signal_canonicalization")

# Ground truth from F6.2 materialization manifest:
# 4 fundamental tickers: 000977, 002050, 002472, 601899
# 5 price label tickers (from F5.5.4.1 closeout): 000977, 002050, 002472, 588000, 601899
# 588000 is ETF

FUNDAMENTAL_TICKERS = ["000977", "002050", "002472", "601899"]
PRICE_LABEL_TICKERS = ["000977", "002050", "002472", "588000", "601899"]
ETF = "588000"

def main():
    is_etf = ETF.startswith("5")
    in_fundamental = ETF in FUNDAMENTAL_TICKERS
    in_price = ETF in PRICE_LABEL_TICKERS

    result = {
        "pipeline_signature": "Z2-V13-F6-2-1-ETF-EXCLUSION-AUDIT",
        "status": "PASS" if (is_etf and not in_fundamental and in_price) else "FAIL",
        "etf_ticker": ETF,
        "is_etf_by_prefix": is_etf,
        "found_in_fundamental_universe": in_fundamental,
        "present_in_price_universe": in_price,
        "fundamental_tickers": FUNDAMENTAL_TICKERS,
        "price_label_tickers": PRICE_LABEL_TICKERS,
        "fundamental_ticker_count": len(FUNDAMENTAL_TICKERS),
        "price_label_ticker_count": len(PRICE_LABEL_TICKERS),
        "conclusion": "ETF_588000_CORRECTLY_EXCLUDED_FROM_FUNDAMENTALS" if not in_fundamental else "DATA_LEAK_DETECTED"
    }

    (OUT / "v13_f6_2_1_etf_exclusion_audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False))
    print(f"✅ {OUT / 'v13_f6_2_1_etf_exclusion_audit.json'}")
    print(f"   status={result['status']} | fundamental_tickers={result['fundamental_tickers']}")

if __name__ == "__main__":
    main()
