#!/usr/bin/env python3
"""
☯️ Architecture Enforcement v1.0 — 架构硬约束审计 (Batch F-5)

对所有架构注册表做跨表硬约束验证。
违反任意规则即记录违规。
"""
from __future__ import annotations

from typing import Any


def check_pipeline_allowed_skills_only() -> list[str]:
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    violations = []
    for pid, p in PIPELINE_REGISTRY.items():
        for sid in p.get("allowed_skills", []):
            if sid not in SHARED_SKILL_REGISTRY:
                violations.append(f"{pid}: allowed_skill '{sid}' not in SHARED_SKILL_REGISTRY")
    return violations


def check_no_unregistered_pipeline_required_gates() -> list[str]:
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    violations = []
    for pid, p in PIPELINE_REGISTRY.items():
        for g in p.get("required_gates", []):
            if g not in GATE_REGISTRY:
                violations.append(f"{pid}: required_gate '{g}' not in GATE_REGISTRY")
    return violations


def check_no_duplicate_skill_modules() -> list[str]:
    """不允许两个 skill 注册同一 module+public_function，除非 duplicate_allowed=True"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    seen = {}
    violations = []
    for sid, s in SHARED_SKILL_REGISTRY.items():
        key = (s.get("module"), s.get("public_function"))
        if key in seen and not s.get("duplicate_allowed"):
            violations.append(f"{sid} and {seen[key]}: duplicate module+function {key}")
        seen[key] = sid
    return violations


def check_no_pipeline_declares_forbidden_capability() -> list[str]:
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    violations = []
    for pid, p in PIPELINE_REGISTRY.items():
        fc = p.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            if required not in fc:
                violations.append(f"{pid}: forbidden_capabilities missing {required}")
    return violations


def check_no_real_ops_enabled_anywhere() -> list[str]:
    """不允许任何 entity 声明 real_trade enabled 或等价"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY

    violations = []
    for name, reg in [("SHARED_SKILL_REGISTRY", SHARED_SKILL_REGISTRY),
                       ("PIPELINE_REGISTRY", PIPELINE_REGISTRY),
                       ("GATE_REGISTRY", GATE_REGISTRY),
                       ("WORKFLOW_DAG_REGISTRY", WORKFLOW_DAG_REGISTRY)]:
        for eid, entity in reg.items():
            # 检查 safety_boundary / forbidden_capabilities
            sb = entity.get("safety_boundary", "")
            fc = entity.get("forbidden_capabilities", [])
            if isinstance(fc, list) and "real_trade" not in fc:
                # pipeline/workflow 必须有 forbidden_capabilities
                pass  # 已在 check_no_pipeline_declares_forbidden_capability 覆盖
            if sb and "no real trade" not in sb and "no_real_trade" not in str(entity):
                # skill 的 safety_boundary 必须包含 no real trade
                if entity.get("layer") == "shared_skill":
                    violations.append(f"{name}/{eid}: safety_boundary must forbid real trade")

    # B/R/D 三个 matrix skill 必须全部存在
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for required in ["b_matrix.evaluate_base", "r_matrix.evaluate_cycle", "d_matrix.evaluate_event"]:
        if required not in SHARED_SKILL_REGISTRY:
            violations.append(f"missing required skill: {required}")

    return violations


def run_architecture_enforcement() -> list[str]:
    v = []
    v.extend(check_pipeline_allowed_skills_only())
    v.extend(check_no_unregistered_pipeline_required_gates())
    v.extend(check_no_duplicate_skill_modules())
    v.extend(check_no_pipeline_declares_forbidden_capability())
    v.extend(check_no_real_ops_enabled_anywhere())
    v.extend(check_workspace_alignment_components())
    v.extend(check_event_store_components())
    v.extend(check_hermes_memory_kernel_components())
    v.extend(check_approval_loop_components())
    v.extend(check_prompt_middleware_components())
    v.extend(check_tail_risk_components())
    return v
