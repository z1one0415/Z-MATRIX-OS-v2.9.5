#!/usr/bin/env python3
"""☯️ Z-G11 组合风控 — gate_pipeline.py v1.0
运行: 每周+调仓前 | 功能: 持仓集中度/角色桶/因子暴露检查
依赖: Z-G01 (via z17_loader) + MEMORY.md持仓
输出: 风险警告 + RISK_ALERT_REQUIRES_ACCOUNT_CONFIRMATION
注意: 当前未接券商账户真相，不输出实盘减仓动作
"""

import argparse, json, os, re, sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

WORKSPACE = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
MEMORY_MD = WORKSPACE.parent / "MEMORY.md"
sys.path.insert(0, str(WORKSPACE))

try:
    from pipelines.z17_loader import market_truth
except ImportError:
    market_truth = lambda t: {"status":"stub","price":0,"name":"?"}

def _parse_positions():
    """解析持仓"""
    positions = []
    if not MEMORY_MD.exists(): return positions
    text = open(MEMORY_MD).read()
    for m in re.finditer(r'\|\s*([^|]+?)\s+(\d{6})\s*\|\s*([\d,]+股)\s*\|\s*([\d.]+)\s*\|', text):
        name = m.group(1).strip()
        code = m.group(2)
        shares = int(m.group(3).replace("股","").replace(",",""))
        cost = float(m.group(4))
        g1 = market_truth(code)
        price = g1.get("price") or cost
        value = shares * price
        positions.append({"code":code,"name":name,"shares":shares,"cost":cost,
                          "price":price,"value":value,
                          "industry": g1.get("industry", "")})
    return positions

def _classify_chain(code, name, industry=""):
    """产业链分类 — unified chain taxonomy provider"""
    try:
        from pipelines.chain_taxonomy_provider import match_chain_detail
        detail = match_chain_detail(ticker=code, name=name, industry=industry)
        return detail.get("primary_chain") or "未映射", detail
    except Exception as e:
        return "未映射", {
            "primary_chain": None,
            "secondary_chains": [],
            "match_reason": "error",
            "confidence": "UNMAPPED",
            "error": str(e)[:120],
        }

def run():
    now = datetime.now(timezone(timedelta(hours=8)))
    result = {"pipeline_signature":"Z-G11_组合风控_v2.9.5-draft","timestamp":now.isoformat(),
              "status":"running","sections":{}}
    
    print(f"\n☯️ Z-G11 组合风控 — {now.strftime('%Y-%m-%d')}")
    print("=" * 60)
    
    positions = _parse_positions()
    if not positions:
        print("⚠️ 无持仓数据")
        result["status"] = "DATA_GAP"
        result["sections"]["reason"] = "NO_POSITION_DATA"
        result["sections"]["action"] = "NO_ACCOUNT_TRUTH"
        result["sections"]["account_truth"] = {
            "connected": False,
            "position_source": "MEMORY_MD_REGEX",
            "cash_source": "NOT_CONNECTED",
            "fills_source": "NOT_CONNECTED",
            "broker_source": "NOT_CONNECTED",
            "confidence": "LOW_ACCOUNT_TRUTH",
        }
        return result
    
    total_value = sum(p["value"] for p in positions)
    
    # 1. 单票集中度
    print("\n📊 单票占比:")
    warnings = []
    for p in positions:
        pct = p["value"]/total_value*100 if total_value else 0
        flag = "⚠️" if pct > 40 else ("🔴" if pct > 25 else "✅")
        print(f"  {flag} {p['code']} {p['name']:<8s} {pct:5.1f}%  (¥{p['value']:,.0f})")
        if pct > 40: warnings.append(f"单票集中度过高: {p['name']} {pct:.0f}%")
    
    # 2. 产业链集中度
    print(f"\n🔗 产业链分布:")
    chain_map = {}
    for p in positions:
        ch, detail = _classify_chain(p["code"], p["name"], p.get("industry", ""))
        p["chain"] = ch
        p["chain_detail"] = detail
        chain_map[ch] = chain_map.get(ch, 0) + p["value"]
    for ch, val in sorted(chain_map.items(), key=lambda x: x[1], reverse=True):
        pct = val/total_value*100 if total_value else 0
        flag = "⚠️" if pct > 60 else "✅"
        print(f"  {flag} {ch}: {pct:.1f}%")
        if pct > 60: warnings.append(f"产业链过度集中: {ch} {pct:.0f}%")
    
    # 3. 现金比例 (假设总资产=持仓+现金, 估算)
    cash_ratio = None  # NOT_CONNECTED — not a placeholder, explicitly unavailable
    print(f"\n💰 现金比例: 未接入账户实测数据")
    
    # 4. 裁决
    print(f"\n📋 裁决:")
    if warnings:
        result["status"] = "DEGRADED_ACCOUNT_TRUTH_REQUIRED"
        print(f"  ⚠️ {len(warnings)}条风险警告")
        for w in warnings: print(f"    - {w}")
        result["sections"]["action"] = "RISK_ALERT_REQUIRES_ACCOUNT_CONFIRMATION"
        result["sections"]["suggested_human_check"] = [
            "确认真实账户持仓",
            "确认现金与可用资金",
            "确认成交成本与实际仓位",
            "确认是否需要减仓",
        ]
    else:
        print(f"  ✅ 组合风险正常")
        result["status"] = "PASS_PROXY"
        result["sections"]["action"] = "PORTFOLIO_OK_PROXY"
    
    # Structured chain exposure
    chain_exposure = {}
    for ch, val in sorted(chain_map.items(), key=lambda x: x[1], reverse=True):
        pct = val / total_value * 100 if total_value else 0
        chain_exposure[ch] = {"value": round(val, 2), "pct": round(pct, 2),
                              "status": "OVER_CONCENTRATED" if pct > 60 else "OK"}
    result["sections"]["chain_exposure"] = chain_exposure

    # Structured single position exposure
    single_exposure = {}
    for p in positions:
        pct = p["value"] / total_value * 100 if total_value else 0
        single_exposure[p["code"]] = {"name": p["name"], "value": round(p["value"], 2),
                                        "pct": round(pct, 2),
                                        "status": "OVER_CONCENTRATED" if pct > 40 else ("WATCH" if pct > 25 else "OK")}
    result["sections"]["single_position_exposure"] = single_exposure

    result["sections"]["positions"] = positions
    result["sections"]["total_value"] = total_value
    result["sections"]["warnings"] = warnings
    result["sections"]["cash"] = {"cash_ratio": None, "source": "NOT_CONNECTED", "capability": "cash_exposure_disabled"}
    result["sections"]["account_truth"] = {
        "connected": False,
        "position_source": "MEMORY_MD_REGEX",
        "cash_source": "NOT_CONNECTED",
        "fills_source": "NOT_CONNECTED",
        "broker_source": "NOT_CONNECTED",
        "confidence": "LOW_ACCOUNT_TRUTH",
    }
    return result

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G11 组合风控")
    args = p.parse_args()
    run()
