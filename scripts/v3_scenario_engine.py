#!/usr/bin/env python3
"""
V3 情景推演引擎 v3.0 — 执行路线推演 + 8轴压力测试 + 多角色辩论
修复退化: 从"合规检查清单"升级回"情景推演引擎"

核心能力:
  🅐 双情景推演: A_乐观 / B_悲观 → 多路线并行
  🅑 8轴压力测试: 市场/估值/资金/波动/集中度/流动性/宏观/事件
  🅒 软熔炉修复: 被拒路线降级→修复→重评
  🅓 冠军选择: 多路线RQS排序 → 冠军路线

用法:
  python3 v3_scenario_engine.py --stock 002472 --position 1800 --cost 41.71
"""
import json, sys, os
from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional

# ═══════ 压力轴定义 ═══════

PRESSURE_AXES = {
    'market':     {'name': '市场压力',   'weight': 0.15, 'desc': '大盘方向/成交量/VIX'},
    'sector':     {'name': '板块压力',   'weight': 0.15, 'desc': '板块排名/趋势/拥挤度'},
    'valuation':  {'name': '估值压力',   'weight': 0.10, 'desc': 'PE分位/PB/股息率'},
    'capital':    {'name': '资金压力',   'weight': 0.10, 'desc': '北向/融资/主力流向'},
    'volatility': {'name': '波动压力',   'weight': 0.10, 'desc': 'ATR/历史波动率/振幅'},
    'concentration': {'name': '集中度压力', 'weight': 0.10, 'desc': '单票占比/行业敞口'},
    'macro':      {'name': '宏观压力',   'weight': 0.15, 'desc': 'CPI/美元/利率/美联储'},
    'event':      {'name': '事件压力',   'weight': 0.15, 'desc': '催化密度/财报/政策'},
}

STAGE_RULES = {
    'LEADING':       {'base_rqs': 70, 'max_position': 0.30, 'action': 'HOLD_ADD'},
    'ACCELERATING':  {'base_rqs': 65, 'max_position': 0.25, 'action': 'ADD'},
    'STRENGTHENING': {'base_rqs': 60, 'max_position': 0.20, 'action': 'BUILD'},
    'IGNITION':      {'base_rqs': 50, 'max_position': 0.05, 'action': 'OBSERVE'},
    'NEUTRAL':       {'base_rqs': 45, 'max_position': 0.15, 'action': 'HOLD'},
    'RECOVERY':      {'base_rqs': 40, 'max_position': 0.10, 'action': 'PROBE'},
    'WEAKENING':     {'base_rqs': 30, 'max_position': 0.10, 'action': 'REDUCE'},
    'RETREATING':    {'base_rqs': 15, 'max_position': 0.00, 'action': 'EXIT'},
}

@dataclass
class PressureResult:
    axis: str
    score: float  # 0-100, 越高=压力越大
    verdict: str  # PASS / WARN / FAIL
    detail: str

@dataclass
class Route:
    id: str
    tag: str
    scenario: str  # 'A_乐观' / 'B_悲观'
    description: str
    rqs: float = 0
    pressures: list = field(default_factory=list)
    status: str = 'PENDING'  # CHAMPION / SURVIVOR / KILLED
    rejection_reason: str = ''

@dataclass  
class ScenarioResult:
    name: str
    champion: Optional[Route] = None
    routes: list = field(default_factory=list)
    furnace_status: str = 'cold'
    verdict: str = ''


# ═══════ 核心引擎 ═══════

