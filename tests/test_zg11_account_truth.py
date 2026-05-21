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
        f.write("| 双环传动 002472 | 100股 | 44.01 |\n")
        f.write("| 紫金矿业 601899 | 140股 | 31.00 |\n")
        f.write("| 贵州茅台 600519 | 3股 | 1500.00 |\n")
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__("pathlib").Path(mem_path)
        prices = {
            "002472": {"status": "PASS", "price": 44, "name": "双环传动"},
            "601899": {"status": "PASS", "price": 31, "name": "紫金矿业"},
            "600519": {"status": "PASS", "price": 1500, "name": "贵州茅台"},
        }
        mod.market_truth = lambda t: prices[t]
        
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


def test_zg11_degraded_when_concentrated()
    test_zg11_uses_chain_taxonomy_provider_for_consumer_brand()
    test_zg11_no_local_hardcoded_chain_table():
    spec = importlib.util.spec_from_file_location("zg11", "pipelines/Z-G11_组合风控/gate_pipeline.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
        # 70%+ concentration triggers warning
        f.write("| 双环传动 002472 | 1800股 | 44.01 |\n" * 5)
        mem_path = f.name
    
    try:
        mod.MEMORY_MD = __import__("pathlib").Path(mem_path)
        prices = {
            "002472": {"status": "PASS", "price": 44, "name": "双环传动"},
            "601899": {"status": "PASS", "price": 31, "name": "紫金矿业"},
            "600519": {"status": "PASS", "price": 1500, "name": "贵州茅台"},
        }
        mod.market_truth = lambda t: prices[t]
        
        r = mod.run()
        assert r["status"] == "DEGRADED_ACCOUNT_TRUTH_REQUIRED", f"got {r['status']}"
        assert r["sections"]["action"] == "RISK_ALERT_REQUIRES_ACCOUNT_CONFIRMATION"
        assert "suggested_human_check" in r["sections"]
        print(f"✅ concentration→DEGRADED_ACCOUNT_TRUTH_REQUIRED")
    finally:
        os.unlink(mem_path)




def test_zg11_uses_chain_taxonomy_provider_for_consumer_brand():
    import tempfile
    from pathlib import Path
    spec = importlib.util.spec_from_file_location('zg11','pipelines/Z-G11_组合风控/gate_pipeline.py')
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    with tempfile.NamedTemporaryFile(mode='w',suffix='.md',delete=False) as f:
        f.write('| 贵州茅台 600519 | 3股 | 1500.00 |\n')
        f.write('| 五粮液 000858 | 20股 | 220.00 |\n')
        f.write('| 双环传动 002472 | 100股 | 44.01 |\n')
        mem_path = f.name
    try:
        mod.MEMORY_MD = Path(mem_path)
        prices = {
            '600519':{'status':'PASS','price':1500,'name':'贵州茅台','industry':'食品饮料'},
            '000858':{'status':'PASS','price':220,'name':'五粮液','industry':'食品饮料'},
            '002472':{'status':'PASS','price':44,'name':'双环传动','industry':'机器人'},
        }
        mod.market_truth = lambda t: prices[t]
        r = mod.run()
        positions = r['sections']['positions']
        mt = [p for p in positions if p['code']=='600519'][0]
        wy = [p for p in positions if p['code']=='000858'][0]
        assert mt['chain'] == '消费品牌', f'茅台 chain={mt["chain"]}'
        assert wy['chain'] == '消费品牌', f'五粮液 chain={wy["chain"]}'
        assert mt['chain_detail']['primary_chain'] == '消费品牌'
        assert 'industry' in mt
        print(f'✅ 茅台→{mt["chain"]} 五粮液→{wy["chain"]}')
    finally:
        os.unlink(mem_path)

def test_zg11_no_local_hardcoded_chain_table():
    source = open('pipelines/Z-G11_组合风控/gate_pipeline.py',encoding='utf-8').read()
    assert 'chain_taxonomy_provider' in source
    assert 'match_chain_detail' in source
    assert '"AI算力":[' not in source
    assert '"机器人":[' not in source
    assert '"资源":[' not in source
    print('✅ Z-G11: no hardcoded chain table, uses chain_taxonomy_provider')

if __name__ == "__main__":
    test_zg11_no_positions_returns_data_gap()
    test_zg11_positions_ok_returns_pass_proxy()
    test_zg11_never_outputs_reduce_risk()
    test_zg11_degraded_when_concentrated()
    test_zg11_uses_chain_taxonomy_provider_for_consumer_brand()
    test_zg11_no_local_hardcoded_chain_table()
    print("\n🏁 Z-G11 account truth contract tests PASS")
