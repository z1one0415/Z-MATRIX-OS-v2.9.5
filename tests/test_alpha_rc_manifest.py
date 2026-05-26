"""Alpha RC Manifest tests"""
import sys, os; sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_rc.manifest_builder import build_v3_alpha_release_manifest

def test_manifest_contains_v2910_to_v2917():
    m = build_v3_alpha_release_manifest()
    assert len(m["frozen_version_range"]) == 8
    assert "v2.9.10-dev" in m["frozen_version_range"]
    assert "v2.9.17-dev" in m["frozen_version_range"]
    print("✅ manifest covers v2.9.10 to v2.9.17")

def test_manifest_runtime_false():
    m = build_v3_alpha_release_manifest()
    assert m["runtime_enabled"] is False
    print("✅ manifest runtime=False")

def test_manifest_required_scripts_present():
    m = build_v3_alpha_release_manifest()
    assert len(m["required_verify_scripts"]) == 8
    print(f"✅ {len(m['required_verify_scripts'])} required scripts")

if __name__ == "__main__":
    test_manifest_contains_v2910_to_v2917()
    test_manifest_runtime_false()
    test_manifest_required_scripts_present()
    print("\n🏁 Alpha RC Manifest tests PASS")
