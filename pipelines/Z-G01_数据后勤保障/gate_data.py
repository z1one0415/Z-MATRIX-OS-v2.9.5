#!/usr/bin/env python3
"""🛢️ Z-G01 gate_data.py — 数据后勤保障主引擎 (Data Service Layer)
NOT a pipeline script. All pipelines consume this service via z17_loader. (v1.0)
所有管线通过z17_loader导入此模块。提供8个标准数据函数。
门禁: 分级TTL(行情3s/财务1d/画像7d), 降级链: Sina→baostock→Tushare→DEGRADED
"""

import json, time, urllib.request, sys, os
from pathlib import Path
from datetime import datetime, timedelta

# ═══ Tushare 数据源 (主力) ═══
_TUSHARE_PRO = None
_TUSHARE_AVAILABLE = False

def _get_ts_pro():
    """初始化 tushare pro_api（惰性加载）"""
    global _TUSHARE_PRO, _TUSHARE_AVAILABLE
    if _TUSHARE_PRO is not None:
        return _TUSHARE_PRO
    # 从多来源读取 token
    token = os.environ.get("TUSHARE_TOKEN") or ""
    if not token:
        try:
            tp = Path.home() / ".tushare" / "token"
            if tp.exists():
                token = tp.read_text().strip()
        except:
            pass
    if not token:
        _TUSHARE_AVAILABLE = False
        return None
    try:
        import tushare as ts
        ts.set_token(token)
        _TUSHARE_PRO = ts.pro_api()
        _TUSHARE_AVAILABLE = True
        return _TUSHARE_PRO
    except Exception:
        _TUSHARE_AVAILABLE = False
        return None

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


# ═══ Tushare 数据源: 日K线 (主力) ═══
def _ts_kline(ticker, days=120, adjust="qfq"):
    """tushare 日K线 — 主力数据源。
    adjust="qfq" → 前复权 (默认, 用于研究/均线/形态)
    adjust=None  → 不复权 (用于执行验证)
    降级: tushare→baostock
    """
    pro = _get_ts_pro()
    if pro is None:
        return _bs_kline_internal(ticker, days, adjust="research" if adjust=="qfq" else "raw")
    try:
        suffix = "SZ" if ticker[0] in "03" else "SH"
        ts_code = f"{ticker}.{suffix}"
        end = datetime.now().strftime("%Y%m%d")
        start = (datetime.now() - timedelta(days=days + 30)).strftime("%Y%m%d")
        df = pro.daily(ts_code=ts_code, start_date=start, end_date=end)
        if df is None or df.empty:
            return _bs_kline_internal(ticker, days, adjust="research" if adjust=="qfq" else "raw")
        df = df.sort_values("trade_date")
        rows = []
        for _, r in df.iterrows():
            rows.append({
                "date": r["trade_date"],
                "open": float(r["open"]),
                "high": float(r["high"]),
                "low": float(r["low"]),
                "close": float(r["close"]),
                "volume": float(r["vol"]) if "vol" in r and r["vol"] else 0.0,
                "amount": float(r["amount"]) if "amount" in r and r["amount"] else 0.0,
            })
        # 前复权: 用 adj_factor API 调整全部价格
        if adjust == "qfq":
            try:
                adj_df = pro.adj_factor(ts_code=ts_code)
                if adj_df is not None and not adj_df.empty:
                    adj_df = adj_df.sort_values("trade_date")
                    latest_adj = float(adj_df.iloc[-1]["adj_factor"])
                    for row in rows:
                        adj_row = adj_df[adj_df["trade_date"] == row["date"]]
                        if not adj_row.empty:
                            factor = float(adj_row.iloc[0]["adj_factor"])
                            if factor > 0:
                                ratio = latest_adj / factor
                                row["open"] = round(row["open"] * ratio, 2)
                                row["high"] = round(row["high"] * ratio, 2)
                                row["low"] = round(row["low"] * ratio, 2)
                                row["close"] = round(row["close"] * ratio, 2)
                                row["volume"] = int(row["volume"] * ratio)
            except Exception:
                pass
        return {
            "dates": [r["date"] for r in rows],
            "open": [r["open"] for r in rows],
            "high": [r["high"] for r in rows],
            "low": [r["low"] for r in rows],
            "close": [r["close"] for r in rows],
            "volume": [r["volume"] for r in rows],
            "amount": [r["amount"] for r in rows],
            "prices": [r["close"] for r in rows],
            "count": len(rows),
            "source": "tushare",
            "adjust": adjust,
            "data_contract": "OHLCV_DAILY_V1",
        }
    except Exception as e:
        return _bs_kline_internal(ticker, days, adjust="research" if adjust=="qfq" else "raw")

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


