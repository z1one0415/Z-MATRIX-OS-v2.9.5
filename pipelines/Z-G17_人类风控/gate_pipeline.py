#!/usr/bin/env python3
"""☯️ Z-G17 人类风控 — v1.1 | 实时数据接入 | Tilt检测+L1.6+Confession+上下文记录"""
import argparse, json, sys, os
from datetime import datetime, timedelta, timezone
from pathlib import Path
WORKSPACE = Path(__file__).resolve().parent.parent.parent
LEDGER = WORKSPACE.parent / "human_behavior_ledger.jsonl"
sys.path.insert(0, str(WORKSPACE))
TZ = timezone(timedelta(hours=8))

try:
    from pipelines.z17_loader import market_truth, l25_macro
    _HAS_Z01 = True
except ImportError:
    market_truth = lambda t: {"status":"stub","price":0,"name":"?"}
    l25_macro = lambda: {"status":"stub","filled":0}
    _HAS_Z01 = False


def _get_market_snapshot():
    """实时市场快照 — 上证/深证/科创"""
    try:
        import urllib.request
        codes = "sh000001,sz399001,sh000688,sz399006"
        url = f"http://hq.sinajs.cn/list={codes}"
        req = urllib.request.Request(url, headers={"Referer":"https://finance.sina.com.cn"})
        raw = urllib.request.urlopen(req, timeout=5).read().decode("gbk")
        result = {}
        for line in raw.split("\n"):
            if "=" not in line: continue
            name = line.split("=")[0].replace("var hq_str_","")
            data = line.split('"')[1] if '"' in line else ""
            if not data: continue
            fields = data.split(",")
            if len(fields) > 3:
                try:
                    result[name] = {"price":float(fields[3]),"change_pct":round((float(fields[3])/float(fields[2])-1)*100,2) if fields[2] else 0}
                except: pass
        return result
    except:
        return {"error": "unavailable"}


def _get_portfolio_context(ticker):
    """获取该标的在当前组合中的上下文"""
    mem = WORKSPACE.parent / "MEMORY.md"
    if not mem.exists():
        return {"positions": [], "note": "无MEMORY数据"}
    text = open(mem).read()
    positions = []
    import re
    for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|\s*([\d.]+)\s*\|', text):
        positions.append({"name":m.group(1).strip(),"code":m.group(2),
                          "shares":int(m.group(3).replace("股","").replace(",","")),
                          "cost":float(m.group(4))})
    
    my_pos = [p for p in positions if p["code"] == ticker]
    total_value = sum(p["cost"]*p["shares"] for p in positions)
    
    return {
        "my_position": my_pos[0] if my_pos else None,
        "total_positions": len(positions),
        "portfolio_value": round(total_value, 2),
        "concentration": round(my_pos[0]["cost"]*my_pos[0]["shares"]/total_value*100, 1) if my_pos and total_value else 0,
    }


