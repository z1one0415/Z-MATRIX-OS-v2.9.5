#!/usr/bin/env python3
# allowlist: forbidden-token-definition
"""
☯️ Pipeline Registry v1.0 — Z-MATRIX-OS 三层架构第二层 (Batch F-2)

三层架构:
  Layer 3: System Control (控制器)
  Layer 2: Pipeline Application (管线组合应用层) ← 本注册表
  Layer 1: Shared Skill Module (通用技能层)

原则:
  1. 每条 pipeline 只能在 allowed_skills 中调用技能
  2. allowed_skills 必须全部存在于 SHARED_SKILL_REGISTRY
  3. pipeline 不得私造同类技能模块
  4. forbidden_capabilities 声明 pipeline 禁止的能力
"""
from __future__ import annotations

from typing import Any

PIPELINE_REGISTRY: dict[str, dict[str, Any]] = {
    "Z-G18": {
        "layer": "pipeline_application",
        "pipeline_path": "pipelines/Z-G18_天机引擎/gate_pipeline.py",
        "purpose": "Build G18 paper prediction and full Z9 preview chain",
        "allowed_skills": [
            "r_matrix.evaluate_cycle",
            "evidence.aggregate_upstream",
            "conflict.resolve",
            "decision.finalize",
            "paper.record",
            "z9.sample.build",
            "z9.queue.build",
            "z9.backfill_task.build",
            "z9.calibration_policy.preview",
            "safety.no_real_trade",
            "investment.role_review.build",
        ],
        "required_gates": [
            "safety.no_real_trade",
            "contract.validation",
            "z9.preview_only",
            "investment.role_review.required",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "broker_order",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "G18",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "RC-release": {
        "layer": "pipeline_application",
        "pipeline_path": "scripts/verify_rc_candidate.sh",
        "purpose": "Verify release candidate package and safety boundaries",
        "allowed_skills": [
            "rc.checksum.build",
        ],
        "required_gates": [
            "rc.packaging",
            "rc.verification",
            "safety.boundary_scan",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "RC",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-G09": {
        "layer": "pipeline_application",
        "pipeline_path": "pipelines/Z-G09_全局轮动筛选/gate_pipeline.py",
        "purpose": "R-Matrix cycle four-king rotation scan",
        "allowed_skills": [
            "r_matrix.evaluate_cycle",
        ],
        "required_gates": [
            "r_matrix.cycle_valid",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "R-Matrix",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-G14": {
        "layer": "pipeline_application",
        "pipeline_path": "pipelines/Z-G14_月度全量选股/gate_pipeline.py",
        "purpose": "Monthly full-market sweep with R-Matrix cycle scan",
        "allowed_skills": [
            "r_matrix.evaluate_cycle",
        ],
        "required_gates": [
            "r_matrix.cycle_valid",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "real_z9_write",
            "real_market_fetch",
            "auto_calibration",
        ],
        "owner": "R-Matrix",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-InvestmentRoleReview": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix.investment.investment_role_workflow",
        "purpose": "Run complete B/R/D investment role review before any paper record",
        "allowed_skills": [
            "b_matrix.evaluate_base",
            "r_matrix.evaluate_cycle",
            "d_matrix.evaluate_event",
            "stock_role.classify",
            "account.constitution.check",
            "portfolio.exposure.analyze",
            "pre_trade.checklist.validate",
            "investment.role_review.build",
            "chain_force.evaluate_10x5",
            "sector_stage.detect",
            "financial.health_gate",
            "z8.position_control",
            "g17.manual_veto.preview",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "b_matrix.base_valid",
            "d_matrix.event_valid",
            "stock_role.classification_valid",
            "account.constitution.valid",
            "portfolio.exposure.valid",
            "pre_trade.checklist.complete",
            "chain_force.valid",
            "sector_stage.valid",
            "financial.health_valid",
            "z8.position_control.valid",
            "investment.role_review.required",
            "safety.no_real_trade",
            "human.final_override.required",
        ],
        "forbidden_capabilities": [
            "real_trade", "real_z9_write", "real_market_fetch", "auto_calibration",
            "convert_to_base", "long_hold",
        ],
        "owner": "SystemCore",
        "contract": "docs/architecture/PIPELINE_REGISTRY_V10.md",
        "test": "tests/test_pipeline_registry.py",
    },
    "Z-PaperDataLoop": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix.paper_trading",
        "purpose": "Run paper ledger, local outcome backfill, exposure calculation, lightweight backtest, and monthly review",
        "allowed_skills": [
            "data_facts.load_price_bars",
            "paper_trade.ledger.build",
            "paper_trade.outcome_backfill.calculate",
            "portfolio.exposure.calculate_from_history",
            "backtest.lightweight_role.run",
            "monthly_review.build",
            "safety.no_real_trade",
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
        "owner": "PaperTrading",
        "contract": "docs/architecture/PERSONAL_QUANT_DATA_VALIDITY_LAYER_V10.md",
        "test": "tests/test_lightweight_backtest.py",
    },
    "Z-EventStore": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/event_store/",
        "owner": "EventStore",
        "allowed_skills": [
            "event_store.event.build",
            "event_store.local.append",
            "event_store.local.query",
            "event_store.lineage.trace",
            "event_store.jsonl.export",
            "event_store.paper_event.build",
            "event_store.outcome_event.build",
            "event_store.role_event.build",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "event.schema.valid",
            "event.safety.valid",
            "event.lineage.valid",
            "event.append_only.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade",
            "broker_order",
            "real_z9_write",
            "hermes_memory_write",
            "auto_calibration",
            "prompt_auto_injection",
            "real_market_fetch",
            "external_api_default_on",
        ],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_store_architecture.py",
    },
                                "Z-V32BRDHistoricalStrategyValidation": {"layer":"pipeline_application","pipeline_path":"zmatrix/brd_replay/","owner":"BRDReplay",
        "allowed_skills":["brd_replay.pit_features.build","brd_replay.classifier.run","brd_replay.paper_action.build","brd_replay.outcome.link","brd_replay.metrics.build","brd_replay.report.build","safety.no_real_trade"],
        "required_gates":["brd_replay.point_in_time.valid","brd_replay.paper_only.valid","brd_replay.no_real_trade.valid","brd_replay.no_broker.valid","brd_replay.no_z9.valid","safety.no_real_trade"],
        "forbidden_capabilities":["real_trade","broker_order","auto_buy","auto_sell","auto_position_close","real_z9_write","hermes_memory_write","auto_calibration","prompt_auto_injection","system_prompt_write","runtime_prompt_injection","external_api_default_on"],
        "contract":"docs/contracts/V32_BRD_HISTORICAL_STRATEGY_VALIDATION_V10.md","test":"tests/test_brd_single_day_strategy_replay.py"},
"Z-V31DataReplay": {
        "layer": "pipeline_application", "pipeline_path": "zmatrix/historical_replay/",
        "owner": "DataReplay",
        "allowed_skills": ["replay.brd_adapter.build","replay.universe.build","replay.engine.run","replay.window.run","safety.no_real_trade"],
        "required_gates": ["replay.no_future_data.valid","replay.no_real_trade.valid","replay.no_broker.valid","replay.preview_only.valid","safety.no_real_trade"],
        "forbidden_capabilities": ["real_trade","broker_order","auto_buy","auto_sell","auto_position_close","real_z9_write","hermes_memory_write","auto_calibration","prompt_auto_injection","real_market_fetch","external_api_default_on"],
        "contract": "docs/contracts/REPLAY_ENGINE_V10.md", "test": "tests/test_historical_replay_engine.py",
    },
    "Z-OutcomeBackfill": {
        "layer": "pipeline_application", "pipeline_path": "zmatrix/paper_outcome/",
        "owner": "PaperOutcome",
        "allowed_skills": ["paper_outcome.backfill.run","paper_outcome.policy.validate","event_store.event.build","safety.no_real_trade"],
        "required_gates": ["paper_outcome.schema.valid","paper_outcome.no_real_trade.valid","paper_outcome.no_hermes.valid","safety.no_real_trade"],
        "forbidden_capabilities": ["real_trade","broker_order","auto_sell","auto_position_close","real_z9_write","hermes_memory_write","auto_calibration","prompt_auto_injection","real_market_fetch","external_api_default_on"],
        "contract": "docs/contracts/PAPER_OUTCOME_BACKFILL_V10.md", "test": "tests/test_paper_outcome_backfill_runner.py",
    },
    "Z-PortfolioExposure": {
        "layer": "pipeline_application", "pipeline_path": "zmatrix/portfolio_exposure/",
        "owner": "PortfolioExposure",
        "allowed_skills": ["portfolio.exposure.calc","portfolio.exposure.report","portfolio.exposure.policy.validate","safety.no_real_trade"],
        "required_gates": ["portfolio.exposure.schema.valid","portfolio.exposure.no_auto_sell.valid","portfolio.exposure.no_real_trade.valid","safety.no_real_trade"],
        "forbidden_capabilities": ["real_trade","broker_order","auto_buy","auto_sell","auto_position_close","real_z9_write","hermes_memory_write","auto_calibration","prompt_auto_injection","real_market_fetch","external_api_default_on"],
        "contract": "docs/contracts/PORTFOLIO_EXPOSURE_V10.md", "test": "tests/test_portfolio_exposure_report.py",
    },
"Z-V3AlphaFinalTagGate": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/alpha_tag/",
        "owner": "AlphaTag",
        "allowed_skills": [
            "alpha_tag.artifact_consistency.validate", "alpha_tag.tag_readiness.validate",
            "alpha_tag.release_notes.build", "alpha_rc.rc_gate.validate",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "alpha_tag.artifact_consistency.valid", "alpha_tag.readiness.valid",
            "alpha_tag.no_git_tag_execute.valid", "alpha_tag.no_git_push_tags.valid",
            "alpha_tag.no_runtime.valid", "alpha_tag.no_real_trade.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "auto_buy", "auto_sell",
            "auto_position_close", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "system_prompt_write",
            "runtime_prompt_injection", "real_market_fetch", "external_api_default_on",
            "git_tag_execute", "git_push_tags",
        ],
        "contract": "docs/contracts/V3_ALPHA_TAG_GATE_V10.md",
        "test": "tests/test_alpha_tag_architecture.py",
    },
"Z-V3AlphaRCPackaging": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/alpha_rc/",
        "owner": "AlphaRC",
        "allowed_skills": [
            "alpha_rc.manifest.build", "alpha_rc.verification_matrix.build",
            "alpha_rc.module_inventory.build", "alpha_rc.known_limitations.build",
            "alpha_rc.rc_gate.validate",
            "integration.readiness_report.build", "dry_run.report.build",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "alpha_rc.manifest.valid", "alpha_rc.verification_matrix.valid",
            "alpha_rc.module_inventory.valid", "alpha_rc.known_limitations.valid",
            "alpha_rc.no_runtime.valid", "alpha_rc.no_real_trade.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "auto_buy", "auto_sell",
            "auto_position_close", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "system_prompt_write",
            "runtime_prompt_injection", "real_market_fetch", "external_api_default_on",
        ],
        "contract": "docs/contracts/V3_ALPHA_RC_GATE_VALIDATION_V10.md",
        "test": "tests/test_alpha_rc_architecture.py",
    },
"Z-V3AlphaDryRunRehearsal": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/dry_run/",
        "owner": "DryRun",
        "allowed_skills": [
            "dry_run.rehearsal.build", "dry_run.rehearsal.validate",
            "dry_run.report.build", "integration.readiness_report.build",
            "safety.no_real_trade",
        ],
        "required_gates": [
            "dry_run.only.valid", "dry_run.no_runtime.valid",
            "dry_run.no_real_trade.valid", "dry_run.no_memory_write.valid",
            "dry_run.no_prompt_injection.valid", "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "auto_buy", "auto_sell",
            "auto_position_close", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "system_prompt_write",
            "runtime_prompt_injection", "real_market_fetch", "external_api_default_on",
        ],
        "contract": "docs/contracts/V3_ALPHA_DRY_RUN_REHEARSAL_V10.md",
        "test": "tests/test_v3_alpha_dry_run_architecture.py",
    },
"Z-V3AlphaReadinessGate": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/integration/",
        "owner": "IntegrationGate",
        "allowed_skills": [
            "integration.readiness_map.build", "integration.capability_audit.run",
            "integration.workflow_alignment.audit", "integration.event_chain.sample_build",
            "integration.event_chain.validate", "integration.safety_matrix.build",
            "integration.readiness_report.build", "safety.no_real_trade",
        ],
        "required_gates": [
            "integration.readiness_map.valid", "integration.capability_audit.valid",
            "integration.workflow_alignment.valid", "integration.event_chain.valid",
            "integration.safety_matrix.valid", "integration.no_runtime_enable.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "auto_buy", "auto_sell",
            "auto_position_close", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "system_prompt_write",
            "runtime_prompt_injection", "real_market_fetch", "external_api_default_on",
        ],
        "contract": "docs/contracts/V3_ALPHA_READINESS_REPORT_V10.md",
        "test": "tests/test_v3_alpha_readiness_architecture.py",
    },
