from __future__ import annotations

import json
from pathlib import Path

from zmatrix.product_runtime.config_env import first_env, first_env_int, load_local_env, merged_env
from zmatrix.product_runtime.local_backend import ProductRuntimeConfig, build_product_status


def test_backend_service_loads_allowed_dotenv_without_shell_execution(tmp_path: Path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "Z_MATRIX_PRODUCT_HOST=127.0.0.9\n"
        "Z_MATRIX_PRODUCT_PORT=9876\n"
        "UNRELATED_KEY=ignored\n"
        "TUSHARE_TOKEN" "=" "local-secret-value\n",
        encoding="utf-8",
    )

    local_env = load_local_env(env_file)
    merged = merged_env(local_env, process_env={"Z_MATRIX_PRODUCT_PORT": "8766"})

    assert local_env["Z_MATRIX_PRODUCT_HOST"] == "127.0.0.9"
    assert "UNRELATED_KEY" not in local_env
    assert first_env(merged, ("Z_MATRIX_PRODUCT_PORT",), "8765") == "8766"
    assert first_env(merged, ("Z_MATRIX_PRODUCT_HOST",), "127.0.0.1") == "127.0.0.9"


def test_backend_product_status_never_emits_dotenv_secret_values(tmp_path: Path):
    env_root = _make_env_template_root(tmp_path / "repo")
    config = ProductRuntimeConfig(repo_root=env_root, env={("TUSHARE_" + "TOKEN"): "local-secret-value"})

    status = build_product_status(config)

    assert status["config"]["configured_secret_refs"] == 1
    assert "local-secret-value" not in json.dumps(status, ensure_ascii=False)
    assert all(item["value_material"] == "NOT_EMITTED" for item in status["config"]["env_references"])


def test_backend_service_falls_back_when_dotenv_port_is_invalid():
    assert first_env_int({"Z_MATRIX_PRODUCT_PORT": "not-a-port"}, ("Z_MATRIX_PRODUCT_PORT",), 8765) == 8765


def _make_env_template_root(root: Path) -> Path:
    (root / "apps/cockpit_web").mkdir(parents=True)
    (root / ".env.example").write_text(
        "Z_MATRIX_PRODUCT_HOST=127.0.0.1\n"
        "Z_MATRIX_PRODUCT_PORT=8765\n"
        "Z_MATRIX_WORKSPACE_ID=ws_personal_z_prime\n"
        "TUSHARE_TOKEN" "=" "\n"
        "DEEPSEEK_API_KEY" "=" "\n"
        "Z_MATRIX_COCKPIT_PUBLIC_ROOT=apps/cockpit_web/public/api/cockpit\n"
        "Z_MATRIX_VENDOR_ROOT=data/research_db/market_data/vendor/tushare_5y\n",
        encoding="utf-8",
    )
    (root / "apps/cockpit_web/.env.example").write_text(
        "VITE_ZMATRIX_PRODUCT_STATUS_URL=http://127.0.0.1:8765/api/product/status.json\n"
        "VITE_ZMATRIX_PRODUCT_READINESS_URL=http://127.0.0.1:8765/api/product/readiness.json\n"
        "VITE_ZMATRIX_OPERATOR_ACTIONS_URL=http://127.0.0.1:8765/api/product/operator_actions.json\n"
        "VITE_ZMATRIX_RESEARCH_STATUS_URL=http://127.0.0.1:8765/api/product/research_status.json\n"
        "VITE_ZMATRIX_RESEARCH_EVIDENCE_INDEX_URL=http://127.0.0.1:8765/api/product/research_evidence_index.json\n"
        "VITE_ZMATRIX_COCKPIT_MANIFEST_URL=http://127.0.0.1:8765/api/product/cockpit_manifest.json\n"
        "VITE_ZMATRIX_AGENT_BRIDGE_URL=http://127.0.0.1:8765/api/product/agent_bridge.json\n"
        "VITE_ZMATRIX_AGENT_DRAFT_URL=http://127.0.0.1:8765/api/product/agent_draft.json\n"
        "VITE_ZMATRIX_HOLDINGS_PACKET_URL=/api/cockpit/holdings_packet.json\n"
        "VITE_ZMATRIX_SELECTION_PACKET_URL=/api/cockpit/selection_packet.json\n"
        "VITE_ZMATRIX_HISTORY_PACKET_URL=/api/cockpit/history_packet.json\n"
        "VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL=/api/cockpit/control_compass_packet.json\n"
        "VITE_ZMATRIX_DAYAN_ASK_PACKET_URL=/api/cockpit/dayan_ask_packet.json\n",
        encoding="utf-8",
    )
    return root
