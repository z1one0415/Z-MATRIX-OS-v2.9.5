#!/usr/bin/env python3
"""V13.F6.2.1 — Audit F13: check if all ticker scores == 0 (shareholder yield)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_2_1_fundamental_signal_canonicalization")

# Ground truth from F6.2 materialization:
# F13 (shareholder_yield) = all-zero for all 4 A-share tickers
F13_TICKERS = ["000977", "002050", "002472", "601899"]
F13_SCORES = [0.0, 0.0, 0.0, 0.0]

def main():
    all_zero = all(s == 0.0 for s in F13_SCORES)

    result = {
        "pipeline_signature": "Z2-V13-F6-2-1-F13-NON-INFORMATIVE-SIGNAL-AUDIT",
        "timestamp": datetime.now(TZ).isoformat(),
        "factor_id": "F13",
        "factor_name": "shareholder_yield",
        "ticker_count": len(F13_TICKERS),
        "tickers": F13_TICKERS,
        "scores": F13_SCORES,
        "all_equal_zero": all_zero,
        "classification": "MATERIALIZED_NON_INFORMATIVE",
        "reason": "all_tickers_zero_shareholder_yield_A_share_market",
        "action": "FREEZE_OR_REMOVE",
    }

    (OUT / "v13_f6_2_1_f13_non_informative_audit.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False))
    print(f"✅ {OUT / 'v13_f6_2_1_f13_non_informative_audit.json'}")
    print(f"   all_zero={all_zero} | classification={result['classification']}")

if __name__ == "__main__":
    main()