"Z-TailRiskAutonomicGates": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/tail_risk/",
        "owner": "TailRisk",
        "allowed_skills": [
            "tail.market_signals.normalize", "tail.limit_down_blackhole.evaluate",
            "tail.domestic_liquidity_crash.evaluate", "tail.hibernate_mode.evaluate",
            "tail.wakeup_probation.evaluate", "tail.d_matrix_freeze.evaluate",
            "tail.risk_isolation.preview", "tail.controller.preview", "tail.policy.validate",
            "tail.controller_event.build", "tail.gate_event.build", "tail.isolation_event.build",
            "event_store.event.build", "safety.no_real_trade",
        ],
        "required_gates": [
            "tail_risk.signal.valid", "tail_risk.preview_only.valid",
            "tail_risk.no_broker_order.valid", "tail_risk.no_real_trade.valid",
            "tail_risk.action_degradation.valid", "tail_risk.no_auto_sell.valid",
            "safety.no_real_trade",
        ],
        "forbidden_capabilities": [
            "real_trade", "broker_order", "auto_buy", "auto_sell",
            "auto_position_close", "real_z9_write", "hermes_memory_write",
            "auto_calibration", "prompt_auto_injection", "real_market_fetch",
            "external_api_default_on",
        ],
        "contract": "docs/contracts/TAIL_RISK_CONTROLLER_V10.md",
        "test": "tests/test_tail_risk_architecture.py",
    },
