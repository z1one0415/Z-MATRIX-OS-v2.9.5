def test_intake_from_review_card():
    from zmatrix.research_db.zg16_review_contract import build_zg16_review_card
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    from zmatrix.research_db.zg16_autocaseforge_intake_adapter import build_autocaseforge_intake_draft
    chain = run_zg16_e2e_stub_chain("600519")
    card = build_zg16_review_card(chain)
    intake = build_autocaseforge_intake_draft(card)
    assert intake["proposal_required"] is True
    assert intake["human_review_required"] is True
    assert intake["production_allowed"] is False
    assert intake["trade_allowed"] is False
    assert intake["autocaseforge_main_write"] is False
    assert intake["runtime_ledger_written"] is False
