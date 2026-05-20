"""
R-Matrix — 轮动评分矩阵
───────────────────────
核心哲学: "买在无人问津时(谷底)，卖在人声鼎沸处(山顶)"
目标角色: mid_term_rotation (中期轮动)
投资周期: 2-4周

看: 周期位置、反转信号、板块确认、弹性空间
不看: 当前PE(周期股PE最低时恰是利润顶峰)、当前盈利

校准 V1.1 (2026-05-06):
  - 加入北向资金/机构连续净流入率作为平滑指标
  - 大市值票(>1000亿)的大资金建仓往往隐蔽平缓，龙虎榜无法捕捉
  - 产能利用率<70%=谷底，>90%=警惕高峰
"""

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class RMatrixResult:
    """R-Matrix 评分结果"""
    code: str
    name: str
    total_score: float
    grade: str

    # 子维度
    cycle_score: float        # C-周期位置
    reversal_score: float     # R-反转信号
    sector_score: float       # F-板块确认
    technical_score: float    # T-技术形态
    elasticity_score: float   # P-弹性空间

    # 关键信号
    cycle_position: str       # BOTTOM/VALLEY/RECOVERY/PEAK/TOP
    north_flow_consecutive: int  # 北向连续净流入天数
    distance_from_peak: float    # 距历史高点跌幅%
    sector_state: str

    recommendation: str
    stop_loss: float
    confidence: float = 1.0
    max_grade: str = "A"
    unknown_dimensions: list[str] = field(default_factory=list)
    execution_mode: str = "human_confirm"
    hard_reject_reasons: list[str] = field(default_factory=list)


