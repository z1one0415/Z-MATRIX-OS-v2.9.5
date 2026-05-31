import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_inventory():
    d=json.loads((W/"runtime_reports/cases/v6a_factor_input_inventory.json").read_text())
    assert d["factor_count"]>=20
    assert d["real_ready_count"]>=10
    assert d["synthetic_blocked_count"]>=2
    assert d["can_validate_factor_count"]==0
def test_mom20_real():
    d=json.loads((W/"runtime_reports/cases/v6a_factor_input_inventory.json").read_text())
    m=[f for f in d["factors"] if f["factor_id"]=="MOM_20D"][0]
    assert m["truth_status"]=="REAL_READY"
    assert m["ready_for_alpha_claim"] is False
def test_pe_ttm_missing():
    d=json.loads((W/"runtime_reports/cases/v6a_factor_input_inventory.json").read_text())
    p=[f for f in d["factors"] if f["factor_id"]=="PE_TTM"][0]
    assert p["truth_status"]=="MISSING_INPUT"
def test_legacy_blocked():
    d=json.loads((W/"runtime_reports/cases/v6a_factor_input_inventory.json").read_text())
    l=[f for f in d["factors"] if f["factor_id"]=="LEGACY_SYNTHETIC_IC"][0]
    assert l["truth_status"]=="SYNTHETIC_BLOCKED"
def test_all_no_alpha():
    d=json.loads((W/"runtime_reports/cases/v6a_factor_input_inventory.json").read_text())
    for f in d["factors"]:
        assert f["ready_for_alpha_claim"] is False
