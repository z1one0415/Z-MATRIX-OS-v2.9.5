#!/usr/bin/env python3
"""
Z2 轻量个股分析器 — 并行请求 + 缓存 + 无全市场拉取。
解决 stock_analyzer.py 的三大问题:
  1. ak.stock_zh_a_spot_em() 拉全市场5000只 → 改为单股API
  2. 市场数据每次重复拉取 → 缓存3分钟
  3. 10-20次请求串行 → 并发拉取
"""
import requests, json, time, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache

CACHE_DIR = os.path.expanduser('~/.openclaw/agents/z2-analyst/workspace/cache')
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Referer': 'https://quote.eastmoney.com/',
}


# ═══════════════════════════════════════════
# 1. 实时行情 — 单股API (不拉全市场)
# ═══════════════════════════════════════════

def _secid(code):
    if code[0] in '569': return f'1.{code}'
    return f'0.{code}'


def get_realtime(code, retries=2):
    """单股实时行情, 带重试+退避"""
    url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f2,f3,f4,f5,f6,f8,f10,f12,f14,f15,f16,f17,f20,f21&secids={_secid(code)}'
    for attempt in range(retries + 1):
        try:
            r = requests.get(url, headers=HEADERS, timeout=15)
            if r.status_code == 200:
                data = r.json()
                items = data.get('data', {}).get('diff', [])
                if items:
                    break
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
        except Exception:
            if attempt < retries:
                time.sleep(2 * (attempt + 1))
    else:
        return {}
    if not items:
        return {}
    item = items[0]
    return {
        'code': item.get('f12',''), 'name': item.get('f14',''),
        'price': item.get('f2',0), 'pct': item.get('f3',0),
        'high': item.get('f15',0), 'low': item.get('f16',0),
        'open': item.get('f17',0), 'prev_close': item.get('f4',0),
        'volume': item.get('f5',0), 'amount': item.get('f6',0),
        'turnover': item.get('f8',0), 'pe': item.get('f9'),
        'market_cap': item.get('f20',0), 'pb': item.get('f21'),
    }


# ═══════════════════════════════════════════
# 2. 历史K线 — 只用akshare(不可替代)
# ═══════════════════════════════════════════

@lru_cache(maxsize=32)
def get_history(code, days=120):
    """K线数据(缓存)"""
    try:
        import akshare as ak
        df = ak.stock_zh_a_hist(symbol=code, period='daily',
                                start_date='20251101', end_date='20500101',
                                adjust='qfq')
        return df.tail(days)
    except Exception:
        return None


# ═══════════════════════════════════════════
# 3. 市场数据 — 一次拉取, 3分钟缓存
# ═══════════════════════════════════════════

_market_cache = {}
_market_cache_time = 0


def get_market_context():
    """市场上下文(融资/北向/涨停/回购/解禁), 缓存3分钟"""
    global _market_cache, _market_cache_time
    now = time.time()
    if _market_cache and now - _market_cache_time < 180:
        return _market_cache

    ctx = {'margin': {}, 'north': {}, 'breadth': {}, 'repurchase': {}, 'unlock': {}}
    try:
        import akshare as ak
        # 融资
        try:
            sh = ak.macro_china_market_margin_sh()
            ctx['margin']['sh'] = float(sh.iloc[-1, 1]) if len(sh) > 0 else None
        except: pass
        # 北向
        try:
            hsgt = ak.stock_hsgt_hist_em(symbol="北向资金")
            if len(hsgt) > 5:
                ctx['north']['5d_net'] = float(hsgt['净流入'].tail(5).sum())
        except: pass
        # 涨停
        try:
            zt = ak.stock_zt_pool_em(date=time.strftime('%Y%m%d'))
            ctx['breadth']['zt_count'] = len(zt) if zt is not None else 0
        except: pass
        # 回购
        try:
            rep = ak.stock_repurchase_em()
            ctx['repurchase']['count'] = len(rep) if rep is not None else 0
        except: pass
    except Exception:
        pass

    _market_cache = ctx
    _market_cache_time = now
    return ctx


# ═══════════════════════════════════════════
# 4. 并行分析引擎
# ═══════════════════════════════════════════

