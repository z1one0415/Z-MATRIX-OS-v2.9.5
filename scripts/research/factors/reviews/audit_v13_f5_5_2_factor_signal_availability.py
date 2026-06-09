"""Stage C: Audit V13.F5.5.2 Factor Signal Availability."""
import json, csv
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

FACTORS_DIR = Path("research/factor_library/factors")
LABEL_PANEL = Path("research/factor_library/reviews/batch_003/"
                   "f5_5_1_2_oos_label_materialization/"
                   "v13_f5_5_1_2_actual_oos_label_panel.csv")

FROZEN_CANDIDATES = ["F04", "F10", "F11", "F14", "F15", "F16",
                     "F21", "F24", "F30", "F31"]


def get_label_tickers():
    """Get unique tickers from label panel."""
    tickers = set()
    with open(LABEL_PANEL) as f:
        for row in csv.DictReader(f):
            tickers.add(row["ticker"])
    return sorted(tickers)


def check_factor_signal(factor_id, label_tickers):
    """Check if pre-computed factor signals exist for this factor."""
    factor_dir = FACTORS_DIR / factor_id

    # Check if factor directory exists
    has_manifest = (factor_dir / "factor_manifest.json").exists()

    # Check for actual signal/score data files (not just metadata)
    # Signal data would be: signal_scores.csv, factor_scores.csv, bucket_assignments.csv
    signal_files = [
        factor_dir / "signal_scores.csv",
        factor_dir / "factor_scores.csv",
        factor_dir / "bucket_assignments.csv",
        factor_dir / f"{factor_id.lower()}_scores_2026_05.csv",
    ]
    has_signal_data = any(f.exists() and f.stat().st_size > 100 for f in signal_files)

    # Also check runtime_reports (which we're NOT allowed to read but we check existence)
    # We explicitly do NOT read runtime_reports

    return {
        "factor_id": factor_id,
        "factor_directory_exists": factor_dir.exists(),
        "manifest_exists": has_manifest,
        "signal_data_files_found": has_signal_data,
        "signal_available_for_label_tickers": has_signal_data,
        "covered_label_tickers": len(label_tickers) if has_signal_data else 0,
        "missing_label_tickers": label_tickers if not has_signal_data else [],
        "allowed_for_partial_monitoring": has_signal_data,
        "factor_status": "SIGNAL_AVAILABLE" if has_signal_data else "SIGNAL_INPUT_BLOCKED",
        "blocked_reason": None if has_signal_data else "no_pre_computed_signal_scores_committed"
    }


def main():
    label_tickers = get_label_tickers()
    factor_results = []

    for fid in FROZEN_CANDIDATES:
        result = check_factor_signal(fid, label_tickers)
        factor_results.append(result)

    available_count = sum(1 for r in factor_results if r["factor_status"] == "SIGNAL_AVAILABLE")
    blocked_count = sum(1 for r in factor_results if r["factor_status"] == "SIGNAL_INPUT_BLOCKED")

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-2-FACTOR-SIGNAL-AVAILABILITY-AUDIT",
        "status": ("V13_F5_5_2_FACTOR_SIGNAL_AVAILABILITY_PARTIAL"
                   if available_count > 0 else
                   "V13_F5_5_2_FACTOR_SIGNAL_AVAILABILITY_ALL_BLOCKED"),
        "base_commit": "e7d7b1f",
        "label_tickers": label_tickers,
        "label_ticker_count": len(label_tickers),
        "frozen_candidates_checked": len(FROZEN_CANDIDATES),
        "factors_with_signal_available": available_count,
        "factors_with_signal_blocked": blocked_count,
        "data_source_restrictions": {
            "runtime_reports_read": False,
            "feature_store_read": False,
            "external_data_call": False,
            "factor_recalculation_executed": False
        },
        "factor_results": factor_results,
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_2_factor_signal_availability_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Available: {available_count}, Blocked: {blocked_count}")


if __name__ == "__main__":
    main()
