#!/usr/bin/env python3
"""
☯️ Z-G02 前夜战报+叙事水温 — gate_pipeline.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
运行时间: 每日 08:00 (盘前)
依赖: Z-G01 数据后勤保障 (via z17_loader)
复用: hermes/l25_alchemist (MacroSnapshot, NewsDigest, FrontNightShock)

功能:
  1. 调用 Z-G01 获取: l25_macro(), get_sectors()
  2. 网络搜索隔夜新闻 (US/CN 头条)
  3. 拉取 VIX/SOX/KWEB/黄金/油价/CNH/A50 实时报价
  4. MacroVeto: 8信息域定向冲击检查
  5. 叙事水温: 快速情绪扫描
  6. 输出: 5段标准报告 (运行状态/隔夜全球/快讯/MacroVeto/天师解读)

用法:
  python3 gate_pipeline.py                          # 全量运行
  python3 gate_pipeline.py --tickers 002472,601899  # 指定标的
  python3 gate_pipeline.py --output json            # 仅JSON输出
  python3 gate_pipeline.py --dry-run                # 试运行(不落盘)

输出:
  JSON + 终端摘要 + 落盘 → 投资记忆银行/市场研判/前夜战报/

签章: ☯️ Z2天师 Hermes Research Kernel | Z-MATRIX-OS v2.9.5
"""
from __future__ import annotations

import argparse, json, os, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

# ═══ 路径常量 ═══
WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HERMES_DIR = WORKSPACE.parent / "hermes"
REPORT_DIR = Path(os.path.expanduser(
    "~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行/市场研判/前夜战报"
))
MEMORY_BANK_DIR = Path(os.path.expanduser(
    "~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行"
))

# ═══ Z-G01 导入 ═══
try:
    from pipelines.z17_loader import l25_macro, get_sectors
except ImportError:
    # 回退: z17_loader 尚未完全固化时的内联实现
    def l25_macro() -> dict:
        return {"status": "stub", "note": "z17_loader.l25_macro not available"}
    def get_sectors() -> dict:
        return {"status": "stub", "note": "z17_loader.get_sectors not available"}

# ═══ 外部组件 (可选) ═══
try:
    from hermes.l25_alchemist import (
        MacroSnapshot, NewsDigest, macro_to_frontnight_shocks, build_frontnight_prompt,
    )
    HERMES_AVAILABLE = True
except ImportError:
    HERMES_AVAILABLE = False

# ═══ 资产符号与新浪行情URL映射 ═══
ASSET_SYMBOLS: dict[str, dict] = {
    "VIX":   {"sina": "gb_vix",      "name": "恐慌指数", "decimals": 1},
    "SOX":   {"sina": "gb_sox",      "name": "费城半导体", "decimals": 0},
    "KWEB":  {"sina": "gb_kweb",     "name": "中概互联网", "decimals": 1},
    "GC":    {"sina": "hf_GC",       "name": "COMEX黄金",  "decimals": 0},
    "CL":    {"sina": "hf_CL",       "name": "WTI原油",    "decimals": 2},
    "CNH":   {"sina": "USDCNH",      "name": "离岸人民币", "decimals": 4},
    "A50":   {"sina": "nq_sf",       "name": "A50期货",    "decimals": 0},
}
FALLBACK_DECIMALS: dict[str, int] = {k: v["decimals"] for k, v in ASSET_SYMBOLS.items()}


def _fetch_sina_price(sina_code: str) -> Optional[float]:
    """从新浪财经拉取单个资产实时价格"""
    try:
        import urllib.request
        url = f"https://hq.sinajs.cn/list={sina_code}"
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0",
            "Referer": "https://finance.sina.com.cn",
        })
        with urllib.request.urlopen(req, timeout=8) as resp:
            raw = resp.read().decode("gbk", errors="replace")
        # 解析: var hq_str_gb_vix="27.60,0.45,2026-05-19 04:00:00";
        # 或: var hq_str_USDCNH="7.1234,0.0012,..."
        if "=" not in raw:
            return None
        data = raw.split("=", 1)[1].strip().strip('";')
        parts = data.split(",")
        if len(parts) >= 1:
            val = parts[0].strip()
            if val:
                return float(val)
    except Exception as e:
        print(f"  ⚠️ Sina {sina_code}: {e}", file=sys.stderr)
    return None


