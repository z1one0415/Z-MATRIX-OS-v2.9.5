"""Stage D: V13.F5.5.2.2 Blocked Factor Preservation."""
import json
from pathlib import Path

OUT = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
OUT.mkdir(parents=True, exist_ok=True)

preservation = {
    "pipeline_signature": "Z2-V13-F5-5-2-2-BLOCKED-FACTOR-PRESERVATION",
    "status": "V13_F5_5_2_2_BLOCKED_FACTORS_PRESERVED",
    "base_commit": "ac96790",
    "blocked_factors": ["F14", "F15", "F16"],
    "blocked_reason": {
        "F14": "BLOCKED_BY_SOURCE_DATA",
        "F15": "BLOCKED_BY_SOURCE_DATA",
        "F16": "BLOCKED_BY_SOURCE_DATA"
    },
    "blocked_factors_not_used_in_monitoring": True,
    "blocked_factors_not_downgraded": True,
    "blocked_factors_not_rejected": True,
    "requires_separate_source_repair_plan": True
}

(OUT / "v13_f5_5_2_2_blocked_factor_preservation.json").write_text(
    json.dumps(preservation, indent=2) + "\n")
print("Written: blocked factor preservation")
