"""G16-5 tests — E2E Stub Draft Chain"""
import os, tempfile

def test_e2e_chain_creates_all_4_drafts():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("600519")
    assert r["chain_status"] == "DRAFT_CHAIN_CREATED"
    assert "hypothesis_draft" in r
    assert "annotation_draft" in r
    assert "analysis_zone_draft" in r
    assert "caseforge_draft_proposal" in r

def test_e2e_chain_all_outputs_production_false():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("600519")
    assert r["production_allowed"] is False
    for key in ["hypothesis_draft","annotation_draft","analysis_zone_draft","caseforge_draft_proposal"]:
        assert r[key]["production_allowed"] is False, f"{key} production not false"

def test_e2e_chain_all_outputs_trade_and_verdict_false():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("600519")
    assert r["trade_allowed"] is False
    assert r["verdict_allowed"] is False

def test_e2e_chain_requires_human_review():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("600519")
    assert r["human_review_required"] is True
    assert r["proposal_required"] is True
    assert r["closed"] is False

def test_e2e_chain_does_not_write_runtime_ledgers():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("600519")
    assert r["runtime_ledger_written"] is False
    assert r["researchdb_main_write"] is False

def test_sell_on_news_trap_chain_not_blocked():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("600519", hypothesis_type="SELL_ON_NEWS_TRAP")
    assert r["chain_status"] == "DRAFT_CHAIN_CREATED"

def test_missing_ticker_blocks_chain():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    r = run_zg16_e2e_stub_chain("")
    assert r["chain_status"] == "BLOCKED"
    assert r["quality_status"] == "DATA_INSUFFICIENT"
