#!/usr/bin/env python3
"""🛢️ Z-G01 gate_data.py — 数据后勤保障主引擎 (Data Service Layer)
NOT a pipeline script. All pipelines consume this service via z17_loader. (v1.0)
所有管线通过z17_loader导入此模块。提供8个标准数据函数。
门禁: 分级TTL(行情3s/财务1d/画像7d), 降级链: Sina→baostock→Tushare→DEGRADED
"""

import json, time, urllib.request, sys, os

# ═══ 输出等级 (O1-O5) + Capability Mask 范式 (v2.9.5 open-intelligence) ═══
OUTPUT_LEVELS = {
    "O5_EXECUTABLE": "完整行动提案(需HumanConfirm)",
    "O4_PAPER_PLAN": "纸面计划(可输出完整Z-G16)",
    "O3_CONDITIONAL": "条件路线(价格/仓位待补齐)",
    "O2_DIAGNOSTIC": "诊断+缺口+可能性",
    "O1_DATA_GAP": "数据缺失说明+修复建议",
}
CAPABILITY_MASK_KEYS = ["exact_price_zone","paper_fill_price","micro_absorption",
    "l2_bid_depth","dividend_score","m1_preheat","position_playbook","execution_proposal"]

def capability_mask(disabled: list, output_level: str, errors: list = None) -> dict:
    """生成能力掩码 — 替代旧PASS/DEGRADED/BLOCK
    
    forbidden_now: 当前不可执行的输出 (硬禁止)
    re_enable_conditions: 未来满足条件后可恢复的输出路径
    conditional_future_outputs: 同re_enable_conditions, 语义更明确的别名
    """
    cond = []
    if "PAPER_PROBE" in _forbidden_by_disabled(disabled):
        cond.append({"output":"PAPER_PROBE","requires":["world=PAPER_WORLD","MT=PASS","L1.5=SAFE"]})
    return {
        "output_level": output_level,
        "disabled_capabilities": disabled,
        "allowed_outputs": _allowed_by_level(output_level),
        "conditional_outputs": cond,  # = future re-enable path, not currently executable
        "conditional_future_outputs": cond,  # explicit alias
        "forbidden_actions": _forbidden_by_disabled(disabled),
        "forbidden_now": _forbidden_by_disabled(disabled),  # explicit alias: currently blocked
        "re_enable_conditions": cond,  # what must change to re-enable
        "required_next_data": _required_by_disabled(disabled),
        "errors": errors or []
    }

def _required_by_disabled(disabled: list) -> list:
    req = []
    if "exact_price_zone" in disabled: req.append("MT_PASS_or_DQ>=85")
    if "execution_proposal" in disabled: req.append("MT_PASS+L1.5_SAFE")
    if "paper_fill_price" in disabled: req.append("MT_PASS+execution_quote+TTL_valid")
    return req

def _allowed_by_level(level: str) -> list:
    m = {
        "O5": ["full_plan","price_zones","position","paper_probe","watch","wait"],
        "O4": ["paper_plan","conditional_routes","watch","wait","paper_track"],
        "O3": ["conditional_routes","watch","wait","gap_report","zg16_lite"],
        "O2": ["diagnostic","gap_report","watch","condition_route","evidence_report"],
        "O1": ["data_gap_report"],
    }
    return m.get(level, ["data_gap_report"])

def _forbidden_by_disabled(disabled: list) -> list:
    forbidden = []
    if "exact_price_zone" in disabled: forbidden.append("PAPER_PROBE")
    if "execution_proposal" in disabled: forbidden.extend(["HUMAN_CONFIRM_PROBE","ActionProposal"])
    return forbidden
from datetime import datetime, timedelta

# 分级TTL (按数据类型, v2.9.5-draft)
TOLERANCE_BASE = 1.0  # execution_quote block_threshold (research uses wider)
_cache = {}

def _now(): return int(time.time())
def _cache_get(k, ttl=300):
    e = _cache.get(k)
    return e if e and _now()-e.get("_ts",0)<ttl else None
