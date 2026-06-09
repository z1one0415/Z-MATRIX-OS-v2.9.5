"""G18 Fast Risk Overlay Replay Tests — V13.G18.3

Proves G18 no longer outputs static 75% / PAPER_TRACK in known failure scenarios.

Test cases:
  1. 双环 5/26: Volume climax + long upper shadow → WAIT, score <= 50
  2. 双环 5/29: Cost line + D1 support + cycle origin break → REDUCE_OR_WAIT, score <= 40
  3. 双环 6/9:  Rebound but prior breakdown not repaired → CONDITIONAL_TRACK or WAIT, score <= 65
  4. 紫金:     -17.4% floating loss + key level break → WAIT or REDUCE, score <= 45

Minimum pass criteria: G18 MUST NOT output 75% / PAPER_TRACK / paper_track_allowed=true
in ANY of the above scenarios.
"""
import pytest
from zmatrix.prediction.fast_risk_overlay import (
    evaluate_fast_risk_overlay,
    MarketSnapshot,
)


class TestShuanghuanMay26:
    """双环 5/26: price=44.72, volume_ratio=2.0, long_upper_shadow=true"""

    def setup_method(self):
        self.snap = MarketSnapshot(
            close=44.72,
            high=46.20,  # (46.20 - 44.72) / 46.20 = 0.032 >= 0.03
            volume=200_000_000,
            avg_volume_20d=100_000_000,  # ratio = 2.0
            user_cost_line=43.00,
            d1_support=43.50,
            cycle_origin=40.00,
        )
        self.result = evaluate_fast_risk_overlay(self.snap, base_score=75)

    def test_paper_track_not_allowed(self):
        assert self.result.paper_track_allowed is False, (
            f"paper_track_allowed should be False, got {self.result.paper_track_allowed}"
        )

    def test_action_is_wait(self):
        assert self.result.recommended_action == "WAIT", (
            f"Expected WAIT, got {self.result.recommended_action}"
        )

    def test_final_score_capped(self):
        assert self.result.final_score <= 50, (
            f"Expected score <= 50, got {self.result.final_score}"
        )

    def test_not_75(self):
        assert self.result.final_score != 75, "Score must NOT be static 75"

    def test_volume_climax_triggered(self):
        assert "R1_VOLUME_CLIMAX" in self.result.triggered_gates

    def test_long_upper_shadow_triggered(self):
        assert "R2_LONG_UPPER_SHADOW" in self.result.triggered_gates


class TestShuanghuanMay29:
    """双环 5/29: price=39.23, cost_line_break + d1_support_break + cycle_origin_break"""

    def setup_method(self):
        self.snap = MarketSnapshot(
            close=39.23,
            high=40.50,
            volume=150_000_000,
            avg_volume_20d=100_000_000,
            user_cost_line=43.00,   # close < cost_line → R3
            d1_support=41.00,       # close < d1_support → R4
            cycle_origin=40.00,     # close < cycle_origin → R5
        )
        self.result = evaluate_fast_risk_overlay(self.snap, base_score=75)

    def test_paper_track_not_allowed(self):
        assert self.result.paper_track_allowed is False

    def test_action_is_reduce_or_wait(self):
        assert self.result.recommended_action in ("REDUCE_OR_WAIT", "AVOID"), (
            f"Expected REDUCE_OR_WAIT or AVOID, got {self.result.recommended_action}"
        )

    def test_final_score_capped_40(self):
        assert self.result.final_score <= 40, (
            f"Expected score <= 40, got {self.result.final_score}"
        )

    def test_not_75(self):
        assert self.result.final_score != 75

    def test_multi_support_break_triggered(self):
        assert "R6_MULTI_SUPPORT_BREAK" in self.result.triggered_gates

    def test_critical_severity(self):
        assert self.result.max_severity == "CRITICAL"


