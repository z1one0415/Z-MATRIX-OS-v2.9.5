from __future__ import annotations

import http.client
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from zmatrix.product_runtime.local_backend import (
    ProductRuntimeConfig,
    build_agent_bridge_status,
    build_config_template_status,
    build_agent_research_draft,
    build_operator_actions,
    build_product_status,
    build_research_status,
    make_handler,
)


def test_product_status_reports_cockpit_and_registry(tmp_path: Path):
    public_root = tmp_path / "public"
    public_root.mkdir()
    for name in (
        "holdings_packet.json",
        "selection_packet.json",
        "history_packet.json",
        "control_compass_packet.json",
        "dayan_ask_packet.json",
    ):
        (public_root / name).write_text('{"paperOnly": true}\n', encoding="utf-8")
    registry_path = tmp_path / "skill_registry.generated.json"
    registry_path.write_text(
        json.dumps(
            [
                {"skill_id": "COCKPIT.READ", "domain": "COCKPIT", "runtime_adapter": "CONCRETE"},
                {"skill_id": "REPORT.READ", "domain": "REPORT", "runtime_adapter": "FRAMEWORK_ONLY"},
            ]
        ),
        encoding="utf-8",
    )

    status = build_product_status(ProductRuntimeConfig(public_root=public_root, registry_path=registry_path, env={}))

    assert status["status"] == "Z_MATRIX_PRODUCT_RUNTIME_READY"
    assert status["cockpit"]["packet_count"] == 5
    assert status["registry"]["skill_count"] == 2
    assert status["registry"]["domain_count"] == 2
    assert status["capabilities"]["agent_bridge"] is True
    assert status["capabilities"]["configuration_templates"] is True
    assert status["config"]["ready"] is True
    assert status["config"]["secret_material_policy"] == "TEMPLATE_KEYS_ONLY_ENV_VALUES_NEVER_EMITTED"
    assert status["config"]["configured_secret_refs"] == 0
    assert status["safety"]["broker_runtime"] == "BLOCKED"
    assert status["safety"]["real_trade"] == "BLOCKED"


def test_config_template_status_reports_env_references_without_values(tmp_path: Path):
    root = tmp_path / "repo"
    root.mkdir()
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
    cockpit_env = root / "apps/cockpit_web/.env.example"
    cockpit_env.parent.mkdir(parents=True)
    cockpit_env.write_text(
        "VITE_ZMATRIX_PRODUCT_STATUS_URL=http://127.0.0.1:8765/api/product/status.json\n"
        "VITE_ZMATRIX_OPERATOR_ACTIONS_URL=http://127.0.0.1:8765/api/product/operator_actions.json\n"
        "VITE_ZMATRIX_RESEARCH_STATUS_URL=http://127.0.0.1:8765/api/product/research_status.json\n"
        "VITE_ZMATRIX_AGENT_BRIDGE_URL=http://127.0.0.1:8765/api/product/agent_bridge.json\n"
        "VITE_ZMATRIX_AGENT_DRAFT_URL=http://127.0.0.1:8765/api/product/agent_draft.json\n"
        "VITE_ZMATRIX_HOLDINGS_PACKET_URL=/api/cockpit/holdings_packet.json\n"
        "VITE_ZMATRIX_SELECTION_PACKET_URL=/api/cockpit/selection_packet.json\n"
        "VITE_ZMATRIX_HISTORY_PACKET_URL=/api/cockpit/history_packet.json\n"
        "VITE_ZMATRIX_CONTROL_COMPASS_PACKET_URL=/api/cockpit/control_compass_packet.json\n"
        "VITE_ZMATRIX_DAYAN_ASK_PACKET_URL=/api/cockpit/dayan_ask_packet.json\n",
        encoding="utf-8",
    )

    status = build_config_template_status(root, env={("TUSHARE_" + "TOKEN"): "local-secret-value"})

    assert status["ready"] is True
    assert status["configured_secret_refs"] == 1
    ref = next(item for item in status["env_references"] if item["key"] == "TUSHARE_TOKEN")
    assert ref["configured"] is True
    assert ref["value_material"] == "NOT_EMITTED"
    assert "local-secret-value" not in json.dumps(status)


