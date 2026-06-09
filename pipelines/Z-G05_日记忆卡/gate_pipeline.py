#!/usr/bin/env python3
"""
☯️ Z-G05 日记忆卡 — gate_pipeline.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
运行时间: 每日 15:30 (盘后)
依赖: Z-G01 数据后勤保障 (via z17_loader)
复用: hermes/daily_card (日记忆卡结构)

功能:
  1. 调用 Z-G01 获取: market_truth() 对所有持仓标的
  2. 从 MEMORY.md 读取当前持仓
  3. 生成当日记忆卡: 市场快照 + 持仓追踪 + 催化剂状态
  4. 自动追加到 MEMORY.md
  5. 输出: Markdown格式日卡

用法:
  python3 gate_pipeline.py                          # 全量运行
  python3 gate_pipeline.py --tickers 002472,601899  # 仅追踪指定标的
  python3 gate_pipeline.py --dry-run                # 试运行(不落盘)
  python3 gate_pipeline.py --output json            # 仅JSON

输出:
  JSON + 终端摘要 + Markdown日卡 + MEMORY.md自动追加

签章: ☯️ Z2天师 Hermes Research Kernel | Z-MATRIX-OS v2.9.5
"""
from __future__ import annotations

import argparse, json, os, re, sys, time
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Optional

# ═══ 路径常量 ═══
WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
DAILY_CARDS_DIR = WORKSPACE.parent / "记忆宫殿" / "Z2信息熔炉" / "投资记忆银行" / "日记忆卡"
REPORT_ROOT = Path(os.path.expanduser(
    "~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行"
))

# ═══ Z-G01 导入 ═══
try:
    from pipelines.z17_loader import market_truth, dq_score, l4_health
except ImportError:
    from zmatrix.core.degraded_contract import dependency_unavailable
    def market_truth(tickers: list[str] | None = None) -> dict:
        return dependency_unavailable("z17_loader.market_truth", "z17_loader unavailable", "RESTORE_Z01_DATA_PIPELINE")
    def dq_score() -> dict:
        return dependency_unavailable("z17_loader.dq_score", "z17_loader unavailable", "RESTORE_Z01_DATA_PIPELINE")
    def l4_health() -> dict:
        return dependency_unavailable("z17_loader.l4_health", "z17_loader unavailable", "RESTORE_Z01_DATA_PIPELINE")


# ═══ 持仓解析 ═══
def parse_positions_from_memory(memory_path: Path) -> list[dict]:
    """从 MEMORY.md 解析当前持仓"""
    positions = []
    if not memory_path.exists():
        return positions
    with open(memory_path) as f:
        text = f.read()

    # 匹配持仓表格: | 双环传动 002472 | 1800股 | 41.71 | 44.01 | 🟢 +4,140 |
    # 格式: | 名称 代码 | 持仓量 | 成本 | 现价 | 浮盈/亏 | 日变动 |
    pos_pattern = re.compile(
        r'\|\s*([^|]+?)\s+(\d{6})\s*\|'
        r'\s*([\d,]+股)\s*\|'
        r'\s*([\d.]+)\s*\|'
        r'\s*([\d.]+)\s*\|'
        r'\s*([🔴🟢🟡]?\s*[-+][\d,]+)'
    )
    for m in pos_pattern.finditer(text):
        name = m.group(1).strip()
        code = m.group(2).strip()
        shares_str = m.group(3).strip().replace("股", "").replace(",", "")
        cost = float(m.group(4))
        price = float(m.group(5))
        pnl_str = m.group(6).strip()
        try:
            shares = int(shares_str)
        except ValueError:
            shares = 0
        # 解析浮盈/亏数值
        pnl_num = 0
        pnl_match = re.search(r'[-+]([\d,]+)', pnl_str)
        if pnl_match:
            pnl_num = float(pnl_match.group().replace(",", ""))
        positions.append({
            "code": code, "name": name, "shares": shares,
            "cost": cost, "price_last": price, "pnl": pnl_num,
            "pnl_str": pnl_str,
        })

    return positions