def _cache_set(k, v):
    v["_ts"] = _now(); _cache[k] = v

def _sina_quote(ticker):
    pfx = "sz" if ticker[0] in "03" else "sh"
    try:
        u = f"http://hq.sinajs.cn/list={pfx}{ticker}"
        req = urllib.request.Request(u, headers={"Referer":"https://finance.sina.com.cn"})
        raw = urllib.request.urlopen(req, timeout=5).read().decode("gbk")
        if '=""' in raw: return {"error":"empty"}
        p = raw.split('"')[1].split(",")
        if len(p)<32 or p[3] in ("","0.000","0.00"): return {"error":"invalid"}
        return {"price":float(p[3]),"open":float(p[1]),"high":float(p[4]),"low":float(p[5]),
                "volume":p[8],"name":p[0],"source":"sina_api","time":p[31] if len(p)>31 else ""}
    except Exception as e:
        return {"error":str(e)[:60]}

def _bs_raw_kline(ticker, days=10):
    """仅用于execution_price校验。adjustflag=3(不复权)。禁止用于均线/R-Matrix/形态。"""
    return _bs_kline_internal(ticker, days, adjust="raw")

def _bs_research_kline(ticker, days=10):
    """仅用于均线/历史收益/R-Matrix/形态研究。adjustflag=2(前复权)。禁止用于execution交叉验证。"""
    return _bs_kline_internal(ticker, days, adjust="research")

def _bs_kline_internal(ticker, days, adjust="research"):
    """拉取baostock日K OHLCV — 按用途分离adjustflag
    adjust="research" → adjustflag=2 (前复权, 用于均线/收益率/形态)
    adjust="raw"      → adjustflag=3 (不复权, 用于execution交叉验证)
    
    Returns dict with: dates/open/high/low/close/volume/amount/prices/adjust_flag/adjust_type/data_contract
    prices == close for backward compatibility with Z-G09/Z-G10/R-Matrix/D-Matrix.
    """
    try:
        import baostock as bs; bs.login()
        pfx = "sz" if ticker[0] in "03" else "sh"
        code = f"{pfx}.{ticker}"
        flag = "2" if adjust == "research" else "3"
        s = (datetime.now()-timedelta(days=max(days+10,100))).strftime("%Y-%m-%d")
        e = datetime.now().strftime("%Y-%m-%d")
        fields = "date,open,high,low,close,volume,amount"
        rs = bs.query_history_k_data_plus(code, fields, start_date=s, end_date=e, frequency="d", adjustflag=flag)
        rows = []
        missing = set()
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1] != "" and float(r[1]) > 0:
                try:
                    rows.append({"date": r[0], "open": float(r[1]), "high": float(r[2]),
                                "low": float(r[3]), "close": float(r[4]),
                                "volume": float(r[5]) if r[5] and r[5] != "" else 0.0,
                                "amount": float(r[6]) if len(r) > 6 and r[6] and r[6] != "" else 0.0})
                except (IndexError, ValueError):
                    rows.append({"date": r[0], "open": float(r[1]), "high": float(r[2]),
                                "low": float(r[3]), "close": float(r[4]), "volume": 0.0, "amount": 0.0})
        bs.logout()
        if not rows:
            return {"error": "no_data"}
        # Check for missing fields
        if all(r["amount"] == 0.0 for r in rows):
            missing.add("amount")
        result = {
            "dates": [r["date"] for r in rows],
            "open": [r["open"] for r in rows],
            "high": [r["high"] for r in rows],
            "low": [r["low"] for r in rows],
            "close": [r["close"] for r in rows],
            "volume": [r["volume"] for r in rows],
            "amount": [r["amount"] for r in rows] if "amount" not in missing else [],
            "prices": [r["close"] for r in rows],  # backward compat
            "count": len(rows),
            "adjust_flag": flag,
            "adjust_type": adjust,
            "data_contract": "OHLCV_DAILY_V1",
        }
        if missing:
            result["missing_fields"] = sorted(missing)
        return result
    except Exception as ex:
        return {"error": str(ex)[:60]}

