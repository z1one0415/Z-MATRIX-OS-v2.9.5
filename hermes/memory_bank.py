"""
Hermes 决策记忆卡系统 v1.0
每张卡片保留完整决策情境, 不脱水。
新决策前自动搜索相似卡片, 主动推送校准。
"""
import json, os, hashlib
from datetime import datetime
from difflib import SequenceMatcher

MEMORY_PATH = os.path.expanduser('~/.openclaw/agents/z2-analyst/workspace/hermes/memory_bank.json')


def load_bank():
    if os.path.exists(MEMORY_PATH):
        with open(MEMORY_PATH) as f:
            return json.load(f)
    return {'cards': [], 'patterns': {}, 'stats': {'total': 0, 'by_stock': {}, 'by_type': {}}}


def save_bank(bank):
    with open(MEMORY_PATH, 'w') as f:
        json.dump(bank, f, ensure_ascii=False, indent=2)


def create_card(stock, situation, your_view, my_advice, actual_action, outcome, cost, lesson, tags, emotion, priority_scene):
    """
    创建一张决策记忆卡 — 不脱水, 保留完整温度。

    stock: 标的代码
    situation: 当时的市场情境(段落, 不是要点)
    your_view: 你的判断和直觉(原话)
    my_advice: 我的建议(原话)
    actual_action: 实际操作
    outcome: 事后结果
    cost: 代价(元)
    lesson: 教训(未来怎么做)
    tags: 标签列表(['过度保守','信号确认','D1洗盘'])
    emotion: 事后情绪('后悔'/'庆幸'/'愤怒'/'平静')
    priority_scene: 对应的决策优先级场景(A/B/C/D/E)
    """
    bank = load_bank()
    card = {
        'id': hashlib.md5(f"{datetime.now().isoformat()}{stock}".encode()).hexdigest()[:8],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'stock': stock,
        'situation': situation,
        'your_view': your_view,
        'my_advice': my_advice,
        'actual_action': actual_action,
        'outcome': outcome,
        'cost': cost,
        'lesson': lesson,
        'tags': tags,
        'emotion': emotion,
        'priority_scene': priority_scene,
    }
    bank['cards'].append(card)
    bank['stats']['total'] += 1
    bank['stats']['by_stock'][stock] = bank['stats']['by_stock'].get(stock, 0) + 1
    for tag in tags:
        bank['stats']['by_type'][tag] = bank['stats']['by_type'].get(tag, 0) + 1

    # 更新模式
    _update_patterns(bank, card)

    save_bank(bank)
    return card['id']


def _update_patterns(bank, card):
    """发现模式 — 同标签出现3次以上自动记录"""
    for tag in card['tags']:
        count = sum(1 for c in bank['cards'] if tag in c['tags'])
        if count >= 3 and tag not in bank.get('patterns', {}):
            bank['patterns'][tag] = {
                'detected_at': datetime.now().strftime('%Y-%m-%d'),
                'occurrences': count,
                'suggestion': _pattern_suggestion(tag, count),
            }


def _pattern_suggestion(tag, count):
    suggestions = {
        '过度保守': '卖出前检查催化剂是否已兑现。未兑现→持有。',
        '过度乐观': '买入前检查未来7天宏观日历。有雷→只1/4试探。',
        '执行不足': '信号确认(概率>70%)→直接加至目标仓位，不等。',
        '买入过早': '场景B(宏观逆风)→不建新仓，等事件落地。',
        '信号确认': '场景A→执行优先于分散。冲锋时不谈防守。',
        'D1洗盘': '多重催化+竞价平开+全板块同步跌=洗盘→D2大概率拉升。',
    }
    return suggestions.get(tag, f'该模式已出现{count}次, 建议总结规律。')


