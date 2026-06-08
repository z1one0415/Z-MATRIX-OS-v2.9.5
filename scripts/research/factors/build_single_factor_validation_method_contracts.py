#!/usr/bin/env python3
"""V13.F2.2 — Stage B: single factor validation method contracts."""
import json, sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parent.parent.parent.parent / "runtime_reports" / "research" / "factors"
RUNTIME.mkdir(parents=True, exist_ok=True)

f03 = {
    "factor_id": "F03",
    "factor_name": "INDUSTRY_RELATIVE_STRENGTH",
    "factor_family": "MOMENTUM",
    "input_panel_path": "runtime_reports/research/factors/f03_industry_relative_strength_panel.csv",
    "validation_ready": True,
    "validation_methods": {
        "ic": {
            "enabled_next_step": True,
            "method": "spearman_rank_correlation",
            "minimum_month_count": 12,
            "preferred_month_count": 24
        },
        "rank_ic": {
            "enabled_next_step": True,
            "method": "cross_sectional_rank_ic_by_rebalance_month"
        },
        "bucket_spread": {
            "enabled_next_step": True,
            "bucket_count": 3,
            "bucket_labels": ["LOW", "MID", "HIGH"],
            "spread": "HIGH_MINUS_LOW"
        },
        "horizon_split": {
            "enabled_next_step": True,
            "horizons": ["20D", "60D"]
        },
        "regime_split": {
            "enabled_next_step": True,
            "regime_sources": ["market_return_20d", "market_return_60d", "volatility_regime"]
        },
        "cost_adjusted": {
            "enabled_next_step": True,
            "round_trip_cost_bps": 30
        }
    },
    "forbidden_validation_methods_this_round": [
        "MULTI_FACTOR_COMPOSITE",
        "WEIGHT_OPTIMIZATION",
        "PAPER_TRADING",
        "V13_6_PREP",
        "ALPHA_CLAIM"
    ],
    "expected_hypothesis": "industry-relative winners should outperform industry-relative losers over 20D/60D",
    "risk_notes": "may duplicate sector wind / industry momentum exposure",
    "required_diagnostics": [
        "sector-neutral check",
        "industry concentration check",
        "regime split"
    ],
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

f06 = {
    "factor_id": "F06",
    "factor_name": "FUNDAMENTAL_QUALITY",
    "factor_family": "FUNDAMENTAL",
    "input_panel_path": "runtime_reports/research/factors/f06_fundamental_quality_panel.csv",
    "validation_ready": True,
    "validation_methods": {
        "ic": {
            "enabled_next_step": True,
            "method": "spearman_rank_correlation",
            "minimum_month_count": 12,
            "preferred_month_count": 24
        },
        "rank_ic": {
            "enabled_next_step": True,
            "method": "cross_sectional_rank_ic_by_rebalance_month"
        },
        "bucket_spread": {
            "enabled_next_step": True,
            "bucket_count": 3,
            "bucket_labels": ["LOW", "MID", "HIGH"],
            "spread": "HIGH_MINUS_LOW"
        },
        "horizon_split": {
            "enabled_next_step": True,
            "horizons": ["20D", "60D"]
        },
        "regime_split": {
            "enabled_next_step": True,
            "regime_sources": ["market_return_20d", "market_return_60d", "volatility_regime"]
        },
        "cost_adjusted": {
            "enabled_next_step": True,
            "round_trip_cost_bps": 30
        }
    },
    "forbidden_validation_methods_this_round": [
        "MULTI_FACTOR_COMPOSITE",
        "WEIGHT_OPTIMIZATION",
        "PAPER_TRADING",
        "V13_6_PREP",
        "ALPHA_CLAIM"
    ],
    "expected_hypothesis": "high-quality fundamental stocks should outperform low-quality stocks over 60D more than 20D",
    "risk_notes": "disclosure lag / stale fundamentals / low rebalance diversity",
    "required_diagnostics": [
        "disclosure freshness",
        "reporting period distribution",
        "quality score dispersion",
        "horizon decay"
    ],
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

contract = {
    "pipeline_signature": "Z2-V13-F2-2-METHOD-CONTRACTS",
    "status": "SINGLE_FACTOR_VALIDATION_METHOD_CONTRACTS_BUILT",
    "factor_count": 2,
    "factors": [f03, f06],
    "alpha_claim_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

dst = RUNTIME / "single_factor_validation_method_contracts.json"
dst.write_text(json.dumps(contract, indent=2))
print(f"[F2.2-B] Method contracts built -> {dst}")
sys.exit(0)
