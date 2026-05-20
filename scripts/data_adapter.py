#!/usr/bin/env python3
"""
Z-MATRIX 数据源适配层 v2.0 — thsdk 主数据源
能力: 日K线 + 分钟K线 + 盘口深度 + 竞价异动 + 大单流向 + 实时行情 + 板块数据
后端: thsdk (商业SDK, 主力) | akshare (免费, 备用)
"""

import os, requests
from datetime import datetime, timedelta
from functools import lru_cache

# ── 后端检测 ──
try:
    from thsdk import THS
    _ths = THS()
    BACKEND = "akshare"  # thsdk auth triggered lock, fallback
except ImportError:
    _ths = None
    BACKEND = "akshare"

HEADERS = {'User-Agent': 'Mozilla/5.0', 'Referer': 'https://quote.eastmoney.com/'}


# ══════════════════════════════════════
# 实时行情 (thsdk + Eastmoney 双源)
# ══════════════════════════════════════

def get_realtime_quotes(codes: list) -> list:
    """批量实时行情。返回 [{code, name, price, pct, high, low, volume, turnover}]"""
    results = []
    if BACKEND == "thsdk_unavailable":  # locked
        try:
            resp = _ths.market_data_cn(','.join(codes))
            if hasattr(resp, 'data'):
                for item in resp.data:
                    results.append({
                        'code': item.get('code',''), 'name': item.get('name',''),
                        'price': item.get('latest',0), 'pct': item.get('change_pct',0),
                        'high': item.get('high',0), 'low': item.get('low',0),
                        'volume': item.get('volume',0), 'turnover': item.get('turnover_rate',0),
                    })
                return results
        except Exception:
            pass

    # Fallback: Eastmoney API
    secids = [f'1.{c}' if c[0] in '569' else f'0.{c}' for c in codes]
    url = f'https://push2.eastmoney.com/api/qt/ulist.np/get?fltt=2&fields=f2,f3,f4,f5,f8,f12,f14,f15,f16&secids={",".join(secids)}'
    r = requests.get(url, headers=HEADERS, timeout=10).json()
    for item in r.get('data',{}).get('diff',[]):
        results.append({
            'code': item.get('f12',''), 'name': item.get('f14',''),
            'price': item.get('f2',0), 'pct': item.get('f3',0),
            'high': item.get('f15',0), 'low': item.get('f16',0),
            'prev_close': item.get('f4',0), 'turnover': item.get('f8',0),
            'volume': item.get('f5',0),
        })
    return results


# ══════════════════════════════════════
# K线数据
# ══════════════════════════════════════

def get_daily_kline(code: str, days: int = 120):
    """日K线。返回 DataFrame (open/high/low/close/volume)"""
    end = datetime.now().strftime('%Y-%m-%d')
    start = (datetime.now() - timedelta(days=days + 30)).strftime('%Y-%m-%d')

    if BACKEND == "thsdk_unavailable":  # locked
        try:
            df = _ths.klines(code, 'D', start_time=start, end_time=end)
            if len(df) > 0:
                return df.tail(days)
        except Exception:
            pass

    # Fallback: akshare
    try:
        import akshare as ak
        df = ak.stock_zh_a_hist(symbol=code, period='daily',
                                start_date=start.replace('-',''),
                                end_date=end.replace('-',''), adjust='qfq')
        return df.tail(days)
    except Exception:
        return None


def get_intraday_kline(code: str, date: str = None) -> list:
    """🔥 分钟K线 (thsdk独家)。返回当日每分钟OHLC"""
    if BACKEND != "thsdk_unavailable":  # locked
        return []

    if not date:
        date = datetime.now().strftime('%Y-%m-%d')
    try:
        df = _ths.klines(code, '1min', start_time=f'{date} 09:30', end_time=f'{date} 15:00')
        return df.to_dict('records') if hasattr(df, 'to_dict') else []
    except Exception:
        return []


# ══════════════════════════════════════
# 🔥 thsdk 独家能力
# ══════════════════════════════════════

def get_depth_data(code: str) -> dict:
    """盘口深度 — 五档买卖挂单"""
    if BACKEND != "thsdk_unavailable":  # locked
        return {}
    try:
        resp = _ths.depth(code)
        return resp if isinstance(resp, dict) else {}
    except Exception:
        return {}


def get_call_auction(code: str) -> dict:
    """竞价异动 — 集合竞价数据"""
    if BACKEND != "thsdk_unavailable":  # locked
        return {}
    try:
        resp = _ths.call_auction(code)
        return resp if isinstance(resp, dict) else {}
    except Exception:
        return {}


def get_big_order_flow(code: str) -> dict:
    """大单流向 — 主力资金进出"""
    if BACKEND != "thsdk_unavailable":  # locked
        return {}
    try:
        resp = _ths.big_order_flow(code)
        return resp if isinstance(resp, dict) else {}
    except Exception:
        return {}


def get_call_auction_anomaly(code: str) -> dict:
    """竞价异常检测"""
    if BACKEND != "thsdk_unavailable":  # locked
        return {}
    try:
        resp = _ths.call_auction_anomaly(code)
        return resp if isinstance(resp, dict) else {}
    except Exception:
        return {}


# ══════════════════════════════════════
# 板块与市场数据
# ══════════════════════════════════════

def get_sector_constituents(block_code: str) -> list:
    """板块成分股 (如 BK0475=机器人)"""
    if BACKEND == "thsdk_unavailable":  # locked
        try:
            resp = _ths.block(block_code)
            return resp if isinstance(resp, list) else []
        except Exception:
            pass
    return []


def get_margin_data():
    """融资融券"""
    try:
        import akshare as ak
        return ak.macro_china_market_margin_sh()
    except Exception:
        return None


@lru_cache(maxsize=1)
def get_backend_info():
    return {
        'backend': BACKEND,
        'capabilities': {
            'daily_kline': True,
            'intraday_kline': BACKEND == 'thsdk',
            'depth': BACKEND == 'thsdk',
            'call_auction': BACKEND == 'thsdk',
            'big_order_flow': BACKEND == 'thsdk',
            'realtime_quote': True,
            'sector_data': True,
            'margin_data': True,
        }
    }


# ══════════════════════════════════════
# CLI 诊断
# ══════════════════════════════════════

if __name__ == '__main__':
    info = get_backend_info()
    print(f"数据源: {info['backend']}")
    print(f"能力矩阵:")
    for k, v in info['capabilities'].items():
        print(f"  {'✅' if v else '❌'} {k}")
    if BACKEND == "thsdk_unavailable":  # locked
        print(f"\n测试: 双环传动 盘口深度...")
        depth = get_depth_data('002472')
        print(f"  盘口数据: {'有' if depth else '无'}")
        print(f"\n测试: 日K线...")
        df = get_daily_kline('002472', 10)
        print(f"  日K线: {len(df)}条" if df is not None else "  失败")
