def test_memory_candidate_from_intake():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    from zmatrix.research_db.zg16_review_contract import build_zg16_review_card
    from zmatrix.research_db.zg16_autocaseforge_intake_adapter import build_autocaseforge_intake_draft
    from zmatrix.research_db.zg16_memory_candidate_adapter import build_monthly_memory_candidate
    chain = run_zg16_e2e_stub_chain("600519")
    card = build_zg16_review_card(chain)
    intake = build_autocaseforge_intake_draft(card)
    mc = build_monthly_memory_candidate(intake)
    assert mc["memory_status"] == "CANDIDATE_ONLY"
    assert mc["human_review_required"] is True
    assert mc["memory_main_write"] is False
    assert mc["researchdb_main_write"] is False
    assert mc["production_allowed"] is False
    assert mc["trade_allowed"] is False
