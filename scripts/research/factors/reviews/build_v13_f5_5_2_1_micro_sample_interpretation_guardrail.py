"""Stage D: Build V13.F5.5.2.1 Micro-Sample Interpretation Guardrail."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

guardrail = {
    "pipeline_signature": "Z2-V13-F5-5-2-1-MICRO-SAMPLE-INTERPRETATION-GUARDRAIL",
    "status": "V13_F5_5_2_1_GUARDRAIL_ACTIVE",
    "base_commit": "ecaf0a4",
    "micro_sample_warning_required": True,
    "ticker_count": 5,
    "minimum_for_formal_oos_validation": ">=475 tickers and >=6 OOS months",
    "current_vs_minimum": {
        "current_tickers": 5,
        "required_tickers": 475,
        "current_oos_months": 1,
        "required_oos_months": 6,
        "gap_tickers": 470,
        "gap_months": 5
    },
    "allowed_use": [
        "pipeline_diagnostic",
        "join_validation",
        "sanity_check",
        "early_directional_observation"
    ],
    "forbidden_use": [
        "alpha_claim",
        "promotion_review",
        "suspension_decision",
        "rejection_decision",
        "portfolio_weight",
        "trade_signal"
    ]
}

out_path = OUT / "v13_f5_5_2_1_micro_sample_interpretation_guardrail.json"
out_path.write_text(json.dumps(guardrail, indent=2) + "\n")
print(f"Written: {out_path}")
