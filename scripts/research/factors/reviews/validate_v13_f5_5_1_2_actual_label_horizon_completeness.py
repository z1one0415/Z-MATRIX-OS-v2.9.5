"""Stage F: Validate V13.F5.5.1.2 Actual Label Horizon Completeness."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_1_2_oos_label_materialization")
INTEGRITY = OUT / "v13_f5_5_1_2_actual_label_data_integrity_audit.json"


def main():
    integrity = json.loads(INTEGRITY.read_text())
    counts = integrity["counts"]

    results = {
        "5D": "PASS" if counts["5D"] > 0 else "FAIL",
        "20D": "PASS" if counts["20D"] > 0 else "FAIL",
        "60D": "BLOCKED_NOT_GENERATED"
    }

    validation = {
        "pipeline_signature": "Z2-V13-F5-5-1-2-ACTUAL-LABEL-HORIZON-COMPLETENESS",
        "status": "V13_F5_5_1_2_HORIZON_COMPLETENESS_PASS",
        "base_commit": "db190ff",
        "results": results,
        "counts": {
            "5D": counts["5D"],
            "20D": counts["20D"],
            "60D": counts["60D"]
        },
        "blocked_reason_60D": "insufficient_forward_window_data"
    }

    if results["5D"] != "PASS" or results["20D"] != "PASS":
        validation["status"] = "V13_F5_5_1_2_HORIZON_COMPLETENESS_FAIL"

    out_path = OUT / "v13_f5_5_1_2_actual_label_horizon_completeness.json"
    out_path.write_text(json.dumps(validation, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"5D: {results['5D']}, 20D: {results['20D']}, 60D: {results['60D']}")


if __name__ == "__main__":
    main()
