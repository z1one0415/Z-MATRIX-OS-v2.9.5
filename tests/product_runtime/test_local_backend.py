from __future__ import annotations

import http.client
import json
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

from zmatrix.product_runtime.local_backend import ProductRuntimeConfig, build_product_status, make_handler


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

        conn.request("GET", "/api/cockpit/holdings_packet.json")
        packet_response = conn.getresponse()
        packet = json.loads(packet_response.read().decode("utf-8"))
        assert packet_response.status == 200
        assert packet["name"] == "holdings_packet.json"

        conn.request("OPTIONS", "/api/product/status.json")
        options_response = conn.getresponse()
        options_response.read()
        assert options_response.status == 204
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
