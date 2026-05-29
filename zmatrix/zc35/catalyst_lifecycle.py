"""V4.0 ZC35 CatalystLifecycle — standalone module"""
from __future__ import annotations
LIFECYCLE = ["PRE_EVENT","EVENT_ACTIVE","POST_EVENT_DECAY","EXHAUSTED"]

class CatalystLifecycleEngine:
    def classify(self, event):
        if not event.get('publish_time'): return {"status":"DATA_INSUFFICIENT","direct_trade_allowed":False,"real_trade_allowed":False,"broker_order_allowed":False}
        ev = event.get('evidence_level','D')
        if ev == 'D': return {"lifecycle":"PRE_EVENT","sell_on_news_risk":"HIGH","direct_trade_allowed":False,"real_trade_allowed":False,"action":"WATCH_ONLY"}
        if event.get('scheduled_without_surprise'): return {"lifecycle":"PRE_EVENT","sell_on_news_risk":"MEDIUM","direct_trade_allowed":False,"real_trade_allowed":False,"action":"OBSERVE"}
        return {"lifecycle":"EVENT_ACTIVE","residual_power":0.8,"sell_on_news_risk":"LOW","direct_trade_allowed":False,"real_trade_allowed":False,"action":"PAPER_TRACK"}
