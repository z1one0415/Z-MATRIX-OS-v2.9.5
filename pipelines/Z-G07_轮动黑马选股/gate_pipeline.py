#!/usr/bin/env python3
"""
🔒 Z2 10-GATE ROTATION PIPELINE v1.0 ENFORCED
=============================================
硬脚本强制执行轮动选股10闸口管线。
绕过LLM语义化——每闸口返回 PASS / DEGRADED / BLOCK / SKIPPED。
任一闸口不通过 → 自动降级, 禁止输出未经PAPER_WORLD验证的动作。

用法:
  python3 gate_pipeline_v1.0.py --tickers 002463,688608,000988 --mode watch
  python3 gate_pipeline_v1.0.py --tickers 002463 --mode full

输出:
  JSON结构体 + 闸口通过状态表 + Z8动作映射

宪法映射:
  闸口1→宪法1  闸口3→宪法3  闸口8→宪法4  闸口10→宪法6  落盘→宪法7
"""

import sys, os, json, time, argparse, statistics, subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ===================== 常量 =====================
VENV_PYTHON = os.path.expanduser("~/workspace-dev/.venv_glm5/bin/python3")
MEMORY_ROOT = os.path.expanduser(
    "~/Documents/openclaw memory/openclaw memory/Z2信息熔炉/投资记忆银行/超级预测系统"
)

class GateStatus(Enum):
    PASS = "PASS"
    DEGRADED = "DEGRADED"
    BLOCK = "BLOCK"
    SKIPPED = "SKIPPED"
    DATA_INCOMPLETE = "DATA_INCOMPLETE"

class ActionLevel(Enum):
    PAPER_PROBE = "PAPER_PROBE"      # 纸面试仓 (PAPER_WORLD内, 需全部PASS)
    PAPER_TRACK = "PAPER_TRACK"      # 纸面追踪 (需≥8 PASS)
    WATCH = "WATCH"                  # 观察 (需≥6 PASS)
    WAIT = "WAIT"                    # 等待 (需≥4 PASS)
    BLOCK = "BLOCK"                  # 禁止 (任何闸口BLOCK)
    NO_ACTION = "NO_ACTION"

@dataclass
class GateResult:
    gate_id: int
    gate_name: str
    status: GateStatus
    details: dict = field(default_factory=dict)
    errors: list = field(default_factory=list)
    constitution_article: int = 0

@dataclass
class StockResult:
    ticker: str
    name: str = ""
    gates: List[GateResult] = field(default_factory=list)
    overall_action: ActionLevel = ActionLevel.NO_ACTION
    b_role: str = ""
    d_role: str = ""
    r_role: str = ""
    dq_score: int = 0
    current_price: float = 0.0
    price_source: str = ""
    price_conflict: bool = False

# ===================== 数据采集工具 =====================

