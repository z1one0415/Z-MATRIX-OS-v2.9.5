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

def test_hermes_memory_bank_not_modified_in_workspace_alignment():
    import subprocess
    r = subprocess.run(
        ["git", "diff", "--name-only", "v2.9.9-dev...HEAD"],
        capture_output=True, text=True, check=True,
    )
    changed = set(r.stdout.splitlines())
    assert "hermes/memory_bank.json" not in changed, \
        f"hermes/memory_bank.json modified in {sorted(changed)}"
    print("✅ hermes memory_bank.json not modified in v2.9.9-dev...HEAD")

def test_hermes_adapter_is_inventory_only_policy():
    from zmatrix.architecture.hermes_adapter_registry import HERMES_ADAPTER_REGISTRY
    for aid, adapter in HERMES_ADAPTER_REGISTRY.items():
        assert adapter.get("write_allowed") is False, f"{aid}: write_allowed"
        assert adapter.get("auto_calibration_allowed") is False, f"{aid}: auto_calibration"
        assert adapter.get("real_trade_allowed") is False, f"{aid}: real_trade"
        assert adapter.get("runtime_mode") in ("preview_only", "read_only", "inventory_only"), \
            f"{aid}: runtime_mode={adapter.get('runtime_mode')}"
    print("✅ all adapters inventory-only policy enforced")

if __name__ == "__main__":
    test_registry_exists(); test_no_real_trade(); test_no_auto_calibration()
    test_no_write(); test_integrity_clean(); test_doc_exists()
    test_hermes_memory_bank_not_modified_in_workspace_alignment()
    test_hermes_adapter_is_inventory_only_policy()
    print("\n🏁 Hermes Adapter Registry — tests PASS")
