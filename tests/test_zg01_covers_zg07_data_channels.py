"""Verify G07 no longer imports baostock/Sina/old R-Matrix"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_g07_no_baostock_import():
    s = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py").read()
    assert "import baostock" not in s, "G07 still imports baostock"
    print("✅ no baostock")

def test_g07_no_sina_direct():
    s = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py").read()
    assert "hq.sinajs.cn" not in s, "G07 still accesses Sina"
    assert "urllib.request" not in s, "G07 still uses urllib"
    print("✅ no Sina/urllib")

def test_g07_no_old_rmatrix():
    s = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py").read()
    assert "oscillation_king_ranker_v11" not in s, "G07 still imports old R-Matrix"
    assert "rank_type_a_horizontal" not in s, "G07 still calls Type A"
    assert "rank_type_b_rising_channel" not in s, "G07 still calls Type B"
    print("✅ no old R-Matrix")

def test_g07_uses_z17_loader():
    s = open("pipelines/Z-G07_轮动黑马选股/gate_pipeline.py").read()
    assert "z17_loader" in s or "from pipelines.z17_loader" in s, "G07 doesn't use z17_loader"
    print("✅ uses z17_loader")

if __name__ == "__main__":
    test_g07_no_baostock_import()
    test_g07_no_sina_direct()
    test_g07_no_old_rmatrix()
    test_g07_uses_z17_loader()
    print("\n🏁 Z-G07 data channel tests PASS")
