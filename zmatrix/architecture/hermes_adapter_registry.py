"""Hermes Adapter Registry v1.0 — 索引 hermes/ 旧模块 (v2.9.10-dev)
不改变 hermes/ 内部逻辑。所有适配器默认 preview-only / read-only / inventory-only。
"""
from __future__ import annotations
from pathlib import Path

HERMES_ADAPTER_REGISTRY = {
    "hermes.z9_calibration.preview": {
        "adapter_type": "hermes_adapter",
        "source_path": "hermes/Z9_Calibration_Engine.py",
        "status": "LEGACY",
        "runtime_mode": "preview_only",
        "write_allowed": False, "real_trade_allowed": False, "auto_calibration_allowed": False,
        "notes": "Existing Z9 calibration engine, not rewritten in v2.9.10",
    },
    "hermes.narrative_radar.scan": {
        "adapter_type": "hermes_adapter", "source_path": "hermes/narrative_radar.py",
        "status": "UNKNOWN", "runtime_mode": "inventory_only",
        "write_allowed": False, "real_trade_allowed": False, "auto_calibration_allowed": False,
    },
    "hermes.memory_bank.lookup": {
        "adapter_type": "hermes_adapter", "source_path": "hermes/memory_bank.py",
        "status": "UNKNOWN", "runtime_mode": "read_only",
        "write_allowed": False, "real_trade_allowed": False, "auto_calibration_allowed": False,
    },
}

def list_hermes_adapters() -> dict:
    return dict(HERMES_ADAPTER_REGISTRY)

def check_hermes_adapter_registry_integrity() -> list[str]:
    violations = []
    for aid, a in HERMES_ADAPTER_REGISTRY.items():
        if a.get("write_allowed"): violations.append(f"{aid}: write_allowed should be False")
        if a.get("real_trade_allowed"): violations.append(f"{aid}: real_trade_allowed should be False")
        if a.get("auto_calibration_allowed"): violations.append(f"{aid}: auto_calibration_allowed should be False")
        if a["status"] not in ("LEGACY","UNKNOWN","STUB","ACTIVE"):
            violations.append(f"{aid}: invalid status")
    return violations
