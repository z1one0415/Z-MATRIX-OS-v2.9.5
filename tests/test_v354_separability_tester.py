from zmatrix.invalidation_anatomy.separability_tester import test_path_separability

def test_separability_data_insufficient():
    r = test_path_separability(anatomy_rows=[])
    assert r["separability_status"] == "DATA_INSUFFICIENT"
    assert r["real_trade_allowed"] is False
