from __future__ import annotations

import json
import sys

from scripts.cockpit.export_all_packets import main as export_all_packets_main
from zmatrix.research_db.cockpit.history_read_model import build_history_packet, export_history_packet
from zmatrix.research_db.cockpit.selection_read_model import build_selection_packet, export_selection_packet


def test_selection_packet_uses_v11_watchlist_and_blocks_trade():
    packet = build_selection_packet()
    assert packet["workspaceId"] == "ws_personal_z_prime"
    assert packet["kpis"][0]["label"] == "候选因子"
    assert packet["kpis"][0]["value"] == "16"
    assert packet["audit"]["paperOnly"] is True
    assert packet["audit"]["brokerRuntime"] == "BLOCKED"
    assert packet["audit"]["realTrade"] == "BLOCKED"
    assert packet["candidates"]


def test_history_packet_indexes_runtime_reports_and_blocks_trade():
    packet = build_history_packet()
    assert packet["workspaceId"] == "ws_personal_z_prime"
    assert packet["kpis"][0]["label"] == "累计报告"
    assert int(packet["kpis"][0]["value"].replace(",", "")) > 0
    assert packet["safety"]["paperOnly"] is True
    assert packet["safety"]["brokerRuntime"] == "BLOCKED"
    assert packet["safety"]["realTrade"] == "BLOCKED"
    assert packet["events"]


def test_selection_and_history_export(tmp_path):
    selection_path = tmp_path / "selection_packet.json"
    history_path = tmp_path / "history_packet.json"
    selection = export_selection_packet(selection_path)
    history = export_history_packet(history_path)
    assert json.loads(selection_path.read_text(encoding="utf-8"))["workspaceId"] == selection["workspaceId"]
    assert json.loads(history_path.read_text(encoding="utf-8"))["workspaceId"] == history["workspaceId"]


def test_export_all_packets_script(tmp_path):
    old_argv = sys.argv
    sys.argv = ["export_all_packets.py", "--public-root", str(tmp_path)]
    try:
        assert export_all_packets_main() == 0
    finally:
        sys.argv = old_argv
    for name in ["holdings", "selection", "history"]:
        assert (tmp_path / f"{name}_packet.json").exists()
        payload = json.loads((tmp_path / f"{name}_packet.json").read_text(encoding="utf-8"))
        safety = payload.get("audit", payload.get("safety", {}))
        assert safety["brokerRuntime"] == "BLOCKED"
        assert safety["realTrade"] == "BLOCKED"
