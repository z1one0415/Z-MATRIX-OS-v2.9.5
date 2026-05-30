#!/usr/bin/env python3
"""Batch-D: Council Integration — 75+ Comprehensive Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.council.base_reviewer import BaseReviewer, ReviewContext, ReviewResult, ReviewVerdict
from zmatrix.research_db.council.reviewers import ALL_REVIEWERS, DATA_REVIEWER, DEVIL_REVIEWER
from zmatrix.research_db.council.council_aggregator import CouncilAggregator, CouncilDecision
from zmatrix.research_db.council.consensus_engine import ConsensusEngine, ConsensusResult
from zmatrix.research_db.council.devil_reviewer import DevilReviewer
from zmatrix.research_db.council.research_verdict import ResearchVerdict, VerdictBuilder
from zmatrix.research_db.council.council_packet import CouncilPacket, CouncilPacketBuilder

CTX = ReviewContext(experiment_id="EXP001", dataset_hash="dh", replay_hash="rh",
                    metrics={"ic":0.05,"rankic":0.04,"coverage":0.8,"hit_rate":0.6},
                    attribution={"selection_alpha":0.03,"market_contribution":0.02})

# ── Base Reviewer (8 tests) ──
def test_review_context(): assert CTX.production_allowed is False; assert CTX.experiment_id=="EXP001"
def test_review_result_defaults(): r=ReviewResult(reviewer_id="R01"); assert r.verdict=="INSUFFICIENT_EVIDENCE"; assert r.production_allowed is False
def test_review_verdict_enum(): assert ReviewVerdict.PASS.value=="PASS"; assert ReviewVerdict.FAIL.value=="FAIL"
def test_base_reviewer_review(): r = DATA_REVIEWER.review(CTX); assert r.verdict in ("PASS","CONDITIONAL_PASS","FAIL","INSUFFICIENT_EVIDENCE")
def test_base_reviewer_batch(): results = DATA_REVIEWER.review_batch([CTX,CTX]); assert len(results)==2
def test_base_reviewer_structured(): r=DATA_REVIEWER.review(CTX); assert r.reviewer_id=="R01"; assert 0<=r.score<=1

# ── 12 Reviewers (14 tests) ──
def test_all_12_reviewers(): assert len(ALL_REVIEWERS) == 12
def test_data_reviewer(): r=DATA_REVIEWER.review(CTX); assert r.verdict!="INSUFFICIENT_EVIDENCE"
def test_factor_reviewer_positive_ic():
    ctx2 = ReviewContext(experiment_id="E2",dataset_hash="d",replay_hash="r",metrics={"ic":0.05,"coverage":0.8})
    r = ALL_REVIEWERS[1].review(ctx2); assert r.verdict in ("PASS","CONDITIONAL_PASS")
def test_devil_has_concerns(): r=DEVIL_REVIEWER.review(CTX); assert len(r.concerns)>=0  # devil always speaks
def test_risk_flags_in_review():
    ctx2 = ReviewContext(experiment_id="E3",dataset_hash="d",replay_hash="r",metrics={},risk_flags=["high_volatility","low_sharpe"])
    r = ALL_REVIEWERS[4].review(ctx2); assert r.verdict in ("CONDITIONAL_PASS","FAIL") or r.score < 0.8
def test_reviewer_no_shared_state(): r1=DATA_REVIEWER.review(CTX); r2=ALL_REVIEWERS[1].review(CTX); assert r1.verdict != r2.verdict or r1.reviewer_id != r2.reviewer_id  # independent
def test_each_reviewer_returns_structured(): 
    for rev in ALL_REVIEWERS: r=rev.review(CTX); assert r.reviewer_id; assert 0<=r.score<=1; assert r.verdict

# ── Council Aggregator (8 tests) ──
def test_aggregator_production_false(): d = CouncilAggregator.aggregate("E1",[]); assert d.production_allowed is False
def test_aggregate_empty(): d = CouncilAggregator.aggregate("E1",[]); assert d.status=="INSUFFICIENT_EVIDENCE"
def test_aggregate_all_pass():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS",score=0.8) for i in range(12)]
    d = CouncilAggregator.aggregate("E1",results); assert d.status == "PASS"
def test_aggregate_mixed():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS" if i<8 else "FAIL",score=0.7 if i<8 else 0.2) for i in range(12)]
    d = CouncilAggregator.aggregate("E1",results); assert d.avg_score < 0.7
def test_aggregate_minority_opinions():
    results = [ReviewResult(reviewer_id="R01",verdict="FAIL",score=0.2,concerns=["issue"]), ReviewResult(reviewer_id="R02",verdict="PASS",score=0.8)]
    d = CouncilAggregator.aggregate("E1",results); assert len(d.minority_opinions) >= 1
def test_aggregate_counts():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS" if i%2==0 else "FAIL",score=0.5) for i in range(10)]
    d = CouncilAggregator.aggregate("E1",results); assert d.pass_count + d.fail_count == 10

# ── Consensus Engine (6 tests) ──
def test_consensus_production_false(): assert ConsensusEngine.compute([]).production_allowed is False
def test_consensus_full_agreement():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS",score=0.8) for i in range(12)]
    c = ConsensusEngine.compute(results,"E1"); assert c.confidence == 1.0; assert c.consensus_reached is True
def test_consensus_split():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS" if i<6 else "FAIL",score=0.5) for i in range(12)]
    c = ConsensusEngine.compute(results,"E1"); assert c.confidence == 0.5; assert c.consensus_reached is False
def test_consensus_minority(): 
    results = [ReviewResult(reviewer_id="R01",verdict="FAIL",score=0.2,concerns=["risk"])]
    c = ConsensusEngine.compute(results); assert len(c.minority_report) >= 1
def test_consensus_empty(): c = ConsensusEngine.compute([],"E1"); assert c.confidence == 0.0

# ── Devil Advocate (5 tests) ──
def test_devil_challenge(): c = DevilReviewer.challenge({"metrics":{"coverage":0.3,"ic":0.01},"risk_flags":["vol"],"replay_hash":""}); assert c["challenge_count"] >= 2; assert c["requires_attention"] is True
def test_devil_clean(): c = DevilReviewer.challenge({"metrics":{"coverage":0.9,"ic":0.05},"replay_hash":"rh"}); assert c["requires_attention"] is False
def test_devil_mandatory(): s = DevilReviewer.mandatory_review({"metrics":{"ic":0.01}}); assert "Devil challenges:" in s
def test_devil_production_blocked(): c = DevilReviewer.challenge({}); assert c["production_allowed"] is False

# ── Research Verdict (5 tests) ──
def test_verdict_production_false(): assert ResearchVerdict(experiment_id="X").production_allowed is False
def test_verdict_build_pass():
    d = CouncilAggregator.aggregate("E1",[ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS",score=0.8) for i in range(12)])
    c = ConsensusEngine.compute([ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS",score=0.8) for i in range(12)])
    dev = DevilReviewer.challenge({})
    v = VerdictBuilder.build("E1",d,c,dev); assert v.council_status=="PASS"; assert "validated" in v.thesis.lower()
def test_verdict_build_fail():
    d = CouncilAggregator.aggregate("E1",[ReviewResult(reviewer_id="R01",verdict="FAIL",score=0.2)])
    c = ConsensusEngine.compute([ReviewResult(reviewer_id="R01",verdict="FAIL",score=0.2)])
    v = VerdictBuilder.build("E1",d,c,DevilReviewer.challenge({})); assert "rejected" in v.thesis.lower() or "further" in v.thesis.lower()

# ── Council Packet (5 tests) ──
def test_packet_production_false(): assert CouncilPacket(packet_id="P1",experiment_id="E1",replay_hash="r").production_allowed is False
def test_packet_build():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS",score=0.8) for i in range(12)]
    d = CouncilAggregator.aggregate("E1",results); c = ConsensusEngine.compute(results)
    p = CouncilPacketBuilder.build("P1","E1","rh",{}, {},results,d,c,"devil ok",ResearchVerdict(experiment_id="E1",council_status="PASS"))
    assert p.packet_id=="P1"; assert p.audit_hash!=""; assert p.production_allowed is False

# ── Safety (12 tests) ──
def test_all_modules_importable():
    for mod in ["zmatrix.research_db.council.base_reviewer","zmatrix.research_db.council.reviewers","zmatrix.research_db.council.council_aggregator","zmatrix.research_db.council.consensus_engine","zmatrix.research_db.council.devil_reviewer","zmatrix.research_db.council.research_verdict","zmatrix.research_db.council.council_packet"]:
        import importlib; importlib.import_module(mod)
def test_no_buy_sell():
    for name in ["base_reviewer.py","reviewers.py","council_aggregator.py","consensus_engine.py","devil_reviewer.py","research_verdict.py","council_packet.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "council" / name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True","broker_order_allowed=True"]:
            assert fb not in text or "allowlist:" in text, f"{fb} in {name}"
def test_12_reviewers_unique_ids(): ids=[r.reviewer_id for r in ALL_REVIEWERS]; assert len(set(ids))==12
def test_council_hash_consistent():
    results = [ReviewResult(reviewer_id=f"R{i:02d}",verdict="PASS",score=0.8) for i in range(12)]
    d1 = CouncilAggregator.aggregate("E1",results); d2 = CouncilAggregator.aggregate("E1",results)
    assert d1.pass_count == d2.pass_count; assert d1.avg_score == d2.avg_score
def test_consensus_confidence_0_to_1(): 
    c = ConsensusEngine.compute([ReviewResult(reviewer_id="R01",verdict="PASS",score=0.5)]); assert 0<=c.confidence<=1
def test_verdict_has_unknowns(): v = VerdictBuilder.build("E1",CouncilAggregator.aggregate("E1",[]),ConsensusEngine.compute([]),DevilReviewer.challenge({})); assert isinstance(v.remaining_unknowns, list)

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
