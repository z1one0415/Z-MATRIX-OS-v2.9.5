#!/usr/bin/env python3
"""
☯️ Workflow DAG Registry v1.0 — 管线工作流契约 (Batch F-4)

Workflow DAG 把 Shared Skill 连接成有向无环图。
每条 workflow 属于一条 pipeline，串联 nodes=skills/gates，定义 edges=执行顺序。

原则:
  1. workflow.nodes 中的 skill/gate 必须存在于各自的 registry
  2. workflow.required_gates 必须存在于 GATE_REGISTRY
  3. workflow.pipeline 必须存在于 PIPELINE_REGISTRY
  4. workflow 不允许环
  5. workflow 不允许声明 forbidden capabilities 之外的真实能力
"""
from __future__ import annotations

from typing import Any

WORKFLOW_DAG_REGISTRY: dict[str, dict[str, Any]] = {
    "Z-G18.paper_z9_preview_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-G18",
        "purpose": "Run G18 paper prediction and Z9 preview chain",
        "nodes": [
            "investment.role_review.build",
            "r_matrix.evaluate_cycle",
            "evidence.aggregate_upstream",
            "conflict.resolve",
            "decision.finalize",
            "paper.record",
            "z9.sample.build",
            "z9.queue.build",
            "z9.backfill_task.build",
            "z9.calibration_policy.preview",
        ],
        "edges": [
            ["investment.role_review.build", "r_matrix.evaluate_cycle"],
            ["r_matrix.evaluate_cycle", "evidence.aggregate_upstream"],
            ["evidence.aggregate_upstream", "conflict.resolve"],
            ["conflict.resolve", "decision.finalize"],
            ["decision.finalize", "paper.record"],
            ["paper.record", "z9.sample.build"],
            ["z9.sample.build", "z9.queue.build"],
            ["z9.queue.build", "z9.backfill_task.build"],
            ["z9.backfill_task.build", "z9.calibration_policy.preview"],
        ],
        "required_gates": [
            "safety.no_real_trade",
            "contract.validation",
            "z9.preview_only",
            "investment.role_review.required",
        ],
        "output_contracts": [
            "G18_PAPER_EXECUTION_RECORD_V10",
            "Z9_CALIBRATION_SAMPLE_V10",
            "Z9_INGESTION_QUEUE_V10",
            "Z9_OUTCOME_BACKFILL_V10",
            "Z9_CALIBRATION_POLICY_V10",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write",
            "real_market_fetch", "auto_calibration",
        ],
        "contract": "docs/architecture/WORKFLOW_DAG_V10.md",
        "test": "tests/test_workflow_dag.py",
    },
    "RC.release_verification_workflow": {
        "layer": "workflow_dag",
        "pipeline": "RC-release",
        "purpose": "Run release candidate package and safety verification",
        "nodes": [
            "rc.checksum.build",
            "rc.packaging",
            "rc.verification",
            "safety.boundary_scan",
        ],
        "edges": [
            ["rc.checksum.build", "rc.packaging"],
            ["rc.packaging", "rc.verification"],
            ["rc.verification", "safety.boundary_scan"],
        ],
        "required_gates": [
            "rc.packaging", "rc.verification", "safety.boundary_scan",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write",
            "real_market_fetch", "auto_calibration",
        ],
        "contract": "docs/architecture/WORKFLOW_DAG_V10.md",
        "test": "tests/test_workflow_dag.py",
    },
    "RMatrix.cycle_validation_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-G09",
        "purpose": "Run R-Matrix cycle validation before rotation scan",
        "nodes": [
            "r_matrix.evaluate_cycle",
            "r_matrix.cycle_valid",
        ],
        "edges": [
            ["r_matrix.evaluate_cycle", "r_matrix.cycle_valid"],
        ],
        "required_gates": [
            "r_matrix.cycle_valid",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write",
            "real_market_fetch", "auto_calibration",
        ],
        "contract": "docs/architecture/WORKFLOW_DAG_V10.md",
        "test": "tests/test_workflow_dag.py",
    },
    "Z-Investment.role_control_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-InvestmentRoleReview",
        "purpose": "Run complete B/R/D role control review before any paper record",
        "nodes": [
            "chain_force.evaluate_10x5",
            "sector_stage.detect",
            "financial.health_gate",
            "b_matrix.evaluate_base",
            "r_matrix.evaluate_cycle",
            "d_matrix.evaluate_event",
            "stock_role.classify",
            "account.constitution.check",
            "portfolio.exposure.analyze",
            "z8.position_control",
            "pre_trade.checklist.validate",
            "g17.manual_veto.preview",
            "safety.no_real_trade",
            "human.final_override.required",
        ],
        "edges": [
            ["chain_force.evaluate_10x5", "sector_stage.detect"],
            ["sector_stage.detect", "financial.health_gate"],
            ["financial.health_gate", "b_matrix.evaluate_base"],
            ["b_matrix.evaluate_base", "stock_role.classify"],
            ["r_matrix.evaluate_cycle", "stock_role.classify"],
            ["d_matrix.evaluate_event", "stock_role.classify"],
            ["stock_role.classify", "account.constitution.check"],
            ["account.constitution.check", "portfolio.exposure.analyze"],
            ["portfolio.exposure.analyze", "z8.position_control"],
            ["z8.position_control", "pre_trade.checklist.validate"],
            ["pre_trade.checklist.validate", "g17.manual_veto.preview"],
            ["g17.manual_veto.preview", "safety.no_real_trade"],
            ["safety.no_real_trade", "human.final_override.required"],
        ],
        "required_gates": [
            "chain_force.valid", "sector_stage.valid", "financial.health_valid",
            "b_matrix.base_valid", "d_matrix.event_valid",
            "stock_role.classification_valid", "account.constitution.valid",
            "portfolio.exposure.valid", "z8.position_control.valid",
            "pre_trade.checklist.complete",
            "safety.no_real_trade", "human.final_override.required",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write",
            "real_market_fetch", "auto_calibration",
        ],
        "contract": "docs/architecture/WORKFLOW_DAG_V10.md",
        "test": "tests/test_workflow_dag.py",
    },
    "Z-PaperData.paper_outcome_loop_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-PaperDataLoop",
        "purpose": "Run local paper ledger outcome loop and lightweight backtest",
        "nodes": [
            "data_facts.load_price_bars",
            "paper_trade.ledger.build",
            "paper_trade.outcome_backfill.calculate",
            "portfolio.exposure.calculate_from_history",
            "backtest.lightweight_role.run",
            "monthly_review.build",
            "safety.no_real_trade",
        ],
        "edges": [
            ["data_facts.load_price_bars", "paper_trade.ledger.build"],
            ["paper_trade.ledger.build", "paper_trade.outcome_backfill.calculate"],
            ["paper_trade.outcome_backfill.calculate", "portfolio.exposure.calculate_from_history"],
            ["portfolio.exposure.calculate_from_history", "backtest.lightweight_role.run"],
            ["backtest.lightweight_role.run", "monthly_review.build"],
            ["monthly_review.build", "safety.no_real_trade"],
        ],
        "required_gates": [
            "data_facts.valid",
            "paper_ledger.valid",
            "outcome_backfill.valid",
            "backtest.report.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write",
            "real_market_fetch", "external_api_default_on", "auto_calibration",
        ],
        "contract": "docs/architecture/PERSONAL_QUANT_DATA_VALIDITY_LAYER_V10.md",
        "test": "tests/test_lightweight_backtest.py",
    },
    "Z-EventStore.unified_event_ledger_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-EventStore",
        "purpose": "Unified event ledger: build → store → query → lineage → export → safety",
        "nodes": [
            "event_store.event.build",
            "event_store.local.append",
            "event_store.local.query",
            "event_store.lineage.trace",
            "event_store.jsonl.export",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "event.schema.valid",
            "event.safety.valid",
            "event.lineage.valid",
            "event.append_only.valid",
            "safety.no_real_trade",
        ],
        "edges": [
            ("event_store.event.build", "event_store.local.append"),
            ("event_store.local.append", "event_store.local.query"),
            ("event_store.local.query", "event_store.lineage.trace"),
            ("event_store.lineage.trace", "event_store.jsonl.export"),
            ("event_store.jsonl.export", "safety.no_real_trade"),
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write",
            "hermes_memory_write", "auto_calibration", "prompt_auto_injection",
            "real_market_fetch", "external_api_default_on",
        ],
        "contract": "docs/architecture/EVENT_STORE_ARCHITECTURE_V10.md",
        "test": "tests/test_event_store_architecture.py",
    },
    "Z-Hermes.memory_kernel_preview_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-HermesMemoryKernel",
        "purpose": "Hermes memory kernel read-only preview workflow",
        "nodes": [
            "hermes.core_memory.load", "hermes.working_context.build",
            "hermes.heuristics.retrieve", "hermes.prompt_patch.preview",
            "hermes.memory_candidate.preview", "hermes.calibration_event.preview",
            "hermes.memory_kernel.preview",
            "hermes.memory_candidate_event.build", "hermes.calibration_event.build",
            "hermes.prompt_patch_event.build",
            "safety.no_real_trade",
        ],
        "edges": [
            ("hermes.core_memory.load", "hermes.working_context.build"),
            ("hermes.working_context.build", "hermes.heuristics.retrieve"),
            ("hermes.heuristics.retrieve", "hermes.prompt_patch.preview"),
            ("hermes.prompt_patch.preview", "hermes.memory_kernel.preview"),
            ("hermes.memory_kernel.preview", "hermes.memory_candidate.preview"),
            ("hermes.memory_candidate.preview", "hermes.calibration_event.preview"),
            ("hermes.calibration_event.preview", "hermes.memory_candidate_event.build"),
            ("hermes.memory_candidate_event.build", "hermes.calibration_event.build"),
            ("hermes.calibration_event.build", "hermes.prompt_patch_event.build"),
            ("hermes.prompt_patch_event.build", "safety.no_real_trade"),
        ],
        "required_gates": [
            "hermes.read_only.valid", "hermes.preview_only.valid",
            "hermes.no_memory_write.valid", "hermes.no_auto_calibration.valid",
            "hermes.no_prompt_auto_injection.valid", "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "real_market_fetch",
            "external_api_default_on",
        ],
        "contract": "docs/architecture/HERMES_MEMORY_KERNEL_ARCHITECTURE_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
    "Z-Prompt.middleware_preview_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-PromptMiddlewarePreview",
        "purpose": "Prompt hot-patching middleware preview: request → render → audit → event",
        "nodes": [
            "prompt.patch_request.build", "prompt.policy.validate_request",
            "prompt.render_preview.build", "prompt.policy.validate_render",
            "prompt.audit.build", "prompt.policy.validate_audit",
            "prompt.patch_request_event.build", "prompt.render_preview_event.build",
            "prompt.audit_event.build",
            "safety.no_real_trade",
        ],
        "edges": [
            ("prompt.patch_request.build", "prompt.policy.validate_request"),
            ("prompt.policy.validate_request", "prompt.render_preview.build"),
            ("prompt.render_preview.build", "prompt.policy.validate_render"),
            ("prompt.policy.validate_render", "prompt.audit.build"),
            ("prompt.audit.build", "prompt.policy.validate_audit"),
            ("prompt.policy.validate_audit", "prompt.patch_request_event.build"),
            ("prompt.patch_request_event.build", "prompt.render_preview_event.build"),
            ("prompt.render_preview_event.build", "prompt.audit_event.build"),
            ("prompt.audit_event.build", "safety.no_real_trade"),
        ],
        "required_gates": [
            "prompt.preview_only.valid", "prompt.no_runtime_injection.valid",
            "prompt.no_system_prompt_write.valid", "prompt.no_auto_injection.valid",
            "prompt.audit.valid", "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "system_prompt_write",
            "runtime_prompt_injection", "real_market_fetch", "external_api_default_on",
        ],
        "contract": "docs/architecture/PROMPT_HOT_PATCHING_MIDDLEWARE_PREVIEW_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
    "Z-Approval.reflection_loop_workflow": {
        "layer": "workflow_dag",
        "pipeline": "Z-ApprovalReflectionLoop",
        "purpose": "Approval-Required Reflection Loop: request → policy → queue → decision → event",
        "nodes": [
            "approval.request.build",
            "approval.policy.validate_request",
            "approval.queue.preview",
            "approval.decision.build",
            "approval.policy.validate_decision",
            "approval.request_event.build",
            "approval.human_event.build",
            "safety.no_real_trade",
        ],
        "edges": [
            ("approval.request.build", "approval.policy.validate_request"),
            ("approval.policy.validate_request", "approval.queue.preview"),
            ("approval.queue.preview", "approval.decision.build"),
            ("approval.decision.build", "approval.policy.validate_decision"),
            ("approval.policy.validate_decision", "approval.request_event.build"),
            ("approval.request_event.build", "approval.human_event.build"),
            ("approval.human_event.build", "safety.no_real_trade"),
        ],
        "required_gates": [
            "approval.request.valid", "approval.decision.valid",
            "approval.no_auto_effect.valid", "approval.human_required.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "real_market_fetch",
            "external_api_default_on",
        ],
        "contract": "docs/architecture/APPROVAL_REQUIRED_REFLECTION_LOOP_V10.md",
        "test": "tests/test_approval_loop_architecture.py",
    },
}


