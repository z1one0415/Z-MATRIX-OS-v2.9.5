import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
def test_input_pack_script_real():
    t=(W/"scripts/cases/build_v10_council_input_pack.py").read_text()
    assert len(t)>300 and "v9_formal_factor_stability" in t
def test_council_script_real():
    t=(W/"scripts/cases/run_v10_research_council_review.py").read_text()
    assert len(t)>300 and "council_votes" in t
def test_devil_script_real():
    t=(W/"scripts/cases/run_v10_devil_advocate_review.py").read_text()
    assert len(t)>300
def test_thesis_script_real():
    t=(W/"scripts/cases/build_v10_candidate_factor_thesis_pack.py").read_text()
    assert len(t)>200
def test_evidence_not_null():
    inp=json.loads((W/"runtime_reports/cases/v10_council_input_pack.json").read_text())
    for pf in inp["promoted_factors"]:
        for k in ["mean_rankic","rankic_ir","decay_pattern","robustness_grade"]:
            assert pf.get(k) is not None,f"{pf['factor_id']}.{k} is null"
def test_council_verdict_blocked():
    cr=json.loads((W/"runtime_reports/cases/v10_research_council_review.json").read_text())
    for r in cr["reviews"]:
        assert r["investment_verdict"]=="BLOCKED"
def test_thesis_no_investment():
    tp=json.loads((W/"runtime_reports/cases/v10_candidate_factor_thesis_pack.json").read_text())
    for c in tp["candidates"]:
        assert c["investment_action"]=="NONE"
def test_v11_allowed():
    g=json.loads((W/"runtime_reports/cases/v11_paper_watchlist_entry_gate.json").read_text())
    assert "ALLOWED" in g["status"]
def test_closeout_valid():
    co=json.loads((W/"runtime_reports/cases/case_expansion_v10_closeout.json").read_text())
    assert co["alpha_validated"] is False
    assert co["investment_action_count"]==0
    assert co["buy_sell_instruction_count"]==0
