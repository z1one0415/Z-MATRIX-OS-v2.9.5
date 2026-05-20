#!/usr/bin/env python3
"""
Hermes 日记忆卡生成器 v1.0
输入: 日期 → 聚合当天的前夜战报+叙事雷达+25因子评分+持仓快照+决策
输出: 一张完整的日记忆卡 JSON

用法: python3 daily_card.py 2026-05-14
      python3 daily_card.py --today
"""
import json, os, sys, subprocess
from datetime import datetime


MEMORY_PATH = os.path.expanduser('~/.openclaw/agents/z2-analyst/workspace/hermes/daily_cards.json')
MELT_PATH = os.path.expanduser('~/Documents/openclaw memory/openclaw memory/Z2信息熔炉')


def find_file(pattern_root, date_str, subdirs):
    """在熔炉目录中搜索匹配日期的文件"""
    for subdir in subdirs:
        d = os.path.join(MELT_PATH, subdir)
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if date_str in f and f.endswith('.md'):
                return os.path.join(d, f)
    return None


def extract_forecast(date_str):
    """从前夜战报提取关键数据"""
    fp = find_file(date_str, date_str, ['前夜战报'])
    if not fp:
        return None
    with open(fp) as f:
        text = f.read()
    # 提取第一段关键数据(简单规则)
    lines = text.split('\n')
    forecast = {'source': fp, 'summary': ''}
    for line in lines[:30]:
        forecast['summary'] += line.strip() + ' '
        if len(forecast['summary']) > 500:
            break
    return forecast


def extract_narrative(date_str):
    """从叙事雷达提取关键数据"""
    fp = find_file(date_str, date_str, ['叙事雷达'])
    if not fp:
        return None
    with open(fp) as f:
        text = f.read()
    narrative = {'source': fp, 'slogan': '', 'exhaustion': '', 'diversity': '', 'themes': []}
    for line in text.split('\n'):
        if 'Slogan' in line and '|' not in line:
            narrative['slogan'] = line.strip()
        if 'Exhaustion' in line and '→' not in line:
            narrative['exhaustion'] = line.strip()
        if 'Diversity' in line and '→' not in line:
            narrative['diversity'] = line.strip()
    return narrative


def run_prediction(date_str):
    """运行超级预测引擎获取25因子评分"""
    eng = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'predict_engine.py')
    if not os.path.exists(eng):
        return None
    try:
        result = subprocess.run(['python3', eng], capture_output=True, text=True, timeout=10)
        return result.stdout
    except:
        return None


def get_positions_snapshot(date_str):
    """持仓快照(从交易者校准获取)"""
    cal = os.path.join(os.path.dirname(__file__), '..', '..', 'scripts', 'trader_calibration.py')
    if not os.path.exists(cal):
        return None
    try:
        result = subprocess.run(['python3', cal], capture_output=True, text=True, timeout=10)
        # 提取持仓部分
        lines = result.stdout.split('\n')
        positions = []
        capture = False
        for line in lines:
            if '当前持仓' in line:
                capture = True
                continue
            if capture and line.strip():
                positions.append(line.strip())
            elif capture and not line.strip():
                break
        return positions
    except:
        return None


def create_daily_card(date_str, decisions=None):
    """创建一张日记忆卡"""
    card = {
        'date': date_str,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'sections': {},
        'decisions': decisions or [],
    }

    # 前夜战报
    f = extract_forecast(date_str)
    if f:
        card['sections']['forecast'] = f

    # 叙事雷达
    n = extract_narrative(date_str)
    if n:
        card['sections']['narrative'] = n

    # 超级预测
    p = run_prediction(date_str)
    if p:
        card['sections']['prediction_scores'] = p.strip()

    # 持仓
    pos = get_positions_snapshot(date_str)
    if pos:
        card['sections']['positions'] = pos

    # 关键事件 (从记忆银行提取当天的决策)
    bank_path = os.path.join(os.path.dirname(__file__), 'memory_bank.json')
    if os.path.exists(bank_path):
        with open(bank_path) as f:
            bank = json.load(f)
        # memory_bank.json 是 list 格式 (v2.9.3)
        if isinstance(bank, list):
            day_cards = [c for c in bank if date_str in c.get('timestamp', '')]
        else:
            day_cards = [c for c in bank.get('cards', []) if date_str in c.get('timestamp', '')]
        if day_cards:
            card['sections']['decision_cards_today'] = [{
                'id': c.get('id', ''),
                'stock': c.get('stock', ''),
                'tags': c.get('tags', []),
                'cost': c.get('cost', 0),
                'lesson': c.get('lesson', '')[:100],
            } for c in day_cards]

    # 持久化
    bank_path_all = os.path.join(os.path.dirname(__file__), 'daily_cards.json')
    daily_cards = []
    if os.path.exists(bank_path_all):
        with open(bank_path_all) as f:
            daily_cards = json.load(f)

    # 覆盖同一天
    daily_cards = [c for c in daily_cards if c['date'] != date_str]
    daily_cards.append(card)
    daily_cards.sort(key=lambda x: x['date'])

    with open(bank_path_all, 'w') as f:
        json.dump(daily_cards, f, ensure_ascii=False, indent=2)

    return card


if __name__ == '__main__':
    if '--today' in sys.argv:
        date_str = datetime.now().strftime('%Y-%m-%d')
    elif len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')

    card = create_daily_card(date_str)
    sections_found = sum(1 for v in card['sections'].values() if v)
    print(f'Hermes日记忆卡 {date_str}: {sections_found}个数据源已聚合')
    for k, v in card['sections'].items():
        if v:
            if isinstance(v, list):
                print(f'  ✅ {k}: {len(v)}条')
            elif isinstance(v, dict):
                print(f'  ✅ {k}: {v.get("source", "已提取")}')
            else:
                print(f'  ✅ {k}: {len(str(v))}字符')
