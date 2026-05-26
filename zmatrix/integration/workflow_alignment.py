"""Workflow Alignment Audit — check pipelines, workflows, gates alignment"""
from __future__ import annotations

from zmatrix.integration.schemas import ALPHA_REQUIRED_PIPELINES, ALPHA_REQUIRED_WORKFLOWS
from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
from zmatrix.architecture.gate_registry import GATE_REGISTRY


def audit_workflow_alignment() -> dict:
    """Audit v3.0-alpha workflow alignment."""
    missing_pipelines = [p for p in ALPHA_REQUIRED_PIPELINES if p not in PIPELINE_REGISTRY]
    missing_workflows = [w for w in ALPHA_REQUIRED_WORKFLOWS if w not in WORKFLOW_DAG_REGISTRY]

    missing_gates = []
    node_violations = []
    edge_violations = []

    for wid in ALPHA_REQUIRED_WORKFLOWS:
        w = WORKFLOW_DAG_REGISTRY.get(wid, {})

        # Check required_gates
        for g in w.get("required_gates", []):
            if g not in GATE_REGISTRY:
                missing_gates.append(f"{wid} -> {g}")

        # Check nodes registered
        for nid in w.get("nodes", []):
            if nid not in SHARED_SKILL_REGISTRY and nid not in GATE_REGISTRY:
                node_violations.append(f"{wid}: node {nid} not found")

        # Check edges reference existing nodes
        nodes_set = set(w.get("nodes", []))
        for src, dst in w.get("edges", []):
            if src not in nodes_set:
                edge_violations.append(f"{wid}: edge source {src} not in nodes")
            if dst not in nodes_set:
                edge_violations.append(f"{wid}: edge dest {dst} not in nodes")

    return {
        "audit_version": "WORKFLOW_ALIGNMENT_AUDIT_V10",
        "missing_pipelines": missing_pipelines,
        "missing_workflows": missing_workflows,
        "missing_gates": missing_gates,
        "node_violations": node_violations,
        "edge_violations": edge_violations,
        "pass": len(missing_pipelines) == 0 and len(missing_workflows) == 0
               and len(missing_gates) == 0 and len(node_violations) == 0
               and len(edge_violations) == 0,
    }