"Z-PromptMiddlewarePreview": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/prompt_middleware/",
        "owner": "PromptMiddleware",
        "allowed_skills": [
            "prompt.patch_request.build", "prompt.render_preview.build", "prompt.audit.build",
            "prompt.policy.validate_request", "prompt.policy.validate_render", "prompt.policy.validate_audit",
            "prompt.patch_request_event.build", "prompt.render_preview_event.build", "prompt.audit_event.build",
            "event_store.event.build", "safety.no_real_trade",
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
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_architecture.py",
    },
    "Z-ApprovalReflectionLoop": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/approval_loop/",
        "owner": "ApprovalLoop",
        "allowed_skills": [
            "approval.request.build", "approval.decision.build",
            "approval.policy.validate_request", "approval.policy.validate_decision",
            "approval.queue.preview",
            "approval.request_event.build", "approval.human_event.build",
            "event_store.event.build", "safety.no_real_trade",
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
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_loop_architecture.py",
    },
    "Z-HermesMemoryKernel": {
        "layer": "pipeline_application",
        "pipeline_path": "zmatrix/hermes_kernel/ + zmatrix/hermes_memory/",
        "owner": "Hermes",
        "allowed_skills": [
            "hermes.core_memory.load", "hermes.working_context.build",
            "hermes.heuristics.retrieve", "hermes.prompt_patch.preview",
            "hermes.memory_candidate.preview", "hermes.calibration_event.preview",
            "hermes.memory_kernel.preview",
            "hermes.memory_candidate_event.build", "hermes.calibration_event.build",
            "hermes.prompt_patch_event.build",
            "event_store.event.build", "safety.no_real_trade",
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
        "contract": "docs/contracts/HERMES_MEMORY_KERNEL_V10.md",
        "test": "tests/test_hermes_memory_architecture.py",
    },
}


