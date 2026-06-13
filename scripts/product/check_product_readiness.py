#!/usr/bin/env python3
"""Check local product readiness for Z-MATRIX-OS V4-PRO."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from zmatrix.product_runtime.local_backend import (
    ProductRuntimeConfig,
    build_agent_bridge_status,
    build_operator_actions,
    build_product_status,
    build_research_status,
)


REPO_ROOT = Path(__file__).resolve().parents[2]
READINESS_PASS = "Z_MATRIX_LOCAL_PRODUCT_READINESS_PASS"
READINESS_BLOCKED = "Z_MATRIX_LOCAL_PRODUCT_READINESS_BLOCKED"


@dataclass(frozen=True)
class ReadinessOptions:
    root: Path = REPO_ROOT
    config: ProductRuntimeConfig = ProductRuntimeConfig()


def build_product_readiness(options: ReadinessOptions = ReadinessOptions()) -> dict[str, Any]:
    root = options.root
    config = options.config
    product = build_product_status(config)
    research = build_research_status(config)
    bridge = build_agent_bridge_status(config)
    actions = build_operator_actions(config)
    checks = [
        _file_check(root, "runbook", "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md"),
        _file_check(root, "cockpit-env", "apps/cockpit_web/.env.example"),
        _file_check(root, "backend-service", "scripts/product/start_backend_service.py"),
        _file_check(root, "local-launcher", "scripts/product/start_local_workstation.sh"),
        _file_check(root, "report-export", "scripts/product/export_research_report_pack.py"),
        _file_check(root, "product-smoke", "scripts/verify_z_matrix_product_smoke.sh"),
        _status_check("product-runtime", product["status"] == "Z_MATRIX_PRODUCT_RUNTIME_READY", product["status"]),
        _status_check("research-status", research["status"] == "Z_MATRIX_RESEARCH_STATUS_READY", research["status"]),
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
            "registered_skills": product["registry"]["skill_count"],
            "research_capabilities": research["capability_count"],
            "ready_research_capabilities": research["ready_count"],
            "agent_intents": len(bridge["allowed_intents"]),
            "operator_actions": len(actions["actions"]),
        },
        "safety": {
            "alpha_claim": "BLOCKED",
            "promotion": "BLOCKED",
            "broker_runtime": "BLOCKED",
            "real_trade": "BLOCKED",
            "agent_direct_mutation": "BLOCKED",
        },
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


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Z-MATRIX local product readiness")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--workspace-id", default="ws_personal_z_prime")
    args = parser.parse_args()
    config = ProductRuntimeConfig(host=args.host, port=args.port, workspace_id=args.workspace_id)
    packet = build_product_readiness(ReadinessOptions(config=config))
    print(json.dumps(packet, ensure_ascii=False, indent=2))
    return 0 if packet["status"] == READINESS_PASS else 1


if __name__ == "__main__":
    raise SystemExit(main())
