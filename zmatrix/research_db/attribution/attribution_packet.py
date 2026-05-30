"""Batch-A: Research Packet — snapshot + audit + markdown + JSON."""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class AttributionPacket:
    packet_id: str; created_at: str; version: str = "v1"
    attribution_count: int = 0; cost_count: int = 0; reason_count: int = 0
    markdown_report: str = ""; json_summary: dict = field(default_factory=dict)
    production_allowed: bool = field(default=False, repr=False)
    def __post_init__(self): self.production_allowed = False

class AttributionPacketBuilder:
    @staticmethod
    def build(packet_id: str, attributions: list, costs: list, reasons: list,
              report_generator) -> AttributionPacket:
        from datetime import datetime, timezone
        p = AttributionPacket(packet_id=packet_id, created_at=datetime.now(timezone.utc).isoformat(),
                              attribution_count=len(attributions), cost_count=len(costs), reason_count=len(reasons))
        p.markdown_report = report_generator.generate_markdown(attributions, costs, reasons)
        p.json_summary = report_generator.generate_json(attributions)
        return p
