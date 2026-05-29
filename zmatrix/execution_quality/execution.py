"""V4.0-C5 ExecutionQuality — paper-only execution engine"""
from __future__ import annotations

class TransactionCostModel:
    @staticmethod
    def compute(entry_price, exit_price, volume):
        commission = max(5, entry_price*volume*0.0003) + max(5, exit_price*volume*0.0003)
        stamp = exit_price*volume*0.001; notional = entry_price*volume
        slippage = 0.0005; cost = (commission+stamp)/notional+slippage if notional else 0.01
        return {"commission_pct":commission/notional*100 if notional else 0,"stamp_pct":stamp/notional*100 if notional else 0,"slippage_pct":slippage*100,"total_cost_pct":cost*100,"real_trade_allowed":False,"broker_order_allowed":False}

class LimitBoardGate:
    ALLOWED = ["PAPER_ONLY_OBSERVE","WAIT","NOT_FILLABLE","LIQUIDITY_TRAP","ROUTE_REJECTED","DATA_INSUFFICIENT"]
    FORBIDDEN = ["BUY","SELL","ORDER","BROKER_ORDER","AUTO_EXECUTE"]
    @staticmethod
    def check(ohlc, prev_close):
        o=ohlc.get('open');h=ohlc.get('high');l=ohlc.get('low');c=ohlc.get('close')
        if not all([o,h,l,c]) or not prev_close: return {"action":"DATA_INSUFFICIENT","real_trade_allowed":False}
        pct=(c-prev_close)/prev_close*100
        if o==h==l==c and pct>=9.8: return {"action":"NOT_FILLABLE","real_trade_allowed":False,"broker_order_allowed":False}
        return {"action":"PAPER_ONLY_OBSERVE","real_trade_allowed":False,"broker_order_allowed":False}

class PaperOrderPreview:
    @staticmethod
    def generate(ticker, action, size, price):
        return {"ticker":ticker,"action":action,"size":size,"price":price,"real_trade_allowed":False,"broker_order_allowed":False,"paper_only":True,"human_review_required":True}
