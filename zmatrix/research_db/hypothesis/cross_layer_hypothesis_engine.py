"""CrossLayer Hypothesis Engine v1.2 — cross-layer signal → hypothesis only"""
from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
import uuid
from datetime import datetime, timezone


class HypothesisType(str, Enum):
    NARRATIVE_REALITY_DIVERGENCE = "NARRATIVE_REALITY_DIVERGENCE"
    PHYSICAL_PRE_SIGNAL = "PHYSICAL_PRE_SIGNAL"
    CATALYST_CONFIRMED_BY_PROXY = "CATALYST_CONFIRMED_BY_PROXY"
    SELL_ON_NEWS_TRAP = "SELL_ON_NEWS_TRAP"
    EVENT_WITHOUT_MARKET_REACTION = "EVENT_WITHOUT_MARKET_REACTION"
    MARKET_REACTION_WITHOUT_EVENT = "MARKET_REACTION_WITHOUT_EVENT"
    DATA_SOURCE_DEGRADATION_IMPACT = "DATA_SOURCE_DEGRADATION_IMPACT"


@dataclass
class ResearchHypothesis:
    hypothesis_id: str
    hypothesis_type: str = ""
    ticker: str = ""
    involved_layers: list[str] = field(default_factory=list)
    drivers: list[str] = field(default_factory=list)
    confidence: float = 0.0
    severity: str = "LOW"
    explanation: str = ""
    alternative_explanations: list[str] = field(default_factory=list)
    required_followups: list[str] = field(default_factory=list)
    generated_at: str = ""
    verdict_allowed: bool = False
    trade_allowed: bool = False
    production_allowed: bool = False
    human_review_required: bool = True


def generate_hypothesis(
    hypothesis_type: str,
    ticker: str,
    involved_layers: list[str],
    drivers: list[str],
    confidence: float = 0.0,
    severity: str = "LOW",
) -> dict:
    """Generate a structured hypothesis. Never generates verdicts or trade signals."""
    return {
        "hypothesis_id": f"HYPO-{uuid.uuid4().hex[:12]}",
        "hypothesis_type": hypothesis_type,
        "ticker": ticker,
        "involved_layers": involved_layers,
        "drivers": drivers,
        "confidence": min(max(confidence, 0.0), 1.0),
        "severity": severity,
        "explanation": "",
        "alternative_explanations": [],
        "required_followups": [],
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "verdict_allowed": False,
        "trade_allowed": False,
        "production_allowed": False,
        "human_review_required": True,
    }


def detect_sell_on_news_trap(narrative: dict, physical: dict) -> dict | None:
    """Detect potential sell-on-news trap pattern."""
    if not narrative or not physical:
        return None
    return generate_hypothesis(
        HypothesisType.SELL_ON_NEWS_TRAP,
        ticker=narrative.get("ticker", ""),
        involved_layers=["narrative_event", "physical_signal"],
        drivers=["narrative-event", "physical-signal-divergence"],
        confidence=0.3,
        severity="MEDIUM",
    )


def detect_physical_pre_signal(signals: list[dict]) -> list[dict]:
    """Detect physical signals that may precede market moves."""
    results = []
    for sig in signals:
        if sig.get("signal_type", "").startswith("supply"):
            h = generate_hypothesis(
                HypothesisType.PHYSICAL_PRE_SIGNAL,
                ticker=sig.get("ticker", ""),
                involved_layers=["physical_signal"],
                drivers=["supply-chain-signal"],
                confidence=0.25,
                severity="LOW",
            )
            results.append(h)
    return results


def detect_narrative_reality_divergence(narrative_event: dict, reality_check: dict) -> dict | None:
    """Detect divergence between narrative and physical reality."""
    if reality_check.get("verdict") in ("INCONCLUSIVE",):
        return generate_hypothesis(
            HypothesisType.NARRATIVE_REALITY_DIVERGENCE,
            ticker=narrative_event.get("ticker", ""),
            involved_layers=["narrative_event", "reality_check"],
            drivers=["narrative-reality-gap"],
            confidence=0.2,
            severity="LOW",
        )
    return None


def validate_hypothesis(h: dict) -> dict:
    errors = []
    if h.get("verdict_allowed") is True:
        errors.append("verdict_allowed must be false")
    if h.get("trade_allowed") is True:
        errors.append("trade_allowed must be false")
    if h.get("production_allowed") is True:
        errors.append("production_allowed must be false")
    return {"valid": len(errors) == 0, "errors": errors}
