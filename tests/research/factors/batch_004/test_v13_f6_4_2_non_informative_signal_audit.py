"""Test V13.F6.4.2 Non-Informative Signal Audit."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def test_audit_exists():
    assert (D / "v13_f6_4_2_non_informative_signal_audit.json").exists()

def test_f13_named():
    a = _l("v13_f6_4_2_non_informative_signal_audit.json")
    assert len(a["non_informative_factors"]) == 1
    assert a["non_informative_factors"][0]["factor_id"] == "F13"
    assert a["non_informative_factors"][0]["status"] == "MATERIALIZED_NON_INFORMATIVE"

def test_f13_has_signal_but_zero_variance():
    a = _l("v13_f6_4_2_non_informative_signal_audit.json")
    f = a["non_informative_factors"][0]
    assert f["has_signal_scores"] is True
    assert f["adds_cross_sectional_information"] is False
    assert f["adds_zero_variance_column"] is True

def test_count_impact():
    a = _l("v13_f6_4_2_non_informative_signal_audit.json")
    assert a["impact"]["informative_signal_ready_count"] == 23
    assert a["impact"]["non_informative_count"] == 1

def test_not_demoted():
    a = _l("v13_f6_4_2_non_informative_signal_audit.json")
    assert "Keep as MATERIALIZED_NON_INFORMATIVE" in a["non_informative_factors"][0]["do_not_demote"]
