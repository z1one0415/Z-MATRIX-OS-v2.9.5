"""
Z2天师 Hermes — 情绪与叙事雷达 (v1.0)
爬虫采集 → Z2天师自提取 → NarrativeMetrics → L1.6 → EventStore

设计:
- Z2天师用自己的 deepseek-v4-pro 做叙事分析, 不依赖 gemma4
- 爬虫用 OpenClaw web_fetch + Python beautifulsoup4
- 成本 ~$0.012/次, ~$1/月
- 输出写入 EventStore, 供 L1.6 Node 读取拦截

定时: 07:30 盘前 / 11:30 午间 / 14:30 尾盘
"""
from __future__ import annotations

import json
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hermes.narrative_models import NarrativeSource, NarrativeEntropyEvent
from hermes.narrative_prompts import NARRATIVE_ANALYSIS_PROMPT


class NarrativeRadar:
    """情绪与叙事雷达 — Z2天师自驱动版"""

    def __init__(self, memory_dir: str | None = None):
        self.memory_dir = Path(memory_dir) if memory_dir else Path(
            "/Users/z1/.openclaw/agents/z2-analyst/workspace/hermes/narrative_memory"
        )
        self.memory_dir.mkdir(parents=True, exist_ok=True)

    # ═══ 数据采集 ═══

    def scrape_cls(self) -> list[NarrativeSource]:
        """财联社24小时电报 (待实现: web_fetch cls.cn)"""
        return []  # 实际实现: web_fetch + HTML解析

    def scrape_xueqiu(self) -> list[NarrativeSource]:
        """雪球热帖 (待实现: requests + 解析)"""
        return []

    def scrape_taoguba(self) -> list[NarrativeSource]:
        """淘股吧散户区 (待实现: web_fetch + 正则)"""
        return []

    def scrape_xuangubao(self) -> list[NarrativeSource]:
        """选股宝题材热度 (待实现: web_fetch)"""
        return []

    def collect_all(self) -> list[NarrativeSource]:
        """全量采集 — 四个渠道"""
        sources = []
        for scraper in [self.scrape_cls, self.scrape_xueqiu,
                         self.scrape_taoguba, self.scrape_xuangubao]:
            try:
                sources.extend(scraper())
            except Exception:
                pass
        return sources

    # ═══ 叙事分析 ═══

    def build_analysis_prompt(self, sources: list[NarrativeSource]) -> str:
        """构造分析输入 — 拼接所有采集文本"""
        texts = []
        for s in sources:
            segment = f"[{s.channel}] {s.title}\n{s.body[:300]}"
            texts.append(segment)

        combined = "\n---\n".join(texts)
        return NARRATIVE_ANALYSIS_PROMPT.format(sources_text=combined[:8000])

    def parse_analysis_result(self, raw_json: str) -> dict[str, Any]:
        """解析 Z2天师的分析输出"""
        try:
            # 提取 JSON 块
            start = raw_json.find("{")
            end = raw_json.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(raw_json[start:end])
        except json.JSONDecodeError:
            pass
        return {
            "slogan_repetition_ratio": 0.5,
            "marginal_buyer_exhaustion": 0.5,
            "narrative_diversity": 0.5,
            "narrative_acceleration": 0.0,
            "dominant_emotion": "unknown",
            "top_narratives": [],
            "summary": "解析失败",
        }

    # ═══ L1.6 信号生成 ═══

    def compute_l16_signal(self, metrics: dict[str, Any]) -> tuple[str, str]:
        """
        根据 NarrativeMetrics 计算 L1.6 信号和动作

        返回: (signal, action)
        """
        slogan = float(metrics.get("slogan_repetition_ratio", 0))
        exhaustion = float(metrics.get("marginal_buyer_exhaustion", 0))
        diversity = float(metrics.get("narrative_diversity", 1))
        emotion = str(metrics.get("dominant_emotion", "neutral"))

        # 狂热预警
        if slogan > 0.7 and exhaustion > 0.5:
            return ("MANIA_WARNING", "RESTRICT_NEW_ENTRY")
        if slogan > 0.6 and emotion == "greed":
            return ("MANIA_BUILDING", "CLOSE_NEW_MANIA")

        # 投降信号
        if diversity < 0.2 and emotion == "fear":
            return ("CAPITULATION_SIGNAL", "MARK_CONTRARIAN_OPPORTUNITY")
        if exhaustion > 0.8 and emotion == "fear":
            return ("CAPITULATION_FORMING", "PREPARE_REVERSE_WATCH")

        # 叙事崩溃
        if diversity < 0.15:
            return ("NARRATIVE_COLLAPSE", "DEFENSIVE_ONLY")

        return ("NEUTRAL", "NO_ACTION")

    # ═══ 全流程 ═══

    def run_full_scan(self, analysis_result: dict[str, Any] | None = None) -> NarrativeEntropyEvent:
        """
        全流程: 采集(可选) → 分析 → 计算 → Event

        analysis_result: 如果提供, 跳过爬虫采集, 直接使用分析结果
        (主代理用 subagent 完成 LLM 分析后传入)
        """
        now = datetime.now(timezone.utc)
        metrics = analysis_result or {}

        # 计算 L1.6 信号
        signal, action = self.compute_l16_signal(metrics)

        # 构建事件
        event = NarrativeEntropyEvent(
            scan_time=now.isoformat(),
            sources_scanned=0,  # 由调用方填充
            slogan_repetition_ratio=float(metrics.get("slogan_repetition_ratio", 0)),
            marginal_buyer_exhaustion=float(metrics.get("marginal_buyer_exhaustion", 0)),
            narrative_diversity=float(metrics.get("narrative_diversity", 0)),
            narrative_acceleration=float(metrics.get("narrative_acceleration", 0)),
            dominant_emotion=str(metrics.get("dominant_emotion", "neutral")),
            top_narratives=list(metrics.get("top_narratives", [])),
            l16_signal=signal,
            l16_action=action,
            evidence_hash=hashlib.sha256(
                json.dumps(metrics, sort_keys=True, default=str).encode()
            ).hexdigest()[:16],
        )

        # 持久化到记忆
        self._save_event(event)

        return event

    # ═══ 持久化 ═══

    def _save_event(self, event: NarrativeEntropyEvent) -> None:
        """写入叙事记忆文件"""
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filepath = self.memory_dir / f"{day}_narrative.jsonl"

        with open(filepath, "a") as f:
            f.write(json.dumps(event.to_dict(), ensure_ascii=False, default=str) + "\n")

    def load_latest(self) -> dict[str, Any] | None:
        """加载最近一次扫描结果"""
        files = sorted(self.memory_dir.glob("*_narrative.jsonl"), reverse=True)
        if not files:
            return None
        lines = files[0].read_text().strip().split("\n")
        if lines:
            return json.loads(lines[-1])
        return None

    def get_today_events(self) -> list[dict[str, Any]]:
        """获取今日所有叙事事件"""
        day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        filepath = self.memory_dir / f"{day}_narrative.jsonl"
        if not filepath.exists():
            return []
        events = []
        for line in filepath.read_text().strip().split("\n"):
            if line:
                events.append(json.loads(line))
        return events


# 全局单例
_radar: NarrativeRadar | None = None


def get_narrative_radar() -> NarrativeRadar:
    global _radar
    if _radar is None:
        _radar = NarrativeRadar()
    return _radar
