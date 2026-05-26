"""Alpha Tag Release Notes tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.alpha_tag.release_notes_builder import build_v3_alpha_rc1_release_notes

def test_release_notes_contains_version_chain():
    n = build_v3_alpha_rc1_release_notes()
    for v in ["v2.9.10","v2.9.11","v2.9.12","v2.9.13","v2.9.14","v2.9.15","v2.9.16","v2.9.17","v2.9.18"]:
        assert v in n
    print("✅ release notes contains version chain")

def test_release_notes_contains_no_real_trade_warning():
    n = build_v3_alpha_rc1_release_notes()
    assert "No real trading" in n
    assert "No broker connection" in n
    print("✅ release notes contains no-real-trade warnings")

def test_release_notes_contains_tag_command_preview():
    n = build_v3_alpha_rc1_release_notes()
    assert "git tag" in n
    assert "git push" in n
    print("✅ release notes contains tag command preview")

def test_release_notes_says_preview_only():
    n = build_v3_alpha_rc1_release_notes()
    assert "preview only" in n.lower()
    print("✅ release notes says preview only")

if __name__ == "__main__":
    test_release_notes_contains_version_chain()
    test_release_notes_contains_no_real_trade_warning()
    test_release_notes_contains_tag_command_preview()
    test_release_notes_says_preview_only()
    print("\n🏁 Alpha Tag Release Notes tests PASS")
