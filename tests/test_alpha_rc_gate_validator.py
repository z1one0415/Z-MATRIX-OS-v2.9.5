"""Alpha RC Gate Validator tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_rc.rc_gate_validator import validate_v3_alpha_rc_gate

def test_rc_gate_passes():
    r = validate_v3_alpha_rc_gate()
    assert r["pass"] is True, f"violations: {r.get('violations', [])}"
    print("✅ RC gate passes")

def test_rc_gate_runtime_false():
    r = validate_v3_alpha_rc_gate()
    assert r["runtime_enabled"] is False
    print("✅ runtime_enabled=False")

def test_rc_gate_real_trade_false():
    r = validate_v3_alpha_rc_gate()
    assert r["real_trade_allowed"] is False
    print("✅ real_trade_allowed=False")

def test_rc_gate_rejects_manifest_auto_sell_true():
    import zmatrix.alpha_rc.rc_gate_validator as v
    original = v.build_v3_alpha_release_manifest
    def bad_manifest():
        m = original()
        m["safety"]["auto_sell_allowed"] = True
        return m
    v.build_v3_alpha_release_manifest = bad_manifest
    try:
        r = v.validate_v3_alpha_rc_gate()
        assert r["pass"] is False
        assert any("manifest.safety.auto_sell_allowed" in x for x in r["violations"])
    finally:
        v.build_v3_alpha_release_manifest = original
    print("✅ rejects manifest.safety.auto_sell_allowed=True")

def test_rc_gate_rejects_module_inventory_hermes_write_true():
    import zmatrix.alpha_rc.rc_gate_validator as v
    original = v.build_v3_alpha_frozen_module_inventory
    def bad_inventory():
        inv = original()
        inv["safety"]["hermes_memory_write_allowed"] = True
        return inv
    v.build_v3_alpha_frozen_module_inventory = bad_inventory
    try:
        r = v.validate_v3_alpha_rc_gate()
        assert r["pass"] is False
        assert any("module_inventory.safety.hermes_memory_write_allowed" in x for x in r["violations"])
    finally:
        v.build_v3_alpha_frozen_module_inventory = original
    print("✅ rejects module_inventory.safety.hermes_memory_write_allowed=True")

def test_rc_gate_rejects_dry_run_runtime_true():
    import zmatrix.alpha_rc.rc_gate_validator as v
    original = v.build_v3_alpha_dry_run_report
    def bad_dry_run():
        d = original()
        d["runtime_enabled"] = True
        return d
    v.build_v3_alpha_dry_run_report = bad_dry_run
    try:
        r = v.validate_v3_alpha_rc_gate()
        assert r["pass"] is False
        assert any("dry_run_report.runtime_enabled" in x for x in r["violations"])
    finally:
        v.build_v3_alpha_dry_run_report = original
    print("✅ rejects dry_run_report.runtime_enabled=True")

def test_rc_gate_rejects_non_dict_manifest_safety():
    import zmatrix.alpha_rc.rc_gate_validator as v
    original = v.build_v3_alpha_release_manifest
    def bad_manifest():
        m = original()
        m["safety"] = "bad"
        return m
    v.build_v3_alpha_release_manifest = bad_manifest
    try:
        r = v.validate_v3_alpha_rc_gate()
        assert r["pass"] is False
        assert any("manifest.safety must be dict" in x for x in r["violations"])
    finally:
        v.build_v3_alpha_release_manifest = original
    print("✅ rejects non-dict manifest.safety")

if __name__ == "__main__":
    test_rc_gate_passes()
    test_rc_gate_runtime_false()
    test_rc_gate_real_trade_false()
    test_rc_gate_rejects_manifest_auto_sell_true()
    test_rc_gate_rejects_module_inventory_hermes_write_true()
    test_rc_gate_rejects_dry_run_runtime_true()
    test_rc_gate_rejects_non_dict_manifest_safety()
    print("\n🏁 Alpha RC Gate Validator tests PASS")
