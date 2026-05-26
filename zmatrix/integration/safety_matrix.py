"""Cross-Layer Safety Matrix — check all layers forbid all forbidden capabilities"""
from __future__ import annotations

from zmatrix.integration.schemas import ALPHA_FORBIDDEN_CAPABILITIES
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY

_LAYER_PIPELINES = {
    "EVENT_STORE": "Z-EventStore",
    "HERMES_MEMORY": "Z-HermesMemoryKernel",
    "APPROVAL_LOOP": "Z-ApprovalReflectionLoop",
    "PROMPT_MIDDLEWARE": "Z-PromptMiddlewarePreview",
    "TAIL_RISK": "Z-TailRiskAutonomicGates",
    "SYSTEM_CONTROLLER": "RC-release",
}


def build_cross_layer_safety_matrix() -> dict:
    """Build a safety matrix for all v3.0 layers vs forbidden capabilities."""
    cap_list = sorted(ALPHA_FORBIDDEN_CAPABILITIES)
    layers = sorted(_LAYER_PIPELINES.keys())
    matrix = {}
    violations = []

    for layer_name, pid in _LAYER_PIPELINES.items():
        p = PIPELINE_REGISTRY.get(pid, {})
        fc = set(p.get("forbidden_capabilities", []))
        row = {}
        for cap in cap_list:
            forbidden = cap in fc
            row[cap] = forbidden
            if not forbidden:
                violations.append(f"{layer_name}: missing forbidden_capability '{cap}'")
        matrix[layer_name] = row

    return {
        "matrix_version": "CROSS_LAYER_SAFETY_MATRIX_V10",
        "layers": layers,
        "capabilities": cap_list,
        "matrix": matrix,
        "violations": violations,
        "pass": len(violations) == 0,
    }
