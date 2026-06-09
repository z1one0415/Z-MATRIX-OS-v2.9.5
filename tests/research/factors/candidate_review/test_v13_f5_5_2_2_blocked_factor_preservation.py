"""Tests for V13.F5.5.2.2 Blocked Factor Preservation."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
def _l(n): return json.loads((D / n).read_text())

def test_preservation():
    p = _l("v13_f5_5_2_2_blocked_factor_preservation.json")
    assert p["blocked_factors"] == ["F14", "F15", "F16"]
    assert p["blocked_factors_not_used_in_monitoring"] is True
    assert p["blocked_factors_not_downgraded"] is True
    assert p["blocked_factors_not_rejected"] is True
    assert p["requires_separate_source_repair_plan"] is True