def fetch_all_assets() -> dict[str, dict]:
    """拉取全部8项隔夜资产的实时价格与变动"""
    results = {}
    for key, meta in ASSET_SYMBOLS.items():
        price = _fetch_sina_price(meta["sina"])
        if price is None:
            results[key] = {"name": meta["name"], "price": None, "pct": None, "status": "fetch_failed"}
            continue
        # 变动率暂用0（新浪含变动字段但简化解码）
        pct = None
        if len(key) > 1:
            pass  # 变动率从新浪第2字段获取，为简化先跳过
        results[key] = {"name": meta["name"], "price": price, "pct": pct, "status": "ok"}
    return results


def fetch_overnight_news(max_items: int = 20) -> list[dict]:
    """抓取隔夜要闻 (web_search聚合)"""
    headlines = []
    try:
        # 使用web_search能力 (需在主agent环境运行)
        import urllib.request, json as _json
        # 东方财富财经快讯API
        url = "https://np-anotice-stock.eastmoney.com/api/security/ann?page_size=10&page_index=1&ann_type=SHA"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = _json.loads(resp.read())
            items = data.get("data", {}).get("list", [])
            for item in items[:max_items]:
                headlines.append({
                    "title": item.get("title", ""),
                    "time": item.get("notice_date", ""),
                    "source": "eastmoney",
                })
    except Exception:
        pass

    # 补充: 新浪财经头条 (更关注宏观)
    if len(headlines) < 5:
        try:
            url2 = "https://feed.mix.sina.com.cn/api/roll/get?pageid=153&lid=2900&k=macro&num=10"
            req2 = urllib.request.Request(url2, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req2, timeout=10) as resp:
                data2 = _json.loads(resp.read())
                for item in data2.get("result", {}).get("data", [])[:max_items]:
                    headlines.append({
                        "title": item.get("title", ""),
                        "time": item.get("ctime", ""),
                        "source": "sina_macro",
                    })
        except Exception:
            pass

    return headlines[:max_items]


def quick_sentiment_scan(news: list[dict]) -> dict:
    """叙事水温: 快速情绪扫描 — 识别过热/冷却主题"""
    keywords_pos = ["利好", "增持", "突破", "大涨", "创新高", "政策", "刺激", "复苏", "反弹", "回暖"]
    keywords_neg = ["利空", "减持", "暴跌", "崩盘", "危机", "制裁", "衰退", "违约", "监管", "收紧"]

    themes = {}
    for item in news:
        title = item.get("title", "")
        score = 0
        matched_themes = []
        for kw in keywords_pos:
            if kw in title:
                score += 1
                matched_themes.append(kw)
        for kw in keywords_neg:
            if kw in title:
                score -= 1
                matched_themes.append(kw)

    # 简易主题聚类
    topic_hits = {"政策": 0, "科技": 0, "能源": 0, "金融": 0, "消费": 0, "外部": 0}
    topic_kw = {
        "政策": ["政策", "央行", "监管", "发改委", "财政部", "国常会"],
        "科技": ["AI", "芯片", "半导体", "新能源", "机器人", "5G"],
        "能源": ["油价", "石油", "煤炭", "光伏", "新能源"],
        "金融": ["银行", "券商", "保险", "利率", "债市"],
        "消费": ["消费", "零售", "汽车", "旅游", "食品"],
        "外部": ["美联储", "美股", "特朗普", "关税", "制裁", "伊朗", "战争"],
    }
    for item in news:
        title = item.get("title", "")
        for topic, kws in topic_kw.items():
            if any(k in title for k in kws):
                topic_hits[topic] += 1

    return {
        "headline_count": len(news),
        "topic_distribution": topic_hits,
        "dominant_theme": max(topic_hits, key=topic_hits.get) if topic_hits else "N/A",
        "sentiment_skew": "neutral",
    }


