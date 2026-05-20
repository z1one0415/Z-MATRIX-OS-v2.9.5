#!/usr/bin/env python3
"""
波动周期对冲映射器 — 找与持仓波动相反的对冲标的
用途: 轮换操盘时无缝切换，消除资金空窗期
"""

HEDGE_MAP = {
    # 高波动进攻型 → 低波动防御型对冲对
    '002472': {  # 双环传动 — 机器人/高波动
        'name': '双环传动',
        'volatility': '高(ATR~5%)',
        'cycle': '机器人周期',
        'hedges': [
            {'code': '600900', 'name': '长江电力', 'reason': '独立来水周期, ATR<1%, 零相关',
             'switch_rule': '双环高位→长江电力(收息), 双环回调→买回双环'},
            {'code': '510880', 'name': '红利ETF',  'reason': '高股息, 银行+煤炭, 防御属性',
             'switch_rule': '机器人退潮→红利ETF(股息5%), 机器人回暖→切回双环'},
        ]
    },
    '601899': {  # 紫金矿业 — 铜金/中高波动
        'name': '紫金矿业',
        'volatility': '中高(ATR~3%)',
        'cycle': '铜金资源周期',
        'hedges': [
            {'code': '510880', 'name': '红利ETF',  'reason': '高股息防御, 美元强时红利优于铜金',
             'switch_rule': '美元走强→红利ETF, 美元走弱→切回紫金'},
            {'code': '600900', 'name': '长江电力', 'reason': '零相关, 独立水电周期',
             'switch_rule': '铜价见顶→长江电力, 铜价触底→切回紫金'},
        ]
    },
    '159603': {  # 科创50ETF — 科技/中波动
        'name': '科创50ETF',
        'volatility': '中(ATR~2%)',
        'cycle': 'AI半导体周期',
        'hedges': [
            {'code': '510880', 'name': '红利ETF',  'reason': '科技涨时红利横盘, 科技跌时红利抗跌',
             'switch_rule': '科技过热(Exhaustion>8)→红利ETF, 科技回调到位→切回'},
            {'code': '518880', 'name': '黄金ETF',   'reason': '科技与黄金负相关(risk-on/off切换)',
             'switch_rule': '科技见顶→黄金避险, 风险偏好回归→切回科技'},
        ]
    },
    # 防御型 → 进攻型反向映射
    '600900': {
        'name': '长江电力',
        'volatility': '极低(ATR<1%)',
        'cycle': '独立来水周期',
        'hedges': [
            {'code': '002472', 'name': '双环传动', 'reason': '高弹性, 机器人周期',
             'switch_rule': '长江横盘→双环有催化时切换'},
        ]
    },
    '510880': {
        'name': '红利ETF',
        'volatility': '极低(ATR<0.5%)',
        'cycle': '股息/防御周期',
        'hedges': [
            {'code': '002472', 'name': '双环传动', 'reason': '高弹性进攻',
             'switch_rule': '市场risk-on→双环, risk-off→红利'},
            {'code': '601899', 'name': '紫金矿业', 'reason': '铜金进攻',
             'switch_rule': '美元走弱→紫金, 美元走强→红利'},
        ]
    },
}


def find_hedge(code: str) -> dict:
    """为持仓找最优对冲标的"""
    stock = HEDGE_MAP.get(code, {})
    if not stock:
        return {'error': f'{code} 不在映射表, 请手动添加'}
    return {
        'stock': f'{stock["name"]}({code})',
        'profile': f'{stock["volatility"]} | {stock["cycle"]}',
        'hedges': stock['hedges'],
    }


def portfolio_hedge_check(holdings: list) -> dict:
    """全组合对冲检查 — 所有持仓是否都有对冲对"""
    results = {}
    for code in holdings:
        info = find_hedge(code)
        if 'error' not in info:
            hedge_codes = [h['code'] for h in info['hedges']]
            owned_hedge = [h for h in hedge_codes if h in holdings]
            results[code] = {
                'has_hedge_in_portfolio': len(owned_hedge) > 0,
                'owned_hedges': owned_hedge,
                'best_hedge': info['hedges'][0] if info['hedges'] else None,
            }
    return results


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        code = sys.argv[1]
        info = find_hedge(code)
        if 'error' in info:
            print(info['error'])
        else:
            print(f"{info['stock']} | {info['profile']}")
            for h in info['hedges']:
                print(f"  ⇄ {h['name']}({h['code']}) — {h['reason']}")
                print(f"    切换: {h['switch_rule']}")
    else:
        # 全组合检查
        holdings = ['002472','601899','159603']
        result = portfolio_hedge_check(holdings)
        print("═══ 组合对冲检查 ═══")
        for code, r in result.items():
            symbol = '✅' if r['has_hedge_in_portfolio'] else '❌'
            print(f"{symbol} {code}: 组合内对冲={r['has_hedge_in_portfolio']}")
            if not r['has_hedge_in_portfolio'] and r['best_hedge']:
                print(f"   → 建议加入: {r['best_hedge']['name']}({r['best_hedge']['code']})")
