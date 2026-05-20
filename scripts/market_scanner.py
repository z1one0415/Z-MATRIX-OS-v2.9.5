#!/usr/bin/env python3
"""
Z2 批量行情扫描器 — 分批拉取全市场数据，绕过反爬限制。
每批最多N只股票，批次间延迟M秒，永不触发东方财富限流。
"""
import requests, time, json, sys

BATCH_SIZE = 500      # 每批最多500只(远低于触发反爬的阈值)
BATCH_DELAY = 0.5     # 批次间延迟0.5秒
PAGE_SIZE = 100        # 每次API请求100只(东方财富单页上限)
REQUEST_DELAY = 0.2   # 请求间延迟

FIELDS = 'f2,f3,f4,f5,f12,f14,f15,f16,f17,f20'


def fetch_page(market, page, size=PAGE_SIZE):
    """拉取一页行情数据"""
    # market: 0=深圳 1=上海
    url = (
        f'https://push2.eastmoney.com/api/qt/clist/get'
        f'?pn={page}&pz={size}&po=1&np=1&fltt=2&invt=2'
        f'&fid=f3&fs=m:{market}+t:2,m:{market}+t:13,m:{market}+t:80'
        f'&fields={FIELDS}'
    )
    r = requests.get(url, timeout=15).json()
    items = r.get('data', {}).get('diff', [])
    total = r.get('data', {}).get('total', 0)
    return items, total


def scan_all(market='all', top_n=0, sort_by='pct'):
    """
    分批拉取全市场实时行情。
    market: 'all'/'sz'/'sh'
    top_n: 返回前N只, 0=全部
    sort_by: 'pct'按涨跌幅排序, 'amount'按成交额排序
    """
    all_stocks = []
    markets = []
    if market in ('all', 'sz'): markets.append(0)
    if market in ('all', 'sh'): markets.append(1)

    for mkt in markets:
        name = '深圳' if mkt == 0 else '上海'
        # 先拉第一页获取总数
        items, total = fetch_page(mkt, 1)

        if not items:
            print(f'  ⚠️ {name}: 无数据', file=sys.stderr)
            continue

        all_stocks.extend(items)
        total_pages = min((total + PAGE_SIZE - 1) // PAGE_SIZE, 50)  # 最多50页

        print(f'  {name}: 共{total}只, {total_pages}页, 分批拉取中...', file=sys.stderr)

        fetched = 0
        for page in range(2, total_pages + 1):
            if fetched >= BATCH_SIZE:
                print(f'    批次休息{REQUEST_DELAY}秒...', file=sys.stderr)
                time.sleep(BATCH_DELAY)
                fetched = 0

            items, _ = fetch_page(mkt, page)
            all_stocks.extend(items)
            fetched += len(items)
            time.sleep(REQUEST_DELAY)

        print(f'  {name}: 完成, 共{len(all_stocks)}只', file=sys.stderr)

    # 排序
    if sort_by == 'pct':
        all_stocks.sort(key=lambda x: x.get('f3', -999) or -999, reverse=True)
    elif sort_by == 'amount':
        all_stocks.sort(key=lambda x: x.get('f6', 0) or 0, reverse=True)

    if top_n > 0:
        all_stocks = all_stocks[:top_n]

    return all_stocks


def format_output(stocks, fmt='text'):
    """格式化输出"""
    if fmt == 'json':
        result = []
        for s in stocks:
            result.append({
                'code': s.get('f12',''), 'name': s.get('f14',''),
                'price': s.get('f2'), 'pct': s.get('f3'),
                'high': s.get('f15'), 'low': s.get('f16'),
                'volume': s.get('f5'), 'amount': s.get('f6'),
                'market_cap': s.get('f20'),
            })
        return json.dumps(result, ensure_ascii=False, indent=2)

    lines = []
    for i, s in enumerate(stocks[:200]):  # 最多显示200只
        name = s.get('f14','?')
        code = s.get('f12','?')
        price = s.get('f2','?')
        pct = s.get('f3')
        pct_str = f'{pct:+.2f}%' if pct is not None else '?'
        lines.append(f'{i+1}. {name}({code}) {price} {pct_str}')
    return '\n'.join(lines)


if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='Z2 批量行情扫描器')
    ap.add_argument('--market', default='all', choices=['all','sz','sh'])
    ap.add_argument('--top', type=int, default=20, help='返回前N只')
    ap.add_argument('--sort', default='pct', choices=['pct','amount'])
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    stocks = scan_all(market=args.market, top_n=args.top, sort_by=args.sort)
    print(format_output(stocks, fmt='json' if args.json else 'text'))
