"""Stage E: V13.F5.5.6 Seven vs Ten Factor Gate Split."""
import json
from pathlib import Path
OUT = Path("research/factor_library/reviews/batch_003/f5_5_6_expansion_gate_plan")
OUT.mkdir(parents=True, exist_ok=True)
s = {
    "pipeline_signature": "Z2-V13-F5-5-6-SEVEN-VS-TEN-FACTOR-GATE-SPLIT",
    "status": "V13_F5_5_6_GATE_SPLIT_DEFINED",
    "base_commit": "7cc8a76",
    "seven_factor_path": {
        "factors": ["F04","F10","F11","F21","F24","F30","F31"],
        "can_enter_expanded_diagnostic": True,
        "promotion_allowed": False,
        "full_candidate_review_allowed": False,
        "note": "7-factor path can proceed to expanded sample diagnostic but NOT to promotion"
    },
    "ten_factor_path": {
        "factors": ["F04","F10","F11","F14","F15","F16","F21","F24","F30","F31"],
        "blocked_until_f14_f15_f16_repaired": True,
        "required_for_full_unified_monitoring": True,
        "required_for_candidate_lifecycle_decisions": True
    },
    "blocked_factor_rules": {
        "F14_F15_F16_not_downgraded_due_to_missing_source": True,
        "F14_F15_F16_not_replaced_by_price_proxy": True,
        "F14_F15_F16_preserved_in_frozen_registry": True
    }
}
(OUT / "v13_f5_5_6_seven_vs_ten_factor_gate_split.json").write_text(json.dumps(s, indent=2) + "\n")
print("Written: 7 vs 10 factor gate split")
