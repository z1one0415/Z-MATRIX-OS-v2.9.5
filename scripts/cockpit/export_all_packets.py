#!/usr/bin/env python3
"""Export all read-only cockpit packets for the frontend shell."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from zmatrix.research_db.cockpit.history_read_model import export_history_packet
from zmatrix.research_db.cockpit.holdings_read_model import (
    SAMPLE_HOLDINGS_SNAPSHOT,
    export_holdings_packet,
)
from zmatrix.research_db.cockpit.selection_read_model import export_selection_packet


def main() -> int:
    parser = argparse.ArgumentParser(description="Export all Z-MATRIX cockpit packets")
    parser.add_argument("--public-root", default="apps/cockpit_web/public/api/cockpit")
    parser.add_argument("--workspace-id", default="ws_personal_z_prime")
    args = parser.parse_args()

    root = Path(args.public_root)
    root.mkdir(parents=True, exist_ok=True)
    packets = {
        "holdings": export_holdings_packet(
            root / "holdings_packet.json",
            workspace_id=args.workspace_id,
            snapshot_path=SAMPLE_HOLDINGS_SNAPSHOT,
        ),
        "selection": export_selection_packet(root / "selection_packet.json", workspace_id=args.workspace_id),
        "history": export_history_packet(root / "history_packet.json", workspace_id=args.workspace_id),
    }
    print(
        json.dumps(
            {
                "status": "COCKPIT_PACKETS_EXPORTED",
                "public_root": str(root),
                "packets": {
                    key: {
                        "workspaceId": packet["workspaceId"],
                        "paperOnly": _paper_only(packet),
                        "brokerRuntime": _broker_runtime(packet),
                        "realTrade": _real_trade(packet),
                    }
                    for key, packet in packets.items()
                },
            },
            ensure_ascii=False,
        )
    )
    return 0


def _paper_only(packet: dict) -> bool:
    return bool(packet.get("audit", packet.get("safety", {})).get("paperOnly"))


def _broker_runtime(packet: dict) -> str:
    return str(packet.get("audit", packet.get("safety", {})).get("brokerRuntime"))


def _real_trade(packet: dict) -> str:
    return str(packet.get("audit", packet.get("safety", {})).get("realTrade"))


if __name__ == "__main__":
    raise SystemExit(main())
