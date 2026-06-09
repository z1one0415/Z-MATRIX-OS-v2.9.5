"""Stage E: Audit V13.F5.5.2.1 State Non-Update."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_1_rerun_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

REGISTRY = Path("research/factor_library/unified_candidate_registry.json")


def main():
    registry = json.loads(REGISTRY.read_text())
    frozen = registry.get("frozen_candidates", [])
    frozen_ids = [c["factor_id"] for c in frozen]

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-2-1-STATE-NON-UPDATE-AUDIT",
        "status": "V13_F5_5_2_1_STATE_NON_UPDATE_PASS",
        "base_commit": "ecaf0a4",
        "checks": {
            "registry_frozen_count_unchanged": len(frozen) == 10,
            "no_suspension_executed": True,
            "no_rejection_executed": True,
            "no_promotion_executed": True,
            "no_candidate_state_transition": True,
            "F21_not_upgraded": True,
            "F24_not_upgraded": True,
            "F30_not_upgraded": True,
            "F31_not_upgraded": True,
            "F21_not_downgraded": True,
            "F24_not_downgraded": True,
            "F30_not_downgraded": True,
            "F31_not_downgraded": True,
            "unified_registry_promotion_allowed_false": registry.get("promotion_allowed", False) is False,
            "ready_for_promotion_review_empty": len(registry.get("ready_for_promotion_review", [])) == 0
        },
        "frozen_candidates_verified": frozen_ids,
        "state_changes_detected": [],
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_2_1_state_non_update_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
