"""Correlation Calculator — pair-wise stock correlation"""
from __future__ import annotations

def calc_correlation(prices_a: list[float], prices_b: list[float]) -> float | None:
    """Pearson correlation of daily returns for two stocks."""
    if len(prices_a) < 10 or len(prices_b) < 10:
        return None
    n = min(len(prices_a), len(prices_b))
    a_ret = [(prices_a[i]-prices_a[i-1])/prices_a[i-1] for i in range(1, n)]
    b_ret = [(prices_b[i]-prices_b[i-1])/prices_b[i-1] for i in range(1, n)]
    avg_a = sum(a_ret)/len(a_ret)
    avg_b = sum(b_ret)/len(b_ret)
    cov = sum((ar-avg_a)*(br-avg_b) for ar, br in zip(a_ret, b_ret))/(len(a_ret)-1)
    std_a = (sum((ar-avg_a)**2 for ar in a_ret)/(len(a_ret)-1))**0.5
    std_b = (sum((br-avg_b)**2 for br in b_ret)/(len(b_ret)-1))**0.5
    return round(cov/(std_a*std_b), 2) if std_a > 0 and std_b > 0 else None

def build_correlation_matrix(positions: list[dict], prices_map: dict[str, list[float]]) -> dict:
    """Build pair-wise correlation matrix for positions."""
    tickers = [p["ticker"] for p in positions]
    matrix = {}
    for i, ta in enumerate(tickers):
        for j, tb in enumerate(tickers):
            if i < j:
                corr = calc_correlation(prices_map.get(ta, []), prices_map.get(tb, []))
                if corr is not None and corr > 0.70:
                    matrix[f"{ta}-{tb}"] = {"correlation": corr, "warning": "high_correlation" if corr > 0.80 else None}
    return matrix
