"""Z-G11 account truth contract — no REDUCE_RISK, status reflects account reality"""
import sys, os, tempfile, json, importlib.util
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_zg11_no_positions_returns_data_gap():
    spec = importlib.util.spec_from_file_location("zg11", "pipelines/Z-G11_组合风控/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("")  # no positions
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__("pathlib").Path(mem_path)
        r = mod.run()
        assert r["status"] == "DATA_GAP"
        assert r["sections"]["reason"] == "NO_POSITION_DATA"
        assert r["sections"]["action"] == "NO_ACCOUNT_TRUTH"
        assert r["sections"]["account_truth"]["connected"] is False
        print(f"✅ no positions→DATA_GAP NO_ACCOUNT_TRUTH")
    finally:
        os.unlink(mem_path)


def test_zg11_positions_ok_returns_pass_proxy():
    spec = importlib.util.spec_from_file_location("zg11", "pipelines/Z-G11_组合风控/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        f.write("| 双环传动 002472 | 1800股 | 44.01 |\n")
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__("pathlib").Path(mem_path)
        mod.market_truth = lambda t: {"status": "PASS", "price": 44, "name": "双环传动"}
        
        r = mod.run()
        assert r["status"] == "PASS_PROXY", f"got {r['status']}"
        assert r["sections"]["action"] == "PORTFOLIO_OK_PROXY"
        assert r["sections"]["account_truth"]["connected"] is False
        assert r["sections"]["account_truth"]["confidence"] == "LOW_ACCOUNT_TRUTH"
        print(f"✅ positions OK→PASS_PROXY")
    finally:
        os.unlink(mem_path)


def test_zg11_never_outputs_reduce_risk():
    """Verify no REDUCE_RISK in any Z-G11 output path"""
    source = open("pipelines/Z-G11_组合风控/gate_pipeline.py", encoding="utf-8").read()
    assert "REDUCE_RISK" not in source, "Z-G11 still contains REDUCE_RISK"
    print("✅ Z-G11: no REDUCE_RISK anywhere in source")


def test_zg11_degraded_when_concentrated():
    spec = importlib.util.spec_from_file_location("zg11", "pipelines/Z-G11_组合风控/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        # 70%+ concentration triggers warning
        f.write("| 双环传动 002472 | 1800股 | 44.01 |\n" * 5)
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__("pathlib").Path(mem_path)
        mod.market_truth = lambda t: {"status": "PASS", "price": 44, "name": "双环传动"}
        
        r = mod.run()
        assert r["status"] == "DEGRADED_ACCOUNT_TRUTH_REQUIRED", f"got {r['status']}"
        assert r["sections"]["action"] == "RISK_ALERT_REQUIRES_ACCOUNT_CONFIRMATION"
        assert "suggested_human_check" in r["sections"]
        print(f"✅ concentration→DEGRADED_ACCOUNT_TRUTH_REQUIRED")
    finally:
        os.unlink(mem_path)


if __name__ == "__main__":
    test_zg11_no_positions_returns_data_gap()
    test_zg11_positions_ok_returns_pass_proxy()
    test_zg11_never_outputs_reduce_risk()
    test_zg11_degraded_when_concentrated()
    print("\n🏁 Z-G11 account truth contract tests PASS")
