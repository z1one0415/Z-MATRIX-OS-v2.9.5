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


def scan_oscillation_king(tickers: list[str]) -> list[dict]:
    """波动天王: 5日线 BOX hunter (17% BOX optimal)"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date="2026-05-23",frequency="d",adjustflag="2")
        all_c = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': all_c.append(float(r[1]))
        sampled = all_c[::5]
        if len(sampled)>=20:
            r = classify_rhythm(sampled, beta_threshold=0.002, box_amp_min=5, box_amp_max=200)
            results.append({"ticker":t,"king":"波动天王",**r})
    bs.logout()
    return results


def scan_rhythm_king(tickers: list[str]) -> list[dict]:
    """律动天王: 周线 mid-term swing (30% BOX)"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date="2026-05-23",frequency="w",adjustflag="2")
        closes = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': closes.append(float(r[1]))
        if len(closes)>=20:
            r = classify_rhythm(closes, beta_threshold=0.004, box_amp_min=10, box_amp_max=150)
            results.append({"ticker":t,"king":"律动天王",**r})
    bs.logout()
    return results


def scan_rotation_king(tickers: list[str]) -> list[dict]:
    """轮动天王: 双周线 rotation entry (13% BOX, 3x monthly entries)"""
    import baostock as bs
    from zmatrix.scoring.r_matrix.rhythm_king_weekly import classify_rhythm
    bs.login()
    results = []
    for t in tickers:
        prefix = "sz" if t[0] in "03" else "sh"
        rs = bs.query_history_k_data_plus(f"{prefix}.{t}","date,close",
            start_date="2024-01-01",end_date="2026-05-23",frequency="d",adjustflag="2")
        all_c = []
        while rs.next():
            r = rs.get_row_data()
            if r[1] and r[1]!='': all_c.append(float(r[1]))
        sampled = all_c[::10]
        if len(sampled)>=6:
            r = classify_rhythm(sampled, beta_threshold=0.004, box_amp_min=8, box_amp_max=200)
            results.append({"ticker":t,"king":"轮动天王",**r})
    bs.logout()
    return results
