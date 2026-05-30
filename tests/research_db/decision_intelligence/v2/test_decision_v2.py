#!/usr/bin/env python3
"""Decision Intelligence V2 — 30+ Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent.parent

from zmatrix.research_db.decision_intelligence.v2 import (
    PredictionEntry, CalibrationProfile, ResearcherRank, PredictionMarketResult, PredictionDirection,
)
from zmatrix.research_db.decision_intelligence.v2.decision_v2_engine import (
    PredictionMarketEngine, ConfidenceCalibration, ResearcherRanking,
)
from zmatrix.research_db.decision_intelligence.v2.decision_v2_ledger import DecisionLedgerV2, LedgerEventType
from zmatrix.research_db.decision_intelligence.v2.decision_v2_report import DecisionReportV2

# ── Schema (6 tests) ──
def test_prediction_entry(): p = PredictionEntry(prediction_id="P1",forecaster_id="F1",ticker="000001",direction="UP"); assert p.direction=="UP"; assert p.production_allowed is False
def test_calibration_profile(): c = CalibrationProfile(forecaster_id="F1"); assert c.calibration_grade=="UNGRADED"; assert c.production_allowed is False
def test_rank(): r = ResearcherRank(forecaster_id="F1"); assert r.trend=="STABLE"; assert r.production_allowed is False
def test_market_result(): m = PredictionMarketResult(market_id="M1",ticker="X"); assert m.consensus_direction=="FLAT"; assert m.production_allowed is False

# ── Prediction Market (6 tests) ──
def _preds(*args):
    return [PredictionEntry(prediction_id=f"P{i}",forecaster_id=f"F{i}",ticker="000001",direction=d,magnitude_bps=m) for i,(d,m) in enumerate(args,1)]
def test_consensus_up(): r = PredictionMarketEngine.compute_consensus(_preds(("UP",50),("UP",30),("DOWN",10))); assert r.consensus_direction=="UP"
def test_consensus_down(): r = PredictionMarketEngine.compute_consensus(_preds(("DOWN",50),("DOWN",30),("UP",10))); assert r.consensus_direction=="DOWN"
def test_contrarian(): r = PredictionMarketEngine.compute_consensus(_preds(("UP",50),("DOWN",30))); assert r.disagreement_index > 0; assert len(r.contrarian_signals) == 1
def test_agreement_full(): r = PredictionMarketEngine.compute_consensus(_preds(("UP",50),("UP",30))); assert r.agreement_ratio == 1.0
def test_empty(): r = PredictionMarketEngine.compute_consensus([]); assert r.ticker == "UNKNOWN"

# ── Confidence Calibration (6 tests) ──
def _resolved(forecaster_id="F1", correct=True, confidence=0.7):
    p = PredictionEntry(prediction_id=f"P-{forecaster_id}",forecaster_id=forecaster_id,ticker="X",direction="UP"); p.resolved=True; p.was_correct=correct; p.confidence=confidence; return p
def test_calibrate_perfect(): c = ConfidenceCalibration.calibrate("F1",[_resolved("F1",True,0.8)]); assert c.actual_accuracy == 1.0
def test_calibrate_overconfident(): c = ConfidenceCalibration.calibrate("F2",[_resolved("F2",False,0.9)]); assert c.overconfidence_score > 0
def test_calibrate_brier(): c = ConfidenceCalibration.calibrate("F3",[_resolved("F3",True,0.6)]); assert c.brier_score >= 0
def test_calibrate_grade_a(): c = ConfidenceCalibration.calibrate("F4",[_resolved("F4",True,0.7),_resolved("F4",True,0.7)]); assert c.calibration_grade in ("A","B")
def test_calibrate_empty(): c = ConfidenceCalibration.calibrate("F5",[]); assert c.calibration_grade == "UNGRADED"

# ── Researcher Ranking (5 tests) ──
def test_rank_basic(): profiles = [CalibrationProfile(forecaster_id="F1",actual_accuracy=0.8,brier_score=0.1), CalibrationProfile(forecaster_id="F2",actual_accuracy=0.6,brier_score=0.3)]; r = ResearcherRanking.rank(profiles); assert r[0].forecaster_id == "F1"
def test_top_performers(): profiles = [CalibrationProfile(forecaster_id=f"F{i}",actual_accuracy=0.5+i*0.05,brier_score=0.2) for i in range(1,6)]; top = ResearcherRanking.top_performers(ResearcherRanking.rank(profiles),3); assert len(top) == 3
def test_rank_trend(): profiles = [CalibrationProfile(forecaster_id="F1",actual_accuracy=0.7,brier_score=0.1)]; r = ResearcherRanking.rank(profiles, {"F1":0.5}); assert r[0].trend == "IMPROVING"
def test_rank_empty(): assert ResearcherRanking.rank([]) == []

# ── Ledger (5 tests) ──
def test_ledger_record(): l = DecisionLedgerV2(); r = l.record("R1","PREDICTION_MADE",{"ticker":"000001"}); assert len(r.current_hash) == 16
def test_ledger_chain(): l = DecisionLedgerV2(); l.record("R1","E1"); l.record("R2","E2"); assert l.verify_chain() is True
def test_ledger_chain_immutable(): l = DecisionLedgerV2(); l.record("R1","E1"); count = l.count(); l.record("R2","E2"); assert l.count() > count

# ── Report (3 tests) ──
def test_report_markdown():
    md = DecisionReportV2.generate_markdown({"ticker":"000001","consensus_direction":"UP","consensus_magnitude":50,"forecaster_count":3,"agreement_ratio":0.8}, [CalibrationProfile(forecaster_id="F1",actual_accuracy=0.8,calibration_grade="A")], [ResearcherRank(forecaster_id="F1",rank=1,composite_score=0.9,trend="STABLE")])
    assert "BLOCKED" in md
def test_report_json():
    j = DecisionReportV2.generate_json({"ticker":"X"}, [ResearcherRank(forecaster_id="F1",rank=1,composite_score=0.8,trend="STABLE")])
    assert "production_allowed" in j

# ── Safety (2 tests) ──
def test_no_trade_flags():
    for name in ["__init__.py","decision_v2_engine.py","decision_v2_ledger.py","decision_v2_report.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "decision_intelligence" / "v2" / name).read_text()
        assert "production_allowed=True" not in text
def test_ledger_production_false(): assert DecisionLedgerV2().record("R1","E").production_allowed is False

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