def fetch_live_prices_for_positions(positions: list[dict]) -> dict[str, dict]:
    """为持仓标的获取实时价格 (东方财富API)"""
    if not positions:
        return {}
    codes = [p["code"] for p in positions]
    try:
        import urllib.request
        def secid(c):
            return f"1.{c}" if c[0] in "569" else f"0.{c}"
        secids = [secid(c) for c in codes]
        url = ("https://push2.eastmoney.com/api/qt/ulist.np/get"
               f"?fltt=2&fields=f2,f3,f4,f5,f8,f10,f12,f14&secids={','.join(secids)}")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        results = {}
        for item in data.get("data", {}).get("diff", []):
            code = item.get("f12", "")
            results[code] = {
                "name": item.get("f14", "?"),
                "price": item.get("f2"),
                "pct": item.get("f3"),
                "high": item.get("f4"),
                "low": item.get("f5"),
                "open": item.get("f8"),
                "volume": item.get("f10"),
            }
        return results
    except Exception as e:
        print(f"  ⚠️ 实时价格获取失败: {e}", file=sys.stderr)
        return {}


def get_market_snapshot() -> dict:
    """获取大盘快照 — 上证/深证/创业板"""
    try:
        import urllib.request
        url = ("https://push2.eastmoney.com/api/qt/ulist.np/get"
               "?fltt=2&fields=f2,f3,f4,f5,f12,f14&secids=1.000001,0.399001,0.399006")
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())
        indices = {}
        name_map = {"000001": "上证指数", "399001": "深证成指", "399006": "创业板指"}
        for item in data.get("data", {}).get("diff", []):
            code = item.get("f12", "")
            indices[code] = {
                "name": name_map.get(code, item.get("f14", "?")),
                "price": item.get("f2"),
                "pct": item.get("f3"),
            }
        return indices
    except Exception:
        return {"000001": {"error": "fetch_failed"}}