def get_pipeline(pipeline_id: str) -> dict | None:
    return PIPELINE_REGISTRY.get(pipeline_id)


def get_allowed_skills(pipeline_id: str) -> list[str]:
    p = get_pipeline(pipeline_id)
    return list(p["allowed_skills"]) if p else []


def check_pipeline_registry_integrity() -> list[str]:
    """检查 Pipeline Registry 完整性，返回违规列表"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY

    violations = []

    for pid, pipeline in PIPELINE_REGISTRY.items():
        # layer 必须正确
        if pipeline.get("layer") != "pipeline_application":
            violations.append(f"{pid}: layer != pipeline_application")

        # 必须有 pipeline_path
        if not pipeline.get("pipeline_path"):
            violations.append(f"{pid}: missing pipeline_path")

        # 必须有 owner
        if not pipeline.get("owner"):
            violations.append(f"{pid}: missing owner")

        # forbidden_capabilities 必须包含 no-real-ops
        fc = pipeline.get("forbidden_capabilities", [])
        for required in ["real_trade", "real_z9_write", "real_market_fetch", "auto_calibration"]:
            if required not in fc:
                violations.append(f"{pid}: forbidden_capabilities missing {required}")

        # allowed_skills 必须全部存在于 SHARED_SKILL_REGISTRY
        for skill_id in pipeline.get("allowed_skills", []):
            if skill_id not in SHARED_SKILL_REGISTRY:
                violations.append(f"{pid}: allowed_skill '{skill_id}' not in SHARED_SKILL_REGISTRY")

    return violations


def check_pipeline_skills_registered() -> list[str]:
    """返回所有 pipeline 使用的 skill 中未被 SHARED_SKILL_REGISTRY 注册的"""
    from zmatrix.architecture.skill_registry import SHARED_SKILL_REGISTRY

    unregistered = []
    for pid, pipeline in PIPELINE_REGISTRY.items():
        for skill_id in pipeline.get("allowed_skills", []):
            if skill_id not in SHARED_SKILL_REGISTRY:
                unregistered.append(f"{pid} -> {skill_id}")
    return unregistered