# ═══ Tushare 数据源: 财务指标 (主力, 降级→baostock) ═══
def _ts_finance(ticker):
    """tushare 财务指标。降级链: tushare→_bs_finance
    通过 fina_indicator + daily_basic 获取核心指标。
    """
    pro = _get_ts_pro()
    if pro is None:
        return _bs_finance(ticker)
    try:
        suffix = "SZ" if ticker[0] in "03" else "SH"
        ts_code = f"{ticker}.{suffix}"
        df = pro.fina_indicator(ts_code=ts_code, start_date="20251231")
        if df is None or df.empty:
            return _bs_finance(ticker)
        r = df.iloc[0]
        rv = {
            "symbol": ticker, "industry": "",
            "has_finance": True,
            "q1_eps": float(r.get("eps", 0)) if r.get("eps") and str(r["eps"]).strip() != "" else None,
            "roe_5y_avg": float(r.get("roe", 0)) / 100 if r.get("roe") and str(r["roe"]).strip() != "" else None,
            "roic_5y": float(r.get("roic", 0)) / 100 if r.get("roic") and str(r["roic"]).strip() != "" else None,
            "gross_margin": float(r.get("gross_margin")) / 100 if r.get("gross_margin") and str(r["gross_margin"]).strip() != "" else None,
            "debt_ratio": float(r.get("debt_to_assets")) / 100 if r.get("debt_to_assets") and str(r["debt_to_assets"]).strip() != "" else None,
            "pe_ttm": None, "pb": None,
        }
        # 补 PE/PB
        try:
            db = pro.daily_basic(ts_code=ts_code, start_date="20260501", end_date="20260526", fields="trade_date,pe,pb")
            if db is not None and not db.empty:
                last = db.iloc[-1]
                rv["pe_ttm"] = float(last["pe"]) if last.get("pe") and str(last["pe"]).strip() != "" else None
                rv["pb"] = float(last["pb"]) if last.get("pb") and str(last["pb"]).strip() != "" else None
        except Exception:
            pass
        return rv
    except Exception:
        return _bs_finance(ticker)

