#!/usr/bin/env python3
"""
☯️ Shared Skill Registry v1.0 — Z-MATRIX-OS 三层架构收束 (Batch F-1)

所有通用能力必须注册到此表。
所有 pipeline 只能组合调用已注册的 skill module。
禁止重复建设同类技能模块。

原则:
  1. 一个 skill 只有一个 canonical id
  2. used_by 列明所有消费管线
  3. duplicate_allowed 默认为 False
  4. 无任何 skill 可声明 real trade enabled
"""
from __future__ import annotations

from typing import Any

# ── Registry ──

SHARED_SKILL_REGISTRY: dict[str, dict[str, Any]] = {
    "r_matrix.evaluate_cycle": {
        "layer": "shared_skill",
        "module": "zmatrix.scoring.r_matrix.r_matrix_service",
        "public_function": "evaluate_r_matrix_cycle",
        "owner": "R-Matrix",
        "used_by": ["Z-G09", "Z-G14", "Z-G18"],
        "contract": "docs/contracts/R_MATRIX_V2_CONTRACT.md",
        "test": "tests/test_rmatrix_contract_schema.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real market fetch, no auto calibration",
    },
    "evidence.aggregate_upstream": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.upstream_evidence_aggregator",
        "public_function": "build_upstream_evidence",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_UPSTREAM_EVIDENCE_V10.md",
        "test": "tests/test_g18_upstream_evidence_aggregation.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade",
    },
    "conflict.resolve": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.conflict_resolver",
        "public_function": "resolve_upstream_conflicts",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_CONFLICT_RESOLVER_V10.md",
        "test": "tests/test_g18_conflict_resolver.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade",
    },
    "decision.finalize": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.final_decision_envelope",
        "public_function": "build_final_decision",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md",
        "test": "tests/test_g18_final_decision_envelope_v11.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no broker order",
    },
    "paper.record": {
        "layer": "shared_skill",
        "module": "zmatrix.prediction.paper_execution_record",
        "public_function": "build_paper_execution_record",
        "owner": "G18",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/G18_PAPER_EXECUTION_RECORD_V10.md",
        "test": "tests/test_g18_paper_execution_record.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write",
    },
    "z9.sample.build": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_calibration_sample",
        "public_function": "build_z9_calibration_sample",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_CALIBRATION_SAMPLE_V10.md",
        "test": "tests/test_z9_calibration_sample_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write",
    },
    "z9.queue.build": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_ingestion_queue",
        "public_function": "build_z9_ingestion_queue_item",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_INGESTION_QUEUE_V10.md",
        "test": "tests/test_z9_ingestion_queue_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real queue write, no real Z9 write",
    },
    "z9.backfill_task.build": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_outcome_backfill",
        "public_function": "build_z9_outcome_backfill_task",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_OUTCOME_BACKFILL_V10.md",
        "test": "tests/test_z9_outcome_backfill_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real market fetch, no real outcome backfill",
    },
    "z9.calibration_policy.preview": {
        "layer": "shared_skill",
        "module": "zmatrix.calibration.z9_calibration_policy",
        "public_function": "build_calibration_policy_preview",
        "owner": "Z9",
        "used_by": ["Z-G18"],
        "contract": "docs/contracts/Z9_CALIBRATION_POLICY_V10.md",
        "test": "tests/test_z9_calibration_policy_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real EV weight change, no real R-Matrix param change, no real G18 rule change",
    },
    "safety.no_real_trade": {
        "layer": "shared_skill",
        "module": "zmatrix.action.action_contracts",
        "public_function": "assert_no_real_trade",
        "owner": "SystemCore",
        "used_by": ["Z-G18", "Z9-all"],
        "contract": "docs/contracts/G18_FINAL_DECISION_ENVELOPE_V11.md",
        "test": "tests/test_g18_final_decision_envelope_v11.py",
        "duplicate_allowed": False,
        "safety_boundary": "foundational: no real trade — forbids BUY/SELL/AUTO_TRADE/MARKET_ORDER/BROKER_ORDER",
    },
    "rc.checksum.build": {
        "layer": "shared_skill",
        "module": "scripts.build_rc_package_manifest",
        "public_function": "main (CLI)",
        "owner": "RC",
        "used_by": ["RC-release"],
        "contract": "docs/architecture/SHARED_SKILL_REGISTRY_V10.md",
        "test": "tests/test_rc_packaging.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no Z9 write, only SHA256 checksum generation",
    },
    # ── B/R/D Investment Role Control (v2.9.8-dev) ──
    "b_matrix.evaluate_base": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.b_matrix",
        "public_function": "evaluate_b_matrix",
        "owner": "R-Matrix",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/B_MATRIX_V10.md",
        "test": "tests/test_b_matrix_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, financial-health only",
    },
    "d_matrix.evaluate_event": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.d_matrix",
        "public_function": "evaluate_d_matrix",
        "owner": "D-Matrix",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/D_MATRIX_V10.md",
        "test": "tests/test_d_matrix_contract.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, stop_loss_required, cannot_convert_to_base",
    },
    "stock_role.classify": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.stock_role_classifier",
        "public_function": "classify_stock_role",
        "owner": "R-Matrix",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/STOCK_ROLE_CLASSIFIER_V10.md",
        "test": "tests/test_stock_role_classifier.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, D cannot become A",
    },
    "account.constitution.check": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.account_constitution",
        "public_function": "check_account_constitution",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/ACCOUNT_CONSTITUTION_V10.md",
        "test": "tests/test_account_constitution.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, bucket/cash/exposure constraints only",
    },
    "portfolio.exposure.analyze": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.portfolio_exposure",
        "public_function": "analyze_portfolio_exposure",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/PORTFOLIO_EXPOSURE_V10.md",
        "test": "tests/test_portfolio_exposure.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, exposure/correlation analysis only",
    },
    "pre_trade.checklist.validate": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.pre_trade_checklist",
        "public_function": "validate_pre_trade_checklist",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/PRE_TRADE_CHECKLIST_V10.md",
        "test": "tests/test_pre_trade_checklist.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, 8-question validation only",
    },
    "investment.role_review.build": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.investment_role_workflow",
        "public_function": "build_investment_role_review",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/contracts/INVESTMENT_ROLE_WORKFLOW_V10.md",
        "test": "tests/test_investment_role_workflow.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, paper-review only",
    },
    "g17.manual_veto.preview": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.g17_human_veto",
        "public_function": "build_g17_human_veto_preview",
        "owner": "G17",
        "used_by": ["Z-InvestmentRoleReview", "Z-G18"],
        "contract": "docs/contracts/G17_HUMAN_VETO_V10.md",
        "test": "tests/test_g17_human_veto.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, human final veto required, paper-only",
    },
    "chain_force.evaluate_10x5": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.chain_force",
        "public_function": "evaluate_chain_force_10x5",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_chain_force_10x5.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, force analysis only",
    },
    "sector_stage.detect": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.sector_stage",
        "public_function": "detect_sector_stage",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_sector_stage.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, sector stage only",
    },
    "financial.health_gate": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.financial_health_gate",
        "public_function": "check_financial_health",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_financial_health_gate.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, financial health only",
    },
    "z8.position_control": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.z8_position_control",
        "public_function": "evaluate_z8_position_control",
        "owner": "SystemCore",
        "used_by": ["Z-InvestmentRoleReview"],
        "contract": "docs/architecture/BRD_7_LAYER_SELECTION_FILTER_V10.md",
        "test": "tests/test_z8_position_control.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, position limits only",
    },
    "data_facts.load_price_bars": {
        "layer": "shared_skill",
        "module": "zmatrix.data_facts.loaders",
        "public_function": "load_price_bars",
        "owner": "DataFacts",
        "used_by": ["Z-PaperDataLoop"],
        "contract": "docs/contracts/DATA_FACT_LAYER_V10.md",
        "test": "tests/test_data_fact_schemas.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, local CSV only, no external API",
    },
    "paper_trade.ledger.build": {
        "layer": "shared_skill",
        "module": "zmatrix.paper_trading.ledger",
        "public_function": "build_paper_trade_entry",
        "owner": "PaperTrading",
        "used_by": ["Z-PaperDataLoop"],
        "contract": "docs/contracts/PAPER_TRADE_LEDGER_V10.md",
        "test": "tests/test_paper_trade_ledger.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, paper ledger only",
    },
    "paper_trade.outcome_backfill.calculate": {
        "layer": "shared_skill",
        "module": "zmatrix.paper_trading.outcome_backfill_runner",
        "public_function": "calculate_outcome_for_entry",
        "owner": "PaperTrading",
        "used_by": ["Z-PaperDataLoop"],
        "contract": "docs/contracts/OUTCOME_BACKFILL_RUNNER_V10.md",
        "test": "tests/test_outcome_backfill_runner.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, local price bars only",
    },
    "portfolio.exposure.calculate_from_history": {
        "layer": "shared_skill",
        "module": "zmatrix.investment.portfolio_exposure_calculation",
        "public_function": "calculate_exposure_from_price_history",
        "owner": "SystemCore",
        "used_by": ["Z-PaperDataLoop"],
        "contract": "docs/contracts/PORTFOLIO_EXPOSURE_HISTORY_V10.md",
        "test": "tests/test_portfolio_exposure_calculation.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, local history calculation only",
    },
    "backtest.lightweight_role.run": {
        "layer": "shared_skill",
        "module": "zmatrix.backtest.lightweight_backtest",
        "public_function": "run_lightweight_role_backtest",
        "owner": "Backtest",
        "used_by": ["Z-PaperDataLoop"],
        "contract": "docs/contracts/LIGHTWEIGHT_BACKTEST_V10.md",
        "test": "tests/test_lightweight_backtest.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, paper entries only",
    },
    "monthly_review.build": {
        "layer": "shared_skill",
        "module": "zmatrix.paper_trading.monthly_review",
        "public_function": "build_monthly_review",
        "owner": "PaperTrading",
        "used_by": ["Z-PaperDataLoop"],
        "contract": "docs/contracts/MONTHLY_REVIEW_V10.md",
        "test": "tests/test_monthly_review.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, review report only",
    },

    # === EventStore skills (v2.9.11-dev) ===
    "event_store.event.build": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.builders",
        "public_function": "build_event",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_ids.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, no Hermes memory write, local EventStore only",
    },
    "event_store.local.append": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.store",
        "public_function": "LocalEventStore.append_event",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/LOCAL_EVENT_STORE_V10.md",
        "test": "tests/test_event_store_local.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, no Hermes memory write, local EventStore only",
    },
    "event_store.local.query": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.query",
        "public_function": "filter_events_by_type",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_query_export.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, read-only queries",
    },
    "event_store.lineage.trace": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.lineage",
        "public_function": "trace_event_lineage",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_LINEAGE_V10.md",
        "test": "tests/test_event_lineage.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, read-only lineage trace",
    },
    "event_store.jsonl.export": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.exporters",
        "public_function": "export_events_to_jsonl",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_query_export.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, no Hermes memory write, local JSONL export only",
    },
    "event_store.paper_event.build": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.adapters",
        "public_function": "build_paper_ledger_event",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, no Hermes memory write, build only no append",
    },
    "event_store.outcome_event.build": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.adapters",
        "public_function": "build_outcome_backfill_event",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, no Hermes memory write, build only no append",
    },
    "event_store.role_event.build": {
        "layer": "shared_skill",
        "module": "zmatrix.event_store.adapters",
        "public_function": "build_role_classification_event",
        "owner": "EventStore",
        "used_by": ["Z-EventStore"],
        "contract": "docs/contracts/EVENT_STORE_V10.md",
        "test": "tests/test_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no real Z9 write, no Hermes memory write, build only no append",
    },

    # === Hermes Memory Kernel skills (v2.9.12-dev) ===
    "hermes.core_memory.load": {
        "layer": "shared_skill", "module": "zmatrix.hermes_kernel.core_memory",
        "public_function": "build_core_memory_preview", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/CORE_MEMORY_V10.md",
        "test": "tests/test_core_memory.py",
        "duplicate_allowed": False,
        "safety_boundary": "read-only, preview-only, no Hermes memory write, no real trade",
    },
    "hermes.working_context.build": {
        "layer": "shared_skill", "module": "zmatrix.hermes_kernel.working_context",
        "public_function": "build_working_context_from_events", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/WORKING_CONTEXT_V10.md",
        "test": "tests/test_working_context.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no Hermes memory write, no Z9 write, no EventStore write",
    },
    "hermes.heuristics.retrieve": {
        "layer": "shared_skill", "module": "zmatrix.hermes_kernel.retrieval",
        "public_function": "retrieve_relevant_heuristics", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/LEARNED_HEURISTICS_V10.md",
        "test": "tests/test_learned_heuristics.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, no vector DB, no network, no write, no prompt injection",
    },
    "hermes.prompt_patch.preview": {
        "layer": "shared_skill", "module": "zmatrix.hermes_kernel.prompt_patch_preview",
        "public_function": "build_prompt_patch_preview", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/PROMPT_PATCH_PREVIEW_V10.md",
        "test": "tests/test_prompt_patch_preview.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, preview-only, no prompt auto injection, no Hermes memory write, requires human approval",
    },
    "hermes.memory_candidate.preview": {
        "layer": "shared_skill", "module": "zmatrix.hermes_memory.memory_candidate_preview",
        "public_function": "build_memory_candidate_preview", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/MEMORY_CANDIDATE_PREVIEW_V10.md",
        "test": "tests/test_memory_candidate_preview.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, DRAFT only, no Hermes memory write, no auto approval, no auto calibration",
    },
    "hermes.calibration_event.preview": {
        "layer": "shared_skill", "module": "zmatrix.hermes_memory.calibration_event_preview",
        "public_function": "build_calibration_event_preview", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/CALIBRATION_EVENT_PREVIEW_V10.md",
        "test": "tests/test_calibration_event_preview.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, preview-only, no auto apply, no auto calibration, no Hermes memory write",
    },
    "hermes.memory_kernel.preview": {
        "layer": "shared_skill", "module": "zmatrix.hermes_memory.hermes_memory_kernel",
        "public_function": "build_hermes_memory_kernel_preview", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/HERMES_MEMORY_KERNEL_V10.md",
        "test": "tests/test_hermes_memory_kernel.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, read-only preview, no Hermes memory write, no prompt injection, no EventStore append",
    },
    "hermes.memory_candidate_event.build": {
        "layer": "shared_skill", "module": "zmatrix.hermes_memory.event_adapters",
        "public_function": "build_memory_candidate_event", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/MEMORY_CANDIDATE_PREVIEW_V10.md",
        "test": "tests/test_hermes_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, no Hermes memory write, no auto approval",
    },
    "hermes.calibration_event.build": {
        "layer": "shared_skill", "module": "zmatrix.hermes_memory.event_adapters",
        "public_function": "build_calibration_event", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/CALIBRATION_EVENT_PREVIEW_V10.md",
        "test": "tests/test_hermes_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, no auto apply, no auto calibration",
    },
    "hermes.prompt_patch_event.build": {
        "layer": "shared_skill", "module": "zmatrix.hermes_memory.event_adapters",
        "public_function": "build_prompt_patch_event", "owner": "Hermes",
        "used_by": ["Z-HermesMemoryKernel"],
        "contract": "docs/contracts/PROMPT_PATCH_PREVIEW_V10.md",
        "test": "tests/test_hermes_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, no auto injection, requires human approval",
    },

    # === Approval Loop skills (v2.9.13-dev) ===
    "approval.request.build": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.approval_request",
        "public_function": "build_approval_request", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/APPROVAL_REQUEST_V10.md",
        "test": "tests/test_approval_request.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, approval required, no Hermes memory write, no real Z9 write, no auto calibration, no prompt injection",
    },
    "approval.decision.build": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.approval_decision",
        "public_function": "build_human_approval_decision", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/HUMAN_APPROVAL_DECISION_V10.md",
        "test": "tests/test_approval_decision.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, approval required, no Hermes memory write, no real Z9 write, no auto calibration, no prompt injection",
    },
    "approval.policy.validate_request": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.approval_policy",
        "public_function": "validate_approval_request", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_policy.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, validation only, no auto effects, no write",
    },
    "approval.policy.validate_decision": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.approval_policy",
        "public_function": "validate_approval_decision", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_policy.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, validation only, no auto effects, no write",
    },
    "approval.queue.preview": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.approval_queue",
        "public_function": "build_approval_queue_preview", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/APPROVAL_QUEUE_PREVIEW_V10.md",
        "test": "tests/test_approval_queue.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, preview only, no auto process, no write",
    },
    "approval.request_event.build": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.event_adapters",
        "public_function": "build_approval_request_event", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, no write, no auto effects",
    },
    "approval.human_event.build": {
        "layer": "shared_skill", "module": "zmatrix.approval_loop.event_adapters",
        "public_function": "build_human_approval_event", "owner": "ApprovalLoop",
        "used_by": ["Z-ApprovalReflectionLoop"],
        "contract": "docs/contracts/APPROVAL_LOOP_V10.md",
        "test": "tests/test_approval_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, no write, no auto effects",
    },


    # === Prompt Middleware skills (v2.9.14-dev) ===
    "prompt.patch_request.build": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.patch_request",
        "public_function": "build_prompt_patch_request", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_PATCH_REQUEST_V10.md",
        "test": "tests/test_prompt_patch_request.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, preview-only, no runtime injection, no system_prompt write, no auto injection, no Hermes memory write",
    },
    "prompt.render_preview.build": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.renderer",
        "public_function": "render_prompt_patch_preview", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_RENDER_PREVIEW_V10.md",
        "test": "tests/test_prompt_middleware_renderer.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, PREVIEW_ONLY render, no system_prompt write, no runtime injection, no Hermes memory write",
    },
    "prompt.audit.build": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.audit",
        "public_function": "build_prompt_patch_audit_record", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_PATCH_AUDIT_V10.md",
        "test": "tests/test_prompt_patch_audit.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, audit metadata only, no runtime injection, no Hermes memory write",
    },
    "prompt.policy.validate_request": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.policy",
        "public_function": "validate_prompt_patch_request", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_policy.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, validation only, no runtime injection, no system_prompt write, no auto injection",
    },
    "prompt.policy.validate_render": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.policy",
        "public_function": "validate_prompt_render_preview", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_policy.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, validation only, PREVIEW_ONLY, no runtime injection",
    },
    "prompt.policy.validate_audit": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.policy",
        "public_function": "validate_prompt_patch_audit", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_policy.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, audit validation only, no runtime injection, no Hermes memory write",
    },
    "prompt.patch_request_event.build": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.event_adapters",
        "public_function": "build_prompt_patch_request_event", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, no runtime injection, no system_prompt write, no Hermes memory write",
    },
    "prompt.render_preview_event.build": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.event_adapters",
        "public_function": "build_prompt_render_preview_event", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, PREVIEW_ONLY event, no Hermes memory write",
    },
    "prompt.audit_event.build": {
        "layer": "shared_skill", "module": "zmatrix.prompt_middleware.event_adapters",
        "public_function": "build_prompt_patch_audit_event", "owner": "PromptMiddleware",
        "used_by": ["Z-PromptMiddlewarePreview"],
        "contract": "docs/contracts/PROMPT_MIDDLEWARE_V10.md",
        "test": "tests/test_prompt_middleware_event_adapters.py",
        "duplicate_allowed": False,
        "safety_boundary": "no real trade, build only, no append, audit event only, no Hermes memory write",
    },

}


