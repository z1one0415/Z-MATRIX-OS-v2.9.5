"""Stage D: Build V13.F5.5.3 Signal Score Schema."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")
OUT.mkdir(parents=True, exist_ok=True)


def main():
    schema = {
        "pipeline_signature": "Z2-V13-F5-5-3-SIGNAL-SCORE-SCHEMA",
        "status": "V13_F5_5_3_SIGNAL_SCORE_SCHEMA_DEFINED",
        "base_commit": "bfb48a7",
        "schema_version": "1.0",
        "required_fields": [
            {"name": "factor_id", "type": "string", "description": "Factor identifier"},
            {"name": "ticker", "type": "string", "description": "Stock ticker"},
            {"name": "rebalance_date", "type": "date", "description": "Signal evaluation date"},
            {"name": "score", "type": "float", "description": "Raw factor score"},
            {"name": "rank", "type": "int", "description": "Cross-sectional rank (1=best)"},
            {"name": "bucket", "type": "int", "description": "Quintile bucket (1-5)"},
            {"name": "score_available_at", "type": "date", "description": "Point-in-time availability date"},
            {"name": "source_artifact_ref", "type": "string", "description": "Path to source artifact"},
            {"name": "signal_role", "type": "string", "description": "Must be FACTOR_SIGNAL_ONLY"}
        ],
        "csv_header": "factor_id,ticker,rebalance_date,score,rank,bucket,score_available_at,source_artifact_ref,signal_role",
        "constraints": {
            "signal_role": "FACTOR_SIGNAL_ONLY",
            "not_outcome_label": True,
            "not_trade_signal": True,
            "not_alpha_signal": True,
            "not_position_weight": True,
            "not_buy_sell_signal": True,
            "not_order_signal": True
        },
        "usage_restrictions": {
            "allowed_for": ["partial_monitoring_diagnostic", "directional_spread_calculation"],
            "blocked_for": ["trade_execution", "alpha_claim", "position_sizing",
                           "order_generation", "production", "broker"]
        }
    }

    out_path = OUT / "v13_f5_5_3_signal_score_schema.json"
    out_path.write_text(json.dumps(schema, indent=2) + "\n")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