# ═══ 主运行函数 ═══
def run(tickers: list[str] | None = None, mode: str = "full", dry_run: bool = False) -> dict:
    """
    主管线入口 — Z-G05 日记忆卡

    Args:
        tickers: 额外关注的标的代码 (为空则使用 MEMORY.md 持仓)
        mode: "full" / "positions_only" / "json"
        dry_run: 试运行(不追加MEMORY.md)

    Returns:
        GateResultJSON 格式
    """
    now = datetime.now(timezone(timedelta(hours=8)))
    today_str = now.strftime("%Y-%m-%d")
    pipeline = "Z-G05"
    pipeline_name = "日记忆卡"

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

    print(f"\n☯️ {pipeline} {pipeline_name} — {today_str} 盘后 15:30")
    print(f"  模式: {mode} | 标的: {tickers or 'MEMORY.md持仓'}")
    print("=" * 62)

    # ── 第1段: 运行状态 ──
    print("\n📡 [1/4] 运行状态 — 数据采集中...")
    t0 = time.time()

    # 加载持仓
    positions = parse_positions_from_memory(MEMORY_MD)
    print(f"  ✅ 持仓解析: {len(positions)}只标的")
    for p in positions:
        print(f"     {p['code']} {p['name']}: {p['shares']}股 成本{p['cost']}")

    # 拉取实时价格
    live_prices = fetch_live_prices_for_positions(positions)
    print(f"  ✅ 实时价格: {len(live_prices)}只标的上线")

    # 大盘快照
    indices = get_market_snapshot()
    print(f"  ✅ 大盘快照: {len(indices)}个指数")

    # Z-G01 市场真相
    mtruth = {}
    try:
        mtruth = market_truth([p["code"] for p in positions] if positions else None)
        print(f"  ✅ Z-G01 market_truth: 已获取")
    except Exception as e:
        result["errors"].append(f"market_truth: {e}")
        mtruth = {"error": str(e)}

    t1 = time.time()
    status_info = {
        "positions_count": len(positions),
        "live_prices_ok": len(live_prices),
        "indices_count": len(indices),
        "z_g01_status": "ok" if "error" not in mtruth else "partial",
        "fetch_duration_ms": int((t1 - t0) * 1000),
    }
    result["sections"]["运行状态"] = status_info

    # ── 第2段: 市场快照 ──
    print(f"\n📊 [2/4] 市场快照:")
    snapshot = {"indices": {}, "positions_tracking": [], "portfolio_summary": {}}
    for code, idx in indices.items():
        p = idx.get("price")
        pct = idx.get("pct")
        icon = "🔴" if (pct or 0) < -1 else ("🟢" if (pct or 0) > 1 else "⚪")
        snapshot["indices"][code] = idx
        p_str = f"{p:.2f}" if p else "N/A"
        pct_str = f"{pct:+.2f}%" if pct is not None else "—"
        print(f"  {icon} {idx.get('name', code):8s} {p_str:>10s} {pct_str:>8s}")

    # 持仓追踪表
    total_cost = 0.0
    total_value = 0.0
    print(f"\n  📋 持仓追踪:")
    print(f"  {'代码':<8s} {'名称':<10s} {'持仓':>6s} {'成本':>8s} {'现价':>8s} {'市值':>10s} {'浮盈/亏':>10s} {'日变动%':>8s}")
    print(f"  {'-'*74}")
    for pos in positions:
        code = pos["code"]
        live = live_prices.get(code, {})
        current_price = live.get("price") or pos.get("price_last", 0)
        current_pct = live.get("pct") or 0
        shares = pos["shares"]
        cost = pos["cost"]
        market_value = shares * current_price
        cost_value = shares * cost
        pnl = market_value - cost_value
        pnl_pct = (pnl / cost_value * 100) if cost_value > 0 else 0
        icon = "🟢" if pnl > 0 else "🔴"
        total_cost += cost_value
        total_value += market_value

        snapshot["positions_tracking"].append({
            "code": code, "name": pos["name"], "shares": shares,
            "cost": cost, "price_current": current_price,
            "market_value": round(market_value, 2),
            "pnl": round(pnl, 2), "pnl_pct": round(pnl_pct, 2),
            "day_change_pct": round(current_pct, 2) if current_pct else 0,
        })
        print(f"  {code:<8s} {pos['name']:<10s} {shares:>5d}股 {cost:>7.2f} {current_price:>7.2f} "
              f"{market_value:>9.0f} {icon}{pnl:>+8.0f} ({pnl_pct:+.1f}%) {current_pct:>+7.2f}%")

    total_pnl = total_value - total_cost
    total_pnl_pct = (total_pnl / total_cost * 100) if total_cost > 0 else 0
    snapshot["portfolio_summary"] = {
        "total_cost": round(total_cost, 2),
        "total_value": round(total_value, 2),
        "total_pnl": round(total_pnl, 2),
        "total_pnl_pct": round(total_pnl_pct, 2),
    }
    icon_pf = "🟢" if total_pnl > 0 else "🔴"
    print(f"  {'-'*74}")
    print(f"  {'合计':<19s} {'':>5s}  {'':>8s} {'':>8s} {total_value:>9.0f} {icon_pf}{total_pnl:>+8.0f} ({total_pnl_pct:+.1f}%)")

    result["sections"]["市场快照"] = snapshot

    # ── 第3段: 催化剂状态 ──
    print(f"\n⚡ [3/4] 催化剂状态:")
    catalyst_items = _extract_catalysts(MEMORY_MD, today_str)
    if catalyst_items:
        for cat in catalyst_items:
            icon = "✅" if cat.get("active") else "⏳"
            print(f"  {icon} {cat.get('ticker','')} {cat.get('event','')} | {cat.get('status','')}")
    else:
        print(f"  ℹ️ 无活跃催化剂 (当日无预排事件)")
    result["sections"]["催化剂状态"] = catalyst_items

    # ── 第3.5段: 补充模块采集 ──
    print(f"\n🔧 [3.5/4] 补充模块采集...")
    try:
        from zmatrix.daily_memory.memory_card_modules import (
            collect_g18_decisions, collect_g17_risk_events,
            collect_factor_monitoring_snapshot, collect_z9_posterior_entries,
            generate_tomorrow_focus
        )
        tickers_in_scope = [p["code"] for p in positions]
        g18_decisions = collect_g18_decisions(tickers_in_scope)
        g17_events = collect_g17_risk_events(tickers_in_scope)
        factor_snapshot = collect_factor_monitoring_snapshot()
        z9_entries = collect_z9_posterior_entries(today_str)
        tomorrow_focus = generate_tomorrow_focus(g18_decisions, g17_events, catalyst_items)
        print(f"  ✅ G18决策: {g18_decisions.get('status','?')}")
        print(f"  ✅ G17风控: {g17_events.get('status','?')}")
        print(f"  ✅ 因子监控: {factor_snapshot.get('status','?')}")
        print(f"  ✅ Z9后验: {z9_entries.get('status','?')}")
        print(f"  ✅ 明日关注: {len(tomorrow_focus)}项")
    except Exception as e:
        print(f"  ⚠️ 补充模块采集失败: {e}")
        g18_decisions = {"status": "unavailable", "reason": str(e)}
        g17_events = {"status": "unavailable", "reason": str(e)}
        factor_snapshot = {"status": "unavailable", "reason": str(e)}
        z9_entries = {"status": "unavailable", "reason": str(e)}
        tomorrow_focus = []

    supplementary = {
        "g18_decisions": g18_decisions,
        "g17_risk_events": g17_events,
        "factor_monitoring": factor_snapshot,
        "z9_posterior": z9_entries,
        "tomorrow_focus": tomorrow_focus,
    }
    result["sections"].update(supplementary)

    # ── 第4段: 日记忆卡生成 ──
    print(f"\n📝 [4/4] 日记忆卡整合:")
    daily_card_md = _generate_daily_card_md(today_str, snapshot, catalyst_items, result, supplementary)

    # 预览头部
    for line in daily_card_md.split("\n")[:20]:
        print(f"  {line}")
    print(f"  ... (共{len(daily_card_md.split(chr(10)))}行)")

    result["sections"]["日记忆卡"] = {"markdown": daily_card_md, "line_count": len(daily_card_md.split("\n"))}
    result["status"] = "completed"
    result["pipeline_stamp"] = f"{pipeline}_v2.9.5_{today_str}"

    print(f"\n{'='*62}")
    print(f"✅ {pipeline} 完成 | 持仓{len(positions)}只 | 组合{total_pnl_pct:+.2f}%")
    print(f"   耗时: {status_info['fetch_duration_ms']}ms\n")

    # ── 落盘 ──
    if not dry_run:
        _save_daily_card(result, today_str, daily_card_md)
        _auto_append_memory(result, today_str, daily_card_md)

    return result


