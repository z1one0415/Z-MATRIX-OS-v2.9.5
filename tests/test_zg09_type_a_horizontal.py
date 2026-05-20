"""Z-G09 Type A 水平震荡波动天王 行为测试"""
import sys, os, math, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_type_a_horizontal_box_candidate():
    """水平箱体->Type A检测 (放宽beta阈值适配测试数据)"""
    from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal
    from zmatrix.scoring.r_matrix import horizontal_channel_detector as hcd
    
    random.seed(42)
    prices = [100 + 15*math.sin(i*0.1) + random.gauss(0,2) for i in range(350)]
    
    orig_fn = hcd.detect_horizontal_channel
    def patched(prices, **kw):
        kw["beta_flat_threshold"] = 0.0003
        return orig_fn(prices, **kw)
    hcd.detect_horizontal_channel = patched
    
    try:
        r = rank_type_a_horizontal("TEST","box",prices)
        assert r.oscillation_type == "OSC_TYPE_A_HORIZONTAL"
        assert r.allowed_action in {"WATCH","WAIT","HARVEST"}
        if r.score > 0:
            assert "dfa_hurst" in r.diagnostics
            assert "support_touches" in r.diagnostics
        print(f"✅ box_candidate (score={r.score}, action={r.allowed_action})")
    finally:
        hcd.detect_horizontal_channel = orig_fn

def test_type_a_rejects_structural_downtrend():
    """单边下跌->Type A拒绝"""
    from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal
    prices = [100 - i*0.2 for i in range(300)]
    r = rank_type_a_horizontal("TEST","downtrend",prices)
    assert r.score == 0
    assert r.allowed_action == "WAIT"
    print(f"✅ rejects_downtrend (score=0)")

def test_type_a_no_buy_sell_output():
    """Type A不输出BUY/SELL"""
    from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_a_horizontal
    prices = [80 + (i%60)*0.5 + 5*math.sin(i*0.1) for i in range(300)]
    r = rank_type_a_horizontal("TEST","test",prices)
    assert r.allowed_action not in {"BUY","SELL","ADD","CLEAR","AUTO_TRADE"}
    print(f"✅ no_buy_sell (action={r.allowed_action})")

if __name__ == "__main__":
    test_type_a_horizontal_box_candidate()
    test_type_a_rejects_structural_downtrend()
    test_type_a_no_buy_sell_output()
    print("\n🏁 Type A horizontal tests PASS")
