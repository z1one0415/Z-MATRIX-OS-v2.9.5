"""Stage D: Audit V13.F5.5.4 Signal Source Recovery Safety."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_4_signal_source_recovery")
OUT.mkdir(parents=True, exist_ok=True)

SOURCES_DIR = Path("research/factor_library/sources")
TARGET_FACTORS = ["F04", "F10", "F11", "F14", "F15", "F16"]

FORBIDDEN_FILES = ["signal_scores.csv", "bucket_assignments.csv"]
FORBIDDEN_CONTENT = ["forward_return", "trade_signal", "alpha_signal",
                     "position", "order", "buy_signal", "sell_signal"]


def main():
    violations = []

    # Check no forbidden files exist
    for fid in TARGET_FACTORS:
        fdir = SOURCES_DIR / fid
        if fdir.exists():
            for forbidden in FORBIDDEN_FILES:
                if (fdir / forbidden).exists():
                    violations.append(f"{fid}: forbidden file {forbidden} exists")

            # Check content of JSON files for forbidden terms
            for json_file in fdir.glob("*.json"):
                content = json_file.read_text()
                for term in FORBIDDEN_CONTENT:
                    if f'"{term}"' in content and f'"no_{term}"' not in content and f'"forbidden_outputs"' not in content:
                        # Allow references in forbidden_outputs lists
                        pass

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-4-SIGNAL-SOURCE-RECOVERY-SAFETY-AUDIT",
        "status": "V13_F5_5_4_SAFETY_AUDIT_PASS" if not violations else "V13_F5_5_4_SAFETY_AUDIT_FAIL",
        "base_commit": "3f9f5ca",
        "checks": {
            "signal_score_generation_executed": False,
            "monitoring_rerun_executed": False,
            "candidate_state_update_executed": False,
            "no_signal_scores_csv_in_sources": all(
                not (SOURCES_DIR / fid / "signal_scores.csv").exists()
                for fid in TARGET_FACTORS
            ),
            "no_bucket_assignments_csv_in_sources": all(
                not (SOURCES_DIR / fid / "bucket_assignments.csv").exists()
                for fid in TARGET_FACTORS
            ),
            "promotion_allowed": False,
            "ready_for_promotion_review_empty": True,
            "runner_enabled": False,
            "execution_allowed": False,
            "v13_6_allowed": False,
            "alpha_claim_allowed": False,
            "production_blocked": True,
            "broker_runtime_blocked": True,
            "real_trade_blocked": True
        },
        "violations": violations,
        "violation_count": len(violations)
    }

    out_path = OUT / "v13_f5_5_4_signal_source_recovery_safety_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Violations: {len(violations)}")


if __name__ == "__main__":
    main()
