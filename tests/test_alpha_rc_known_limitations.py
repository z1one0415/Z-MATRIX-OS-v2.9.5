"""Alpha RC Known Limitations tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_rc.known_limitations import build_v3_alpha_known_limitations

def test_known_limitations_at_least_10_items():
    l = build_v3_alpha_known_limitations()
    assert len(l["limitations"]) >= 10
    print(f"✅ {len(l['limitations'])} limitations")

def test_known_limitations_says_not_live_trading():
    l = build_v3_alpha_known_limitations()
    assert any("not a live trading" in x.lower() for x in l["limitations"])
    print("✅ limitations state not a live trading system")

if __name__ == "__main__":
    test_known_limitations_at_least_10_items()
    test_known_limitations_says_not_live_trading()
    print("\n🏁 Alpha RC Known Limitations tests PASS")
