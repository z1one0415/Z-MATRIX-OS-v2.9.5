#!/usr/bin/env python3
"""
☯️ System Controller MVP v1.0 — 最小系统控制器 (Batch F-8)

只负责读取 registry 并生成 execution plan。
不执行真实业务。
"""
from __future__ import annotations

from datetime import datetime


def build_system_execution_plan(
    workflow_id: str,
    *,
    dry_run: bool = True,
) -> dict:
    """
    生成系统执行计划预览。

    dry_run 默认为 True。
    execution_allowed 必须 False。
    real_ops_allowed 必须 False。
    不实际调用 G18/Z9/R-Matrix。
    只生成 plan preview。
    """
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY, topological_order
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY

    workflow = WORKFLOW_DAG_REGISTRY.get(workflow_id)
    validation = {
        "workflow_exists": workflow is not None,
        "pipeline_registered": False,
        "nodes_registered": False,
        "gates_registered": False,
        "no_real_ops": False,
        "ready_for_runtime": False,
    }

    if not workflow:
        return {
            "controller_version": "v1.0",
            "workflow_id": workflow_id,
            "pipeline_id": None,
            "dry_run": dry_run,
            "execution_allowed": False,
            "real_ops_allowed": False,
            "ordered_nodes": [],
            "required_gates": [],
            "skill_nodes": [],
            "gate_nodes": [],
            "forbidden_capabilities": [],
            "validation": validation,
            "reason": "WORKFLOW_NOT_FOUND",
        }

    pid = workflow.get("pipeline", "")
    pipeline = PIPELINE_REGISTRY.get(pid)
    validation["pipeline_registered"] = pipeline is not None

    nodes = list(workflow.get("nodes", []))
    try:
        ordered = topological_order(workflow_id)
    except ValueError:
        ordered = nodes

    skill_nodes = [n for n in nodes if n in SHARED_SKILL_REGISTRY]
    gate_nodes = [n for n in nodes if n in GATE_REGISTRY]
    required_gates = list(workflow.get("required_gates", []))
    forbidden = list(workflow.get("forbidden_capabilities", []))

    validation["nodes_registered"] = all(
        n in SHARED_SKILL_REGISTRY or n in GATE_REGISTRY for n in nodes
    )
    validation["gates_registered"] = all(
        g in GATE_REGISTRY for g in required_gates
    )
    validation["no_real_ops"] = all(
        r in forbidden for r in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]
    )
    validation["ready_for_runtime"] = False  # MVP: 永远 False

    return {
        "controller_version": "v1.0",
        "workflow_id": workflow_id,
        "pipeline_id": pid,
        "dry_run": dry_run,
        "execution_allowed": False,
        "real_ops_allowed": False,
        "ordered_nodes": ordered,
        "required_gates": required_gates,
        "skill_nodes": skill_nodes,
        "gate_nodes": gate_nodes,
        "forbidden_capabilities": forbidden,
        "validation": validation,
        "reason": "SYSTEM_CONTROLLER_MVP_PLAN_ONLY_NO_RUNTIME_EXECUTION",
    }