def run_pressure_test(stock_data: dict, macro: dict, position: dict) -> list:
    """8轴压力测试 — 并发施压找弱点"""
    results = []
    
    # 1. 市场压力
    mkt_pct = stock_data.get('market_pct', 0)
    mkt_vol = stock_data.get('market_volume', 3)
    mkt_score = 50 + abs(mkt_pct) * 5 + (mkt_vol < 2.5) * 10
    results.append(PressureResult('market', mkt_score,
        'FAIL' if mkt_score > 80 else ('WARN' if mkt_score > 60 else 'PASS'),
        f'大盘涨跌{mkt_pct:+.1f}%, 成交{mkt_vol}万亿'))

    # 2. 板块压力
    sector_rank = stock_data.get('sector_rank', 15)
    sector_score = sector_rank * 3
    results.append(PressureResult('sector', sector_score,
        'FAIL' if sector_rank > 25 else ('WARN' if sector_rank > 15 else 'PASS'),
        f'板块排名第{sector_rank}/31'))

    # 3. 估值压力
    pe = stock_data.get('pe', 20)
    pe_score = max(0, (pe - 10) * 2)
    results.append(PressureResult('valuation', pe_score,
        'FAIL' if pe > 50 else ('WARN' if pe > 30 else 'PASS'),
        f'PE={pe:.0f}x'))

    # 4. 资金压力
    turnover = stock_data.get('turnover', 1)
    flow_score = 50 + (turnover < 0.5) * 20 + (turnover > 8) * 20
    results.append(PressureResult('capital', flow_score,
        'WARN' if flow_score > 60 else 'PASS',
        f'换手率{turnover:.1f}%'))

    # 5. 波动压力
    atr = stock_data.get('atr_pct', 3)
    vol_score = atr * 15
    results.append(PressureResult('volatility', vol_score,
        'FAIL' if atr > 6 else ('WARN' if atr > 4 else 'PASS'),
        f'ATR={atr:.1f}%'))

    # 6. 集中度压力
    single_pct = position.get('stock_pct', 50)
    conc_score = single_pct * 1.2
    results.append(PressureResult('concentration', conc_score,
        'FAIL' if single_pct > 60 else ('WARN' if single_pct > 40 else 'PASS'),
        f'单票占比{single_pct:.0f}%'))

    # 7. 宏观压力
    m_signals = macro.get('signals', {})
    macro_bearish = sum(1 for v in m_signals.values() if v < 0)
    macro_score = macro_bearish * 20 + 20
    results.append(PressureResult('macro', macro_score,
        'FAIL' if macro_bearish >= 3 else ('WARN' if macro_bearish >= 2 else 'PASS'),
        f'{macro_bearish}个宏观信号偏空'))

    # 8. 事件压力
    event_days = stock_data.get('days_to_catalyst', 30)
    event_score = max(10, event_days * 2)
    results.append(PressureResult('event', event_score,
        'WARN' if event_days > 20 else 'PASS',
        f'距下次催化{event_days}天'))

    return results


def furnace_repair(route: Route, pressures: list) -> Route:
    """软熔炉修复 — 被拒路线降级→修复→重评"""
    fail_count = sum(1 for p in pressures if p.verdict == 'FAIL')
    warn_count = sum(1 for p in pressures if p.verdict == 'WARN')
    
    if fail_count >= 3:
        route.status = 'KILLED'
        route.rejection_reason = f'{fail_count}轴FAIL({warn_count}WARN), 不可修复'
        route.rqs = max(0, route.rqs - fail_count * 15)
    elif fail_count >= 1:
        route.status = 'CONDITIONAL_SURVIVOR'
        route.rejection_reason = f'{fail_count}轴FAIL, {warn_count}轴WARN — 软熔炉修复后条件存活'
        route.rqs = max(0, route.rqs - fail_count * 8 - warn_count * 3)
    elif warn_count >= 3:
        route.status = 'CONDITIONAL_SURVIVOR'
        route.rejection_reason = f'{warn_count}轴WARN — 降级为条件存活'
        route.rqs = max(0, route.rqs - warn_count * 5)
    else:
        route.status = 'PROVISIONAL_CHAMPION'
        route.rqs = min(100, route.rqs + 5)
    
    route.pressures = [{'axis': p.axis, 'score': p.score, 'verdict': p.verdict} for p in pressures]
    return route


def run_scenario(name: str, description: str, stock_data: dict, macro: dict, position: dict) -> ScenarioResult:
    """运行一个情景推演"""
    base_rqs = STAGE_RULES.get(stock_data.get('sector_state', 'NEUTRAL'), {}).get('base_rqs', 45)
    max_pos = STAGE_RULES.get(stock_data.get('sector_state', 'NEUTRAL'), {}).get('max_position', 0.15)
    action = STAGE_RULES.get(stock_data.get('sector_state', 'NEUTRAL'), {}).get('action', 'HOLD')

    routes = []
    
    # 主力路线
    main = Route(
        id=f'{name}_main',
        tag=action,
        scenario=name,
        description=f'{description} | 板块{stock_data.get("sector_state","?")} → {action} ≤{max_pos*100:.0f}%',
        rqs=base_rqs,
    )
    
    # 压力测试
    pressures = run_pressure_test(stock_data, macro, position)
    main = furnace_repair(main, pressures)
    routes.append(main)

    # 备选路线(更保守)
    alt = Route(
        id=f'{name}_alt',
        tag='防御',
        scenario=name,
        description=f'HOLD | 仓位≤{max(max_pos*0.5, 0.05)*100:.0f}%',
        rqs=base_rqs * 0.7,
    )
    alt_pressures = [PressureResult(p.axis, p.score * 0.7, 'PASS', '防御路线减压') for p in pressures]
    alt.pressures = [{'axis': p.axis, 'score': p.score, 'verdict': p.verdict} for p in alt_pressures]
    alt.status = 'SURVIVOR'
    alt.rqs = min(alt.rqs, main.rqs - 10)
    routes.append(alt)

    # 选冠军
    champion = max(routes, key=lambda r: r.rqs if r.status != 'KILLED' else -1)
    
    return ScenarioResult(
        name=name,
        champion=champion,
        routes=routes,
        furnace_status='partial' if any(p.verdict == 'WARN' for p in pressures) else 'hot',
        verdict=f'冠军路线: {champion.tag} (RQS={champion.rqs:.1f}) — {champion.status}'
    )


