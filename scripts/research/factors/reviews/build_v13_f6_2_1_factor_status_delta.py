#!/usr/bin/env python3
"""V13.F6.2.1 — Generate factor registry delta (F13 → MATERIALIZED_NON_INFORMATIVE)."""
import json
from pathlib import Path
from datetime import datetime, timezone, timedelta

TZ = timezone(timedelta(hours=8))
OUT = Path("research/factor_library/reviews/batch_004/f6_2_1_fundamental_signal_canonicalization")

def main():
    delta = {
        "pipeline_signature": "Z2-V13-F6-2-1-FACTOR-STATUS-DELTA",
        "timestamp": datetime.now(TZ).isoformat(),
        "factors_audited": 7,
        "materialized_count": 7,
        "informative_count": 6,
        "non_informative_count": 1,
        "informative_factors": ["F06","F07","F08","F12","F14","F15"],
        "non_informative_factors": ["F13"],
        "delta": {
            "F13": {
                "status_before": "MATERIALIZED",
                "status_after": "MATERIALIZED_NON_INFORMATIVE",
                "reason": "all_equal_zero_shareholder_yield",
                "monitoring_eligible": False,
                "recommendation": "FREEZE_OR_REMOVE"
            }
        },
        "registry_update_required": True,
        "monitoring_rerun_executed": False
    }
    
    (OUT / "v13_f6_2_1_factor_status_delta.json").write_text(
        json.dumps(delta, indent=2, ensure_ascii=False))
    print(f"✅ {OUT / 'v13_f6_2_1_factor_status_delta.json'}")

if __name__ == "__main__":
    main()
