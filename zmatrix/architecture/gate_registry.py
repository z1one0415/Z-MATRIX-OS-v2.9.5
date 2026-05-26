#!/usr/bin/env python3
"""
☯️ Gate Registry v1.0 — Z-MATRIX-OS 三层架构第三层组件 (Batch F-3)

Gate Registry 是系统控制层的 gate 注册表。
所有安全边界、contract validation、preview-only、RC verification 闸门必须注册于此。

原则:
  1. gate 是系统控制层组件，不得实现业务判断
  2. pipeline.required_gates 必须全部存在于 GATE_REGISTRY
  3. blocking gate 不可降级通过
"""
from __future__ import annotations

from typing import Any

GATE_REGISTRY: dict[str, dict[str, Any]] = {
    "safety.no_real_trade": {
        "layer": "system_control",
        "gate_type": "safety",
        "purpose": "Block real trade / broker order / market order capabilities",
        "owner": "SystemCore",
        "applies_to": ["Z-G18", "Z-G09", "Z-G14", "RC-release"],
        "enforced_by": "zmatrix.action.action_contracts.assert_no_real_trade",
        "blocking": True,
        "degradable": False,
        "forbidden_tokens": [
            "BUY", "SELL", "AUTO_TRADE", "MARKET_ORDER", "BROKER_ORDER", "REAL_TRADE",
        ],
        "contract": "docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md",
        "test": "tests/test_g18_final_decision_envelope_v11.py",
    },
    "z9.preview_only": {
        "layer": "system_control",
        "gate_type": "write_boundary",
        "purpose": "Ensure all Z9 outputs remain preview-only and no real write occurs",
        "owner": "Z9",
        "applies_to": ["Z-G18"],
        "enforced_by": "tests/test_z9_calibration_policy_contract.py",
        "blocking": True,
        "degradable": False,
        "required_false_flags": [
            "z9_real_write_allowed", "z9_queue_write_allowed",
            "z9_outcome_write_allowed", "z9_market_fetch_allowed",
            "z9_auto_calibration_allowed",
        ],
        "contract": "docs/contracts/Z9_CALIBRATION_POLICY_V10.md",
        "test": "tests/test_z9_calibration_policy_contract.py",
    },
    "contract.validation": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure architecture contracts and runtime payload contracts are structurally valid",
        "owner": "SystemCore",
        "applies_to": ["Z-G18", "RC-release"],
        "enforced_by": "tests/*_contract*.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/GATE_REGISTRY_V10.md",
        "test": "tests/test_gate_registry.py",
    },
    "rc.packaging": {
        "layer": "system_control",
        "gate_type": "release",
        "purpose": "Ensure RC release package files and checksums are complete",
        "owner": "RC",
        "applies_to": ["RC-release"],
        "enforced_by": "tests/test_rc_packaging.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/release/RC_MANIFEST_v2.9.6.md",
        "test": "tests/test_rc_packaging.py",
    },
    "rc.verification": {
        "layer": "system_control",
        "gate_type": "release",
        "purpose": "Run RC verification gate and safety boundary scan",
        "owner": "RC",
        "applies_to": ["RC-release"],
        "enforced_by": "scripts/verify_rc_candidate.sh",
        "blocking": True,
        "degradable": False,
        "contract": "docs/release/RC_VERIFICATION_REPORT_TEMPLATE_v2.9.6.md",
        "test": "tests/test_rc_verification_gate.py",
    },
    "r_matrix.cycle_valid": {
        "layer": "system_control",
        "gate_type": "data_contract",
        "purpose": "Ensure R-Matrix cycle output is contract-valid before downstream use",
        "owner": "R-Matrix",
        "applies_to": ["Z-G09", "Z-G14"],
        "enforced_by": "tests/test_rmatrix_contract_schema.py",
        "blocking": True,
        "degradable": True,
        "contract": "docs/contracts/R_MATRIX_V2_CONTRACT.md",
        "test": "tests/test_rmatrix_contract_schema.py",
    },
    "safety.boundary_scan": {
        "layer": "system_control",
        "gate_type": "safety",
        "purpose": "Scan executable surfaces for real trade / real write boundary leaks",
        "owner": "SystemCore",
        "applies_to": ["RC-release"],
        "enforced_by": "scripts/verify_rc_candidate.sh",
        "blocking": True,
        "degradable": False,
        "contract": "docs/release/RC_MANIFEST_v2.9.6.md",
        "test": "tests/test_rc_verification_gate.py",
    },
    # ── B/R/D Investment Role Gates (v2.9.8-dev) ──
    "b_matrix.base_valid": {
        "layer": "system_control",
        "gate_type": "data_contract",
        "purpose": "Ensure B-Matrix output is contract-valid and base_role_eligible",
        "owner": "R-Matrix",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_b_matrix_contract.py",
        "blocking": True,
        "degradable": True,
        "contract": "docs/contracts/B_MATRIX_V10.md",
        "test": "tests/test_b_matrix_contract.py",
    },
    "d_matrix.event_valid": {
        "layer": "system_control",
        "gate_type": "data_contract",
        "purpose": "Ensure D-Matrix output is contract-valid and short_event_eligible",
        "owner": "D-Matrix",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_d_matrix_contract.py",
        "blocking": True,
        "degradable": True,
        "contract": "docs/contracts/D_MATRIX_V10.md",
        "test": "tests/test_d_matrix_contract.py",
    },
    "stock_role.classification_valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure Stock Role Classifier output is valid and D cannot become A",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_stock_role_classifier.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/STOCK_ROLE_CLASSIFIER_V10.md",
        "test": "tests/test_stock_role_classifier.py",
    },
    "account.constitution.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure candidate passes bucket/cash/exposure constraints",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_account_constitution.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/ACCOUNT_CONSTITUTION_V10.md",
        "test": "tests/test_account_constitution.py",
    },
    "portfolio.exposure.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure candidate does not cause excessive portfolio overlap",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_portfolio_exposure.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/PORTFOLIO_EXPOSURE_V10.md",
        "test": "tests/test_portfolio_exposure.py",
    },
    "pre_trade.checklist.complete": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure pre-trade 8-question checklist is complete before paper record",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_pre_trade_checklist.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/PRE_TRADE_CHECKLIST_V10.md",
        "test": "tests/test_pre_trade_checklist.py",
    },
    "human.final_override.required": {
        "layer": "system_control",
        "gate_type": "safety",
        "purpose": "Ensure G17 human final veto is required before any real decision",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview", "Z-G18"],
        "enforced_by": "zmatrix.investment.investment_role_workflow (g17_human_veto_required=True)",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/SYSTEM_CONTROLLER_MVP_V10.md",
        "test": "tests/test_system_controller_mvp.py",
    },
    "chain_force.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure 10-chain×5-force analysis is complete",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_chain_force_10x5.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_chain_force_10x5.py",
    },
    "sector_stage.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure sector stage is valid and rotation rules are applied",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_sector_stage.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_sector_stage.py",
    },
    "financial.health_valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure financial health hard gate is passed before long-term core evaluation",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_financial_health_gate.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_financial_health_gate.py",
    },
    "z8.position_control.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure Z8 position control limits are respected",
        "owner": "SystemCore",
        "applies_to": ["Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_z8_position_control.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_z8_position_control.py",
    },

    "investment.role_review.required": {
        "layer": "system_control",
        "gate_type": "investment_control",
        "purpose": "Ensure G18 paper record cannot bypass B/R/D 7-layer investment role review",
        "owner": "SystemCore",
        "applies_to": ["Z-G18", "Z-InvestmentRoleReview"],
        "enforced_by": "tests/test_brd_architecture_integration.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_brd_architecture_integration.py",
    },

    "data_facts.valid": {
        "layer": "system_control",
        "gate_type": "data_contract",
        "purpose": "Ensure local CSV data facts satisfy schemas",
        "owner": "DataFacts",
        "applies_to": ["Z-PaperDataLoop"],
        "enforced_by": "tests/test_data_fact_schemas.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/DATA_FACT_LAYER_V10.md",
        "test": "tests/test_data_fact_schemas.py",
    },
    "paper_ledger.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure paper ledger blocks D_REJECT/WATCH_ONLY and forbidden action tokens",
        "owner": "PaperTrading",
        "applies_to": ["Z-PaperDataLoop"],
        "enforced_by": "tests/test_paper_trade_ledger.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/PAPER_TRADE_LEDGER_V10.md",
        "test": "tests/test_paper_trade_ledger.py",
    },
    "outcome_backfill.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure outcome backfill uses local price bars and never writes Z9",
        "owner": "PaperTrading",
        "applies_to": ["Z-PaperDataLoop"],
        "enforced_by": "tests/test_outcome_backfill_runner.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/OUTCOME_BACKFILL_RUNNER_V10.md",
        "test": "tests/test_outcome_backfill_runner.py",
    },
    "backtest.report.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "purpose": "Ensure lightweight backtest produces role-based metrics without trade execution",
        "owner": "Backtest",
        "applies_to": ["Z-PaperDataLoop"],
        "enforced_by": "tests/test_lightweight_backtest.py",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/LIGHTWEIGHT_BACKTEST_V10.md",
        "test": "tests/test_lightweight_backtest.py",
    },
    "event.schema.valid": {
        "layer": "system_control",
        "gate_type": "contract",
        "owner": "SystemCore",
        "purpose": "Validate event schema compliance",
        "applies_to": ["Z-EventStore"],
        "enforced_by": "zmatrix.event_store.validators.validate_event",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/EVENT_SCHEMA_V10.md",
        "test": "tests/test_event_schema.py",
    },
    "event.safety.valid": {
        "layer": "system_control",
        "gate_type": "safety",
        "owner": "SystemCore",
        "purpose": "Ensure event safety fields block real ops",
        "applies_to": ["Z-EventStore"],
        "enforced_by": "zmatrix.event_store.validators.validate_event",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/EVENT_SCHEMA_V10.md",
        "test": "tests/test_event_schema.py",
    },
    "event.lineage.valid": {
        "layer": "system_control",
        "gate_type": "data_contract",
        "owner": "SystemCore",
        "purpose": "Validate event lineage fields (source_event_id / parent_event_id)",
        "applies_to": ["Z-EventStore"],
        "enforced_by": "zmatrix.event_store.validators.validate_event_lineage",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/EVENT_LINEAGE_V10.md",
        "test": "tests/test_event_lineage.py",
    },
    "event.append_only.valid": {
        "layer": "system_control",
        "gate_type": "safety",
        "owner": "SystemCore",
        "purpose": "Enforce append-only write semantics (no overwrite)",
        "applies_to": ["Z-EventStore"],
        "enforced_by": "zmatrix.event_store.store.LocalEventStore.append_event",
        "blocking": True,
        "degradable": False,
        "contract": "docs/contracts/LOCAL_EVENT_STORE_V10.md",
        "test": "tests/test_event_store_local.py",
    },
    "hermes.read_only.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Enforce Hermes memory kernel read-only mode",
        "applies_to": ["Z-HermesMemoryKernel"],
        "enforced_by": "zmatrix.hermes_kernel.validators.validate_hermes_safety",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/HERMES_MEMORY_KERNEL_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
    "hermes.preview_only.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Ensure Hermes outputs are preview-only",
        "applies_to": ["Z-HermesMemoryKernel"],
        "enforced_by": "zmatrix.hermes_kernel.validators.validate_hermes_safety",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/HERMES_MEMORY_KERNEL_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
    "hermes.no_memory_write.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block Hermes memory write from kernel",
        "applies_to": ["Z-HermesMemoryKernel"],
        "enforced_by": "zmatrix.hermes_kernel.validators.validate_hermes_safety",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/HERMES_MEMORY_KERNEL_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
    "hermes.no_auto_calibration.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block auto calibration from Hermes kernel",
        "applies_to": ["Z-HermesMemoryKernel"],
        "enforced_by": "zmatrix.hermes_kernel.validators.validate_hermes_safety",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/HERMES_MEMORY_KERNEL_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
    "hermes.no_prompt_auto_injection.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block prompt auto injection from Hermes kernel",
        "applies_to": ["Z-HermesMemoryKernel"],
        "enforced_by": "zmatrix.hermes_kernel.validators.validate_hermes_safety",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/PROMPT_PATCH_PREVIEW_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
        "prompt.preview_only.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Ensure prompt middleware is preview-only",
        "applies_to": ["Z-PromptMiddlewarePreview"],
        "enforced_by": "zmatrix.prompt_middleware.policy.assert_no_prompt_runtime_effects",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
    "prompt.no_runtime_injection.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block runtime injection from prompt middleware",
        "applies_to": ["Z-PromptMiddlewarePreview"],
        "enforced_by": "zmatrix.prompt_middleware.policy.assert_no_prompt_runtime_effects",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
    "prompt.no_system_prompt_write.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block system_prompt write from prompt middleware",
        "applies_to": ["Z-PromptMiddlewarePreview"],
        "enforced_by": "zmatrix.prompt_middleware.policy.assert_no_prompt_runtime_effects",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
    "prompt.no_auto_injection.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block prompt auto injection from prompt middleware",
        "applies_to": ["Z-PromptMiddlewarePreview"],
        "enforced_by": "zmatrix.prompt_middleware.policy.assert_no_prompt_runtime_effects",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
    "prompt.audit.valid": {
        "layer": "system_control", "gate_type": "contract",
        "owner": "SystemCore", "purpose": "Ensure prompt audit record is valid",
        "applies_to": ["Z-PromptMiddlewarePreview"],
        "enforced_by": "zmatrix.prompt_middleware.policy.validate_prompt_patch_audit",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/PROMPT_PATCH_AUDIT_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
"approval.request.valid": {
        "layer": "system_control", "gate_type": "contract",
        "owner": "SystemCore", "purpose": "Validate approval request structure",
        "applies_to": ["Z-ApprovalReflectionLoop"],
        "enforced_by": "zmatrix.approval_loop.approval_policy.validate_approval_request",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/APPROVAL_REQUEST_V10.md",
        "test": "tests/test_approval_loop_architecture.py",
    },
    "approval.decision.valid": {
        "layer": "system_control", "gate_type": "contract",
        "owner": "SystemCore", "purpose": "Validate approval decision structure",
        "applies_to": ["Z-ApprovalReflectionLoop"],
        "enforced_by": "zmatrix.approval_loop.approval_policy.validate_approval_decision",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/HUMAN_APPROVAL_DECISION_V10.md",
        "test": "tests/test_approval_loop_architecture.py",
    },
    "approval.no_auto_effect.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Block auto effects from approval loop",
        "applies_to": ["Z-ApprovalReflectionLoop"],
        "enforced_by": "zmatrix.approval_loop.approval_policy.assert_no_auto_effects",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_loop_architecture.py",
    },
    "approval.human_required.valid": {
        "layer": "system_control", "gate_type": "safety",
        "owner": "SystemCore", "purpose": "Ensure human approval is required",
        "applies_to": ["Z-ApprovalReflectionLoop"],
        "enforced_by": "zmatrix.approval_loop.approval_policy.assert_no_auto_effects",
        "blocking": True, "degradable": False,
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_loop_architecture.py",
    },
}


