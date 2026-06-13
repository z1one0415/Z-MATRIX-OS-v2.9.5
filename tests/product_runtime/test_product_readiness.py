from __future__ import annotations

from pathlib import Path

from scripts.product.check_product_readiness import READINESS_PASS, ReadinessOptions, build_product_readiness
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
    assert packet["safety"]["broker_runtime"] == "BLOCKED"
    assert packet["safety"]["real_trade"] == "BLOCKED"


def _make_readiness_root(root: Path) -> Path:
    files = {
        "docs/release/Z_MATRIX_OS_V4_PRO_LOCAL_WORKSTATION_RUNBOOK.md": "# runbook\n",
        "apps/cockpit_web/.env.example": "VITE_ZMATRIX_PRODUCT_STATUS_URL=http://127.0.0.1:8765/api/product/status.json\n",
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
