"""
D-Matrix — 黑马评分矩阵
───────────────────────
核心哲学: "事件驱动 + 资金异动，不靠基本面选黑马"
目标角色: dark_horse (黑马)
投资周期: 1-5天，快进快出

看: 催化剂强度、资金异动、筹码弹性、上方阻力
不看: PE、ROE、估值(黑马不需要业绩支撑)

校准 V1.1 (2026-05-06):
  - K-筹码结构加入"上方套牢盘比例"和"距历史新高距离"
  - 上方套牢盘>30% → 游资不愿意拉升, 扣分
  - 无催化剂 → 直接拒绝 (铁律)
"""

from __future__ import annotations
from dataclasses import dataclass


@dataclass
class DMatrixResult:
    """D-Matrix 评分结果"""
    code: str
    name: str
    total_score: float
    grade: str

    # 子维度
    event_score: float        # E-事件强度 (35%权重)
    capital_score: float      # Z-资金异动 (30%)
    chip_score: float         # K-筹码结构 (20%)
    blast_score: float        # B-爆发弹性 (15%)

    # 关键信号
    catalyst_present: bool
    catalyst_description: str
    overhead_resistance_pct: float  # 上方套牢盘比例
    distance_to_ath: float          # 距历史新高%
    market_cap: float               # 市值(亿)
    turnover_rate: float            # 换手率
    volatility: float               # 波动率
    consecutive_limit_up: int       # 连续涨停板数

    recommendation: str
    stop_loss: float
    max_hold_days: int


