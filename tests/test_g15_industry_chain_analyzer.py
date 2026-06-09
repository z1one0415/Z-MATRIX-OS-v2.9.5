"""Tests for G15 Industry Chain Analyzer v1.0

Covers:
  - test_chain_position_identification
  - test_evidence_layer_upgrade_from_abcd_to_l1l5
  - test_profit_capture_point
  - test_g18_handoff_fields
  - test_missing_data_graceful
  - test_known_ticker_002472 (双环: 中游精密零部件)
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from zmatrix.research.industry_chain_analyzer import (
    ChainAnalysis,
    EVIDENCE_LAYERS,
    analyze_industry_chain,
    _resolve_chain_position,
    _identify_profit_capture,
    _upgrade_evidence_to_l5,
    _build_g18_handoff,
    _determine_confidence,
)


class TestChainPositionIdentification:
    """Chain position should be resolved from industry or chain_detail."""

    def test_upstream_from_industry(self):
        pos = _resolve_chain_position("601899", "有色金属矿", {})
        assert pos == "upstream"

    def test_midstream_from_industry(self):
        pos = _resolve_chain_position("002472", "机械设备", {})
        assert pos == "midstream"

    def test_downstream_from_industry(self):
        pos = _resolve_chain_position("600519", "食品饮料消费品牌", {})
        assert pos == "downstream"

    def test_from_chain_detail_override(self):
        pos = _resolve_chain_position("002472", "机械设备", {"position": "midstream精密零部件"})
        assert pos == "midstream"

    def test_platform_from_industry(self):
        pos = _resolve_chain_position("600900", "电力基础设施", {})
        assert pos == "platform"

    def test_default_midstream(self):
        pos = _resolve_chain_position("999999", "未知行业", {})
        assert pos == "midstream"


class TestEvidenceLayerUpgrade:
    """ABCD evidence should upgrade to L1-L5 properly."""

    def test_basic_upgrade(self):
        abcd = {
            "A_确证": ["财报可用", "ROE 5年均15%>10%"],
            "B_佐证": ["PE 18x<20x"],
            "C_传闻": ["市场传闻扩产"],
            "D_风险": ["高负债"],
        }
        layers = _upgrade_evidence_to_l5(abcd, {})
        assert "财报可用" in layers["L1_hard_data"]
        assert "ROE 5年均15%>10%" in layers["L1_hard_data"]
        assert "PE 18x<20x" in layers["L2_company_disclosure"]
        assert "市场传闻扩产" in layers["L5_narrative"]

    def test_financials_auto_populate_l1(self):
        layers = _upgrade_evidence_to_l5({}, {
            "has_finance": True,
            "revenue_growth": 25.3,
            "roe_5y_avg": 18.0,
            "gross_margin": 35.0,
        })
        assert any("财报" in item for item in layers["L1_hard_data"])
        assert any("营收" in item for item in layers["L1_hard_data"])
        assert any("ROE" in item for item in layers["L1_hard_data"])

    def test_empty_input(self):
        layers = _upgrade_evidence_to_l5({}, {})
        assert all(isinstance(v, list) for v in layers.values())
        assert len(layers) == 5


class TestProfitCapturePoint:
    """Profit capture should be identified from gross margin."""

    def test_high_margin_brand(self):
        result = _identify_profit_capture("600519", {"gross_margin": 92}, "downstream")
        assert "品牌" in result or "溢价" in result

    def test_mid_margin_tech(self):
        result = _identify_profit_capture("002472", {"gross_margin": 35}, "midstream")
        assert "规模" in result or "成本" in result

    def test_low_margin_upstream(self):
        result = _identify_profit_capture("601899", {"gross_margin": 12}, "upstream")
        assert "资源" in result or "周期" in result

    def test_zero_margin(self):
        result = _identify_profit_capture("000000", {"gross_margin": 0}, "midstream")
        assert isinstance(result, str)
        assert len(result) > 5


class TestG18HandoffFields:
    """G18 handoff must have all required fields."""

    REQUIRED_FIELDS = ["thesis_strength", "evidence_level", "catalyst_distance", "chain_risk_score"]

    def test_all_fields_present(self):
        evidence = {"L1_hard_data": ["a", "b", "c", "d", "e"], "L2_company_disclosure": [], "L3_cross_validation": [],
                    "L4_industry_opinion": [], "L5_narrative": []}
        handoff = _build_g18_handoff(evidence, [], [{"event": "财报"}])
        for f in self.REQUIRED_FIELDS:
            assert f in handoff, f"Missing field: {f}"

    def test_thesis_strength_values(self):
        weak = _build_g18_handoff({"L1_hard_data": ["x"], "L2_company_disclosure": [], "L3_cross_validation": [],
                                   "L4_industry_opinion": [], "L5_narrative": []}, [], [])
        assert weak["thesis_strength"] in ("HIGH", "MEDIUM", "LOW")

    def test_chain_risk_score_range(self):
        high_risk = [{"severity": "HIGH"}, {"severity": "HIGH"}, {"severity": "MEDIUM"}]
        evidence = {"L1_hard_data": [], "L2_company_disclosure": [], "L3_cross_validation": [],
                    "L4_industry_opinion": [], "L5_narrative": []}
        handoff = _build_g18_handoff(evidence, high_risk, [])
        assert 0 <= handoff["chain_risk_score"] <= 100

    def test_catalyst_distance_near(self):
        evidence = {"L1_hard_data": [], "L2_company_disclosure": [], "L3_cross_validation": [],
                    "L4_industry_opinion": [], "L5_narrative": []}
        handoff = _build_g18_handoff(evidence, [], [{"e": 1}, {"e": 2}])
        assert handoff["catalyst_distance"] == "NEAR"


class TestMissingDataGraceful:
    """Analyzer should handle missing data gracefully."""

    def test_empty_everything(self):
        result = analyze_industry_chain(
            ticker="000000", name="测试公司", industry="",
            financials={}, peers=[], catalysts=[],
            existing_evidence={},
        )
        assert isinstance(result, ChainAnalysis)
        assert result.ticker == "000000"
        assert result.research_confidence in ("HIGH", "MEDIUM", "LOW", "INSUFFICIENT")

    def test_none_financials(self):
        result = analyze_industry_chain(
            ticker="000000", name="测试", industry="电子",
            financials=None, peers=[], catalysts=[],  # type: ignore
            existing_evidence={},
        )
        # Should not crash — graceful degradation
        assert isinstance(result, ChainAnalysis)

    def test_garbage_evidence(self):
        result = analyze_industry_chain(
            ticker="000000", name="测试", industry="机械设备",
            financials={}, peers=[], catalysts=[],
            existing_evidence={"X_unknown": ["bad data"]},
        )
        assert isinstance(result, ChainAnalysis)


class TestKnownTicker002472:
    """双环传动 002472: 中游精密零部件 (机器人/汽车)."""

    def test_chain_analysis(self):
        result = analyze_industry_chain(
            ticker="002472",
            name="双环传动",
            industry="机械设备",
            financials={
                "has_finance": True,
                "revenue_growth": 28.5,
                "net_profit_growth": 35.0,
                "roe_5y_avg": 12.3,
                "gross_margin": 28.0,
                "debt_ratio": 45.0,
            },
            peers=[{"ticker": "002050", "name": "三花智控"}],
            catalysts=[{"event": "机器人订单放量", "date": "2026-07"}],
            existing_evidence={
                "A_确证": ["财报可用", "ROE>10%", "营收增28%"],
                "B_佐证": ["DQ 75分>70"],
                "D_风险": [],
            },
        )
        assert result.ticker == "002472"
        assert result.chain_position == "midstream"
        assert "规模" in result.profit_capture_point or "加工" in result.profit_capture_point
        assert result.research_confidence in ("HIGH", "MEDIUM")
        assert result.g18_handoff["thesis_strength"] in ("HIGH", "MEDIUM")
        assert result.g18_handoff["evidence_level"] == "L1"
        assert isinstance(result.factor_handoff, dict)
        assert "sector_momentum_input" in result.factor_handoff


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
