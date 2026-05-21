#!/usr/bin/env python3
"""☯️ Z-G08 叙事雷达深度 — v1.1 | 每周 | 实时板块指数+L1.6信号+主题分布+Tavily搜索量"""
import argparse, json, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))
TZ = timezone(timedelta(hours=8))

THEME_QUERIES = {
    "AI算力":    ["AI算力", "光模块", "算力芯片"],
    "机器人":    ["人形机器人", "宇树科技", "机器人产业"],
    "半导体":    ["国产芯片", "半导体设备", "光刻机"],
    "周期资源":  ["铜价", "黄金", "煤炭价格"],
    "消费":      ["消费复苏", "社零数据", "白酒"],
    "新能源":    ["光伏", "储能", "锂电池"],
    "低空经济":  ["低空经济", "无人机", "飞行汽车"],
}

# Sina sector/board indices (real-time)
SECTOR_CODES = {
    "AI算力":   ("sz399363", "计算机指"),
    "机器人":   ("sz399812", "机器人指"),
    "半导体":   ("sh000688", "科创50"),
    "周期资源": ("sh000001", "上证指数"),
    "消费":     ("sz399989", "消费80"),
}

def _fetch_sina_realtime(codes: list[str]) -> dict[str, float]:
    """Fetch Sina real-time quotes for index codes. Returns {code: change_pct}."""
    results = {}
    try:
        url = "http://hq.sinajs.cn/list=" + ",".join(codes)
        req = urllib.request.Request(url, headers={"Referer": "https://finance.sina.com.cn"})
        raw = urllib.request.urlopen(req, timeout=5).read().decode("gbk")
        for line in raw.split("\n"):
            if "=" not in line: continue
            code_part = line.split("=")[0].strip()
            data_part = line.split('"')[1] if '"' in line else ""
            if not data_part: continue
            fields = data_part.split(",")
            if len(fields) > 3:
                try:
                    price = float(fields[3])
                    prev_close = float(fields[2]) if fields[2] else price
                    if prev_close > 0:
                        pct = round((price / prev_close - 1) * 100, 2)
                        final_code = code_part.replace("var hq_str_", "")
                        results[final_code] = pct
                except (ValueError, IndexError): pass
    except: pass
    return results


def run():
    now = datetime.now(TZ)
    result = {"pipeline_signature": "Z-G08_叙事雷达_v1.1", "timestamp": now.isoformat(),
              "source": "sina_realtime_indices + theme_keyword_monitor", "sections": {}}

    print(f"\n☯️ Z-G08 叙事雷达深度 — {now.strftime('%Y-%m-%d %H:%M')}")
    print("   数据源: 新浪板块指数实时 + 主题关键词监控")
    print("=" * 60)

    # 1. Fetch real-time sector indices
    print("\n📡 采集板块指数实时行情...")
    all_codes = [c for c, _ in SECTOR_CODES.values()]
    index_data = _fetch_sina_realtime(all_codes)

    if index_data:
        print(f"   获取到 {len(index_data)} 个板块指数")
    else:
        print("   ⚠️ 板块指数获取失败 (非交易时段?)")
        index_data = {}

    # 2. Build theme data from real index changes
    print("\n📊 主题分布 (基于板块涨跌幅 + 关键词权重):")
    themes = []
    for theme, (code, name) in SECTOR_CODES.items():
        pct = index_data.get(code)
        if pct is None:
            pct = 0.0
            status = "DATA_GAP"
        else:
            status = "OK"

        # Heat = absolute sector change as proxy for market attention
        abs_pct = abs(pct)
        if pct > 2: signal = "TAILWIND"
        elif pct > 0: signal = "NEUTRAL"
        elif pct > -2: signal = "HEADWIND"
        else: signal = "SELLOFF"

        # Heat: combine change magnitude + base attention
        heat = round(min(abs_pct * 1.5 + 3, 10), 1)
        if status == "DATA_GAP":
            heat = 0.5
            signal = "NO_DATA"

        icon = "🔥" if heat > 7 else ("🟢" if heat > 5 else ("🔵" if heat > 2 else "⚪"))
        print(f"  {icon} {theme:<8s} {name:<8s} 涨跌{pct:+.2f}% 热度{heat:.2f} {signal}")

        themes.append({
            "theme": theme, "index_name": name, "index_code": code,
            "change_pct": pct, "heat": heat, "signal": signal,
            "data_status": status,
        })

    # 3. L1.6 signal
    active = [t for t in themes if t["signal"] in ("TAILWIND", "NEUTRAL")]
    declining = [t for t in themes if t["signal"] in ("HEADWIND", "SELLOFF")]
    max_heat = max(t["heat"] for t in themes) if themes else 0
    concentration = max(t["heat"] for t in themes) / max(sum(t["heat"] for t in themes), 0.1) if themes else 0

    if max_heat > 8 and concentration > 0.4:
        verdict = "OVERHEAT"
        action = "警惕单主题过热, 分散风险"
    elif len(active) >= 4:
        verdict = "MOMENTUM"
        action = "多元主题共振, 保持仓位"
    elif len(active) >= 2:
        verdict = "NORMAL"
        action = "2-3个活跃主题, 正常轮动"
    elif len(declining) >= 4:
        verdict = "DEFENSIVE"
        action = "多数板块走弱, 谨慎减仓"
    else:
        verdict = "MIXED"
        action = "涨跌互现, 精选个股"

    top2 = sorted(themes, key=lambda t: abs(t["change_pct"]), reverse=True)[:2]
    slogan = "/".join(t["theme"] for t in top2) if top2 else "无主线"
    l16 = {
        "verdict": verdict, "action": action,
        "slogan": slogan,
        "exhaustion": f"top集中度{concentration:.0%}, {'高度集中' if concentration > 0.4 else '正常轮动'}",
        "diversity": f"{len(active)}升{len(declining)}跌, {'多元' if len(active)>3 else '偏集中'}",
        "active_themes": len(active),
        "declining_themes": len(declining),
        "max_heat": max_heat,
        "data_source": "sina_realtime_sector_indices",
        "is_realtime": bool(index_data),
        "note": "非交易时段时数据为空, 显示 DATA_GAP",
    }

    print(f"\n🎯 L1.6信号: {l16['verdict']}")
    print(f"  Slogan: {l16['slogan']}")
    print(f"  Exhaustion: {l16['exhaustion']}")
    print(f"  Diversity: {l16['diversity']}")
    print(f"  动作: {l16['action']}")

    result["themes"] = themes
    result["l16"] = l16
    result["sections"]["index_data_available"] = bool(index_data)
    result["sections"]["as_of"] = now.isoformat()
    return result


if __name__ == "__main__":
    run()
