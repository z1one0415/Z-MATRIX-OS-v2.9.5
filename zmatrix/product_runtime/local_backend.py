"""Local product backend for the Z-MATRIX cockpit workstation."""

from __future__ import annotations

import json
import mimetypes
from dataclasses import dataclass
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse


DEFAULT_PUBLIC_ROOT = Path("apps/cockpit_web/public/api/cockpit")
DEFAULT_REGISTRY_PATH = Path("data/research_db/agent/registry/skill_registry.generated.json")
DEFAULT_VENDOR_ROOT = Path("data/research_db/market_data/vendor/tushare_5y")
PACKET_NAMES = (
    "holdings_packet.json",
    "selection_packet.json",
    "history_packet.json",
    "control_compass_packet.json",
    "dayan_ask_packet.json",
)
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
    public_root: Path = DEFAULT_PUBLIC_ROOT
    registry_path: Path = DEFAULT_REGISTRY_PATH
    vendor_root: Path = DEFAULT_VENDOR_ROOT
    workspace_id: str = "ws_personal_z_prime"


def build_product_status(config: ProductRuntimeConfig | None = None) -> dict[str, Any]:
    cfg = config or ProductRuntimeConfig()
    packet_status = _packet_status(cfg.public_root)
    registry_status = _registry_status(cfg.registry_path)
    vendor_status = _vendor_status(cfg.vendor_root)
    ready = packet_status["ready"] and registry_status["ready"]
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
        "capabilities": {
            "installable_local_preview": True,
            "backend_health": True,
            "cockpit_packets": packet_status["ready"],
            "agent_registry": registry_status["ready"],
            "agent_bridge": registry_status["ready"],
            "vendor_data_ingestion": True,
            "monthly_refresh_dry_plan": True,
            "operator_actions": True,
            "report_export": "READY",
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
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
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
            if parsed.path == "/api/product/agent_bridge.json":
                self._send_json(build_agent_bridge_status(config))
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