def test_local_backend_serves_health_and_cockpit_packet(tmp_path: Path):
    public_root = tmp_path / "public"
    public_root.mkdir()
    for name in (
        "holdings_packet.json",
        "selection_packet.json",
        "history_packet.json",
        "control_compass_packet.json",
        "dayan_ask_packet.json",
    ):
        (public_root / name).write_text(json.dumps({"name": name}), encoding="utf-8")
    registry_path = tmp_path / "skill_registry.generated.json"
    registry_path.write_text(json.dumps([{"domain": "COCKPIT", "runtime_adapter": "CONCRETE"}]), encoding="utf-8")
    config = ProductRuntimeConfig(public_root=public_root, registry_path=registry_path)

    server = ThreadingHTTPServer(("127.0.0.1", 0), make_handler(config))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        conn = http.client.HTTPConnection("127.0.0.1", server.server_port, timeout=5)
        conn.request("GET", "/health")
        response = conn.getresponse()
        payload = json.loads(response.read().decode("utf-8"))
        assert response.status == 200
        assert payload["status"] == "Z_MATRIX_PRODUCT_RUNTIME_READY"
        assert response.getheader("Access-Control-Allow-Origin") == "http://127.0.0.1:5173"

        conn.request("GET", "/api/product/operator_actions.json", headers={"Origin": "http://127.0.0.1:5174"})
        local_origin_response = conn.getresponse()
        local_origin_response.read()
        assert local_origin_response.status == 200
        assert local_origin_response.getheader("Access-Control-Allow-Origin") == "http://127.0.0.1:5174"

        conn.request("GET", "/api/cockpit/holdings_packet.json")
        packet_response = conn.getresponse()
        packet = json.loads(packet_response.read().decode("utf-8"))
        assert packet_response.status == 200
        assert packet["name"] == "holdings_packet.json"

        conn.request("OPTIONS", "/api/product/status.json")
        options_response = conn.getresponse()
        options_response.read()
        assert options_response.status == 204

        conn.request("GET", "/api/product/operator_actions.json")
        actions_response = conn.getresponse()
        actions = json.loads(actions_response.read().decode("utf-8"))
        assert actions_response.status == 200
        assert actions["auto_run_enabled"] is False
        assert actions["human_review_required"] is True
        assert {item["id"] for item in actions["actions"]} >= {"product-smoke", "workstation-package"}

        conn.request("GET", "/api/product/research_status.json")
        research_response = conn.getresponse()
        research = json.loads(research_response.read().decode("utf-8"))
        assert research_response.status == 200
        assert research["capability_count"] >= 8
        assert research["safety"]["broker_runtime"] == "BLOCKED"

        conn.request("GET", "/api/product/agent_bridge.json")
        bridge_response = conn.getresponse()
        bridge = json.loads(bridge_response.read().decode("utf-8"))
        assert bridge_response.status == 200
        assert bridge["default_agent"] == "Hermes"
        assert bridge["routing"]["human_review_required"] is True
        assert bridge["routing"]["broker_runtime"] == "BLOCKED"

        conn.request(
            "POST",
            "/api/product/agent_draft.json",
            body=json.dumps({"question": "请整理半导体设备国产化的研究证据", "selectedFragments": ["产业洞察阵"]}),
            headers={"Content-Type": "application/json"},
        )
        draft_response = conn.getresponse()
        draft = json.loads(draft_response.read().decode("utf-8"))
        assert draft_response.status == 200
        assert draft["status"] == "Z_MATRIX_AGENT_DRAFT_READY"
        assert draft["default_agent"] == "Hermes"
        assert draft["human_review_required"] is True
        assert draft["safety"]["real_trade"] == "BLOCKED"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_operator_actions_are_manual_and_block_runtime_paths():
    actions = build_operator_actions()

    assert actions["status"] == "Z_MATRIX_OPERATOR_ACTIONS_READY"
    assert actions["auto_run_enabled"] is False
    assert len(actions["actions"]) >= 5
    assert {action["id"] for action in actions["actions"]} >= {"research-report-export"}
    for action in actions["actions"]:
        assert action["mode"] == "LOCAL_TERMINAL_MANUAL"
        assert action["safety"]["broker_runtime"] == "BLOCKED"
        assert action["safety"]["real_trade"] == "BLOCKED"


def test_research_status_maps_product_capabilities_to_repository_paths():
    status = build_research_status()

    assert status["capability_count"] >= 8
    assert status["ready_count"] >= 6
    assert {item["id"] for item in status["capabilities"]} >= {"factor-library", "historical-oos", "gatekeeper-audit"}
    assert status["report_export"]["status"] == "LOCAL_EXPORT_READY"
    assert status["report_export"]["command"].endswith("scripts/product/export_research_report_pack.py")
    assert status["report_export"]["artifact_policy"] == "LOCAL_FILES_ONLY"
    assert status["monthly_refresh"]["mode"] == "LOCAL_TERMINAL_MANUAL_DRY_PLAN"
    assert status["monthly_refresh"]["command"].endswith("--dry-plan")
    assert status["monthly_refresh"]["safety"]["broker_runtime"] == "BLOCKED"
    assert status["safety"]["real_trade"] == "BLOCKED"


def test_agent_bridge_status_is_research_draft_only():
    status = build_agent_bridge_status()

    assert status["default_agent"] == "Hermes"
    assert status["interaction_mode"] == "NATURAL_LANGUAGE_RESEARCH_DRAFT"
    assert status["llm_runtime"]["key_material"] == "ENV_ONLY"
    assert status["llm_runtime"]["external_call_from_backend"] == "DISABLED_BY_DEFAULT"
    assert status["routing"]["max_risk_level"] == "R2_DRAFT"
    assert status["routing"]["proposal_required"] is True
    assert status["routing"]["human_review_required"] is True
    assert status["routing"]["direct_command_runtime"] == "BLOCKED"
    assert status["safety"]["broker_runtime"] == "BLOCKED"
    assert status["safety"]["real_trade"] == "BLOCKED"


def test_agent_research_draft_blocks_operation_intent():
    allowed = build_agent_research_draft({"question": "请整理半导体设备国产化研究证据", "selectedFragments": ["产业洞察阵"]})
    blocked = build_agent_research_draft({"question": "请" + "买" + "入" + "某目标"})

    assert allowed["status"] == "Z_MATRIX_AGENT_DRAFT_READY"
    assert allowed["intent_id"] == "prepare-audit-reference"
    assert allowed["draft_layers"] == ["chat", "drafts"]
    assert allowed["human_review_required"] is True
    assert allowed["safety"]["broker_runtime"] == "BLOCKED"
    assert blocked["status"] == "Z_MATRIX_AGENT_DRAFT_REJECTED"
    assert blocked["rejection_reasons"] == ["FORBIDDEN_OPERATION_REQUEST"]
    assert blocked["safety"]["real_trade"] == "BLOCKED"