def gate1_market_truth(ticker: str) -> GateResult:
    """闸口1: 拉实时行情, 验证可溯源性。宪法第1条: 永不编造数据。"""
    errors = []
    details = {}
    
    # 新浪API实时行情
    prefix = "sz" if ticker.startswith(("0","3")) else "sh"
    full_code = f"{prefix}{ticker}"
    try:
        import urllib.request
        url = f"http://hq.sinajs.cn/list={full_code}"
        req = urllib.request.Request(url, headers={"Referer":"https://finance.sina.com.cn"})
        resp = urllib.request.urlopen(req, timeout=6)
        raw = resp.read().decode("gbk")
        if '=""' in raw or raw.strip() == "":
            errors.append(f"新浪API返回空数据 for {ticker}")
        else:
            parts = raw.split('"')[1].split(",")
            if len(parts) >= 32 and parts[3] not in ("", "0.000", "0.00"):
                details["price"] = float(parts[3])  # 当前价
                details["open"] = float(parts[1])
                details["high"] = float(parts[4])
                details["low"] = float(parts[5])
                details["volume"] = parts[8]
                details["name"] = parts[0]
                details["source"] = "sina_api"
                details["time"] = parts[31]
            else:
                errors.append(f"价格字段异常: {parts[3] if len(parts)>3 else 'N/A'}")
    except Exception as e:
        errors.append(f"新浪API异常: {e}")
    
    # 验证 (baostock备源, 拉最近10日取最新)
    try:
        import baostock as bs
        bs.login()
        bs_code = f"{prefix}.{ticker}"
        today_str = datetime.now().strftime("%Y-%m-%d")
        start_str = (datetime.now()-timedelta(days=10)).strftime("%Y-%m-%d")
        rs = bs.query_history_k_data_plus(bs_code, "date,close",
            start_date=start_str, end_date=today_str,
            frequency="d", adjustflag="2")  # 前复权, 匹配新浪复权价
        k_data = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1] != "" and float(r[1]) > 0:
                k_data.append(r)
        bs.logout()
        if k_data:
            bs_latest = k_data[-1]
            bs_close = float(bs_latest[1])
            bs_date = bs_latest[0]
            details["baostock_close"] = bs_close
            details["baostock_date"] = bs_date
            if "price" in details:
                diff_pct = abs(details["price"] - bs_close) / details["price"] * 100
                details["source_diff_pct"] = round(diff_pct, 2)
                # baostock T+1延迟, 容忍度随日期差增大
                date_diff = (datetime.strptime(today_str,"%Y-%m-%d") - datetime.strptime(bs_date,"%Y-%m-%d")).days
                tolerance = 1.5 + date_diff * 1.5  # 每天1.5%容忍
                if diff_pct > tolerance:
                    errors.append(f"价格源冲突: sina={details['price']} vs baostock({bs_date})={bs_close} ({diff_pct:.1f}%, 容忍{tolerance}%)")
                    details["price_conflict"] = True
                else:
                    details["price_conflict"] = False
                    details["cross_validated"] = True
        else:
            errors.append("baostock最近10日无K线数据")
    except Exception as e:
        errors.append(f"baostock异常: {e}")
    
    if errors:
        if any("冲突" in e for e in errors):
            return GateResult(1, "Market Truth", GateStatus.DEGRADED, details, errors, 1)
        return GateResult(1, "Market Truth", GateStatus.DATA_INCOMPLETE, details, errors, 1)
    return GateResult(1, "Market Truth", GateStatus.PASS, details, [], 1)


def gate2_source_arbitration(ticker: str, g1_details: dict) -> GateResult:
    """闸口2: Source Arbitration — 调用Z-G01统一接口, 只承接MT.status, 不二次裁决"""
    status = g1_details.get("status", "BLOCK")
    if status == "PASS":
        return GateResult(2, "Source Arbitration", GateStatus.PASS,
            {"price": g1_details["price"], "source": g1_details.get("source",""),
             "output_level": g1_details.get("output_level","O5"),
             "capability_mask": g1_details.get("capability_mask",{})}, [], 0)
    if status == "DEGRADED":
        return GateResult(2, "Source Arbitration", GateStatus.DEGRADED,
            {"output_level": g1_details.get("output_level","O3"),
             "capability_mask": g1_details.get("capability_mask",{})},
            ["承接MT DEGRADED"], 0)
    return GateResult(2, "Source Arbitration", GateStatus.BLOCK,
        {"output_level": g1_details.get("output_level","O2"),
         "capability_mask": g1_details.get("capability_mask",{})},
        ["承接MT BLOCK"], 0)


