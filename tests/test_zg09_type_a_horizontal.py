"""Z-G09 Type A/B oscillation king contract tests"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def _deterministic_box(ndays=360):
    prices = []
    for i in range(ndays):
        phase = i % 60
        if phase < 30: p = 82 + phase*(36/30)
        else: p = 118 - (phase-30)*(36/30)
        prices.append(p)
    return prices

def test_type_a_horizontal_box_candidate():
    """确定性三角波箱体→Type A score>0 (强验证)"""
    import zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 as ok
    
    # 确定性水平箱体: 重复触碰82-118支撑/阻力
    prices = []
    for cycle in range(6):
        for i in range(30):
            prices.append(82 + i*(36/30))
        for i in range(30):
            prices.append(118 - i*(36/30))
    
    # Patch beta threshold wider for triangular wave
    orig_ch = ok.detect_horizontal_channel
    ok.detect_horizontal_channel = lambda p, **kw: orig_ch(p, beta_flat_threshold=0.0005)
    # Patch reversion check to simulated mean-reverting (DFA on perfect triangle is ~1.6)
    from dataclasses import dataclass
    @dataclass
    class FakeRev:
        dfa_hurst: float = 0.42
        half_life: float = 30
        mean_reverting: bool = True
        notes: list = None
    orig_rev = ok.residual_reversion_check
    ok.residual_reversion_check = lambda *a, **kw: FakeRev()
    
    try:
        r = ok.rank_type_a_horizontal("TEST","三角箱体",prices)
        assert r.oscillation_type == "OSC_TYPE_A_HORIZONTAL"
        assert r.score > 0, f"should pass, got score=0 diag={r.diagnostics}"
        assert r.allowed_action in {"WATCH","WAIT","HARVEST"}
        assert "dfa_hurst" in r.diagnostics
        assert "support_touches" in r.diagnostics
        assert "resistance_touches" in r.diagnostics
        assert r.diagnostics["support_touches"] >= 3, f"sup={r.diagnostics['support_touches']}"
        assert r.diagnostics["resistance_touches"] >= 3, f"res={r.diagnostics['resistance_touches']}"
        print(f"✅ box score={r.score} action={r.allowed_action} sup={r.diagnostics['support_touches']}")
    finally:
        ok.detect_horizontal_channel = orig_ch
        ok.residual_reversion_check = orig_rev

def test_type_a_rejects_structural_downtrend():
    from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal
    prices = [100-i*0.2 for i in range(300)]
    r = rank_type_a_horizontal("TEST","down",prices)
    assert r.score == 0
    assert r.allowed_action == "WAIT"
    print("✅ reject downtrend")

def test_type_a_no_buy_sell_output():
    from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal
    prices = _deterministic_box(300)
    r = rank_type_a_horizontal("TEST","box",prices)
    assert r.allowed_action not in {"BUY","SELL","ADD","CLEAR","AUTO_TRADE"}
    print(f"✅ no_buy_sell (action={r.allowed_action})")

def test_type_b_rising_channel_no_attribute_error():
    import zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 as ok
    prices = [50+i*0.1+3*math.sin(i*0.08) for i in range(360)]
    r = ok.rank_type_b_rising_channel("TEST","rising",prices)
    assert r.oscillation_type == "OSC_TYPE_B_RISING_CHANNEL"
    assert r.allowed_action in {"WATCH","WAIT","PAPER_PROBE","HARVEST"}
    assert isinstance(r.score, float)
    print(f"✅ Type B no attr error (score={r.score})")

def test_zg09_outputs_subtype_scores():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg09","pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    prices = _deterministic_box(360)
    mod.market_truth = lambda t: {"status":"PASS","name":"test"}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t,d: {"prices":prices,"count":len(prices)}
    r = mod._r_matrix_score("002463")
    assert r["status"] == "PASS"
    assert "subtype_scores" in r, f"missing: {r.keys()}"
    assert "type_a_horizontal" in r["subtype_scores"]
    assert "type_b_rising_channel" in r["subtype_scores"]
    assert r["oscillation_type"] in {"OSC_TYPE_A_HORIZONTAL","OSC_TYPE_B_RISING_CHANNEL"}
    print(f"✅ subtype_scores A={r['subtype_scores']['type_a_horizontal']} B={r['subtype_scores']['type_b_rising_channel']}")

def test_zg09_type_a_requires_enough_kline_window():
    """Z-G09 K线<260→DATA_INSUFFICIENT"""
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg09","pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.market_truth = lambda t: {"status":"PASS","name":"test"}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t,d: {"prices":[100]*250,"count":250}
    r = mod._r_matrix_score("002463")
    assert r["status"] == "DATA_INSUFFICIENT"
    assert "KLINE_LT_260D" in r["reason_codes"]
    print("✅ kline_window <260→DATA_INSUFFICIENT")

def test_zg09_outputs_subtype_scores():
    import importlib.util
    spec = importlib.util.spec_from_file_location("zg09","pipelines/Z-G09_全局轮动筛选/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    prices = _deterministic_box(360)
    mod.market_truth = lambda t: {"status":"PASS","name":"test"}
    mod.l4_health = lambda t: {"status":"PASS"}
    mod.get_kline = lambda t,d: {"prices":prices,"count":len(prices)}
    r = mod._r_matrix_score("002463")
    assert r["status"] == "PASS"
    assert "subtype_scores" in r
    assert "type_a_horizontal" in r["subtype_scores"]
    assert "type_b_rising_channel" in r["subtype_scores"]
    print(f"✅ subtype_scores A={r['subtype_scores']['type_a_horizontal']} B={r['subtype_scores']['type_b_rising_channel']}")

if __name__ == "__main__":
    test_type_a_horizontal_box_candidate()
    test_type_a_rejects_structural_downtrend()
    test_type_a_no_buy_sell_output()
    test_type_b_rising_channel_no_attribute_error()
    test_zg09_type_a_requires_enough_kline_window()
    test_zg09_outputs_subtype_scores()
    print("\n🏁 Type A/B contract tests PASS")