def _extract_catalysts(memory_path: Path, today_str: str) -> list[dict]:
    """从 MEMORY.md 提取催化剂/事件日历"""
    catalysts = []
    if not memory_path.exists():
        return catalysts

    with open(memory_path) as f:
        text = f.read()

    # 搜索"下次FOMC""FOMC纪要""财报""解禁"等关键词
    patterns = [
        (r'FOMC[：:]\s*(\d+/\d+)', "FOMC"),
        (r'FOMC纪要[：:]\s*(\d+/\d+)', "FOMC纪要"),
        (r'下次FOMC[：:]\s*(\d+/\d+)', "FOMC"),
    ]
    for pat, label in patterns:
        for m in re.finditer(pat, text):
            date_part = m.group(1)
            if today_str in date_part or date_part == today_str:
                catalysts.append({
                    "ticker": "MACRO",
                    "event": label,
                    "date": date_part,
                    "status": "today",
                    "active": True,
                })

    return catalysts


def _generate_daily_card_md(date_str: str, snapshot: dict, catalysts: list[dict], _result: dict, supplementary: dict | None = None) -> str:
    """生成日记忆卡 Markdown (9 modules)"""
    indices = snapshot.get("indices", {})
    positions = snapshot.get("positions_tracking", [])
    pf = snapshot.get("portfolio_summary", {})
    supplementary = supplementary or {}

    lines = []
    lines.append(f"## 📅 {date_str} 日记忆卡")
    lines.append("")
    lines.append(f"> pipeline: Z-G05 | 生成: {datetime.now(timezone(timedelta(hours=8))).isoformat()}")
    lines.append("")

    # 市场概况
    lines.append("### 🏛️ 大盘")
    lines.append("")
    lines.append("| 指数 | 收盘 | 涨跌幅 |")
    lines.append("|------|------|--------|")
    for code, idx in indices.items():
        p = idx.get("price", "N/A")
        pct = idx.get("pct", 0) or 0
        icon = "🔴" if pct < -1 else ("🟢" if pct > 1 else "⚪")
        lines.append(f"| {idx.get('name', code)} | {p} | {icon} {pct:+.2f}% |")
    lines.append("")

    # 持仓
    lines.append("### 📊 持仓追踪")
    lines.append("")
    lines.append("| 代码 | 名称 | 持仓 | 成本 | 现价 | 市值 | 浮盈/亏 | 日变动 |")
    lines.append("|------|------|------|------|------|------|---------|--------|")
    for pos in positions:
        icon = "🟢" if pos["pnl"] > 0 else "🔴"
        lines.append(
            f"| {pos['code']} | {pos['name']} | {pos['shares']}股 | "
            f"{pos['cost']:.2f} | {pos['price_current']:.2f} | "
            f"{pos['market_value']:,.0f} | {icon} {pos['pnl']:+,.0f} ({pos['pnl_pct']:+.1f}%) | "
            f"{pos['day_change_pct']:+.2f}% |"
        )
    pf_icon = "🟢" if pf.get("total_pnl", 0) > 0 else "🔴"
    lines.append(f"| **合计** | | | | | **{pf.get('total_value', 0):,.0f}** | "
                 f"**{pf_icon} {pf.get('total_pnl', 0):+,.0f} ({pf.get('total_pnl_pct', 0):+.1f}%)** | |")
    lines.append("")

    # 催化剂
    if catalysts:
        lines.append("### ⚡ 催化剂")
        lines.append("")
        for cat in catalysts:
            icon = "✅" if cat.get("active") else "⏳"
            lines.append(f"- {icon} **{cat.get('ticker','')}** {cat.get('event','')} — {cat.get('status','')}")
        lines.append("")

    # G18 决策
    g18 = supplementary.get("g18_decisions", {})
    lines.append("### 🎯 G18 决策追踪")
    lines.append("")
    if g18.get("status") == "ok" and g18.get("decisions"):
        lines.append("| 标的 | 动作 | 评分 | 风控标志 |")
        lines.append("|------|------|------|----------|")
        for tk, d in g18["decisions"].items():
            flags = ", ".join(d.get("risk_flags", [])) or "无"
            lines.append(f"| {tk} | {d.get('action','?')} | {d.get('score',0)} | {flags} |")
    else:
        lines.append(f"> G18: {g18.get('status', 'unavailable')} — {g18.get('note', g18.get('reason', ''))}")
    lines.append("")

    # G17 风控
    g17 = supplementary.get("g17_risk_events", {})
    lines.append("### 🛡️ G17 风控事件")
    lines.append("")
    if g17.get("status") == "ok" and g17.get("assessments"):
        lines.append("| 标的 | 风控等级 | 触发规则 | 门控 | 必审 |")
        lines.append("|------|----------|----------|------|------|")
        for tk, a in g17["assessments"].items():
            rules = ", ".join(a.get("triggered_rules", [])[:3]) or "无"
            lines.append(f"| {tk} | {a.get('risk_level','?')} | {rules} | {a.get('action_gate','?')} | {'\u2757' if a.get('must_review') else '\u2714\ufe0f'} |")
    else:
        lines.append(f"> G17: {g17.get('status', 'unavailable')}")
    lines.append("")

    # 因子监控
    factor = supplementary.get("factor_monitoring", {})
    lines.append("### 📊 因子监控快照")
    lines.append("")
    if factor.get("status") == "ok":
        lines.append(f"- 总因子数: {factor.get('total_factors', 0)}")
        lines.append(f"- 信号就绪: {factor.get('signal_ready', 0)}")
        lines.append(f"- 监控完成: {factor.get('monitoring_done', 0)}")
        lines.append(f"- 已封堵: {factor.get('blocked', 0)}")
        lines.append(f"- 最后运行: {factor.get('last_run_date', 'N/A')}")
    else:
        lines.append(f"> 因子监控: {factor.get('status', 'unavailable')}")
    lines.append("")

    # Z9 后验
    z9 = supplementary.get("z9_posterior", {})
    lines.append("### 🔬 Z9 后验入口")
    lines.append("")
    if z9.get("status") == "ok":
        preds_due = z9.get("predictions_due", [])
        vals = z9.get("validations_pending", [])
        cal = z9.get("calibration_status", {})
        lines.append(f"- 今日到期预测: {len(preds_due)}条")
        for p in preds_due[:5]:
            lines.append(f"  - {p.get('ticker','?')}: {p.get('prediction','?')} (制于{p.get('made_date','?')})")
        lines.append(f"- 待验证: {len(vals)}条")
        lines.append(f"- 校准: 总{cal.get('total_predictions',0)}/已验{cal.get('validated',0)} 准确率{cal.get('accuracy_pct','N/A')}%")
    else:
        lines.append(f"> Z9: {z9.get('status', 'unavailable')}")
    lines.append("")

    # 明日关注
    tomorrow = supplementary.get("tomorrow_focus", [])
    lines.append("### 👀 明日关注")
    lines.append("")
    if tomorrow:
        lines.append("| 标的 | 原因 | 优先级 | 行动 |")
        lines.append("|------|------|--------|------|")
        for item in tomorrow[:10]:
            lines.append(f"| {item.get('ticker','?')} | {item.get('reason','?')} | {item.get('priority','?')} | {item.get('action_required','?')} |")
    else:
        lines.append("> 无特别关注事项")
    lines.append("")

    lines.append("---")
    lines.append(f"**签章**: ☯️ Z2天师 | Z-MATRIX-OS v2.9.5 | Z-G05 日记忆卡")
    lines.append("")

    return "\n".join(lines)


