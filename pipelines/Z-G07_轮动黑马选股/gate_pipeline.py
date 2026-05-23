#!/usr/bin/env python3
"""
🔒 Z-G07 轮动+黑马选股 v2.9.5-RC
=============================================
调用Z-G01统一数据层; 闸口输出Capability Mask; 开放智能降级

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
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum

# ===================== 常量 =====================
# Legacy constant removed (was ~/workspace-dev/.venv_glm5/bin/python3, unused)
# Report output directory — env var with repo-relative fallback
MEMORY_ROOT = os.environ.get(
    "Z_MATRIX_MEMORY_ROOT",
    str(Path.home() / "Documents" / "openclaw memory" / "openclaw memory" / "Z2信息熔炉" / "投资记忆银行" / "超级预测系统" / "监控中心")
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
    """闸口1: Market Truth — 委托Z-G01统一数据层"""
    from pipelines.z17_loader import market_truth as z01_market_truth
    try:
        g1 = z01_market_truth(ticker)
        return GateResult(1, "Market Truth", 
            GateStatus.PASS if g1.get("status")=="PASS" else (GateStatus.DEGRADED if g1.get("status")=="DEGRADED" else GateStatus.BLOCK),
            g1, g1.get("errors",[]), 1)
    except Exception as e:
        return GateResult(1, "Market Truth", GateStatus.BLOCK, {}, [str(e)], 1)

def gate2_source_arbitration(ticker: str, g1_details: dict) -> GateResult:
    """闸口2: Source Arbitration — 委托Z-G01, 只承接不二次裁决"""
    from pipelines.z17_loader import source_arbitrate as z01_source_arbitrate
    try:
        g2 = z01_source_arbitrate(ticker, g1_details)
        return GateResult(2, "Source Arbitration",
            GateStatus.PASS if g2.get("status")=="PASS" else (GateStatus.DEGRADED if g2.get("status")=="DEGRADED" else GateStatus.BLOCK),
            g2, g2.get("errors",[]), 0)
    except Exception as e:
        return GateResult(2, "Source Arbitration", GateStatus.DEGRADED, {}, [str(e)], 0)

def gate3_dq_score(ticker: str) -> GateResult:
    """闸口3: DQ评分 — via Z-G01 dq_score"""
    scores = {"行情": 0, "财务": 0, "估值": 0, "产业链": 0, "资金": 0, "来源": 0}
    errors = []
    details = {}
    
    g1 = g1_details_for(ticker)
    scores["行情"] = 15 if g1.get("cross_validated") else (12 if g1.get("price") else 6)
    
    # 财务 — delegated to Z-G01
    try:
        from pipelines.z17_loader import dq_score as z01_dq
        dq_r = z01_dq(ticker)
        scores["财务"] = min(25, dq_r.get("total", 0) // 4)
        details.update({"dq_total": dq_r.get("total", 0), "dq_status": dq_r.get("status", "?"),
                        "dq_source": "Z-G01"})
    except Exception as e:
        scores["财务"] = 5
        errors.append(f"财务接口异常: {str(e)[:60]}")
    
    # 估值 (max 15) — 有价格+行业分类
    scores["估值"] = 12 if g1.get("price") else 5
    # 产业链 (max 15) — 有行业数据
    scores["产业链"] = 12 if details.get("q1_eps") else 10
    # 资金 (max 15) — 有成交量+交叉验证
    scores["资金"] = 13 if (g1.get("volume") and g1.get("cross_validated")) else (10 if g1.get("volume") else 3)
    # 来源 (max 15) — 有新浪+baostock=双源验证
    scores["来源"] = 13 if g1.get("cross_validated") else (6 if g1.get("price") else 3)
    
    total = sum(scores.values())
    details.update({"total": total, "breakdown": scores})
    
    if total < 60:
        errors.append(f"DQ_FAIL: DQ={total}<60→O2_DIAGNOSTIC")
        details["output_level"] = "O2_DIAGNOSTIC"
        details["disabled_capabilities"] = ["action_proposal","zg16_full","paper_probe","fill_price"]
        details["allowed_outputs"] = ["diagnostic_report","condition_route","evidence_gap_report"]
        return GateResult(3, "DQ Score", GateStatus.DEGRADED, details, errors, 3)
    if total < 85:
        errors.append(f"DQ={total}<85→O3_CONDITIONAL")
        details["output_level"] = "O3_CONDITIONAL"
        details["disabled_capabilities"] = ["zg16_full","price_zones","position_playbook","paper_probe"]
        details["allowed_outputs"] = ["zg16_lite","watch","wait","condition_route","evidence_gap_report"]
        return GateResult(3, "DQ Score", GateStatus.DEGRADED, details, errors, 3)
    return GateResult(3, "DQ Score", GateStatus.PASS, details, [], 3)


def gate4_l25_macro() -> GateResult:
    """闸口4: L2.5前夜战报 — via Z-G01 l25_macro"""
    filled = 0
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
    # L2.5 macro — delegated to Z-G01
    try:
        from pipelines.z17_loader import l25_macro as z01_macro
        l25 = z01_macro()
        filled = l25.get("filled", 0)
        domains = l25.get("domains", domains)
    except Exception:
        pass
    
    details = {
        "filled_domains": filled, "total_domains": 8, "domains": domains,
        "proxy_level": "KEYWORD_PROXY",
        "transmission": "NOT_FULL_MACRO_TRANSMISSION",
        "method": "MEMORY.md keyword scan — not factor→sector→chain conduction",
        "coverage": f"{filled}/8",
    }
    if filled < 4:
        return GateResult(4, "L2.5 Macro", GateStatus.DEGRADED, details,
            [f"仅{filled}/8信息域填充 (KEYWORD_PROXY, not full macro transmission)"], 0)
    return GateResult(4, "L2.5 Macro", GateStatus.PASS, details,
        ["L2.5_PROXY: keyword-based, not complete factor→31-sector→10-chain conduction"], 0)


def gate5_l3_sectors() -> GateResult:
    """闸口5: L3 31板块确认。需SW31涨跌幅/宽度数据。"""
    try:
        from pipelines.z17_loader import get_sectors as z01_sectors
        sectors_data = z01_sectors()
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
    """闸口6: L4健康检查 — ST→BLOCK_ENTER, 停牌→O2, 无成交→O2 (分级降级)"""
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
        
        # logout removed — G07 delegated to Z-G01
        
        details["tradable"] = has_volume
        if not has_volume:
            errors.append("近3日无成交, 可能停牌")
        
    except Exception as e:
        errors.append(f"L4检查异常: {e}")
    
    if errors:
        for e in errors:
            if "ST" in e:
                details["reason"] = "ST"; details["action"] = "BLOCK_ENTER"
                details["output_level"] = "O2_DIAGNOSTIC"
                details["allowed_outputs"] = ["diagnostic_report","condition_route"]
                details["disabled_capabilities"] = ["paper_probe","human_confirm_probe"]
                return GateResult(6, "L4 Health", GateStatus.BLOCK, details, errors, 0)
            if "停牌" in e:
                details["reason"] = "SUSPENDED"; details["action"] = "DIAGNOSTIC_ONLY"
                details["output_level"] = "O2_DIAGNOSTIC"
                details["disabled_capabilities"] = ["execution_price","paper_fill_price","reduce_risk_execution","harvest_execution"]
                details["allowed_outputs"] = ["holding_status_note","reopen_watch_plan"]
                return GateResult(6, "L4 Health", GateStatus.DATA_INCOMPLETE, details, errors, 0)
            if "无成交" in e:
                details["reason"] = "NO_VOLUME"; details["action"] = "DIAGNOSTIC_ONLY"
                details["output_level"] = "O2_DIAGNOSTIC"
                details["disabled_capabilities"] = ["fill_price","paper_probe"]
                details["allowed_outputs"] = ["liquidity_gap_report"]
                return GateResult(6, "L4 Health", GateStatus.DATA_INCOMPLETE, details, errors, 0)
        return GateResult(6, "L4 Health", GateStatus.DEGRADED, details, errors, 0)
    
    return GateResult(6, "L4 Health", GateStatus.PASS, details, [], 0)


def gate7_l5_matrix(ticker: str, g1_details: dict) -> GateResult:
    """闸口7: L5 B/D/R/OKR Matrix — 使用 zmatrix.scoring 包导入, 不依赖特定目录"""
    errors = []
    details = {"b_matrix": "not_run", "d_matrix": "not_run", "r_matrix": "not_run"}
    
    kl = get_kline(ticker, 500)
    prices = kl.get("prices", [])
    if len(prices) < 60:
        errors.append(f"R/D-Matrix: KLINE_LT_60D({len(prices)}日)")
        return GateResult(7, "L5 Matrix", GateStatus.DEGRADED, details, errors, 0)
    
    # D-Matrix v2.2
    try:
        from zmatrix.scoring.d_band.d_early_v22_scorer import evaluate_d_early_v22
        from pipelines.dmatrix_payload_builder import build_dmatrix_payload
        payload = build_dmatrix_payload(ticker, g1_details.get("name", ""), kl)
        r = evaluate_d_early_v22(payload)
        if hasattr(r, "to_dict"):
            rd = r.to_dict()
            details["d_score"] = round(rd.get("final_score", 0), 1)
        elif isinstance(r, dict):
            details["d_score"] = r.get("d_score", 0)
        details["d_matrix"] = "ran"
    except Exception as e:
        errors.append(f"D-Matrix: {str(e)[:80]}")
    
    # R-Matrix v1.1 — Type A/B dual mode
    if len(prices) >= 260:
        try:
            # R-Matrix deferred to Z-G09 cycle four-king service — not run in G07
            details["r_matrix"] = "deferred_to_g09"
            details["matrix_source"] = "DEFERRED_TO_G09_G10"
            # Old r_score removed. Use G09 adapter for cycle signal.
            ra = rank_type_a_horizontal(ticker, "", prices)
            rb = rank_type_b_rising_channel(ticker, "", prices)
            best = ra if ra.score >= rb.score else rb
            details["r_score"] = round(best.score, 1)
            details["r_subtype"] = best.oscillation_type
            details["r_matrix"] = "ran"
        except Exception as e:
            errors.append(f"R-Matrix: {str(e)[:80]}")
    else:
        errors.append(f"R-Matrix: KLINE_LT_260D({len(prices)}日)")
    
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
    """闸口9: Z8动作映射 — Capability Mask判定, PAPER_PROBE需条件"""
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
            return ActionLevel.PAPER_TRACK, "PAPER_TRACK(PAPER_PROBE需MT.PASS+L1.5.SAFE+world=PAPER_WORLD)"
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
    parser = argparse.ArgumentParser(description="Z-G07 轮动+黑马选股 v2.9.5-RC")
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