def _bs_finance(ticker):
    try:
        import baostock as bs; bs.login()
        pfx = "sz" if ticker[0] in "03" else "sh"
        code = f"{pfx}.{ticker}"
        rv = {"q1_eps":None,"has_finance":False,"industry":""}
        for y,q in [(2026,1),(2025,4),(2025,3)]:
            try:
                rs = bs.query_profit_data(code,year=y,quarter=q)
                while rs.next():
                    r = rs.get_row_data()
                    if r and len(r)>3 and r[3] not in ("","0","0.000000"):
                        rv["has_finance"]=True
                        if y==2026 and q==1: rv["q1_eps"]=r[3]
            except: pass
        try:
            rs = bs.query_stock_industry(code)
            while rs.next():
                r = rs.get_row_data()
                if len(r)>3: rv["industry"]=r[3]
        except: pass
        bs.logout(); return rv
    except Exception as ex:
        return {"error":str(ex)[:60],"has_finance":False}

def _bs_l4(ticker):
    try:
        import baostock as bs; bs.login()
        pfx = "sz" if ticker[0] in "03" else "sh"
        code = f"{pfx}.{ticker}"
        rv = {"name":"","tradable":True,"is_st":False,"errors":[]}
        rs = bs.query_stock_basic(code)
        while rs.next():
            r = rs.get_row_data(); nm = r[1] if r[1] else ""
            rv["name"]=nm
            if "ST" in nm.upper() or "*ST" in nm: rv["is_st"]=True; rv["errors"].append(f"ST:{nm}")
        s = (datetime.now()-timedelta(days=5)).strftime("%Y-%m-%d")
        e = datetime.now().strftime("%Y-%m-%d")
        rs2 = bs.query_history_k_data_plus(code,"date,volume,tradestatus",start_date=s,end_date=e,frequency="d",adjustflag="2")
        has_vol=False
        while rs2.next():
            r = rs2.get_row_data()
            if r[2]=='1' and float(r[1])>0: has_vol=True
        rv["tradable"]=has_vol
        if not has_vol: rv["errors"].append("近5日无成交,可能停牌")
        bs.logout(); return rv
    except Exception as ex:
        return {"error":str(ex)[:60],"tradable":False}