def _bs_finance(ticker):
    """B-Matrix financial data contract — returns FINANCIAL_BMATRIX_V1 fields.
    Missing fields are None + logged in missing_fields. Never fabricates data."""
    try:
        import baostock as bs; bs.login()
        pfx = "sz" if ticker[0] in "03" else "sh"
        code = f"{pfx}.{ticker}"
        rv = {
            "symbol": ticker, "industry": "",
            "has_finance": False,
            # Profitability
            "q1_eps": None, "roe_5y_avg": None, "roic_5y": None,
            "roe_trend": None, "roic_trend": None,
            "gross_margin": None, "gross_margin_stability": None,
            # Valuation
            "pe_ttm": None, "pb": None,
            "profit_percentile_5y": None,
            # Balance sheet
            "debt_ratio": None, "goodwill_ratio": None,
            "interest_bearing_debt_growth_2y": None,
            # Dividend
            "dividend_yield": None, "dividend_years_stable": None,
            "dividends_paid_2y": None,
            # Cash flow
            "ocf_2y": None, "ocf_3y": None,
            "net_profit_3y": None, "capex_2y": None,
            # Qualitative (not from baostock, explicit stub)
            "is_state_owned": None,
            "brand_premium_score": None,
            "pricing_power_score": None,
            "supply_constraint_score": None,
            "scarcity_durability_score": None,
            "brand_mindshare_score": None,
            "channel_health_score": None,
            "policy_stability_score": None,
            "asset_monopoly_score": None,
            "cost_curve_score": None,
            "resource_quality_score": None,
            # Contract
            "data_contract": "FINANCIAL_BMATRIX_V1",
            "missing_fields": [],
        }
        missing = []

        # 1. Profit data (EPS + try ROE from 4 quarters)
        for y, q in [(2026, 1), (2025, 4), (2025, 3), (2025, 2), (2025, 1), (2024, 4)]:
            try:
                rs = bs.query_profit_data(code, year=y, quarter=q)
                while rs.next():
                    r = rs.get_row_data()
                    if r and len(r) > 3 and r[3] not in ("", "0", "0.000000"):
                        rv["has_finance"] = True
                        if y == 2026 and q == 1:
                            rv["q1_eps"] = r[3]
                        # ROE: index varies by baostock version, try r[5] or r[7]
                        if len(r) > 7 and r[7] and r[7] not in ("", "0"):
                            try:
                                rv["roe_5y_avg"] = rv.get("roe_5y_avg") or float(r[7])
                            except ValueError: pass
            except Exception:
                pass

        # 2. Industry
        try:
            rs = bs.query_stock_industry(code)
            while rs.next():
                r = rs.get_row_data()
                if len(r) > 3:
                    rv["industry"] = r[3]
        except Exception:
            pass

        # 3. Latest PE/PB from daily K-line (cheapest path)
        try:
            from datetime import timedelta
            s = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            e = datetime.now().strftime("%Y-%m-%d")
            rs = bs.query_history_k_data_plus(code, "date,peTTM,pbMRQ",
                                              start_date=s, end_date=e, frequency="d", adjustflag="2")
            while rs.next():
                r = rs.get_row_data()
                if len(r) > 2 and r[1] and r[1] != "" and float(r[1]) > 0:
                    rv["pe_ttm"] = float(r[1])
                if len(r) > 2 and r[2] and r[2] != "" and float(r[2]) > 0:
                    rv["pb"] = float(r[2])
        except Exception:
            missing.append("pe_ttm,pb")

        # 4. Balance sheet: try to get debt_ratio from latest report
        try:
            rs = bs.query_balance_data(code, year=2026, quarter=1)
            while rs.next():
                r = rs.get_row_data()
                # debt_ratio ≈ total_liability / total_assets
                if len(r) > 10:
                    try:
                        tl = float(r[8]) if r[8] and r[8] != "" else None
                        ta = float(r[7]) if r[7] and r[7] != "" else None
                        if tl and ta and ta > 0:
                            rv["debt_ratio"] = round(tl / ta, 3)
                    except (ValueError, IndexError): pass
                # goodwill
                if len(r) > 20:
                    try:
                        gw = float(r[20]) if r[20] and r[20] != "" else 0
                        na = float(r[12]) if len(r) > 12 and r[12] and r[12] != "" else ta
                        if na and na > 0 and gw > 0:
                            rv["goodwill_ratio"] = round(gw / na, 4)
                    except (ValueError, IndexError): pass
        except Exception:
            missing.append("balance_sheet")

        # 5. Cash flow: OCF from latest report
        try:
            rs = bs.query_cash_flow_data(code, year=2026, quarter=1)
            while rs.next():
                r = rs.get_row_data()
                # OCF index varies; try common positions
                for idx in [5, 6, 7, 9]:
                    if len(r) > idx and r[idx] and r[idx] not in ("", "0"):
                        try:
                            ocf = float(r[idx])
                            if abs(ocf) > 1000:  # plausibly real OCF in 万元
                                rv["ocf_3y"] = [ocf]  # single period, partial
                                break
                        except ValueError: pass
        except Exception:
            missing.append("cash_flow")

        rv["missing_fields"] = missing
        bs.logout()
        return rv
    except Exception as ex:
        return {"error": str(ex)[:60], "has_finance": False, "missing_fields": ["baostock_unavailable"]}

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
        lt_close = kdata["close"][-1] if kdata.get("close") else bs["prices"][-1]
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
    # 主力: tushare, 降级: baostock
    kdata = _ts_kline(ticker, max(n+30, 100), adjust="qfq")
    if kdata.get("error"):
        kdata = _bs_research_kline(ticker, max(n+30, 100))
    if kdata.get("error"): return {"status":"DATA_INCOMPLETE","prices":[],"error":kdata["error"]}
    # Extract OHLCV arrays, trim to n
    rv = {
        "status": "PASS" if kdata.get("count",0) >= min(n,20) else "DEGRADED",
        "prices": kdata["close"][-n:] if kdata.get("close") else [],
        "open": kdata["open"][-n:] if kdata.get("open") else [],
        "high": kdata["high"][-n:] if kdata.get("high") else [],
        "low": kdata["low"][-n:] if kdata.get("low") else [],
        "close": kdata["close"][-n:] if kdata.get("close") else [],
        "volume": kdata["volume"][-n:] if kdata.get("volume") else [],
        "amount": kdata["amount"][-n:] if kdata.get("amount") else [],
        "count": min(n, kdata.get("count", 0)),
        "data_contract": kdata.get("data_contract", "OHLCV_DAILY_V1"),
        "price_basis": "adjusted_research",
    }
    if kdata.get("missing_fields"):
        rv["missing_fields"] = kdata["missing_fields"]
    _cache_set(ck, rv); return rv

