"""V13.F5.5.4.2 Blocked Source Repair Plan for F14/F15/F16."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_2_blocked_source_repair_plan")
OUT.mkdir(parents=True, exist_ok=True)

# Contract
contract = {
    "pipeline_signature": "Z2-V13-F5-5-4-2-BLOCKED-SOURCE-REPAIR-CONTRACT",
    "status": "V13_F5_5_4_2_BLOCKED_SOURCE_REPAIR_CONTRACT_BUILT",
    "base_commit": "ac96790",
    "planning_only": True,
    "target_factors": ["F14", "F15", "F16"],
    "signal_score_generation_allowed": False,
    "monitoring_execution_allowed": False,
    "candidate_state_update_allowed": False,
    "price_proxy_substitution_allowed": False,
    "promotion_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED"
}

# Source gap audit
gap_audit = {
    "pipeline_signature": "Z2-V13-F5-5-4-2-F14-F15-F16-SOURCE-GAP-AUDIT",
    "status": "V13_F5_5_4_2_SOURCE_GAP_AUDIT_COMPLETE",
    "base_commit": "ac96790",
    "factor_gaps": {
        "F14": {
            "factor_name": "ASSET_GROWTH_DISCIPLINE",
            "factor_type": "FUNDAMENTAL_QUALITY",
            "required_data": ["total_assets", "ann_date", "known_at"],
            "available_data": [],
            "gap": "No PIT-safe fundamental/accounting data committed at 2026-05-06",
            "repair_options": [
                "Commit historical financial statements with ann_date/known_at fields",
                "Use tushare PIT financial data with available_at audit"
            ],
            "price_proxy_allowed": False,
            "synthetic_fundamentals_allowed": False
        },
        "F15": {
            "factor_name": "ACCRUALS_QUALITY",
            "factor_type": "FUNDAMENTAL_QUALITY",
            "required_data": ["operating_cash_flow", "net_income", "total_assets", "ann_date", "known_at"],
            "available_data": [],
            "gap": "No PIT-safe fundamental/accounting data committed at 2026-05-06",
            "repair_options": [
                "Commit historical financial statements with ann_date/known_at fields",
                "Use tushare PIT financial data with available_at audit"
            ],
            "price_proxy_allowed": False,
            "synthetic_fundamentals_allowed": False
        },
        "F16": {
            "factor_name": "SENTIMENT_ATTENTION",
            "factor_type": "PRICE_VOLUME_SENTIMENT",
            "required_data": ["sentiment_score OR attention_proxy_contract"],
            "available_data": [],
            "gap": "No committed sentiment/attention data source",
            "repair_options": [
                "Redefine as PRICE_VOLUME_ATTENTION with explicit volume-attention proxy contract",
                "Commit external sentiment data source with provenance"
            ],
            "price_proxy_allowed": False,
            "note": "If redefined as PRICE_VOLUME_ATTENTION, factor_type must change and formula must be re-contracted"
        }
    }
}

# Required data contract
required_data = {
    "pipeline_signature": "Z2-V13-F5-5-4-2-REQUIRED-DATA-CONTRACT",
    "status": "V13_F5_5_4_2_REQUIRED_DATA_CONTRACT_BUILT",
    "base_commit": "ac96790",
    "F14_F15_requirements": {
        "data_type": "PIT-safe fundamental financial statements",
        "required_fields": ["ticker", "report_period", "ann_date", "known_at",
                           "total_assets", "net_income", "operating_cash_flow"],
        "pit_rules": {
            "must_use_ann_date_not_report_period": True,
            "must_not_forward_fill_future_data": True,
            "must_not_use_synthetic_fundamentals": True,
            "disclosure_staleness_check_required": True
        },
        "minimum_coverage": "5 label tickers at rebalance_date 2026-05-06"
    },
    "F16_requirements": {
        "option_A": {
            "data_type": "External sentiment data with provenance",
            "required_fields": ["ticker", "date", "sentiment_score", "source", "available_at"]
        },
        "option_B": {
            "data_type": "Redefine factor as PRICE_VOLUME_ATTENTION",
            "requires": "New formula_contract with volume-attention proxy definition",
            "factor_type_change": "SENTIMENT_ATTENTION -> PRICE_VOLUME_ATTENTION",
            "must_update_manifest": True
        }
    }
}

# Repair plan closeout
closeout = {
    "pipeline_signature": "Z2-V13-F5-5-4-2-REPAIR-PLAN-CLOSEOUT",
    "status": "V13_F5_5_4_2_REPAIR_PLAN_BUILT",
    "base_commit": "ac96790",
    "planning_only": True,
    "factors_requiring_repair": ["F14", "F15", "F16"],
    "repair_executed": False,
    "signal_scores_generated": False,
    "monitoring_rerun_executed": False,
    "candidate_state_update_executed": False,
    "promotion_allowed": False,
    "runner_enabled": False,
    "execution_allowed": False,
    "production": "BLOCKED",
    "broker_runtime": "BLOCKED",
    "real_trade": "BLOCKED",
    "recommended_next_action": "ACQUIRE_PIT_FUNDAMENTAL_DATA_OR_REDEFINE_F16_FACTOR_TYPE"
}

# Write all 4 files
(OUT / "v13_f5_5_4_2_blocked_source_repair_contract.json").write_text(json.dumps(contract, indent=2) + "\n")
(OUT / "v13_f5_5_4_2_f14_f15_f16_source_gap_audit.json").write_text(json.dumps(gap_audit, indent=2) + "\n")
(OUT / "v13_f5_5_4_2_required_data_contract.json").write_text(json.dumps(required_data, indent=2) + "\n")
(OUT / "v13_f5_5_4_2_repair_plan_closeout.json").write_text(json.dumps(closeout, indent=2) + "\n")
print("Written: 4 repair plan artifacts for F14/F15/F16")
