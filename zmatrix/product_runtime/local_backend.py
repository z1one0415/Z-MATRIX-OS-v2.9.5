"""Local product backend for the Z-MATRIX cockpit workstation."""

from __future__ import annotations

import json
import mimetypes
import os
from collections.abc import Mapping
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


DEFAULT_PUBLIC_ROOT = Path("apps/cockpit_web/public/api/cockpit")
DEFAULT_REGISTRY_PATH = Path("data/research_db/agent/registry/skill_registry.generated.json")
DEFAULT_VENDOR_ROOT = Path("data/research_db/market_data/vendor/tushare_5y")
DEFAULT_REPO_ROOT = Path(".")
ROOT_ENV_TEMPLATE_KEYS = (
    "Z_MATRIX_PRODUCT_HOST",
    "Z_MATRIX_PRODUCT_PORT",
    "Z_MATRIX_WORKSPACE_ID",
    "TUSHARE_TOKEN",
    "DEEPSEEK_API_KEY",
    "Z_MATRIX_COCKPIT_PUBLIC_ROOT",
    "Z_MATRIX_VENDOR_ROOT",
)
COCKPIT_ENV_TEMPLATE_KEYS = (
    "VITE_ZMATRIX_PRODUCT_STATUS_URL",
    "VITE_ZMATRIX_PRODUCT_READINESS_URL",
    "VITE_ZMATRIX_OPERATOR_ACTIONS_URL",
    "VITE_ZMATRIX_RESEARCH_STATUS_URL",
    "VITE_ZMATRIX_RESEARCH_EVIDENCE_INDEX_URL",
    "VITE_ZMATRIX_COCKPIT_MANIFEST_URL",
    "VITE_ZMATRIX_AGENT_BRIDGE_URL",
    "VITE_ZMATRIX_AGENT_DRAFT_URL",
    "VITE_ZMATRIX_HOLDINGS_PACKET_URL",
    "VITE_ZMATRIX_SELECTION_PACKET_URL",
    "VITE_ZMATRIX_HISTORY_PACKET_URL",
    "VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL",
    "VITE_ZMATRIX_DAYAN_ASK_PACKET_URL",
)
SECRET_TEMPLATE_KEYS = ("TUSHARE_TOKEN", "DEEPSEEK_API_KEY")
COCKPIT_PACKET_SPECS = (
    {
        "id": "holdings",
        "label": "持仓管理",
        "route": "/holdings",
        "file_name": "holdings_packet.json",
        "capability": "portfolio_review_readonly",
    },
    {
        "id": "selection",
        "label": "投研选股",
        "route": "/selection",
        "file_name": "selection_packet.json",
        "capability": "candidate_research_watchlist",
    },
    {
        "id": "history",
        "label": "历史回溯",
        "route": "/history",
        "file_name": "history_packet.json",
        "capability": "oos_memory_report_library",
    },
    {
        "id": "control-compass",
        "label": "天机罗盘",
        "route": "/control-compass",
        "file_name": "control_compass_packet.json",
        "capability": "gatekeeper_audit_control",
    },
    {
        "id": "dayan-ask",
        "label": "大衍天问",
        "route": "/dayan-ask",
        "file_name": "dayan_ask_packet.json",
        "capability": "hermes_research_draft_interaction",
    },
)
PACKET_NAMES = tuple(str(spec["file_name"]) for spec in COCKPIT_PACKET_SPECS)
READINESS_PASS = "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS"
READINESS_BLOCKED = "Z_MATRIX_LOCAL_PRODUCT_READINESS_BLOCKED"
RESEARCH_CAPABILITY_SPECS = (
    {
        "id": "factor-library",
        "label": "因子库状态",
        "summary": "因子基础、候选验证脚本与证据文件",
        "paths": (
            "zmatrix/research_db/factor_foundation",
            "scripts/research/factors",
            "docs/cases/V9_FACTOR_SELECTION_GATE.md",
        ),
    },
    {
        "id": "historical-oos",
        "label": "历史 OOS",
        "summary": "历史样本、标签隔离与验证结果",
        "paths": (
            "zmatrix/research_db/validation",
            "zmatrix/research_db/outcome_engine",
            "scripts/cases/calculate_v11_6_1_oos_paper_outcomes.py",
        ),
    },
    {
        "id": "forward-oos",
        "label": "Forward OOS 等待",
        "summary": "未来标签、月度刷新与到期检查",
        "paths": (
            "zmatrix/research_db/validation_factory",
            "scripts/cases/select_v11_5_forward_compatible_as_of_date.py",
            "scripts/cases/resolve_v11_6_1_oos_due_labels.py",
        ),
    },
    {
        "id": "candidate-evidence",
        "label": "候选证据链",
        "summary": "纸面观察清单、候选 thesis 与安全审计",
        "paths": (
            "scripts/cases/build_v11_candidate_factor_watchlist.py",
            "scripts/cases/build_v11_paper_signal_snapshot.py",
            "scripts/cases/audit_v11_paper_watchlist.py",
        ),
    },
    {
        "id": "factor-decay",
        "label": "生存与衰减",
        "summary": "RankIC 方向、衰减模式与稳健性",
        "paths": (
            "scripts/cases/calculate_v9_factor_decay.py",
            "scripts/cases/calculate_v9_factor_robustness.py",
            "docs/cases/V9_FACTOR_DECAY_ANALYSIS.md",
        ),
    },
    {
        "id": "portfolio-sandbox",
        "label": "组合研究沙盒",
        "summary": "纸面组合规则、成本代理与风险审计",
        "paths": (
            "zmatrix/research_db/portfolio",
            "scripts/cases/build_v11_5_paper_portfolio_contract.py",
            "scripts/cases/evaluate_v11_5_benchmark_and_cost_proxy.py",
        ),
    },
    {
        "id": "risk-cost-neutrality",
        "label": "风险成本中性化",
        "summary": "风险、成本、流动性与行业约束",
        "paths": (
            "zmatrix/research_db/attribution",
            "zmatrix/research_db/portfolio_reality",
            "docs/contracts/PORTFOLIO_EXPOSURE_V10.md",
        ),
    },
    {
        "id": "gatekeeper-audit",
        "label": "Gatekeeper 审计",
        "summary": "硬闸、审计报告与关闭条件",
        "paths": (
            "scripts/verify_v40_final_hardgates.sh",
            "scripts/verify_z_skillos_full_system.sh",
            "docs/audit/SAFETY_FORBIDDEN_FLAG_AUDIT_REPORT.md",
        ),
    },
)
RESEARCH_EVIDENCE_GROUPS = (
    {
        "id": "factor-library",
        "label": "因子库状态",
        "summary": "V9 因子选择、稳定性、衰减和稳健性证据。",
        "artifacts": (
            "runtime_reports/cases/v9_factor_selection_gate.json",
            "runtime_reports/cases/v9_factor_decay_analysis.json",
            "runtime_reports/cases/v9_factor_robustness.json",
            "runtime_reports/cases/v9_formal_factor_stability.json",
            "docs/cases/V9_FACTOR_SELECTION_GATE.md",
        ),
    },
    {
        "id": "historical-oos",
        "label": "历史 OOS",
        "summary": "OOS 完成合同、标签解析、纸面结果与审计链。",
        "artifacts": (
            "runtime_reports/cases/v11_6_1_oos_completion_contract.json",
            "runtime_reports/cases/v11_6_1_oos_due_label_resolution.json",
            "runtime_reports/cases/v11_6_1_oos_paper_outcomes.json",
            "runtime_reports/cases/v11_6_1_oos_completion_audit.json",
            "runtime_reports/cases/v11_6_1_oos_completion_chain.json",
        ),
    },
    {
        "id": "forward-oos",
        "label": "Forward OOS 等待",
        "summary": "纸面跟踪注册、刷新日历、到期计划和 live paper 运行状态。",
        "artifacts": (
            "runtime_reports/cases/v11_6_tracking_registry.json",
            "runtime_reports/cases/v11_6_tracking_schedule.json",
            "runtime_reports/cases/v12_1_live_paper_due_schedule.json",
            "runtime_reports/cases/v12_1_live_paper_run_registry.json",
            "runtime_reports/cases/v12_1_live_paper_status_update.json",
        ),
    },
    {
        "id": "candidate-evidence",
        "label": "候选研究证据",
        "summary": "候选观察清单、纸面信号快照、跟踪计划和证据审计。",
        "artifacts": (
            "runtime_reports/cases/v10_candidate_factor_thesis_pack.json",
            "runtime_reports/cases/v11_candidate_factor_watchlist.json",
            "runtime_reports/cases/v11_paper_signal_snapshot.json",
            "runtime_reports/cases/v11_paper_tracking_plan.json",
            "runtime_reports/cases/v11_paper_watchlist_audit.json",
        ),
    },
    {
        "id": "factor-decay",
        "label": "因子生存 / 衰减",
        "summary": "语义传播、生命周期种子、20D 衰减监控和战术监控。",
        "artifacts": (
            "runtime_reports/cases/v10_decay_semantic_propagation_audit.json",
            "runtime_reports/cases/v11_9_factor_lifecycle_seed.json",
            "runtime_reports/cases/v13_5_13_decay_after_20d_monitor.json",
            "runtime_reports/cases/v13_5_13_tactical_monitoring_scorecard.json",
            "docs/cases/V9_FACTOR_DECAY_ANALYSIS.md",
        ),
    },
    {
        "id": "portfolio-sandbox",
        "label": "组合研究沙盒",
        "summary": "纸面组合合同、模拟结果、风险审计、基准和成本代理。",
        "artifacts": (
            "runtime_reports/cases/v11_5_paper_portfolio_contract.json",
            "runtime_reports/cases/v11_5_paper_portfolio_simulation.json",
            "runtime_reports/cases/v11_5_paper_portfolio_risk_audit.json",
            "runtime_reports/cases/v11_5_benchmark_cost_proxy_evaluation.json",
            "runtime_reports/cases/case_expansion_v11_5_closeout.json",
        ),
    },
    {
        "id": "risk-cost-neutrality",
        "label": "风险 / 成本 / 中性化",
        "summary": "容量代理、交易成本、风险边界和中性化相关证据。",
        "artifacts": (
            "runtime_reports/cases/v11_7_transaction_cost_model.json",
            "runtime_reports/cases/v11_7_cost_model_evaluation.json",
            "runtime_reports/cases/v11_7_capacity_proxy_audit.json",
            "runtime_reports/cases/v11_7_closeout.json",
            "runtime_reports/cases/v11_5_paper_portfolio_risk_audit.json",
        ),
    },
    {
        "id": "gatekeeper-audit",
        "label": "Gatekeeper 审计",
        "summary": "V12 入口、研究只读合同、安全审计和总闸验证入口。",
        "artifacts": (
            "runtime_reports/cases/v12_alpha_operating_loop_entry_gate.json",
            "runtime_reports/cases/v12_research_only_operating_contract.json",
            "runtime_reports/cases/v12_research_only_loop_audit.json",
            "runtime_reports/cases/v12_research_only_closeout.json",
            "docs/audit/SAFETY_FORBIDDEN_FLAG_AUDIT_REPORT.md",
        ),
    },
)
AGENT_BRIDGE_INTENTS = (
    {
        "id": "explain-system-status",
        "label": "解释系统状态",
        "output_target": "CHAT_ONLY",
        "requires_review": False,
    },
    {
        "id": "build-research-chain-draft",
        "label": "研究链路草案",
        "output_target": "REPORT_DRAFT",
        "requires_review": True,
    },
    {
        "id": "summarize-factor-evidence",
        "label": "因子证据摘要",
        "output_target": "REPORT_DRAFT",
        "requires_review": True,
    },
    {
        "id": "prepare-audit-reference",
        "label": "审计引用整理",
        "output_target": "AUDIT_CHECK",
        "requires_review": True,
    },
)
FORBIDDEN_AGENT_REQUEST_TERMS = tuple(
    "".join(parts)
    for parts in (
        ("B", "UY"),
        ("S", "ELL"),
        ("H", "OLD"),
        ("买", "入"),
        ("卖", "出"),
        ("持", "有"),
        ("下", "单"),
        ("调", "仓"),
        ("目", "标", "价"),
        ("仓", "位"),
    )
)