def get_financials(ticker):
    ck = f"fin_{ticker}"
    if _cache_get(ck, ttl=86400): return _cache_get(ck, ttl=86400)
    # 主力: tushare, 降级: baostock
    fin = _ts_finance(ticker)
    # Ensure FINANCIAL_BMATRIX_V1 contract shape — fill missing keys with None
    defaults = {
        "symbol": ticker, "industry": "", "has_finance": False,
        "q1_eps": None, "roe_5y_avg": None, "roic_5y": None,
        "roe_trend": None, "roic_trend": None,
        "gross_margin": None, "gross_margin_stability": None,
        "pe_ttm": None, "pb": None, "profit_percentile_5y": None,
        "debt_ratio": None, "goodwill_ratio": None,
        "interest_bearing_debt_growth_2y": None,
        "dividend_yield": None, "dividend_years_stable": None,
        "dividends_paid_2y": None,
        "ocf_2y": None, "ocf_3y": None, "net_profit_3y": None, "capex_2y": None,
        "is_state_owned": None,
        "brand_premium_score": None, "pricing_power_score": None,
        "supply_constraint_score": None, "scarcity_durability_score": None,
        "brand_mindshare_score": None, "channel_health_score": None,
        "policy_stability_score": None, "asset_monopoly_score": None,
        "cost_curve_score": None, "resource_quality_score": None,
        "data_contract": "FINANCIAL_BMATRIX_V1",
        "missing_fields": [],
    }
    for k, v in defaults.items():
        if k not in fin:
            fin[k] = v
    
    # Real missing_fields + coverage computation
    BMATRIX_REQUIRED = [
        "roe_5y_avg", "roic_5y", "pe_ttm", "pb",
        "dividend_yield", "debt_ratio",
        "ocf_3y", "net_profit_3y", "goodwill_ratio",
    ]
    missing = [k for k in BMATRIX_REQUIRED if fin.get(k) is None]
    fin["missing_fields"] = sorted(set(fin.get("missing_fields", []) + missing))
    fin["financial_coverage_ratio"] = round(1 - len(missing) / len(BMATRIX_REQUIRED), 3) if BMATRIX_REQUIRED else 1.0
    
    # B5 brand scarcity evidence coverage (separate from financial coverage)
    B5_REQUIRED = [
        "brand_premium_score", "pricing_power_score",
        "scarcity_durability_score", "brand_mindshare_score",
        "channel_health_score", "terminal_price_stability_score",
        "young_consumer_relevance_score",
    ]
    b5_missing = [k for k in B5_REQUIRED if fin.get(k) is None]
    fin["b5_missing_fields"] = b5_missing
    fin["b5_evidence_coverage_ratio"] = round(1 - len(b5_missing) / len(B5_REQUIRED), 3) if B5_REQUIRED else 0.0
    
    if fin["financial_coverage_ratio"] < 0.5:
        fin["status"] = "DATA_INCOMPLETE"
    elif fin.get("has_finance"):
        fin["status"] = "PASS"
    else:
        fin["status"] = "DEGRADED"
    _cache_set(ck, fin); return fin

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
    mem = os.environ.get(
        "Z_MATRIX_MEMORY_FILE",
        str(Path(__file__).resolve().parents[2] / "MEMORY.md")
    )
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
    rv = {"status":"PASS" if f>=4 else "DEGRADED","filled":f,"total":8,"domains":dm,
          "proxy_level":"KEYWORD_PROXY",
          "transmission":"NOT_FULL_MACRO_TRANSMISSION",
          "memory_source": mem}
    return rv

