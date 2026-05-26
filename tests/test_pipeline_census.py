"""Pipeline Census tests"""
import sys,os; sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from zmatrix.architecture.pipeline_census import (
    list_pipeline_census, get_pipeline_census, check_pipeline_census_integrity,
    compare_census_with_pipeline_registry, detect_pipeline_dirs_without_census, PIPELINE_STATUS
)

def test_census_has_zg01_to_zg18():
    c=list_pipeline_census()
    for i in range(1,19):
        pid=f"Z-G{i:02d}"; assert pid in c, f"missing {pid}"
    print("✅ Z-G01~Z-G18 all in census")

def test_status_values_valid():
    for pid,info in list_pipeline_census().items():
        assert info["status"] in PIPELINE_STATUS, f"{pid}: invalid {info['status']}"
    print("✅ all statuses valid")

def test_registered_pipelines_marked():
    for pid,info in list_pipeline_census().items():
        if info["architecture_registered"]:
            assert info["status"] in ("ACTIVE","LEGACY"), f"{pid} registered but status={info['status']}"
    print("✅ registered pipelines properly marked")

def test_compare_clean():
    v=compare_census_with_pipeline_registry(); assert len(v)==0, f"diffs: {v}"
    print("✅ census vs pipeline_registry consistent")

def test_integrity_clean():
    v=check_pipeline_census_integrity(); assert len(v)==0, f"violations: {v}"
    print("✅ census integrity clean")

def test_census_doc_exists():
    from pathlib import Path; assert Path("docs/architecture/PIPELINE_CENSUS_V10.md").exists()
    print("✅ PIPELINE_CENSUS_V10.md exists")

if __name__ == "__main__":
    test_census_has_zg01_to_zg18(); test_status_values_valid()
    test_registered_pipelines_marked(); test_compare_clean()
    test_integrity_clean(); test_census_doc_exists()
    print("\n🏁 Pipeline Census — tests PASS")
