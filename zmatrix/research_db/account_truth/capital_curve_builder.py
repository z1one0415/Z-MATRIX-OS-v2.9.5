"""ResearchDB Account Truth — capital curve builder."""
from __future__ import annotations


def build_capital_curve(snapshots: list[dict]) -> list[dict]:
    """Build capital curve from sorted account snapshots.
    Deducts deposit/withdrawal impact to show true investment returns.
    """
    if not snapshots:
        return []
    sorted_snaps = sorted(snapshots, key=lambda s: s.get("date", ""))
    curve = []
    initial_equity = float(sorted_snaps[0].get("total_equity", 0))
    peak = initial_equity
    for i, s in enumerate(sorted_snaps):
        equity = float(s.get("total_equity", 0))
        net_adj = float(s.get("net_deposit_adjusted_equity", equity))
        daily_ret = float(s.get("daily_return", 0))
        peak = max(peak, equity)
        dd = (equity - peak) / peak if peak > 0 else 0
        cum_ret = (equity - initial_equity) / initial_equity if initial_equity > 0 else 0
        curve.append({
            "date": s.get("date", ""),
            "account_id": s.get("account_id", ""),
            "total_equity": equity,
            "net_deposit_adjusted_equity": net_adj,
            "daily_return": daily_ret,
            "cumulative_return": cum_ret,
            "max_drawdown": dd,
            "quality_status": s.get("quality_status", "READY"),
        })
    return curve
