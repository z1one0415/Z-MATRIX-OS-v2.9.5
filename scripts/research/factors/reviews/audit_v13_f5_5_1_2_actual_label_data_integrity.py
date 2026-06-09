"""Stage D: Audit V13.F5.5.1.2 Actual Label Data Integrity."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
PANEL = OUT / "v13_f5_5_1_2_actual_oos_label_panel.csv"


def main():
    rows = []
    with open(PANEL) as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames
        for row in reader:
            rows.append(row)

    total = len(rows)
    rows_5d = sum(1 for r in rows if r["horizon"] == "5D")
    rows_20d = sum(1 for r in rows if r["horizon"] == "20D")
    rows_60d = sum(1 for r in rows if r["horizon"] == "60D")

    # Check forward_return non-empty
    empty_returns = sum(1 for r in rows if not r["forward_return"] or r["forward_return"] == "")

    # Check uniqueness of (ticker, rebalance_date, horizon)
    keys = [(r["ticker"], r["rebalance_date"], r["horizon"]) for r in rows]
    unique = len(set(keys)) == len(keys)

    # Check label_available_at >= source_price_end_date
    date_order_ok = all(r["label_available_at"] >= r["source_price_end_date"] for r in rows)

    # Check no forbidden columns
    forbidden = ["factor_score", "rank", "bucket", "alpha_signal",
                 "trade_signal", "position", "order"]
    has_forbidden = any(col in headers for col in forbidden)

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-1-2-ACTUAL-LABEL-DATA-INTEGRITY-AUDIT",
        "status": "V13_F5_5_1_2_LABEL_DATA_INTEGRITY_PASS",
        "base_commit": "db190ff",
        "label_data_row_count": total,
        "checks": {
            "label_data_row_count_gt_zero": total > 0,
            "5D_row_count_gt_zero": rows_5d > 0,
            "20D_row_count_gt_zero": rows_20d > 0,
            "60D_row_count_zero": rows_60d == 0,
            "forward_return_non_empty": empty_returns == 0,
            "ticker_rebalance_horizon_unique": unique,
            "label_available_at_gte_source_end_date": date_order_ok,
            "no_factor_score_rank_bucket": not has_forbidden,
            "no_alpha_trade_position_order": not has_forbidden
        },
        "counts": {
            "total_rows": total,
            "5D": rows_5d,
            "20D": rows_20d,
            "60D": rows_60d,
            "empty_forward_return": empty_returns
        },
        "violation_count": 0
    }

    # Check all checks pass
    violations = sum(1 for v in audit["checks"].values() if v is False)
    audit["violation_count"] = violations
    if violations > 0:
        audit["status"] = "V13_F5_5_1_2_LABEL_DATA_INTEGRITY_FAIL"

    out_path = OUT / "v13_f5_5_1_2_actual_label_data_integrity_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Rows: {total}, Violations: {violations}")


if __name__ == "__main__":
    main()
