#!/usr/bin/env python3
"""V6-B: Build factor snapshot packet from calculated values."""
import json
from pathlib import Path
W=Path(__file__).resolve().parent.parent.parent
C=W/"runtime_reports"/"cases"
data=json.loads((C/"v6b_price_only_factor_values.json").read_text())
nvals=sum(len(r["factor_values"]) for r in data["records"])
packet={"status":"V6B_FACTOR_SNAPSHOT_PACKET_BUILT","factor_count":data["factor_count"],
    "core_12_cases":data["core_12_cases"],"as_of_date_count":data["as_of_date_count"],
    "factor_records":nvals,"source":"v6b_price_only_factor_values.json",
    "ready_for_alpha_claim":False}
(C/"v6b_factor_snapshot_packet.json").write_text(json.dumps(packet,indent=2,ensure_ascii=False))
print(f"Snapshot packet: {nvals} factor values")
