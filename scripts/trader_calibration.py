#!/usr/bin/env python3
"""
Z2 交易者校准引擎 v1.0
功能: 记录每笔操作 → 事后复盘 → 分析个人偏差模式
输入: 交易记录 + 事后N天价格
输出: 偏差诊断 (乐观偏误/保守偏误/时机偏误)
"""
import json, os, sys
from datetime import datetime

CALIBRATION_FILE = os.path.expanduser('~/.openclaw/agents/z2-analyst/workspace/cache/trader_calibration.json')

# ═══════ 已记录的交易(从用户截图提取) ═══════
TRADES = [
    # (日期, 代码, 名称, 方向, 价格, 股数, 原因)
    ('2026-04-28', '000977', '浪潮信息', 'buy',  72.99, 100, 'AI算力底部试探'),
    ('2026-04-28', '000977', '浪潮信息', 'buy',  72.45, 100, 'AI算力底部试探'),
    ('2026-05-06', '000977', '浪潮信息', 'sell', 72.80, 100, '见涨就卖'),
    ('2026-05-06', '000977', '浪潮信息', 'sell', 74.50, 100, '见涨就卖'),
    ('2026-05-07', '601899', '紫金矿业', 'buy',  34.80, 300, '铜价强，左侧建仓'),
    ('2026-05-07', '601899', '紫金矿业', 'buy',  34.30, 200, '铜价强，左侧建仓'),
    ('2026-05-11', '601899', '紫金矿业', 'buy',  34.18, 300, '加仓拉低成本'),
    ('2026-05-11', '002472', '双环传动', 'buy',  42.08, 300, '机器人展前建仓'),
    ('2026-05-12', '002472', '双环传动', 'buy',  42.11, 200, '机器人展前建仓'),
    ('2026-05-12', '002472', '双环传动', 'buy',  42.09, 100, '机器人展前建仓'),
    ('2026-05-12', '002472', '双环传动', 'buy',  42.18, 100, '机器人展前建仓'),
    ('2026-05-13', '002472', '双环传动', 'buy',  41.45, 300, '回调低位加仓'),
    ('2026-05-14', '002472', '双环传动', 'sell', 42.15, 500, 'D1洗盘高抛'),
    ('2026-05-14', '002472', '双环传动', 'buy',  41.77, 300, 'D1洗盘低吸'),
    ('2026-05-14', '002472', '双环传动', 'buy',  41.76, 200, 'D1洗盘低吸'),
    ('2026-05-14', '002472', '双环传动', 'buy',  41.70, 200, 'D1洗盘低吸'),
    ('2026-05-14', '002472', '双环传动', 'buy',  41.59, 200, 'D1洗盘低吸'),
    ('2026-05-14', '002472', '双环传动', 'buy',  41.50, 200, 'D1洗盘低吸'),
    ('2026-05-14', '002472', '双环传动', 'buy',  41.41, 200, 'D1洗盘低吸'),
    ('2026-05-14', '518880', '黄金ETF',  'sell', 9.79,  1000,'认赔换仓'),
    ('2026-05-14', '159603', '科创50ETF','buy', 1.885, 6500,'PE分位3.73%建仓'),
]

# 事后验证价格(5/15收盘快照)
VERIFICATION = {
    '000977': 78.15,   # 浪潮信息 — 如果持有到现在
    '601899': 32.35,    # 紫金矿业 — 当前浮亏
    '002472': 43.43,    # 双环传动 — 当前浮盈
    '518880': 9.78,     # 黄金ETF — 卖后涨了没
    '159603': 1.85,     # 科创50 — 建仓后
}