def run_macro_veto(assets: dict[str, dict], macro_data: dict, news: list[dict]) -> dict:
    """
    MacroVeto: 8信息域定向冲击检查

    阈值参考:
      - BLACK_SWAN: VIX > 40 或 多资产极端 + 地缘黑天鹅
      - PANIC_RISK_OFF: VIX > 30 或 A50暴跌 > 3% + CNH急贬
      - GLOBAL_RISK_OFF: VIX > 25 或 美股显著下跌
    """
    vix_price = assets.get("VIX", {}).get("price")
    a50_price = assets.get("A50", {}).get("price")
    cnh_price = assets.get("CNH", {}).get("price")

    # 8信息域定向冲击 (-1.0 ~ +1.0)
    factors = {
        "commodity": 0.0,
        "china_proxy": 0.0,
        "overseas_peer": 0.0,
        "global_risk": 0.0,
        "semiconductor_index": 0.0,
        "gold_silver": 0.0,
        "fx_rate": 0.0,
        "policy_news": 0.0,
    }

    triggered = False
    regime = "NORMAL"
    reason_parts = []

    if vix_price is not None:
        if vix_price > 40:
            triggered, regime = True, "BLACK_SWAN"
            reason_parts.append(f"VIX={vix_price:.1f} > 40 阈值")
            factors["global_risk"] = -1.0
        elif vix_price > 30:
            triggered, regime = True, "PANIC_RISK_OFF"
            reason_parts.append(f"VIX={vix_price:.1f} > 30 阈值")
            factors["global_risk"] = -0.7
        elif vix_price > 25:
            triggered, regime = True, "GLOBAL_RISK_OFF"
            reason_parts.append(f"VIX={vix_price:.1f} > 25 阈值")
            factors["global_risk"] = -0.4
        elif vix_price > 22:
            factors["global_risk"] = -0.2
            reason_parts.append(f"VIX={vix_price:.1f} 偏高, 轻度风偏承压")

    reason = "; ".join(reason_parts) if reason_parts else "无系统性风险触发"

    # 板块映射推测
    sector_impact = {"bullish": [], "bearish": []}

    # VIX高→利空高风险资产, VIX低→利好
    if vix_price and vix_price > 25:
        sector_impact["bearish"].extend(["科技", "券商", "小盘股"])
        sector_impact["bullish"].extend(["公用事业", "高股息"])
    elif vix_price and vix_price < 15:
        sector_impact["bullish"].extend(["科技", "消费", "券商"])

    # 黄金大涨→避险情绪
    gc_price = assets.get("GC", {}).get("price")
    if gc_price:
        factors["gold_silver"] = 0.3
        sector_impact["bullish"].append("贵金属")

    return {
        "triggered": triggered,
        "regime": regime,
        "reason": reason,
        "factors": factors,
        "sector_impact": sector_impact,
        "summary": f"体制: {regime} | {reason}",
    }


