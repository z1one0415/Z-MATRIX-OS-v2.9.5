"""V4.0-B3 DataForge + FactorFactory + ZC35/ZC45"""
from __future__ import annotations

# ZC40 LimitBoardFillabilityGate
LIMIT_BOARD_STATUSES = ["NOT_FILLABLE","WAIT_OPEN_BOARD","OPEN_BOARD_CONFIRMATION_REQUIRED","CHASE_RISK","LIQUIDITY_TRAP","PAPER_ONLY_OBSERVE","DATA_INSUFFICIENT"]

class LimitBoardFillabilityGate:
    def check(self, ohlc, prev_close):
        if not ohlc or not prev_close: return {"status":"DATA_INSUFFICIENT","blocks_new_entry":True}
        o,h,l,c = ohlc.get('open'), ohlc.get('high'), ohlc.get('low'), ohlc.get('close')
        pct = (c-prev_close)/prev_close*100 if prev_close else 0
        one_price = o and h and l and c and (h==l) and pct>=9.8
        if one_price: return {"status":"NOT_FILLABLE","blocks_new_entry":True,"one_price_board":True,"consecutive_check":True}
        if pct>=9.8: return {"status":"OPEN_BOARD_CONFIRMATION_REQUIRED","blocks_new_entry":True}
        return {"status":"PAPER_ONLY_OBSERVE","blocks_new_entry":False}

# ZC45 ProxyHedgeStressTest
PROXY_HEDGE_STATUSES = ["PROXY_HEDGE_EFFECTIVE","DEFENSIVE_ONLY","CORRELATION_BREAKDOWN","LIQUIDITY_CRASH_RISK","NOT_A_HEDGE","DATA_INSUFFICIENT"]

class ProxyHedgeStressTest:
    def run(self, defensive_assets, scenario="2020_COVID"):
        if not defensive_assets: return {"status":"DATA_INSUFFICIENT","market_neutral_claim":"FORBIDDEN","auto_allocate":"FORBIDDEN"}
        correlation_risk = len(defensive_assets)<=2
        if correlation_risk: return {"status":"CORRELATION_BREAKDOWN","hedge_effective":False,"market_neutral_claim":"FORBIDDEN"}
        return {"status":"PROXY_HEDGE_EFFECTIVE","hedge_effective":True,"market_neutral_claim":"FORBIDDEN","defensive_only":True}

# ZC35 Catalyst Lifecycle
CATALYST_LIFECYCLE = ["PRE_EVENT","EVENT_ACTIVE","POST_EVENT_DECAY","EXHAUSTED"]

class CatalystLifecycleEngine:
    def classify(self, event):
        if not event.get('publish_time'): return {"status":"DATA_INSUFFICIENT","direct_trade_allowed":False}
        evidence = event.get('evidence_level','D')
        if evidence == 'D': return {"lifecycle":"PRE_EVENT","sell_on_news_risk":"HIGH","direct_trade_allowed":False,"action":"WATCH_ONLY"}
        if event.get('scheduled_without_surprise'): return {"lifecycle":"PRE_EVENT","sell_on_news_risk":"MEDIUM","direct_trade_allowed":False,"action":"OBSERVE"}
        return {"lifecycle":"EVENT_ACTIVE","residual_power":0.8,"sell_on_news_risk":"LOW","direct_trade_allowed":False,"action":"PAPER_TRACK"}

# Multi-Strategy Sleeve
class MultiStrategySleeve:
    def __init__(self): self.sleeves = {"ROLE_CORE":{"weight_cap":0.30,"beta_budget":0.80},"ROLE_ROT":{"weight_cap":0.25,"beta_budget":1.0},"ROLE_HUNT":{"weight_cap":0.15,"beta_budget":1.2,"paper_only":True},"DEFENSIVE":{"weight_cap":0.30,"beta_budget":0.50},"CASH":{"weight_cap":1.0,"beta_budget":0.0}}
    def allocate(self, candidates):
        alloc={}; remaining=1.0
        for sleeve, cfg in self.sleeves.items():
            w=min(cfg['weight_cap'],remaining); alloc[sleeve]=w; remaining-=w
        return {"allocations":alloc,"total_beta_check":sum(alloc.get(s,0)*self.sleeves[s]['beta_budget'] for s in alloc),"production_allowed":False}