def get_skill(skill_id: str) -> dict | None:
    """按 skill_id 查找注册技能"""
    return SHARED_SKILL_REGISTRY.get(skill_id)


def get_skills_by_owner(owner: str) -> list[dict]:
    """按 owner 查找注册技能"""
    return [s for s in SHARED_SKILL_REGISTRY.values() if s["owner"] == owner]


def get_skills_by_pipeline(pipeline_id: str) -> list[tuple[str, dict]]:
    """按消费管线查找注册技能"""
    return [(sid, s) for sid, s in SHARED_SKILL_REGISTRY.items()
            if pipeline_id in s["used_by"]]


def get_duplicate_allowed_skills() -> list[str]:
    """返回允许重复的技能ID列表（应有0个）"""
    return [sid for sid, s in SHARED_SKILL_REGISTRY.items() if s["duplicate_allowed"]]


def check_registry_integrity() -> list[str]:
    """检查注册表完整性，返回所有违规列表"""
    violations = []

    for sid, skill in SHARED_SKILL_REGISTRY.items():
        # 每个 skill 必须有 owner
        if not skill.get("owner"):
            violations.append(f"{sid}: missing owner")

        # 每个 skill 必须有 module
        if not skill.get("module"):
            violations.append(f"{sid}: missing module")

        # 每个 skill 必须有 contract
        if not skill.get("contract"):
            violations.append(f"{sid}: missing contract")

        # 每个 skill 必须有 test
        if not skill.get("test"):
            violations.append(f"{sid}: missing test")

        # 每个 skill 必须有 safety_boundary
        if not skill.get("safety_boundary"):
            violations.append(f"{sid}: missing safety_boundary")

        # 检查 no real trade 声明, 不允许多个 skill_id 指向同一 module
        # (非强制项，仅记录)

    # R-Matrix 只能有一个 canonical skill id
    r_matrix_skills = [sid for sid in SHARED_SKILL_REGISTRY if sid.startswith("r_matrix")]
    if len(r_matrix_skills) != 1:
        violations.append(f"expected exactly 1 r_matrix skill, got {len(r_matrix_skills)}: {r_matrix_skills}")

    return violations
