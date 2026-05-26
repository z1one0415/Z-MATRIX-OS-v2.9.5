"""Beta Calculator — stock beta vs index from local data"""
from __future__ import annotations

def calc_beta(stock_prices: list[float], index_prices: list[float]) -> float | None:
    """Simple beta = covariance(stock,index) / variance(index)."""
    if len(stock_prices) < 10 or len(index_prices) < 10:
        return None
    n = min(len(stock_prices), len(index_prices))
    s = stock_prices[-n:]
    m = index_prices[-n:]
    s_ret = [(s[i]-s[i-1])/s[i-1] for i in range(1, n)]
    m_ret = [(m[i]-m[i-1])/m[i-1] for i in range(1, n)]
    avg_s = sum(s_ret) / len(s_ret)
    avg_m = sum(m_ret) / len(m_ret)
    cov = sum((sr-avg_s)*(mr-avg_m) for sr, mr in zip(s_ret, m_ret)) / (len(s_ret)-1)
    var = sum((mr-avg_m)**2 for mr in m_ret) / (len(m_ret)-1)
    return round(cov/var, 2) if var > 0 else None
