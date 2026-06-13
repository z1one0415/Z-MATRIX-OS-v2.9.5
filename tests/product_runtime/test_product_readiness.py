from __future__ import annotations

from pathlib import Path

from scripts.product.check_product_readiness import (
    READINESS_BLOCKED,
    READINESS_PASS,
    ReadinessOptions,
    build_product_readiness,
)
from zmatrix.product_runtime.local_backend import ProductRuntimeConfig


def test_product_readiness_passes_for_minimal_local_workstation(tmp_path: Path):
    root = _make_readiness_root(tmp_path / "repo")
    config = ProductRuntimeConfig(
        public_root=root / "apps/cockpit_web/public/api/cockpit",
        registry_path=root / "data/research_db/agent/registry/skill_registry.generated.json",
        vendor_root=root / "data/research_db/market_data/vendor/tushare_5y",
    )

    packet = build_product_readiness(ReadinessOptions(root=root, config=config))

    assert packet["status"] == READINESS_PASS
    assert packet["blocking_reasons"] == []
    assert packet["summary"]["cockpit_packets"] == 5
    assert packet["summary"]["agent_intents"] >= 4
    assert packet["summary"]["config_templates"] == 2
    assert packet["safety"]["broker_runtime"] == "BLOCKED"
    assert packet["safety"]["real_trade"] == "BLOCKED"


def test_product_readiness_blocks_missing_required_env_template_key(tmp_path: Path):
    root = _make_readiness_root(tmp_path / "repo")
    (root / ".env.example").write_text(
        "Z_MATRIX_PRODUCT_HOST=127.0.0.1\n"
        "Z_MATRIX_PRODUCT_PORT=8765\n",
        encoding="utf-8",
    )
    config = ProductRuntimeConfig(
        public_root=root / "apps/cockpit_web/public/api/cockpit",
        registry_path=root / "data/research_db/agent/registry/skill_registry.generated.json",
        vendor_root=root / "data/research_db/market_data/vendor/tushare_5y",
    )

    packet = build_product_readiness(ReadinessOptions(root=root, config=config))

    assert packet["status"] == READINESS_BLOCKED
    assert "root-env-template" in packet["blocking_reasons"]
    root_check = next(item for item in packet["checks"] if item["id"] == "root-env-template")
    assert "TUSHARE_TOKEN" in root_check["missing_required_keys"]
    assert root_check["value_material"] == "NOT_EMITTED"


def _make_readiness_root(root: Path) -> Path:
    files = {
        "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md": "# runbook\n",
        ".env.example": (
            "Z_MATRIX_PRODUCT_HOST=127.0.0.1\n"
            "Z_MATRIX_PRODUCT_PORT=8765\n"
            "Z_MATRIX_WORKSPACE_ID=ws_personal_z_prime\n"
            "TUSHARE_TOKEN" "=" "\n"
            "DEEPSEEK_API_KEY" "=" "\n"
            "Z_MATRIX_COCKPIT_PUBLIC_ROOT=apps/cockpit_web/public/api/cockpit\n"
            "Z_MATRIX_VENDOR_ROOT=data/research_db/market_data/vendor/tushare_5y\n"
        ),
        "apps/cockpit_web/.env.example": (
            "VITE_ZMATRIX_PRODUCT_STATUS_URL=http://127.0.0.1:8765/api/product/status.json\n"
            "VITE_ZMATRIX_PRODUCT_READINESS_URL=http://127.0.0.1:8765/api/product/readiness.json\n"
            "VITE_ZMATRIX_OPERATOR_ACTIONS_URL=http://127.0.0.1:8765/api/product/operator_actions.json\n"
            "VITE_ZMATRIX_RESEARCH_STATUS_URL=http://127.0.0.1:8765/api/product/research_status.json\n"
            "VITE_ZMATRIX_AGENT_BRIDGE_URL=http://127.0.0.1:8765/api/product/agent_bridge.json\n"
            "VITE_ZMATRIX_AGENT_DRAFT_URL=http://127.0.0.1:8765/api/product/agent_draft.json\n"
            "VITE_ZMATRIX_HOLDINGS_PACKET_URL=/api/cockpit/holdings_packet.json\n"
            "VITE_ZMATRIX_SELECTION_PACKET_URL=/api/cockpit/selection_packet.json\n"
            "VITE_ZMATRIX_HISTORY_PACKET_URL=/api/cockpit/history_packet.json\n"
            "VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL=/api/cockpit/control_compass_packet.json\n"
            "VITE_ZMATRIX_DAYAN_ASK_PACKET_URL=/api/cockpit/dayan_ask_packet.json\n"
        ),
        "scripts/product/start_backend_service.py": "def main():\n    return None\n",
        "scripts/product/start_local_workstation.sh": "#!/usr/bin/env bash\n",
        "scripts/product/export_research_report_pack.py": "def main():\n    return None\n",
        "scripts/verify_z_matrix_product_smoke.sh": "#!/usr/bin/env bash\n",
        "data/research_db/agent/registry/skill_registry.generated.json": (
            '[{"skill_id":"COCKPIT.READ","domain":"COCKPIT","router_ref":"x"},'
            '{"skill_id":"REPORT.READ","domain":"REPORT","router_ref":"y"}]\n'
        ),
        "data/research_db/market_data/vendor/tushare_5y/20260613/manifest.json": "{}\n",
    }
    for name in (
        "holdings_packet.json",
        "selection_packet.json",
        "history_packet.json",
        "control_compass_packet.json",
        "dayan_ask_packet.json",
    ):
        files[f"apps/cockpit_web/public/api/cockpit/{name}"] = "{}\n"
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return root
