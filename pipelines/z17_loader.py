#!/usr/bin/env python3
"""Z-G01 加载器 — 所有管线通过此文件导入 Z-G01 数据后勤保障"""
import importlib.util, os

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "Z-G01_数据后勤保障", "gate_data.py")
spec = importlib.util.spec_from_file_location("z01_gate_data", _path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

market_truth      = mod.market_truth
source_arbitrate  = mod.source_arbitrate
dq_score          = mod.dq_score
l4_health         = mod.l4_health
get_kline         = mod.get_kline
get_financials    = mod.get_financials
get_sectors       = mod.get_sectors
l25_macro         = mod.l25_macro
