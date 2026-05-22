"""月度轮动扫描 — Rotation King monthly trend classifier integrated with R-Matrix"""
from __future__ import annotations
import baostock as bs


def scan_monthly_rotation(tickers: list[str], names: dict | None = None) -> list[dict]:
    """扫描月度轮动信号"""
    from zmatrix.scoring.r_matrix.rotation_king_monthly import classify_monthly_trend
    if names is None: names = {}
    
    bs.login()
    results = []
    
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}",
            "date,close", start_date="2024-01-01", end_date="2026-05-23",
            frequency="m", adjustflag="2")
        closes = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1] != '':
                closes.append(float(r[1]))
        
        if len(closes) < 6:
            results.append({"ticker": t, "name": names.get(t, "?"), "type": "DATA_INSUFFICIENT",
                           "beta_norm": 0, "channel_amp": 0, "position": 0.5, "action": "WAIT"})
            continue
        
        analysis = classify_monthly_trend(closes)
        results.append({
            "ticker": t,
            "name": names.get(t, "?"),
            **analysis,
        })
    
    bs.logout()
    return results
