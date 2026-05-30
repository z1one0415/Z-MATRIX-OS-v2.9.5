"""V2 Engine — Prediction Market competition + Confidence Calibration + Researcher Ranking."""
from __future__ import annotations
import statistics, math
from . import PredictionEntry, CalibrationProfile, ResearcherRank, PredictionMarketResult, PredictionDirection

class PredictionMarketEngine:
    @staticmethod
    def compute_consensus(predictions: list[PredictionEntry]) -> PredictionMarketResult:
        if not predictions: return PredictionMarketResult(market_id="UNKNOWN", ticker="UNKNOWN")
        ticker = predictions[0].ticker
        ups = sum(1 for p in predictions if p.direction == PredictionDirection.UP.value)
        downs = sum(1 for p in predictions if p.direction == PredictionDirection.DOWN.value)
        flats = sum(1 for p in predictions if p.direction == PredictionDirection.FLAT.value)
        total = len(predictions)
        r = PredictionMarketResult(market_id=f"MARKET-{ticker}", ticker=ticker, forecaster_count=total)
        r.agreement_ratio = max(ups, downs, flats) / total if total > 0 else 0
        r.disagreement_index = (ups * downs + flats * max(ups, downs)) / (total * total) if total > 0 else 0
        r.consensus_direction = PredictionDirection.UP.value if ups > max(downs, flats) else (PredictionDirection.DOWN.value if downs > max(ups, flats) else PredictionDirection.FLAT.value)
        r.consensus_magnitude = statistics.mean(p.magnitude_bps for p in predictions) if predictions else 0
        r.contrarian_signals = [p.prediction_id for p in predictions if p.direction != r.consensus_direction]
        return r

class ConfidenceCalibration:
    @staticmethod
    def calibrate(forecaster_id: str, predictions: list[PredictionEntry]) -> CalibrationProfile:
        resolved = [p for p in predictions if p.resolved]
        p = CalibrationProfile(forecaster_id=forecaster_id, total_predictions=len(resolved))
        if not resolved: return p
        p.correct_predictions = sum(1 for r in resolved if r.was_correct)
        p.actual_accuracy = p.correct_predictions / len(resolved)
        p.mean_confidence = statistics.mean(r.confidence for r in resolved)
        p.overconfidence_score = p.mean_confidence - p.actual_accuracy
        p.brier_score = statistics.mean((r.confidence - (1.0 if r.was_correct else 0.0))**2 for r in resolved)
        # Grade calibration
        if abs(p.overconfidence_score) < 0.05: p.calibration_grade = "A"
        elif abs(p.overconfidence_score) < 0.10: p.calibration_grade = "B"
        elif abs(p.overconfidence_score) < 0.20: p.calibration_grade = "C"
        else: p.calibration_grade = "F"
        return p

class ResearcherRanking:
    @staticmethod
    def rank(profiles: list[CalibrationProfile], historical_ranks: dict = None) -> list[ResearcherRank]:
        results = []
        for prof in profiles:
            r = ResearcherRank(forecaster_id=prof.forecaster_id, directional_accuracy=prof.actual_accuracy,
                               calibration_score=1.0 - prof.brier_score)
            r.composite_score = r.directional_accuracy * 0.4 + r.calibration_score * 0.4 + 0.2
            if historical_ranks and prof.forecaster_id in historical_ranks:
                prev = historical_ranks[prof.forecaster_id]
                diff = r.composite_score - prev
                r.trend = "IMPROVING" if diff > 0.05 else ("DECLINING" if diff < -0.05 else "STABLE")
            results.append(r)
        ranked = sorted(results, key=lambda x: x.composite_score, reverse=True)
        for i, r in enumerate(ranked): r.rank = i + 1
        return ranked

    @staticmethod
    def top_performers(rankings: list[ResearcherRank], n: int = 5) -> list[ResearcherRank]:
        return [r for r in rankings if r.rank <= n]
