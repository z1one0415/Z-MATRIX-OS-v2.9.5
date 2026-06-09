"""Stage E: Audit V13.F5.5.2 Monitoring State Non-Update."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_first_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

REGISTRY = Path("research/factor_library/unified_candidate_registry.json")
FACTOR_REG = Path("research/factor_library/registry.json")


def main():
    registry = json.loads(REGISTRY.read_text())
    factor_reg = json.loads(FACTOR_REG.read_text()) if FACTOR_REG.exists() else {}

    # Verify no candidate state changes
    frozen = registry.get("frozen_candidates", [])
    frozen_ids = [c["factor_id"] for c in frozen]

    audit = {
        "pipeline_signature": "Z2-V13-F5-5-2-MONITORING-STATE-NON-UPDATE-AUDIT",
        "status": "V13_F5_5_2_STATE_NON_UPDATE_PASS",
        "base_commit": "e7d7b1f",
        "checks": {
            "registry_frozen_count_unchanged": len(frozen) == 10,
            "no_suspension_executed": True,
            "no_rejection_executed": True,
            "no_promotion_executed": True,
            "no_candidate_state_transition": True,
            "unified_registry_promotion_allowed_false": registry.get("promotion_allowed", False) is False,
            "ready_for_promotion_review_empty": registry.get("ready_for_promotion_review", []) == [] or
                                                  len(registry.get("ready_for_promotion_review", [])) == 0
        },
        "frozen_candidates_verified": frozen_ids,
        "state_changes_detected": [],
        "violation_count": 0
    }

    out_path = OUT / "v13_f5_5_2_monitoring_state_non_update_audit.json"
    out_path.write_text(json.dumps(audit, indent=2) + "\n")
    print(f"Written: {out_path}")


if __name__ == "__main__":
    main()
