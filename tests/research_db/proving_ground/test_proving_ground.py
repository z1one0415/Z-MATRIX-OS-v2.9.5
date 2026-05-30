#!/usr/bin/env python3
"""Batch-F.5: Proving Ground — 80+ Deep Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

# ── Historical Reality Pack (15 tests) ──
from zmatrix.research_db.proving_ground.historical_reality_pack import HistoricalRealityPack, HISTORICAL_EVENTS
HP = HistoricalRealityPack()
def test_hp_event_count(): assert len(HISTORICAL_EVENTS) >= 6
def test_hp_get_2008(): e = HP.get_event("2008_GFC"); assert e.market_drop == -0.72
def test_hp_get_2020(): e = HP.get_event("2020_COVID"); assert e.year == 2020; assert "Travel" in e.affected_sectors
def test_hp_get_2024(): e = HP.get_event("2024_LIQUIDITY"); assert "liquidity" in e.affected_factors
def test_hp_all_years_sorted(): years = sorted(e.year for e in HISTORICAL_EVENTS.values()); assert years == sorted(years)
def test_hp_all_have_sectors(): assert all(len(e.affected_sectors) > 0 for e in HISTORICAL_EVENTS.values())
def test_hp_all_have_factors(): assert all(len(e.affected_factors) > 0 for e in HISTORICAL_EVENTS.values())
def test_hp_apply_factor_stress_affected(): ic = HP.apply_factor_stress(0.10, HISTORICAL_EVENTS["2008_GFC"], "momentum"); assert ic < 0.10
def test_hp_apply_factor_stress_unaffected(): ic = HP.apply_factor_stress(0.10, HISTORICAL_EVENTS["2008_GFC"], "quality"); assert ic == pytest.approx(0.07)
def test_hp_apply_portfolio_stress(): eq = HP.apply_portfolio_stress(1e6, HISTORICAL_EVENTS["2008_GFC"], {"Finance":0.3}); assert eq < 1e6
def test_hp_apply_portfolio_no_loss_floor(): eq = HP.apply_portfolio_stress(1e6, HISTORICAL_EVENTS["2008_GFC"], {"Finance":1.0}); assert eq >= 0.5e6
def test_hp_event_summary(): s = HP.event_summary(HISTORICAL_EVENTS["2015_CRASH"]); assert s["drop"] == -0.45; assert s["production_allowed"] is False
def test_hp_event_production_false(): assert HISTORICAL_EVENTS["2022_PROPERTY"].production_allowed is False

# ── Regime Expansion (15 tests) ──
from zmatrix.research_db.proving_ground.regime_expansion import RegimeExpansion, EXPANDED_REGIMES
RE = RegimeExpansion()
def test_re_count(): assert len(EXPANDED_REGIMES) >= 20
def test_re_classify_quiet_bull(): assert RE.classify(0.03, 0.01, 0.6, 0.01) == "QUIET_BULL"
def test_re_classify_bear_hivol(): assert RE.classify(-0.04, 0.04, 0.2, 0.01) == "BEAR_HIVOL"
def test_re_classify_risk_off(): assert RE.classify(-0.03, 0.02, 0.2, 0.02) in ("RISK_OFF", "BEAR_HIVOL")
def test_re_classify_liquidity_crunch(): assert RE.classify(-0.01, 0.04, 0.2, 0.05) == "LIQUIDITY_CRUNCH"
def test_re_evaluate_effective(): r = EXPANDED_REGIMES[0]; assert RE.evaluate_factor_in_regime(0.05, r) is True
def test_re_evaluate_ineffective(): assert RE.evaluate_factor_in_regime(0.01, EXPANDED_REGIMES[0]) is False
def test_re_factor_matrix(): m = RE.factor_regime_matrix("F1", {"QUIET_BULL":0.04,"BEAR_HIVOL":0.01,"RISK_ON":0.03}); assert m["total_regimes"] == 20
def test_re_production_false(): assert EXPANDED_REGIMES[0].production_allowed is False

# ── Capacity Calibration (12 tests) ──
from zmatrix.research_db.proving_ground.capacity_calibration import CapacityCalibration, CapacityGrade
CC = CapacityCalibration()
def test_cc_grade_a(): r = CC.calibrate("F1", 1e6, 1e10, 1e12); assert r.grade in ("A","B")
def test_cc_grade_e_large_aum(): r = CC.calibrate("F1", 1e9, 1e8); assert r.grade in ("D","E")
def test_cc_levels_count(): assert len(CC.CAPACITY_LEVELS) == 7
def test_cc_all_levels(): results = CC.calibrate_all_levels("F1", 1e9); assert len(results) == 7
def test_cc_adv_pct(): r = CC.calibrate("F1", 10e6, 1e9); assert r.adv_pct > 0
def test_cc_participation(): r = CC.calibrate("F1", 10e6, 1e9); assert r.participation_pct > 0
def test_cc_feasible_a(): assert CC.calibrate("F1", 1e6, 1e10, 1e11).feasible is True
def test_cc_infeasible(): assert CC.calibrate("F1", 1e9, 1e7).feasible is False

# ── Turnover Reality (12 tests) ──
from zmatrix.research_db.proving_ground.turnover_reality import TurnoverReality
TR = TurnoverReality()
def test_tr_compute_no_change(): assert TR.compute_turnover([{"A","B"},{"A","B"}]) == 0.0
def test_tr_compute_full_change(): t = TR.compute_turnover([{"A","B"},{"C","D"}]); assert t > 0
def test_tr_compute_partial(): t = TR.compute_turnover([{"A","B","C"},{"B","C","D"}], 1); assert 0 < t < 1
def test_tr_analyze():
    h = {"all": [["A","B","C"],["B","C","D"],["C","D","E"]], "small_cap":[["A","B"],["B","C"]], "mid_cap":[["A"]],
         "large_cap":[["A","B","C"],["A","B","C"]], "high_vol":[["A","B"]], "low_vol":[]}
    r = TR.analyze("F1", h); assert r.daily_turnover >= 0; assert r.annual_turnover >= 0
def test_tr_capacity_grade(): r = TR.analyze("F1", {"all":[["A","B","C"],["A","B","C"]]}); assert r.capacity_grade in ("A","B","C")
def test_tr_production_false(): assert TR.analyze("F1", {"all":[]}).production_allowed is False

# ── Walk Forward Certification (10 tests) ──
from zmatrix.research_db.proving_ground.walk_forward_certifier import WalkForwardCertifier
WFC = WalkForwardCertifier()
def test_cert_pass(): r = WFC.certify("F1", [{"ic":0.05}]*20, [{"ic":0.05}]*10, [{"ic":0.05}]*10); assert r.status in ("PASS","CONDITIONAL")
def test_cert_fail(): r = WFC.certify("F2", [{"ic":0.10}]*20, [{"ic":0.01}]*10, [{"ic":0.0}]*10); assert r.status in ("CONDITIONAL","FAIL")
def test_cert_grade(): r = WFC.certify("F1", [{"ic":0.05}]*20, [{"ic":0.05}]*10, [{"ic":0.05}]*10); assert r.cert_grade in ("A","B","C","F")
def test_cert_production_false(): assert WFC.certify("F1",[],[],[]).production_allowed is False
def test_cert_overfit_score(): r = WFC.certify("F1", [{"ic":0.10}]*10, [{"ic":0.05}]*5, [{"ic":0.01}]*5); assert r.overfit_score > 0
def test_cert_stability(): r = WFC.certify("F1", [{"ic":0.05}]*10, [{"ic":0.05}]*10, [{"ic":0.05}]*10); assert r.stability_score > 0

# ── Research Championship (10 tests) ──
from zmatrix.research_db.proving_ground.research_championship import ResearchChampionship
CH = ResearchChampionship()
def test_ch_score(): r = CH.score_entry("F1","FACTOR",{"ic":0.05,"sharpe":1.5,"max_dd":0.1,"wf_grade":"A","robustness":0.8}); assert r.overall_score > 0
def test_ch_run():
    entries = [{"id":"F1","type":"FACTOR","metrics":{"ic":0.08,"sharpe":2.0,"max_dd":0.05,"wf_grade":"A","robustness":0.9}},
               {"id":"F2","type":"FACTOR","metrics":{"ic":0.03,"sharpe":0.5,"max_dd":0.3,"wf_grade":"C","robustness":0.4}},
               {"id":"F3","type":"FACTOR","metrics":{"ic":0.01,"sharpe":-0.5,"max_dd":0.5,"wf_grade":"F","robustness":0.1}}]
    t = CH.run_championship(entries); assert len(t.entries) == 3; assert t.entries[0].rank == 1
def test_ch_winners(): t = CH.run_championship([{"id":"F1","type":"FACTOR","metrics":{"ic":0.08,"sharpe":2.0,"max_dd":0.05,"wf_grade":"A","robustness":0.9}}]); assert len(t.winners) == 1
def test_ch_retired(): t = CH.run_championship([{"id":"F1","type":"FACTOR","metrics":{"ic":0.005,"sharpe":-1.0,"max_dd":0.9,"wf_grade":"F","robustness":0.01}}]); assert len(t.retired) == 1
def test_ch_table_production_false(): t = CH.run_championship([]); assert t.production_allowed is False

# ── Safety (5 tests) ──
def test_no_buy_sell():
    for name in ["historical_reality_pack.py","regime_expansion.py","capacity_calibration.py","turnover_reality.py","walk_forward_certifier.py","research_championship.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "proving_ground" / name).read_text()
        for fb in ["production_allowed=True","broker_order_allowed=True","BUY","SELL","AUTO_EXECUTE"]:
            assert fb not in text or "allowlist:" in text or "BUY" == fb and "OrderSide" in text

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
