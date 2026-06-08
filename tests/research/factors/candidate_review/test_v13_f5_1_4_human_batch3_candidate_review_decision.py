"""V13.F5.1.4 — Human candidate review decision tests."""
import json, subprocess
from pathlib import Path

DECISION_DIR = Path("research/factor_library/reviews/batch_003/f5_1_4_candidate_review_decision")

def test_8_files():
    required = ["batch3_candidate_review_decision_record.json","batch3_candidate_review_decision_matrix.json","batch3_candidate_review_approved_queue.json","batch3_candidate_review_hold_queue.json","batch3_candidate_review_rejected_queue.json","batch3_candidate_review_conditions.json","batch3_candidate_review_safety_audit.json","batch3_candidate_review_closeout.json"]
    for f in required: assert (DECISION_DIR / f).exists()

def test_approved_plus_held_plus_rejected_equals_8():
    rec = json.loads((DECISION_DIR / "batch3_candidate_review_decision_record.json").read_text())
    total = len(rec.get("approved_factors",[])) + len(rec.get("held_factors",[])) + len(rec.get("rejected_factors",[]))
    assert total == 8

def test_matrix_8():
    m = json.loads((DECISION_DIR / "batch3_candidate_review_decision_matrix.json").read_text())
    assert m.get("factor_count") == 8

def test_f26_held():
    rec = json.loads((DECISION_DIR / "batch3_candidate_review_decision_record.json").read_text())
    assert "F26" in rec.get("held_factors",[])

def test_f27_held():
    rec = json.loads((DECISION_DIR / "batch3_candidate_review_decision_record.json").read_text())
    assert "F27" in rec.get("held_factors",[])

def test_no_promotion():
    for name in ["batch3_candidate_review_decision_record.json","batch3_candidate_review_approved_queue.json","batch3_candidate_review_closeout.json"]:
        d = json.loads((DECISION_DIR / name).read_text())
        assert d.get("promotion_allowed") is False, f"{name}: promotion not false"

def test_no_alpha():
    for name in ["batch3_candidate_review_decision_record.json","batch3_candidate_review_approved_queue.json","batch3_candidate_review_closeout.json"]:
        d = json.loads((DECISION_DIR / name).read_text())
        assert d.get("alpha_claim_allowed") is False, f"{name}: alpha not false"

def test_prod_blocked():
    for name in ["batch3_candidate_review_decision_record.json","batch3_candidate_review_closeout.json"]:
        d = json.loads((DECISION_DIR / name).read_text())
        assert d.get("production") == "BLOCKED"
        assert d.get("broker_runtime") == "BLOCKED"
        assert d.get("real_trade") == "BLOCKED"

def test_no_composite():
    d = json.loads((DECISION_DIR / "batch3_candidate_review_closeout.json").read_text())
    assert d.get("multi_factor_composite_built") is False
    assert d.get("weight_optimization_executed") is False

def test_no_candidate_promotion():
    d = json.loads((DECISION_DIR / "batch3_candidate_review_closeout.json").read_text())
    assert d.get("candidate_promotion_executed") is False

def test_safety_0():
    s = json.loads((DECISION_DIR / "batch3_candidate_review_safety_audit.json").read_text())
    assert s.get("violation_count", 999) == 0
    for k,v in s.get("checks",{}).items(): assert v is True, f"check failed: {k}"

def test_next_entry():
    co = json.loads((DECISION_DIR / "batch3_candidate_review_closeout.json").read_text())
    n = co.get("next_legal_entry", "")
    assert "MONITORING" in n or "QUEUE" in n

def test_hold_has_unlock_conditions():
    hq = json.loads((DECISION_DIR / "batch3_candidate_review_hold_queue.json").read_text())
    for f in hq.get("factors", []):
        assert len(f.get("unlock_conditions", [])) > 0, f"{f['factor_id']}: no unlock conditions"

def test_skillos_not_modified():
    r = subprocess.run("git diff --name-only -- skillos", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""

def test_runtime_not_modified():
    r = subprocess.run("git diff --name-only -- runtime_reports", shell=True, capture_output=True, text=True)
    assert r.stdout.strip() == ""
