from __future__ import annotations

import json

from zmatrix.research_db.cockpit.holdings_read_model import (
    build_holdings_packet,
    export_holdings_packet,
    load_holdings_snapshot,
)


def test_loads_z_prime_snapshot():
    snapshot = load_holdings_snapshot()
    assert snapshot["workspace_id"] == "ws_personal_z_prime"
    assert snapshot["account"]["total_assets"] == 110249.84
    assert len(snapshot["positions"]) == 3


def test_builds_frontend_compatible_holdings_packet():
    packet = build_holdings_packet()
    assert packet["workspaceId"] == "ws_personal_z_prime"
    assert packet["account"]["accountMask"] == "550***06"
    assert packet["kpi"]["totalAsset"] == 110249.84
    assert packet["positions"][0]["symbol"] == "601899"
    assert packet["positions"][1]["name"] == "双环传动"
    assert packet["positions"][2]["riskTag"] == "正收益观察"
    assert packet["observationWarehouses"][0]["warehouseType"] == "CORE_OBSERVATION"


def test_packet_is_read_only_and_broker_blocked():
    packet = build_holdings_packet()
    audit = packet["audit"]
    assert audit["paperOnly"] is True
    assert audit["humanReview"] is True
    assert audit["brokerRuntime"] == "BLOCKED"
    assert audit["realTrade"] == "BLOCKED"
    assert "production_allowed" not in json.dumps(packet)


def test_missing_snapshot_returns_partial_packet(tmp_path):
    packet = build_holdings_packet(snapshot_path=tmp_path / "missing.json")
    assert packet["kpi"]["dataFreshness"] == "PARTIAL"
    assert packet["positions"] == []
    assert packet["audit"]["realTrade"] == "BLOCKED"


def test_exports_holdings_packet(tmp_path):
    output = tmp_path / "holdings_packet.json"
    packet = export_holdings_packet(output)
    loaded = json.loads(output.read_text(encoding="utf-8"))
    assert loaded["workspaceId"] == packet["workspaceId"]
    assert loaded["positions"][0]["quantity"] == 800
    assert loaded["audit"]["brokerRuntime"] == "BLOCKED"
