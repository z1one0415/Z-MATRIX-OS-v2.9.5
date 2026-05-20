#!/usr/bin/env python3
"""
Z2 超级预测引擎 v2.1 — 25信号因子×5维加权→概率
新增: 事件日历集成(P2)
用法: python3 predict_engine.py --report --offline
"""
import sys, os, json as _json
from datetime import datetime, timedelta as _timedelta

WEIGHTS = {'M': 0.30, 'I': 0.25, 'F': 0.20, 'T': 0.15, 'R': 0.10}

STOCK_DB = {
    '002472': {'sector': '机械设备', 'growth': True, 'order': True, 'buyback': False, 'stage': 'early', 'pe': 25},
    '601899': {'sector': '有色金属', 'growth': True, 'order': True, 'buyback': True,  'stage': 'decline', 'pe': 10},
    '000977': {'sector': '计算机',   'growth': True, 'order': True, 'buyback': False, 'stage': 'mid', 'pe': 43},
    '601898': {'sector': '煤炭',     'growth': True, 'order': False,'buyback': False, 'stage': 'early', 'pe': 11},
    '600900': {'sector': '公用事业', 'growth': False,'order': False,'buyback': False, 'stage': 'mid', 'pe': 18},
    '002050': {'sector': '机械设备', 'growth': True, 'order': True, 'buyback': False, 'stage': 'early', 'pe': 35},
    '688017': {'sector': '机械设备', 'growth': True, 'order': True, 'buyback': False, 'stage': 'early', 'pe': 80},
}

OFFLINE = {
    '002472': (43.43, 6.63, 40.9, 43.43, 41.28, 3.58),
    '601899': (32.35, -3.49, 32.31, 33.0, 33.56, 1.14),
    '000977': (78.15, 0.0, 70.2, 78.15, 77.38, 9.85),
    '601898': (16.91, 5.03, 15.9, 16.98, 16.14, 0.43),
    '600900': (27.06, 0.45, 26.72, 27.2, 26.94, 0.28),
    '002050': (53.48, 8.19, 49.25, 53.77, 49.28, 5.1),
    '688017': (308.37, 16.37, 262.0, 308.8, 265.5, 7.67),
}

MACRO = {'M1': -1, 'M2': -1, 'M3': -1, 'M4': 1, 'M5': 0}

# ── 事件日历 (P2) ──
_EVENT_PATH = os.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/hermes/event_calendar.json")

def check_macro_events(code=None, days=7):
    """交易前事件检查"""
    if not os.path.exists(_EVENT_PATH):
        return {'scene': 'D', 'warnings': [], 'macro_count': 0}
    with open(_EVENT_PATH) as f:
        events = _json.load(f)
    now = datetime.now()
    end = now + _timedelta(days=days)
    warnings = []; macro_count = 0
    for date_str, evt in events.items():
        try: evt_date = datetime.strptime(date_str, '%Y-%m-%d')
        except: continue
        if evt_date < now or evt_date > end: continue
        if evt.get('type') == 'stock' and code and evt.get('code') != code: continue
        warnings.append({'date': date_str, 'days': (evt_date-now).days, 'event': evt['event'], 'impact': evt['impact'], 'type': evt['type']})
        if evt['type'] in ('macro_US','macro_CN'): macro_count += 1
    scene = 'D'
    if macro_count >= 3 or any(w['impact']=='CRITICAL' for w in warnings): scene = 'B'
    elif any(w['impact'] in ('HIGH','CRITICAL') for w in warnings if w['type']=='industry'): scene = 'A'
    return {'scene': scene, 'warnings': warnings, 'macro_count': macro_count}



def _auto_decision_card(result):
    """P1: 决策后自动创建决策卡"""
    import json as _j, os as _o
    card_path = _o.path.expanduser("~/.openclaw/agents/z2-analyst/workspace/hermes/memory_bank.json")
    if not _o.path.exists(card_path):
        return
    with open(card_path) as f:
        bank = _j.load(f)
    
    # Only create card for significant decisions (prob >70 or <30)
    prob = result.get('prob', 50)
    if 30 < prob < 70:
        return  # Neutral zone, skip
    
    from datetime import datetime as _dt
    card = {
        'id': _dt.now().strftime('%Y%m%d%H%M%S'),
        'timestamp': _dt.now().strftime('%Y-%m-%d %H:%M:%S'),
        'stock': result.get('code','?'),
        'situation': f'引擎评分: 概率{prob}% {result.get("verdict","?")}',
        'tags': ['引擎自动'],
        'cost': 0,
        'lesson': '',
        'emotion': 'neutral',
    }
    bank['cards'].append(card)
    bank['stats']['total'] = len(bank['cards'])
    with open(card_path, 'w') as f:
        _j.dump(bank, f, ensure_ascii=False, indent=2)

