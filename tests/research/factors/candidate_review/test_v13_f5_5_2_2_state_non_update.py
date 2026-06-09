"""Tests for V13.F5.5.2.2 State Non-Update."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_003/f5_5_2_2_seven_factor_partial_monitoring")
def _l(n): return json.loads((D / n).read_text())

def test_state_pass():
    a = _l("v13_f5_5_2_2_state_non_update_audit.json")
    assert a["status"] == "V13_F5_5_2_2_STATE_NON_UPDATE_PASS"
    assert a["violation_count"] == 0
    assert a["checks"]["no_suspension_executed"] is True
    assert a["checks"]["no_promotion_executed"] is True
    assert a["checks"]["seven_monitored_factors_stable"] is True
    assert a["checks"]["three_blocked_factors_not_downgraded"] is True
