#!/usr/bin/env python3
"""Z-G01 加载器 — 统一入口 + 基本schema校验"""
import importlib.util, os

_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    "Z-G01_数据后勤保障", "gate_data.py")
spec = importlib.util.spec_from_file_location("z01_gate_data", _path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

_REQUIRED_MT_KEYS = ["status","output_level","capability_mask","price_basis","quote_domain"]
_REQUIRED_SA_KEYS = ["status","output_level","capability_mask"]

def _validate_mt(result):
    """校验market_truth输出完整性"""
    missing = [k for k in _REQUIRED_MT_KEYS if k not in result]
    if missing:
        result["errors"] = result.get("errors",[]) + [f"MT_MISSING_KEYS:{missing}"]
        result["status"] = result.get("status","BLOCK")
    return result

def market_truth(ticker):
    return _validate_mt(mod.market_truth(ticker))

def source_arbitrate(ticker, g1):
    return mod.source_arbitrate(ticker, g1)

def dq_score(ticker):
    return mod.dq_score(ticker)

def l4_health(ticker):
    return mod.l4_health(ticker)

def get_kline(ticker, n=60):
    return mod.get_kline(ticker, n)

def get_financials(ticker):
    return mod.get_financials(ticker)

def get_sectors():
    return mod.get_sectors()

def l25_macro():
    return mod.l25_macro()
