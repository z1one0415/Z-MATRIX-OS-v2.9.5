from __future__ import annotations

from pathlib import Path
from typing import Dict, List, Optional

from zmatrix.events.event_store import EventRecord, JsonlEventStore

from .contracts import (
    AlphaValidationPosition,
    HumanValidationDecision,
    MarkToMarketSnapshot,
    SettlementReport,
    ValidationPlan,
    PositionStatus,
)


class AlphaValidationLedger:
    """Append-only alpha validation ledger backed by JsonlEventStore."""

    def __init__(self, store_path: str | Path):
        self.store = JsonlEventStore(store_path)

    def append_plan(self, plan: ValidationPlan) -> ValidationPlan:
        self.store.append(EventRecord(
            event_type="AlphaValidationPlanCreatedEvent",
            payload=plan.to_dict(),
            source_ids=[plan.source_proposal_id] if plan.source_proposal_id else [],
            module_versions=plan.module_versions,
        ))
        return plan

    def append_opened(self, position: AlphaValidationPosition, module_versions: Optional[Dict[str, str]] = None) -> AlphaValidationPosition:
        position.validate()
        self.store.append(EventRecord(
            event_type="AlphaValidationOpenedEvent",
            payload=position.to_dict(),
            source_ids=[position.validation_id, position.paper_trade_id],
            module_versions=module_versions or {},
        ))
        return position

    def append_mark(self, snapshot: MarkToMarketSnapshot, module_versions: Optional[Dict[str, str]] = None) -> MarkToMarketSnapshot:
        self.store.append(EventRecord(
            event_type="AlphaValidationMarkedEvent",
            payload=snapshot.to_dict(),
            source_ids=[snapshot.validation_id],
            module_versions=module_versions or {},
        ))
        return snapshot

    def append_decision(self, decision: HumanValidationDecision, module_versions: Optional[Dict[str, str]] = None) -> HumanValidationDecision:
        decision.validate()
        self.store.append(EventRecord(
            event_type="HumanValidationDecisionEvent",
            payload=decision.to_dict(),
            source_ids=[decision.validation_id] + decision.linked_evidence_ids,
            module_versions=module_versions or {},
        ))
        return decision

    def append_settlement(self, settlement: SettlementReport, module_versions: Optional[Dict[str, str]] = None) -> SettlementReport:
        self.store.append(EventRecord(
            event_type="AlphaValidationSettledEvent",
            payload=settlement.to_dict(),
            source_ids=[settlement.validation_id],
            module_versions=module_versions or {},
        ))
        return settlement

    def list_events(self) -> List[EventRecord]:
        return self.store.list_events()

    def events_for(self, validation_id: str) -> List[EventRecord]:
        return self.store.by_validation_id(validation_id)

    def get_plan(self, validation_id: str) -> ValidationPlan | None:
        for ev in self.events_for(validation_id):
            if ev.event_type == "AlphaValidationPlanCreatedEvent":
                payload = ev.payload
                from .contracts import GhostBenchmark
                gb = GhostBenchmark(**payload["ghost_benchmark"])
                payload = {k:v for k,v in payload.items() if k != "ghost_benchmark"}
                return ValidationPlan(ghost_benchmark=gb, **payload)
        return None

    def get_latest_position(self, validation_id: str) -> AlphaValidationPosition | None:
        latest = None
        for ev in self.events_for(validation_id):
            if ev.event_type == "AlphaValidationOpenedEvent":
                payload = ev.payload
                from .contracts import GhostBenchmark
                gb = GhostBenchmark(**payload["ghost_benchmark"])
                payload = {k:v for k,v in payload.items() if k != "ghost_benchmark"}
                latest = AlphaValidationPosition(ghost_benchmark=gb, **payload)
        return latest

    def latest_mark(self, validation_id: str) -> MarkToMarketSnapshot | None:
        latest = None
        for ev in self.events_for(validation_id):
            if ev.event_type == "AlphaValidationMarkedEvent":
                latest = MarkToMarketSnapshot(**ev.payload)
        return latest
