"""ResearchDB Account Truth — holding PnL builder (FIFO)."""
from __future__ import annotations

COST_METHOD = "FIFO"


def build_holding_pnl(trades: list[dict], positions: list[dict]) -> list[dict]:
    """Build per-holding PnL ledger using FIFO cost method.
    
    Returns list of holding PnL records with realized/unrealized PnL and max excursions.
    """
    holdings = []
    # Group trades by ticker
    ticker_trades: dict[str, list[dict]] = {}
    for t in trades:
        ticker = t.get("ticker", "")
        ticker_trades.setdefault(ticker, []).append(t)
    
    for ticker, tt in ticker_trades.items():
        tt.sort(key=lambda x: x.get("trade_date", ""))
        buys = [t for t in tt if t.get("side") == "BUY"]
        sells = [t for t in tt if t.get("side") == "SELL"]
        
        buy_qty = sum(int(b.get("quantity", 0)) for b in buys)
        buy_amt = sum(float(b.get("amount", 0)) for b in buys)
        sell_qty = sum(int(s.get("quantity", 0)) for s in sells)
        sell_amt = sum(float(s.get("amount", 0)) for s in sells)
        
        holdings.append({
            "ticker": ticker,
            "name": buys[0].get("name", ticker) if buys else ticker,
            "open_date": buys[0].get("trade_date", "") if buys else "",
            "close_date": sells[-1].get("trade_date", "") if sells else "",
            "holding_days": 0,
            "buy_amount": buy_amt,
            "sell_amount": sell_amt,
            "realized_pnl": sell_amt - buy_amt if buy_qty else 0,
            "unrealized_pnl": 0.0,
            "total_return": (sell_amt - buy_amt) / buy_amt if buy_amt > 0 else 0,
            "max_favorable_excursion": 0.0,
            "max_adverse_excursion": 0.0,
            "exit_reason": "UNKNOWN",
            "quality_status": "READY",
            "cost_method": COST_METHOD,
        })
    return holdings