def recall(situation_hint=None, stock=None, tags=None, max_cards=5):
    """
    决策前召回 — 搜索最相关的历史卡片。
    按相似度排序, 返回完整卡片(不脱水)。
    """
    bank = load_bank()
    cards = bank['cards']

    if not cards:
        return {'matches': [], 'advice': '暂无历史决策卡。这是全新的情境。', 'patterns_found': []}

    # 过滤
    candidates = []
    for card in cards:
        score = 0
        if stock and card['stock'] == stock:
            score += 30
        if tags:
            for t in tags:
                if t in card.get('tags', []):
                    score += 20
        if situation_hint:
            # 文本相似度
            full_text = card.get('situation', '') + card.get('your_view', '') + card.get('my_advice', '')
            score += SequenceMatcher(None, situation_hint[:200], full_text[:200]).ratio() * 40
        if score > 0:
            candidates.append((score, card))

    candidates.sort(key=lambda x: x[0], reverse=True)
    top = [c for _, c in candidates[:max_cards]]

    # 组装建议
    if top:
        best = top[0]
        tags_found = best.get('tags', [])
        patterns = []
        for tag in tags_found:
            if tag in bank.get('patterns', {}):
                patterns.append(bank['patterns'][tag]['suggestion'])

        advice_parts = []
        if best['cost'] > 0 and best['emotion'] in ('后悔', '愤怒'):
            advice_parts.append(f"⚠️ 上次类似情境代价{best['cost']}元, 情绪:{best['emotion']}")
        if patterns:
            advice_parts.append(f"📊 已发现模式: {'; '.join(patterns[:2])}")
        if best.get('lesson'):
            advice_parts.append(f"💡 上次教训: {best['lesson']}")

        advice = ' | '.join(advice_parts) if advice_parts else '检测到相似情境, 但无明确模式。建议跑引擎确认。'
    else:
        advice = '无相似情境。这是一次新的决策类型。建议严格按照决策优先级框架执行。'

    return {
        'matches': top,
        'advice': advice,
        'patterns_found': [k for k in bank.get('patterns', {}) if any(k in c.get('tags', []) for c in top)],
        'total_cards': len(cards),
    }


def report(verbose=False):
    """记忆银行健康报告"""
    bank = load_bank()
    cards = bank['cards']
    if not cards:
        return '记忆银行为空。'
    lines = [f'Hermes记忆银行 | {len(cards)}张决策卡 | {len(bank.get("patterns",{}))}个已发现模式']
    lines.append(f'标的分布: {bank["stats"]["by_stock"]}')
    lines.append(f'偏差分布: {bank["stats"]["by_type"]}')
    if bank.get('patterns'):
        lines.append(f'已发现模式:')
        for tag, p in bank['patterns'].items():
            lines.append(f'  {tag}({p["occurrences"]}次): {p["suggestion"][:60]}')
    if verbose:
        for card in cards[-3:]:
            lines.append(f'  [{card["timestamp"]}] {card["stock"]} {card["tags"]} 代价{card["cost"]}元')
    return '\n'.join(lines)


# ═══════ 预填充: 从5/13-15复盘提取决策卡 ═══════