def get_workflow(workflow_id: str) -> dict | None:
    return WORKFLOW_DAG_REGISTRY.get(workflow_id)


def get_workflows_for_pipeline(pipeline_id: str) -> list[tuple[str, dict]]:
    return [(wid, w) for wid, w in WORKFLOW_DAG_REGISTRY.items()
            if w.get("pipeline") == pipeline_id]


def topological_order(workflow_id: str) -> list[str]:
    """返回 workflow 的拓扑排序（简单线性，因为 edges 定义的有向顺序）"""
    w = get_workflow(workflow_id)
    if not w:
        return []
    # 用 Kahn 算法探测环
    nodes = list(w["nodes"])
    edges = [list(e) for e in w["edges"]]
    in_degree = {n: 0 for n in nodes}
    adj = {n: [] for n in nodes}
    for fr, to in edges:
        if fr in adj and to in in_degree:
            adj[fr].append(to)
            in_degree[to] += 1

    queue = [n for n in nodes if in_degree[n] == 0]
    order = []
    while queue:
        n = queue.pop(0)
        order.append(n)
        for m in adj.get(n, []):
            in_degree[m] -= 1
            if in_degree[m] == 0:
                queue.append(m)
    # 如果还有剩余节点，说明有环
    if len(order) != len(nodes):
        raise ValueError(f"cycle detected in workflow {workflow_id}")
    return order


