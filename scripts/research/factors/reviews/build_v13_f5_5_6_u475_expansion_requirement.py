"""Stage C: V13.F5.5.6 U475 Expansion Requirement."""
import json
from pathlib import Path
OUT = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
OUT.mkdir(parents=True, exist_ok=True)
r = {
    "pipeline_signature": "Z2-V13-F5-5-6-U475-EXPANSION-REQUIREMENT",
    "status": "V13_F5_5_6_U475_REQUIREMENT_DEFINED",
    "base_commit": "7cc8a76",
    "price_bars_requirements": {
        "minimum_ticker_coverage": 475,
        "preferred_ticker_coverage": 1000,
        "forward_window_5D": True,
        "forward_window_20D": True,
        "forward_window_60D": True,
        "signal_lookback_minimum_days": 60,
        "source": "data/price_bars or equivalent PIT-safe market data"
    },
    "factor_signal_requirements": {
        "seven_factor_minimum_path": ["F04","F10","F11","F21","F24","F30","F31"],
        "ten_factor_full_path": ["F04","F10","F11","F14","F15","F16","F21","F24","F30","F31"],
        "ten_factor_requires": "F14/F15/F16 data source repair completed"
    },
    "label_requirements": {
        "label_role": "OUTCOME_LABEL_ONLY",
        "written_to_feature_store": False,
        "used_for_signal_calculation": False,
        "horizons": ["5D", "20D", "60D"]
    },
    "minimum_for_formal_oos_gate": {
        "ticker_count": 475,
        "oos_months": 6,
        "all_horizons_including_60D": True,
        "signal_coverage_per_factor_gte_90pct": True
    }
}
(OUT / "v13_f5_5_6_u475_expansion_requirement.json").write_text(json.dumps(r, indent=2) + "\n")
print("Written: U475 expansion requirement")
