"""v2.9.5-RC 核心管线 smoke test (7条核心, 非18条全量release smoke) — 验证核心管线可加载, 不调用真实行情"""
import importlib.util, sys, os
from pathlib import Path

PIPELINES = [
    "pipelines/Z-G01_数据后勤保障/gate_data.py",
    "pipelines/Z-G07_轮动黑马选股/gate_pipeline.py",
    "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py",
    "pipelines/Z-G10_全局黑马筛选/gate_pipeline.py",
    "pipelines/Z-G16_纸面验证/gate_pipeline.py",
    "pipelines/Z-G16A_Alpha平行验证仓/gate_pipeline.py",
    "pipelines/Z-G03_盘中确认/gate_pipeline.py",
]

def load_module(path):
    """通过文件路径加载模块"""
    spec = importlib.util.spec_from_file_location(Path(path).stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def test_pipeline_modules_importable():
    """所有核心管线可import"""
    for p in PIPELINES:
        try:
            mod = load_module(p)
            assert mod is not None, f"Failed to load {p}"
            print(f"  ✅ {p.split('/')[-1]}")
        except Exception as e:
            assert False, f"Cannot load {p}: {e}"

def test_run_entrypoints_callable():
    """核心管线有run()入口"""
    for p in PIPELINES:
        mod = load_module(p)
        if hasattr(mod, "run"):
            assert callable(mod.run), f"run() not callable in {p}"
            print(f"  ✅ run() in {p.split('/')[-1]}")

if __name__ == "__main__":
    test_pipeline_modules_importable()
    test_run_entrypoints_callable()
    print("\n🏁 Smoke test PASS")