# ═══ 8个导出函数 ═══
def market_truth(ticker):
    ck = f"mt_{ticker}"
    if _cache_get(ck, ttl=3): return _cache_get(ck, ttl=3)
    errs, dt = [], {"ticker":ticker}
    sina = _sina_quote(ticker)
    if sina.get("error"): errs.append(f"sina:{sina['error']}")
    else: dt.update(sina)
    # execution验证用raw price (adjustflag=3, 不复权)
    bs = _bs_raw_kline(ticker, 10)
    if bs.get("error"): errs.append(f"bs:{bs['error']}")
    elif bs.get("prices"):
        lt_close = bs["close"][-1] if bs.get("close") else bs["prices"][-1]
        lt_date = bs["dates"][-1] if bs.get("dates") else ""
        dt["baostock_close"] = lt_close; dt["baostock_date"] = lt_date
        if "price" in dt:
            today = datetime.now().strftime("%Y-%m-%d")
            dp = abs(dt["price"]-lt_close)/dt["price"]*100
            dt["source_diff_pct"]=round(dp,2)
            dd = max(0,(datetime.strptime(today,"%Y-%m-%d")-datetime.strptime(lt_date,"%Y-%m-%d")).days) if lt_date else 0
            is_same_trading_date = lt_date == today
            if is_same_trading_date:
                # Same trading day: standard thresholds apply
                if dp <= 0.30: dt["cross_validated"]=True; dt["price_conflict"]=False
                elif dp <= 1.0: dt["cross_validated"]=False; dt["price_conflict"]=False; dt["degraded"]=True; errs.append(f"execution_quote DEGRADED:{dt['price']}vs{lt_close}({dp:.1f}%)")
                else: dt["price_conflict"]=True; errs.append(f"execution_quote BLOCK:{dt['price']}vs{lt_close}({dp:.1f}%>1.0%)")
            else:
                # Real-time vs previous close: never BLOCK on diff alone
                dt["historical_close_date"] = lt_date
                dt["comparison_mode"] = "realtime_vs_previous_close_reference"
                dt["cross_validated"] = False
                dt["degraded"] = True
                dt["price_conflict"] = False  # not a true conflict, just different dates
                errs.append(f"REALTIME_VS_PREV_CLOSE_REFERENCE_ONLY (diff={dp:.1f}%)")
    # Status: no-price→BLOCK, price-conflict→BLOCK, errs/warnings→DEGRADED, else PASS
    if not dt.get("price"): st = "BLOCK"
    elif dt.get("price_conflict"): st = "BLOCK"
    elif errs: st = "DEGRADED"
    else: st = "PASS"
    # Capability Mask: 根据status确定输出等级
    cap_level = "O5" if st=="PASS" else ("O3" if st=="DEGRADED" else "O2")
    # When only reference comparison (not true cross-validation), disable paper_fill but allow watch/diagnostic
    is_reference_only = dt.get("comparison_mode") == "realtime_vs_previous_close_reference"
    if is_reference_only:
        cap_disabled = ["paper_fill_price", "exact_price_zone"]
    elif st == "PASS":
        cap_disabled = []
    elif st == "DEGRADED":
        cap_disabled = ["exact_price_zone", "paper_fill_price"]
    else:
        cap_disabled = ["exact_price_zone", "paper_fill_price", "execution_proposal"]
    dt["price_basis"] = "raw_unadjusted"; dt["quote_domain"] = "execution_quote"; dt["quote_role"] = "primary"; dt["output_level"] = cap_level
    dt["capability_mask"] = capability_mask(cap_disabled, cap_level, errs)
    rv = {**dt,"status":st,"errors":errs}; _cache_set(ck,rv); return rv

def source_arbitrate(ticker, g1):
    """Source Arbitration — 只承接MarketTruth状态, 不二次裁决"""
    st = g1.get("status","BLOCK")
    return {
        "status": st,
        "price": g1.get("price") if st != "BLOCK" else None,
        "source": g1.get("source",""),
        "price_basis": g1.get("price_basis",""),
        "quote_domain": g1.get("quote_domain",""),
        "quote_role": g1.get("quote_role",""),
        "output_level": g1.get("output_level",""),
        "capability_mask": g1.get("capability_mask",{}),
        "cross_validated": g1.get("cross_validated",False),
        "selected_sources": g1.get("selected_sources",[]),
        "errors": g1.get("errors",[])
    }

def dq_score(ticker):
    g1 = market_truth(ticker); fin = _bs_finance(ticker)
    sc = {"行情":15 if g1.get("cross_validated") else (12 if g1.get("price") else 6),
          "财务":22 if fin.get("has_finance") else 8,
          "估值":12 if g1.get("price") else 5,
          "产业链":12 if fin.get("q1_eps") else 10,
          "资金":13 if (g1.get("volume") and g1.get("cross_validated")) else (10 if g1.get("volume") else 3),
          "来源":13 if g1.get("cross_validated") else (6 if g1.get("price") else 3)}
    t = sum(sc.values()); errs = []
    if t<60: st="DQ_FAIL"; errs.append(f"DQ={t}<60→DIAGNOSTIC_ONLY")
    elif t<85: st="DEGRADED"; errs.append(f"DQ={t}<85")
    else: st="PASS"
    return {"status":st,"total":t,"breakdown":sc,"errors":errs,"q1_eps":fin.get("q1_eps"),"industry":fin.get("industry","")}

def l4_health(ticker):
    bs = _bs_l4(ticker); errs = list(bs.get("errors",[]))
    if bs.get("is_st"): return {"status":"BLOCK","name":bs.get("name",""),"errors":errs}
    if not bs.get("tradable"): return {"status":"BLOCK","name":bs.get("name",""),"errors":errs}
    if errs: return {"status":"DEGRADED","name":bs.get("name",""),"errors":errs}
    return {"status":"PASS","name":bs.get("name",""),"tradable":True,"errors":[]}