def check_workflow_dag_integrity() -> list[str]:
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY

    violations = []

    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        if w.get("layer") != "workflow_dag":
            violations.append(f"{wid}: layer != workflow_dag")
        if not w.get("pipeline"):
            violations.append(f"{wid}: missing pipeline")
        if not w.get("purpose"):
            violations.append(f"{wid}: missing purpose")
        if not w.get("nodes"):
            violations.append(f"{wid}: missing nodes")
        if not w.get("contract"):
            violations.append(f"{wid}: missing contract")
        if not w.get("test"):
            violations.append(f"{wid}: missing test")

        # pipeline 必须存在于 PIPELINE_REGISTRY
        pid = w.get("pipeline")
        if pid and pid not in PIPELINE_REGISTRY:
            violations.append(f"{wid}: pipeline '{pid}' not in PIPELINE_REGISTRY")

        # nodes 中 skill 必须存在于 SHARED_SKILL_REGISTRY
        for nid in w.get("nodes", []):
            if nid not in SHARED_SKILL_REGISTRY and nid not in GATE_REGISTRY:
                violations.append(f"{wid}: node '{nid}' not in any registry")

        # required_gates 必须存在于 GATE_REGISTRY
        for g in w.get("required_gates", []):
            if g not in GATE_REGISTRY:
                violations.append(f"{wid}: required_gate '{g}' not in GATE_REGISTRY")

        # 不允许环
        try:
            topological_order(wid)
        except ValueError as e:
            violations.append(f"{wid}: {e}")

        # forbidden_capabilities 必须包含 no-real-ops
        fc = w.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            if required not in fc:
                violations.append(f"{wid}: forbidden_capabilities missing {required}")

    return violations


def check_workflow_nodes_registered() -> list[str]:
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    unreg = []
    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        for nid in w.get("nodes", []):
            if nid not in SHARED_SKILL_REGISTRY and nid not in GATE_REGISTRY:
                unreg.append(f"{wid} -> {nid}")
    return unreg


def check_workflow_gates_registered() -> list[str]:
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    missing = []
    for wid, w in WORKFLOW_DAG_REGISTRY.items():
        for g in w.get("required_gates", []):
            if g not in GATE_REGISTRY:
                missing.append(f"{wid} -> {g}")
    return missing