def _save_daily_card(result: dict, date_str: str, daily_card_md: str):
    """落盘: 日记忆卡MD"""
    DAILY_CARDS_DIR.mkdir(parents=True, exist_ok=True)
    fname = DAILY_CARDS_DIR / f"{date_str}_日记忆卡.md"
    with open(fname, "w") as f:
        f.write(daily_card_md)
    print(f"📁 日卡已落盘: {fname}")

    # 同时保存JSON
    json_dir = DAILY_CARDS_DIR / "json"
    json_dir.mkdir(parents=True, exist_ok=True)
    jname = json_dir / f"{date_str}_日记忆卡.json"
    with open(jname, "w") as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"📁 JSON已落盘: {jname}")


def _auto_append_memory(result: dict, date_str: str, daily_card_md: str):
    """自动追加到 MEMORY.md (在末尾插入日记忆卡条目)"""
    if not MEMORY_MD.exists():
        print(f"⚠️ MEMORY.md 不存在, 跳过追加")
        return

    with open(MEMORY_MD) as f:
        original = f.read()

    # 生成追加条目
    append_block = f"""

---

{_generate_daily_card_md(date_str, result['sections'].get('市场快照', {}), result['sections'].get('催化剂状态', []), result)}

<!-- Z-END-OF-DAY-MARKER -->
"""

    # 替换上次的日结束标记和新内容
    if "<!-- Z-END-OF-DAY-MARKER -->" in original:
        # 移除旧的日结束标记块
        idx = original.rfind("<!-- Z-END-OF-DAY-MARKER -->")
        # 回退到最近的 --- 分隔线
        sep_idx = original.rfind("\n---\n", 0, idx)
        if sep_idx > 0:
            original = original[:sep_idx]

    with open(MEMORY_MD, "w") as f:
        f.write(original + append_block)

    print(f"📝 MEMORY.md 已自动追加日卡条目")


