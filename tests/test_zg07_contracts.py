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


def test_zg07_gate7_no_absolute_path():
    """gate7 must not reference ~/.openclaw absolute workspace path"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    assert "~/.openclaw" not in gate7, "gate7 still uses ~/.openclaw absolute path"
    assert "os.path.exists(d_script)" not in gate7, "gate7 still checks d_script path existence"
    assert "os.path.exists(r_script)" not in gate7, "gate7 still checks r_script path existence"
    print("✅ gate7: no ~/.openclaw path, no os.path.exists checks")


def test_zg07_gate7_uses_zmatrix_scoring_package():
    """gate7 imports from current zmatrix.scoring, not external paths"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    assert "zmatrix.scoring.d_band" in gate7, "gate7 missing d_band import"
    assert "zmatrix.scoring.r_matrix" in gate7, "gate7 missing r_matrix import"
    assert "get_kline(" in gate7, "gate7 should use get_kline not bs direct"
    assert "rank_type_a_horizontal" in gate7, "gate7 should dual-mode Type A/B"
    print("✅ gate7: zmatrix.scoring imports + get_kline + Type A/B")


def test_zg07_gate7_uses_500_day_kline():
    """gate7 uses >=500 day kline window for Type A support (needs 260+)"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    assert "get_kline(ticker, 500)" in gate7 or "get_kline(ticker,500)" in gate7, \
        "gate7 should use 500-day kline window"
    assert "KLINE_LT_260D" in gate7, "gate7 should check 260-day minimum for Type A"
    print("✅ gate7: 500-day window + 260D minimum check")


if __name__ == "__main__":
    test_zg07_gate3_details_initialized_before_loop()
    test_zg07_gate7_no_absolute_path()
    test_zg07_gate7_uses_zmatrix_scoring_package()
    test_zg07_gate7_uses_500_day_kline()
    print("\n🏁 Z-G07 contracts tests PASS")