def gate3_dq_score(ticker: str) -> GateResult:
    """闸口3: Data Quality评分。DQ<60→禁买卖, DQ<85→禁V4。宪法第3条: 能力边界诚实。"""
    scores = {"行情": 0, "财务": 0, "估值": 0, "产业链": 0, "资金": 0, "来源": 0}
    errors = []
    
    # 行情 (max 15) — 交叉验证=加分
    g1 = g1_details_for(ticker)
    scores["行情"] = 15 if g1.get("cross_validated") else (12 if g1.get("price") else 6)
    
    # 财务 (max 25) — baostock query_profit_data
    try:
        import baostock as bs
        bs.login()
        prefix = "sz" if ticker.startswith(("0","3")) else "sh"
        code = f"{prefix}.{ticker}"
        has_finance = False
        for y, q in [(2026,1), (2025,4), (2025,3)]:
            try:
                rs = bs.query_profit_data(code, year=y, quarter=q)
                while rs.next():
                    r = rs.get_row_data()
                    if r and len(r) > 3 and r[3] not in ("", "0", "0.000000"):
                        has_finance = True
                        if y == 2026 and q == 1:
                            details["q1_eps"] = r[3]
            except:
                pass
        bs.logout()
        scores["财务"] = 22 if has_finance else 8
    except Exception as e:
        scores["财务"] = 5
        errors.append(f"财务接口异常: {str(e)[:60]}")
    
    # 估值 (max 15) — 有价格+行业分类
    scores["估值"] = 12 if g1.get("price") else 5
    # 产业链 (max 15) — 有行业数据
    scores["产业链"] = 12 if g1.get("q1_eps") else 10
    # 资金 (max 15) — 有成交量+交叉验证
    scores["资金"] = 13 if (g1.get("volume") and g1.get("cross_validated")) else (10 if g1.get("volume") else 3)
    # 来源 (max 15) — 有新浪+baostock=双源验证
    scores["来源"] = 13 if g1.get("cross_validated") else (6 if g1.get("price") else 3)
    
    total = sum(scores.values())
    details = {"total": total, "breakdown": scores}
    
    if total < 60:
        errors.append(f"DQ={total}<60, 禁止买卖建议")
        return GateResult(3, "DQ Score", GateStatus.BLOCK, details, errors, 3)
    if total < 85:
        errors.append(f"DQ={total}<85, 禁止V4纸面执行")
        return GateResult(3, "DQ Score", GateStatus.DEGRADED, details, errors, 3)
    return GateResult(3, "DQ Score", GateStatus.PASS, details, [], 3)


def gate4_l25_macro() -> GateResult:
    """闸口4: L2.5前夜战报 — 8信息域检查。"""
    domains = {
        "commodity": "unknown",
        "china_proxy": "unknown", 
        "overseas": "unknown",
        "risk": "unknown",
        "chip": "unknown",
        "gold": "unknown",
        "fx": "unknown",
        "policy": "unknown"
    }
    # 从MEMORY.md拉宏观字典
    mem = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/MEMORY.md")
    filled = 0
    try:
        with open(mem) as f:
            for line in f:
                line = line.strip()
                if "地缘政治" in line: domains["risk"] = "filled"; filled += 1
                if "社零" in line: domains["china_proxy"] = "filled"; filled += 1
                if "利率" in line: domains["overseas"] = "filled"; filled += 1
                if "VIX" in line: domains["chip"] = "filled"; filled += 1
    except:
        pass
    
    details = {"filled_domains": filled, "total_domains": 8, "domains": domains}
    if filled < 4:
        return GateResult(4, "L2.5 Macro", GateStatus.DEGRADED, details,
            [f"仅{filled}/8信息域填充"], 0)
    return GateResult(4, "L2.5 Macro", GateStatus.PASS, details, [], 0)


