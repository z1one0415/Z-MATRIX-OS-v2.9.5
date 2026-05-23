"""G07 behavior tests — actual function calls, not source grep"""
import sys, os, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_gate5_uses_z01_not_sina():
    spec = importlib.util.spec_from_file_location("zg07_gate", "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    # Monkeypatch get_sectors
    mod.get_sectors = lambda: {"sectors": 5, "status": "PASS"}
    r = mod.gate5_l3_sectors()
    assert r.gate_id == 5
    assert r.status.name in ("PASS", "DATA_INCOMPLETE")
    assert r.details.get("source") == "Z-G01.get_sectors"
    print(f"✅ gate5: status={r.status.name} sectors={r.details.get('sectors_available')}")

def test_gate6_uses_z01_not_baostock():
    spec = importlib.util.spec_from_file_location("zg07_gate", "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    # Monkeypatch l4_health
    mod.l4_health = lambda t: {"status": "PASS", "name": "测试", "is_st": False, "errors": []}
    r = mod.gate6_l4_health("002472")
    assert r.gate_id == 6
    assert r.details.get("source") == "Z-G01"
    print(f"✅ gate6: status={r.status.name} name={r.details.get('name')}")

def test_gate7_r_matrix_deferred():
    spec = importlib.util.spec_from_file_location("zg07_gate", "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.get_kline = lambda t,d: {"prices": [10]*300, "volume": [1000]*300, "count": 300,
                                  "close": [10]*300, "open": [10]*300, "high": [11]*300, "low": [9]*300,
                                  "amount": [10000]*300, "dates": ["2026-05-20"]*300}
    r = mod.gate7_l5_matrix("002472", {"name": "双环传动"})
    assert r.details.get("r_matrix") == "deferred_to_g09"
    assert r.details.get("r_score") is None
    print(f"✅ gate7: r_matrix={r.details['r_matrix']} source={r.details.get('matrix_source')}")

if __name__ == "__main__":
    test_gate5_uses_z01_not_sina()
    test_gate6_uses_z01_not_baostock()
    test_gate7_r_matrix_deferred()
    print("\n🏁 Z-G07 data channel tests PASS")
