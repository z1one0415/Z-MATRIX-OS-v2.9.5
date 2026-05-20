"""
B-Matrix V2.0 — 底仓评分矩阵
────────────────────────────
核心哲学: "不死的压舱石 + 持续生息"
角色定位: 角色化评分层 + 纪律约束输入，非交易决策引擎
投资周期: 3-5年

V2.0 升级:
  ✅ Q-质量陷阱防线: 经营现金流/分红来源/应收存货商誉/监管风险
  ✅ 多角色输出: 一个标的可同时是底仓+轮动
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class BMatrixResult:
    code: str; name: str; total_score: float; grade: str
    stability_score: float; dividend_score: float; valuation_score: float
    moat_score: float; perpetuity_score: float
    roe_5y_avg: float; debt_ratio: float; dividend_yield: float
    pe_current: float; pb_current: float; roe_current: float
    pb_roe_ok: bool; valuation_trap_warning: str
    quality_penalty: float = 0
    quality_warnings: list[str] = field(default_factory=list)
    cashflow_ok: bool = True
    recommendation: str = ""; stop_loss: float = 0


class BMatrix:
    WEIGHTS = {"stability":0.25,"dividend":0.20,"valuation":0.25,"moat":0.20,"perpetuity":0.10}
    ROE_MIN = 8.0; DEBT_MAX = 70.0

    def score(self, code: str, name: str, *,
              financials: dict | None = None, spot: dict | None = None,
              industry: str = "", is_soe: bool = False, is_leader: bool = False,
              cashflow_quality: dict | None = None) -> BMatrixResult:
        fin = financials or {}; spt = spot or {}
        roe_5y = float(fin.get("roe_5y", fin.get("roe_5y_avg", fin.get("roe", 0))) or 0)
        roe = float(fin.get("roe", fin.get("roe_current", roe_5y)) or 0)
        debt = float(fin.get("debt_ratio", fin.get("debt_to_assets", 50)) or 50)
        pe = float(fin.get("pe", 0) or 0); pb = float(fin.get("pb", 0) or 0)
        dy = float(spt.get("dividend_yield", fin.get("dividend_yield", 0)) or 0)
        current = float(spt.get("current", 0) or 0)

        # S-稳定性
        stability = min(10.0, max(0, (roe_5y - 8) / 2 * 5 + 5)) if roe_5y > 0 else 5.0
        # D-分红力
        if dy >= 4.0: dividend = 10.0
        elif dy >= 2.0: dividend = 7.0 + (dy - 2) / 2 * 3
        elif dy > 0: dividend = 5.0
        else: dividend = 3.0
        # V-估值安全 + PB-ROE
        valuation = 5.0; pb_roe_ok = True; trap_warning = ""
        if pe > 0 and pb > 0 and roe > 0:
            if pe < 10: valuation = 9.0
            elif pe < 20: valuation = 7.0 + (20 - pe) / 10 * 2
            elif pe < 30: valuation = 5.0 + (30 - pe) / 10 * 2
            elif pe < 40: valuation = 3.0 + (40 - pe) / 10 * 2
            else: valuation = 2.0
            if pb < 1.0 and roe < 5.0:
                pb_roe_ok = False; trap_warning = f"⚠️ 低PB陷阱: PB={pb:.1f} ROE={roe:.1f}%"
                valuation = max(2.0, valuation - 3.0)
            elif pb < 1.5 and roe > 10:
                valuation = min(10.0, valuation + 1.0)
            elif pb > 5 and roe < 10:
                pb_roe_ok = False; trap_warning = f"⚠️ 高PB低ROE: PB={pb:.1f} ROE={roe:.1f}%"

        # Q-质量陷阱防线 (V2.0 新增)
        quality_penalty = 0; quality_warnings = []; cashflow_ok = True
        cf = cashflow_quality or {}
        if cf:
            cf_ratio = float(cf.get("ocf_to_profit", 1.0) or 1.0)
            if cf_ratio < 0.5:
                quality_penalty += 2.0; cashflow_ok = False
                quality_warnings.append(f"经营现金流仅为净利润{cf_ratio:.0%}, 利润质量严重存疑")
            elif cf_ratio < 0.8:
                quality_penalty += 1.0
                quality_warnings.append(f"经营现金流/净利润={cf_ratio:.0%}, 匹配度偏低")
            if cf.get("dividend_from_debt"):
                quality_penalty += 2.0; cashflow_ok = False
                quality_warnings.append("高分红依赖举债或一次性利润, 不可持续")
            if cf.get("receivables_abnormal"):
                quality_penalty += 1.0; quality_warnings.append("应收账款异常膨胀")
            if cf.get("inventory_abnormal"):
                quality_penalty += 1.0; quality_warnings.append("存货异常积压")
            if cf.get("goodwill_ratio", 0) > 30:
                quality_penalty += 1.5; quality_warnings.append(f"商誉占比{cf['goodwill_ratio']:.0f}%, 减值风险高")
            if cf.get("regulatory_risk"):
                quality_penalty += 1.0; quality_warnings.append(f"行业监管风险: {cf['regulatory_risk']}")

        # M-护城河
        moat = 5.0
        if is_leader: moat += 2.0
        if is_soe: moat += 1.0
        if debt < 40: moat += 1.0
        if roe > 15: moat += 1.0
        moat = min(10.0, moat)
        # G-永续性
        perpetual = ["银行","公用事业","交通运输","食品饮料","医药生物","煤炭","石油石化","电力设备","通信","保险"]
        perpetuity = 8.0 if industry in perpetual else 5.0
        if is_soe: perpetuity += 1.0; perpetuity = min(10.0, perpetuity)

        total = stability*0.25+dividend*0.20+valuation*0.25+moat*0.20+perpetuity*0.10
        if 0 < roe_5y < self.ROE_MIN: total -= 2.0
        if debt > self.DEBT_MAX: total -= 2.0
        total -= quality_penalty
        total = round(max(0.0, min(10.0, total)), 1)

        if total >= 8.0: grade = "A"; rec = "✅ 核心底仓"
        elif total >= 6.5: grade = "B"; rec = "✅ 次级底仓"
        elif total >= 5.0: grade = "C"; rec = "⚠️ 不推荐底仓"
        else: grade = "D"; rec = "❌ 不符合底仓标准"
        stop_loss = round(current * 0.90, 2) if current > 0 else 0

        return BMatrixResult(code=code,name=name,total_score=total,grade=grade,
            stability_score=round(stability,1),dividend_score=round(dividend,1),
            valuation_score=round(valuation,1),moat_score=round(moat,1),
            perpetuity_score=round(perpetuity,1),roe_5y_avg=round(roe_5y,1),
            debt_ratio=round(debt,1),dividend_yield=round(dy,2),
            pe_current=round(pe,1),pb_current=round(pb,1),roe_current=round(roe,1),
            pb_roe_ok=pb_roe_ok,valuation_trap_warning=trap_warning,
            quality_penalty=round(quality_penalty,1),
            quality_warnings=quality_warnings,cashflow_ok=cashflow_ok,
            recommendation=rec,stop_loss=stop_loss)
