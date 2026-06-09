"""Stage C: Classify V13.F5.5.3 Signal Source Restoration Paths."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_3_signal_score_restoration")
OUT.mkdir(parents=True, exist_ok=True)

AUDIT = OUT / "v13_f5_5_3_existing_signal_artifact_audit.json"


def main():
    audit = json.loads(AUDIT.read_text())
    results = audit["factor_audit_results"]

    classifications = {
        "READY_TO_USE_EXISTING_SIGNAL": [],
        "EXTRACT_FROM_EXISTING_MATERIALIZED_PANEL": [],
        "REQUIRES_SIGNAL_SCORE_MATERIALIZATION": [],
        "REQUIRES_FACTOR_REIMPLEMENTATION": [],
        "BLOCKED_NO_SOURCE": []
    }

    factor_paths = []
    for r in results:
        cls = r["restoration_class"]
        # Normalize to standard classes
        if cls == "EXTRACT_FROM_EXISTING_PANEL_OR_REBUILD_REQUIRED":
            cls = "REQUIRES_SIGNAL_SCORE_MATERIALIZATION"

        if cls not in classifications:
            classifications[cls] = []
        classifications[cls].append(r["factor_id"])

        factor_paths.append({
            "factor_id": r["factor_id"],
            "restoration_class": cls,
            "has_formula_ref": r["formula_contract_exists"],
            "has_manifest": r["manifest_exists"],
            "actionable_in_f5_5_3_1": cls == "REQUIRES_SIGNAL_SCORE_MATERIALIZATION",
            "blocked_reason": (None if cls != "BLOCKED_NO_SOURCE"
                               else "no_factor_directory_or_manifest_in_clean_branch")
        })

    actionable = sum(1 for p in factor_paths if p["actionable_in_f5_5_3_1"])
    blocked = sum(1 for p in factor_paths if not p["actionable_in_f5_5_3_1"])

    classification = {
        "pipeline_signature": "Z2-V13-F5-5-3-SIGNAL-SOURCE-CLASSIFICATION",
        "status": "V13_F5_5_3_SIGNAL_SOURCE_CLASSIFICATION_COMPLETE",
        "base_commit": "bfb48a7",
        "summary": {
            "total_frozen_candidates": 10,
            "actionable_for_f5_5_3_1": actionable,
            "blocked_requires_prior_work": blocked
        },
        "class_distribution": {k: v for k, v in classifications.items() if v},
        "factor_restoration_paths": factor_paths,
        "f5_5_3_1_eligible_factors": [p["factor_id"] for p in factor_paths
                                       if p["actionable_in_f5_5_3_1"]],
        "blocked_factors_requiring_prior_batch_work": [
            p["factor_id"] for p in factor_paths if not p["actionable_in_f5_5_3_1"]
        ]
    }

    out_path = OUT / "v13_f5_5_3_signal_source_classification.json"
    out_path.write_text(json.dumps(classification, indent=2) + "\n")
    print(f"Written: {out_path}")
    print(f"Actionable: {actionable}, Blocked: {blocked}")


if __name__ == "__main__":
    main()
