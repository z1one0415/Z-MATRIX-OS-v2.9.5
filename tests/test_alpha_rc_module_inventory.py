"""Alpha RC Module Inventory tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_rc.module_inventory import build_v3_alpha_frozen_module_inventory

def test_module_inventory_contains_8_core_packages():
    i = build_v3_alpha_frozen_module_inventory()
    assert len(i["frozen_modules"]) == 8
    assert len(i["runtime_disabled_modules"]) == 8
    print(f"✅ inventory has {len(i['frozen_modules'])} frozen modules")

def test_module_inventory_all_preview_or_runtime_disabled():
    i = build_v3_alpha_frozen_module_inventory()
    assert len(i["preview_only_modules"]) >= 4
    assert len(i["runtime_disabled_modules"]) == 8
    print("✅ all modules preview/runtime-disabled")

if __name__ == "__main__":
    test_module_inventory_contains_8_core_packages()
    test_module_inventory_all_preview_or_runtime_disabled()
    print("\n🏁 Alpha RC Module Inventory tests PASS")
