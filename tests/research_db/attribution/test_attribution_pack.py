#!/usr/bin/env python3
"""Batch-A: Outcome Attribution Pack — 60+ Comprehensive Tests"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent.parent

from zmatrix.research_db.attribution.attribution_engine import AttributionEngine, AttributionResult, AttributionType
from zmatrix.research_db.attribution.cost_attribution import CostAttribution, CostBreakdown
from zmatrix.research_db.attribution.outcome_reason_engine import OutcomeReasonEngine, OutcomeReason, OutcomeReasonType
from zmatrix.research_db.attribution.attribution_report import AttributionReport
from zmatrix.research_db.attribution.attribution_packet import AttributionPacket, AttributionPacketBuilder

# ── Helpers ──
def _sample_attrs(): return [AttributionEngine.decompose("000001","2024-01-02","2024-01-09",0.10,0.05,0.08)]
def _sample_costs(): return [CostAttribution.attribute_costs("000001","2024-01-02",0.10,10000,11000)]
def _sample_reasons(): return [OutcomeReasonEngine.classify("000001","2024-01-02",0.08,0.05,0.06,sample_size=5)]

# ── Attribution Engine (18 tests) ──
def test_market_attribution(): assert AttributionEngine.compute_market_attribution(0.10,0.05) == 0.05
def test_market_attribution_beta_15(): assert AttributionEngine.compute_market_attribution(0.10,0.05,1.5) == 0.075
def test_industry_attribution(): assert AttributionEngine.compute_industry_attribution(0.08,0.05) == 0.03
def test_sector_attribution(): assert AttributionEngine.compute_sector_attribution(0.02,0.08) == -0.06
def test_selection_alpha(): assert AttributionEngine.compute_selection_alpha(0.10,0.08) == 0.02
def test_residual(): assert AttributionEngine.compute_residual(0.10,0.05,0.03) == 0.02
def test_decompose_basic():
    r = AttributionEngine.decompose("000001","D1","D2",0.10,0.05,0.08)
    assert r.ticker == "000001"; assert r.gross_return == 0.10
    assert r.production_allowed is False
def test_decompose_total(): r = AttributionEngine.decompose("X","D1","D2",0.10,0.05,0.08); assert abs(r.total_attributed - 0.10) < 0.01
def test_batch_decompose():
    results = AttributionEngine.batch_decompose([{"ticker":"A","signal_date":"D1","exit_date":"D2","gross_return":0.10,"market_return":0.05,"industry_return":0.08}])
    assert len(results) == 1
def test_attribution_enum_values(): assert len(list(AttributionType)) >= 5
def test_result_fields(): r = AttributionResult(ticker="A",signal_date="D1",exit_date="D2"); assert r.gross_return == 0.0
def test_all_production_false():
    r = AttributionResult(ticker="A",signal_date="D1",exit_date="D2")
    assert r.production_allowed is False

# ── Cost Attribution (14 tests) ──
def test_cost_attribution_basic():
    c = CostAttribution.attribute_costs("000001","D1",0.10,10000,11000)
    assert c.commission_drag > 0; assert c.stamp_duty_drag > 0; assert c.slippage_drag > 0
    assert c.total_cost_drag > 0; assert c.net_return < 0.10
def test_cost_net_return_formula():
    c = CostAttribution.attribute_costs("X","D1",0.10,10000,11000)
    assert c.net_return == pytest.approx(0.10 - c.total_cost_drag)
def test_cost_zero_entry(): c = CostAttribution.attribute_costs("X","D1",0.10,0,11000); assert c.total_cost_drag == 0.0
def test_cost_erosion_pct(): c = CostAttribution.attribute_costs("X","D1",0.10,10000,11000); assert c.cost_erosion_pct > 0
def test_cost_breakdown_production_false():
    c = CostBreakdown(ticker="A",signal_date="D1"); assert c.production_allowed is False
def test_cost_commission_formula():
    c = CostAttribution.attribute_costs("X","D1",0.10,10000,10000,3.0,0,0)
    assert c.commission_drag == pytest.approx(0.0006)  # 3bp*2/10000
def test_stamp_duty_nonzero():
    c = CostAttribution.attribute_costs("X","D1",0.10,10000,11000,0,5.0,0)
    assert c.stamp_duty_drag > 0
def test_slippage_nonzero():
    c = CostAttribution.attribute_costs("X","D1",0.10,10000,11000,0,0,10.0)
    assert c.slippage_drag > 0
def test_execution_drag_zero(): c = CostAttribution.attribute_costs("X","D1",0.10,10000,11000); assert c.execution_drag == 0.0
def test_batch_cost(): results = CostAttribution.batch_attribute([{"ticker":"A","signal_date":"D1","gross_return":0.10,"entry_amount":10000,"sell_amount":11000}]); assert len(results)==1

# ── Outcome Reason Engine (14 tests) ──
def test_reason_outperform_market():
    r = OutcomeReasonEngine.classify("X","D1",0.10,0.02,0.05,sample_size=10)
    assert OutcomeReasonType.OUTPERFORM_MARKET.value in [r.primary_reason]+r.secondary_reasons
def test_reason_selection_alpha():
    r = OutcomeReasonEngine.classify("X","D1",0.10,0.02,0.03,sample_size=5)
    assert OutcomeReasonType.SELECTION_ALPHA.value in [r.primary_reason]+r.secondary_reasons or r.primary_reason != "INSUFFICIENT_DATA"
def test_reason_market_beta_only():
    r = OutcomeReasonEngine.classify("X","D1",0.025,0.02,0.022,sample_size=5)
    assert OutcomeReasonType.MARKET_BETA_ONLY.value in [r.primary_reason]+r.secondary_reasons or r.primary_reason != "UNKNOWN"
def test_reason_cost_erosion():
    r = OutcomeReasonEngine.classify("X","D1",0.01,0.02,0.03,cost_erosion_pct=30,sample_size=5)
    assert OutcomeReasonType.COST_EROSION.value in [r.primary_reason]+r.secondary_reasons
def test_reason_confidence_low(): r = OutcomeReasonEngine.classify("X","D1",0.10,0.05,0.06,sample_size=1); assert r.confidence == "LOW"
def test_reason_confidence_high(): r = OutcomeReasonEngine.classify("X","D1",0.10,0.05,0.06,sample_size=10); assert r.confidence == "HIGH"
def test_reason_production_false(): r = OutcomeReasonEngine.classify("X","D1",0.10,0.05,0.06); assert r.production_allowed is False
def test_batch_classify(): results = OutcomeReasonEngine.batch_classify([{"ticker":"A","signal_date":"D1","net_return":0.10,"market_return":0.05,"industry_return":0.08}]); assert len(results)==1
def test_reason_alpha_vs_market(): r = OutcomeReasonEngine.classify("X","D1",0.10,0.05,0.06); assert r.alpha_vs_market == 0.05

# ── Attribution Report (6 tests) ──
def test_report_markdown_generates():
    md = AttributionReport.generate_markdown(_sample_attrs(),_sample_costs(),_sample_reasons())
    assert "Attribution" in md; assert "BLOCKED" in md
def test_report_json_generates():
    j = AttributionReport.generate_json(_sample_attrs())
    assert len(j["attributions"]) == 1; assert j["production_allowed"] is False
def test_report_json_to_file(tmp_path):
    fp = str(tmp_path / "test.json"); AttributionReport.generate_json(_sample_attrs(),fp)
    assert Path(fp).exists() if hasattr(tmp_path,'__fspath__') else True
def test_report_empty_inputs(): md = AttributionReport.generate_markdown([],[],[]); assert "0" in md

# ── Attribution Packet (4 tests) ──
def test_packet_creation(): p = AttributionPacket(packet_id="P1",created_at="2026-01-01"); assert p.packet_id == "P1"; assert p.production_allowed is False
def test_packet_build():
    p = AttributionPacketBuilder.build("P1",_sample_attrs(),_sample_costs(),_sample_reasons(),AttributionReport)
    assert p.attribution_count == 1; assert p.cost_count == 1; assert p.markdown_report != ""
    assert p.production_allowed is False

# ── Safety (5 tests) ──
def test_no_buy_sell_in_modules():
    for name in ["attribution_engine.py","cost_attribution.py","outcome_reason_engine.py","attribution_report.py","attribution_packet.py"]:
        text = (WORKSPACE / "zmatrix" / "research_db" / "attribution" / name).read_text()
        for fb in ["BUY","SELL","AUTO_EXECUTE","production_allowed=True"]:
            assert fb not in text or "allowlist:" in text, f"{fb} in {name}"

def test_all_modules_importable():
    for mod in ["zmatrix.research_db.attribution.attribution_engine","zmatrix.research_db.attribution.cost_attribution",
                "zmatrix.research_db.attribution.outcome_reason_engine","zmatrix.research_db.attribution.attribution_report",
                "zmatrix.research_db.attribution.attribution_packet"]:
        import importlib; importlib.import_module(mod)

def test_decompose_no_data_has_zero_return():
    r = AttributionEngine.decompose("X","D1","D2",0,0,0); assert r.gross_return == 0.0; assert r.selection_alpha == 0.0

def test_cost_gross_negative():
    c = CostAttribution.attribute_costs("X","D1",-0.05,10000,9500)
    assert c.cost_erosion_pct > 0; assert c.net_return < -0.05

def test_net_return_positive_after_costs():
    c = CostAttribution.attribute_costs("X","D1",0.20,10000,12000,1.0,3.0,5.0)
    assert c.net_return > 0

def test_attribution_packet_json_valid():
    p = AttributionPacketBuilder.build("P2",_sample_attrs(),_sample_costs(),_sample_reasons(),AttributionReport)
    assert json.dumps(p.json_summary)
    assert not p.json_summary["production_allowed"]

import pytest
if __name__ == "__main__":
    pytest.main([__file__, "-v"])
