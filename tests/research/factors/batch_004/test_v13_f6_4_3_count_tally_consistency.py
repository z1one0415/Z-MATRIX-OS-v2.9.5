"""Test V13.F6.4.3 Count Tally Consistency."""
import json
from pathlib import Path

D2 = Path("research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation")
D3 = Path("research/factor_library/reviews/batch_004/f6_4_3_count_tally_consistency")
def _l2(n): return json.loads((D2 / n).read_text())
def _l3(n): return json.loads((D3 / n).read_text())

def test_sum_equals_60():
    l = _l2("v13_f6_4_2_corrected_full_factor_ledger.json")
    assert sum(l["status_counts"].values()) == 60

def test_sum_equals_60_semantics():
    s = _l3("v13_f6_4_3_corrected_count_semantics.json")
    assert s["slot_status_count_sum"] == 60

def test_defined_blocked_is_12_ledger():
    l = _l2("v13_f6_4_2_corrected_full_factor_ledger.json")
    assert l["status_counts"]["DEFINED_BLOCKED"] == 12

def test_defined_blocked_is_12_closeout():
    co = _l2("v13_f6_4_2_closeout.json")
    assert co["corrected_tally"]["defined_blocked"] == 12

def test_defined_blocked_is_12_semantics():
    cs = _l2("v13_f6_4_2_count_semantics_patch.json")
    assert cs["corrected_counts"]["defined_blocked"] == 12

def test_three_sources_agree():
    a = _l2("v13_f6_4_2_corrected_full_factor_ledger.json")["status_counts"]["DEFINED_BLOCKED"]
    b = _l2("v13_f6_4_2_closeout.json")["corrected_tally"]["defined_blocked"]
    c = _l2("v13_f6_4_2_count_semantics_patch.json")["corrected_counts"]["defined_blocked"]
    assert a == b == c == 12, f"ledger={a}, closeout={b}, semantics={c}"

def test_f03r_not_in_main_ledger():
    l = _l2("v13_f6_4_2_corrected_full_factor_ledger.json")
    ids = [f["factor_id"] for f in l["factors"]]
    assert "F03R" not in ids

def test_no_16_or_11_pollution():
    """Verify no stale 16 or 11 in any batch_004 JSON."""
    import subprocess
    r = subprocess.run(['grep', '-R', '"defined_blocked".*:.*1[16]', 
        'research/factor_library/reviews/batch_004/f6_4_2_historical_status_preservation/',
        'research/factor_library/reviews/batch_004/f6_4_3_count_tally_consistency/'],
        capture_output=True, text=True)
    # Allow 12 but reject 16 and 11
    for line in r.stdout.split('\n'):
        if ': 16' in line or ': 11' in line:
            assert False, f"Stale count found: {line.strip()}"

def test_f6_4_3_artifacts_exist():
    for f in ["v13_f6_4_3_count_tally_contract.json","v13_f6_4_3_tally_reconciliation_audit.json",
              "v13_f6_4_3_corrected_count_semantics.json","v13_f6_4_3_safety_audit.json",
              "v13_f6_4_3_closeout.json"]:
        assert (D3 / f).exists(), f"Missing: {f}"
