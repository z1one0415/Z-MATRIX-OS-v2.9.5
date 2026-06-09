"""Test V13.F6.4.2 Safety Audit."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def test_safety_pass():
    s = _l("v13_f6_4_2_safety_audit.json")
    assert s["status"] == "V13_F6_4_2_SAFETY_AUDIT_PASS"
    assert s["violation_count"] == 0

def test_no_demotion():
    s = _l("v13_f6_4_2_safety_audit.json")
    assert s["checks"]["no_status_demotion_executed"] is True
    assert s["checks"]["all_rejected_factors_preserved"] is True
    assert s["checks"]["f13_non_informative_label_preserved"] is True

def test_no_execution():
    s = _l("v13_f6_4_2_safety_audit.json")
    assert s["checks"]["no_signal_regenerated"] is True
    assert s["checks"]["no_monitoring_rerun"] is True
    assert s["checks"]["no_promotion"] is True
    assert s["checks"]["runner_enabled"] is False
    assert s["checks"]["execution_allowed"] is False
    assert s["checks"]["production_blocked"] is True
