"""Stage B: Audit V13.F5.5.3 Existing Signal Artifacts."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")
OUT.mkdir(parents=True, exist_ok=True)

FACTORS_DIR = Path("research/factor_library/factors")
REVIEWS_DIR = Path("research/factor_library/reviews")
CONFIGS_DIR = Path("configs/research/factors")

FROZEN_CANDIDATES = ["F04", "F10", "F11", "F14", "F15", "F16",
                     "F21", "F24", "F30", "F31"]


def audit_factor(factor_id):
    """Audit existing artifacts for one factor."""
    fdir = FACTORS_DIR / factor_id

    has_dir = fdir.exists()
    has_manifest = (fdir / "factor_manifest.json").exists() if has_dir else False
    has_validation = (fdir / "validation_snapshot.json").exists() if has_dir else False
    has_evidence = (fdir / "evidence_envelope.json").exists() if has_dir else False
    has_app_contract = (fdir / "application_contract.json").exists() if has_dir else False
    has_guardrail = (fdir / "guardrail_profile.json").exists() if has_dir else False

    # Check for actual signal data files
    signal_files = ["signal_scores.csv", "factor_scores.csv",
                    "bucket_assignments.csv", f"{factor_id.lower()}_scores.csv"]
    has_signal_csv = any((fdir / f).exists() for f in signal_files) if has_dir else False
    has_bucket_csv = (fdir / "bucket_assignments.csv").exists() if has_dir else False

    # Check for materialized panel references
    has_materialized_panel = has_manifest and has_validation

    # Check formula contract reference
    formula_ref = None
    if has_manifest:
        manifest = json.loads((fdir / "factor_manifest.json").read_text())
        formula_ref = manifest.get("formula_ref")

    # Determine restoration class
    if has_signal_csv:
        restoration_class = "READY_TO_USE_EXISTING_SIGNAL"
        next_action = "VALIDATE_AND_ALIGN_WITH_LABEL_TICKERS"
    elif has_manifest and has_validation and formula_ref:
        restoration_class = "REQUIRES_SIGNAL_SCORE_MATERIALIZATION"
        next_action = "PLAN_SIGNAL_SCORE_MATERIALIZATION"
    elif has_dir and has_manifest:
        restoration_class = "EXTRACT_FROM_EXISTING_PANEL_OR_REBUILD_REQUIRED"
        next_action = "PLAN_SIGNAL_SCORE_MATERIALIZATION"
    else:
        restoration_class = "BLOCKED_NO_SOURCE"
        next_action = "REQUIRES_FACTOR_DIRECTORY_AND_MANIFEST_FIRST"

    return {
        "factor_id": factor_id,
        "factor_directory_exists": has_dir,
        "manifest_exists": has_manifest,
        "validation_snapshot_exists": has_validation,
        "evidence_envelope_exists": has_evidence,
        "application_contract_exists": has_app_contract,
        "guardrail_profile_exists": has_guardrail,
        "signal_scores_csv_exists": has_signal_csv,
        "bucket_assignments_csv_exists": has_bucket_csv,
        "materialized_panel_exists": has_materialized_panel,
        "formula_contract_exists": formula_ref is not None,
        "formula_ref": formula_ref,
        "restoration_class": restoration_class,
        "next_required_action": next_action
    }


def main():
    results = [audit_factor(fid) for fid in FROZEN_CANDIDATES]

    # Summary counts
    class_counts = {}
    for r in results:
        c = r["restoration_class"]
        class_counts[c] = class_counts.get(c, 0) + 1

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-3-EXISTING-SIGNAL-ARTIFACT-AUDIT",
        "status": "V13_F5_5_3_EXISTING_SIGNAL_ARTIFACT_AUDIT_COMPLETE",
        "base_commit": "bfb48a7",
        "frozen_candidates_audited": len(FROZEN_CANDIDATES),
        "data_source_restrictions": {
            "runtime_reports_read": False,
            "feature_store_read": False,
            "broker_read": False,
            "trading_read": False,
            "execution_read": False,
            "external_data_read": False
        },
        "class_summary": class_counts,
        "factor_audit_results": results,
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_3_existing_signal_artifact_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")
    for cls, cnt in class_counts.items():
        print(f"  {cls}: {cnt}")


if __name__ == "__main__":
    main()
