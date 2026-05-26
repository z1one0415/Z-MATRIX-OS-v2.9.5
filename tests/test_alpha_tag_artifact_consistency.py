"""Alpha Tag Artifact Consistency tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_tag.artifact_consistency import validate_alpha_rc_artifact_consistency

def test_artifact_consistency_passes():
    r = validate_alpha_rc_artifact_consistency()
    assert r["pass"] is True, f"violations: {r.get('violations', [])}"
    print("✅ artifact consistency passes")

def test_artifact_consistency_checks_all_required_artifacts():
    r = validate_alpha_rc_artifact_consistency()
    assert len(r["checked_artifacts"]) == 10
    print(f"✅ checks {len(r['checked_artifacts'])} artifacts")

def test_artifact_consistency_json_matches_builders():
    r = validate_alpha_rc_artifact_consistency()
    assert r["json_artifacts_match_builders"] is True
    print("✅ JSON artifacts match builders")

def test_artifact_consistency_checks_required_verify_scripts():
    r = validate_alpha_rc_artifact_consistency()
    assert len(r["checked_verify_scripts"]) >= 8
    print(f"✅ checks {len(r['checked_verify_scripts'])} scripts")

def test_artifact_consistency_includes_tag_release_artifacts():
    r = validate_alpha_rc_artifact_consistency()
    artifacts = set(r["checked_artifacts"])
    assert "release/alpha_rc/v3_alpha_rc1_release_notes.md" in artifacts
    assert "release/alpha_rc/v3_alpha_tag_command_preview_v10.md" in artifacts
    assert "release/alpha_rc/v3_alpha_final_release_summary_v10.md" in artifacts
    print("✅ includes v2.9.19 tag release artifacts")

if __name__ == "__main__":
    test_artifact_consistency_passes()
    test_artifact_consistency_checks_all_required_artifacts()
    test_artifact_consistency_json_matches_builders()
    test_artifact_consistency_checks_required_verify_scripts()
    test_artifact_consistency_includes_tag_release_artifacts()
    print("\n🏁 Alpha Tag Artifact Consistency tests PASS")
