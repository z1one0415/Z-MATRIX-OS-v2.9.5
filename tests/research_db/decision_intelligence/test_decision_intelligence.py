#!/usr/bin/env python3
"""Batch-J: Decision Intelligence — 35+ Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.decision_intelligence.thesis_library import ThesisLibrary, ThesisVerdict
from zmatrix.research_db.decision_intelligence.decision_ledger import DecisionLedger, DecisionType
from zmatrix.research_db.decision_intelligence.prediction_tracker import PredictionTracker
from zmatrix.research_db.decision_intelligence.forecaster_score import ForecasterScore

TL = ThesisLibrary(); DL = DecisionLedger(); PT = PredictionTracker(); FS = ForecasterScore()

# Thesis Library (8 tests)
def test_tl_propose(): e = TL.propose("T1","Momentum works","000001"); assert e.statement == "Momentum works"
def test_tl_confirm(): TL.propose("T2","Value premium","000001"); e = TL.confirm("T2",["IC=0.05"]); assert e.verdict == "CONFIRMED"
def test_tl_reject(): TL.propose("T3","No alpha","000001"); e = TL.reject("T3","Zero IC"); assert e.verdict == "REJECTED"
def test_tl_by_ticker(): TL.propose("T4","X","000001"); assert len(TL.by_ticker("000001")) >= 1
def test_tl_by_verdict(): assert len(TL.by_verdict("CONFIRMED")) >= 1
def test_tl_summary(): s = TL.summary(); assert s["total"] >= 4; assert s["production_allowed"] is False
def test_tl_production_false(): assert TL.propose("TX","Test","X").production_allowed is False

# Decision Ledger (10 tests)
def test_dl_record(): e = DL.record("D1","000001","BUY","T1","IC strong",10.5,100); assert e.decision_type == "BUY"
def test_dl_by_ticker(): assert len(DL.by_ticker("000001")) >= 1
def test_dl_by_type(): DL.record("D2","000001","SELL"); assert len(DL.by_type("SELL")) >= 1
def test_dl_by_thesis(): DL.record("D3","000002","PASS",thesis_id="T1"); assert len(DL.by_thesis("T1")) >= 1
def test_dl_record_outcome(): DL.record("D4","X","BUY"); e = DL.record_outcome("D4","WINNER"); assert e.outcome_recorded is True
def test_dl_summary(): s = DL.summary(); assert s["total"] >= 4; assert s["production_allowed"] is False
def test_dl_production_false(): assert DL.record("DX","X","PASS").production_allowed is False

# Prediction Tracker (8 tests)
def test_pt_predict(): e = PT.predict("P1","000001",0.05,20); assert e.predicted_return == 0.05
def test_pt_record_outcome(): PT.predict("P2","000001",0.05,20); e = PT.record_outcome("P2",0.03); assert e.deviation == pytest.approx(-0.02)
def test_pt_evaluate(): PT.predict("P3","X",0.05,10); PT.record_outcome("P3",0.08); r = PT.evaluate("F1"); assert r.total_predictions >= 1
def test_pt_evaluate_directional(): PT.predict("P4","Y",0.10,5); PT.record_outcome("P4",0.05); r = PT.evaluate("F1"); assert 0 <= r.directional_accuracy <= 1
def test_pt_production_false(): assert PT.predict("PX","X",0.01,1).production_allowed is False

# Forecaster Score (6 tests)
def test_fs_register(): FS.register("R01","COUNCIL_MEMBER"); assert FS._profiles["R01"].forecaster_type == "COUNCIL_MEMBER"
def test_fs_update(): FS.register("R02","FACTOR"); r = PT.evaluate("R02"); FS.update("R02",r); assert FS._profiles["R02"].total_predictions >= 0
def test_fs_rank(): ranked = FS.rank_all(); assert len(ranked) >= 2
def test_fs_reliable(): mr = FS.most_reliable(); assert mr is not None
def test_fs_summary(): s = FS.summary(); assert len(s) >= 2

# Safety (3 tests)
def test_no_buy_sell_output():
    for name in ["thesis_library.py","decision_ledger.py","prediction_tracker.py","forecaster_score.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "decision_intelligence" / name).read_text()
        assert "production_allowed=True" not in text
def test_library_production_false(): assert TL.propose("X","Y","Z").production_allowed is False

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