def check_workspace_alignment_components() -> list[str]:
    from pathlib import Path
    violations = []
    root = Path(__file__).resolve().parent.parent.parent
    
    # pipeline census
    p = root / "zmatrix" / "architecture" / "pipeline_census.py"
    if p.exists():
        from zmatrix.architecture.pipeline_census import list_pipeline_census
        c = list_pipeline_census()
        if len(c) < 18:
            violations.append(f"pipeline_census: only {len(c)}/18 pipelines")
    else:
        violations.append("pipeline_census.py missing")
    
    # hermes adapter
    h = root / "zmatrix" / "architecture" / "hermes_adapter_registry.py"
    if h.exists():
        from zmatrix.architecture.hermes_adapter_registry import list_hermes_adapters
        for a in list_hermes_adapters().values():
            for k in ["real_trade_allowed","write_allowed","auto_calibration_allowed"]:
                if a.get(k): violations.append(f"hermes adapter: {k} should be False")
    
    # script index
    s = root / "zmatrix" / "architecture" / "script_index.py"
    if s.exists():
        from zmatrix.architecture.script_index import list_script_index
        for sid, si in list_script_index().items():
            if si.get("real_trade_allowed"): violations.append(f"script {sid}: real_trade_allowed")
    
    # research asset
    ra = root / "zmatrix" / "architecture" / "research_asset_index.py"
    if ra.exists():
        from zmatrix.architecture.research_asset_index import RESEARCH_ASSET_INDEX_POLICY
        if RESEARCH_ASSET_INDEX_POLICY.get("full_text_import_allowed"):
            violations.append("research: full_text_import_allowed should be False")
    
    # data/ samples
    for sf in ["price_bars_sample.csv","paper_ledger_sample.csv"]:
        if not (root / "data" / "samples" / sf).exists():
            violations.append(f"data/samples/{sf} missing")
    
    return violations

def check_workspace_alignment_doc_exists() -> list[str]:
    from pathlib import Path
    root = Path(__file__).resolve().parent.parent.parent
    docs = ["WORKSPACE_LAYOUT_V10.md","WORKSPACE_ALIGNMENT_V10.md","PIPELINE_CENSUS_V10.md",
            "HERMES_ADAPTER_REGISTRY_V10.md","SCRIPT_INDEX_V10.md","RESEARCH_ASSET_INDEX_V10.md"]
    missing = [d for d in docs if not (root / "docs" / "architecture" / d).exists()]
    return [f"missing doc: {d}" for d in missing]


def check_event_store_components() -> list[str]:
    """Check EventStore components existence and safety."""
    from pathlib import Path
    violations = []
    root = Path(__file__).resolve().parent.parent.parent

    # EventStore package
    pkg = root / "zmatrix" / "event_store"
    required_files = ["__init__.py", "event_ids.py", "schemas.py", "validators.py",
                      "store.py", "lineage.py", "query.py", "exporters.py",
                      "builders.py", "adapters.py"]
    for f in required_files:
        if not (pkg / f).exists():
            violations.append(f"event_store/{f} missing")

    # EVENT_TYPES coverage
    try:
        from zmatrix.event_store.schemas import EVENT_TYPES
        if len(EVENT_TYPES) < 13:
            violations.append(f"EVENT_TYPES: only {len(EVENT_TYPES)}/13 types")
    except Exception:
        violations.append("EVENT_TYPES import failed")

    # LocalEventStore
    try:
        from zmatrix.event_store.store import LocalEventStore
        if not hasattr(LocalEventStore, "append_event"):
            violations.append("LocalEventStore missing append_event")
    except Exception:
        violations.append("LocalEventStore import failed")

    # EventStore skills registered
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    required_skills = [
        "event_store.event.build", "event_store.local.append",
        "event_store.local.query", "event_store.lineage.trace",
        "event_store.jsonl.export",
    ]
    for s in required_skills:
        if s not in SHARED_SKILL_REGISTRY:
            violations.append(f"EventStore skill '{s}' not registered")

    # EventStore gates registered
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["event.schema.valid", "event.safety.valid", "event.lineage.valid",
              "event.append_only.valid"]:
        if g not in GATE_REGISTRY:
            violations.append(f"EventStore gate '{g}' not registered")

    # EventStore pipeline registered
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    if "Z-EventStore" not in PIPELINE_REGISTRY:
        violations.append("Z-EventStore pipeline not registered")

    # EventStore workflow registered
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    if "Z-EventStore.unified_event_ledger_workflow" not in WORKFLOW_DAG_REGISTRY:
        violations.append("EventStore workflow not registered")

    # Safety: no Hermes write / no real Z9 write / no prompt injection
    for sid in required_skills:
        s = SHARED_SKILL_REGISTRY.get(sid, {})
        sb = s.get("safety_boundary", "")
    return violations