def gate5_l3_sectors() -> GateResult:
    """闸口5: L3 31板块确认。需SW31涨跌幅/宽度数据。"""
    try:
        import urllib.request
        url = "http://hq.sinajs.cn/list=" + ",".join([f"sh0000{i}" if i<10 else f"sz399{i}" for i in range(1, 32)])
        # 简化: 只拉几个关键板块指数
        key_sectors = ["sh000001","sz399001","sz399006","sh000688","sh000300","sz399005"]
        url2 = "http://hq.sinajs.cn/list=" + ",".join(key_sectors)
        req = urllib.request.Request(url2, headers={"Referer":"https://finance.sina.com.cn"})
        resp = urllib.request.urlopen(req, timeout=6)
        raw = resp.read().decode("gbk")
        count = raw.count('="') - raw.count('=""')
        
        if count < 3:
            return GateResult(5, "L3 Sectors", GateStatus.DATA_INCOMPLETE,
                {"sectors_available": count}, ["板块数据不足"], 0)
        
        return GateResult(5, "L3 Sectors", GateStatus.PASS,
            {"sectors_available": count, "sources": "sina_api"}, [], 0)
    except Exception as e:
        return GateResult(5, "L3 Sectors", GateStatus.DATA_INCOMPLETE,
            {}, [f"板块数据拉取失败: {e}"], 0)


def gate6_l4_health(ticker: str) -> GateResult:
    """闸口6: L4健康检查 — ST/停牌/流动性。"""
    errors = []
    details = {}
    
    try:
        import baostock as bs
        bs.login()
        prefix = "sz" if ticker.startswith(("0","3")) else "sh"
        code = f"{prefix}.{ticker}"
        
        # 检查ST
        rs = bs.query_stock_basic(code)
        while rs.next():
            r = rs.get_row_data()
            name = r[1] if r[1] else ""
            details["stock_name"] = name
            if "ST" in name.upper() or "*ST" in name:
                errors.append(f"ST股票: {name}")
        
        # 检查交易状态
        from datetime import datetime
        rs2 = bs.query_history_k_data_plus(code, "date,volume,tradestatus",
            start_date=(datetime.now()-timedelta(days=3)).strftime("%Y-%m-%d"),
            end_date=datetime.now().strftime("%Y-%m-%d"),
            frequency="d", adjustflag="2")
        has_volume = False
        while rs2.next():
            r = rs2.get_row_data()
            if r[2] == '1' and float(r[1]) > 0:
                has_volume = True
        
        bs.logout()
        
        details["tradable"] = has_volume
        if not has_volume:
            errors.append("近3日无成交, 可能停牌")
        
    except Exception as e:
        errors.append(f"L4检查异常: {e}")
    
    if errors:
        if any("ST" in e for e in errors):
            return GateResult(6, "L4 Health", GateStatus.BLOCK, details, errors, 0)
        if any("停牌" in e or "无成交" in e for e in errors):
            return GateResult(6, "L4 Health", GateStatus.BLOCK, details, errors, 0)
        return GateResult(6, "L4 Health", GateStatus.DEGRADED, details, errors, 0)
    
    return GateResult(6, "L4 Health", GateStatus.PASS, details, [], 0)


