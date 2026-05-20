"""Z-G07 contracts — gate3 details init, gate7 no absolute path, gate7 uses zmatrix.scoring"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg07_gate3_details_initialized_before_loop():
    """gate3_dq_score: details dict must be initialized before try/except blocks write to it"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate3 = source.split("def gate3_dq_score")[1].split("def gate4")[0]
    # details = {} must appear before the first details["..."] write
    first_write = gate3.find('details["')
    init_line = gate3.find("details = {}")
    assert init_line >= 0, "gate3 missing details = {}"
    assert init_line < first_write, "details = {} at %d must be before details[ write at %d" % (init_line, first_write)
    print("✅ gate3: details = {} initialized before q1_eps write")


def test_zg07_gate7_has_r_matrix_access():
    """gate7 can reach zmatrix.scoring.r_matrix — via direct import or sys.path"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    has_import = "zmatrix.scoring.r_matrix" in gate7
    has_path = "zmatrix/scoring/r_matrix" in gate7
    assert has_import or has_path, "gate7 cannot reach R-Matrix"
    print(f"✅ gate7 R-Matrix access: import={'yes' if has_import else 'no'} path={'yes' if has_path else 'no'}")


def test_zg07_gate7_uses_zmatrix_scoring_or_path():
    """gate7 accesses D-Matrix via zmatrix.scoring import or filesystem path"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    has_d_import = "zmatrix.scoring.d_band" in gate7
    has_d_path = "zmatrix/scoring/d_band" in gate7
    has_r_import = "zmatrix.scoring.r_matrix" in gate7
    has_r_path = "zmatrix/scoring/r_matrix" in gate7
    assert has_d_import or has_d_path, "gate7 cannot reach D-Matrix"
    assert has_r_import or has_r_path, "gate7 cannot reach R-Matrix"
    print(f"✅ gate7 D/R access: import=({has_d_import},{has_r_import}) path=({has_d_path},{has_r_path})")


def test_zg07_gate7_has_minimum_kline_window():
    """gate7 has kline access — 500d(preferred) or 250d(minimum) window"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    has_500 = "get_kline(ticker, 500)" in gate7 or "get_kline(ticker,500)" in gate7
    has_250 = "days=250" in gate7 or "days=500" in gate7
    has_baostock = "query_history_k_data_plus" in gate7
    assert has_500 or has_250 or has_baostock, "gate7 has no kline access"
    print(f"✅ gate7 kline: 500d={'yes' if has_500 else 'no'} 250d={'yes' if has_250 else 'no'} bs={'yes' if has_baostock else 'no'}")



def test_zg07_gate3_industry_chain_uses_details_q1_eps():
    """产业链评分 reads details['q1_eps'], not g1['q1_eps']"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate3 = source.split("def gate3_dq_score")[1].split("def gate4")[0]
    assert 'details.get("q1_eps")' in gate3, "产业链 should read details.q1_eps"
    assert 'g1.get("q1_eps")' not in gate3, "产业链 should NOT read g1.q1_eps"
    print("✅ 产业链: reads details.q1_eps, not g1.q1_eps")

if __name__ == "__main__":
    test_zg07_gate3_details_initialized_before_loop()
    test_zg07_gate7_has_r_matrix_access()
    test_zg07_gate7_uses_zmatrix_scoring_or_path()
    test_zg07_gate3_industry_chain_uses_details_q1_eps()
    test_zg07_gate7_has_minimum_kline_window()
    print("\n🏁 Z-G07 contracts tests PASS")
