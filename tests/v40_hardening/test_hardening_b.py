"""Hardening-B integration tests — real_trade_allowed lock + acceptance matrix truth"""
from pathlib import Path

def test_no_real_trade_allowed_expression():
    src = Path("zmatrix/scoring/dispatcher.py").read_text(encoding="utf-8")
    for bad in ['real_trade_allowed=r_mode == "human_confirm"',"real_trade_allowed=r_mode == 'human_confirm'",'real_trade_allowed=d_mode == "human_confirm"',"real_trade_allowed=d_mode == 'human_confirm'","real_trade_allowed=True"]:
        assert bad not in src, f"Forbidden pattern still in dispatcher: {bad}"

def test_limit_board_integration():
    from zmatrix.zc40.limit_board_fillability import LimitBoardFillabilityGate
    lb = LimitBoardFillabilityGate()
    r = lb.check({'open':10,'high':10,'low':10,'close':10}, 9.09)
    assert r['status']=='NOT_FILLABLE' and r['blocks_new_entry']==True and r['real_trade_allowed']==False

def test_proxy_hedge_integration():
    from zmatrix.zc45.proxy_hedge_stress import ProxyHedgeStressTest
    ph = ProxyHedgeStressTest()
    r = ph.run(['gold'])
    assert r['status']=='CORRELATION_BREAKDOWN' and r['market_neutral_claim']=='FORBIDDEN' and r['real_trade_allowed']==False

def test_catalyst_integration():
    from zmatrix.zc35.catalyst_lifecycle import CatalystLifecycleEngine
    cl = CatalystLifecycleEngine()
    r = cl.classify({'publish_time':'2026-05-29','evidence_level':'B'})
    assert r['direct_trade_allowed']==False and r['real_trade_allowed']==False

def test_failover_integration():
    from zmatrix.runtime.failover import LLMProviderFailoverPolicy
    fp = LLMProviderFailoverPolicy()
    result, report = fp.execute_with_failover("t1", lambda p: (_ for _ in ()).throw(Exception("fail")))
    assert result is None and report.final_status=="FAILED_CLOSED" and report.new_judgement_generated==False

def test_acceptance_matrix_truthful():
    text = Path("docs/upgrade/V40_FULL_SCOPE_ACCEPTANCE_MATRIX.md").read_text(encoding="utf-8")
    assert "SMOKE_DONE" in text or "PARTIAL" in text
    assert "Current release status: SMOKE_PROTOTYPE" in text

def test_content_asset_index_truthful():
    text = Path("docs/upgrade/V40_CONTENT_ASSET_INDEX.md").read_text(encoding="utf-8")
    assert "REGISTRY_ONLY" in text or "SMOKE_DONE" in text

def test_closeout_truth_report():
    t = Path("docs/release/V40_CLOSEOUT_TRUTH_REPORT.md")
    assert t.exists()
    c = t.read_text(encoding="utf-8")
    assert ("SMOKE_PROTOTYPE" in c or "INTEGRATION_COMPLETE_CANDIDATE" in c) and "NOT_APPROVED" in c and "BLOCKED" in c

def test_shim_delegates():
    from zmatrix.runtime.batch3_gates import LimitBoardFillabilityGate as LB1
    from zmatrix.zc40.limit_board_fillability import LimitBoardFillabilityGate as LB2
    assert LB1 is LB2