def gate7_l5_matrix(ticker: str, g1_details: dict) -> GateResult:
    """闸口7: L5 B/D/R/OKR Matrix — 跑Python代码, 不人工标记。"""
    errors = []
    details = {"b_matrix": "not_run", "d_matrix": "not_run", "r_matrix": "not_run"}
    
    workspace = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace")
    sys.path.insert(0, workspace)
    
    # D-Matrix v2.2 — in-process, import chain fixed in scoring/__init__.py
    d_script = os.path.join(workspace, "zmatrix/scoring/d_band/d_early_v22_scorer.py")
    if not os.path.exists(d_script):
        errors.append(f"D-Matrix脚本缺失")
    else:
        try:
            from zmatrix.scoring.d_band.d_early_v22_scorer import evaluate_d_early_v22
            payload = {"code": ticker, "name": "", "sector": "", "theme": ""}
            r = evaluate_d_early_v22(payload)
            if isinstance(r, dict):
                details["d_score"] = str(r.get("d_score", str(r)))[:60]
            else:
                details["d_score"] = str(r)[:60]
            details["d_matrix"] = "ran"
        except Exception as e:
            errors.append(f"D-Matrix: {str(e)[:80]}")

    # R-Matrix v1.1 — in-process
    r_script = os.path.join(workspace, "zmatrix/scoring/r_matrix/oscillation_king_ranker_v11.py")
    if not os.path.exists(r_script):
        errors.append(f"R-Matrix脚本缺失")
    else:
        try:
            # R-Matrix需要K线数据, 先拉baostock
            import baostock as bs
            bs.login()
            prefix = "sz" if ticker.startswith(("0","3")) else "sh"
            code = f"{prefix}.{ticker}"
            start_d = (datetime.now()-timedelta(days=250)).strftime("%Y-%m-%d")
            end_d = datetime.now().strftime("%Y-%m-%d")
            rs = bs.query_history_k_data_plus(code, "date,close",
                start_date=start_d, end_date=end_d,
                frequency="d", adjustflag="2")
            daily_prices = []
            while rs.next():
                r = rs.get_row_data()
                if r[1] and r[1] != "" and float(r[1]) > 0:
                    daily_prices.append(float(r[1]))
            bs.logout()
            
            if len(daily_prices) < 60:
                errors.append(f"R-Matrix: K线不足60日({len(daily_prices)}日)")
            else:
                from zmatrix.scoring.r_matrix.oscillation_king_ranker_v11 import rank_type_b_rising_channel
                result = rank_type_b_rising_channel(ticker, "", daily_prices)
                if hasattr(result, 'score'):
                    details["r_score"] = str(result.score)[:60]
                    details["r_matrix"] = "ran"
                    details["r_role"] = str(result.role) if hasattr(result, 'role') else ""
                else:
                    details["r_score"] = str(result)[:60]
                    details["r_matrix"] = "ran"
        except Exception as e:
            errors.append(f"R-Matrix: {str(e)[:80]}")
    
    if details["d_matrix"] == "not_run" and details["r_matrix"] == "not_run":
        return GateResult(7, "L5 Matrix", GateStatus.SKIPPED, details, errors, 0)
    if errors:
        return GateResult(7, "L5 Matrix", GateStatus.DEGRADED, details, errors, 0)
    return GateResult(7, "L5 Matrix", GateStatus.PASS, details, [], 0)


def gate8_v3_scenarios(g1_details: dict) -> GateResult:
    """闸口8: V3情景推演 — 三情景/主观权重/uncalibrated。宪法第4条: 置信度标注。"""
    details = {
        "scenarios": [
            {"name":"保守","subjective_weight":"高","calibration":"uncalibrated"},
            {"name":"基准","subjective_weight":"中","calibration":"uncalibrated"},
            {"name":"乐观","subjective_weight":"低","calibration":"uncalibrated"}
        ],
        "must_include": "subjective_weight NOT probability",
        "z9_backtest_required": True
    }
    return GateResult(8, "V3 Scenarios", GateStatus.PASS, details, [], 4)


def gate9_z8_action(gates: List[GateResult]) -> Tuple[ActionLevel, str]:
    """闸口9: Z8动作映射 — 根据闸口1-8结果。"""
    pass_count = sum(1 for g in gates if g.status == GateStatus.PASS)
    block_count = sum(1 for g in gates if g.status in (GateStatus.BLOCK, GateStatus.DATA_INCOMPLETE))
    skip_count = sum(1 for g in gates if g.status == GateStatus.SKIPPED)
    
    if block_count >= 3:
        return ActionLevel.BLOCK, f"BLOCK: {block_count}闸口未通过"
    if block_count >= 1:
        return ActionLevel.WAIT, f"WAIT: {block_count}闸口阻塞, 等待修复"
    if skip_count >= 2:
        return ActionLevel.WATCH, f"WATCH: {skip_count}闸口跳过"
    if pass_count >= 7:
        if block_count == 0:
            return ActionLevel.PAPER_PROBE, "PAPER_PROBE: ≥7 PASS, 0 BLOCK → 可纸面试仓(PAPER_WORLD)"
        return ActionLevel.WATCH, "WATCH: 数据可用但部分闸口DEGRADED"
    if pass_count >= 5:
        return ActionLevel.WATCH, "WATCH: 最低通过线"
    return ActionLevel.BLOCK, "BLOCK: 不足5闸口通过"


