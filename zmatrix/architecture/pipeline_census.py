"""Pipeline Census v1.0 — 全量管线清点 (v2.9.10-dev)"""
from __future__ import annotations

PIPELINE_STATUS = {
    "ACTIVE": "actively used and architecture-registered",
    "LEGACY": "old pipeline retained for compatibility",
    "STUB": "placeholder or incomplete pipeline",
    "DEPRECATED": "should not be used for new work",
    "UNKNOWN": "exists but not yet classified",
}

_PIPELINE_CENSUS_DATA = {
    "Z-G01": {"path":"pipelines/Z-G01_数据后勤保障","status":"UNKNOWN","architecture_registered":False,"notes":"data logistics / market truth / financial source"},
    "Z-G02": {"path":"pipelines/Z-G02_前夜战报","status":"UNKNOWN","architecture_registered":False,"notes":"front-night war report"},
    "Z-G03": {"path":"pipelines/Z-G03_盘中确认","status":"UNKNOWN","architecture_registered":False,"notes":"intraday confirmation"},
    "Z-G04": {"path":"pipelines/Z-G04_尾盘过滤","status":"UNKNOWN","architecture_registered":False,"notes":"end-of-day filter"},
    "Z-G05": {"path":"pipelines/Z-G05_日记忆卡","status":"UNKNOWN","architecture_registered":False,"notes":"daily memory card"},
    "Z-G06": {"path":"pipelines/Z-G06_复盘反馈","status":"UNKNOWN","architecture_registered":False,"notes":"review feedback"},
    "Z-G07": {"path":"pipelines/Z-G07_轮动黑马选股","status":"UNKNOWN","architecture_registered":False,"notes":"rotation dark horse"},
    "Z-G08": {"path":"pipelines/Z-G08_叙事雷达深度","status":"UNKNOWN","architecture_registered":False,"notes":"narrative radar deep"},
    "Z-G09": {"path":"pipelines/Z-G09_全局轮动筛选","status":"ACTIVE","architecture_registered":True,"notes":"R-Matrix cycle four-king rotation scan"},
    "Z-G10": {"path":"pipelines/Z-G10_全局黑马筛选","status":"UNKNOWN","architecture_registered":False,"notes":"global dark horse"},
    "Z-G11": {"path":"pipelines/Z-G11_组合风控","status":"UNKNOWN","architecture_registered":False,"notes":"portfolio risk control"},
    "Z-G12": {"path":"pipelines/Z-G12_系统巡检","status":"STUB","architecture_registered":False,"notes":"system inspection"},
    "Z-G13": {"path":"pipelines/Z-G13_底仓管理","status":"UNKNOWN","architecture_registered":False,"notes":"base position management"},
    "Z-G14": {"path":"pipelines/Z-G14_月度全量选股","status":"ACTIVE","architecture_registered":True,"notes":"monthly full-market sweep with R-Matrix cycle"},
    "Z-G15": {"path":"pipelines/Z-G15_产业链深研","status":"UNKNOWN","architecture_registered":False,"notes":"industry chain deep research"},
    "Z-G16": {"path":"pipelines/Z-G16_纸面验证","status":"STUB","architecture_registered":False,"notes":"paper verification"},
    "Z-G17": {"path":"pipelines/Z-G17_人类风控","status":"STUB","architecture_registered":False,"notes":"human risk control"},
    "Z-G18": {"path":"pipelines/Z-G18_天机引擎","status":"ACTIVE","architecture_registered":True,"notes":"G18 paper prediction / Z9 preview chain"},
}

def list_pipeline_census() -> dict:
    return dict(_PIPELINE_CENSUS_DATA)

def get_pipeline_census(pid: str) -> dict | None:
    return _PIPELINE_CENSUS_DATA.get(pid)

def check_pipeline_census_integrity() -> list[str]:
    violations = []
    for pid, info in _PIPELINE_CENSUS_DATA.items():
        if info["status"] not in PIPELINE_STATUS:
            violations.append(f"{pid}: invalid status '{info['status']}'")
        if not info["path"]:
            violations.append(f"{pid}: missing path")
    return violations

def compare_census_with_pipeline_registry() -> list[str]:
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    diffs = []
    for pid, info in _PIPELINE_CENSUS_DATA.items():
        if pid in PIPELINE_REGISTRY and not info["architecture_registered"]:
            diffs.append(f"{pid}: in PIPELINE_REGISTRY but census marks not registered")
        if pid not in PIPELINE_REGISTRY and info["architecture_registered"]:
            diffs.append(f"{pid}: census marks registered but not in PIPELINE_REGISTRY")
    return diffs

def detect_pipeline_dirs_without_census() -> list[str]:
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent.parent / "pipelines"
    dirs = sorted(d.name for d in root.iterdir() if d.is_dir() and d.name.startswith("Z-G"))
    # 提取Z-G编号
    census_ids = set(_PIPELINE_CENSUS_DATA.keys())
    found = set()
    for d in dirs:
        parts = d.split("_")
        if parts: found.add(parts[0])
    return sorted(found - census_ids)