# ═══ 海外资产 + 新闻快讯 (Z-G02/Z-G08消费) ═══

OVERSEAS_ASSETS: dict[str, dict] = {
    "VIX":   {"sina": "gb_vix",  "name": "恐慌指数", "decimals": 1},
    "SOX":   {"sina": "gb_sox",  "name": "费城半导体", "decimals": 0},
    "KWEB":  {"sina": "gb_kweb", "name": "中概互联网", "decimals": 1},
    "GC":    {"sina": "hf_GC",   "name": "COMEX黄金",  "decimals": 0},
    "CL":    {"sina": "hf_CL",   "name": "WTI原油",    "decimals": 2},
    "CNH":   {"sina": "USDCNH",  "name": "离岸人民币", "decimals": 4},
    "A50":   {"sina": "nq_sf",   "name": "A50期货",    "decimals": 0},
}


def _fetch_overseas_sina(sina_code: str) -> tuple:
    """Sina海外资产 — gb_*: field[0]=name, field[1]=price, field[2]=pct.
    hf_*: field[0]=price. Returns (price, pct)."""
    try:
        url = f"https://hq.sinajs.cn/list={sina_code}"
        req = urllib.request.Request(url, headers={"Referer":"https://finance.sina.com.cn"})
        raw = urllib.request.urlopen(req, timeout=8).read().decode("gbk", errors="replace")
        if "=" not in raw: return None, None
        parts = raw.split("=",1)[1].strip().strip('";').split(",")
        if len(parts) < 2: return None, None
        try:
            price = float(parts[0])
            pct = float(parts[1]) if len(parts) > 1 and parts[1] else None
        except ValueError:
            try: price = float(parts[1]); pct = float(parts[2]) if len(parts) > 2 and parts[2] else None
            except (ValueError, IndexError): return None, None
        return round(price, 6), round(pct, 2) if pct is not None else None
    except: return None, None


def fetch_overseas_assets() -> dict:
    """统一海外资产数据 — Z-G01中枢提供，Z-G02直接消费"""
    ck = "overseas"
    if _cache_get(ck, ttl=60): return _cache_get(ck, ttl=60)
    results = {}
    for key, meta in OVERSEAS_ASSETS.items():
        price, pct = _fetch_overseas_sina(meta["sina"])
        results[key] = {
            "name": meta["name"], "decimals": meta["decimals"],
            "price": round(price, meta["decimals"]) if price is not None else None,
            "pct": pct, "key": key, "status": "ok" if price is not None else "fetch_failed",
        }
    rv = {"status": "PASS" if sum(1 for r in results.values() if r["price"]) >= 3 else "DEGRADED",
          "assets": results, "count": len(results),
          "online": sum(1 for r in results.values() if r["price"]),
          "pipeline_signature": "Z-G01_overseas_v1"}
    _cache_set(ck, rv); return rv


