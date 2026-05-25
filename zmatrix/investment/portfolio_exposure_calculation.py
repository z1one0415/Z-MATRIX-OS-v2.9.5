"""Portfolio Exposure Calculation v1.0 — 基于本地价格历史的真实计算"""
from __future__ import annotations
from datetime import datetime
import statistics

def _get_prices(bars: list[dict], limit: int = None) -> list[float]:
    prices = []
    for b in bars:
        try: prices.append(float(b.get("adj_close", b.get("close", 0))))
        except: continue
    if limit: prices = prices[-limit:]
    return prices

def _calc_beta(prices_a: list[float], prices_b: list[float]) -> float | None:
    if len(prices_a) < 5 or len(prices_b) < 5: return None
    min_len = min(len(prices_a), len(prices_b))
    a, b = prices_a[-min_len:], prices_b[-min_len:]
    ra = [(a[i]-a[i-1])/a[i-1]*100 for i in range(1,len(a))]
    rb = [(b[i]-b[i-1])/b[i-1]*100 for i in range(1,len(b))]
    if len(ra) < 3: return None
    cov = statistics.covariance(ra, rb) if hasattr(statistics, 'covariance') else sum((x-sum(ra)/len(ra))*(y-sum(rb)/len(rb)) for x,y in zip(ra,rb))/len(ra)
    var_b = statistics.variance(rb) if len(rb) > 1 else 0
    if var_b == 0: return None
    try: return round(cov / var_b, 2)
    except: return None

def _calc_corr(prices_a: list[float], prices_b: list[float]) -> float | None:
    if len(prices_a) < 5 or len(prices_b) < 5: return None
    min_len = min(len(prices_a), len(prices_b))
    a, b = prices_a[-min_len:], prices_b[-min_len:]
    try:
        if not hasattr(statistics, 'correlation'):
            n = len(a)
            ma, mb = sum(a)/n, sum(b)/n
            num = sum((x-ma)*(y-mb) for x,y in zip(a,b))
            da = (sum((x-ma)**2 for x in a)/n)**0.5
            db = (sum((y-mb)**2 for y in b)/n)**0.5
            return round(num/(n*da*db), 2) if da and db else None
        return round(statistics.correlation(a, b), 2)
    except: return None

def _calc_max_drawdown(prices: list[float]) -> float | None:
    if len(prices) < 2: return None
    peak = prices[0]; mdd = 0.0
    for p in prices:
        peak = max(peak, p)
        dd = (peak - p) / peak * 100
        mdd = max(mdd, dd)
    return round(mdd, 2)

def calculate_exposure_from_price_history(candidate: dict, portfolio: list[dict], price_bars_by_ticker: dict[str, list[dict]], market_proxy_bars: list[dict] | None = None) -> dict:
    ticker = candidate.get("ticker", "")
    chain = candidate.get("chain", "")
    bars = price_bars_by_ticker.get(ticker, [])
    prices = _get_prices(bars, limit=250)

    market_prices = _get_prices(market_proxy_bars or [], limit=250) if market_proxy_bars else None

    market_beta = _calc_beta(prices, market_prices) if market_prices else None
    max_dd = _calc_max_drawdown(prices)
    degraded = len(prices) < 20

    # sector proxy beta — use first portfolio stock in same sector
    sector_beta = None
    for pos in portfolio or []:
        if pos.get("sector") == candidate.get("sector") and pos.get("ticker") != ticker:
            pos_bars = price_bars_by_ticker.get(pos.get("ticker", ""), [])
            pos_prices = _get_prices(pos_bars, limit=250)
            sector_beta = _calc_beta(prices, pos_prices)
            if sector_beta: break

    correlations = {}
    for horizon, days in [("60d", 60), ("120d", 120), ("250d", 250)]:
        h_prices = prices[-days:] if len(prices) >= days else prices
        m_prices = market_prices[-days:] if market_prices and len(market_prices) >= days else market_prices
        if m_prices:
            correlations[horizon] = _calc_corr(h_prices, m_prices)
        else:
            correlations[horizon] = None

    drawdown_overlap = degraded
    warnings = []
    if degraded:
        warnings.append("INSUFFICIENT_PRICE_HISTORY")

    same_chain_weight = sum(p.get("weight",0) for p in (portfolio or []) if p.get("chain")==chain and p.get("ticker")!=ticker)
    duplicate_exposure = same_chain_weight + 5.0
    if duplicate_exposure > 35:
        warnings.append(f"CHAIN_EXPOSURE:{duplicate_exposure:.1f}>35")

    return {
        "market_beta": market_beta, "sector_beta": sector_beta,
        "max_drawdown": max_dd, "drawdown_overlap": drawdown_overlap,
        "correlation_60d": correlations.get("60d"),
        "correlation_120d": correlations.get("120d"),
        "correlation_250d": correlations.get("250d"),
        "degraded": degraded, "duplicate_exposure_pct": round(duplicate_exposure,1),
        "exposure_gate_passed": not degraded,
        "add_position_allowed": not degraded,
        "warnings": warnings,
    }