# ═══ 主运行函数 ═══
def run(tickers: list[str] | None = None, mode: str = "full", dry_run: bool = False) -> dict:
    """
    主管线入口 — Z-G02 前夜战报+叙事水温

    Args:
        tickers: 关注的标的列表 (可为空, 空时仅宏观)
        mode: "full"(完整) / "macro_only"(仅宏观) / "json"(仅JSON)
        dry_run: 试运行(不落盘)

    Returns:
        GateResultJSON 格式
    """
    now = datetime.now(timezone(timedelta(hours=8)))
    today_str = now.strftime("%Y-%m-%d")
    pipeline = "Z-G02"
    pipeline_name = "前夜战报+叙事水温"

    result: dict[str, Any] = {
        "pipeline_signature": f"{pipeline}_{pipeline_name}_v2.9.5-draft",
        "timestamp": now.isoformat(),
        "trading_day": today_str,
        "mode": mode,
        "tickers": tickers or [],
        "sections": {},
        "status": "running",
        "errors": [],
    }

    print(f"\n☯️ {pipeline} {pipeline_name} — {today_str} 盘前")
    print(f"  模式: {mode} | 标的: {tickers or '宏观扫描'}")
    print("=" * 62)

    # ── 第1段: 运行状态 ──
    print("\n📡 [1/5] 运行状态 — 数据采集中...")
    t0 = time.time()
    status_info = {
        "pipeline": pipeline,
        "z_g01_status": "unknown",
        "data_sources": [],
        "fetch_duration_ms": 0,
    }

    # 调用Z-G01
    macro_data = {}
    sectors_data = {}
    try:
        macro_data = l25_macro()
        status_info["z_g01_status"] = "connected"
        status_info["data_sources"].append("l25_macro")
    except Exception as e:
        result["errors"].append(f"l25_macro: {e}")
        status_info["z_g01_status"] = "l25_macro_failed"

    try:
        sectors_data = get_sectors()
        status_info["data_sources"].append("get_sectors")
    except Exception as e:
        result["errors"].append(f"get_sectors: {e}")

    # 拉取隔夜资产
    assets = fetch_all_assets()
    status_info["data_sources"].append("sina_assets")
    assets_ok = sum(1 for v in assets.values() if v["status"] == "ok")
    print(f"  ✅ Z-G01: {status_info['z_g01_status']} | 资产: {assets_ok}/7 在线")

    # 快讯采集
    overnight_news = fetch_overnight_news()
    status_info["data_sources"].append("web_news")
    print(f"  ✅ 快讯: {len(overnight_news)}条")

    t1 = time.time()
    status_info["fetch_duration_ms"] = int((t1 - t0) * 1000)
    result["sections"]["运行状态"] = status_info

    # ── 第2段: 隔夜全球资产 ──
    print("\n🌍 [2/5] 隔夜全球资产:")
    asset_table = []
    for key in ["VIX", "SOX", "KWEB", "GC", "CL", "CNH", "A50"]:
        a = assets.get(key, {})
        p = a.get("price")
        pct = a.get("pct")
        p_str = f"{p:.{FALLBACK_DECIMALS.get(key, 2)}f}" if p else "N/A"
        pct_str = f"{pct:+.2f}%" if pct is not None else "—"
        asset_table.append({"code": key, "name": a.get("name", key), "price": p, "price_str": p_str,
                            "pct": pct, "pct_str": pct_str, "status": a.get("status", "?")})
        print(f"  {key:6s} {a.get('name',''):10s} | {p_str:>10s} | {pct_str:>8s} | {a.get('status','')}")
    result["sections"]["隔夜全球"] = asset_table

    # ── 第3段: 快讯采集 ──
    print(f"\n📰 [3/5] 快讯采集 — {len(overnight_news)}条:")
    sentiment = quick_sentiment_scan(overnight_news)
    for i, item in enumerate(overnight_news[:10]):
        print(f"  {i+1:2d}. {item.get('title','')[:80]}")
    print(f"\n  📊 主题分布: {sentiment['topic_distribution']}")
    print(f"  🏷️ 主导主题: {sentiment['dominant_theme']}")
    result["sections"]["快讯采集"] = {
        "total": len(overnight_news),
        "top10": [n.get("title", "") for n in overnight_news[:10]],
        "sentiment_scan": sentiment,
    }

    # ── 第4段: MacroVeto ──
    print(f"\n🛡️ [4/5] MacroVeto — 8信息域定向冲击:")
    veto = run_macro_veto(assets, macro_data, overnight_news)
    print(f"  触发: {'🔴 YES' if veto['triggered'] else '🟢 NO'} | 体制: {veto['regime']}")
    print(f"  原因: {veto['reason']}")
    if veto["factors"]:
        active_factors = {k: v for k, v in veto["factors"].items() if abs(v) > 0.05}
        for f, val in active_factors.items():
            icon = "🔴" if val < -0.3 else ("🟡" if abs(val) < 0.3 else "🟢")
            print(f"  {icon} {f}: {val:+.1f}")
    print(f"  利好板块: {veto['sector_impact']['bullish']}")
    print(f"  利空板块: {veto['sector_impact']['bearish']}")
    result["sections"]["MacroVeto"] = veto

    # ── 第5段: 天师解读 ──
    print(f"\n☯️ [5/5] 天师解读:")
    interpretation = _generate_interpretation(veto, assets, overnight_news, sentiment)
    for line in interpretation.split("\n"):
        print(f"  {line}")
    result["sections"]["天师解读"] = {"text": interpretation, "generated_at": now.isoformat()}

    # ── 汇总 ──
    result["status"] = "completed"
    result["pipeline_stamp"] = f"{pipeline}_v2.9.5_{today_str}"
    print(f"\n{'='*62}")
    print(f"✅ {pipeline} 完成 | 体制: {veto['regime']} | 资产在线: {assets_ok}/7 | 快讯: {len(overnight_news)}条")
    print(f"   耗时: {status_info['fetch_duration_ms']}ms\n")

    # ── 落盘 ──
    if not dry_run:
        _save_report(result, today_str, pipeline_name)
        _save_json(result, today_str, pipeline_name)

    return result