def get_gate(gate_id: str) -> dict | None:
    return GATE_REGISTRY.get(gate_id)


def get_gates_for_pipeline(pipeline_id: str) -> list[tuple[str, dict]]:
    return [(gid, g) for gid, g in GATE_REGISTRY.items()
            if pipeline_id in g.get("applies_to", [])]


def check_gate_registry_integrity() -> list[str]:
    violations = []
    for gid, gate in GATE_REGISTRY.items():
        if gate.get("layer") != "system_control":
            violations.append(f"{gid}: layer != system_control")
        if not gate.get("gate_type"):
            violations.append(f"{gid}: missing gate_type")
        if not gate.get("owner"):
            violations.append(f"{gid}: missing owner")
        if not gate.get("applies_to"):
            violations.append(f"{gid}: missing applies_to")
        if not gate.get("enforced_by"):
            violations.append(f"{gid}: missing enforced_by")
        if not gate.get("contract"):
            violations.append(f"{gid}: missing contract")
        if not gate.get("test"):
            violations.append(f"{gid}: missing test")
    return violations


def check_pipeline_required_gates_registered() -> list[str]:
    """检查 PIPELINE_REGISTRY.required_gates 是否全部存在于 GATE_REGISTRY"""
    from zmatrix.architecture.pipeline_registry import PIPELINE_REGISTRY

    missing = []
    for pid, p in PIPELINE_REGISTRY.items():
        for g in p.get("required_gates", []):
            if g not in GATE_REGISTRY:
                missing.append(f"{pid} -> {g}")
    return missing
