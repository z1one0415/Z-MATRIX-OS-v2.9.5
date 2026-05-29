"""C2-1/2 Integration tests — DataForge depth + FactorFactory depth"""
from pathlib import Path

def test_evidence_hash_stable():
    from zmatrix.dataforge.forge_depth import evidence_hash_build, EvidenceCard
    c1 = EvidenceCard("ev1","000001","","roe",15.2,"2026-05-29")
    c2 = EvidenceCard("ev1","000001","","roe",15.2,"2026-05-29")
    assert c1.evidence_hash == c2.evidence_hash

def test_pit_snapshot():
    from zmatrix.dataforge.forge_depth import PITSnapshot
    s = PITSnapshot("s1","2026-05-29","2026-04-25",pit_safe=True)
    assert s.production_allowed == False

def test_cross_source_conflict():
    from zmatrix.dataforge.forge_depth import CrossSourceValidation
    r = CrossSourceValidation.check({"roe":[{"value":15},{"value":14.5}]})
    assert r['status'] == 'CONSISTENT'

def test_fact_store():
    from zmatrix.dataforge.forge_depth import FactExtractionStore, EvidenceCard
    fs = FactExtractionStore(); fs.append(EvidenceCard("ev1","000001"))
    assert len(fs.get_by_ticker("000001")) == 1
    assert fs.production_allowed() == False

def test_trading_calendar():
    from zmatrix.factor_factory.factory_depth import TradingCalendar
    dates = [f"2026-05-{str(i).zfill(2)}" for i in range(1,31)]
    assert TradingCalendar.count_forward_trading_days(dates,"2026-05-01",20) >= 20

def test_outcome_horizon_t20_strict():
    from zmatrix.factor_factory.factory_depth import OutcomeHorizonDepth
    dates = [f"2026-06-{str(i).zfill(2)}" for i in range(1,30)]
    r = OutcomeHorizonDepth.check(dates,"2026-06-01","t20")
    assert r['horizon_ready']
    r2 = OutcomeHorizonDepth.check(dates[:5],"2026-01-01","t20")
    assert not r2['horizon_ready'] and r2['sample_ready'] == False

def test_ic_calculator():
    from zmatrix.factor_factory.factory_depth import ICICalculator
    r = ICICalculator.pearson_ic([1,2,3,4,5],[2,4,6,8,10])
    assert r['ic'] and r['ic'] > 0.9

def test_net_executable_blocked():
    from zmatrix.factor_factory.factory_depth import NetExecutableReturn
    r = NetExecutableReturn.compute(5.0,{'limit_up':True})
    assert r['executable'] == False and r['net_executable_return'] is None
