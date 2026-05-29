from pathlib import Path

def test_c2_all_calls_c2_1_closeout():
    t = Path("scripts/verify_v40_hardening_c2_all.sh").read_text(encoding="utf-8")
    assert "verify_v40_hardening_c2_1_truth_closeout.sh" in t

def test_forbidden_scan_covers_6_flags():
    t = Path("scripts/verify_v40_hardening_c2_all.sh").read_text(encoding="utf-8")
    for token in ["real_trade_allowed=True","broker_order_allowed=True","runtime_enabled=True","auto_buy_allowed=True","auto_sell_allowed=True","production_allowed=True"]:
        assert token in t

def test_c2_1_verify_strict():
    t = Path("scripts/verify_v40_hardening_c2_1_truth_closeout.sh").read_text(encoding="utf-8")
    assert "False ACCEPTANCE_DONE" in t
    assert "count" not in t or "m.count" not in t

def test_release_status_unchanged():
    t = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md").read_text(encoding="utf-8")
    assert "INTEGRATION_SMOKE_CANDIDATE" in t
    assert "RC1 status: NOT_APPROVED" in t
    assert "INTEGRATION_COMPLETE_CANDIDATE" not in t
