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
            "vendor_data_ingestion": True,
            "monthly_refresh_dry_plan": True,
            "operator_actions": True,
            "report_export": "PLANNED",
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
        ],
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
            if parsed.path.startswith("/api/cockpit/"):
                relative = unquote(parsed.path.removeprefix("/api/cockpit/"))
                self._send_public_file(relative)
                return
            self.send_error(404, "Not found")

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
            self.wfile.write(encoded)

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
            self.wfile.write(content)

        def _send_common_headers(self) -> None:
            origin = self.headers.get("Origin", "")
            allowed_origin = origin if _is_allowed_local_origin(origin) else "http://127.0.0.1:5173"
            self.send_header("Cache-Control", "no-store")
            self.send_header("Access-Control-Allow-Origin", allowed_origin)
            self.send_header("Vary", "Origin")
            self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
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


def _is_allowed_local_origin(origin: str) -> bool:
    if not origin:
        return False
    parsed = urlparse(origin)
    return parsed.scheme == "http" and parsed.hostname in {"127.0.0.1", "localhost"}
