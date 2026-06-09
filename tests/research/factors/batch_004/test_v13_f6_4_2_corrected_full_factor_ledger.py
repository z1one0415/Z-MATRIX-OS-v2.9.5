"""Test V13.F6.4.2 Corrected Full Factor Ledger."""
import json
from pathlib import Path
D = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
def _l(n): return json.loads((D / n).read_text())

def get_status(fid):
    l = _l("v13_f6_4_2_corrected_full_factor_ledger.json")
    for f in l["factors"]:
        if f["factor_id"] == fid:
            return f["status"]
    return None

def test_rejected_not_reserved():
    for fid in ["F02","F03","F05"]:
        assert get_status(fid) == "REJECTED", f"{fid} should be REJECTED"

def test_f01_orange():
    assert get_status("F01") == "ORANGE_MONITORING"

def test_f13_non_informative():
    assert get_status("F13") == "MATERIALIZED_NON_INFORMATIVE"

def test_source_audit():
    for fid in ["F17","F18","F19","F20"]:
        assert get_status(fid) == "SOURCE_AUDIT_COMPLETED", f"{fid} wrong status"

def test_watch_only():
    for fid in ["F22","F26","F27","F34"]:
        assert get_status(fid) == "WATCH_ONLY", f"{fid} should be WATCH_ONLY"

def test_status_counts():
    l = _l("v13_f6_4_2_corrected_full_factor_ledger.json")
    sc = l["status_counts"]
    assert sc.get("REJECTED", 0) == 3
    assert sc.get("ORANGE_MONITORING", 0) == 1
    assert sc.get("MATERIALIZED_NON_INFORMATIVE", 0) == 1
    assert sc.get("SOURCE_AUDIT_COMPLETED", 0) == 4
    assert sc.get("WATCH_ONLY", 0) == 4

def test_60_slots():
    l = _l("v13_f6_4_2_corrected_full_factor_ledger.json")
    assert l["total_slots"] == 60
    assert len(l["factors"]) == 60