def analyze_trades():
    """分析所有已记录交易，输出偏差诊断"""
    positions = {}  # code → {total_shares, total_cost}
    records = []

    for date, code, name, direction, price, shares, reason in TRADES:
        if code not in positions:
            positions[code] = {'shares': 0, 'cost': 0, 'name': name,
                               'buys': [], 'sells': [], 'reasons': []}

        pos = positions[code]
        if direction == 'buy':
            pos['shares'] += shares
            pos['cost'] += price * shares
            pos['buys'].append((date, price, shares))
            pos['reasons'].append(('buy', reason))
        else:
            pos['shares'] -= shares
            # 按比例减成本
            if pos['shares'] > 0:
                avg = pos['cost'] / max(pos['shares'] + shares, 1)
                pos['cost'] -= avg * shares
            pos['sells'].append((date, price, shares))
            pos['reasons'].append(('sell', reason))

    # ═══ 偏差诊断 ═══
    findings = []

    # 1. 浪潮信息: 卖出时机分析
    langchao = positions.get('000977', {})
    langchao_buys = langchao.get('buys', [])
    langchao_sells = langchao.get('sells', [])
    if langchao_buys and langchao_sells:
        avg_buy = sum(p for _, p, _ in langchao_buys) / len(langchao_buys)
        avg_sell = sum(p for _, p, _ in langchao_sells) / len(langchao_sells)
        current = VERIFICATION.get('000977', avg_sell)
        profit_made = (avg_sell / avg_buy - 1) * 100
        profit_possible = (current / avg_buy - 1) * 100
        missed = profit_possible - profit_made

        findings.append({
            'stock': '浪潮信息',
            'pattern': '卖出过早 (保守偏误)',
            'detail': f'买入均价{avg_buy:.1f}, 卖出均价{avg_sell:.1f}(+{profit_made:.1f}%)',
            'what_if': f'如持有至今: {current}(+{profit_possible:.1f}%), 少赚{missed:.1f}%',
            'diagnosis': '在AI主升浪第一天卖出。行情初期见涨就跑, 属于过度保守。',
            'fix': '设定"至少持有到催化剂兑现"的门槛, 而非"见涨就跑"。',
        })

    # 2. 紫金矿业: 买入时机分析
    zijin = positions.get('601899', {})
    zijin_buys = zijin.get('buys', [])
    if zijin_buys:
        avg_buy = sum(p for _, p, _ in zijin_buys) / len(zijin_buys)
        current = VERIFICATION.get('601899', avg_buy)
        loss = (current / avg_buy - 1) * 100

        findings.append({
            'stock': '紫金矿业',
            'pattern': '买入过早 (乐观偏误)',
            'detail': f'分3批建仓均价{avg_buy:.2f}, 现价{current}({loss:+.1f}%)',
            'context': '建仓期 5/7-11, 三天后CPI/PPI/沃什三雷齐爆',
            'diagnosis': '在宏观逆风(加息预期+强美元)前重仓周期股。对宏观风险不够敏感。',
            'fix': '买入前检查: 未来1周是否有重大宏观事件？有→只试探, 不全押。',
        })

    # 3. 双环传动: 做T操作分析
    shuanghuan = positions.get('002472', {})
    sh_buys = shuanghuan.get('buys', [])
    sh_sells = shuanghuan.get('sells', [])
    if sh_buys:
        # 分两阶段: 5/11-13建仓 vs 5/14做T
        early_buys = [(d, p, s) for d, p, s in sh_buys if d <= '2026-05-13']
        d1_buys = [(d, p, s) for d, p, s in sh_buys if d == '2026-05-14']
        early_avg = sum(p for _, p, _ in early_buys) / len(early_buys) if early_buys else 0
        d1_avg = sum(p for _, p, _ in d1_buys) / len(d1_buys) if d1_buys else 0
        d1_sell_avg = sum(p for _, p, _ in sh_sells) / len(sh_sells) if sh_sells else 0
        current = VERIFICATION.get('002472', 0)

        # 如果不做T(死拿): 成本≈early_avg
        # 做T后: 成本被拉低
        d1_low = 41.03  # 5/14最低点

        findings.append({
            'stock': '双环传动',
            'pattern': '做T操作正确, 但仓位不足',
            'detail': f'早期建仓均价{early_avg:.2f}, D1做T:卖@{d1_sell_avg} + 买@{d1_avg:.2f}',
            'what_if': f'D1最低{d1_low}, 如在41.0满仓抄底→成本可降至~41.1, 当前+{current/d1_low*100-100:.1f}%',
            'diagnosis': '判断正确(D1洗盘→D2拉升), 但执行偏保守, 只加了部分仓位。'
                        '确认模式后应加大仓位。',
            'fix': '建立"信号确认→加仓"的联动规则: D2开盘低开+前日确认洗盘→加仓至目标仓位。',
        })

    # 4. 全局偏差汇总
    conservative_count = sum(1 for f in findings if '保守' in f['pattern'])
    optimistic_count = sum(1 for f in findings if '乐观' in f['pattern'])

    return {
        'findings': findings,
        'summary': {
            'total_trades': len(TRADES),
            'stocks_traded': len(set(t[1] for t in TRADES)),
            'conservative_bias': conservative_count,
            'optimistic_bias': optimistic_count,
            'dominant_bias': '过度保守' if conservative_count > optimistic_count else (
                '过度乐观' if optimistic_count > conservative_count else '平衡但有混合偏误'),
        },
        'positions': {code: {
            'name': pos['name'],
            'shares': pos['shares'],
            'avg_cost': round(pos['cost'] / pos['shares'], 2) if pos['shares'] > 0 else 0,
            'current': VERIFICATION.get(code, 0),
            'pnl_pct': round((VERIFICATION.get(code, 0) / (pos['cost'] / pos['shares']) - 1) * 100, 1) if pos['shares'] > 0 and pos['cost'] > 0 else 0,
        } for code, pos in positions.items()},
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }


if __name__ == '__main__':
    report = analyze_trades()

    print(f'═══ Z2 交易者校准报告 {report["timestamp"]} ═══')
    print()
    print(f'已记录{report["summary"]["total_trades"]}笔交易, {report["summary"]["stocks_traded"]}只标的')
    print(f'主导偏差: {report["summary"]["dominant_bias"]}')
    print()

    for f in report['findings']:
        print(f'▸ {f["stock"]}: {f["pattern"]}')
        print(f'  {f["detail"]}')
        if 'what_if' in f:
            print(f'  {f["what_if"]}')
        print(f'  诊断: {f["diagnosis"]}')
        print(f'  修正: {f["fix"]}')
        print()

    print('═══ 当前持仓 ═══')
    for code, pos in report['positions'].items():
        if pos['shares'] > 0:
            color = '🟢' if pos['pnl_pct'] > 0 else '🔴'
            print(f'  {pos["name"]}({code}): {pos["shares"]}股 成本{pos["avg_cost"]} 现{pos["current"]} {color}{pos["pnl_pct"]:+.1f}%')

    # 保存
    with open(CALIBRATION_FILE, 'w') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f'\n已保存到 {CALIBRATION_FILE}')
