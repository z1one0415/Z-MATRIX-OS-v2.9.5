"""V13.GCORE.2 — Integration Replay: G15→G18→G17→G05 flow.

Validates that all G-Core modules work together for the 双环 5/26 scenario.
"""
import pytest
from zmatrix.research.industry_chain_analyzer import analyze_industry_chain
from zmatrix.prediction.human_risk_engine import evaluate_human_risk
from zmatrix.prediction.human_risk_schema import HumanRiskInput
from zmatrix.prediction.fast_risk_overlay import evaluate_fast_risk_overlay, MarketSnapshot
from zmatrix.daily_memory.memory_card_modules import (
    collect_g17_risk_events, generate_tomorrow_focus
)


class TestIntegrationReplayShuanghuan526:
    """双环 5/26 全链联调"""

    def test_g15_thesis_still_valid(self):
        """G15: 产业链逻辑仍可"""
        result = analyze_industry_chain(
            ticker="002472", name="双环传动", industry="机械设备",
            financials={"has_finance": True, "roe_5y_avg": 12.0, "pe_ttm": 35},
            peers=[], catalysts=[],
            existing_evidence={"A_确证": ["机器人减速器龙头"], "B_佐证": ["环动IPO"]}
        )
        # Chain analysis should give MEDIUM or HIGH thesis
        assert result.g18_handoff["thesis_strength"] in ("MEDIUM", "HIGH")
        assert result.research_confidence in ("MEDIUM", "HIGH")

    def test_g17_risk_orange(self):
        """G17: 天量长上影 → ORANGE"""
        inp = HumanRiskInput(
            ticker="002472",
            close=44.72, high=46.50,
            volume=200_000_000, avg_volume_20d=100_000_000,
            daily_return=-0.01,
            user_cost_line=41.71,
            d1_support=45.00,  # close below support
        )
        result = evaluate_human_risk(inp)
        assert result.risk_level == "ORANGE"
        assert result.paper_track_allowed is False

    def test_g18_fast_risk_overlay_reduces_score(self):
        """G18: fast risk overlay reduces 75 → ≤55"""
        snap = MarketSnapshot(
            close=44.72, high=46.50,
            volume=200_000_000, avg_volume_20d=100_000_000,
        )
        result = evaluate_fast_risk_overlay(snap, base_score=75)
        assert result.final_score <= 55
        assert result.paper_track_allowed is False

    def test_g05_tomorrow_focus_includes_risk(self):
        """G05: tomorrow focus captures G17 risk event"""
        g17_events = {
            "assessments": {
                "002472": {"risk_level": "ORANGE", "triggered_rules": ["R06"], "must_review": True}
            }
        }
        focus = generate_tomorrow_focus(
            g18_decisions={}, g17_events=g17_events, catalysts=[]
        )
        # Should include 002472 in tomorrow's review
        tickers_in_focus = [f["ticker"] for f in focus]
        assert "002472" in tickers_in_focus

    def test_full_chain_coherent(self):
        """Full chain: slow logic OK + fast risk HIGH = WAIT, not PAPER_TRACK"""
        # G15 says thesis is valid (provide evidence for MEDIUM thesis)
        chain = analyze_industry_chain(
            ticker="002472", name="双环传动", industry="机械设备",
            financials={"has_finance": True, "roe_5y_avg": 12.0},
            peers=[], catalysts=[],
            existing_evidence={"A_确证": ["机器人减速器龙头"], "B_佐证": ["环动IPO"]}
        )
        # G17 says dangerous
        risk = evaluate_human_risk(HumanRiskInput(
            ticker="002472", close=44.72, high=46.50,
            volume=200_000_000, avg_volume_20d=100_000_000,
            d1_support=45.00
        ))
        # Coherence: thesis OK but risk elevated = WAIT (not PAPER_TRACK)
        assert chain.g18_handoff["thesis_strength"] in ("MEDIUM", "HIGH")
        assert risk.risk_level in ("ORANGE", "RED")
        assert risk.paper_track_allowed is False