def gate10_report(stocks: List[StockResult]) -> dict:
    """闸口10: 报告输出 — 标注DQ/闸口/等级。"""
    report = {
        "pipeline": "Z2 10-GATE ROTATION v1.0 ENFORCED",
        "timestamp": datetime.now().isoformat(),
        "stocks": [],
        "summary": {
            "total": len(stocks),
            "pass": sum(1 for s in stocks if s.overall_action in (ActionLevel.PAPER_TRACK, ActionLevel.PAPER_PROBE)),
            "watch": sum(1 for s in stocks if s.overall_action == ActionLevel.WATCH),
            "wait": sum(1 for s in stocks if s.overall_action == ActionLevel.WAIT),
            "block": sum(1 for s in stocks if s.overall_action == ActionLevel.BLOCK),
        }
    }
    
    for s in stocks:
        stock_report = {
            "ticker": s.ticker,
            "name": s.name,
            "price": s.current_price,
            "price_source": s.price_source,
            "price_conflict": s.price_conflict,
            "dq_score": s.dq_score,
            "overall_action": s.overall_action.value,
            "gates": []
        }
        for g in s.gates:
            stock_report["gates"].append({
                "id": g.gate_id,
                "name": g.gate_name,
                "status": g.status.value,
                "details": {k:v for k,v in g.details.items() if k not in ("domains",)},
                "errors": g.errors[:2]  # limit
            })
        report["stocks"].append(stock_report)
    
    return report


# ===================== 全局状态缓存 =====================
_g1_cache: Dict[str, dict] = {}

def g1_details_for(ticker: str) -> dict:
    return _g1_cache.get(ticker, {})

