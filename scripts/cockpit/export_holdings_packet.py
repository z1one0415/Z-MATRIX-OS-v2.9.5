#!/usr/bin/env python3
"""Export the read-only holdings packet consumed by the cockpit frontend."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from zmatrix.research_db.cockpit.holdings_read_model import (
    DEFAULT_HOLDINGS_PACKET,
    DEFAULT_HOLDINGS_SNAPSHOT,
    export_holdings_packet,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Z-MATRIX cockpit holdings packet")
    parser.add_argument("--snapshot", default=str(DEFAULT_HOLDINGS_SNAPSHOT))
    parser.add_argument("--output", default=str(DEFAULT_HOLDINGS_PACKET))
    parser.add_argument("--workspace-id", default="ws_personal_z_prime")
    args = parser.parse_args()

    packet = export_holdings_packet(
        Path(args.output),
        workspace_id=args.workspace_id,
        snapshot_path=Path(args.snapshot),
    )
    print(
        json.dumps(
            {
                "status": "COCKPIT_HOLDINGS_PACKET_EXPORTED",
                "output": args.output,
                "workspaceId": packet["workspaceId"],
                "position_count": len(packet["positions"]),
                "paperOnly": packet["audit"]["paperOnly"],
                "brokerRuntime": packet["audit"]["brokerRuntime"],
                "realTrade": packet["audit"]["realTrade"],
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
