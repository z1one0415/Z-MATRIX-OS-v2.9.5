"""G16-6C tests — Review UI Contract"""
def test_build_review_card_from_chain():
    from zmatrix.research_db.zg16_e2e_stub_chain import run_zg16_e2e_stub_chain
    from zmatrix.research_db.zg16_review_contract import build_zg16_review_card
    chain = run_zg16_e2e_stub_chain("600519")
    card = build_zg16_review_card(chain)
    assert card["production_allowed"] is False
    assert card["trade_allowed"] is False
    assert card["human_review_required"] is True
    assert len(card["required_decision"]) >= 2
    assert len(card["sections"]) >= 3
