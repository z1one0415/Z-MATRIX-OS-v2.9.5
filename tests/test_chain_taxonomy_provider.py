"""Chain taxonomy provider contract tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_moutai_maps_to_consumer_brand_not_resource():
    from pipelines.chain_taxonomy_provider import match_chain_detail
    d = match_chain_detail("600519", "贵州茅台", "食品饮料")
    assert d["primary_chain"] == "消费品牌", f"got {d['primary_chain']}"
    assert d["confidence"] in {"HIGH", "MEDIUM"}
    assert d["match_reason"] in {"code", "industry"}
    print(f"✅ 茅台→{d['primary_chain']} ({d['confidence']})")


def test_wuliangye_maps_to_consumer_brand_not_resource():
    from pipelines.chain_taxonomy_provider import match_chain_detail
    d = match_chain_detail("000858", "五粮液", "食品饮料")
    assert d["primary_chain"] == "消费品牌", f"got {d['primary_chain']}"
    print(f"✅ 五粮液→{d['primary_chain']}")


def test_zijin_maps_to_resource():
    from pipelines.chain_taxonomy_provider import match_chain_detail
    d = match_chain_detail("601899", "紫金矿业", "有色金属")
    assert d["primary_chain"] == "资源周期", f"got {d['primary_chain']}"
    print(f"✅ 紫金→{d['primary_chain']}")


def test_semiconductor_has_secondary_chain():
    from pipelines.chain_taxonomy_provider import match_chain_detail
    d = match_chain_detail("688981", "中芯国际", "半导体")
    assert d["primary_chain"] in {"半导体", "AI算力"}
    assert isinstance(d["secondary_chains"], list)
    print(f"✅ 中芯→{d['primary_chain']} secondary={d['secondary_chains']}")


def test_chain_density_counts_consumer_brand():
    from pipelines.chain_taxonomy_provider import chain_density
    density = chain_density(["600519"], ["贵州茅台"], ["食品饮料"])
    assert density["消费品牌"] == 1
    assert density["资源周期"] == 0
    print(f"✅ density: 消费={density['消费品牌']} 资源={density['资源周期']}")


def test_unmapped_stock_goes_to_blind():
    from pipelines.chain_taxonomy_provider import match_chain_detail, chain_density
    d = match_chain_detail("000001", "平安银行", "银行")
    assert d["primary_chain"] is None
    assert d["confidence"] == "UNMAPPED"
    density = chain_density(["000001"], ["平安银行"], ["银行"])
    assert density["⚠️未映射(盲区)"] == 1
    print(f"✅ 平安银行→UNMAPPED, blind=1")


if __name__ == "__main__":
    test_moutai_maps_to_consumer_brand_not_resource()
    test_wuliangye_maps_to_consumer_brand_not_resource()
    test_zijin_maps_to_resource()
    test_semiconductor_has_secondary_chain()
    test_chain_density_counts_consumer_brand()
    test_unmapped_stock_goes_to_blind()
    print("\n🏁 Chain taxonomy provider tests PASS")
