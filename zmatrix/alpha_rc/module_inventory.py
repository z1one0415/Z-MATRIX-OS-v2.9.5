"""Module Inventory — list frozen preview/read-only/runtime-disabled modules"""
from __future__ import annotations

from zmatrix.alpha_rc.schemas import DEFAULT_ALPHA_RC_SAFETY

_CORE_MODULES = [
    ("zmatrix/event_store/", "local append-only, no Z9/Hermes write"),
    ("zmatrix/hermes_kernel/", "read-only / preview-only core memory"),
    ("zmatrix/hermes_memory/", "preview-only MemoryCandidate/Calibration/Kernel"),
    ("zmatrix/approval_loop/", "approval record only, no auto effect"),
    ("zmatrix/prompt_middleware/", "preview-only, no runtime injection"),
    ("zmatrix/tail_risk/", "preview-only, no broker / no auto sell"),
    ("zmatrix/integration/", "readiness-check-only"),
    ("zmatrix/dry_run/", "rehearsal-only"),
]


def build_v3_alpha_frozen_module_inventory() -> dict:
    frozen = []
    preview = []
    read_only = []
    runtime_disabled = []

    for path, note in _CORE_MODULES:
        frozen.append({"path": path, "status": "FROZEN", "notes": note})
        if "preview" in note:
            preview.append(path)
        if "read-only" in note or "readonly" in note:
            read_only.append(path)
        runtime_disabled.append(path)

    return {
        "inventory_version": "V3_ALPHA_FROZEN_MODULE_INVENTORY_V10",
        "frozen_modules": frozen,
        "preview_only_modules": preview,
        "read_only_modules": read_only,
        "runtime_disabled_modules": runtime_disabled,
        "forbidden_capabilities": [
            "real_trade", "broker_order", "auto_buy", "auto_sell",
            "auto_position_close", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "system_prompt_write",
            "runtime_prompt_injection", "external_api_default_on",
        ],
        "safety": dict(DEFAULT_ALPHA_RC_SAFETY),
    }
