"""Readiness Map — build v3.0-alpha readiness map for all layers"""
from __future__ import annotations

from zmatrix.integration.schemas import (
    ALPHA_REQUIRED_PIPELINES, ALPHA_REQUIRED_WORKFLOWS,
    ALPHA_REQUIRED_GATES, ALPHA_FORBIDDEN_CAPABILITIES,
    DEFAULT_INTEGRATION_SAFETY,
)
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
from zmatrix.architecture.gate_registry import GATE_REGISTRY


def build_v3_alpha_readiness_map() -> dict:
    """Build a readiness map for all v3.0-alpha layers."""
    _pipeline_map = {
        "WORKSPACE": "Z-PipelineCensus",
        "EVENT_STORE": "Z-EventStore",
        "HERMES_MEMORY": "Z-HermesMemoryKernel",
        "APPROVAL_LOOP": "Z-ApprovalReflectionLoop",
        "PROMPT_MIDDLEWARE": "Z-PromptMiddlewarePreview",
        "TAIL_RISK": "Z-TailRiskAutonomicGates",
        "SYSTEM_CONTROLLER": "RC-release",
    }
    _workflow_map = {
        "EVENT_STORE": "Z-EventStore.unified_event_ledger_workflow",
        "HERMES_MEMORY": "Z-Hermes.memory_kernel_preview_workflow",
        "APPROVAL_LOOP": "Z-Approval.reflection_loop_workflow",
        "PROMPT_MIDDLEWARE": "Z-Prompt.middleware_preview_workflow",
        "TAIL_RISK": "Z-TailRisk.autonomic_gates_preview_workflow",
    }
    _verify_map = {
        "WORKSPACE": "scripts/verify_workspace_alignment_candidate.sh",
        "EVENT_STORE": "scripts/verify_event_store_candidate.sh",
        "HERMES_MEMORY": "scripts/verify_hermes_memory_candidate.sh",
        "APPROVAL_LOOP": "scripts/verify_approval_loop_candidate.sh",
        "PROMPT_MIDDLEWARE": "scripts/verify_prompt_middleware_candidate.sh",
        "TAIL_RISK": "scripts/verify_tail_risk_candidate.sh",
    }

    layers = {}
    for layer_name in ["WORKSPACE", "EVENT_STORE", "HERMES_MEMORY",
                        "APPROVAL_LOOP", "PROMPT_MIDDLEWARE", "TAIL_RISK",
                        "SYSTEM_CONTROLLER"]:
        pid = _pipeline_map.get(layer_name, "")
        wid = _workflow_map.get(layer_name, "")
        pipeline_registered = pid in PIPELINE_REGISTRY
        workflow_registered = wid in WORKFLOW_DAG_REGISTRY if wid else True
        status = "READY_FOR_ALPHA" if pipeline_registered and workflow_registered else "BLOCKED"

        layers[layer_name] = {
            "layer": layer_name,
            "status": status,
            "pipeline": pid,
            "workflow": wid,
            "pipeline_registered": pipeline_registered,
            "workflow_registered": workflow_registered,
            "verify_script": _verify_map.get(layer_name, ""),
            "runtime_allowed": False,
            "write_allowed": False,
            "real_trade_allowed": False,
            "notes": "preview-only, no runtime",
        }

    # Required pipelines
    missing_pipelines = [p for p in ALPHA_REQUIRED_PIPELINES if p not in PIPELINE_REGISTRY]
    missing_workflows = [w for w in ALPHA_REQUIRED_WORKFLOWS if w not in WORKFLOW_DAG_REGISTRY]
    missing_gates = [g for g in ALPHA_REQUIRED_GATES if g not in GATE_REGISTRY]

    return {
        "readiness_map_version": "V3_ALPHA_READINESS_MAP_V10",
        "mode": "READINESS_CHECK_ONLY",
        "alpha_runtime_allowed": False,
        "layers": layers,
        "missing_pipelines": missing_pipelines,
        "missing_workflows": missing_workflows,
        "missing_gates": missing_gates,
        "required_pipelines": sorted(ALPHA_REQUIRED_PIPELINES),
        "required_workflows": sorted(ALPHA_REQUIRED_WORKFLOWS),
        "required_gates": sorted(ALPHA_REQUIRED_GATES),
        "forbidden_capabilities": sorted(ALPHA_FORBIDDEN_CAPABILITIES),
        "safety": dict(DEFAULT_INTEGRATION_SAFETY),
    }