def predict(code, rt_data=None):
    cfg = STOCK_DB.get(code, {})
    rt = rt_data or {'price': 0, 'pct': 0, 'high': 0, 'low': 0, 'prev': 0, 'turnover': 0, 'name': code}
    
    m = dict(MACRO)
    rank_map = {'机械设备': 4, '计算机': 8, '公用事业': 3, '有色金属': 26, '煤炭': 5}
    rank = rank_map.get(cfg.get('sector',''), 15)
    i = {'I1': 1 if rank <= 5 else (0 if rank <= 15 else -1), 'I2': 1 if rt['pct'] > 0.5 else (-1 if rt['pct'] < -0.5 else 0), 'I3': 0, 'I4': 1, 'I5': 0}
    pe = cfg.get('pe', 20)
    f = {'F1': 1 if pe < 15 else (0 if pe < 30 else -1), 'F2': 1 if cfg.get('growth') else -1, 'F3': 1 if cfg.get('order') else 0, 'F4': 0, 'F5': 1 if cfg.get('buyback') else 0}
    t = {'T1': 1 if rt['pct'] > 2 else (-1 if rt['pct'] < -2 else 0), 'T2': 1 if 0.5 <= rt['turnover'] <= 5 else (-1 if rt['turnover'] > 8 else 0), 'T3': 0, 'T4': 0, 'T5': 1 if rt['prev'] > 0 and rt['low'] > rt['prev'] * 0.95 else (-1 if rt['prev'] > 0 and rt['low'] < rt['prev'] * 0.93 else 0)}
    smap = {'early': 1, 'mid': 0, 'late': -1, 'decline': -1}
    r = {'R1': smap.get(cfg.get('stage', 'mid'), 0), 'R2': 0, 'R3': 0, 'R4': 0}
    
    sigs = {**m, **i, **f, **t, **r}
    def dim(p): vals = [v for k, v in sigs.items() if k.startswith(p)]; return sum(vals)/max(len(vals),1)
    dims = {d: round(dim(d), 2) for d in ['M','I','F','T','R']}
    total = sum(dims[d] * WEIGHTS[d] for d in WEIGHTS)
    prob = max(5, min(95, 50 + total * 35))
    bull = sum(1 for v in sigs.values() if v > 0); bear = sum(1 for v in sigs.values() if v < 0); neut = sum(1 for v in sigs.values() if v == 0)
    
    if prob >= 70: verdict, action = '看涨', '积极做多'
    elif prob >= 55: verdict, action = '偏乐观', '轻仓试探'
    elif prob >= 45: verdict, action = '观望', '观望等信号'
    elif prob >= 30: verdict, action = '偏悲观', '减仓观望'
    else: verdict, action = '看跌', '不做多/对冲'
    
    return {'code': code, 'name': rt.get('name', code), 'price': rt['price'], 'pct': rt['pct'],
            'prob': round(prob,1), 'verdict': verdict, 'action': action, 'dims': dims,
            'bull': bull, 'neut': neut, 'bear': bear,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'event_check': check_macro_events(code, 7)}
    _auto_decision_card(result)


if __name__ == '__main__':
    results = []
    for code, cfg in STOCK_DB.items():
        od = OFFLINE.get(code, (0,0,0,0,0,0))
        args = {k:v for k,v in cfg.items() if k != 'pe'}
        r = predict(code, {'price': od[0], 'pct': od[1], 'low': od[2], 'high': od[3], 'prev': od[4], 'turnover': od[5], 'name': code})
        results.append(r)
    
    results.sort(key=lambda x: x['prob'], reverse=True)
    
    # Event summary
    ec = results[0].get('event_check', {})
    scene_icons = {'A': '🟢催化剂', 'B': '🔴逆风', 'D': '⚪无事件'}
    print(f"📅 事件日历: {scene_icons.get(ec.get('scene','D'),'?')} | 宏观:{ec.get('macro_count',0)}个")
    crit = [w for w in ec.get('warnings',[]) if w['impact']=='CRITICAL']
    high = [w for w in ec.get('warnings',[]) if w['impact']=='HIGH']
    if crit: print(f"  🔴 {' '.join(w['event'] for w in crit)}")
    if high: print(f"  🟠 {', '.join(w['event'] for w in high[:3])}")
    
    print(f"\n{'标的':10s} {'概率':>5s} {'判定':6s} {'操作':10s} {'信号(多/中/空)'}")
    print('-' * 55)
    for r in results:
        nm = STOCK_DB[r['code']]['sector']
        print(f"{nm:4s} {r['code']} {r['prob']:4.0f}% {r['verdict']:4s}   {r['action']:8s}  {r['bull']}/{r['neut']}/{r['bear']}")