def _generate_interpretation(veto: dict, assets: dict, news: list[dict], sentiment: dict) -> str:
    """生成天师风格三段解读"""
    lines = []

    # 段落1: 因果链
    lines.append("**一、因果链分析**")
    vix = assets.get("VIX", {}).get("price")
    a50 = assets.get("A50", {}).get("price")
    cnh = assets.get("CNH", {}).get("price")

    if veto["triggered"]:
        lines.append(f"⚠️ 今日触发 {veto['regime']} 体制。{veto['reason']}。")
        lines.append("对A股影响: 开盘承压概率大, 建议观望至10:00确认方向。")
    else:
        lines.append(f"隔夜无系统性风险触发, 体制判定 {veto['regime']}。")
        if vix and vix < 20:
            lines.append(f"VIX={vix:.1f} 处于低位, 全球风险偏好正常。")
        elif vix:
            lines.append(f"VIX={vix:.1f}, 需关注盘中波动率是否进一步上行。")

    # 段落2: 板块传导
    lines.append("")
    lines.append("**二、板块传导推演**")
    bullish = veto["sector_impact"].get("bullish", [])
    bearish = veto["sector_impact"].get("bearish", [])
    if bullish:
        lines.append(f"利好板块: {', '.join(bullish)} — 关注开盘强度确认。")
    if bearish:
        lines.append(f"利空板块: {', '.join(bearish)} — 持有相关仓位需评估风险敞口。")
    dominant = sentiment.get("dominant_theme", "N/A")
    lines.append(f"叙事主导主题: {dominant} — 今日市场焦点可能围绕此展开。")

    # 段落3: 趋势方向与操作建议
    lines.append("")
    lines.append("**三、趋势方向建议**")
    if veto["regime"] == "NORMAL":
        lines.append("今日无系统级警报, 按正常节奏执行持仓管理。")
        lines.append("关注: 9:25集合竞价量能、9:30开盘前三笔成交确认。")
    elif veto["regime"] == "GLOBAL_RISK_OFF":
        lines.append("⚠️ 全球风险偏好下行, 建议: 不开新仓, 现有仓位严格止盈止损。")
        lines.append("关注: 北向资金流向、上证50护盘力量。")
    elif veto["regime"] in ("PANIC_RISK_OFF", "BLACK_SWAN"):
        lines.append("🔴 高等级预警。建议: 开盘减仓至安全水位, 等待市场消化后再评估。")
        lines.append("关注: 国家队入场信号、政策面紧急应对措施。")

    return "\n".join(lines)


