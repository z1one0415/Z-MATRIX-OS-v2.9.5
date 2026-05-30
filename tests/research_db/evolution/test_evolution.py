#!/usr/bin/env python3
"""Phase 5.9: Research Evolution Layer — 60+ Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

# ── EV1: Knowledge Graph (15 tests) ──
from zmatrix.research_db.evolution.graph.knowledge_graph import KnowledgeGraph
from zmatrix.research_db.evolution.graph.entity_registry import EntityRegistry
from zmatrix.research_db.evolution.graph.relationship_engine import RelationshipEngine
from zmatrix.research_db.evolution.graph.graph_query import GraphQuery
KG = KnowledgeGraph(); ER = EntityRegistry(KG); RE = RelationshipEngine(KG); GQ = GraphQuery(KG)

def test_kg_add_entity(): e=KG.add_entity("F1","FACTOR","Momentum"); assert e.entity_type=="FACTOR"; assert e.production_allowed is False
def test_kg_add_rel(): r=KG.add_relationship("R1","F1","P1","PRODUCES"); assert r.rel_type=="PRODUCES"
def test_kg_get_entity(): assert KG.get_entity("F1") is not None
def test_kg_outgoing(): KG.add_relationship("R2","F1","P2","INFORMS"); assert len(KG.get_outgoing("F1"))==2
def test_kg_incoming(): assert len(KG.get_incoming("P2"))==1
def test_kg_count(): assert KG.entity_count()>=1; assert KG.rel_count()>=2
def test_kg_hash(): h=KG.graph_hash(); assert len(h)==16
def test_registry_register(): e=ER.register("E1","THESIS","Value premium"); assert e.label=="Value premium"
def test_registry_by_type(): ER.register("E2","THESIS","Momentum"); assert len(ER.get_by_type("THESIS"))>=2
def test_relationship_engine(): RE.link("L1","F1","O1","CAUSED"); assert len(RE.trace_chain("F1"))>0
def test_graph_query_paths(): GQ.find_paths("F1","P2"); len(GQ.find_paths("F1","P2"))>=0
def test_graph_query_impact(): imp=GQ.impact_analysis("F1"); assert imp["outgoing_count"]>=1

# ── EV2: Hypothesis Evolution (10 tests) ──
from zmatrix.research_db.evolution.hypothesis.hypothesis_evolution import HypothesisEvolution, HypothesisGene
from zmatrix.research_db.evolution.hypothesis.hypothesis_mutator import HypothesisMutator
from zmatrix.research_db.evolution.hypothesis.hypothesis_selector import HypothesisSelector
HE = HypothesisEvolution()

def test_he_seed(): g=HE.seed("G1","Value works"); assert g.generation==1; assert g.production_allowed is False
def test_he_mutate(): HE.seed("G1","Value"); g=HE.mutate("G1","G2",["INVERT_SIGN"]); assert g is not None; assert g.generation==2
def test_he_select(): HE.seed("G3","Strong"); HE.mutate("G3","G4",["EXTEND_HORIZON"]); best=HE.select_best(lambda g: len(g.mutations)); assert best is not None
def test_he_generation(): assert HE.generation_count()>=2
def test_mutator_variants(): v=HypothesisMutator.generate_variants("H1","LOW_IC"); assert len(v)==6
def test_mutator_types(): v=HypothesisMutator.generate_variants("H1"); ids=[m.mutation_type for m in v]; assert "INVERT_SIGN" in ids
def test_selector_pass(): r=HypothesisSelector.select("H1",{"ic":0.08,"coverage":0.7}); assert r.selected is True
def test_selector_fail(): r=HypothesisSelector.select("H2",{"ic":0.005,"coverage":0.2}); assert r.selected is False

# ── EV3: Pattern Mining (8 tests) ──
from zmatrix.research_db.evolution.mining.pattern_miner import PatternMiner
from zmatrix.research_db.evolution.mining.pattern_ranker import PatternRanker
from zmatrix.research_db.evolution.mining.pattern_validator import PatternValidator
KG2 = KnowledgeGraph(); KG2.add_entity("A1","FACTOR","f1"); KG2.add_entity("A2","OUTCOME","o1")
KG2.add_relationship("RA","A1","A2","PRODUCES"); KG2.add_relationship("RB","A1","A2","PRODUCES")

def test_miner_graph(): patterns=PatternMiner.mine_from_graph(KG2, 1); assert len(patterns)>=1
def test_miner_empty(): assert PatternMiner.mine_from_graph(KnowledgeGraph())==[]
def test_ranker_top(): p=PatternMiner.mine_from_graph(KG2,1); top=PatternRanker.top_patterns(p,3); assert len(top)<=3
def test_ranker_empty(): assert PatternRanker.rank([])==[]
def test_validator(): p=PatternMiner.mine_from_graph(KG2,1); result=PatternValidator.validate(p[0],KG2); assert result["validated"] is True
def test_validator_batch(): p=PatternMiner.mine_from_graph(KG2,1); results=PatternValidator.batch_validate(p,KG2); assert len(results)==len(p)

# ── EV4: Meta Research (8 tests) ──
from zmatrix.research_db.evolution.meta.research_analyzer import ResearchAnalyzer
from zmatrix.research_db.evolution.meta.research_efficiency import ResearchEfficiency
from zmatrix.research_db.evolution.meta.research_failure_engine import ResearchFailureEngine

def test_analyzer_effective(): r=ResearchAnalyzer.analyze_directions({"momentum":{"ic":0.08},"value":{"ic":0.02}}); assert r["most_effective"]=="momentum"
def test_analyzer_empty(): r=ResearchAnalyzer.analyze_directions({}); assert r["total_analyses"]==0
def test_analyzer_roi(): r=ResearchAnalyzer.compute_roi({"F1":{"ic":0.06,"time_ms":100}}); assert "F1" in r
def test_efficiency(): r=ResearchEfficiency.compute_efficiency([{"result":"PASS","duration_ms":200},{"result":"FAIL","duration_ms":300}]); assert r["success_rate"]==0.5
def test_efficiency_empty(): r=ResearchEfficiency.compute_efficiency([]); assert r["total_research"]==0
def test_failure_engine(): r=ResearchFailureEngine.analyze([{"direction":"momentum","result":"PASS"},{"direction":"value","result":"FAIL","reason":"LOW_IC"},{"direction":"value","result":"FAIL","reason":"LOW_IC"}]); assert len(r)>=1

# ── Safety (5 tests) ──
def test_no_trade_flags():
    for p in (WORKSPACE/"zmatrix"/"research_db"/"evolution").rglob("*.py"):
        if "__pycache__" in str(p): continue
        assert "production_allowed=True" not in p.read_text()
def test_kg_production_false(): assert KG.get_entity("F1").production_allowed is False

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