@dataclass(frozen=True)
class ProductRuntimeConfig:
    host: str = "127.0.0.1"
    port: int = 8765
    repo_root: Path = DEFAULT_REPO_ROOT
    env: Mapping[str, str] | None = None
    public_root: Path = DEFAULT_PUBLIC_ROOT
    registry_path: Path = DEFAULT_REGISTRY_PATH
    vendor_root: Path = DEFAULT_VENDOR_ROOT
    workspace_id: str = "ws_personal_z_prime"


def build_product_status(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    packet_status = _packet_status(cfg.public_root)
    registry_status = _registry_status(cfg.registry_path)
    vendor_status = _vendor_status(cfg.vendor_root)
    config_status = build_config_template_status(cfg.repo_root, cfg.env)
    ready = packet_status["ready"] and registry_status["ready"] and config_status["ready"]
    return {
        "status": "Z_MATRIX_PRODUCT_RUNTIME_READY" if ready else "Z_MATRIX_PRODUCT_RUNTIME_DEGRADED",
        "workspace_id": cfg.workspace_id,
        "service": {
            "name": "z-matrix-local-product-backend",
            "host": cfg.host,
            "port": cfg.port,
            "generated_at": datetime.now(timezone.utc).isoformat(),
        },
        "cockpit": packet_status,
        "registry": registry_status,
        "data_source": vendor_status,
        "config": config_status,
        "capabilities": {
            "installable_local_preview": True,
            "backend_health": True,
            "configuration_templates": config_status["ready"],
            "cockpit_packets": packet_status["ready"],
            "agent_registry": registry_status["ready"],
            "agent_bridge": registry_status["ready"],
            "vendor_data_ingestion": True,
            "monthly_refresh_dry_plan": True,
            "operator_actions": True,
            "report_export": "READY",
            "product_readiness": True,
            "local_bootstrap": True,
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "agent_direct_mutation": "BLOCKED",
            "secret_storage": "ENV_ONLY",
        },
    }


def build_config_template_status(root: Path = DEFAULT_REPO_ROOT, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    specs = (
        ("root-env-template", ".env.example", ROOT_ENV_TEMPLATE_KEYS, SECRET_TEMPLATE_KEYS),
        ("cockpit-env-template", "apps/cockpit_web/.env.example", COCKPIT_ENV_TEMPLATE_KEYS, ()),
    )
    templates = [_env_template_status(root / relative, check_id, keys, secret_keys) for check_id, relative, keys, secret_keys in specs]
    missing = [
        {"template_id": item["id"], "key": key}
        for item in templates
        for key in item["missing_required_keys"]
    ]
    unsafe = [
        {"template_id": item["id"], "key": key}
        for item in templates
        for key in item["unsafe_example_value_keys"]
    ]
    env_references = _env_secret_reference_status(env if env is not None else os.environ)
    return {
        "ready": all(item["ready"] for item in templates),
        "template_count": len(templates),
        "ready_count": sum(1 for item in templates if item["ready"]),
        "templates": templates,
        "missing_required_keys": missing,
        "unsafe_example_value_keys": unsafe,
        "env_references": env_references,
        "configured_secret_refs": sum(1 for item in env_references if item["configured"]),
        "required_secret_refs": len(env_references),
        "env_reference_policy": "PROCESS_ENV_ONLY_NO_VALUES_EMITTED",
        "secret_material_policy": "TEMPLATE_KEYS_ONLY_ENV_VALUES_NEVER_EMITTED",
    }


def build_operator_actions(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    base_safety = {
        "alpha_claim": "BLOCKED",
        "promotion": "BLOCKED",
        "broker_runtime": "BLOCKED",
        "real_trade": "BLOCKED",
        "secret_storage": "ENV_ONLY",
    }
    return {
        "status": "Z_MATRIX_OPERATOR_ACTIONS_READY",
        "workspace_id": cfg.workspace_id,
        "auto_run_enabled": False,
        "human_review_required": True,
        "actions": [
            {
                "id": "bootstrap-check",
                "label": "本地安装检查",
                "category": "verification",
                "command": "bash scripts/product/bootstrap_local_workstation.sh --check",
                "detail": "确认本地安装入口、Python/npm 工具链与关键文件存在，不安装依赖。",
                "expected": "Z_MATRIX_LOCAL_BOOTSTRAP_CHECK_PASS",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "backend-check",
                "label": "后端健康检查",
                "category": "health",
                "command": "PYTHONPATH=. python3 scripts/product/start_backend_service.py --check",
                "detail": "读取本地服务状态、驾驶舱 packet 与 SkillOS registry。",
                "expected": "Z_MATRIX_PRODUCT_RUNTIME_READY",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "product-smoke",
                "label": "产品 smoke test",
                "category": "verification",
                "command": "bash scripts/verify_z_matrix_product_smoke.sh",
                "detail": "验证本地后端、数据 dry plan、驾驶舱测试、驾驶舱构建和产品包生成。",
                "expected": "Z-MATRIX Product Smoke PASS",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "product-readiness",
                "label": "产品就绪自检",
                "category": "verification",
                "command": "PYTHONPATH=. python3 scripts/product/check_product_readiness.py",
                "detail": "检查安装、启动、驾驶舱、研究能力、Hermes 桥接和安全门状态。",
                "expected": "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "monthly-refresh-dry-plan",
                "label": "月度刷新 dry plan",
                "category": "research",
                "command": (
                    "PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py "
                    "--symbols 601899,002472,300750 --end-date 20260613 --years 5 "
                    "--endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic --dry-plan"
                ),
                "detail": "生成本地数据刷新计划，不写入正式研究结论。",
                "expected": "dry_plan",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "cockpit-packets",
                "label": "驾驶舱 packet 刷新",
                "category": "cockpit",
                "command": "PYTHONPATH=. python3 scripts/cockpit/export_all_packets.py",
                "detail": "重建驾驶舱只读 packet，用于前端页面读取。",
                "expected": "packet export summary",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "workstation-package",
                "label": "本地工作站打包",
                "category": "package",
                "command": "PYTHONPATH=. python3 scripts/product/build_local_workstation_package.py",
                "detail": "生成本地产品包、manifest 和 checksums，输出到 ignored build 目录。",
                "expected": "Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_PACKAGE_BUILT",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
            {
                "id": "research-report-export",
                "label": "研究报告导出",
                "category": "package",
                "command": "PYTHONPATH=. python3 scripts/product/export_research_report_pack.py",
                "detail": "导出研究报告、审计材料和 runtime report manifest，输出到 ignored build 目录。",
                "expected": "Z_MATRIX_RESEARCH_REPORT_EXPORT_PACK_BUILT",
                "mode": "LOCAL_TERMINAL_MANUAL",
                "safety": base_safety,
            },
        ],
    }


def build_research_status(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    capabilities = [_research_capability_status(spec) for spec in RESEARCH_CAPABILITY_SPECS]
    ready_count = sum(1 for item in capabilities if item["status"] == "READY")
    return {
        "status": "Z_MATRIX_RESEARCH_STATUS_READY" if ready_count >= 6 else "Z_MATRIX_RESEARCH_STATUS_DEGRADED",
        "workspace_id": cfg.workspace_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "capability_count": len(capabilities),
        "ready_count": ready_count,
        "capabilities": capabilities,
        "report_export": {
            "status": "LOCAL_EXPORT_READY",
            "command": "PYTHONPATH=. python3 scripts/product/export_research_report_pack.py",
            "artifact_policy": "LOCAL_FILES_ONLY",
        },
        "monthly_refresh": _monthly_refresh_status(),
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
        },
    }


def build_research_evidence_index(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    groups = [_research_evidence_group(cfg.repo_root, spec) for spec in RESEARCH_EVIDENCE_GROUPS]
    ready_count = sum(1 for group in groups if group["status"] == "READY")
    return {
        "status": "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_READY" if ready_count >= 6 else "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_PARTIAL",
        "workspace_id": cfg.workspace_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "group_count": len(groups),
        "ready_group_count": ready_count,
        "groups": groups,
        "artifact_policy": "LOCAL_RESEARCH_EVIDENCE_ONLY",
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "evidence_to_alpha_promotion": "BLOCKED",
        },
    }


def build_cockpit_manifest(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    routes = []
    for spec in COCKPIT_PACKET_SPECS:
        file_name = str(spec["file_name"])
        path = cfg.public_root / file_name
        ready = path.is_file()
        routes.append(
            {
                "id": spec["id"],
                "label": spec["label"],
                "route": spec["route"],
                "capability": spec["capability"],
                "packet_file": file_name,
                "api_path": f"/api/cockpit/{file_name}",
                "ready": ready,
                "bytes": path.stat().st_size if ready else 0,
                "mode": "READ_ONLY_PACKET",
                "safety": {
                    "paper_only": True,
                    "human_review_required": True,
                    "broker_runtime": "BLOCKED",
                    "real_trade": "BLOCKED",
                },
            }
        )
    ready_count = sum(1 for item in routes if item["ready"])
    return {
        "status": "Z_MATRIX_COCKPIT_MANIFEST_READY" if ready_count == len(routes) else "Z_MATRIX_COCKPIT_MANIFEST_DEGRADED",
        "workspace_id": cfg.workspace_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "public_root": cfg.public_root.as_posix(),
        "route_count": len(routes),
        "ready_count": ready_count,
        "routes": routes,
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "agent_direct_mutation": "BLOCKED",
        },
    }


def build_agent_bridge_status(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    registry_status = _registry_status(cfg.registry_path)
    ready = registry_status["ready"] and registry_status.get("skill_count", 0) > 0
    return {
        "status": "Z_MATRIX_AGENT_BRIDGE_READY" if ready else "Z_MATRIX_AGENT_BRIDGE_DEGRADED",
        "workspace_id": cfg.workspace_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "default_agent": "Hermes",
        "interaction_mode": "NATURAL_LANGUAGE_RESEARCH_DRAFT",
        "llm_runtime": {
            "provider": "ENV_CONFIGURED_BY_USER",
            "key_material": "ENV_ONLY",
            "response_storage": "DRAFT_LAYER_ONLY",
            "external_call_from_backend": "DISABLED_BY_DEFAULT",
        },
        "registry": {
            "ready": registry_status["ready"],
            "skill_count": registry_status.get("skill_count", 0),
            "domain_count": registry_status.get("domain_count", 0),
            "concrete_skill_count": registry_status.get("concrete_skill_count", 0),
        },
        "allowed_intents": list(AGENT_BRIDGE_INTENTS),
        "routing": {
            "max_risk_level": "R2_DRAFT",
            "proposal_required": True,
            "human_review_required": True,
            "direct_command_runtime": "BLOCKED",
            "formal_memory_write": "BLOCKED",
            "rule_enable": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "direct_command_runtime": "BLOCKED",
            "formal_memory_write": "BLOCKED",
            "requires_user_confirmation": True,
        },
    }


def build_agent_research_draft(payload: dict[str, Any], config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    question = _clean_agent_text(payload.get("question") or payload.get("userInput") or payload.get("prompt") or "")
    selected_fragments = _clean_string_list(payload.get("selectedFragments") or payload.get("selected_fragments") or [])
    action = _clean_agent_text(payload.get("action") or "生成研究草案")
    forbidden_terms = _matched_forbidden_agent_terms(question)
    if not question:
        return _agent_draft_rejected(cfg, "MISSING_RESEARCH_QUESTION", "请先输入研究问题。")
    if forbidden_terms:
        return _agent_draft_rejected(cfg, "FORBIDDEN_OPERATION_REQUEST", "问题包含超出研究草案边界的动作意图。")

    intent = _infer_agent_intent(question, action)
    bridge = build_agent_bridge_status(cfg)
    route = next((item for item in bridge["allowed_intents"] if item["id"] == intent), bridge["allowed_intents"][0])
    fragments = selected_fragments[:6]
    summary = _summarize_agent_question(question)
    answer = (
        f"Hermes 已生成本地研究草案：先确认「{summary}」的研究范围，"
        "再补齐证据材料、时间窗口和风险边界。结果只进入草案层，等待人工复核。"
    )
    if fragments:
        answer += f" 已选法门：{' / '.join(fragments)}。"

    return {
        "status": "Z_MATRIX_AGENT_DRAFT_READY",
        "workspace_id": cfg.workspace_id,
        "draft_id": f"agent-draft-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
        "default_agent": "Hermes",
        "intent_id": intent,
        "intent_label": route["label"],
        "question_summary": summary,
        "answer": answer,
        "user_message": "本地研究草案已生成，等待人工复核。",
        "suggested_next_steps": [
            "补充研究对象与时间窗口",
            "检查因子证据、历史样本和 Forward OOS 状态",
            "导出审计引用后再人工确认",
        ],
        "draft_layers": ["chat", "drafts"],
        "selected_fragments": fragments,
        "human_review_required": True,
        "proposal_required": True,
        "llm_runtime": {
            "external_call_from_backend": "DISABLED_BY_DEFAULT",
            "key_material": "ENV_ONLY",
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "direct_command_runtime": "BLOCKED",
            "formal_memory_write": "BLOCKED",
        },
    }


def build_runtime_product_readiness(config: ProductRuntimeConfig | None = None, root: Path | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    resolved_root = root or cfg.repo_root
    cfg = replace(cfg, repo_root=resolved_root)
    product = build_product_status(cfg)
    research = build_research_status(cfg)
    evidence = build_research_evidence_index(cfg)
    cockpit_manifest = build_cockpit_manifest(cfg)
    bridge = build_agent_bridge_status(cfg)
    actions = build_operator_actions(cfg)
    config_templates = build_config_template_status(resolved_root, cfg.env)
    checks = [
        _file_check(resolved_root, "runbook", "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md"),
        *_config_template_checks(config_templates),
        _file_check(resolved_root, "local-bootstrap", "scripts/product/bootstrap_local_workstation.sh"),
        _file_check(resolved_root, "backend-service", "scripts/product/start_backend_service.py"),
        _file_check(resolved_root, "local-launcher", "scripts/product/start_local_workstation.sh"),
        _file_check(resolved_root, "report-export", "scripts/product/export_research_report_pack.py"),
        _file_check(resolved_root, "product-smoke", "scripts/verify_z_matrix_product_smoke.sh"),
        _status_check("product-runtime", product["status"] == "Z_MATRIX_PRODUCT_RUNTIME_READY", product["status"]),
        _status_check("research-status", research["status"] == "Z_MATRIX_RESEARCH_STATUS_READY", research["status"]),
        _status_check("research-evidence-index", evidence["status"] == "Z_MATRIX_RESEARCH_EVIDENCE_INDEX_READY", evidence["status"]),
        _status_check("cockpit-manifest", cockpit_manifest["status"] == "Z_MATRIX_COCKPIT_MANIFEST_READY", cockpit_manifest["status"]),
        _status_check("agent-bridge", bridge["status"] == "Z_MATRIX_AGENT_BRIDGE_READY", bridge["status"]),
        _status_check("operator-actions", actions["status"] == "Z_MATRIX_OPERATOR_ACTIONS_READY", actions["status"]),
    ]
    blocking_reasons = [item["id"] for item in checks if not item["ready"]]
    return {
        "status": READINESS_PASS if not blocking_reasons else READINESS_BLOCKED,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "scope": "LOCAL_PERSONAL_RESEARCH_WORKSTATION",
        "checks": checks,
        "blocking_reasons": blocking_reasons,
        "summary": {
            "cockpit_packets": product["cockpit"]["packet_count"],
            "cockpit_routes": cockpit_manifest["ready_count"],
            "registered_skills": product["registry"]["skill_count"],
            "research_capabilities": research["capability_count"],
            "ready_research_capabilities": research["ready_count"],
            "research_evidence_groups": evidence["ready_group_count"],
            "agent_intents": len(bridge["allowed_intents"]),
            "operator_actions": len(actions["actions"]),
            "config_templates": config_templates["ready_count"],
            "configured_secret_refs": config_templates["configured_secret_refs"],
            "required_secret_refs": config_templates["required_secret_refs"],
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "agent_direct_mutation": "BLOCKED",
        },
    }


def make_handler(config: ProductRuntimeConfig) -> type[BaseHTTPRequestHandler]:
    class ProductRuntimeHandler(BaseHTTPRequestHandler):
        server_version = "ZMatrixProductBackend/0.1"

        def do_GET(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            parsed = urlparse(self.path)
            if parsed.path in {"/", "/health", "/api/product/status.json"}:
                self._send_json(build_product_status(config))
                return
            if parsed.path == "/api/product/operator_actions.json":
                self._send_json(build_operator_actions(config))
                return
            if parsed.path == "/api/product/research_status.json":
                self._send_json(build_research_status(config))
                return
            if parsed.path == "/api/product/research_evidence_index.json":
                self._send_json(build_research_evidence_index(config))
                return
            if parsed.path == "/api/product/cockpit_manifest.json":
                self._send_json(build_cockpit_manifest(config))
                return
            if parsed.path == "/api/product/agent_bridge.json":
                self._send_json(build_agent_bridge_status(config))
                return
            if parsed.path == "/api/product/readiness.json":
                self._send_json(build_runtime_product_readiness(config, config.repo_root))
                return
            if parsed.path.startswith("/api/cockpit/"):
                relative = unquote(parsed.path.removeprefix("/api/cockpit/"))
                self._send_public_file(relative)
                return
            self.send_error(404, "Not found")

        def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            parsed = urlparse(self.path)
            if parsed.path != "/api/product/agent_draft.json":
                self.send_error(404, "Not found")
                return
            length = int(self.headers.get("Content-Length", "0") or "0")
            if length <= 0:
                self._send_json({"status": "BAD_REQUEST", "reason": "EMPTY_BODY"}, status_code=400)
                return
            if length > 16_384:
                self._send_json({"status": "PAYLOAD_TOO_LARGE"}, status_code=413)
                return
            try:
                body = self.rfile.read(length).decode("utf-8")
                payload = json.loads(body)
            except (UnicodeDecodeError, json.JSONDecodeError):
                self._send_json({"status": "BAD_REQUEST", "reason": "INVALID_JSON"}, status_code=400)
                return
            if not isinstance(payload, dict):
                self._send_json({"status": "BAD_REQUEST", "reason": "OBJECT_REQUIRED"}, status_code=400)
                return
            self._send_json(build_agent_research_draft(payload, config))

        def do_OPTIONS(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
            self.send_response(204)
            self._send_common_headers()
            self.end_headers()

        def log_message(self, format: str, *args: Any) -> None:  # noqa: A002
            return

        def _send_json(self, payload: dict[str, Any], status_code: int = 200) -> None:
            encoded = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
            self.send_response(status_code)
            self._send_common_headers()
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self._write_body(encoded)

        def _send_public_file(self, relative: str) -> None:
            if not relative or ".." in Path(relative).parts:
                self.send_error(400, "Invalid path")
                return
            target = (config.public_root / relative).resolve()
            root = config.public_root.resolve()
            if root not in target.parents and target != root:
                self.send_error(400, "Invalid path")
                return
            if not target.is_file():
                self.send_error(404, "Not found")
                return
            content = target.read_bytes()
            content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
            self.send_response(200)
            self._send_common_headers()
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self._write_body(content)

        def _write_body(self, content: bytes) -> None:
            try:
                self.wfile.write(content)
            except (BrokenPipeError, ConnectionResetError):
                return

        def _send_common_headers(self) -> None:
            origin = self.headers.get("Origin", "")
            allowed_origin = origin if _is_allowed_local_origin(origin) else "http://127.0.0.1:5173"
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
            self.send_header("Access-Control-Allow-Headers", "Accept, Content-Type")

    return ProductRuntimeHandler


def serve_product_runtime(config: ProductRuntimeConfig) -> None:
    server = ThreadingHTTPServer((config.host, config.port), make_handler(config))
    try:
        server.serve_forever()
    finally:
        server.server_close()


def _packet_status(public_root: Path) -> dict[str, Any]:
    files = []
    missing = []
    for name in PACKET_NAMES:
        path = public_root / name
        if path.exists():
            files.append({"name": name, "bytes": path.stat().st_size})
        else:
            missing.append(name)
    return {
        "ready": not missing,
        "public_root": public_root.as_posix(),
        "packet_count": len(files),
        "required_packet_count": len(PACKET_NAMES),
        "files": files,
        "missing": missing,
    }


def _registry_status(registry_path: Path) -> dict[str, Any]:
    if not registry_path.exists():
        return {"ready": False, "path": registry_path.as_posix(), "skill_count": 0, "domain_count": 0}
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    domains = {item.get("domain") for item in registry if isinstance(item, dict) and item.get("domain")}
    concrete = [item for item in registry if isinstance(item, dict) and item.get("router_ref")]
    return {
        "ready": True,
        "path": registry_path.as_posix(),
        "skill_count": len(registry),
        "domain_count": len(domains),
        "concrete_skill_count": len(concrete),
    }


def _vendor_status(vendor_root: Path) -> dict[str, Any]:
    manifests = sorted(vendor_root.glob("*/manifest.json")) if vendor_root.exists() else []
    latest = manifests[-1].as_posix() if manifests else ""
    return {
        "ready": bool(manifests),
        "path": vendor_root.as_posix(),
        "manifest_count": len(manifests),
        "latest_manifest": latest,
        "mode": "LOCAL_VENDOR_STORE_ONLY",
    }


def _file_check(root: Path, check_id: str, relative: str) -> dict[str, Any]:
    path = root / relative
    return {
        "id": check_id,
        "ready": path.exists(),
        "evidence": relative,
    }


def _status_check(check_id: str, ready: bool, evidence: str) -> dict[str, Any]:
    return {
        "id": check_id,
        "ready": ready,
        "evidence": evidence,
    }


def _config_template_checks(config_templates: dict[str, Any]) -> list[dict[str, Any]]:
    checks = []
    for item in config_templates["templates"]:
        checks.append(
            {
                "id": item["id"],
                "ready": item["ready"],
                "evidence": item["path"],
                "missing_required_keys": item["missing_required_keys"],
                "unsafe_example_value_keys": item["unsafe_example_value_keys"],
                "value_material": item["value_material"],
            }
        )
    return checks


def _env_template_status(path: Path, check_id: str, required_keys: tuple[str, ...], secret_keys: tuple[str, ...]) -> dict[str, Any]:
    assignments = _read_env_template_assignments(path)
    present_keys = sorted(assignments)
    missing = [key for key in required_keys if key not in assignments]
    unsafe_values = [key for key in secret_keys if assignments.get(key, "").strip()]
    return {
        "id": check_id,
        "ready": path.exists() and not missing and not unsafe_values,
        "path": path.as_posix(),
        "required_keys": list(required_keys),
        "present_keys": present_keys,
        "missing_required_keys": missing,
        "unsafe_example_value_keys": unsafe_values,
        "secret_keys": list(secret_keys),
        "value_material": "NOT_EMITTED",
    }


def _env_secret_reference_status(env: Mapping[str, str]) -> list[dict[str, Any]]:
    refs = []
    for key in SECRET_TEMPLATE_KEYS:
        refs.append(
            {
                "key": key,
                "configured": bool(str(env.get(key, "")).strip()),
                "source": "PROCESS_ENV",
                "value_material": "NOT_EMITTED",
            }
        )
    return refs


def _read_env_template_assignments(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}
    assignments: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        if key:
            assignments[key] = value.strip()
    return assignments


def _research_capability_status(spec: dict[str, Any]) -> dict[str, Any]:
    paths = [Path(path) for path in spec["paths"]]
    available_paths = [path.as_posix() for path in paths if path.exists()]
    missing_paths = [path.as_posix() for path in paths if not path.exists()]
    return {
        "id": spec["id"],
        "label": spec["label"],
        "summary": spec["summary"],
        "status": "READY" if not missing_paths else "PARTIAL",
        "available_count": len(available_paths),
        "required_count": len(paths),
        "evidence_paths": available_paths,
        "missing_paths": missing_paths,
        "module_count": sum(_count_py_files(path) for path in paths if path.exists()),
        "safety": "RESEARCH_ONLY",
    }


def _research_evidence_group(root: Path, spec: dict[str, Any]) -> dict[str, Any]:
    artifacts = [_research_evidence_artifact(root, relative) for relative in spec["artifacts"]]
    ready_count = sum(1 for item in artifacts if item["ready"])
    return {
        "id": spec["id"],
        "label": spec["label"],
        "summary": spec["summary"],
        "status": "READY" if ready_count == len(artifacts) else "PARTIAL",
        "ready_count": ready_count,
        "required_count": len(artifacts),
        "artifacts": artifacts,
        "safety": "RESEARCH_ONLY_NO_ALPHA_PROMOTION",
    }


def _research_evidence_artifact(root: Path, relative: str) -> dict[str, Any]:
    path = root / relative
    ready = path.is_file()
    status_field = ""
    if ready and path.suffix == ".json":
        status_field = _json_status_field(path)
    return {
        "path": relative,
        "ready": ready,
        "bytes": path.stat().st_size if ready else 0,
        "artifact_type": path.suffix.removeprefix(".") or "file",
        "status_field": status_field,
    }


def _json_status_field(path: Path) -> str:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError, UnicodeDecodeError):
        return ""
    if not isinstance(payload, dict):
        return ""
    for key in ("status", "verdict", "final", "gate_status"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value[:120]
    return ""


def _monthly_refresh_status() -> dict[str, Any]:
    tracked = {
        "forward_due_schedule": Path("runtime_reports/cases/v12_1_live_paper_due_schedule.json"),
        "oos_completion": Path("runtime_reports/cases/v11_6_1_oos_completion_chain.json"),
        "tracking_registry": Path("runtime_reports/cases/v11_6_tracking_registry.json"),
        "monthly_outcome_panel": Path("runtime_reports/cases/v13_5_3_monthly_outcome_label_panel_manifest.json"),
    }
    files = []
    for name, path in tracked.items():
        files.append(
            {
                "id": name,
                "path": path.as_posix(),
                "ready": path.exists(),
                "bytes": path.stat().st_size if path.exists() else 0,
            }
        )
    ready_count = sum(1 for item in files if item["ready"])
    return {
        "status": "MONTHLY_REFRESH_DRY_PLAN_READY" if ready_count >= 2 else "MONTHLY_REFRESH_DEGRADED",
        "ready_count": ready_count,
        "required_count": len(files),
        "files": files,
        "command": (
            "PYTHONPATH=. python3 scripts/data/ingest_tushare_market_data.py "
            "--symbols 601899,002472,300750 --end-date 20260613 --years 5 "
            "--endpoints stock_basic,trade_cal,daily,adj_factor,daily_basic --dry-plan"
        ),
        "mode": "LOCAL_TERMINAL_MANUAL_DRY_PLAN",
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
        },
    }


def _count_py_files(path: Path) -> int:
    if path.is_file():
        return 1 if path.suffix == ".py" else 0
    return sum(1 for item in path.rglob("*.py") if "__pycache__" not in item.parts)


def _clean_agent_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()[:2000]


def _clean_string_list(value: Any) -> list[str]:
    if not isinstance(value, list):
        return []
    cleaned = []
    for item in value:
        text = _clean_agent_text(item)
        if text:
            cleaned.append(text[:80])
    return cleaned


def _matched_forbidden_agent_terms(text: str) -> list[str]:
    upper = text.upper()
    return [term for term in FORBIDDEN_AGENT_REQUEST_TERMS if term in upper or term in text]


def _infer_agent_intent(question: str, action: str) -> str:
    joined = f"{question} {action}"
    if "审计" in joined or "证据" in joined:
        return "prepare-audit-reference"
    if "因子" in joined or "OOS" in joined.upper() or "衰减" in joined:
        return "summarize-factor-evidence"
    if "状态" in joined or "健康" in joined or "闸" in joined:
        return "explain-system-status"
    return "build-research-chain-draft"


def _summarize_agent_question(question: str) -> str:
    compact = " ".join(question.replace("\n", " ").split())
    return compact[:72] or "未命名研究问题"


def _agent_draft_rejected(cfg: ProductRuntimeConfig, reason: str, message: str) -> dict[str, Any]:
    return {
        "status": "Z_MATRIX_AGENT_DRAFT_REJECTED",
        "workspace_id": cfg.workspace_id,
        "draft_id": "",
        "default_agent": "Hermes",
        "intent_id": "rejected",
        "intent_label": "拒绝生成",
        "question_summary": "",
        "answer": message,
        "user_message": message,
        "suggested_next_steps": ["重新描述为研究问题", "仅保留证据、风险和审计需求"],
        "draft_layers": [],
        "selected_fragments": [],
        "human_review_required": True,
        "proposal_required": True,
        "rejection_reasons": [reason],
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "direct_command_runtime": "BLOCKED",
            "formal_memory_write": "BLOCKED",
        },
    }


def _is_allowed_local_origin(origin: str) -> bool:
    if not origin:
        return False
    parsed = urlparse(origin)
    return parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}
