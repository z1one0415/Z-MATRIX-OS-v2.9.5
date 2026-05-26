"""Alpha Tag Readiness Validator tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_tag.tag_readiness_validator import validate_v3_alpha_tag_readiness

def test_tag_readiness_passes():
    r = validate_v3_alpha_tag_readiness()
    assert r["overall_status"] == "READY_FOR_TAG_REVIEW"
    assert r["ready_for_tag_review"] is True
    print("✅ tag readiness passes")

def test_tag_readiness_does_not_allow_git_tag_execute():
    r = validate_v3_alpha_tag_readiness()
    assert r["git_tag_execute_allowed"] is False
    print("✅ git_tag_execute_allowed=False")

def test_tag_readiness_does_not_allow_git_push_tags():
    r = validate_v3_alpha_tag_readiness()
    assert r["git_push_tags_allowed"] is False
    print("✅ git_push_tags_allowed=False")

def test_tag_readiness_runtime_false():
    r = validate_v3_alpha_tag_readiness()
    assert r["runtime_enabled"] is False
    print("✅ runtime_enabled=False")

def test_tag_readiness_real_trade_false():
    r = validate_v3_alpha_tag_readiness()
    assert r["real_trade_allowed"] is False
    print("✅ real_trade_allowed=False")

def test_tag_readiness_blocks_failed_artifact_consistency():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_alpha_rc_artifact_consistency
    def bad_cs():
        return {"pass": False, "violations": ["artifact mismatch"]}
    v.validate_alpha_rc_artifact_consistency = bad_cs
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert r["blocking_issues"]
    finally:
        v.validate_alpha_rc_artifact_consistency = original
    print("✅ blocks failed artifact consistency")

def test_tag_readiness_blocks_failed_rc_gate():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_v3_alpha_rc_gate
    def bad_rc():
        return {"pass": False, "violations": ["rc failed"]}
    v.validate_v3_alpha_rc_gate = bad_rc
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert r["blocking_issues"]
    finally:
        v.validate_v3_alpha_rc_gate = original
    print("✅ blocks failed RC gate")

def test_tag_readiness_blocks_rc_gate_git_tag_execute_true():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_v3_alpha_rc_gate
    def bad_rc():
        return {"pass": True, "violations": [], "git_tag_execute_allowed": True}
    v.validate_v3_alpha_rc_gate = bad_rc
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert any("rc_gate.git_tag_execute_allowed" in x for x in r["blocking_issues"])
    finally:
        v.validate_v3_alpha_rc_gate = original
    print("✅ blocks rc_gate.git_tag_execute_allowed=True")

def test_tag_readiness_blocks_artifact_consistency_git_push_tags_true():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_alpha_rc_artifact_consistency
    def bad_cs():
        return {"pass": True, "violations": [], "git_push_tags_allowed": True}
    v.validate_alpha_rc_artifact_consistency = bad_cs
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert any("artifact_consistency.git_push_tags_allowed" in x for x in r["blocking_issues"])
    finally:
        v.validate_alpha_rc_artifact_consistency = original
    print("✅ blocks artifact_consistency.git_push_tags_allowed=True")

def test_tag_readiness_blocks_artifact_consistency_runtime_true():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_alpha_rc_artifact_consistency
    def bad_cs():
        return {"pass": True, "violations": [], "runtime_enabled": True}
    v.validate_alpha_rc_artifact_consistency = bad_cs
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert any("artifact_consistency.runtime_enabled" in x for x in r["blocking_issues"])
    finally:
        v.validate_alpha_rc_artifact_consistency = original
    print("✅ blocks artifact_consistency.runtime_enabled=True")

def test_tag_readiness_blocks_rc_gate_safety_auto_sell_true():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_v3_alpha_rc_gate
    def bad_rc():
        return {"pass": True, "violations": [], "safety": {"auto_sell_allowed": True}}
    v.validate_v3_alpha_rc_gate = bad_rc
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert any("rc_gate.safety.auto_sell_allowed" in x for x in r["blocking_issues"])
    finally:
        v.validate_v3_alpha_rc_gate = original
    print("✅ blocks rc_gate.safety.auto_sell_allowed=True")

def test_tag_readiness_blocks_non_dict_rc_gate_safety():
    import zmatrix.alpha_tag.tag_readiness_validator as v
    original = v.validate_v3_alpha_rc_gate
    def bad_rc():
        return {"pass": True, "violations": [], "safety": "bad"}
    v.validate_v3_alpha_rc_gate = bad_rc
    try:
        r = v.validate_v3_alpha_tag_readiness()
        assert r["overall_status"] == "BLOCKED"
        assert any("rc_gate.safety must be dict" in x for x in r["blocking_issues"])
    finally:
        v.validate_v3_alpha_rc_gate = original
    print("✅ blocks non-dict rc_gate safety")

if __name__ == "__main__":
    test_tag_readiness_passes()
    test_tag_readiness_does_not_allow_git_tag_execute()
    test_tag_readiness_does_not_allow_git_push_tags()
    test_tag_readiness_runtime_false()
    test_tag_readiness_real_trade_false()
    test_tag_readiness_blocks_failed_artifact_consistency()
    test_tag_readiness_blocks_failed_rc_gate()
    test_tag_readiness_blocks_rc_gate_git_tag_execute_true()
    test_tag_readiness_blocks_artifact_consistency_git_push_tags_true()
    test_tag_readiness_blocks_artifact_consistency_runtime_true()
    test_tag_readiness_blocks_rc_gate_safety_auto_sell_true()
    test_tag_readiness_blocks_non_dict_rc_gate_safety()
    print("\n🏁 Alpha Tag Readiness Validator tests PASS")
