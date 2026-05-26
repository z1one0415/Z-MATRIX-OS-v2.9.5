"""Hermes Adapter Registry tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.hermes_adapter_registry import list_hermes_adapters, check_hermes_adapter_registry_integrity

def test_registry_exists():
    a=list_hermes_adapters(); assert len(a)>=2; print(f"✅ {len(a)} adapters")

def test_no_real_trade():
    for a in list_hermes_adapters().values():
        assert not a.get("real_trade_allowed"), f"real_trade in {a}"
    print("✅ no real trade")

def test_no_auto_calibration():
    for a in list_hermes_adapters().values():
        assert not a.get("auto_calibration_allowed")
    print("✅ no auto calibration")

def test_no_write():
    for a in list_hermes_adapters().values():
        assert not a.get("write_allowed")
    print("✅ no write allowed")

def test_integrity_clean():
    v=check_hermes_adapter_registry_integrity(); assert len(v)==0, f"{v}"
    print("✅ integrity clean")

def test_doc_exists():
    from pathlib import Path; assert Path("docs/architecture/HERMES_ADAPTER_REGISTRY_V10.md").exists()
    print("✅ doc exists")

if __name__ == "__main__":
    test_registry_exists(); test_no_real_trade(); test_no_auto_calibration()
    test_no_write(); test_integrity_clean(); test_doc_exists()
    print("\n🏁 Hermes Adapter Registry — tests PASS")