def fetch_news_headlines(max_items: int = 15) -> dict:
    """统一新闻快讯 — 东方财富+Sina"""
    ck = "news"
    if _cache_get(ck, ttl=300): return _cache_get(ck, ttl=300)
    headlines = []
    errors = []
    # 东方财富公告
    try:
        url = "https://np-anotice-stock.eastmoney.com/api/security/ann?page_size=10&page_index=1&ann_type=SHA"
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        data = json.loads(urllib.request.urlopen(req, timeout=8).read())
        for item in data.get("data",{}).get("list",[])[:10]:
            headlines.append(item.get("title","")[:120])
    except Exception as e: errors.append(f"eastmoney:{str(e)[:60]}")
    # Sina finance headlines
    try:
        url = "https://finance.sina.com.cn/"
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0","Referer":"https://finance.sina.com.cn/"})
        raw = urllib.request.urlopen(req, timeout=8).read().decode("gbk", errors="replace")
        import re
        for m in re.finditer(r'<title>(.*?)</title>', raw):
            t = m.group(1).strip()
            if len(t) > 10 and t not in headlines:
                headlines.append(t[:120])
    except Exception as e: errors.append(f"sina:{str(e)[:60]}")
    if not headlines: errors.append("no_news_sources")
    rv = {"status": "PASS" if headlines else "DEGRADED",
          "headlines": headlines[:max_items], "count": len(headlines[:max_items]),
          "errors": errors, "pipeline_signature": "Z-G01_news_v1"}
    _cache_set(ck, rv); return rv



# ═══ 磁盘持久化缓存 (data/price_bars/*.csv + data/fundamentals/*.csv) ═══
_DATA_CACHE_DIRS = {
    "price_bars": Path(__file__).resolve().parents[2] / "data" / "price_bars",
    "fundamentals": Path(__file__).resolve().parents[2] / "data" / "fundamentals",
}
for _d in _DATA_CACHE_DIRS.values():
    _d.mkdir(parents=True, exist_ok=True)

def _disk_cache_save(data_type: str, ticker: str, rows: list[dict]):
    import csv
    path = _DATA_CACHE_DIRS.get(data_type)
    if path is None or not rows:
        return
    filepath = path / f"{ticker}.csv"
    with open(filepath, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

def _disk_cache_load(data_type: str, ticker: str) -> list[dict] | None:
    import csv
    path = _DATA_CACHE_DIRS.get(data_type)
    if path is None:
        return None
    filepath = path / f"{ticker}.csv"
    if not filepath.exists():
        return None
    try:
        with open(filepath, "r", encoding="utf-8-sig") as f:
            return list(csv.DictReader(f))
    except Exception:
        return None

def disk_cache_persist(ticker: str, kline_result: dict):
    """将 get_kline / _ts_kline 的结果持久化到 data/price_bars/{ticker}.csv"""
    dates = kline_result.get("dates", [])
    if not dates:
        return
    n = len(dates)
    rows = []
    for i in range(n):
        rows.append({
            "date": dates[i],
            "open": str(kline_result["open"][i]) if i < len(kline_result.get("open", [])) else "",
            "high": str(kline_result["high"][i]) if i < len(kline_result.get("high", [])) else "",
            "low": str(kline_result["low"][i]) if i < len(kline_result.get("low", [])) else "",
            "close": str(kline_result["close"][i]) if i < len(kline_result.get("close", [])) else "",
            "volume": str(kline_result["volume"][i]) if i < len(kline_result.get("volume", [])) else "",
            "amount": str(kline_result["amount"][i]) if i < len(kline_result.get("amount", [])) else "",
        })
    _disk_cache_save("price_bars", ticker, rows)

def disk_cache_save_financial(ticker: str, fin_result: dict):
    """将 get_financials 结果持久化到 data/fundamentals/{ticker}_fin.csv"""
    import csv
    path = _DATA_CACHE_DIRS["fundamentals"] / f"{ticker}_fin.csv"
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(fin_result.keys()))
        w.writeheader()
        w.writerow(fin_result)


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv)>1 else "002463"
    g1 = market_truth(t); print(f"闸①:{g1['status']} price={g1.get('price')} cross={g1.get('cross_validated')}")
    dq = dq_score(t); print(f"闸③:DQ={dq['total']} {dq['status']}")
    l4 = l4_health(t); print(f"闸⑥:{l4['status']} {l4.get('name')}")
    kl = get_kline(t,60); print(f"K线:{kl['count']}bars")
    print(f"缓存:{len(_cache)}条")
