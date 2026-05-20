#!/usr/bin/env python3
"""☯️ Z-G16A Alpha平行验证仓 — gate_pipeline.py v1.0
定位: 承接Z-G16纸面执行计划或Human/System分歧→PAPER_WORLD前向验证
世界: PAPER_WORLD (不连接真实账户)
职责: 验证计划创建→开仓→盯市→结算→人类画像沉淀
"""

import argparse, json, sys, os
from datetime import datetime, timezone, timedelta
from pathlib import Path

WORKSPACE = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(WORKSPACE))

def run(plan=None):
    now = datetime.now(timezone(timedelta(hours=8)))
    plan = plan or _demo_plan()
    
    result = {
        "pipeline_signature": "Z-G16A_Alpha平行验证_v1.0-draft",
        "timestamp": now.isoformat(),
        "world": "PAPER_WORLD",
        "validation_id": plan.get("validation_id", f"val_{now.strftime('%Y%m%d%H%M')}"),
        "symbol": plan.get("symbol", ""),
        "plan_status": "CREATED",
    }
    
    print(f"\n☯️ Z-G16A Alpha平行验证仓 — PAPER_WORLD")
    print("=" * 60)
    
    # 验证计划完整性
    required = ["validation_hypothesis", "ghost_benchmark", "planned_horizon_days", 
                "invalidation_conditions", "primary_role"]
    missing = [f for f in required if not plan.get(f)]
    if missing:
        print(f"⛔ 验证计划不完整, 缺失: {missing}")
        result["plan_status"] = "REJECTED"
        return result
    
    print(f"\n📋 验证计划: {plan['validation_id']}")
    print(f"  标的: {plan.get('symbol')} {plan.get('name','')}")
    print(f"  角色: {plan.get('primary_role','')}")
    print(f"  假设: {plan.get('validation_hypothesis','')}")
    print(f"  幽灵基准: {plan.get('ghost_benchmark','')}")
    print(f"  计划周期: {plan.get('planned_horizon_days',30)}天")
    print(f"  最大回撤: {plan.get('max_acceptable_drawdown',15)}%")
    print(f"  失效条件: {plan.get('invalidation_conditions',[])}")
    
    if plan.get("human_reason"):
        print(f"  Human分歧: {plan['human_reason']}")
    if plan.get("system_verdict_at_entry"):
        print(f"  System判决: {plan['system_verdict_at_entry']}")
    
    # 开仓模拟
    entry_price = plan.get("entry_price", 100)
    benchmark_price = plan.get("benchmark_price", entry_price)
    slippage = 0.0015
    fill_price = entry_price * (1 + slippage)
    
    print(f"\n📊 PAPER_WORLD开仓:")
    print(f"  入场价: {entry_price:.2f} | 填报价: {fill_price:.2f}")
    print(f"  基准价: {benchmark_price:.2f} | 滑点: {slippage*100:.2f}%")
    print(f"  数量: 1U (纸面验证单位)")
    
    # 成本
    costs = {
        "slippage": round((fill_price - entry_price), 2),
        "commission": round(fill_price * 0.0003, 2),
        "total": round((fill_price - entry_price) + fill_price * 0.0003, 2)
    }
    print(f"  成本: 滑点{costs['slippage']:.2f} + 佣金{costs['commission']:.2f} = {costs['total']:.2f}")
    
    result["position"] = {
        "entry_price": entry_price,
        "fill_price": round(fill_price, 2),
        "benchmark_price": benchmark_price,
        "costs": costs,
        "world": "PAPER_WORLD",
        "status": "OPEN"
    }
    
    # 结算预览
    print(f"\n📝 结算规则:")
    print(f"  验证到期: {plan['planned_horizon_days']}天后自动结算")
    print(f"  主动收益 = 标的收益 - 基准收益")
    print(f"  跑赢基准 → promote / continue")
    print(f"  跑输基准 → retire / ETF review")
    print(f"  ⚠️ PAPER_WORLD only — 不写入真实账户")
    
    result["settlement_preview"] = {
        "horizon_days": plan["planned_horizon_days"],
        "active_return_formula": "stock_return - benchmark_return",
        "promote_threshold": 0.03,
        "retire_threshold": -0.05
    }
    
    return result

def _demo_plan():
    return {
        "validation_id": "val_20260519_001",
        "world": "PAPER_WORLD",
        "symbol": "002463",
        "name": "沪电股份",
        "primary_role": "R_MATRIX",
        "validation_hypothesis": "PCB量价齐升逻辑下, 沪电将跑赢半导体ETF基准",
        "ghost_benchmark": "半导体ETF (512480)",
        "planned_horizon_days": 30,
        "max_acceptable_drawdown": 15,
        "invalidation_conditions": ["跌破MA60且放量", "光模块板块跌幅>15%", "AI资本开支预期下调"],
        "entry_price": 102.6,
        "benchmark_price": 1.85,
        "human_reason": "系统判WATCH, 但财报增速+62%值得纸面验证",
        "system_verdict_at_entry": "WAIT (DQ=87, AMT=102.6, L3=PARTIAL)",
        "source": "Z-G16_PaperExecutionCoach",
        "source_proposal_id": "zg16_plan_20260519_001"
    }

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Z-G16A Alpha平行验证仓")
    p.add_argument("--plan", type=str, default="", help="验证计划JSON文件路径")
    args = p.parse_args()
    plan = None
    if args.plan and os.path.exists(args.plan):
        plan = json.load(open(args.plan))
    run(plan=plan)
