"""v2.9.5-RC 18条管线 manifest smoke — 强制校验README一致性+入口契约"""
import importlib.util, sys, os
from pathlib import Path

# executable: 目录存在 + import OK + callable run()
# prototype:  目录存在 + import OK (不强制run())
# doc_only:   仅README标注, 无代码入口
PIPELINE_MANIFEST = {
    "Z-G01": {"path": "pipelines/Z-G01_数据后勤保障/gate_data.py", "status": "executable_core"},
    "Z-G02": {"path": "pipelines/Z-G02_前夜战报/gate_pipeline.py", "status": "prototype"},
    "Z-G03": {"path": "pipelines/Z-G03_盘中确认/gate_pipeline.py", "status": "prototype"},
    "Z-G04": {"path": "pipelines/Z-G04_尾盘过滤/gate_pipeline.py", "status": "executable_light"},
    "Z-G05": {"path": "pipelines/Z-G05_日记忆卡/gate_pipeline.py", "status": "executable_core"},
    "Z-G06": {"path": "pipelines/Z-G06_复盘反馈/gate_pipeline.py", "status": "executable_core"},
    "Z-G07": {"path": "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py", "status": "prototype"},
    "Z-G08": {"path": "pipelines/Z-G08_叙事雷达深度/gate_pipeline.py", "status": "prototype"},
    "Z-G09": {"path": "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py", "status": "executable_core"},
    "Z-G10": {"path": "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py", "status": "executable_core"},
    "Z-G11": {"path": "pipelines/Z-G11_组合风控/gate_pipeline.py", "status": "executable_light"},
    "Z-G12": {"path": "pipelines/Z-G12_系统巡检/gate_pipeline.py", "status": "executable_core"},
    "Z-G13": {"path": "pipelines/Z-G13_底仓管理/gate_pipeline.py", "status": "executable_light"},
    "Z-G14": {"path": "pipelines/Z-G14_月度全量选股/gate_pipeline.py", "status": "prototype"},
    "Z-G15": {"path": "pipelines/Z-G15_产业链深研/gate_pipeline.py", "status": "prototype"},
    "Z-G16": {"path": "pipelines/Z-G16_纸面验证/gate_pipeline.py", "status": "executable_core"},
    "Z-G16A": {"path": "pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py", "status": "executable_core"},
    "Z-G17": {"path": "pipelines/Z-G17_人类风控/gate_pipeline.py", "status": "executable_light"},
}

README_STATUS_MAP = {"🟢": "executable", "🟡": "prototype", "🔴": "doc_only"}

def load_module(path):
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_manifest_all_18():
    assert len(PIPELINE_MANIFEST) == 18
    print("  ✅ 18/18")

def test_executable_paths_and_run():
    """executable: 目录存在 + import + callable run()"""
    failed = []
    for code, item in PIPELINE_MANIFEST.items():
        if item["status"] not in ("executable_core","executable_light"): continue
        p = Path(item["path"])
        assert p.exists(), f"{code}: MISSING {p}"
        mod = load_module(str(p))
        # Z-G01 is Data Service (market_truth+source_arbitrate, not run())
        if "gate_data.py" in item["path"]:
            assert hasattr(mod, "market_truth"), f"{code}: data service missing market_truth"
            assert hasattr(mod, "source_arbitrate"), f"{code}: data service missing source_arbitrate"
            print(f"  ✅ {code}: data service (market_truth+source_arbitrate)")
        else:
            assert hasattr(mod, "run"), f"{code}: executable must have run()"
            assert callable(mod.run), f"{code}: run() not callable"
            print(f"  ✅ {code}: path+import+run()")
    assert not failed

def test_prototype_import():
    """prototype: 目录存在 + import OK"""
    for code, item in PIPELINE_MANIFEST.items():
        if item["status"] != "prototype": continue
        p = Path(item["path"])
        assert p.exists(), f"{code}: MISSING {p}"
        mod = load_module(str(p))
        assert mod is not None, f"{code}: import failed"
        print(f"  ✅ {code}: path+import (prototype)")

def test_pipeline_readme_status_consistent():
    """pipelines/README.md 状态与manifest一致"""
    readme = Path("pipelines/README.md").read_text(encoding="utf-8")
    for code, item in PIPELINE_MANIFEST.items():
        lines = [ln for ln in readme.splitlines() if f"| {code} " in ln]
        assert lines, f"{code}: missing in pipelines/README.md"
        line = lines[0]
        expected_icon = {"executable_core": "🟢", "executable_light": "🟢-light", "prototype": "🟡", "doc_only": "🔴"}[item["status"]]
        assert expected_icon in line, f"{code}: manifest={item['status']} but README={line.strip()}"
    print("  ✅ pipelines/README状态与manifest一致")

def test_root_and_pipeline_readme_consistent():
    """根README与pipelines README release/code状态精确一致"""
    def extract(text):
        if "release-ready candidate" in text: return "release-ready candidate"
        if "code-ready candidate" in text: return "code-ready candidate"
        return None
    root = Path("README.md").read_text(encoding="utf-8")
    pipe = Path("pipelines/README.md").read_text(encoding="utf-8")
    rs = extract(root); ps = extract(pipe)
    assert rs is not None, "README.md missing candidate state"
    assert ps is not None, "pipelines/README.md missing candidate state"
    assert rs == ps, f"State mismatch: root={rs}, pipelines={ps}"
    print(f"  ✅ root={rs}, pipelines={ps}")

if __name__ == "__main__":
    test_manifest_all_18()
    test_executable_paths_and_run()
    test_prototype_import()
    test_pipeline_readme_status_consistent()
    test_root_and_pipeline_readme_consistent()
    print("\n🏁 18-pipeline manifest smoke + README consistency PASS")
