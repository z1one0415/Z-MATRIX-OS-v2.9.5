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


def test_zg07_gate7_fail_closed_no_absolute_path():
    """gate7 must NOT use ~/.openclaw or filesystem path to access scorers"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    assert "~/.openclaw/agents" not in gate7, "gate7 uses ~/.openclaw absolute path"
    assert "zmatrix/scoring/" not in gate7, "gate7 should import via package, not filesystem path"
    assert "zmatrix.scoring.d_band" in gate7, "gate7 missing d_band import"
    assert "zmatrix.scoring.r_matrix" in gate7, "gate7 missing r_matrix import"
    print("✅ gate7: package imports only, no ~/.openclaw or filesystem path")


def test_zg07_gate7_uses_dmatrix_payload_builder():
    """gate7 uses build_dmatrix_payload, not inline payload dict"""
    source = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", encoding="utf-8").read()
    gate7 = source.split("def gate7_l5_matrix")[1].split("def gate8")[0]
    assert "build_dmatrix_payload" in gate7, "gate7 should use shared payload builder"
    print("✅ gate7: uses build_dmatrix_payload")


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


def test_zg07_gate3_q1_eps_preserved_in_details_runtime():
    """q1_eps written then details.update() — must not be overwritten"""
    import importlib.util, sys, types

    # Mock baostock before loading module
    class FakeRS:
        def __init__(self):
            self.used = False
        def next(self):
            if not self.used:
                self.used = True
                return True
            return False
        def get_row_data(self):
            return ["", "", "", "0.50"]

    class FakeBS:
        def login(self): pass
        def logout(self): pass
        def query_profit_data(self, *a, **kw): return FakeRS()
        def query_stock_industry(self, *a, **kw): return FakeRS()

    sys.modules["baostock"] = FakeBS()

    spec = importlib.util.spec_from_file_location("zg07", "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    mod.g1_details_for = lambda t: {"price": 10, "cross_validated": True, "volume": 100000}

    r = mod.gate3_dq_score("002463")

    assert r.details.get("q1_eps") == "0.50", f"q1_eps lost: {r.details}"
    assert "total" in r.details
    assert "breakdown" in r.details
    assert r.details["breakdown"]["产业链"] == 12, f"chain score should be 12: {r.details['breakdown']}"
    print(f"✅ q1_eps={r.details['q1_eps']} preserved, 产业链={r.details['breakdown']['产业链']}")

if __name__ == "__main__":
    test_zg07_gate3_details_initialized_before_loop()
    test_zg07_gate7_fail_closed_no_absolute_path()
    test_zg07_gate7_uses_dmatrix_payload_builder()
    test_zg07_gate3_industry_chain_uses_details_q1_eps()
    test_zg07_gate3_q1_eps_preserved_in_details_runtime()
    test_zg07_gate7_has_minimum_kline_window()
    print("\n🏁 Z-G07 contracts tests PASS")
