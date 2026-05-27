from zmatrix.strategy_repair.return_unit_guard import normalize_return_display_value

def test_return_unit_display_not_double_scaled():
    r = normalize_return_display_value(1.5086)
    assert r["display_pct"] == 1.5086
    assert r["display_text"] == "+1.51%"
    assert r["must_not_multiply_by_100"] is True
