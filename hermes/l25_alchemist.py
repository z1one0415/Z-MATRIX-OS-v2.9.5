"""
Z-MATRIX-OS v2.9.2 — L2.5 前夜战报增强管线
yfinance → RSS爬虫 → Z2天师炼丹炉 → FrontNightShock → LangGraph流A

调用链: 08:00 yfinance采集 → 08:01 RSS快讯 → 08:02 Z2天师合成 → 08:03 MacroVeto/chain_delta
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class MacroSnapshot:
    """隔夜全球资产快照"""
    vix: float = 0.0; vix_pct: float = 0.0; vix_3sigma: bool = False
    sox: float = 0.0; sox_pct: float = 0.0
    kweb: float = 0.0; kweb_pct: float = 0.0
    gold: float = 0.0; gold_pct: float = 0.0
    copper: float = 0.0; copper_pct: float = 0.0
    tnx: float = 0.0; tnx_pct: float = 0.0
    cnh: float = 0.0; cnh_pct: float = 0.0
    a50: float = 0.0; a50_pct: float = 0.0
    timestamp: str = ""

    def to_prompt_text(self) -> str:
        alerts = []
        if self.vix_3sigma: alerts.append("⚠️ VIX突破3σ")
        return f"""VIX: {self.vix:.1f} ({self.vix_pct:+.1%}) {'[3σ]' if self.vix_3sigma else ''}
SOX: {self.sox:.0f} ({self.sox_pct:+.1%})
KWEB: {self.kweb:.1f} ({self.kweb_pct:+.1%})
黄金: {self.gold:.0f} ({self.gold_pct:+.1%})
铜: {self.copper:.2f} ({self.copper_pct:+.1%})
美债10Y: {self.tnx:.2f}% ({self.tnx_pct:+.1%})
CNH: {self.cnh:.4f} ({self.cnh_pct:+.1%})
A50期货: {self.a50:.0f} ({self.a50_pct:+.1%})
{'警报: ' + '; '.join(alerts) if alerts else '无极端异动'}"""


@dataclass
class NewsDigest:
    """隔夜快讯摘要"""
    headlines: list[str] = field(default_factory=list)
    source_count: int = 0
    keywords: list[str] = field(default_factory=list)

    def to_prompt_text(self) -> str:
        if not self.headlines:
            return "无快讯数据"
        return "\n".join(f"- {h}" for h in self.headlines[:15])


Z2_ALCHEMIST_PROMPT = """你是 Z-MATRIX 宏观战情分析师。现在是 {trading_day} 早上 08:15。

## 量化异动
{macro_data}

## 隔夜快讯
{news_data}

## 任务

### 1. 尾部风险判决 (MacroVeto)
评估上述组合是否构成需要否决所有进攻的市场体制。如果是，直接输出Veto，停止后续。
- BLACK_SWAN: VIX>40 或 多资产同时极端 + 地缘/政策黑天鹅
- PANIC_RISK_OFF: VIX>30 或 A50暴跌>3% + CNH急贬
- GLOBAL_RISK_OFF: VIX>25 或 美股显著下跌

### 2. 八大因子定向冲击
如果未触发Veto，翻译为8信息域的定向冲击 (-1.0到1.0):
- commodity: 商品传导
- china_proxy: 中国资产代理
- overseas_peer: 海外对标
- global_risk: 全球风险偏好
- semiconductor_index: 半导体传导
- gold_silver: 贵金属传导
- fx_rate: 汇率传导
- policy_news: 政策新闻

### 3. SW31板块映射
指出隔夜事件利好哪些A股板块，利空哪些。

## 输出格式
```json
{{
    "macro_veto": {{
        "triggered": true|false,
        "regime": "NORMAL"|"GLOBAL_RISK_OFF"|"PANIC_RISK_OFF"|"BLACK_SWAN",
        "reason": "触发原因"
    }},
    "factors": {{
        "commodity": 0.0, "china_proxy": 0.0, "overseas_peer": 0.0,
        "global_risk": 0.0, "semiconductor_index": 0.0, "gold_silver": 0.0,
        "fx_rate": 0.0, "policy_news": 0.0
    }},
    "sector_impact": {{
        "bullish": ["板块1"],
        "bearish": ["板块2"]
    }},
    "summary": "一句话总结"
}}
```
"""


def build_frontnight_prompt(
    trading_day: str,
    macro: MacroSnapshot,
    news: NewsDigest,
) -> str:
    """构造 Z2天师炼丹炉输入"""
    return Z2_ALCHEMIST_PROMPT.format(
        trading_day=trading_day,
        macro_data=macro.to_prompt_text(),
        news_data=news.to_prompt_text(),
    )


def parse_alchemist_output(raw: str) -> dict[str, Any]:
    """解析Z2天师JSON输出"""
    try:
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start >= 0 and end > start:
            return json.loads(raw[start:end])
    except json.JSONDecodeError:
        pass
    return {
        "macro_veto": {"triggered": False, "regime": "NORMAL", "reason": "parse_failed"},
        "factors": {},
        "sector_impact": {"bullish": [], "bearish": []},
        "summary": "解析失败",
    }


def macro_to_frontnight_shocks(macro: MacroSnapshot) -> list[dict[str, Any]]:
    """MacroSnapshot → FrontNightShock[] (给现有L2.5管道用)"""
    shocks = []
    for name, value, direction in [
        ("US_VIX", macro.vix_pct, "headwind" if macro.vix_pct > 0 else "tailwind"),
        ("US_SOX", macro.sox_pct, "tailwind" if macro.sox_pct > 0 else "headwind"),
        ("KWEB", macro.kweb_pct, "tailwind" if macro.kweb_pct > 0 else "headwind"),
        ("GOLD", macro.gold_pct, "tailwind" if macro.gold_pct > 0 else "headwind"),
        ("COPPER", macro.copper_pct, "tailwind" if macro.copper_pct > 0 else "headwind"),
        ("CNH", macro.cnh_pct, "headwind" if macro.cnh_pct > 0 else "tailwind"),
        ("A50", macro.a50_pct, "tailwind" if macro.a50_pct > 0 else "headwind"),
    ]:
        shocks.append({
            "factor": name, "family": "macro",
            "value": abs(value), "direction": direction,
            "confidence": 0.85,
            "raw_change_pct": round(value * 100, 2),
            "note": f"{name}: {value:+.1%}",
        })
    return shocks