class TestShuanghuanJune9:
    """双环 6/9: price=44.87, rebound but prior breakdown not fully repaired.
    
    Scenario: price rebounded above cycle_origin but still below cost_line,
    and sector rotation has faded. Prior breakdown signals caution.
    """

    def setup_method(self):
        self.snap = MarketSnapshot(
            close=44.87,
            high=45.50,
            volume=120_000_000,
            avg_volume_20d=100_000_000,
            user_cost_line=46.50,   # still below cost line → R3
            d1_support=44.00,       # above d1_support (repaired)
            cycle_origin=40.00,     # above cycle origin (repaired)
            # Sector rotation faded during breakdown
            sector_momentum_rank_current=18,
            sector_momentum_rank_prior=12,  # drop of 6 >= 5 → R8
        )
        self.result = evaluate_fast_risk_overlay(self.snap, base_score=75)

    def test_paper_track_not_allowed(self):
        assert self.result.paper_track_allowed is False, (
            f"paper_track_allowed should be False, got {self.result.paper_track_allowed}"
        )

    def test_action_is_conditional_or_wait(self):
        assert self.result.recommended_action in ("CONDITIONAL_TRACK", "WAIT"), (
            f"Expected CONDITIONAL_TRACK or WAIT, got {self.result.recommended_action}"
        )

    def test_final_score_capped_65(self):
        assert self.result.final_score <= 65, (
            f"Expected score <= 65, got {self.result.final_score}"
        )

    def test_not_75(self):
        assert self.result.final_score != 75

    def test_cost_line_break_triggered(self):
        assert "R3_COST_LINE_BREAK" in self.result.triggered_gates

    def test_sector_rotation_triggered(self):
        assert "R8_SECTOR_ROTATION_FADE" in self.result.triggered_gates


class TestZijin:
    """紫金: price=28.05, floating_loss=-17.4%, key_level_30_break, gold_weakening.
    
    Cost line ~33.95 (implies -17.4% floating loss at 28.05).
    Key level 30 broken. Cycle origin around 25 (gold bull start).
    D1 support at 29.5 broken.
    """

    def setup_method(self):
        self.snap = MarketSnapshot(
            close=28.05,
            high=28.80,
            volume=180_000_000,
            avg_volume_20d=150_000_000,
            user_cost_line=33.95,   # -17.4% floating loss → R3
            d1_support=29.50,       # close < d1_support → R4
            cycle_origin=30.00,     # key level 30 broken → R5
            # Style headwind (gold weakening = style mismatch for resource stocks)
            style_mismatch_duration_days=7,  # >= 5 → R9
        )
        self.result = evaluate_fast_risk_overlay(self.snap, base_score=75)

    def test_paper_track_not_allowed(self):
        assert self.result.paper_track_allowed is False

    def test_action_is_wait_or_reduce(self):
        assert self.result.recommended_action in ("WAIT", "REDUCE_OR_WAIT", "AVOID"), (
            f"Expected WAIT/REDUCE_OR_WAIT/AVOID, got {self.result.recommended_action}"
        )

    def test_final_score_capped_45(self):
        assert self.result.final_score <= 45, (
            f"Expected score <= 45, got {self.result.final_score}"
        )

    def test_not_75(self):
        assert self.result.final_score != 75

    def test_multi_support_break_triggered(self):
        """R3 + R4 + R5 all triggered → R6 CRITICAL"""
        assert "R6_MULTI_SUPPORT_BREAK" in self.result.triggered_gates

    def test_critical_severity(self):
        assert self.result.max_severity == "CRITICAL"


class TestNoRiskGatesBaseCase:
    """Baseline: when no risk gates triggered, G18 should still output 75/PAPER_TRACK."""

    def setup_method(self):
        self.snap = MarketSnapshot(
            close=50.00,
            high=50.50,  # shadow = 0.5/50.5 = 0.0099 < 0.03
            volume=80_000_000,
            avg_volume_20d=100_000_000,  # ratio = 0.8 < 2.0
            user_cost_line=45.00,   # close > cost → no R3
            d1_support=48.00,       # close > support → no R4
            cycle_origin=42.00,     # close > origin → no R5
        )
        self.result = evaluate_fast_risk_overlay(self.snap, base_score=75)

    def test_paper_track_allowed(self):
        assert self.result.paper_track_allowed is True

    def test_action_is_paper_track(self):
        assert self.result.recommended_action == "PAPER_TRACK"

    def test_score_is_75(self):
        assert self.result.final_score == 75

    def test_no_gates_triggered(self):
        assert len(self.result.triggered_gates) == 0