def run(override=None):
    now = datetime.now(TZ)
    
    # Auto-detect: try to get from command line or use interactive default
    if override is None:
        override = {"ticker":"002463","system_action":"WAIT","human_action":"WATCH","reason":"手动覆盖(请提供原因)"}
    
    ticker = override.get("ticker","?")
    result = {"pipeline_signature":"Z-G17_人类风控_v1.1","timestamp":now.isoformat(),
              "data_sources": _HAS_Z01, "sections":{}}
    
    print(f"\n☯️ Z-G17 人类风控 — HumanOverride检测 v1.1")
    print(f"   数据源: {'Z-G01实时' if _HAS_Z01 else '⚠️ stub模式'}")
    print("=" * 60)
    
    # ── 1. 实时上下文采集 ──
    print("\n📡 [1/4] 实时上下文采集:")
    
    g1 = market_truth(ticker) if _HAS_Z01 else {"status":"stub","price":0,"name":"?"}
    macro = l25_macro() if _HAS_Z01 else {"status":"stub","filled":0}
    market = _get_market_snapshot()
    portfolio = _get_portfolio_context(ticker)
    
    print(f"  标的: {ticker} {g1.get('name','?')} @{g1.get('price','?')}")
    print(f"  宏观: {macro.get('filled',0)}/8域填充 {'✅' if macro.get('status')=='PASS' else '⚠️'}")
    print(f"  大盘: {len(market)}个指数")
    if portfolio["my_position"]:
        print(f"  持仓: {portfolio['my_position']['shares']}股 @{portfolio['my_position']['cost']} 集中度{portfolio['concentration']}%")
    
    result["sections"]["context"] = {
        "market_snapshot": market,
        "macro": macro,
        "portfolio": portfolio,
        "stock_price": g1.get("price") if _HAS_Z01 else None,
    }
    
    # ── 2. L1.6 Tilt检测 ──
    print(f"\n🔍 [2/4] L1.6 Tilt检测:")
    
    tilt = False
    tilt_reasons = []
    
    # 主观词检测
    subjective_words = ["觉得","感觉","应该会","肯定会","一定涨","内幕","听说","小道","赌","梭哈","满仓"]
    reason = override.get("reason","")
    for w in subjective_words:
        if w in reason:
            tilt = True
            tilt_reasons.append(f"主观感觉词: '{w}'")
            break
    
    # 覆盖系统判断
    if override["system_action"] in ("BLOCK","WAIT") and override["human_action"] in ("WATCH",):
        tilt = True
        tilt_reasons.append("覆盖系统BLOCK/WAIT→WATCH")
    
    # 高集中度+再加仓
    if portfolio["concentration"] > 40 and override.get("human_action") in ("WATCH",):
        tilt = True
        tilt_reasons.append(f"已高集中度{portfolio['concentration']}%但仍要操作")
    
    # 宏观逆风+乐观操作
    if macro.get("filled", 0) >= 5 and any(w in reason for w in ["加仓","买入","追"]):
        tilt = True
        tilt_reasons.append("宏观逆风下仍然加仓")
    
    icon = "✅" if not tilt else "⚠️"
    print(f"  {icon} TILT: {'触发' if tilt else '未触发'}")
    if tilt:
        for r in tilt_reasons:
            print(f"    → {r}")
        print(f"  ⚠️ 建议: Confession Room确认 + 降低系统背书 + 记录到HumanBehaviorLedger")
    
    # ── 3. 记录到 Ledger ──
    print(f"\n📝 [3/4] 记录:")
    
    entry = {
        **override,
        "timestamp": now.isoformat(),
        "tilt": tilt,
        "tilt_reasons": tilt_reasons,
        "context": result["sections"]["context"],
        "data_available": _HAS_Z01,
    }
    
    try:
        with open(LEDGER, 'a') as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        print(f"  ✅ 已追加: {LEDGER}")
        # Count total
        with open(LEDGER) as f:
            total = sum(1 for _ in f)
        print(f"  📊 Ledger累计: {total}条记录")
    except Exception as e:
        print(f"  ⚠️ 记录失败: {e}")
    
    result["override"] = entry
    result["sections"]["ledger_count"] = total if 'total' in dir() else 0
    
    # ── 4. 模式检测 ──
    print(f"\n📊 [4/4] 历史模式:")
    if LEDGER.exists():
        try:
            with open(LEDGER) as f:
                history = [json.loads(l) for l in f if l.strip()]
            
            ticker_ops = [h for h in history if h.get("ticker") == ticker]
            tilt_count = sum(1 for h in history if h.get("tilt"))
            
            print(f"  该标的: {len(ticker_ops)}次操作")
            print(f"  整体TILT率: {tilt_count}/{len(history)} ({tilt_count/max(len(history),1)*100:.0f}%)")
            
            if tilt_count / max(len(history),1) > 0.4:
                print(f"  ⚠️ TILT率偏高(>{40}%), 建议降低操作频率")
        except:
            print(f"  ⚠️ 历史数据读取异常")
    else:
        print(f"  尚无历史记录")
    
    return result


if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G17 人类风控 v1.1")
    p.add_argument("--ticker", default="002463")
    p.add_argument("--system", default="WAIT")
    p.add_argument("--human", default="WATCH")
    p.add_argument("--reason", default="手动覆盖")
    args = p.parse_args()
    run({"ticker":args.ticker,"system_action":args.system,"human_action":args.human,"reason":args.reason})