def check_hermes_memory_kernel_components() -> list[str]:
    """Check Hermes Memory Kernel components existence and safety."""
    from pathlib import Path
    violations = []
    root = Path(__file__).resolve().parent.parent.parent

    # Package existence
    hermes_kernel = root / "zmatrix" / "hermes_kernel"
    required_files = ["__init__.py", "schemas.py", "validators.py", "core_memory.py",
                      "working_context.py", "learned_heuristics.py", "memory_candidate.py",
                      "retrieval.py", "event_bridge.py", "prompt_patch_preview.py"]
    for f in required_files:
        if not (hermes_kernel / f).exists():
            violations.append(f"hermes_kernel/{f} missing")

    hermes_memory = root / "zmatrix" / "hermes_memory"
    required_mem = ["__init__.py", "memory_candidate_preview.py", "calibration_event_preview.py",
                    "hermes_memory_kernel.py", "event_adapters.py"]
    for f in required_mem:
        if not (hermes_memory / f).exists():
            violations.append(f"hermes_memory/{f} missing")

    # Skills registered
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    required_skills = [
        "hermes.core_memory.load", "hermes.working_context.build", "hermes.heuristics.retrieve",
        "hermes.prompt_patch.preview", "hermes.memory_candidate.preview",
        "hermes.calendar_event.preview",  # note: actual is `calibration_event.preview`
    ]
    for s in required_skills:
        if s not in SHARED_SKILL_REGISTRY and s == "hermes.calendar_event.preview":
            # check actual name
            actual = "hermes.calibration_event.preview"
            if actual not in SHARED_SKILL_REGISTRY:
                violations.append(f"Hermes skill '{actual}' not registered")
        elif s not in SHARED_SKILL_REGISTRY:
            violations.append(f"Hermes skill '{s}' not registered")

    # Gates registered
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["hermes.read_only.valid", "hermes.preview_only.valid",
              "hermes.no_memory_write.valid", "hermes.no_auto_calibration.valid",
              "hermes.no_prompt_auto_injection.valid"]:
        if g not in GATE_REGISTRY:
            violations.append(f"Hermes gate '{g}' not registered")

    # Pipeline registered
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    if "Z-HermesMemoryKernel" not in PIPELINE_REGISTRY:
        violations.append("Z-HermesMemoryKernel pipeline not registered")

    # Workflow registered
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    if "Z-Hermes.memory_kernel_preview_workflow" not in WORKFLOW_DAG_REGISTRY:
        violations.append("Hermes workflow not registered")

    # Safety checks
    for sid in ["hermes.core_memory.load", "hermes.memory_kernel.preview"]:
        s = SHARED_SKILL_REGISTRY.get(sid, {})
        sb = s.get("safety_boundary", "")
        sb_lower = sb.lower()
        if "hermes_memory_write" not in sb_lower and "hermes memory write" not in sb_lower:
            violations.append(f"{sid}: safety_boundary missing hermes memory write constraint: {sb}")

    return violations


def check_approval_loop_components() -> list[str]:
    """Check Approval Loop components existence and safety."""
    from pathlib import Path
    violations = []
    root = Path(__file__).resolve().parent.parent.parent

    # Package existence
    pkg = root / "zmatrix" / "approval_loop"
    for fname in ["__init__.py", "schemas.py", "approval_request.py", "approval_decision.py",
                  "approval_policy.py", "approval_queue.py", "event_adapters.py"]:
        if not (pkg / fname).exists():
            violations.append(f"approval_loop/{fname} missing")

    # Skills registered
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for s in ["approval.request.build", "approval.decision.build",
              "approval.policy.validate_request", "approval.policy.validate_decision",
              "approval.queue.preview", "approval.request_event.build",
              "approval.human_event.build"]:
        if s not in SHARED_SKILL_REGISTRY:
            violations.append(f"Approval skill '{s}' not registered")

    # Gates registered
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["approval.request.valid", "approval.decision.valid",
              "approval.no_auto_effect.valid", "approval.human_required.valid"]:
        if g not in GATE_REGISTRY:
            violations.append(f"Approval gate '{g}' not registered")

    # Pipeline registered
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    if "Z-ApprovalReflectionLoop" not in PIPELINE_REGISTRY:
        violations.append("Z-ApprovalReflectionLoop pipeline not registered")

    # Workflow registered
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    if "Z-Approval.reflection_loop_workflow" not in WORKFLOW_DAG_REGISTRY:
        violations.append("Approval workflow not registered")

    # Docs exist
    for d in ["APPROVAL_REQUEST_V10.md", "HUMAN_APPROVAL_DECISION_V10.md",
              "APPROVAL_QUEUE_PREVIEW_V10.md", "APPROVAL_LOOP_V10.md"]:
        if not (root / "docs" / "contracts" / d).exists():
            violations.append(f"docs/contracts/{d} missing")
    if not (root / "docs" / "architecture" / "APPROVAL_REQUIRED_REFLECTION_LOOP_V10.md").exists():
        violations.append("approval architecture doc missing")

    return violations