class DMatrix:
    """黑马评分引擎"""

    WEIGHTS = {
        "event":   0.35,  # E-事件强度 (最重要)
        "capital": 0.30,  # Z-资金异动
        "chip":    0.20,  # K-筹码结构
        "blast":   0.15,  # B-爆发弹性
    }

    # 硬门
    MARKET_CAP_MAX = 500    # >500亿不算黑马(太大拉不动)
    TURNOVER_MIN = 2.0      # 换手率底线

    def score(self, code: str, name: str, *,
              catalyst: dict | None = None,
              spot: dict | None = None,
              kline_records: list[dict] | None = None,
              dragon_tiger: dict | None = None,
              overhead_resistance: float = 0,
              distance_to_ath: float = 0,
              consecutive_limit_up: int = 0,
              is_tradable: bool = True,
              is_locked_board: bool = False,
              ) -> DMatrixResult:
        """对黑马候选打分。

        Args:
            catalyst: 催化剂信息 {"type":"政策/订单/重组/概念","description":"...","strength":1-10}
            spot: 实时行情
            kline_records: K线数据
            dragon_tiger: 龙虎榜数据 {"desks":[...], "net_buy":..., "active":bool}
            overhead_resistance: 上方套牢盘比例(%)
            distance_to_ath: 距历史新高(%)
            consecutive_limit_up: 连续涨停板数
        """
        cat = catalyst or {}
        spt = spot or {}
        dt = dragon_tiger or {}
        records = kline_records or []

        # ── 硬门1: 无催化剂 → 直接拒绝 ──────────────
        has_catalyst = bool(cat.get("type") or cat.get("description"))
        cat_strength = float(cat.get("strength", 0))

        if not has_catalyst or cat_strength < 2:
            return DMatrixResult(
                code=code, name=name, total_score=0, grade="D",
                event_score=0, capital_score=0, chip_score=0, blast_score=0,
                catalyst_present=False, catalyst_description="无催化剂",
                overhead_resistance_pct=overhead_resistance,
                distance_to_ath=distance_to_ath, market_cap=0,
                turnover_rate=0, volatility=0, consecutive_limit_up=0,
                recommendation="❌ 无催化剂 — 不符合黑马标准",
                stop_loss=0, max_hold_days=0,
            )

        # ── 基础数据 ─────────────────────────────────
        market_cap = float(spt.get("market_cap_亿", 0) or 0)
        turnover = float(spt.get("turnover", 0) or 0)
        chg_today = float(spt.get("chg_pct", 0) or 0)
        current = float(spt.get("current", 0) or 0)

        closes = [r["close"] for r in records] if records else []
        volatility = 0
        if len(closes) >= 10:
            import numpy as np
            rets = np.diff(closes) / closes[:-1]
            volatility = float(np.std(rets) * np.sqrt(252) * 100)

        # ── E-事件强度 (35%) ─────────────────────────
        event = cat_strength  # 基础分 = 催化剂强度(1-10)

        # 事件类型加分
        cat_type = str(cat.get("type", ""))
        if "政策" in cat_type:
            event += 1.5     # 政策级别最高
        elif "订单" in cat_type:
            event += 1.0     # 实质性利好
        elif "重组" in cat_type:
            event += 1.0     # 资产重组
        elif "概念" in cat_type:
            event += 0.5     # 概念炒作确定性低

        # 连续涨停确认事件强度
        if consecutive_limit_up >= 3:
            event += 2.0     # 3连板 → 市场已投票确认
        elif consecutive_limit_up >= 1:
            event += 1.0

        event = min(10.0, event)

        # ── Z-资金异动 (30%) ─────────────────────────
        capital = 5.0

        # 龙虎榜
        if dt.get("active"):
            capital += 2.0    # 有龙虎榜数据
            if dt.get("net_buy", 0) > 0:
                capital += 1.0  # 净买入

        # 游资活跃度
        desk_count = dt.get("desks", [])
        if isinstance(desk_count, list) and len(desk_count) >= 3:
            capital += 1.5
        elif isinstance(desk_count, int) and desk_count >= 3:
            capital += 1.5

        # 今日涨幅 (黑马需要已经启动)
        if chg_today > 5:
            capital += 1.5
        elif chg_today > 2:
            capital += 0.5

        # 连续放量
        if records and len(records) >= 5:
            vols = [r["volume"] for r in records[-5:]]
            avg_vol = sum(vols) / 5
            if len(records) >= 10:
                prev_avg = sum(r["volume"] for r in records[-10:-5]) / 5
                if avg_vol > prev_avg * 2:
                    capital += 1.5   # 放量2倍

        capital = min(10.0, capital)

        # ── K-筹码结构 (20%) ─────────────────────────
        chip = 5.0

        # 小盘加分
        if market_cap < 50:
            chip += 3.0      # 小盘 → 最容易拉
        elif market_cap < 100:
            chip += 2.0      # 中小盘
        elif market_cap < 200:
            chip += 1.0
        elif market_cap > self.MARKET_CAP_MAX:
            chip -= 3.0      # >500亿 → 拉不动

        # 换手率
        if turnover > 10:
            chip += 2.0      # 高换手 → 筹码活跃
        elif turnover > 5:
            chip += 1.0
        elif turnover < self.TURNOVER_MIN:
            chip -= 2.0      # 换手太低 → 无关注

        # ⚠️ 上方套牢盘 (V1.1新增)
        if overhead_resistance > 30:
            chip -= 3.0       # 上方套牢盘>30% → 游资不愿意拉升
        elif overhead_resistance > 15:
            chip -= 1.5

        # 距历史新高 (越近越好——上方无阻力)
        if distance_to_ath > -5:    # 距新高<5%
            chip += 1.5
        elif distance_to_ath > -15:
            chip += 0.5

        chip = min(10.0, max(0, chip))

        # ── B-爆发弹性 (15%) ─────────────────────────
        # 黑马要的就是高弹性(和底仓完全相反)
        if volatility > 80:
            blast = 10.0       # 极大弹性
        elif volatility > 60:
            blast = 8.0
        elif volatility > 40:
            blast = 6.0
        elif volatility > 25:
            blast = 4.0
        else:
            blast = 2.0       # 波动太低 → 不适合黑马

        # ── 加权总分 ─────────────────────────────────
        total = (
            event * self.WEIGHTS["event"] +
            capital * self.WEIGHTS["capital"] +
            chip * self.WEIGHTS["chip"] +
            blast * self.WEIGHTS["blast"]
        )
        total = round(max(0.0, min(10.0, total)), 1)

        # ── 可交易性检查 (V2.0) ──────────────────────
        # 一字板/停牌/不可交易 → 大幅扣分
        if is_locked_board:
            total -= 4.0  # 一字板无法买入
        elif not is_tradable:
            total -= 2.0  # 停牌/其他不可交易
        total = round(max(0.0, total), 1)

        # ── 评级 ─────────────────────────────────────
        if total >= 7.5:
            grade = "A"; rec = "🔥 强黑马信号 — 短线出击"
            max_hold = 5
        elif total >= 6.0:
            grade = "B"; rec = "✅ 黑马候选 — 小仓位试探"
            max_hold = 3
        elif total >= 4.5:
            grade = "C"; rec = "⚠️ 信号偏弱 — 观望"
            max_hold = 0
        else:
            grade = "D"; rec = "❌ 不符合黑马标准"
            max_hold = 0

        stop_loss = round(current * 0.95, 2)  # 黑马止损紧-5%

        return DMatrixResult(
            code=code, name=name, total_score=total, grade=grade,
            event_score=round(event, 1),
            capital_score=round(capital, 1),
            chip_score=round(chip, 1),
            blast_score=round(blast, 1),
            catalyst_present=True,
            catalyst_description=str(cat.get("description", cat.get("type", ""))),
            overhead_resistance_pct=round(overhead_resistance, 1),
            distance_to_ath=round(distance_to_ath, 1),
            market_cap=round(market_cap, 1),
            turnover_rate=round(turnover, 2),
            volatility=round(volatility, 1),
            consecutive_limit_up=consecutive_limit_up,
            recommendation=rec,
            stop_loss=stop_loss,
            max_hold_days=max_hold,
        )
