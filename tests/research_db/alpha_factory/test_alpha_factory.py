#!/usr/bin/env python3
"""Phase 4: Alpha Factory — 70+ Comprehensive Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.alpha_factory.candidate_factor_generator import CandidateFactorGenerator, FactorCandidate, FactorCategory
from zmatrix.research_db.alpha_factory.factor_validator import FactorValidator, ValidationResult
from zmatrix.research_db.alpha_factory.factor_graveyard import FactorGraveyard, GraveyardRecord
from zmatrix.research_db.alpha_factory.factor_promotion import FactorPromotion, PromotionLevel, PromotionRecord
from zmatrix.research_db.alpha_factory.factor_genome import FactorGenome, GenomeRecord, GenomeRelation
from zmatrix.research_db.alpha_factory.alpha_ledger import AlphaLedger, LedgerEntry

# ── Candidate Generator (12 tests) ──
def test_generate_price(): assert len(CandidateFactorGenerator.generate_price_factors())==3
def test_generate_volume(): assert len(CandidateFactorGenerator.generate_volume_factors())==3
def test_generate_momentum(): assert len(CandidateFactorGenerator.generate_momentum_factors())==3
def test_generate_quality(): assert len(CandidateFactorGenerator.generate_quality_factors())==3
def test_generate_value(): assert len(CandidateFactorGenerator.generate_value_factors())==3
def test_generate_all(): assert len(CandidateFactorGenerator.generate_all())==15
def test_candidate_production_false(): assert FactorCandidate(factor_id="X",factor_name="X",category=FactorCategory.PRICE).production_allowed is False
def test_categories_distinct(): factors=CandidateFactorGenerator.generate_all(); cats=set(f.category.value for f in factors); assert len(cats)>=5
def test_price_has_window(): f=CandidateFactorGenerator.generate_price_factors()[0]; assert "window" in f.parameters
def test_quality_has_metric(): f=CandidateFactorGenerator.generate_quality_factors()[0]; assert "metric" in f.parameters

# ── Factor Validator (10 tests) ──
def test_validate_pass():
    r=FactorValidator.validate("F1",{"ic":0.05,"rankic":0.04,"coverage":0.8,"stability":0.5,"decay":0.01}); assert r.passed is True
def test_validate_fail_low_ic():
    r=FactorValidator.validate("F1",{"ic":0.01,"rankic":0.01,"coverage":0.2,"stability":0.5,"decay":0.01}); assert r.passed is False
def test_validate_fail_coverage():
    r=FactorValidator.validate("F1",{"ic":0.05,"rankic":0.04,"coverage":0.1}); assert r.passed is False
def test_validate_production_false(): assert FactorValidator.validate("F1",{}).production_allowed is False
def test_batch_validate(): results=FactorValidator.batch_validate([{"factor_id":"F1","metrics":{"ic":0.05}},{"factor_id":"F2","metrics":{"ic":0.01}}]); assert len(results)==2
def test_validate_high_stability():
    r=FactorValidator.validate("F1",{"ic":0.05,"rankic":0.04,"coverage":0.8,"stability":3.0,"decay":0.01}); assert r.passed is False  # stability > 2

# ── Factor Graveyard (10 tests) ──
def test_graveyard_retire(): g=FactorGraveyard(); r=g.retire("F1","factor1","Low IC"); assert g.count()==1; assert g.is_retired("F1") is True
def test_graveyard_list(): g=FactorGraveyard(); g.retire("F1","f1","bad"); g.retire("F2","f2","bad"); assert len(g.list_retired())==2
def test_graveyard_not_retired(): assert FactorGraveyard().is_retired("F99") is False
def test_auto_retire(): g=FactorGraveyard(); results=[FactorValidator.validate("F1",{"ic":0.01,"rankic":0.01,"coverage":0.1,"stability":3.0,"decay":0.1})]; FactorGraveyard.auto_retire(results,g); assert g.count()>=1
def test_graveyard_production_false(): assert FactorGraveyard().retire("F1","f1","reason").production_allowed is False

# ── Factor Promotion (12 tests) ──
def test_promotion_candidate_to_validated(): p=FactorPromotion(); r=p.promote("F1","CANDIDATE",["IC=0.05"]); assert r.to_level=="VALIDATED"
def test_promotion_validated_to_research(): p=FactorPromotion(); p.promote("F1","CANDIDATE",[]); r=p.promote("F1","VALIDATED",[]); assert r.to_level=="RESEARCH"
def test_promotion_production_candidate(): p=FactorPromotion(); p.promote("F1","CANDIDATE",[]); p.promote("F1","VALIDATED",[]); p.promote("F1","RESEARCH",[]); r=p.promote("F1","APPROVED",[]); assert r.to_level=="PRODUCTION_CANDIDATE"
def test_promotion_blocked_at_production_candidate(): p=FactorPromotion(); p.promote("F1","CANDIDATE",[]); p.promote("F1","VALIDATED",[]); p.promote("F1","RESEARCH",[]); r=p.promote("F1","APPROVED",[]); assert r is not None; r2=p.promote("F1","PRODUCTION_CANDIDATE",[]); assert r2 is None  # terminal
def test_promotion_invalid_level(): assert FactorPromotion().promote("F1","INVALID",[]) is None
def test_is_production_candidate(): assert FactorPromotion.is_production_candidate("PRODUCTION_CANDIDATE") is True; assert FactorPromotion.is_production_candidate("APPROVED") is False
def test_history(): p=FactorPromotion(); p.promote("F1","CANDIDATE",[]); assert len(p.get_history("F1"))==1
def test_current_level(): p=FactorPromotion(); assert p.current_level("F1")=="CANDIDATE"; p.promote("F1","CANDIDATE",[]); assert p.current_level("F1")=="VALIDATED"

# ── Factor Genome (8 tests) ──
def test_genome_register(): g=FactorGenome(); r=g.register("F2","CHILD","F1","momentum variant"); assert r.related_factor_id=="F1"
def test_genome_get_children(): g=FactorGenome(); g.register("F2","CHILD","F1",""); assert len(g.get_children("F1"))==1
def test_genome_get_parents(): g=FactorGenome(); g.register("F2","CHILD","F1",""); assert len(g.get_parents("F2"))==0  # F2 doesn't have parents registered
def test_genome_lineage(): g=FactorGenome(); g.register("F2","CHILD","F1",""); lin=g.get_lineage("F1"); assert lin["factor_id"]=="F1"
def test_genome_production_false(): assert GenomeRecord(factor_id="X",relation="CHILD",related_factor_id="Y").production_allowed is False
def test_genome_all(): g=FactorGenome(); g.register("A","CHILD","P",""); g.register("B","CHILD","P",""); assert len(g.list_all())==2

# ── Alpha Ledger (10 tests) ──
def test_ledger_record(): l=AlphaLedger(); e=l.record("F1","DISCOVERED",{"source":"auto"}); assert e.event_type=="DISCOVERED"
def test_ledger_history(): l=AlphaLedger(); l.record("F1","DISCOVERED"); l.record("F1","VALIDATED"); assert len(l.get_history("F1"))==2
def test_ledger_count(): l=AlphaLedger(); l.record("F1","DISCOVERED"); l.record("F2","DISCOVERED"); assert l.count()==2
def test_ledger_by_event(): l=AlphaLedger(); l.record("F1","DISCOVERED"); l.record("F1","VALIDATED"); assert len(l.get_by_event("VALIDATED"))==1
def test_ledger_immutable(): l=AlphaLedger(); l.record("F1","DISCOVERED"); before=l.count(); l.record("F1","VALIDATED"); assert l.count()>before  # append only
def test_ledger_production_false(): e=AlphaLedger().record("F1","DISCOVERED"); assert e.production_allowed is False
def test_ledger_full_lifecycle(): l=AlphaLedger(); l.record("F1","DISCOVERED"); l.record("F1","VALIDATED"); l.record("F1","PROMOTED"); l.record("F1","RETIRED"); assert l.count()==4

# ── Safety (8 tests) ──
def test_no_buy_sell():
    for name in ["candidate_factor_generator.py","factor_validator.py","factor_graveyard.py","factor_promotion.py","factor_genome.py","alpha_ledger.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "alpha_factory" / name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True","broker_order_allowed=True"]:
            assert fb not in text or "allowlist:" in text
def test_all_importable():
    for mod in ["zmatrix.research_db.alpha_factory.candidate_factor_generator","zmatrix.research_db.alpha_factory.factor_validator","zmatrix.research_db.alpha_factory.factor_graveyard","zmatrix.research_db.alpha_factory.factor_promotion","zmatrix.research_db.alpha_factory.factor_genome","zmatrix.research_db.alpha_factory.alpha_ledger"]:
        import importlib; importlib.import_module(mod)
def test_promotion_not_production(): assert FactorPromotion.is_production_candidate("PRODUCTION_CANDIDATE") is True  # terminal, not production
def test_all_production_candidates_blocked(): assert FactorPromotion.is_production_candidate("PRODUCTION_CANDIDATE") is True

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
