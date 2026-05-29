# allowlist: forbidden-token-definition
"""V4.0 ZC35 CatalystLifecycleEngine v2.0 — 完整催化生命周期引擎

升级内容 (基于双环传动002472 10个月6轮催化周期实证):
- v1.0: 仅4状态(PRE_EVENT/EVENT_ACTIVE/POST_EVENT_DECAY/EXHAUSTED)
- v2.0: 5级催化分类(S/A/B/C/D) + 半衰期表 + 情绪周期映射 + 叠加效应引擎

ZC35 域归属: SEAT_04_CATALYST_TRACKER + SEAT_06_EVENT_SPECIALIST
"""
from __future__ import annotations
from typing import Optional

# ── v1.0 保留 (向后兼容) ──
LIFECYCLE = ["PRE_EVENT", "EVENT_ACTIVE", "POST_EVENT_DECAY", "EXHAUSTED"]

# ── v2.0 新增 ──

# 催化级别分类 (跨标的通用, 基于实证)
CATALYST_TAXONOMY = {
    "S": {
        "label": "范式级产品/事件",
        "examples": ["全球首款量产产品发布", "分拆上市过会", "独家大额订单"],
        "half_life_days": 7,
        "full_decay_days": 15,
        "peak_phase": "D+6~D+10",
        "pre_run_days": 5,
        "price_amplification": 1.0,
        "sentiment_boost_c": 40,
        "sell_on_news_risk": "MEDIUM",
        "tradeable": True,
    },
    "A": {
        "label": "国家级政策/标准",
        "examples": ["发改委政策发布会", "国家级标准发布", "产业基金设立"],
        "half_life_days": 2,
        "full_decay_days": 5,
        "peak_phase": "D-1~D+1",
        "pre_run_days": 3,
        "price_amplification": 0.55,
        "sentiment_boost_c": 20,
        "sell_on_news_risk": "HIGH",
        "tradeable": True,
    },
    "B": {
        "label": "公司级事件/预期",
        "examples": ["子公司IPO预期", "大额订单公告", "战略合作协议"],
        "half_life_days": 3,
        "full_decay_days": 7,
        "peak_phase": "D+0~D+2",
        "pre_run_days": 2,
        "price_amplification": 0.35,
        "sentiment_boost_c": 12,
        "sell_on_news_risk": "MEDIUM",
        "tradeable": True,
    },
    "C": {
        "label": "行业会议/外部财报",
        "examples": ["Google I/O", "英伟达财报", "COMPUTEX"],
        "half_life_days": 1,
        "full_decay_days": 3,
        "peak_phase": "D-1~D+0",
        "pre_run_days": 3,
        "price_amplification": 0.15,
        "sentiment_boost_c": 6,
        "sell_on_news_risk": "HIGH",
        "tradeable": False,  # 仅会前可做, 开幕即卖
    },
    "D": {
        "label": "无效催化 ⚠️ NEGATIVE",
        "examples": ["计划内博览会开幕", "常规行业论坛"],
        "half_life_days": 0,
        "full_decay_days": 0,
        "peak_phase": "NONE",
        "pre_run_days": 0,
        "price_amplification": -0.10,  # 负信号!
        "sentiment_boost_c": -10,
        "sell_on_news_risk": "CERTAIN",
        "tradeable": False,
    },
}

# 情绪周期阶段
SENTIMENT_PHASES = [
    "VACUUM",         # 真空期: D+16+, 无催化
    "PRE_RUN",        # 抢跑期: D-5~D-1, 信息泄露
    "EVENT_BURST",    # 爆发期: D+0~D+3
    "CONTINUATION",   # 延续期: D+4~D+8
    "PLATEAU",        # 平台期: D+9~D+12
    "DECAY",          # 退潮期: D+13~D+15
]