def get_kline(ticker, n=60):
    ck = f"kl_{ticker}_{n}"
    if _cache_get(ck, ttl=30): return _cache_get(ck, ttl=30)
    bs = _bs_research_kline(ticker, max(n+30, 100))
    if bs.get("error"): return {"status":"DATA_INCOMPLETE","prices":[],"error":bs["error"]}
    # Extract OHLCV arrays, trim to n
    rv = {
        "status": "PASS" if bs.get("count",0) >= min(n,20) else "DEGRADED",
        "prices": bs["close"][-n:] if bs.get("close") else [],
        "open": bs["open"][-n:] if bs.get("open") else [],
        "high": bs["high"][-n:] if bs.get("high") else [],
        "low": bs["low"][-n:] if bs.get("low") else [],
        "close": bs["close"][-n:] if bs.get("close") else [],
        "volume": bs["volume"][-n:] if bs.get("volume") else [],
        "amount": bs["amount"][-n:] if bs.get("amount") else [],
        "count": min(n, bs.get("count", 0)),
        "data_contract": bs.get("data_contract", "OHLCV_DAILY_V1"),
        "price_basis": "adjusted_research",
    }
    if bs.get("missing_fields"):
        rv["missing_fields"] = bs["missing_fields"]
    _cache_set(ck, rv); return rv

def get_financials(ticker):
    ck = f"fin_{ticker}"
    if _cache_get(ck, ttl=86400): return _cache_get(ck, ttl=86400)
    fin = _bs_finance(ticker)
    rv = {"status":"PASS" if fin.get("has_finance") else "DEGRADED",**fin}
    _cache_set(ck,rv); return rv

def get_sectors():
    ck = "sectors"
    if _cache_get(ck): return _cache_get(ck)
    try:
        u = "http://hq.sinajs.cn/list="+",".join(["sh000001","sz399001","sz399006","sh000688","sh000300"])
        req = urllib.request.Request(u, headers={"Referer":"https://finance.sina.com.cn"})
        raw = urllib.request.urlopen(req, timeout=5).read().decode("gbk")
        c = raw.count('="')-raw.count('=""')
        rv = {"status":"PASS" if c>=3 else "DATA_INCOMPLETE","sectors":c}
    except Exception as e:
        rv = {"status":"DATA_INCOMPLETE","error":str(e)[:60]}
    _cache_set(ck,rv); return rv

def l25_macro():
    mem = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/MEMORY.md")
    dm = {"risk":0,"china":0,"overseas":0,"chip":0,"gold":0,"fx":0,"policy":0,"commodity":0}
    try:
        txt = open(mem).read()
        if "地缘" in txt or "伊朗" in txt: dm["risk"]=1
        if "社零" in txt or "工业" in txt: dm["china"]=1
        if "FOMC" in txt or "利率" in txt: dm["overseas"]=1
        if "VIX" in txt: dm["chip"]=1
        if "黄金" in txt: dm["gold"]=1
        if "CNH" in txt or "汇率" in txt: dm["fx"]=1
        if "政策" in txt: dm["policy"]=1
        if "油价" in txt or "铜" in txt: dm["commodity"]=1
    except: pass
    f = sum(dm.values())
    return {"status":"PASS" if f>=4 else "DEGRADED","filled":f,"total":8,"domains":dm}

if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv)>1 else "002463"
    g1 = market_truth(t); print(f"闸①:{g1['status']} price={g1.get('price')} cross={g1.get('cross_validated')}")
    dq = dq_score(t); print(f"闸③:DQ={dq['total']} {dq['status']}")
    l4 = l4_health(t); print(f"闸⑥:{l4['status']} {l4.get('name')}")
    kl = get_kline(t,60); print(f"K线:{kl['count']}bars")
    print(f"缓存:{len(_cache)}条")
