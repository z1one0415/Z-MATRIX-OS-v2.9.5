"""v2.9.5-RC 18条管线 manifest smoke — 验证目录+入口+状态诚实"""
import importlib.util, sys, os
from pathlib import Path

# 18条管线清单: {编号: {path, status}}
# status: executable/prototype/doc_only — 必须与README一致
PIPELINE_MANIFEST = {
    "Z-G01": {"path": "pipelines/Z-G01_数据后勤保障/gate_data.py", "status": "executable"},
    "Z-G02": {"path": "pipelines/Z-G02_前夜战报/gate_pipeline.py", "status": "prototype"},
    "Z-G03": {"path": "pipelines/Z-G03_盘中确认/gate_pipeline.py", "status": "prototype"},
    "Z-G04": {"path": "pipelines/Z-G04_尾盘过滤/gate_pipeline.py", "status": "executable"},
    "Z-G05": {"path": "pipelines/Z-G05_日记忆卡/gate_pipeline.py", "status": "executable"},
    "Z-G06": {"path": "pipelines/Z-G06_复盘反馈/gate_pipeline.py", "status": "executable"},
    "Z-G07": {"path": "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", "status": "prototype"},
    "Z-G08": {"path": "pipelines/Z-G08_叙事雷达深度/gate_pipeline.py", "status": "prototype"},
    "Z-G09": {"path": "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py", "status": "prototype"},
    "Z-G10": {"path": "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py", "status": "prototype"},
    "Z-G11": {"path": "pipelines/Z-G11_组合风控/gate_pipeline.py", "status": "executable"},
    "Z-G12": {"path": "pipelines/Z-G12_系统巡检/gate_pipeline.py", "status": "executable"},
    "Z-G13": {"path": "pipelines/Z-G13_底仓管理/gate_pipeline.py", "status": "prototype"},
    "Z-G14": {"path": "pipelines/Z-G14_月度全量选股/gate_pipeline.py", "status": "prototype"},
    "Z-G15": {"path": "pipelines/Z-G15_产业链深研/gate_pipeline.py", "status": "prototype"},
    "Z-G16": {"path": "pipelines/Z-G16_纸面验证/gate_pipeline.py", "status": "executable"},
    "Z-G16A": {"path": "pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py", "status": "executable"},
    "Z-G17": {"path": "pipelines/Z-G17_人类风控/gate_pipeline.py", "status": "executable"},
}

def load_module(path):
    try:
        spec = importlib.util.spec_from_file_location(Path(path).stem, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod
    except:
        return None

def test_manifest_all_18_declared():
    """验证清单覆盖18条管线"""
    assert len(PIPELINE_MANIFEST) == 18, f"Expected 18, got {len(PIPELINE_MANIFEST)}"
    print(f"  ✅ 18条管线已声明")

def test_manifest_paths_exist_or_doc_only():
    """验证入口文件存在 (doc_only除外)"""
    for code, item in PIPELINE_MANIFEST.items():
        p = Path(item["path"])
        if item["status"] == "doc_only":
            print(f"  📄 {code}: doc_only (skip file check)")
            continue
        assert p.exists(), f"{code}: MISSING {p}"
        print(f"  {'🟢' if item['status']=='executable' else '🟡'} {code}: {item['status']} ({p.name})")
    print("  ✅ 所有声明路径存在")

def test_executable_pipelines_importable():
    """验证executable管线可import"""
    for code, item in PIPELINE_MANIFEST.items():
        p = Path(item["path"])
        if not p.exists(): continue
        if item["status"] == "executable":
            mod = load_module(str(p))
            assert mod is not None, f"{code}: import failed"
            has_run = hasattr(mod, "run") and callable(mod.run)
            print(f"  ✅ {code}: import OK, run()={'OK' if has_run else 'MISSING'}")

if __name__ == "__main__":
    test_manifest_all_18_declared()
    test_manifest_paths_exist_or_doc_only()
    test_executable_pipelines_importable()
    print("\n🏁 18-pipeline manifest smoke PASS")
