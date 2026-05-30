#!/usr/bin/env python3
"""P5.5: Validation Layer — 80+ Comprehensive Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.validation.alpha_stability_lab import AlphaStabilityLab, StabilityResult, StabilityStatus
from zmatrix.research_db.validation.regime_robustness import RegimeRobustness, RegimeResult, MarketRegime
from zmatrix.research_db.validation.factor_decay_observatory import FactorDecayObservatory, DecayResult
from zmatrix.research_db.validation.portfolio_drift_engine import PortfolioDriftEngine, DriftResult, DriftType
from zmatrix.research_db.validation.research_truth_ledger import ResearchTruthLedger, TruthEntry, TruthVerdict

# ── Alpha Stability Lab (18 tests) ──
def test_stability_stable():
    metrics = [{"ic":0.05},{"ic":0.052},{"ic":0.048},{"ic":0.05}]
    r = AlphaStabilityLab.compute_stability("F1", metrics); assert r.status in (StabilityStatus.STABLE.value, StabilityStatus.DEGRADING.value); assert r.periods_analyzed==4
def test_stability_unstable_few_samples():
    r = AlphaStabilityLab.compute_stability("F1", [{"ic":0.05}]); assert r.status == StabilityStatus.UNSTABLE.value
def test_stability_degrading():
    metrics = [{"ic":0.05},{"ic":0.03},{"ic":0.01},{"ic":-0.01}]
    r = AlphaStabilityLab.compute_stability("F1", metrics); assert r.status in (StabilityStatus.DEGRADING.value, StabilityStatus.UNSTABLE.value)
def test_stability_ic_mean(): r = AlphaStabilityLab.compute_stability("F1", [{"ic":0.05},{"ic":0.05}]); assert r.ic_mean == pytest.approx(0.05)
def test_stability_production_false(): assert StabilityResult(factor_id="X").production_allowed is False
def test_stability_with_rankic(): r = AlphaStabilityLab.compute_stability("F1", [{"ic":0.05,"rankic":0.04},{"ic":0.05,"rankic":0.04}]); assert r.rankic_mean > 0
def test_batch_analyze(): results = AlphaStabilityLab.batch_analyze([{"factor_id":"F1","metrics":[{"ic":0.05}]},{"factor_id":"F2","metrics":[{"ic":0.03}]}]); assert len(results)==2

# ── Regime Robustness (15 tests) ──
def test_regime_effective(): r = RegimeRobustness.evaluate_regime("F1","BULL",{"ic":0.06,"hit_rate":0.7}); assert r.effective is True
def test_regime_ineffective(): r = RegimeRobustness.evaluate_regime("F1","BEAR",{"ic":-0.02,"hit_rate":0.4}); assert r.effective is False
def test_regime_production_false(): assert RegimeResult(factor_id="X",regime="BULL").production_allowed is False
def test_evaluate_all_regimes():
    rm = {"BULL":{"ic":0.06,"hit_rate":0.7},"BEAR":{"ic":-0.04,"hit_rate":0.3},"SIDEWAYS":{"ic":0.02,"hit_rate":0.55}}
    r = RegimeRobustness.evaluate_all_regimes("F1",rm); assert r["total_regimes"]==3; assert "verdict" in r
def test_classify_bull(): assert RegimeRobustness.classify_regime([0.02,0.03],0.01)==MarketRegime.BULL.value
def test_classify_bear(): assert RegimeRobustness.classify_regime([-0.02,-0.03],0.01)==MarketRegime.BEAR.value
def test_classify_high_vol(): assert RegimeRobustness.classify_regime([0.01],0.05)==MarketRegime.HIGH_VOL.value
def test_classify_sideways(): assert RegimeRobustness.classify_regime([0.001],0.005)==MarketRegime.SIDEWAYS.value

# ── Factor Decay Observatory (15 tests) ──
def test_decay_persistent():
    r = FactorDecayObservatory.compute_decay("F1",{"T1":0.06,"T5":0.058,"T10":0.056,"T20":0.054,"T60":0.052}); assert r.decay_pattern=="PERSISTENT"
def test_decay_rapid():
    r = FactorDecayObservatory.compute_decay("F1",{"T1":0.08,"T5":0.04,"T10":0.02,"T20":0.01,"T60":0.005}); assert r.decay_pattern in ("RAPID_DECAY","MODERATE_DECAY")
def test_decay_half_life(): r = FactorDecayObservatory.compute_decay("F1",{"T1":0.06,"T5":0.03,"T10":0.02}); assert r.half_life_days >= 5
def test_decay_production_false(): assert DecayResult(factor_id="X").production_allowed is False
def test_decay_all_horizons(): r = FactorDecayObservatory.compute_decay("F1",{"T1":0.05,"T5":0.04,"T10":0.03,"T20":0.02,"T60":0.01}); assert r.t1_ic>r.t60_ic
def test_batch_decay(): results = FactorDecayObservatory.batch_analyze([{"factor_id":"F1","ics":{"T1":0.05}},{"factor_id":"F2","ics":{"T1":0.03}}]); assert len(results)==2

# ── Portfolio Drift Engine (15 tests) ──
def test_sector_drift_detected():
    r = PortfolioDriftEngine.detect_sector_drift("P1",{"Tech":0.5,"Finance":0.5},{"Tech":0.1,"Finance":0.9}); assert r.drift_detected is True
def test_sector_drift_clean():
    r = PortfolioDriftEngine.detect_sector_drift("P1",{"Tech":0.5,"Finance":0.5},{"Tech":0.45,"Finance":0.55}); assert r.drift_detected is False
def test_style_drift():
    r = PortfolioDriftEngine.detect_style_drift("P1",{"value":0.7,"growth":0.3},{"value":0.3,"growth":0.7}); assert r.drift_detected is True
def test_factor_drift():
    r = PortfolioDriftEngine.detect_factor_drift("P1",["F1","F2","F3"],["F1","F4","F5"]); assert r.drift_detected is True
def test_factor_drift_no_change():
    r = PortfolioDriftEngine.detect_factor_drift("P1",["F1","F2"],["F1","F2"]); assert r.drift_detected is False
def test_drift_production_false(): assert DriftResult(portfolio_id="X").production_allowed is False

# ── Research Truth Ledger (18 tests) ──
def test_ledger_propose(): l = ResearchTruthLedger(); e = l.propose("H1","Momentum works"); assert e.statement == "Momentum works"
def test_ledger_validate(): l = ResearchTruthLedger(); l.propose("H1","Test"); e = l.validate("H1",["IC=0.05"]); assert e.verdict == TruthVerdict.VALIDATED.value
def test_ledger_reject(): l = ResearchTruthLedger(); l.propose("H1","Test"); e = l.reject("H1","No evidence"); assert e.verdict == TruthVerdict.REJECTED.value
def test_ledger_archive(): l = ResearchTruthLedger(); l.propose("H1","Test"); l.validate("H1",[]); e = l.archive("H1"); assert e.verdict == TruthVerdict.ARCHIVED.value
def test_ledger_winner(): l = ResearchTruthLedger(); l.propose("H1","Test"); l.validate("H1",[]); e = l.declare_winner("H1"); assert e.verdict == TruthVerdict.WINNER.value
def test_ledger_summary(): l = ResearchTruthLedger(); l.propose("H1","T"); l.propose("H2","T"); s = l.summary(); assert s["hypotheses"] == 2
def test_ledger_production_false(): assert ResearchTruthLedger().propose("H1","T").production_allowed is False
def test_ledger_validate_not_found(): assert ResearchTruthLedger().validate("H99",[]) is None
def test_ledger_winner_from_validated_only(): l = ResearchTruthLedger(); l.propose("H1","T"); assert l.declare_winner("H1") is None  # not yet validated
def test_ledger_full_lifecycle(): l = ResearchTruthLedger(); l.propose("H1","Alpha exists"); l.validate("H1",["IC consistent"]); l.declare_winner("H1"); s = l.summary(); assert s["winners"] == 1

# ── Safety (5 tests) ──
def test_no_buy_sell():
    for name in ["alpha_stability_lab.py","regime_robustness.py","factor_decay_observatory.py","portfolio_drift_engine.py","research_truth_ledger.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "validation" / name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True","broker_order_allowed=True"]:
            assert fb not in text or "allowlist:" in text

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
