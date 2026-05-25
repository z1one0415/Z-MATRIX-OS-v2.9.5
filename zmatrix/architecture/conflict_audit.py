#!/usr/bin/env python3
"""
☯️ Cross-Pipeline Conflict Audit v1.0 — 管线间冲突审计 (Batch F-6)

审计不同 pipeline 是否重复造能力、冲突使用 shared skill、边界声明不一致。
"""
from __future__ import annotations

from typing import Any


def audit_shared_skill_usage() -> dict:
    """返回每条 pipeline 使用的共享技能"""
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    usage = {}
    for pid, p in PIPELINE_REGISTRY.items():
        usage[pid] = list(p.get("allowed_skills", []))
    return usage


def audit_pipeline_skill_conflicts() -> list[str]:
    """审计是否有多个 pipeline 对同一 skill 有不同的 duplicate_allowed 声明"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    conflicts = []
    # 如果某一个 skill 被多个 pipeline 使用，但该 skill 的 duplicate_allowed=True，记录
    for sid, s in SHARED_SKILL_REGISTRY.items():
        if s.get("duplicate_allowed"):
            users = []
            for pid, p in PIPELINE_REGISTRY.items():
                if sid in p.get("allowed_skills", []):
                    users.append(pid)
            if len(users) > 1:
                conflicts.append(f"{sid}: duplicate_allowed=True used by {users}")
    return conflicts


def audit_gate_coverage_gaps() -> list[str]:
    """审计是否有 pipeline 缺少必要的 gate

    只检查 critical gap:
    - Z-G18 没有 z9.preview_only gate
    - RC-release 没有 rc.packaging / rc.verification / safety.boundary_scan
    """
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    gaps = []
    for pid, p in PIPELINE_REGISTRY.items():
        gates = set(p.get("required_gates", []))
        if pid == "Z-G18" and "z9.preview_only" not in gates:
            gaps.append(f"{pid}: missing z9.preview_only gate")
        if pid == "RC-release":
            for g in ["rc.packaging", "rc.verification", "safety.boundary_scan"]:
                if g not in gates:
                    gaps.append(f"{pid}: missing {g} gate")
    return gaps


def audit_rmatrix_single_source_of_truth() -> list[str]:
    """R-Matrix 只能有一个 canonical skill"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    violations = []
    r_skills = [sid for sid in SHARED_SKILL_REGISTRY if sid.startswith("r_matrix")]
    if len(r_skills) != 1:
        violations.append(f"R-Matrix: expected 1 canonical skill, got {len(r_skills)}: {r_skills}")
    elif r_skills[0] != "r_matrix.evaluate_cycle":
        violations.append(f"R-Matrix canonical skill should be r_matrix.evaluate_cycle, got {r_skills[0]}")
    return violations


def audit_z9_preview_boundary_consistency() -> list[str]:
    """Z-G18 必须完整覆盖 Z9 preview chain，所有 Z9 pipeline 必须经过 preview_only gate"""
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    violations = []

    required_z9 = {"z9.sample.build", "z9.queue.build", "z9.backfill_task.build", "z9.calibration_policy.preview"}

    # Z-G18 workflow must have all Z9 chain
    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        if w.get("pipeline") == "Z-G18":
            nodes = set(w.get("nodes", []))
            missing = required_z9 - nodes
            if missing:
                violations.append(f"{wid}: missing Z9 chain nodes: {missing}")

    # all pipelines using Z9 skills must go through z9.preview_only gate
    for pid, p in PIPELINE_REGISTRY.items():
        skills = set(p.get("allowed_skills", []))
        if skills & required_z9:
            gates = p.get("required_gates", [])
            if "z9.preview_only" not in gates:
                violations.append(f"{pid}: uses Z9 skills but missing z9.preview_only gate")

    # B/R/D single source of truth: 不同 pipeline 不得私造同类型矩阵
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for pid, p in PIPELINE_REGISTRY.items():
        skills = set(p.get("allowed_skills", []))
        # Z-G14 如果声明 B-R-D selection rerun, 则不应只有 r_matrix
        if pid == "Z-G14" and "B" in p.get("purpose", "") and "b_matrix.evaluate_base" not in skills:
            violations.append(f"{pid}: purpose mentions B-R-D but only uses r_matrix.evaluate_cycle")
        # D-Matrix 不得允许 convert_to_base
        if "d_matrix.evaluate_event" in skills:
            # 检查 pipeline 层的 forbidden_capabilities 是否包含 convert_to_base
            fc = p.get("forbidden_capabilities", [])
            if "convert_to_base" not in fc and "long_hold" not in fc:
                violations.append(f"{pid}: uses D-Matrix but missing convert_to_base/long_hold in forbidden")

    # Stock Role Classifier 必须消费 B/R/D
    sr_skills = [s for s in SHARED_SKILL_REGISTRY if "stock_role" in SHARED_SKILL_REGISTRY[s].get("module", "")]
    if not sr_skills:
        violations.append("stock_role.classify not found in SHARED_SKILL_REGISTRY")

    return violations




def audit_g18_role_review_dag_dependency() -> list[str]:
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    violations = []
    w = WORKFLOW_DAG_REGISTRY.get("Z-G18.paper_z9_preview_workflow")
    if not w:
        return ["Z-G18.paper_z9_preview_workflow missing"]
    nodes = w.get("nodes", []); edges = w.get("edges", [])
    if "investment.role_review.build" not in nodes:
        violations.append("Z-G18 workflow missing investment.role_review.build")
    if ["investment.role_review.build", "r_matrix.evaluate_cycle"] not in edges:
        violations.append("Z-G18 role review not connected before r_matrix")
    def has_path(src, tgt):
        g = {}; [g.setdefault(a,[]).append(b) for a,b in edges]; seen=set(); stack=[src]
        while stack:
            n=stack.pop()
            if n==tgt: return True
            if n in seen: continue
            seen.add(n); stack.extend(g.get(n,[]))
        return False
    if "investment.role_review.build" in nodes and "paper.record" in nodes and not has_path("investment.role_review.build", "paper.record"):
        violations.append("Z-G18 role review has no DAG path to paper.record")
    return violations

def run_cross_pipeline_conflict_audit() -> list[str]:
    v = []
    v.extend(audit_rmatrix_single_source_of_truth())
    v.extend(audit_z9_preview_boundary_consistency())
    v.extend(audit_gate_coverage_gaps())
    v.extend(audit_pipeline_skill_conflicts())
    v.extend(audit_g18_role_review_dag_dependency())
    return v