def compute_momentum(hist_df):
    """从K线计算动量指标"""
    if hist_df is None or len(hist_df) < 20:
        return {'score': 5, 'rsi': None, 'chg_20d': None, 'macd': '?'}

    closes = hist_df['收盘'].values
    chg_20d = (closes[-1] / closes[-20] - 1) * 100 if len(closes) >= 20 else None
    chg_60d = (closes[-1] / closes[-60] - 1) * 100 if len(closes) >= 60 else None

    # RSI-14
    rsi = None
    if len(closes) >= 15:
        diffs = [closes[i] - closes[i-1] for i in range(1, len(closes))]
        up = sum(d for d in diffs[-14:] if d > 0) / 14
        down = abs(sum(d for d in diffs[-14:] if d < 0)) / 14
        rsi = 100 - 100 / (1 + up / down) if down > 0 else 100

    # MACD
    ema12 = closes[-1]
    ema26 = closes[-1]
    if len(closes) >= 26:
        ema12 = sum(closes[-12:]) / 12
        ema26 = sum(closes[-26:]) / 26
    macd_val = ema12 - ema26
    macd_signal = '多头' if macd_val > 0 else '空头'

    # 评分
    score = 5
    if chg_20d and chg_20d > 5: score += 1
    if chg_20d and chg_20d > 20: score += 1
    if rsi and rsi > 60: score += 1
    if rsi and rsi > 80: score -= 2
    if macd_val > 0: score += 1
    score = max(1, min(10, score))

    return {
        'score': score, 'rsi': round(rsi, 1) if rsi else None,
        'chg_20d': round(chg_20d, 1) if chg_20d else None,
        'chg_60d': round(chg_60d, 1) if chg_60d else None,
        'macd': macd_signal, 'macd_val': round(macd_val, 2)
    }


def analyze(code):
    """完整分析一只股票 — 并行拉取所有数据源"""
    import concurrent.futures
    rt = {}

    # 第一步: 实时行情(必须最先, 因为需要确认代码有效)
    rt = get_realtime(code)
    if not rt:
        return {'error': f'{code} 未找到'}

    # 第二步: 并行拉取历史和行情
    with ThreadPoolExecutor(max_workers=3) as ex:
        f_hist = ex.submit(get_history, code, 120)
        f_mkt = ex.submit(get_market_context)

        hist = f_hist.result()
        mkt = f_mkt.result()

    # 第三步: 计算指标(纯计算, 无IO)
    mom = compute_momentum(hist)

    # 组装结果
    price = rt.get('price', 0) or 0

    result = {
        'code': code, 'name': rt.get('name', '?'),
        'price': price, 'pct': rt.get('pct'),
        'open': rt.get('open'), 'high': rt.get('high'),
        'low': rt.get('low'), 'turnover': rt.get('turnover'),
        'volume': rt.get('volume'), 'amount': rt.get('amount'),
        'pe': rt.get('pe'), 'market_cap': rt.get('market_cap'),
        # 动量
        'momentum': mom,
        # 市场上下文
        'market': {
            'margin': mkt.get('margin', {}).get('sh'),
            'north_5d': mkt.get('north', {}).get('5d_net'),
            'zt_count': mkt.get('breadth', {}).get('zt_count'),
            'repurchase': mkt.get('repurchase', {}).get('count'),
        },
        'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S'),
    }

    # 综合评分(简化版五维)
    m_score = mom.get('score', 5)
    total = round(m_score * 0.4 + 5 * 0.6, 1)  # 基本面给默认5分
    result['total_score'] = total

    if total >= 7: result['recommendation'] = '偏强'
    elif total >= 5: result['recommendation'] = '中性'
    else: result['recommendation'] = '偏弱'

    risk = []
    if mom.get('rsi') and mom['rsi'] > 75: risk.append('RSI超买')
    if mom.get('rsi') and mom['rsi'] < 25: risk.append('RSI超卖')
    result['risk_flags'] = risk

    return result


# ═══════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python3 quick_analyzer.py <代码> [代码2] ...')
        print('示例: python3 quick_analyzer.py 002472')
        sys.exit(1)

    codes = [a for a in sys.argv[1:] if not a.startswith('--')]
    fmt_json = '--json' in sys.argv

    for code in codes:
        start = time.time()
        result = analyze(code)
        elapsed = time.time() - start
        if fmt_json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(f'=== {result.get("name",code)}({code}) ===')
            print(f'  现价: {result.get("price")} ({result.get("pct"):+.2f}%)')
            print(f'  区间: 开{result.get("open")} 高{result.get("high")} 低{result.get("low")}')
            print(f'  换手: {result.get("turnover")}%  量: {result.get("volume")}')
            mom = result.get('momentum', {})
            print(f'  动量: 评分{mom.get("score")} RSI{mom.get("rsi")} 20日{mom.get("chg_20d")}% MACD{mom.get("macd")}')
            mkt = result.get('market', {})
            print(f'  市场: 融资{mkt.get("margin")} 北向{mkt.get("north_5d")} 涨停{mkt.get("zt_count")}家')
            print(f'  总分: {result.get("total_score")} {result.get("recommendation")} 风险: {result.get("risk_flags")}')
            print(f'  ⏱️ 耗时: {elapsed:.1f}秒')
            print()