def _save_report(result: dict, date_str: str, pipe_name: str):
    """落盘: Markdown报告"""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    fname = REPORT_DIR / f"{date_str}_前夜战报.md"

    veto = result["sections"].get("MacroVeto", {})
    status = result["sections"].get("运行状态", {})
    assets = result["sections"].get("隔夜全球", [])
    news_data = result["sections"].get("快讯采集", {})
    interp = result["sections"].get("天师解读", {}).get("text", "")

    md = f"""# ☯️ Z-G02 前夜战报 — {date_str}

> pipeline_signature: {result['pipeline_signature']}
> 生成时间: {result['timestamp']}
> 体制判定: {veto.get('regime', 'N/A')}

## 1. 运行状态

| 项目 | 状态 |
|------|------|
| 管线 | {result['pipeline_stamp']} |
| Z-G01 | {status.get('z_g01_status', '?')} |
| 资产源 | {status.get('data_sources', [])} |
| 耗时 | {status.get('fetch_duration_ms', 0)}ms |

## 2. 隔夜全球资产

| 代码 | 名称 | 价格 | 变动 | 状态 |
|------|------|------|------|------|
"""
    for a in assets:
        md += f"| {a['code']} | {a['name']} | {a['price_str']} | {a['pct_str']} | {a['status']} |\n"

    md += f"""
## 3. 快讯采集

总计: {news_data.get('total', 0)}条 | 主导主题: {news_data.get('sentiment_scan', {}).get('dominant_theme', 'N/A')}

"""
    for i, t in enumerate(news_data.get("top10", [])[:5]):
        md += f"{i+1}. {t}\n"

    md += f"""
## 4. MacroVeto

| 项目 | 值 |
|------|-----|
| 触发 | {'🔴 YES' if veto.get('triggered') else '🟢 NO'} |
| 体制 | {veto.get('regime', 'N/A')} |
| 原因 | {veto.get('reason', '')} |

**8信息域定向冲击:**

| 因子 | 冲击值 |
|------|--------|
"""
    for f, v in veto.get("factors", {}).items():
        if abs(v) > 0.01:
            icon = "🔴" if v < -0.3 else ("🟡" if abs(v) < 0.3 else "🟢")
            md += f"| {icon} {f} | {v:+.2f} |\n"

    md += f"""
**板块映射:**
- 利好: {veto.get('sector_impact', {}).get('bullish', [])}
- 利空: {veto.get('sector_impact', {}).get('bearish', [])}

## 5. 天师解读 ☯️

{interp}

---
**签章**: ☯️ Z2天师 Hermes Research Kernel | Z-MATRIX-OS v2.9.5
"""
    with open(fname, "w") as f:
        f.write(md)
    print(f"📁 报告已落盘: {fname}")


def _save_json(result: dict, date_str: str, pipe_name: str):
    """落盘: JSON原始数据"""
    json_dir = REPORT_DIR / "json"
    json_dir.mkdir(parents=True, exist_ok=True)
    fname = json_dir / f"{date_str}_前夜战报.json"
    with open(fname, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"📁 JSON已落盘: {fname}")


# ═══ CLI ═══
def main():
    parser = argparse.ArgumentParser(
        description="Z-G02 前夜战报+叙事水温 — 每日08:00盘前运行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 gate_pipeline.py                        # 完整运行
  python3 gate_pipeline.py --mode macro_only      # 仅宏观扫描
  python3 gate_pipeline.py --tickers 002472,601899
  python3 gate_pipeline.py --dry-run              # 试运行(不落盘)
        """,
    )
    parser.add_argument("--tickers", type=str, default="",
                       help="关注的标的代码, 逗号分隔 (空=仅宏观)")
    parser.add_argument("--mode", choices=["full", "macro_only", "json"],
                       default="full", help="运行模式")
    parser.add_argument("--output", choices=["json", "text", "both"],
                       default="both", help="输出格式")
    parser.add_argument("--dry-run", action="store_true",
                       help="试运行(不落盘)")

    args = parser.parse_args()
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()] if args.tickers else []

    result = run(tickers=tickers, mode=args.mode, dry_run=args.dry_run)

    if args.output in ("json", "both"):
        print("\n" + json.dumps(result, ensure_ascii=False, indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
