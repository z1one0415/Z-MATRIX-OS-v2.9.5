from pathlib import Path
SCRIPT = Path("scripts/verify_v40_hardening_c2_all.sh")

def _s(): return SCRIPT.read_text(encoding="utf-8")
def _idx(text, token):
    i = text.find(token)
    assert i >= 0, f"Missing: {token}"
    return i

def test_all_required_blocks_present():
    t = _s()
    for token in ["verify_v40_hardening_b.sh","test_truth_matrix_consistency.py","test_depth_modules.py","test_execution_account_depth.py","irf01_full_chain","irf03_factor_chain","irf04_execution_chain","test_hardening_c_integration.py","verify_v40_hardening_c2_1_truth_closeout.sh","test_asset_matrix_truth_sync.py","test_verify_chain_closure.py"]:
        assert token in t, f"Missing block: {token}"

def test_pass_is_last():
    t = _s()
    pidx = _idx(t, "Hardening-C2 PASS")
    for token in ["verify_v40_hardening_c2_1_truth_closeout.sh","test_asset_matrix_truth_sync.py","test_verify_chain_closure.py","Truth report + extended forbidden"]:
        assert _idx(t, token) < pidx, f"{token} must run before final PASS"

def test_no_tail_swallow():
    t = _s()
    tail_count = t.count("| tail"); assert tail_count <= 1, f"Too many tail usages: {tail_count}"

def test_depth_modules_not_blank():
    t = _s()
    assert "test_depth_modules.py" in t and "pytest" in t.split("test_depth_modules.py")[1][:200]

def test_forbidden_scan_6_flags():
    t = _s()
    for f in ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        assert f in t

def test_c2_1_verify_strict():
    t = Path("scripts/verify_v40_hardening_c2_1_truth_closeout.sh").read_text(encoding="utf-8")
    assert "False ACCEPTANCE_DONE" in t
    assert ".count(" not in t

def test_smoke_candidate_unchanged():
    t = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
    assert ("INTEGRATION_SMOKE_CANDIDATE" in t) or ("INTEGRATION_COMPLETE_CANDIDATE" in t)
    assert "RC1 status: NOT_APPROVED" in t or "NOT_APPROVED" in t
    assert "RC1 status: APPROVED" not in t
