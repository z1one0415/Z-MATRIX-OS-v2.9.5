# allowlist: forbidden-token-definition
"""Cross-Layer Safety Matrix — check all layers block key capabilities"""
from __future__ import annotations

from zmatrix.integration.schemas import ALPHA_FORBIDDEN_CAPABILITIES
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY

_LAYER_PIPELINES = {
    "EVENT_STORE": "Z-EventStore",
    "HERMES_MEMORY": "Z-HermesMemoryKernel",
    "APPROVAL_LOOP": "Z-ApprovalReflectionLoop",
    "PROMPT_MIDDLEWARE": "Z-PromptMiddlewarePreview",
    "TAIL_RISK": "Z-TailRiskAutonomicGates",
}

NON_PIPELINE_LAYERS = {
    "SYSTEM_CONTROLLER": {
        "runtime_allowed": False, "real_trade_allowed": False,
        "notes": "System Controller remains plan-only / runtime disabled.",
    },
}

# Key forbidden capabilities each pipeline must explicitly block
_PIPELINE_MUST_FORBID = {
    "EVENT_STORE": ["real_z9_write", "hermes_memory_write", "real_trade"],
    "HERMES_MEMORY": ["hermes_memory_write", "auto_calibration", "prompt_auto_injection", "real_trade"],
    "APPROVAL_LOOP": ["hermes_memory_write", "auto_calibration", "prompt_auto_injection", "real_trade"],
    "PROMPT_MIDDLEWARE": ["runtime_prompt_injection", "system_prompt_write", "prompt_auto_injection", "real_trade"],
    "TAIL_RISK": ["broker_order", "auto_sell", "auto_buy", "auto_position_close", "real_trade"],
}


def build_cross_layer_safety_matrix() -> dict:
    """Build a safety matrix. False=capability not allowed. True=violation."""
    cap_list = sorted(ALPHA_FORBIDDEN_CAPABILITIES)
    layers = sorted(_LAYER_PIPELINES.keys()) + list(NON_PIPELINE_LAYERS.keys())
    matrix = {}
    violations = []

    for layer_name, pid in _LAYER_PIPELINES.items():
        p = PIPELINE_REGISTRY.get(pid, {})
        fc = set(p.get("forbidden_capabilities", []))
        must_forbid = _PIPELINE_MUST_FORBID.get(layer_name, [])
        row = {}
        for cap in cap_list:
            if cap in must_forbid:
                forbidden = cap in fc
                row[cap] = not forbidden  # True = violation
                if not forbidden:
                    violations.append(f"{layer_name}: must forbid '{cap}' but missing from pipeline forbidden_capabilities")
            else:
                row[cap] = False  # Not a required cap for this layer
        matrix[layer_name] = row

    for layer_name in NON_PIPELINE_LAYERS:
        row = {cap: False for cap in cap_list}
        matrix[layer_name] = row

    return {
        "matrix_version": "CROSS_LAYER_SAFETY_MATRIX_V10",
        "matrix_semantics": "False means capability is not allowed; True means violation",
        "layers": layers,
        "capabilities": cap_list,
        "matrix": matrix,
        "violations": violations,
        "pass": len(violations) == 0,
    }
