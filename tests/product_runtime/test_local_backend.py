from __future__ import annotations

import http.client
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from zmatrix.product_runtime.local_backend import (
    ProductRuntimeConfig,
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

    status = build_product_status(ProductRuntimeConfig(public_root=public_root, registry_path=registry_path))

    assert status["status"] == "Z_MATRIX_PRODUCT_RUNTIME_READY"
    assert status["cockpit"]["packet_count"] == 5
    assert status["registry"]["skill_count"] == 2
    assert status["registry"]["domain_count"] == 2
    assert status["safety"]["broker_runtime"] == "BLOCKED"
    assert status["safety"]["real_trade"] == "BLOCKED"


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
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_operator_actions_are_manual_and_block_runtime_paths():
    actions = build_operator_actions()

    assert actions["status"] == "Z_MATRIX_OPERATOR_ACTIONS_READY"
    assert actions["auto_run_enabled"] is False
    assert len(actions["actions"]) >= 5
    for action in actions["actions"]:
        assert action["mode"] == "LOCAL_TERMINAL_MANUAL"
        assert action["safety"]["broker_runtime"] == "BLOCKED"
        assert action["safety"]["real_trade"] == "BLOCKED"


def test_research_status_maps_product_capabilities_to_repository_paths():
    status = build_research_status()

    assert status["capability_count"] >= 8
    assert status["ready_count"] >= 6
    assert {item["id"] for item in status["capabilities"]} >= {"factor-library", "historical-oos", "gatekeeper-audit"}
    assert status["report_export"]["artifact_policy"] == "LOCAL_FILES_ONLY"
    assert status["safety"]["real_trade"] == "BLOCKED"
