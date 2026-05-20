from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Iterable, List

from .contracts import (
    AlphaValidationPosition,
    HumanValidationDecision,
    MarkToMarketSnapshot,
    SettlementReport,
    ValidationPlan,
    DecisionType,
)
from .human_pattern import HumanPatternAnalyzer
from .ledger import AlphaValidationLedger
from .llm_coach import LLMCoachDraftBuilder
from .mark_to_market import MarkToMarketEngine
from .paper_adapter import SimplePaperExecutionAdapter
from .policy import AlphaValidationPolicyGuard
from .report_renderer import AlphaValidationReportRenderer
from .settlement import SettlementEngine
from .validation_plan_builder import ValidationPlanBuilder


class AlphaValidationPipeline:
    """Z-G16A Alpha Parallel Validation pipeline.

    Provides a small but complete application service API for OpenClaw/LangGraph:
    create plan -> open paper position -> mark -> human decision -> close/settle -> coach.
    """

    def __init__(self, store_path: str | Path, require_evidence_pack: bool = False):
        self.policy = AlphaValidationPolicyGuard(require_evidence_pack=require_evidence_pack)
        self.builder = ValidationPlanBuilder(policy=self.policy)
        self.ledger = AlphaValidationLedger(store_path)
        self.paper = SimplePaperExecutionAdapter()
        self.marker = MarkToMarketEngine()
        self.settler = SettlementEngine()
        self.patterns = HumanPatternAnalyzer()
        self.coach = LLMCoachDraftBuilder()
        self.renderer = AlphaValidationReportRenderer()

    def create_plan(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        plan = self.builder.from_payload(payload)
        self.ledger.append_plan(plan)
        return {"plan": plan.to_dict(), "report_md": self.renderer.render_plan(plan)}

    def open_position(self, validation_id: str, entry_price: float, benchmark_price: float, quantity: int,
                      opened_at: str, reference_price_for_fill: float | None = None) -> Dict[str, Any]:
        plan = self.ledger.get_plan(validation_id)
        if not plan:
            raise ValueError(f"validation plan not found: {validation_id}")
        self.policy.validate_plan_or_raise(plan)
        fill = self.paper.open_fill(plan.symbol, quantity, reference_price_for_fill or entry_price, side="BUY")
        pos = AlphaValidationPosition(
            validation_id=validation_id,
            symbol=plan.symbol,
            name=plan.name,
            primary_role=plan.primary_role,
            ghost_benchmark=plan.ghost_benchmark,
            entry_price=fill.fill_price if reference_price_for_fill else entry_price,
            entry_benchmark_price=benchmark_price,
            quantity=quantity,
            opened_at=opened_at,
            planned_horizon_days=plan.planned_horizon_days,
            max_acceptable_drawdown=plan.max_acceptable_drawdown,
            human_hypothesis=plan.human_hypothesis,
            paper_trade_id=fill.paper_trade_id,
            fees=fill.fee,
            cost=fill.fill_price * quantity,
            source_proposal_id=plan.source_proposal_id,
            system_verdict_at_entry=plan.system_verdict_at_entry,
        )
        self.ledger.append_opened(pos, module_versions=plan.module_versions)
        return {"position": pos.to_dict(), "paper_fill": fill.to_dict()}

    def mark_to_market(self, validation_id: str, mark_date: str, symbol_price: float, benchmark_price: float,
                       system_verdict: str | None = None) -> Dict[str, Any]:
        pos = self.ledger.get_latest_position(validation_id)
        if not pos:
            raise ValueError(f"position not found: {validation_id}")
        latest_mark = self.ledger.latest_mark(validation_id)
        if latest_mark:
            pos.max_adverse_return = latest_mark.max_adverse_return
            pos.max_favorable_return = latest_mark.max_favorable_return
            pos.marks_count += 1
        mark = self.marker.mark(pos, mark_date, symbol_price, benchmark_price, system_verdict=system_verdict)
        self.ledger.append_mark(mark)
        return {"mark": mark.to_dict(), "report_md": self.renderer.render_mark(mark)}

    def human_decision(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        decision = HumanValidationDecision(
            validation_id=payload["validation_id"],
            decision_type=payload.get("decision_type", DecisionType.HOLD.value),
            system_suggestion=payload.get("system_suggestion", "WATCH"),
            human_decision=payload.get("human_decision", payload.get("decision_type", "HOLD")),
            reason_code=payload.get("reason_code", "manual_review"),
            human_reason=payload.get("human_reason", ""),
            confidence=float(payload.get("confidence", 0.5)),
            acknowledged_risks=payload.get("acknowledged_risks") or [],
            linked_evidence_ids=payload.get("linked_evidence_ids") or [],
        )
        self.ledger.append_decision(decision)
        return {"decision": decision.to_dict()}

    def settle(self, validation_id: str, close_reason: str, exit_price: float, exit_benchmark_price: float,
               closed_at: str, hypothesis_adherence: bool = True, rule_changed_midway: bool = False) -> Dict[str, Any]:
        pos = self.ledger.get_latest_position(validation_id)
        if not pos:
            raise ValueError(f"position not found: {validation_id}")
        latest_mark = self.ledger.latest_mark(validation_id)
        if latest_mark:
            pos.max_adverse_return = latest_mark.max_adverse_return
            pos.max_favorable_return = latest_mark.max_favorable_return
            pos.marks_count = max(pos.marks_count, 1)
        settlement = self.settler.settle(
            pos,
            close_reason=close_reason,
            exit_price=exit_price,
            exit_benchmark_price=exit_benchmark_price,
            closed_at=closed_at,
            hypothesis_adherence=hypothesis_adherence,
            rule_changed_midway=rule_changed_midway,
        )
        self.ledger.append_settlement(settlement)
        return {"settlement": settlement.to_dict(), "report_md": self.renderer.render_settlement(settlement)}

    def settlements(self) -> List[SettlementReport]:
        out: List[SettlementReport] = []
        for ev in self.ledger.store.list_events("AlphaValidationSettledEvent"):
            out.append(SettlementReport(**ev.payload))
        return out

    def coach_report(self, profile_id: str, period: str) -> Dict[str, Any]:
        rows = self.settlements()
        features = self.patterns.analyze_settlements(rows, profile_id=profile_id, window=period)
        report = self.coach.build(profile_id=profile_id, period=period, settlements=rows, features=features)
        return {
            "features": [f.to_dict() for f in features],
            "coach_report": report.to_dict(),
            "report_md": self.renderer.render_coach(report),
        }
