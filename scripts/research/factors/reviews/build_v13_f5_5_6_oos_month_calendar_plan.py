"""Stage D: V13.F5.5.6 OOS Month Calendar Plan."""
import json
from pathlib import Path
OUT = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
OUT.mkdir(parents=True, exist_ok=True)
p = {
    "pipeline_signature": "Z2-V13-F5-5-6-OOS-MONTH-CALENDAR-PLAN",
    "status": "V13_F5_5_6_OOS_MONTH_CALENDAR_PLAN_BUILT",
    "base_commit": "7cc8a76",
    "minimum_oos_start_exclusive": "2026-05-01",
    "first_available_month": "2026-05",
    "minimum_formal_months": 6,
    "preferred_months": 12,
    "projected_calendar": {
        "month_1": "2026-05",
        "month_2": "2026-06",
        "month_3": "2026-07",
        "month_4": "2026-08",
        "month_5": "2026-09",
        "month_6": "2026-10",
        "month_7_to_12": "2026-11 through 2027-04"
    },
    "formal_gate_cannot_open_until": {
        "oos_months_gte_6": True,
        "ticker_count_gte_475": True,
        "20D_labels_available": True,
        "60D_labels_available_for_60D_factors": True,
        "all_signal_lookback_windows_available": True
    },
    "earliest_possible_formal_gate_open": "2026-10 (if data expansion starts immediately)"
}
(OUT / "v13_f5_5_6_oos_month_calendar_plan.json").write_text(json.dumps(p, indent=2) + "\n")
print("Written: OOS month calendar plan")
