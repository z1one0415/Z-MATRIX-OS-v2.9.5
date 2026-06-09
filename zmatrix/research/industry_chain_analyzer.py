"""☯️ G15 Industry Chain Deep Research — Analyzer v1.0

Transforms shallow A/B/C/D evidence into proper L1-L5 layered analysis
with chain topology, profit capture, and risk assessment.

Evidence Layers:
  L1 — Hard data: financials, orders, prices, capacity utilization
  L2 — Company disclosure: investor meetings, management guidance
  L3 — Cross validation: upstream/downstream confirmation
  L4 — Industry opinion: broker reports, expert views
  L5 — Narrative: market rumor, unverified themes

签章: ☯️ Z2天师 Hermes Research Kernel | Z-MATRIX-OS v2.9.5
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

# ═══ Path Constants ═══
_WORKSPACE = Path(__file__).resolve().parent.parent.parent

# ═══ Evidence Layer Definitions ═══
EVIDENCE_LAYERS = {
    "L1_hard_data": "财报、公告、订单、价格、库存、产能利用率",
    "L2_company_disclosure": "投资者交流、管理层指引、公司战略",
    "L3_cross_validation": "上下游交叉验证、客户/供应商确认",
    "L4_industry_opinion": "券商报告、行业媒体、专家观点",
    "L5_narrative": "市场传闻、题材炒作、未验证叙事",
}

# ═══ Chain Position Taxonomy ═══
CHAIN_POSITIONS = {
    "upstream": "上游原材料/核心零部件供应",
    "midstream": "中游制造/集成/加工",
    "downstream": "下游应用/终端/品牌",
    "platform": "平台/生态/基础设施",
}

# ═══ ABCD → L1-L5 Mapping ═══
_ABCD_TO_L_MAP = {
    "A_确证": "L1_hard_data",
    "B_佐证": "L2_company_disclosure",
    "C_传闻": "L5_narrative",
    "D_风险": "L1_hard_data",  # risk is hard data when from financials
}


@dataclass
class ChainAnalysis:
    """Complete industry chain analysis result."""
    ticker: str
    chain_position: str  # upstream/midstream/downstream/platform
    profit_capture_point: str
    upstream_dependencies: list[dict] = field(default_factory=list)
    downstream_demand: list[dict] = field(default_factory=list)
    evidence_layers: dict = field(default_factory=dict)  # L1-L5
    chain_risks: list[dict] = field(default_factory=list)
    bottleneck_status: str = "UNKNOWN"
    substitution_risk: str = "UNKNOWN"
    research_confidence: str = "INSUFFICIENT"  # HIGH/MEDIUM/LOW/INSUFFICIENT
    g18_handoff: dict = field(default_factory=dict)
    factor_handoff: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        """Serialize to dictionary."""
        return {
            "ticker": self.ticker,
            "chain_position": self.chain_position,
            "profit_capture_point": self.profit_capture_point,
            "upstream_dependencies": self.upstream_dependencies,
            "downstream_demand": self.downstream_demand,
            "evidence_layers": self.evidence_layers,
            "chain_risks": self.chain_risks,
            "bottleneck_status": self.bottleneck_status,
            "substitution_risk": self.substitution_risk,
            "research_confidence": self.research_confidence,
            "g18_handoff": self.g18_handoff,
            "factor_handoff": self.factor_handoff,
        }


# ═══════════════════════════════════════════════════════
# Chain Topology Resolution
# ═══════════════════════════════════════════════════════

def _resolve_chain_position(ticker: str, industry: str, chain_detail: dict) -> str:
    """Determine chain position from chain_taxonomy_provider or heuristics."""
    # If chain_taxonomy_provider gave us a position, use it
    if chain_detail.get("position"):
        pos = chain_detail["position"].lower()
        for key in CHAIN_POSITIONS:
            if key in pos:
                return key

    # Heuristic based on industry keywords
    upstream_keywords = ["材料", "矿", "原料", "资源", "化工原料", "稀土"]
    midstream_keywords = ["制造", "设备", "零部件", "加工", "精密", "机械", "电子"]
    downstream_keywords = ["应用", "终端", "消费", "品牌", "服务", "零售"]
    platform_keywords = ["平台", "云", "生态", "基础设施", "电力", "通信"]

    ind = industry or ""
    if any(k in ind for k in upstream_keywords):
        return "upstream"
    if any(k in ind for k in midstream_keywords):
        return "midstream"
    if any(k in ind for k in downstream_keywords):
        return "downstream"
    if any(k in ind for k in platform_keywords):
        return "platform"

    return "midstream"  # default for manufacturing


def _identify_profit_capture(ticker: str, financials: dict, chain_position: str) -> str:
    """Identify where this company captures profit in the chain."""
    gross_margin = financials.get("gross_margin", 0) or 0
    roe = financials.get("roe_5y_avg", financials.get("roe", 0)) or 0

    if gross_margin > 60:
        return "品牌/技术溢价 (高毛利>60%)"
    elif gross_margin > 40:
        return "技术壁垒/产品差异化 (毛利40-60%)"
    elif gross_margin > 25:
        return "规模效应/成本优势 (毛利25-40%)"
    elif gross_margin > 15:
        return "加工制造/集成服务 (毛利15-25%)"
    else:
        if chain_position == "upstream":
            return "资源禀赋/周期波动 (低毛利上游)"
        return "薄利多销/渠道能力 (低毛利)"


def _build_upstream_dependencies(ticker: str, industry: str, chain_detail: dict) -> list[dict]:
    """Build upstream dependency map."""
    deps = []
    # From chain_taxonomy if available
    upstream = chain_detail.get("upstream", chain_detail.get("suppliers", []))
    if isinstance(upstream, list):
        for item in upstream[:5]:
            if isinstance(item, str):
                deps.append({"name": item, "criticality": "MEDIUM", "substitutable": True})
            elif isinstance(item, dict):
                deps.append({
                    "name": item.get("name", "?"),
                    "criticality": item.get("criticality", "MEDIUM"),
                    "substitutable": item.get("substitutable", True),
                })

    # Heuristic fallback
    if not deps:
        if "机械" in (industry or "") or "设备" in (industry or ""):
            deps = [
                {"name": "钢材/铝材", "criticality": "LOW", "substitutable": True},
                {"name": "电子元器件", "criticality": "MEDIUM", "substitutable": True},
                {"name": "精密轴承/减速器", "criticality": "HIGH", "substitutable": False},
            ]
        elif "电子" in (industry or ""):
            deps = [
                {"name": "晶圆代工", "criticality": "HIGH", "substitutable": False},
                {"name": "封装基板", "criticality": "MEDIUM", "substitutable": True},
            ]

    return deps


def _build_downstream_demand(ticker: str, industry: str, chain_detail: dict) -> list[dict]:
    """Build downstream demand map."""
    demand = []
    downstream = chain_detail.get("downstream", chain_detail.get("customers", []))
    if isinstance(downstream, list):
        for item in downstream[:5]:
            if isinstance(item, str):
                demand.append({"segment": item, "growth": "STABLE", "concentration": "MEDIUM"})
            elif isinstance(item, dict):
                demand.append({
                    "segment": item.get("segment", item.get("name", "?")),
                    "growth": item.get("growth", "STABLE"),
                    "concentration": item.get("concentration", "MEDIUM"),
                })

    if not demand:
        if "机械" in (industry or ""):
            demand = [
                {"segment": "新能源汽车", "growth": "HIGH", "concentration": "LOW"},
                {"segment": "机器人/自动化", "growth": "HIGH", "concentration": "LOW"},
                {"segment": "传统工业", "growth": "STABLE", "concentration": "MEDIUM"},
            ]

    return demand


# ═══════════════════════════════════════════════════════
# Evidence Layer Upgrade (ABCD → L1-L5)
# ═══════════════════════════════════════════════════════

def _upgrade_evidence_to_l5(existing_evidence: dict, financials: dict) -> dict:
    """Convert A/B/C/D evidence to L1-L5 hierarchy."""
    layers = {
        "L1_hard_data": [],
        "L2_company_disclosure": [],
        "L3_cross_validation": [],
        "L4_industry_opinion": [],
        "L5_narrative": [],
    }

    # Map existing ABCD evidence
    for level, items in existing_evidence.items():
        target_layer = _ABCD_TO_L_MAP.get(level, "L5_narrative")
        if isinstance(items, list):
            for item in items:
                layers[target_layer].append(item)

    # Auto-populate L1 from financials
    if financials:
        if financials.get("has_finance"):
            layers["L1_hard_data"].append("财报数据完整可用")
        if financials.get("revenue_growth"):
            rg = financials["revenue_growth"]
            layers["L1_hard_data"].append(f"营收增速 {rg:.1f}%")
        if financials.get("net_profit_growth"):
            ng = financials["net_profit_growth"]
            layers["L1_hard_data"].append(f"净利增速 {ng:.1f}%")
        if financials.get("roe_5y_avg"):
            layers["L1_hard_data"].append(f"5年ROE均值 {financials['roe_5y_avg']:.1f}%")
        if financials.get("gross_margin"):
            layers["L1_hard_data"].append(f"毛利率 {financials['gross_margin']:.1f}%")
        if financials.get("debt_ratio") and financials["debt_ratio"] > 60:
            layers["L1_hard_data"].append(f"⚠️ 负债率 {financials['debt_ratio']:.1f}%>60%")

    return layers


def _assess_chain_risks(chain_position: str, upstream_deps: list, financials: dict) -> list[dict]:
    """Assess chain-specific risks."""
    risks = []

    # Upstream concentration risk
    critical_deps = [d for d in upstream_deps if d.get("criticality") == "HIGH"]
    if critical_deps:
        non_sub = [d for d in critical_deps if not d.get("substitutable", True)]
        if non_sub:
            risks.append({
                "type": "供应链瓶颈",
                "severity": "HIGH",
                "detail": f"{len(non_sub)}个不可替代核心供应商",
            })

    # Financial risks
    if financials:
        debt = financials.get("debt_ratio", 0) or 0
        if debt > 70:
            risks.append({"type": "财务杠杆", "severity": "HIGH", "detail": f"负债率{debt:.0f}%"})
        elif debt > 50:
            risks.append({"type": "财务杠杆", "severity": "MEDIUM", "detail": f"负债率{debt:.0f}%"})

        fcf = financials.get("free_cash_flow", None)
        if fcf is not None and fcf < 0:
            risks.append({"type": "现金流紧张", "severity": "MEDIUM", "detail": "自由现金流为负"})

    # Position-specific risks
    if chain_position == "upstream":
        risks.append({"type": "周期波动", "severity": "MEDIUM", "detail": "上游资源受大宗商品周期影响"})
    elif chain_position == "midstream":
        risks.append({"type": "两端挤压", "severity": "LOW", "detail": "中游受上游成本+下游议价双重压力"})

    return risks


def _determine_confidence(evidence_layers: dict) -> str:
    """Determine research confidence from evidence layers."""
    l1_count = len(evidence_layers.get("L1_hard_data", []))
    l2_count = len(evidence_layers.get("L2_company_disclosure", []))
    l3_count = len(evidence_layers.get("L3_cross_validation", []))

    total_hard = l1_count + l2_count + l3_count
    if total_hard >= 8:
        return "HIGH"
    elif total_hard >= 4:
        return "MEDIUM"
    elif total_hard >= 2:
        return "LOW"
    return "INSUFFICIENT"


# ═══════════════════════════════════════════════════════
# G18 / Factor Library Handoff
# ═══════════════════════════════════════════════════════

def _build_g18_handoff(evidence_layers: dict, chain_risks: list, catalysts: list) -> dict:
    """Build G18 handoff fields for downstream consumption."""
    confidence = _determine_confidence(evidence_layers)

    # Thesis strength from evidence depth
    l1_count = len(evidence_layers.get("L1_hard_data", []))
    if l1_count >= 5:
        thesis_strength = "HIGH"
    elif l1_count >= 3:
        thesis_strength = "MEDIUM"
    else:
        thesis_strength = "LOW"

    # Highest evidence level achieved
    for level in ["L1_hard_data", "L2_company_disclosure", "L3_cross_validation",
                  "L4_industry_opinion", "L5_narrative"]:
        if evidence_layers.get(level):
            evidence_level = level.split("_")[0]  # "L1", "L2", etc.
            break
    else:
        evidence_level = "L5"

    # Catalyst distance
    catalyst_distance = "FAR"
    if catalysts:
        catalyst_distance = "NEAR" if len(catalysts) >= 2 else "MID"

    # Chain risk score (0-100)
    high_risks = sum(1 for r in chain_risks if r.get("severity") == "HIGH")
    med_risks = sum(1 for r in chain_risks if r.get("severity") == "MEDIUM")
    chain_risk_score = min(100, high_risks * 30 + med_risks * 15)

    return {
        "thesis_strength": thesis_strength,
        "evidence_level": evidence_level,
        "catalyst_distance": catalyst_distance,
        "chain_risk_score": chain_risk_score,
    }


def _build_factor_handoff(evidence_layers: dict, chain_position: str, financials: dict) -> dict:
    """Build factor library handoff fields."""
    has_l1 = bool(evidence_layers.get("L1_hard_data"))
    has_growth = bool(financials.get("revenue_growth") or financials.get("net_profit_growth"))

    return {
        "sector_momentum_input": chain_position in ("midstream", "downstream"),
        "fundamental_quality_input": has_l1 and has_growth,
        "theme_strength_input": bool(evidence_layers.get("L5_narrative")),
    }


# ═══════════════════════════════════════════════════════
# Main Entry Point
# ═══════════════════════════════════════════════════════

def analyze_industry_chain(
    ticker: str,
    name: str,
    industry: str,
    financials: dict,
    peers: list,
    catalysts: list,
    existing_evidence: dict,
    chain_detail: Optional[dict] = None,
) -> ChainAnalysis:
    """Full industry chain analysis from available data.

    Args:
        ticker: Stock code (e.g. "002472")
        name: Company name
        industry: Industry classification
        financials: Financial data dict
        peers: List of peer companies
        catalysts: List of upcoming catalysts
        existing_evidence: Existing A/B/C/D evidence dict
        chain_detail: Output from chain_taxonomy_provider (optional)

    Returns:
        ChainAnalysis dataclass with complete analysis
    """
    try:
        chain_detail = chain_detail or {}

        # 1. Chain position
        chain_position = _resolve_chain_position(ticker, industry, chain_detail)

        # 2. Profit capture
        profit_capture = _identify_profit_capture(ticker, financials, chain_position)

        # 3. Upstream/downstream topology
        upstream_deps = _build_upstream_dependencies(ticker, industry, chain_detail)
        downstream_demand = _build_downstream_demand(ticker, industry, chain_detail)

        # 4. Evidence upgrade (ABCD → L1-L5)
        evidence_layers = _upgrade_evidence_to_l5(existing_evidence, financials)

        # 5. Chain risks
        chain_risks = _assess_chain_risks(chain_position, upstream_deps, financials)

        # 6. Bottleneck & substitution assessment
        critical_non_sub = [d for d in upstream_deps
                           if d.get("criticality") == "HIGH" and not d.get("substitutable", True)]
        bottleneck_status = "BOTTLENECK" if critical_non_sub else "CLEAR"

        has_high_margin = (financials.get("gross_margin", 0) or 0) > 30
        substitution_risk = "LOW" if has_high_margin else "MEDIUM"
        if chain_position == "upstream" and not has_high_margin:
            substitution_risk = "HIGH"

        # 7. Research confidence
        research_confidence = _determine_confidence(evidence_layers)

        # 8. G18 handoff
        g18_handoff = _build_g18_handoff(evidence_layers, chain_risks, catalysts)

        # 9. Factor handoff
        factor_handoff = _build_factor_handoff(evidence_layers, chain_position, financials)

        return ChainAnalysis(
            ticker=ticker,
            chain_position=chain_position,
            profit_capture_point=profit_capture,
            upstream_dependencies=upstream_deps,
            downstream_demand=downstream_demand,
            evidence_layers=evidence_layers,
            chain_risks=chain_risks,
            bottleneck_status=bottleneck_status,
            substitution_risk=substitution_risk,
            research_confidence=research_confidence,
            g18_handoff=g18_handoff,
            factor_handoff=factor_handoff,
        )

    except Exception as e:
        # Graceful degradation: return minimal analysis on failure
        return ChainAnalysis(
            ticker=ticker,
            chain_position="UNKNOWN",
            profit_capture_point=f"分析失败: {e}",
            research_confidence="INSUFFICIENT",
            g18_handoff={"thesis_strength": "LOW", "evidence_level": "L5",
                        "catalyst_distance": "FAR", "chain_risk_score": 50},
            factor_handoff={"sector_momentum_input": False,
                           "fundamental_quality_input": False,
                           "theme_strength_input": False},
        )
