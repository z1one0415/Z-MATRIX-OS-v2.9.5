"""Script Index tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.script_index import list_script_index, check_script_index_integrity

def test_verify_scripts_indexed():
    s=list_script_index()
    for v in ["verify_architecture_candidate","verify_investment_role_candidate","verify_personal_quant_data_candidate"]:
        assert v in s, f"missing {v}"
    print("✅ 3 verify scripts indexed")

def test_no_real_trade():
    for s in list_script_index().values():
        assert not s.get("real_trade_allowed")
    print("✅ no real trade")

def test_active_scripts_exist():
    from pathlib import Path
    for sid,s in list_script_index().items():
        if s["status"]=="ACTIVE":
            assert Path(s["path"]).exists(), f"missing {s['path']}"
    print("✅ active scripts exist")

def test_integrity_clean():
    assert len(check_script_index_integrity())==0
    print("✅ integrity clean")

def test_doc_exists():
    from pathlib import Path; assert Path("docs/architecture/SCRIPT_INDEX_V10.md").exists()
    print("✅ doc exists")

if __name__ == "__main__":
    test_verify_scripts_indexed(); test_no_real_trade(); test_active_scripts_exist()
    test_integrity_clean(); test_doc_exists()
    print("\n🏁 Script Index — tests PASS")