def seed():
    """首次运行: 填入已知的决策卡"""
    bank = load_bank()
    if bank['cards']:
        return  # 已填充

    cards_data = [
        {
            'stock': '002472', 'tags': ['D1洗盘', '信号确认', '执行不足'],
            'situation': '5/14机器人展第一天。四重催化(宇树机甲+Figure量产+展会+马斯克)却竞价平开42.30。开盘后45分钟单边下滑到41.03, 全板块同步下跌。换手从0.89%放大到2.2%。',
            'your_view': '我感觉庄家在砸盘清盘然后化整为零入场。这不是出货, 是洗盘。应该加仓, 把成本进一步压低。',
            'my_advice': '全板块都在跌, 确认不是双环个股问题。但你已经1800股了, 建议把黄金ETF的资金买科创50ETF分散风险, 不要继续追加双环。',
            'actual_action': '卖出500股@42.15, 买入1100股@41.5-41.77(分6批), 净增800股。同时黄金资金买了科创50ETF。',
            'outcome': '次日D2全板块暴涨: 双环+6.6%, 绿的+16.4%, 雷赛涨停。双环浮盈+3094元。但如果在41.0满仓加至2300→多赚约1800元。科创50浮亏227元。总机会成本约2032元。',
            'cost': 2032,
            'lesson': '场景A(信号确认)→执行优先于分散。确认D1洗盘后应立即加至目标仓位, 不等更低, 不谈分散。分散是反弹后的事, 不是冲锋时的事。',
            'emotion': '后悔', 'priority_scene': 'A',
        },
        {
            'stock': '601899', 'tags': ['过度乐观', '买入过早', '宏观逆风'],
            'situation': '5/7-11, 铜价伦铜逼近前高$13210, 紫金PE仅10x, 金铜锂三箭齐发。但未来5-8天有CPI(5/13)、PPI(5/14)、沃什上任(5/15)三大宏观事件。',
            'your_view': '紫金是好公司, 铜价强, PE便宜。可以分批建仓, 越跌越买。',
            'my_advice': '同意分批建仓方向。没有特别强调未来一周的宏观风险。',
            'actual_action': '5/7买500@34.55, 5/11买300@34.18。总800股, 成本34.477。',
            'outcome': 'CPI 3.8%→PPI 6%→沃什鹰派→美元98.5→紫金跌至32.35, 浮亏-1685元(-6.1%)。如果等5/14后再建仓→成本可低至32.5。',
            'cost': 1704,
            'lesson': '场景B(宏观逆风)→不建新仓。未来7天有重大宏观事件时, 只1/4仓位试探, 等事件落地后再建。',
            'emotion': '后悔', 'priority_scene': 'B',
        },
        {
            'stock': '000977', 'tags': ['过度保守', '卖出过早'],
            'situation': '4/28买入浪潮信息200股@72.7, AI算力行业龙头。5/6五一后首个交易日, 科创50暴涨5.47%, 半导体全线涨停, AI进入主升浪。',
            'your_view': '浪潮涨了2%, 可以兑现了。',
            'my_advice': '(未参与该决策, 当时的对话记录中无此讨论)',
            'actual_action': '5/6分两笔卖出200股: 72.80和74.50, 均价73.65, 盈利+1.3%(+186元)。',
            'outcome': '浪潮继续上涨, 5/14收盘78.15(+7.5%)。如果持有→可多赚约900元。',
            'cost': 900,
            'lesson': '区分"趋势初期"和"利好兑现"。浪潮卖在AI主升浪D1, 催化剂(黄仁勋访华/算力需求)远未兑现。卖出前检查: 催化剂兑现了吗？',
            'emotion': '后悔', 'priority_scene': 'A',
        },
        {
            'stock': '518880', 'tags': ['止损执行', '正确操作'],
            'situation': '黄金ETF持仓1000股@11.276, 浮亏-13%。近20日净赎回10.74亿, 机构持续流出。金价$4700横盘, 美元走强。',
            'your_view': '黄金ETF表现太差, 想清仓换到更有成长性的资产。',
            'my_advice': '同意清仓。不是认输, 是止损转仓。9,777元去PE分位3.73%的科创50, 确定性更高。',
            'actual_action': '5/14卖出1000股@9.789, 亏损-1499元。资金全部买入科创50ETF和Y份额。',
            'outcome': '黄金次日继续跌-1.5%至9.64。止损避免了额外150元损失。科创50暂时浮亏-227元但长期逻辑成立。',
            'cost': -150,  # 避免的损失
            'lesson': '止损≠错误操作。催化剂兑现前卖出=过早, 催化剂已兑现后止损=正确。黄金的催化剂(降息/地缘)短期内不会兑现。',
            'emotion': '平静', 'priority_scene': 'E',
        },
    ]

    for cd in cards_data:
        card = {
            'id': hashlib.md5(datetime.now().isoformat().encode()).hexdigest()[:8],
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            **cd,
        }
        bank['cards'].append(card)
        bank['stats']['total'] += 1
        bank['stats']['by_stock'][cd['stock']] = bank['stats']['by_stock'].get(cd['stock'], 0) + 1
        for tag in cd['tags']:
            bank['stats']['by_type'][tag] = bank['stats']['by_type'].get(tag, 0) + 1
        _update_patterns(bank, card)

    save_bank(bank)
    print(f'Hermes记忆银行初始化: {len(bank["cards"])}张卡片, {len(bank.get("patterns",{}))}个模式')


if __name__ == '__main__':
    import sys
    if '--seed' in sys.argv:
        seed()
        print(report())
    elif '--recall' in sys.argv:
        stock = sys.argv[sys.argv.index('--recall') + 1] if len(sys.argv) > sys.argv.index('--recall') + 1 else None
        hint = sys.argv[sys.argv.index('--hint') + 1] if '--hint' in sys.argv else None
        result = recall(situation_hint=hint, stock=stock)
        print(f'🔍 Hermes召回 ({result["total_cards"]}张卡片)')
        print(f'💡 {result["advice"]}')
        if result['matches']:
            print(f'📋 最相关卡片:')
            for m in result['matches']:
                print(f'  [{m["timestamp"]}] {m["stock"]} {m["tags"]} → 代价{m["cost"]}元')
    elif '--report' in sys.argv:
        print(report(verbose='--verbose' in sys.argv))
    else:
        print("Hermes记忆银行 v1.0")
        print("  --seed: 初始化(已预填5/13-15决策卡)")
        print("  --recall <股票>: 决策前召回相似卡片")
        print("  --report: 记忆银行健康报告")