# ═══ CLI ═══
def main():
    parser = argparse.ArgumentParser(
        description="Z-G05 日记忆卡 — 每日15:30盘后运行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 gate_pipeline.py                        # 完整运行(使用MEMORY.md持仓)
  python3 gate_pipeline.py --tickers 002472,601899
  python3 gate_pipeline.py --dry-run              # 试运行(不追加MEMORY.md)
  python3 gate_pipeline.py --output json          # 仅JSON输出
        """,
    )
    parser.add_argument("--tickers", type=str, default="",
                       help="关注的标的代码, 逗号分隔 (空=使用MEMORY.md持仓)")
    parser.add_argument("--mode", choices=["full", "positions_only", "json"],
                       default="full", help="运行模式")
    parser.add_argument("--output", choices=["json", "text", "both"],
                       default="both", help="输出格式")
    parser.add_argument("--dry-run", action="store_true",
                       help="试运行(不落盘, 不追加MEMORY.md)")

    args = parser.parse_args()
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()] if args.tickers else None

    result = run(tickers=tickers, mode=args.mode, dry_run=args.dry_run)

    if args.output in ("json", "both"):
        # 输出精简JSON(不含完整markdown)
        out = {k: v for k, v in result.items() if k != "日记忆卡"}
        print("\n" + json.dumps(out, ensure_ascii=False, indent=2, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
