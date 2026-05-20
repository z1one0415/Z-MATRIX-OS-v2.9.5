#!/usr/bin/env python3
"""Z2 轻量实时行情 — 东方财富API直连, 按需拉取任意A股"""
import requests, sys, json

# 常用标的名称映射(可选, 没在表里的也能查)
NAME_MAP = {
    '002472':'双环传动','002050':'三花智控','688017':'绿的谐波',
    '002979':'雷赛智能','601899':'紫金矿业','000636':'风华高科',
    '002747':'埃斯顿','002896':'中大力德','603728':'鸣志电器',
    '301368':'丰立智能','002230':'科大讯飞','002375':'亚厦股份',
    '002777':'久远银海','601898':'中煤能源','600111':'北方稀土',
    '002491':'通鼎互联','300604':'长川科技','688008':'澜起科技',
    '605006':'山东玻纤','688146':'中船特气','688726':'兴福电子',
    '688618':'三旺通信',
}

def quote(*codes, json_fmt=False, retries=2, delay=1.0):
    """拉取实时行情。自动重试+退避。"""
    import time as _time
    for attempt in range(retries + 1):
        try:
            result = _do_quote(codes, json_fmt)
            return result
        except Exception as e:
            if attempt < retries:
                _time.sleep(delay * (attempt + 1))
            else:
                raise e

def _do_quote(codes, json_fmt=False):
    """
    拉取实时行情。
    codes: 股票代码列表, 如 '002472' '601899'
    json_fmt: True返回JSON字符串, False返回格式化文本
    """
    def _secid(c):
        # 沪市: 5xxxxx(ETF/基金) 6xxxxx(A股) 9xxxxx(B股)
        # 深市: 0xxxxx 3xxxxx 1xxxxx 2xxxxx
        if c[0] in '569':
            return f'1.{c}'
        return f'0.{c}'
    secids = [_secid(c) for c in codes]
    fields = 'f2,f3,f4,f5,f6,f7,f8,f10,f12,f14,f15,f16,f17'
    url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields={fields}&secids={",".join(secids)}'
    r = requests.get(url, timeout=10).json()
    results = []
    for item in r.get('data',{}).get('diff',[]):
        name = item.get('f14') or NAME_MAP.get(item.get('f12',''),'?')
        q = {
            'name': name,
            'code': item.get('f12',''),
            'price': item.get('f2'),
            'pct': item.get('f3'),
            'high': item.get('f15'),
            'low': item.get('f16'),
            'open': item.get('f17'),
            'volume': item.get('f5'),
            'amount': item.get('f6'),
            'turnover': item.get('f8'),
            'prev_close': item.get('f4'),
        }
        results.append(q)

    if json_fmt:
        return json.dumps(results, ensure_ascii=False, indent=2)

    lines = []
    for q in results:
        pct_str = f'{q["pct"]:+.2f}%' if q['pct'] is not None else '?'
        lines.append(
            f'{q["name"]}({q["code"]}): {q["price"]} {pct_str} '
            f'开{q["open"]} 高{q["high"]} 低{q["low"]} '
            f'换手{q["turnover"]}% 量{q["volume"]}手'
        )
    return '\n'.join(lines)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('用法: python3 realtime_quote.py <代码1> <代码2> ...')
        print('示例: python3 realtime_quote.py 002472 002050 601899')
        sys.exit(1)

    fmt = '--json' in sys.argv
    codes = [a for a in sys.argv[1:] if not a.startswith('--')]
    print(quote(*codes, json_fmt=fmt))