class RMatrix:
    """轮动评分引擎"""

    WEIGHTS = {
        "cycle":      0.30,  # C-周期位置 (权重最高)
        "reversal":   0.25,  # R-反转信号
        "sector":     0.20,  # F-板块确认
        "technical":  0.15,  # T-技术形态
        "elasticity": 0.10,  # P-弹性空间
    }

    def classify_cycle_position(self, distance_from_peak: float,
                                chg_60d: float, pe: float) -> tuple[str, float]:
        """根据距高点跌幅+60日走势+PE 判定周期位置。

        Returns:
            (位置标签, 评分 0-10)
        """
        # 已创新高 → 山顶
        if distance_from_peak >= 0:
            return ("TOP", 0.0)            # 🔴 卖点
        # 距历史高点 > 40% + 60日仍在跌 → 谷底
        if distance_from_peak < -40 and chg_60d < -10:
            return ("BOTTOM", 10.0)        # 🟢 极佳买点
        # 距高点 25-40% + 企稳 → 谷底确认
        elif distance_from_peak < -25 and chg_60d > -10:
            return ("VALLEY", 8.0)         # 🟢 好买点
        # 距高点 10-25% + 开始回升 → 复苏初期
        elif distance_from_peak < -10 and chg_60d > 0:
            return ("RECOVERY", 6.0)       # 🟡 可买入
        # 距高点 < 10% 但还在涨 → 接近高峰
        elif distance_from_peak > -10 and chg_60d > 10:
            return ("PEAK", 3.0)           # 🟠 谨慎
        # 中间状态
        else:
            return ("RECOVERY", 5.0)

    def score(self, code: str, name: str, *,
              kline_records: list[dict] | None = None,
              sector_state: str = "NEUTRAL",
              sector_name: str = "",
              north_flow_consecutive: int | None = None,
              market_cap: float = 0,
              pe: float = 0,
              historical_high: float = 0,
              decline_converging: bool = False,
              sector_diffusion_ok: bool = False,
              ) -> RMatrixResult:
        """对轮动候选打分。

        Args:
            kline_records: K线数据 [{"close":..., "volume":..., "date":...}, ...]
            sector_state: 板块状态 (LEADING|CONFIRMATION|NEUTRAL|DIVERGENCE|RETREAT)
            north_flow_consecutive: 北向连续净流入天数
            market_cap: 总市值(亿)
            historical_high: 历史高点价格
        """
        records = kline_records or []
        closes = [r["close"] for r in records] if records else []

        if len(closes) < 20:
            return RMatrixResult(
                code=code, name=name, total_score=5.0, grade="C",
                cycle_score=5, reversal_score=5, sector_score=5,
                technical_score=5, elasticity_score=5,
                cycle_position="UNKNOWN", north_flow_consecutive=0,
                distance_from_peak=0, sector_state=sector_state,
                recommendation="⚠️ 数据不足", stop_loss=0,
                confidence=0.0, max_grade="C",
                unknown_dimensions=["kline"],
                execution_mode="paper",
            )

        # ── 计算基础指标 ─────────────────────────────
        latest = closes[-1]
        chg_60d = (closes[-1] / closes[0] - 1) * 100 if len(closes) >= 2 else 0

        # 历史高点 (用60日最高价代理)
        if historical_high <= 0:
            historical_high = max(r.get("high", r["close"]) for r in records) if records else latest
        distance_from_peak = round((latest / historical_high - 1) * 100, 1)

        # ── C-周期位置 (30%) ─────────────────────────
        cycle_pos, cycle_score = self.classify_cycle_position(
            distance_from_peak, chg_60d, pe
        )

        # ── R-反转信号 (25%) ─────────────────────────
        unknown_dimensions: list[str] = []
        max_grade = "A"
        execution_mode = "human_confirm"
        hard_reject_reasons: list[str] = []

        reversal_components: list[tuple[float, float]] = []

        # 北向资金连续流入 (平滑指标，机构建仓更隐蔽)
        if north_flow_consecutive is None:
            unknown_dimensions.append("north_flow")
            max_grade = _lower_max_grade(max_grade, "B")
            execution_mode = "paper"
        else:
            if north_flow_consecutive >= 5:
                north_score = 10.0
            elif north_flow_consecutive >= 3:
                north_score = 7.5
            elif north_flow_consecutive >= 1:
                north_score = 5.0
            else:
                north_score = 0.0
            reversal_components.append((north_score, 0.55))

        # 底部放量信号
        volumes = [r["volume"] for r in records]
        if len(volumes) >= 10:
            recent_vol = sum(volumes[-5:]) / 5
            prev_vol = sum(volumes[-10:-5]) / 5
            if recent_vol > prev_vol * 1.3:
                volume_score = 8.0
            elif recent_vol > prev_vol * 1.1:
                volume_score = 5.0
            else:
                volume_score = 0.0
            reversal_components.append((volume_score, 0.45))
        else:
            unknown_dimensions.append("bottom_volume")

        if reversal_components:
            reversal_weight = sum(weight for _, weight in reversal_components)
            reversal = sum(score * weight for score, weight in reversal_components) / reversal_weight
            # 大市值票: 龙虎榜失真, 北向权重更高。仅在北向数据存在时做平滑。
            if market_cap > 1000 and north_flow_consecutive is not None:
                reversal = reversal * 0.7 + 3.0
            reversal = min(10.0, max(0, reversal))
        else:
            reversal = None
            unknown_dimensions.append("reversal")
            max_grade = _lower_max_grade(max_grade, "B")
            execution_mode = "paper"

        # ── F-板块确认 (20%) ─────────────────────────
        normalized_sector_state = (sector_state or "UNKNOWN").upper()
        state_scores = {
            "LEADING": 9.0, "CONFIRMATION": 7.5,
            "NEUTRAL": 5.0, "DIVERGENCE": 3.0,
            "RETREAT": 0.0, "RETREATING": 0.0,
        }
        if normalized_sector_state == "UNKNOWN":
            sector = None
            unknown_dimensions.append("sector")
            max_grade = _lower_max_grade(max_grade, "B")
            execution_mode = "paper"
        else:
            sector = state_scores.get(normalized_sector_state, 5.0)
            if normalized_sector_state in {"RETREAT", "RETREATING"}:
                hard_reject_reasons.append("板块退潮，R-Matrix 硬拒绝")
                max_grade = "D"
                execution_mode = "paper"

        # ── T-技术形态 (15%) ─────────────────────────
        import numpy as np
        technical = 5.0

        # 均线: 价格站上20日线
        sma20 = float(np.mean(closes[-20:])) if len(closes) >= 20 else latest
        if latest > sma20:
            technical += 1.5

        # RSI: 从超卖区域回升
        if len(closes) >= 14:
            gains = [max(0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
            losses = [max(0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
            avg_gain = float(np.mean(gains[-14:])) if gains else 0
            avg_loss = float(np.mean(losses[-14:])) if losses else 0
            if avg_loss > 0:
                rsi = 100 - 100 / (1 + avg_gain / avg_loss)
                if 30 < rsi < 50:
                    technical += 1.5   # 刚从底部回升
                elif 50 < rsi < 70:
                    technical += 1.0   # 强势区间

        # 60日趋势
        if chg_60d > 5:
            technical += 1.0
        elif chg_60d > -5:
            technical += 0.5

        technical = min(10.0, max(0, technical))

        # ── P-弹性空间 (10%) ─────────────────────────
        # 空间 = 距高点越远 → 弹性越大 → 分数越高
        if distance_from_peak >= 0:
            elasticity = 0.0    # 已创新高，空间有限
        elif distance_from_peak <= -50:
            elasticity = 10.0   # 极大弹性
        elif distance_from_peak <= -40:
            elasticity = 9.0
        elif distance_from_peak <= -30:
            elasticity = 8.0
        elif distance_from_peak <= -20:
            elasticity = 6.5
        elif distance_from_peak <= -10:
            elasticity = 4.5
        elif distance_from_peak <= -5:
            elasticity = 2.5
        else:
            elasticity = 1.0

        # ── 加权总分 ─────────────────────────────────
        dimensions = {
            "cycle": cycle_score,
            "reversal": reversal,
            "sector": sector,
            "technical": technical,
            "elasticity": elasticity,
        }
        known_weight = sum(self.WEIGHTS[key] for key, value in dimensions.items() if value is not None)
        if known_weight <= 0:
            total = 0.0
            confidence = 0.0
        else:
            total = sum(
                value * self.WEIGHTS[key] for key, value in dimensions.items() if value is not None
            ) / known_weight
            total = round(max(0.0, min(10.0, total)), 1)
            confidence = round(known_weight, 2)

        # ── 防左侧接飞刀 (V2.0) ─────────────────────
        if not decline_converging and distance_from_peak < -15:
            total -= 1.5
            max_grade = _lower_max_grade(max_grade, "B")
        if not sector_diffusion_ok and normalized_sector_state not in ("LEADING","CONFIRMATION"):
            total -= 1.0
            if normalized_sector_state == "UNKNOWN":
                max_grade = _lower_max_grade(max_grade, "B")
        total = round(max(0.0, total), 1)
        if hard_reject_reasons:
            total = min(total, 4.9)

        # ── 评级 ─────────────────────────────────────
        if total >= 8.0:
            grade = "A"; rec = "✅ 周期拐点确认 — 轮动建仓"
        elif total >= 6.5:
            grade = "B"; rec = "✅ 左侧机会 — 小仓位试探"
        elif total >= 5.0:
            grade = "C"; rec = "⚠️ 等待更明确信号"
        else:
            grade = "D"; rec = "❌ 不适合轮动"
        grade = _cap_grade(grade, max_grade)
        if grade != "A" and total >= 8.0 and max_grade != "A":
            rec += f"（数据/闸门限制，最高{max_grade}级）"
        if execution_mode == "paper" and grade in {"A", "B", "C"}:
            rec += "；仅纸面跟踪"
        if hard_reject_reasons:
            rec = "❌ 板块退潮硬拒绝"

        stop_loss = round(latest * 0.93, 2)  # 轮动止损-7%

        return RMatrixResult(
            code=code, name=name, total_score=total, grade=grade,
            cycle_score=round(cycle_score, 1),
            reversal_score=round(reversal, 1) if reversal is not None else 0.0,
            sector_score=round(sector, 1) if sector is not None else 0.0,
            technical_score=round(technical, 1),
            elasticity_score=round(elasticity, 1),
            cycle_position=cycle_pos,
            north_flow_consecutive=north_flow_consecutive or 0,
            distance_from_peak=round(distance_from_peak, 1),
            sector_state=normalized_sector_state,
            recommendation=rec,
            stop_loss=stop_loss,
            confidence=confidence,
            max_grade=max_grade,
            unknown_dimensions=unknown_dimensions,
            execution_mode=execution_mode,
            hard_reject_reasons=hard_reject_reasons,
        )


def _lower_max_grade(current: str, cap: str) -> str:
    order = {"D": 0, "C": 1, "B": 2, "A": 3}
    return cap if order[cap] < order[current] else current


def _cap_grade(grade: str, max_grade: str) -> str:
    order = {"D": 0, "C": 1, "B": 2, "A": 3}
    return max_grade if order[grade] > order[max_grade] else grade