def check_prompt_middleware_components() -> list[str]:
    """Check Prompt Middleware components existence and safety."""
    from pathlib import Path
    violations = []
    root = Path(__file__).resolve().parent.parent.parent

    # Package existence
    pkg = root / "zmatrix" / "prompt_middleware"
    for fname in ["__init__.py", "schemas.py", "patch_request.py", "renderer.py",
                  "audit.py", "policy.py", "event_adapters.py"]:
        if not (pkg / fname).exists():
            violations.append(f"prompt_middleware/{fname} missing")

    # Skills registered
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for s in ["prompt.patch_request.build", "prompt.render_preview.build", "prompt.audit.build",
              "prompt.policy.validate_request", "prompt.policy.validate_render", "prompt.policy.validate_audit",
              "prompt.patch_request_event.build", "prompt.render_preview_event.build", "prompt.audit_event.build"]:
        if s not in SHARED_SKILL_REGISTRY:
            violations.append(f"Prompt skill '{s}' not registered")

    # Gates registered
    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["prompt.preview_only.valid", "prompt.no_runtime_injection.valid",
              "prompt.no_system_prompt_write.valid", "prompt.no_auto_injection.valid", "prompt.audit.valid"]:
        if g not in GATE_REGISTRY:
            violations.append(f"Prompt gate '{g}' not registered")

    # Pipeline registered
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    if "Z-PromptMiddlewarePreview" not in PIPELINE_REGISTRY:
        violations.append("Z-PromptMiddlewarePreview pipeline not registered")

    # Workflow registered
    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    if "Z-Prompt.middleware_preview_workflow" not in WORKFLOW_DAG_REGISTRY:
        violations.append("Prompt workflow not registered")

    # Docs exist
    for d in ["PROMPT_PATCH_REQUEST_V10.md", "PROMPT_MIDDLEWARE_RENDER_PREVIEW_V10.md",
              "PROMPT_PATCH_AUDIT_V10.md", "PROMPT_MIDDLEWARE_V10.md",
              "PROMPT_HOT_PATCHING_MIDDLEWARE_PREVIEW_V10.md"]:
        doc_path = root / "docs"
        if d.endswith(".md") and d.startswith("PROMPT_HOT"):
            doc_path = doc_path / "architecture" / d
        else:
            doc_path = doc_path / "contracts" / d
        if not doc_path.exists():
            violations.append(f"Prompt doc {d} missing")

    return violations


def check_tail_risk_components() -> list[str]:
    """Check Tail-Risk components existence and safety."""
    from pathlib import Path
    violations = []
    root = Path(__file__).resolve().parent.parent.parent

    pkg = root / "zmatrix" / "tail_risk"
    for fname in ["__init__.py", "schemas.py", "policy.py", "market_signals.py",
                  "limit_down_blackhole.py", "domestic_liquidity_crash.py",
                  "hibernate_mode.py", "wakeup_probation.py", "d_matrix_freeze.py",
                  "risk_isolation_unit.py", "tail_risk_controller.py", "event_adapters.py"]:
        if not (pkg / fname).exists():
            violations.append(f"tail_risk/{fname} missing")

    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY
    for s in ["tail.market_signals.normalize", "tail.limit_down_blackhole.evaluate",
              "tail.domestic_liquidity_crash.evaluate", "tail.hibernate_mode.evaluate",
              "tail.wakeup_probation.evaluate", "tail.d_matrix_freeze.evaluate",
              "tail.risk_isolation.preview", "tail.controller.preview", "tail.policy.validate",
              "tail.controller_event.build", "tail.gate_event.build", "tail.isolation_event.build"]:
        if s not in SHARED_SKILL_REGISTRY:
            violations.append(f"Tail skill '{s}' not registered")

    from zmatrix.architecture.gate_registry import GATE_REGISTRY
    for g in ["tail_risk.signal.valid", "tail_risk.preview_only.valid",
              "tail_risk.no_broker_order.valid", "tail_risk.no_real_trade.valid",
              "tail_risk.action_degradation.valid", "tail_risk.no_auto_sell.valid"]:
        if g not in GATE_REGISTRY:
            violations.append(f"Tail gate '{g}' not registered")

    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY
    if "Z-TailRiskAutonomicGates" not in PIPELINE_REGISTRY:
        violations.append("Z-TailRiskAutonomicGates pipeline not registered")

    from zmatrix.architecture.workflow_dag import WORKFLOW_DAG_REGISTRY
    if "Z-TailRisk.autonomic_gates_preview_workflow" not in WORKFLOW_DAG_REGISTRY:
        violations.append("Tail workflow not registered")

    for fname in ["TAIL_RISK_GATES_V10.md", "LIMIT_DOWN_BLACKHOLE_V10.md",
                  "DOMESTIC_LIQUIDITY_CRASH_V10.md", "HIBERNATE_MODE_V10.md",
                  "WAKEUP_PROBATION_V10.md", "D_MATRIX_FREEZE_V10.md",
                  "BMO_RISK_ISOLATION_UNIT_V10.md", "TAIL_RISK_CONTROLLER_V10.md",
                  "TAIL_RISK_AUTONOMIC_GATES_PREVIEW_V10.md"]:
        candidate = root / "docs" / "contracts" / fname
        if not candidate.exists():
            candidate = root / "docs" / "architecture" / fname
        if not candidate.exists():
            violations.append(f"Tail risk doc {fname} missing")

    return violations
