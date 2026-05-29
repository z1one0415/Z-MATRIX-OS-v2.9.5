"""V4.0 ZC40 LimitBoardFillabilityGate — standalone module"""
from __future__ import annotations
STATUSES = ["NOT_FILLABLE","WAIT_OPEN_BOARD","OPEN_BOARD_CONFIRMATION_REQUIRED","CHASE_RISK","LIQUIDITY_TRAP","PAPER_ONLY_OBSERVE","DATA_INSUFFICIENT"]

class LimitBoardFillabilityGate:
    def check(self, ohlc, prev_close):
        if not ohlc or not prev_close: return {"status":"DATA_INSUFFICIENT","blocks_new_entry":True,"real_trade_allowed":False,"broker_order_allowed":False}
        o,h,l,c = ohlc.get('open'), ohlc.get('high'), ohlc.get('low'), ohlc.get('close')
        pct = (c-prev_close)/prev_close*100 if prev_close else 0
        if o and h and l and c and h==l and pct>=9.8: return {"status":"NOT_FILLABLE","blocks_new_entry":True,"one_price_board":True,"real_trade_allowed":False,"broker_order_allowed":False}
        if pct>=9.8: return {"status":"OPEN_BOARD_CONFIRMATION_REQUIRED","blocks_new_entry":True,"real_trade_allowed":False,"broker_order_allowed":False}
        return {"status":"PAPER_ONLY_OBSERVE","blocks_new_entry":False,"real_trade_allowed":False,"broker_order_allowed":False}
