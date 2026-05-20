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
    """均值回归箱体→Type A结构验证"""
    import zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 as ok
    random.seed(42)
    prices = [100.0]
    for i in range(500):
        prices.append(100 + random.gauss(0,15))
    prices = prices[-360:]
    orig = ok.detect_horizontal_channel
    ok.detect_horizontal_channel = lambda p, **kw: orig(p, beta_flat_threshold=0.002)
    try:
        r = ok.rank_type_a_horizontal("TEST","OU",prices)
        assert r.oscillation_type == "OSC_TYPE_A_HORIZONTAL"
        assert r.allowed_action in {"WATCH","WAIT","HARVEST"}
        assert "dfa_hurst" in r.diagnostics  # always present even on fail
        print(f"✅ box (score={r.score}, action={r.allowed_action})")
    finally:
        ok.detect_horizontal_channel = orig

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

if __name__ == "__main__":
    test_type_a_horizontal_box_candidate()
    test_type_a_rejects_structural_downtrend()
    test_type_a_no_buy_sell_output()
    test_type_b_rising_channel_no_attribute_error()
    test_zg09_outputs_subtype_scores()
    print("\n🏁 Type A/B contract tests PASS")
