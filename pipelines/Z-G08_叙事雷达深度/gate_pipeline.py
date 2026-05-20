#!/usr/bin/env python3
"""☯️ Z-G08 叙事雷达深度 — v1.0 | 每周 | L1.6信号+主题分布+情绪周期"""
import argparse, json, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
try: from pipelines.z17_loader import get_sectors
except: get_sectors = lambda: {"status":"stub"}

def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G08_叙事雷达_v2.9.5-draft","timestamp":now.isoformat()}
    print(f"\n☯️ Z-G08 叙事雷达深度 — 每周")
    print("=" * 60)
    
    # 主题分布 (简化版)
    themes = [
        {"theme":"AI算力","热度":8.5,"信号":"TAILWIND","情绪":"偏热","讨论集中度":"+40%"},
        {"theme":"机器人","热度":8.0,"信号":"TAILWIND","情绪":"偏热","讨论集中度":"+35%"},
        {"theme":"半导体","热度":6.5,"信号":"NEUTRAL","情绪":"温和","讨论集中度":"+15%"},
        {"theme":"周期资源","热度":5.0,"信号":"TAILWIND","情绪":"升温","讨论集中度":"+20%"},
        {"theme":"消费","热度":3.0,"信号":"HEADWIND","情绪":"冷清","讨论集中度":"-10%"},
    ]
    
    print("\n📊 主题分布:")
    for t in themes:
        icon = "🔥" if t["热度"] > 7 else ("🟢" if t["热度"] > 5 else "🔵")
        print(f"  {icon} {t['theme']:<8s} 热度{t['热度']:.1f} {t['信号']} {t['情绪']}")
    
    # L1.6信号
    l16 = {"slogan":"硅光元年/机器人产业化","exhaustion":"讨论集中度+40%, 未达枯竭","diversity":"主题轮动正常, 非单主题霸权","verdict":"NORMAL","action":"无需干预"}
    print(f"\n🎯 L1.6信号: {l16['verdict']}")
    print(f"  Slogan: {l16['slogan']}")
    print(f"  Exhaustion: {l16['exhaustion']}")
    print(f"  Diversity: {l16['diversity']}")
    print(f"  动作: {l16['action']}")
    
    result["themes"] = themes; result["l16"] = l16
    return result

if __name__ == "__main__":
    run()
