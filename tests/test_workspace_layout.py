"""Workspace Layout tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path; W=Path(__file__).resolve().parent.parent

def test_required_top_level_dirs_exist():
    for d in ["zmatrix","pipelines","tests","docs","scripts","release","data"]:
        assert (W/d).is_dir(), f"missing {d}"
    print("✅ all required top-level dirs exist")

def test_data_dirs_exist():
    for d in ["samples","price_bars","fundamentals","sector_map","paper_ledger","outcomes"]:
        assert (W/"data"/d).is_dir(), f"missing data/{d}"
    print("✅ data subdirs exist")

def test_data_samples_exist():
    for f in ["price_bars_sample.csv","financial_snapshot_sample.csv","sector_chain_sample.csv","paper_ledger_sample.csv","outcomes_sample.csv"]:
        assert (W/"data"/"samples"/f).is_file(), f"missing {f}"
    print("✅ 5 sample CSVs exist")

def test_workspace_layout_doc_exists():
    assert (W/"docs"/"architecture"/"WORKSPACE_LAYOUT_V10.md").is_file()
    print("✅ WORKSPACE_LAYOUT_V10.md exists")

def test_gitkeep_in_data_dirs():
    for d in ["price_bars","fundamentals","sector_map","paper_ledger","outcomes"]:
        assert (W/"data"/d/".gitkeep").is_file(), f"missing .gitkeep in {d}"
    print("✅ .gitkeep in all data subdirs")

if __name__ == "__main__":
    test_required_top_level_dirs_exist(); test_data_dirs_exist()
    test_data_samples_exist(); test_workspace_layout_doc_exists(); test_gitkeep_in_data_dirs()
    print("\n🏁 Workspace Layout — tests PASS")
