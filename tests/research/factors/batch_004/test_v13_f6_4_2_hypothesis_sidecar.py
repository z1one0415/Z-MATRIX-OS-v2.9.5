"""Test V13.F6.4.2 Hypothesis Sidecar."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def test_sidecar_exists():
    assert (D / "v13_f6_4_2_hypothesis_sidecar.json").exists()

def test_f03r_present():
    s = _l("v13_f6_4_2_hypothesis_sidecar.json")
    assert len(s["sidecar_factors"]) == 1
    assert s["sidecar_factors"][0]["factor_id"] == "F03R"

def test_f03r_parent():
    s = _l("v13_f6_4_2_hypothesis_sidecar.json")
    f = s["sidecar_factors"][0]
    assert f["parent_factor"] == "F03"
    assert f["parent_status"] == "REJECTED"
    assert f["status"] == "HYPOTHESIS_ONLY"

def test_restrictions():
    s = _l("v13_f6_4_2_hypothesis_sidecar.json")
    r = s["sidecar_factors"][0]["restrictions"]
    assert r["cannot_enter_frozen_registry"] is True
    assert r["cannot_trigger_promotion"] is True
    assert "academic_reference" in r["only_allowed_for"]

def test_not_in_main_ledger():
    """Verify F03R is NOT in the main F01-F60 ledger."""
    led = _l("v13_f6_4_2_corrected_full_factor_ledger.json")
    ids = [f["factor_id"] for f in led["factors"]]
    assert "F03R" not in ids