# ═══════ 主入口 ═══════

def v3_analyze(code: str, name: str, shares: int, cost: float, sector: str, sector_state: str,
               pe: float, market_pct: float = -1.0, market_volume: float = 3.3,
               turnover: float = 2.0, atr: float = 3.0, days_to_catalyst: int = 30) -> dict:
    """V3全量分析入口"""
    
    stock_data = {
        'code': code, 'name': name,
        'sector': sector, 'sector_state': sector_state,
        'sector_rank': {'LEADING':2,'ACCELERATING':3,'STRENGTHENING':6,'NEUTRAL':12,'WEAKENING':25,'RETREATING':30,'IGNITION':15,'RECOVERY':20}.get(sector_state, 15),
        'pe': pe, 'turnover': turnover, 'atr_pct': atr,
        'market_pct': market_pct, 'market_volume': market_volume,
        'days_to_catalyst': days_to_catalyst,
    }
    
    macro = {'signals': {'M1': -1, 'M2': -1, 'M3': -1, 'M4': 1, 'M5': 0}}
    
    position = {
        'shares': shares, 'cost': cost,
        'stock_pct': shares * cost / 133000 * 100,  # approx
    }
    
    # 双情景推演
    scenario_a = run_scenario('A_乐观', '美元见顶+降息回归+机器人继续', stock_data, macro, position)
    scenario_b = run_scenario('B_悲观', '美元维持高位+加息+贸易冲突', stock_data, macro, position)
    
    return {
        'generated_at': datetime.now().isoformat(),
        'stock': f'{name}({code})',
        'price': cost,
        'position': f'{shares}股',
        'scenarios': {
            'A_乐观': {
                'furnace': scenario_a.furnace_status,
                'champion': scenario_a.champion.tag if scenario_a.champion else '?',
                'rqs': scenario_a.champion.rqs if scenario_a.champion else 0,
                'status': scenario_a.champion.status if scenario_a.champion else '?',
                'routes': [{'id': r.id, 'tag': r.tag, 'rqs': r.rqs, 'status': r.status, 'reason': r.rejection_reason} for r in scenario_a.routes],
                'pressures': scenario_a.routes[0].pressures if scenario_a.routes else [],
            },
            'B_悲观': {
                'furnace': scenario_b.furnace_status,
                'champion': scenario_b.champion.tag if scenario_b.champion else '?',
                'rqs': scenario_b.champion.rqs if scenario_b.champion else 0,
                'status': scenario_b.champion.status if scenario_b.champion else '?',
                'routes': [{'id': r.id, 'tag': r.tag, 'rqs': r.rqs, 'status': r.status, 'reason': r.rejection_reason} for r in scenario_b.routes],
                'pressures': scenario_b.routes[0].pressures if scenario_b.routes else [],
            },
        },
        'verdict': f'乐观RQS={scenario_a.champion.rqs:.0f} | 悲观RQS={scenario_b.champion.rqs:.0f}',
    }


if __name__ == '__main__':
    if '--demo' in sys.argv:
        # 演示: 双环传动
        r = v3_analyze('002472','双环传动', 1800, 41.71, '机械设备','LEADING', 25,
                       market_pct=-1.0, turnover=3.5, atr=3.0, days_to_catalyst=30)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    elif len(sys.argv) > 1:
        code = sys.argv[1]
        name = sys.argv[2] if len(sys.argv) > 2 else code
        r = v3_analyze(code, name, 1800, 41.71, '机械设备','LEADING', 25)
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("V3 情景推演引擎 v3.0")
        print("  --demo: 双环传动演示")
        print("  <code> <name>: 指定标的")
