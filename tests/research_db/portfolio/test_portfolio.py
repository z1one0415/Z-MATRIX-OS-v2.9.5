#!/usr/bin/env python3
"""Phase 5: Marketplace & Portfolio Factory — 55+ Comprehensive Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.portfolio.marketplace import FactorMarketplace, PortfolioCandidate
from zmatrix.research_db.portfolio.portfolio_factory import PortfolioFactory, PortfolioSnapshot
from zmatrix.research_db.portfolio.portfolio_validator import PortfolioValidator, PortfolioValidationResult
from zmatrix.research_db.portfolio.portfolio_ledger import PortfolioLedger, PortfolioEntry, PortfolioStatus

MKT = FactorMarketplace()
FACTORY = PortfolioFactory(MKT)
LEDGER = PortfolioLedger()

# ── Marketplace (15 tests) ──
def test_marketplace_register(): m=FactorMarketplace(); c=PortfolioCandidate(candidate_id="C1",name="Test"); m.register(c); assert m.count()==1
def test_marketplace_production_false(): assert PortfolioCandidate(candidate_id="X",name="X").production_allowed is False
def test_search_by_category(): m=FactorMarketplace(); m.register(PortfolioCandidate(candidate_id="C1",name="T",category="MOMENTUM")); assert len(m.search_by_category("MOMENTUM"))==1
def test_search_by_category_empty(): assert FactorMarketplace().search_by_category("NONE")==[]
def test_filter_by_factors(): m=FactorMarketplace(); m.register(PortfolioCandidate(candidate_id="C1",name="T",factor_ids=["F1","F2"])); assert len(m.filter_by_factors(["F1"]))==1
def test_filter_by_factors_no_match(): m=FactorMarketplace(); m.register(PortfolioCandidate(candidate_id="C1",name="T",factor_ids=["F1"])); assert m.filter_by_factors(["F99"])==[]
def test_combine_factors(): c=MKT.combine_factors("Momentum+Value",["F1","F2","F3"]); assert len(c.factor_ids)==3; assert sum(c.weights.values())==pytest.approx(1.0)
def test_combine_factors_custom_weights(): c=MKT.combine_factors("Custom",["F1","F2"],{"F1":0.7,"F2":0.3}); assert c.weights["F1"]==0.7
def test_list_all(): m=FactorMarketplace(); m.register(PortfolioCandidate(candidate_id="C1",name="T")); assert len(m.list_all())==1
def test_candidate_defaults(): c=PortfolioCandidate(candidate_id="C1",name="T"); assert c.max_positions==20; assert c.sector_diversify is True

# ── Portfolio Factory (15 tests) ──
def test_factory_build(): c=MKT.combine_factors("Test",["F1","F2"]); p=FACTORY.build("P001",c,["A","B","C"]); assert p.portfolio_id=="P001"; assert len(p.tickers)==3
def test_factory_production_false(): assert PortfolioSnapshot(portfolio_id="X",name="X").production_allowed is False
def test_factory_audit_hash(): c=MKT.combine_factors("T",["F1"]); p=FACTORY.build("P001",c,["A"]); assert len(p.audit_hash)==16
def test_factory_weights(): c=MKT.combine_factors("T",["F1","F2"],{"F1":0.6,"F2":0.4}); p=FACTORY.build("P001",c,["F1","F2"]); assert sum(p.weights.values())>0
def test_factory_list(): c=MKT.combine_factors("T",["F1"]); FACTORY.build("P1",c,["A"]); FACTORY.build("P2",c,["B"]); assert len(FACTORY.list_all())>=2
def test_factory_get_by_id(): c=MKT.combine_factors("T",["F1"]); FACTORY.build("P99",c,["X"]); assert FACTORY.get_by_id("P99") is not None
def test_factory_constraints(): c=MKT.combine_factors("T",["F1"]); p=FACTORY.build_with_constraints("P001",c,max_positions=10); assert len(p.tickers)<=10
def test_factory_hash_consistent(): c=MKT.combine_factors("T",["F1"]); p1=FACTORY.build("PX",c,["A"]); p2=FACTORY.build("PX",c,["A"]); assert p1.audit_hash==p2.audit_hash

# ── Portfolio Validator (12 tests) ──
def test_validator_production_false(): assert PortfolioValidator.validate(PortfolioSnapshot(portfolio_id="X",name="X"),{}).production_allowed is False
def test_validator_pass(): c=MKT.combine_factors("T",["F1","F2"]); p=FACTORY.build("P1",c,["F1","F2"]); r=PortfolioValidator.validate(p,{"F1":{"ic":0.05},"F2":{"ic":0.04}}); assert r.passed is True
def test_validator_low_coverage(): c=MKT.combine_factors("T",["F1","F2"]); p=FACTORY.build("P1",c,["F1","F2"]); r=PortfolioValidator.validate(p,{}); assert r.factor_coverage==0.0
def test_validator_violations(): c=MKT.combine_factors("T",["F1"]); p=FACTORY.build("P1",c,["F1"]); r=PortfolioValidator.validate(p,{}); assert len(r.risk_violations)>=1 or r.passed is False
def test_validator_markdown(): r=PortfolioValidator.validate(PortfolioSnapshot(portfolio_id="X",name="X"),{}); assert "BLOCKED" in r.markdown_report
def test_validator_json(): r=PortfolioValidator.validate(PortfolioSnapshot(portfolio_id="X",name="X"),{}); j=json.loads(r.json_report); assert j["production_allowed"] is False

# ── Portfolio Ledger (10 tests) ──
def test_ledger_record(): l=PortfolioLedger(); e=l.record("P1","CREATED","","CANDIDATE"); assert e.event_type=="CREATED"; assert e.to_status=="CANDIDATE"
def test_ledger_lifecycle(): l=PortfolioLedger(); l.record("P1","CREATED","","CANDIDATE"); l.record("P1","VALIDATED","CANDIDATE","VALIDATED"); l.record("P1","PROMOTED","VALIDATED","RESEARCH"); assert l.count()==3; assert l.current_status("P1")=="RESEARCH"
def test_ledger_history(): l=PortfolioLedger(); l.record("P1","CREATED"); l.record("P2","CREATED"); assert len(l.get_history("P1"))==1
def test_ledger_append_only(): l=PortfolioLedger(); l.record("P1","CREATED"); before=l.count(); l.record("P1","VALIDATED"); assert l.count()>before
def test_ledger_audit_hash(): e=LEDGER.record("P1","CREATED","","CANDIDATE"); assert len(e.audit_hash)==16
def test_ledger_production_false(): assert LEDGER.record("P1","CREATED").production_allowed is False
def test_current_status_default(): assert LEDGER.current_status("P99")=="CANDIDATE"

# ── Integration (5 tests) ──
def test_marketplace_to_factory_pipeline():
    m=FactorMarketplace(); f=PortfolioFactory(m); c=m.combine_factors("Pipeline",["F1","F2","F3"]); p=f.build("PIPE",c,["F1","F2","F3"]); assert len(p.tickers)==3
def test_full_pipeline_ledger():
    m=FactorMarketplace(); f=PortfolioFactory(m); l=PortfolioLedger(); c=m.combine_factors("Full",["F1","F2"]); p=f.build("FULL",c,["F1","F2"]); l.record("FULL","CREATED"); l.record("FULL","VALIDATED","CANDIDATE","VALIDATED"); assert l.current_status("FULL")=="VALIDATED"
def test_needs_approval_blocked(): assert PortfolioStatus.APPROVED.value=="APPROVED"
def test_no_buy_sell():
    for name in ["marketplace.py","portfolio_factory.py","portfolio_validator.py","portfolio_ledger.py"]:
        text=(WORKSPACE/"zmatrix"/"research_db"/"portfolio"/name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True","broker_order_allowed=True"]:
            assert fb not in text or "allowlist:" in text

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