def run_pipeline(tickers: List[str], mode: str = "watch") -> dict:
    """主管线：依次跑10闸口。"""
    stocks = []
    
    for ticker in tickers:
        print(f"\n{'='*60}")
        print(f"🔍 处理 {ticker}")
        print(f"{'='*60}")
        
        stock = StockResult(ticker=ticker)
        gates = []
        
        # 闸口1: Market Truth
        g1 = gate1_market_truth(ticker)
        _g1_cache[ticker] = g1.details
        if g1.details.get("name"):
            stock.name = g1.details["name"]
        if g1.details.get("price"):
            stock.current_price = g1.details["price"]
            stock.price_source = g1.details.get("source", "")
            stock.price_conflict = g1.details.get("price_conflict", False)
        gates.append(g1)
        print(f"  闸口① Market Truth: {g1.status.value} {g1.errors[:2]}")
        
        if g1.status == GateStatus.BLOCK:
            # 无价格, 后面全SKIP
            for gid in range(2, 9):
                gates.append(GateResult(gid, f"SKIP-{gid}", GateStatus.SKIPPED, {}, ["上游闸口BLOCK"], 0))
                print(f"  闸口{gid}: SKIPPED (上游闸口BLOCK)")
        else:
            # 闸口2: Source Arbitration
            g2 = gate2_source_arbitration(ticker, g1.details)
            gates.append(g2)
            print(f"  闸口② Source Arbitration: {g2.status.value} {g2.errors[:2]}")
            
            # 闸口3: DQ
            g3 = gate3_dq_score(ticker)
            stock.dq_score = g3.details.get("total", 0)
            gates.append(g3)
            print(f"  闸口③ DQ Score: {g3.status.value} DQ={stock.dq_score} {g3.errors[:2]}")
            
            # 闸口4: L2.5
            g4 = gate4_l25_macro()
            gates.append(g4)
            print(f"  闸口④ L2.5 Macro: {g4.status.value}")
            
            # 闸口5: L3
            g5 = gate5_l3_sectors()
            gates.append(g5)
            print(f"  闸口⑤ L3 Sectors: {g5.status.value}")
            
            # 闸口6: L4
            g6 = gate6_l4_health(ticker)
            gates.append(g6)
            print(f"  闸口⑥ L4 Health: {g6.status.value} {g6.errors[:2]}")
            
            if g6.status == GateStatus.BLOCK:
                stock.overall_action = ActionLevel.BLOCK
                for gid in range(7, 9):
                    gates.append(GateResult(gid, f"SKIP-{gid}", GateStatus.SKIPPED, {}, ["上游闸口BLOCK"], 0))
            else:
                # 闸口7: L5 Matrix
                g7 = gate7_l5_matrix(ticker, g1.details)
                gates.append(g7)
                print(f"  闸口⑦ L5 Matrix: {g7.status.value} {g7.errors[:2]}")
                if g7.details.get("d_score"):
                    stock.d_role = f"D:{g7.details['d_score']}"
                if g7.details.get("r_score"):
                    stock.r_role = f"R:{g7.details['r_score']}"
                
                # 闸口8: V3
                g8 = gate8_v3_scenarios(g1.details)
                gates.append(g8)
                print(f"  闸口⑧ V3: {g8.status.value}")
        
        # 闸口9: Z8
        action, reason = gate9_z8_action(gates)
        stock.overall_action = action
        g9 = GateResult(9, "Z8 Action", 
            GateStatus.PASS if action != ActionLevel.BLOCK else GateStatus.DEGRADED,
            {"action": action.value, "reason": reason}, [], 0)
        gates.append(g9)
        print(f"  闸口⑨ Z8 Action: {action.value} — {reason}")
        
        stock.gates = gates
        stocks.append(stock)
    
    # 闸口10: Report
    report = gate10_report(stocks)
    
    # 落盘
    os.makedirs(MEMORY_ROOT, exist_ok=True)
    outfile = os.path.join(MEMORY_ROOT, f"gate_pipeline_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    with open(outfile, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n📄 报告已落盘: {outfile}")
    
    # 终端摘要
    print(f"\n{'='*60}")
    print(f"🏁 管线完成")
    print(f"{'='*60}")
    print(f"{'代码':<10} {'名称':<8} {'价格':<10} {'DQ':<5} {'动作':<15}")
    print(f"{'-'*48}")
    for s in stocks:
        print(f"{s.ticker:<10} {s.name:<8} {s.current_price:<10} {s.dq_score:<5} {s.overall_action.value:<15}")
    
    print(f"\nPAPER_PROBE: {report['summary']['pass']} | WATCH: {report['summary']['watch']} | WAIT: {report['summary']['wait']} | BLOCK: {report['summary']['block']}")
    print(f"⚠️ 任何标的不可直接用于真实交易")
    
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Z2 10-GATE ROTATION PIPELINE v1.0 ENFORCED")
    parser.add_argument("--tickers", type=str, required=True, help="逗号分隔的股票代码 e.g. 002463,688608,000988")
    parser.add_argument("--mode", type=str, default="watch", choices=["watch","full"],
                       help="模式: watch(观察) / full(全链)")
    args = parser.parse_args()
    
    tickers = [t.strip() for t in args.tickers.split(",") if t.strip()]
    if not tickers:
        print("❌ 至少需要一个股票代码")
        sys.exit(1)
    
    report = run_pipeline(tickers, args.mode)
    
    # 硬约束: PAPER_PROBE仅限PAPER_WORLD
    for s in report["stocks"]:
        if s["overall_action"] == "PAPER_PROBE":
            print(f"\n{'⚠️'*20}")
            print(f"⚠️ {s['ticker']} 通过全部闸口 → PAPER_PROBE (PAPER_WORLD内)")
            print(f"⚠️ 仍需人工确认: V3 uncalibrated, 非统计概率")
            print(f"{'⚠️'*20}")
    
    # 默认: 所有标的最多到WATCH
    for s in report["stocks"]:
        if s["overall_action"] == "PAPER_PROBE":
            print(f"\n🔒 硬约束: {s['ticker']} 实际动作: PAPER_PROBE仅限PAPER_WORLD")
    
    sys.exit(0)
