"""Stage C: Restore V13.F5.5.4 Batch1/Batch2 Factor Source Packages."""
import json
from pathlib import Path

SOURCES_DIR = Path("research/factor_library/sources")

FACTOR_SPECS = {
    "F04": {
        "name": "RESIDUAL_MOMENTUM",
        "type": "PRICE_VOLUME_RISK",
        "batch": "batch_001",
        "family": "MOMENTUM",
        "description": "Residual momentum after market/sector neutralization",
        "source_data": ["data/price_bars"],
        "lookback_days": 60,
        "formula_summary": "cumulative_return(t-60, t-5) - beta * market_return(t-60, t-5)"
    },
    "F10": {
        "name": "LOW_VOLATILITY",
        "type": "PRICE_VOLUME_RISK",
        "batch": "batch_001",
        "family": "RISK",
        "description": "Realized volatility over trailing window (lower = better signal)",
        "source_data": ["data/price_bars"],
        "lookback_days": 20,
        "formula_summary": "std(daily_returns, window=20) inverted"
    },
    "F11": {
        "name": "SHORT_TERM_REVERSAL",
        "type": "PRICE_VOLUME_RISK",
        "batch": "batch_001",
        "family": "REVERSAL",
        "description": "Short-term mean reversion signal (5-day)",
        "source_data": ["data/price_bars"],
        "lookback_days": 5,
        "formula_summary": "-cumulative_return(t-5, t)"
    },
    "F14": {
        "name": "ASSET_GROWTH_DISCIPLINE",
        "type": "FUNDAMENTAL_QUALITY",
        "batch": "batch_002",
        "family": "QUALITY",
        "description": "Penalizes excessive asset growth (lower growth = disciplined)",
        "source_data": ["data/price_bars"],
        "lookback_days": 20,
        "formula_summary": "proxy: -abs(price_change_20d) as discipline indicator",
        "note": "Fundamental data unavailable; using price-proxy for micro-sample diagnostic only"
    },
    "F15": {
        "name": "ACCRUALS_QUALITY",
        "type": "FUNDAMENTAL_QUALITY",
        "batch": "batch_002",
        "family": "QUALITY",
        "description": "Cash flow vs earnings quality (higher = better quality)",
        "source_data": ["data/price_bars"],
        "lookback_days": 20,
        "formula_summary": "proxy: volume_stability_ratio as quality indicator",
        "note": "Fundamental data unavailable; using volume-proxy for micro-sample diagnostic only"
    },
    "F16": {
        "name": "SENTIMENT_ATTENTION",
        "type": "PRICE_VOLUME_SENTIMENT",
        "batch": "batch_002",
        "family": "SENTIMENT",
        "description": "Abnormal volume and price attention signal",
        "source_data": ["data/price_bars"],
        "lookback_days": 10,
        "formula_summary": "volume_ratio(recent_5d / trailing_20d) * abs(return_5d)"
    }
}


def build_manifest(factor_id, spec):
    return {
        "pipeline_signature": f"V13-F5-5-4-RESTORED-MANIFEST-{factor_id}",
        "interface_version": "factor.application.v1",
        "factor_id": factor_id,
        "factor_name": spec["name"],
        "factor_family_id": spec["family"],
        "factor_type": spec["type"],
        "factor_status": "RESTORED_FOR_SIGNAL_MATERIALIZATION",
        "source_data_refs": spec["source_data"],
        "universe_policy": "LABEL_TICKERS_ONLY_FOR_MICRO_SAMPLE",
        "horizon_policy": {
            "allowed_horizons": ["5D", "20D"],
            "blocked_horizons": ["60D"]
        },
        "ready_for_candidate_review": False,
        "ready_for_promotion_review": [],
        "promotion_allowed": False,
        "alpha_claim_allowed": False,
        "production": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED"
    }


def build_formula_contract(factor_id, spec):
    return {
        "pipeline_signature": f"V13-F5-5-4-RESTORED-FORMULA-{factor_id}",
        "factor_id": factor_id,
        "factor_name": spec["name"],
        "formula_summary": spec["formula_summary"],
        "lookback_days": spec["lookback_days"],
        "source_data_required": spec["source_data"],
        "output_fields": ["score", "rank", "bucket"],
        "output_role": "FACTOR_SIGNAL_ONLY",
        "forbidden_outputs": ["forward_return", "trade_signal", "alpha_signal",
                              "position", "order", "buy_signal", "sell_signal"],
        "note": spec.get("note", None)
    }


def build_materialization_requirements(factor_id, spec):
    return {
        "pipeline_signature": f"V13-F5-5-4-RESTORED-MATREQ-{factor_id}",
        "factor_id": factor_id,
        "requirements": {
            "price_bars_available": True,
            "lookback_days_minimum": spec["lookback_days"],
            "tickers_from_label_panel": True,
            "rebalance_date_required": True,
            "full_universe_required": False
        },
        "constraints": {
            "signal_role": "FACTOR_SIGNAL_ONLY",
            "no_forward_return_input": True,
            "no_feature_store_write": True,
            "no_runtime_reports_write": True
        }
    }


def build_source_provenance(factor_id, spec):
    return {
        "pipeline_signature": f"V13-F5-5-4-RESTORED-PROVENANCE-{factor_id}",
        "factor_id": factor_id,
        "restoration_source": "configs/research/factors/factor_domain_registry_v1.json",
        "restoration_commit": "3f9f5ca",
        "original_batch": spec["batch"],
        "restoration_reason": "signal_source_recovery_for_monitoring_rerun",
        "restoration_scope": "minimal_source_package_only",
        "no_signal_scores_included": True,
        "no_bucket_assignments_included": True
    }


def main():
    restored = []
    for factor_id, spec in FACTOR_SPECS.items():
        fdir = SOURCES_DIR / factor_id
        fdir.mkdir(parents=True, exist_ok=True)

        (fdir / "factor_manifest.json").write_text(
            json.dumps(build_manifest(factor_id, spec), indent=2) + "\n")
        (fdir / "formula_contract.json").write_text(
            json.dumps(build_formula_contract(factor_id, spec), indent=2) + "\n")
        (fdir / "signal_materialization_requirements.json").write_text(
            json.dumps(build_materialization_requirements(factor_id, spec), indent=2) + "\n")
        (fdir / "source_provenance.json").write_text(
            json.dumps(build_source_provenance(factor_id, spec), indent=2) + "\n")

        restored.append(factor_id)
        print(f"Restored: {fdir}/ (4 files)")

    print(f"\nTotal restored: {len(restored)} factors")


if __name__ == "__main__":
    main()
