"""Research Asset Index tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.research_asset_index import (
    RESEARCH_ASSET_INDEX_POLICY, RESEARCH_OUTPUT_INDEX_FIELDS, check_research_asset_index_policy
)

def test_full_text_import_disabled():
    assert not RESEARCH_ASSET_INDEX_POLICY.get("full_text_import_allowed")
    print("✅ full text import disabled")

def test_git_import_disabled():
    assert not RESEARCH_ASSET_INDEX_POLICY.get("git_import_allowed")
    print("✅ git import disabled")

def test_schema_has_required():
    for f in ["research_id","ticker","conclusion","confidence","evidence_grade"]:
        assert f in RESEARCH_OUTPUT_INDEX_FIELDS, f"missing {f}"
    print(f"✅ schema: {len(RESEARCH_OUTPUT_INDEX_FIELDS)} fields")

def test_policy_clean():
    assert len(check_research_asset_index_policy())==0
    print("✅ policy clean")

def test_doc_exists():
    from pathlib import Path; assert Path("docs/architecture/RESEARCH_ASSET_INDEX_V10.md").exists()
    print("✅ doc exists")

if __name__ == "__main__":
    test_full_text_import_disabled(); test_git_import_disabled()
    test_schema_has_required(); test_policy_clean(); test_doc_exists()
    print("\n🏁 Research Asset Index — tests PASS")