class CatalystLifecycleEngine:
    """ZC35 催化生命周期引擎 v2.0

    升级内容:
    - 从4状态扩展为5级催化分类(S/A/B/C/D)
    - 加入半衰期、情绪温度、残值计算
    - 催化叠加效应引擎
    - 情绪阶段识别
    """

    # ── v1.0 兼容接口 ──
    def classify(self, event: dict) -> dict:
        """v1.0兼容: 基础催化级别分类"""
        if not event.get('publish_time'):
            return {
                "status": "DATA_INSUFFICIENT",
                "direct_trade_allowed": False,
                "real_trade_allowed": False,
                "broker_order_allowed": False,
            }
        ev = event.get('evidence_level', 'D')
        if ev == 'D':
            return {
                "lifecycle": "PRE_EVENT",
                "sell_on_news_risk": "HIGH",
                "direct_trade_allowed": False,
                "real_trade_allowed": False,
                "action": "WATCH_ONLY",
            }
        if event.get('scheduled_without_surprise'):
            return {
                "lifecycle": "PRE_EVENT",
                "sell_on_news_risk": "MEDIUM",
                "direct_trade_allowed": False,
                "real_trade_allowed": False,
                "action": "OBSERVE",
            }
        return {
            "lifecycle": "EVENT_ACTIVE",
            "residual_power": 0.8,
            "sell_on_news_risk": "LOW",
            "direct_trade_allowed": False,
            "real_trade_allowed": False,
            "action": "PAPER_TRACK",
        }

    # ── v2.0 新增接口 ──

    def get_taxonomy(self, level: str = None) -> dict:
        """获取催化分类学定义"""
        if level:
            return CATALYST_TAXONOMY.get(level, CATALYST_TAXONOMY["D"])
        return CATALYST_TAXONOMY

    def compute_residual_power(self, level: str, days_since_event: int) -> float:
        """计算催化残值 (0.0 ~ amplification)

        衰减模型: 
        - 前半段(D+0~half_life): 线性衰减至0.5
        - 后半段(half_life~full_decay): 线性衰减至0
        - D级催化: 始终为0或负
        """
        profile = CATALYST_TAXONOMY.get(level, CATALYST_TAXONOMY["D"])
        amp = profile["price_amplification"]
        half = profile["half_life_days"]
        full = profile["full_decay_days"]

        if level == "D":
            return amp  # 负信号
        if days_since_event >= full:
            return 0.0
        if days_since_event <= 0:
            return amp * 0.8  # 未发生时已有80%定价
        if days_since_event <= half:
            # 前半段: 1.0 → 0.5
            return amp * (1.0 - 0.5 * days_since_event / half)
        # 后半段: 0.5 → 0.0
        progress = (days_since_event - half) / max(1, full - half)
        return amp * max(0.0, 0.5 - 0.5 * progress)

    def identify_sentiment_phase(self, level: str, days_since_event: int) -> str:
        """根据催化级别和天数识别情绪阶段"""
        profile = CATALYST_TAXONOMY.get(level, CATALYST_TAXONOMY["D"])
        pre_run = profile["pre_run_days"]
        half = profile["half_life_days"]
        full = profile["full_decay_days"]

        if days_since_event >= full:
            return "VACUUM"
        if days_since_event >= half * 1.8:
            return "DECAY"
        if days_since_event >= half * 1.3:
            return "PLATEAU"
        if days_since_event >= 3:
            return "CONTINUATION"
        if days_since_event >= 0:
            return "EVENT_BURST"
        if days_since_event >= -pre_run:
            return "PRE_RUN"
        return "VACUUM"

    def compute_stack_effect(self, catalysts: list[dict]) -> dict:
        """计算多催化叠加效应

        Args:
            catalysts: [{"level":"S","days_since_event":5,"name":"GD01"}, ...]

        Returns:
            {"stack_count": n, "penalty_factor": x, "effective_window_days": d, 
             "total_residual": r, "warning": str | None}
        """
        active = []
        for cat in catalysts:
            level = cat.get("level", "D")
            days = cat.get("days_since_event", 999)
            residual = self.compute_residual_power(level, days)
            taxonomy = CATALYST_TAXONOMY.get(level, CATALYST_TAXONOMY["D"])
            if taxonomy["full_decay_days"] > 0 and days < taxonomy["full_decay_days"]:
                active.append({
                    "name": cat.get("name", "?"),
                    "level": level,
                    "days_since": days,
                    "residual": round(residual, 3),
                    "half_life": taxonomy["half_life_days"],
                    "full_decay": taxonomy["full_decay_days"],
                })

        n = len(active)
        if n <= 1:
            return {
                "stack_count": n,
                "penalty_factor": 1.0,
                "effective_window_days": active[0]["full_decay"] if active else 0,
                "total_residual": round(sum(a["residual"] for a in active), 3),
                "catalysts": active,
                "warning": None,
            }

        base_window = max(a["full_decay"] for a in active)
        penalty = 1.0 + (n - 1) * 0.25  # 每多一层缩短25%
        effective = max(1, int(base_window / penalty))

        return {
            "stack_count": n,
            "penalty_factor": round(penalty, 2),
            "effective_window_days": effective,
            "total_residual": round(sum(a["residual"] for a in active), 3),
            "catalysts": active,
            "warning": "叠加加速催熟: 窗口缩短{}%".format(int((1-1/penalty)*100)) if n >= 2 else None,
        }

    def full_lifecycle_analysis(self, event_level: str, days_since_event: int,
                                event_name: str = "") -> dict:
        """一站式催化生命周期完整分析

        Returns:
            完整的催化状态快照, 可用于:
            - 报告自动生成
            - R-Matrix周期联立
            - 仓位决策辅助
        """
        taxonomy = CATALYST_TAXONOMY.get(event_level, CATALYST_TAXONOMY["D"])
        residual = self.compute_residual_power(event_level, days_since_event)
        sentiment = self.identify_sentiment_phase(event_level, days_since_event)

        # 生命周期状态
        if days_since_event >= taxonomy["full_decay_days"]:
            lifecycle = "EXHAUSTED"
        elif days_since_event >= taxonomy["half_life_days"]:
            lifecycle = "POST_EVENT_DECAY"
        elif days_since_event >= 0:
            lifecycle = "EVENT_ACTIVE"
        else:
            lifecycle = "PRE_EVENT"

        # 交易信号判断
        if taxonomy["tradeable"] and lifecycle == "EVENT_ACTIVE" and residual > 0.3:
            signal = "PAPER_TRACK"  # 可纸面追踪
        elif lifecycle == "PRE_RUN":
            signal = "WATCH_PRE_RUN"
        elif lifecycle in ("EXHAUSTED","POST_EVENT_DECAY") and event_level == "D":
            signal = "AVOID"  # D级催化+已过期=远离
        elif lifecycle == "EXHAUSTED":
            signal = "WAIT_NEW_CATALYST"
        else:
            signal = "OBSERVE"

        return {
            "event_name": event_name,
            "evidence_level": event_level,
            "taxonomy_label": taxonomy["label"],
            "days_since_event": days_since_event,
            "lifecycle": lifecycle,
            "sentiment_phase": sentiment,
            "residual_power": round(residual, 3),
            "half_life_days": taxonomy["half_life_days"],
            "full_decay_days": taxonomy["full_decay_days"],
            "peak_phase": taxonomy["peak_phase"],
            "sell_on_news_risk": taxonomy["sell_on_news_risk"],
            "sentiment_boost_c": taxonomy["sentiment_boost_c"],
            "tradeable": taxonomy["tradeable"],
            "action": signal,
            "direct_trade_allowed": False,
            "real_trade_allowed": False,
            "broker_order_allowed": False,
        }

    def batch_analyze(self, events: list[dict]) -> dict:
        """批量分析多个催化事件的联合效应"""
        individual = []
        for ev in events:
            individual.append(self.full_lifecycle_analysis(
                ev.get("level","D"),
                ev.get("days_since_event",0),
                ev.get("name",""),
            ))

        stack = self.compute_stack_effect(events)

        # 综合情绪判断
        active_phases = [i["sentiment_phase"] for i in individual
                        if i["sentiment_phase"] not in ("VACUUM","DECAY")]
        if not active_phases:
            dominant_phase = "VACUUM"
        elif "EVENT_BURST" in active_phases:
            dominant_phase = "EVENT_BURST"
        elif "CONTINUATION" in active_phases:
            dominant_phase = "CONTINUATION"
        elif "PRE_RUN" in active_phases:
            dominant_phase = "PRE_RUN"
        else:
            dominant_phase = active_phases[0]

        return {
            "events": individual,
            "stack_effect": stack,
            "dominant_sentiment": dominant_phase,
            "total_events": len(events),
            "active_count": stack["stack_count"],
            "summary": self._generate_summary(individual, stack, dominant_phase),
        }

    def _generate_summary(self, individual: list, stack: dict,
                          dominant: str) -> str:
        """生成自然语言摘要"""
        n = stack["stack_count"]
        if n == 0:
            return "催化真空期 — 无有效催化, 等待新事件"
        if n == 1:
            return f"单一催化({individual[0]['evidence_level']}级) — {individual[0]['lifecycle']}, 残值{individual[0]['residual_power']}"
        if n >= 3:
            return f"{n}重催化叠加 — 窗口缩短至{stack['effective_window_days']}天, 主导情绪{dominant}, ⚠️加速催熟风险"
        return f"{n}重催化 — 有效窗口{stack['effective_window_days']}天, 主导{dominant}"

    # ── v2.1 信号分类方法 (基于Top 50大数据实证) ──

    TRUE_SIGNAL_TRIAD = [
        "business_relevance",  # 要素1: 与核心业务直接关联
        "financial_verification",  # 要素2: 有可量化财务/运营验证
        "cycle_resonance",  # 要素3: 行业/宏观周期同向共振
    ]

    FALSE_SIGNAL_TYPES = {
        "sell_on_news": "利好出尽型 — 催化已充分预期, 发布即卖",
        "fundamentals_gap": "基本面脱节型 — 题材热但公司无法承接",
        "diminishing_returns": "边际递减型 — 同质催化重复, 信息增量→0",
        "noise_pollution": "噪音污染型 — 规模太小/非A股驱动, 市场忽略",
    }

    SECTOR_PROFILES = {
        "cyclical": {
            "label": "周期股(钢铁/有色/化工)",
            "rule": "重市场不重财务",
            "best_catalyst": "S/A级: 商品价格突破",
            "true_signal_rate": 0.65,
            "avg_window_days": 15,
        },
        "order_driven": {
            "label": "订单驱动型(特高压/军工)",
            "rule": "中标放量是唯一真信号",
            "best_catalyst": "A级: 大额中标(>10亿)",
            "true_signal_rate": 0.57,
            "avg_window_days": 13,
        },
        "certification": {
            "label": "认证/技术型(储能/电池/芯片)",
            "rule": "认证边际递减, 需业绩验证接力",
            "best_catalyst": "A级: 首次国际认证 / 技术突破",
            "true_signal_rate": 0.65,
            "avg_window_days": 10,
        },
        "defensive": {
            "label": "消费/防御型(食品/粮食)",
            "rule": "重财务不重市场",
            "best_catalyst": "B级: 财报改善 / 分红公告",
            "true_signal_rate": 0.35,
            "avg_window_days": 6,
        },
        "transformation": {
            "label": "周期→成长切换型",
            "rule": "行业拐点+结构扩张=最强催化",
            "best_catalyst": "S级: 行业周期拐点+海外扩张+财政共振",
            "true_signal_rate": 0.95,
            "avg_window_days": 20,
        },
    }

    def classify_true_signal(self, event_name: str, event_level: str,
                             business_relevance: bool = False,
                             financial_verification: bool = False,
                             cycle_resonance: bool = False) -> dict:
        """真信号三要素判定
        
        基于Top 50大数据实证: 三要素全满足=真信号, 缺一存疑, 缺二必假
        
        Args:
            business_relevance: 催化与公司核心业务直接关联?
            financial_verification: 有可量化的财务/运营数据验证?
            cycle_resonance: 与行业/宏观周期同向共振?
        """
        elements = {
            "business_relevance": business_relevance,
            "financial_verification": financial_verification,
            "cycle_resonance": cycle_resonance,
        }
        score = sum(1 for v in elements.values() if v)

        if score == 3:
            verdict = "TRUE_SIGNAL"
            confidence = 0.85
            action = "可操作, 按催化级别执行T2/T3周期"
        elif score == 2:
            verdict = "WEAK_SIGNAL"
            confidence = 0.50
            missing = [k for k, v in elements.items() if not v]
            action = f"信号存疑, 缺少: {missing}"
        elif score == 1:
            verdict = "LIKELY_FALSE"
            confidence = 0.25
            action = "大概率假信号, 不建议操作"
        else:
            verdict = "FALSE_SIGNAL"
            confidence = 0.10
            action = "假信号, 远离"

        return {
            "event": event_name,
            "level": event_level,
            "verdict": verdict,
            "confidence": confidence,
            "triad_score": f"{score}/3",
            "elements": elements,
            "action": action,
        }

    def classify_false_signal(self, event_name: str, reason: str,
                              price_change_pct: float = 0,
                              window_days: int = 0) -> dict:
        """假信号四型态分类
        
        Args:
            reason: 'sell_on_news' | 'fundamentals_gap' | 'diminishing_returns' | 'noise_pollution'
        """
        if reason not in self.FALSE_SIGNAL_TYPES:
            # 自动推断
            if window_days <= 2 and abs(price_change_pct) < 3:
                reason = "noise_pollution"
            elif window_days <= 3 and price_change_pct > 0:
                reason = "sell_on_news"
            elif window_days >= 5 and price_change_pct < 5:
                reason = "fundamentals_gap"
            else:
                reason = "diminishing_returns"

        return {
            "event": event_name,
            "false_type": reason,
            "description": self.FALSE_SIGNAL_TYPES.get(reason, str(reason)),
            "price_change_pct": price_change_pct,
            "window_days": window_days,
            "action": "AVOID — 不以此催化为操作依据",
        }

    def compute_signal_strength(self, level: str, sector: str = "cyclical",
                                triad_score: int = 3,
                                stack_count: int = 1,
                                days_since_event: int = 0) -> dict:
        """综合信号强度计算
        
        整合: 催化级别 + 行业规律 + 三要素 + 叠加惩罚 + 时间衰减
        
        Returns:
            {"strength": 0-10, "verdict": str, "window_days": int, "tradeable": bool}
        """
        taxonomy = CATALYST_TAXONOMY.get(level, CATALYST_TAXONOMY["D"])
        sector_p = self.SECTOR_PROFILES.get(sector, self.SECTOR_PROFILES["cyclical"])

        # 基础强度: 催化级别
        base_strength = {"S": 8, "A": 6, "B": 4, "C": 2, "D": 0}.get(level, 0)

        # 三要素修正: 每缺一要素 -2
        triad_penalty = (3 - triad_score) * 2

        # 叠加惩罚: 每多一层 -1
        stack_penalty = max(0, stack_count - 1) * 1

        # 时间衰减: D+7后开始衰减
        time_decay = max(0, (days_since_event - 7) * 0.3) if days_since_event > 7 else 0

        # 行业基准修正
        sector_bonus = (sector_p["true_signal_rate"] - 0.55) * 3  # vs大盘55%基准

        strength = max(0, min(10, base_strength - triad_penalty - stack_penalty - time_decay + sector_bonus))

        if strength >= 7:
            verdict = "STRONG_SIGNAL"
            tradeable = True
        elif strength >= 5:
            verdict = "MODERATE_SIGNAL"
            tradeable = True
        elif strength >= 3:
            verdict = "WEAK_SIGNAL"
            tradeable = False
        else:
            verdict = "NO_SIGNAL"
            tradeable = False

        # 有效窗口 = 基准窗口 × (strength/10) / 叠加系数
        raw_window = taxonomy["full_decay_days"]
        effective_window = int(raw_window * (strength / 10) / max(1, 1 + (stack_count - 1) * 0.25))

        return {
            "strength": round(strength, 1),
            "verdict": verdict,
            "tradeable": tradeable,
            "effective_window_days": effective_window,
            "components": {
                "base_from_level": base_strength,
                "triad_penalty": -triad_penalty,
                "stack_penalty": -stack_penalty,
                "time_decay": round(-time_decay, 1),
                "sector_adjustment": round(sector_bonus, 1),
            },
        }

    def get_sector_profile(self, sector: str = "cyclical") -> dict:
        """获取行业催化规律档案"""
        return dict(self.SECTOR_PROFILES.get(sector, self.SECTOR_PROFILES["cyclical"]))
