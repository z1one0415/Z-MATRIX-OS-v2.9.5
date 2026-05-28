from __future__ import annotations
"""PATCH-A-2/3: Matrix Data Contract + PIT Rules"""

MATRIX_FACT_REQUIRED_QUESTIONS = ["source","visible_at","report_period","expired","pit_safe_for_trade_date","missing_handling"]

class MatrixFact:
    def __init__(self, ticker, trade_date, fact_name, fact_value, source, source_priority=0, report_period=None, announce_date=None, effective_date=None, collected_at=None, ttl_days=None):
        self.ticker = ticker; self.trade_date = trade_date; self.fact_name = fact_name; self.fact_value = fact_value; self.source = source; self.source_priority = source_priority; self.report_period = report_period; self.announce_date = announce_date; self.effective_date = effective_date; self.collected_at = collected_at; self.ttl_days = ttl_days
        self.freshness_status = "FRESH" if self._check_fresh() else "STALE"
        self.pit_safe = self._check_pit()
        self.quality_status = self._quality()

    def _check_fresh(self):
        if not self.ttl_days: return True
        return True  # placeholder
    def _check_pit(self):
        if self.announce_date and isinstance(self.announce_date, str):
            return self.announce_date.replace("-", "") <= self.trade_date.replace("-", "")
        return True
    def _quality(self):
        if self.fact_value is None: return "DATA_INSUFFICIENT"
        return "READY"

    def to_dict(self):
        return {"ticker":self.ticker,"trade_date":self.trade_date,"fact_name":self.fact_name,"fact_value":self.fact_value,"source":self.source,"source_priority":self.source_priority,"report_period":self.report_period,"announce_date":self.announce_date,"effective_date":self.effective_date,"collected_at":self.collected_at,"ttl_days":self.ttl_days,"freshness_status":self.freshness_status,"pit_safe":self.pit_safe,"quality_status":self.quality_status}

PIT_RULES = {"daily_price": {"rule":"close price at trade_date used for next-day decision","pit_safe":True,"strict":"intraday prices only for same-day context"}, "financial_report": {"rule":"announce_date <= trade_date REQUIRED","pit_safe":False,"strict":"must check announce_date vs trade_date"}, "event_announcement": {"rule":"publish_time <= decision_cutoff REQUIRED","pit_safe":False,"strict":"must have publish_time"}, "lhb_data": {"rule":"披露时间之后才可用","pit_safe":False,"strict":"盘后LHB不能用于当日盘中信号"}, "fund_flow": {"rule":"按可获得时间切分","pit_safe":False,"strict":"盘后资金流不能用于盘中信号"}, "industry_heat": {"rule":"必须有timestamp","pit_safe":False,"strict":"无timestamp的heat指标不可用"}}

DATA_SOURCE_CAPABILITY = {"financial_statements": {"level":"REQUIRED_CORE","source":"tushare income/balance_sheet/cashflow","coverage_estimate":"95%+","available_now":True},"daily_basic_valuation": {"level":"REQUIRED_CORE","source":"tushare daily_basic","coverage_estimate":"90%+","available_now":True},"industry_classification": {"level":"REQUIRED_CORE","source":"tushare stock_basic.industry","coverage_estimate":"99%+","available_now":True},"industry_rank": {"level":"OPTIONAL_ENHANCEMENT","source":"需自行计算行业百分位","coverage_estimate":"计算可得","available_now":False},"chain_evidence": {"level":"OPTIONAL_ENHANCEMENT","source":"需手动标注产业链位置","coverage_estimate":"<10%","available_now":False},"lhb_dragon_tiger": {"level":"OPTIONAL_ENHANCEMENT","source":"tushare top_list","coverage_estimate":"~5% stocks/day","available_now":True},"limit_structure": {"level":"OPTIONAL_ENHANCEMENT","source":"需从日线推断涨跌停","coverage_estimate":"计算可得","available_now":False},"fund_flow": {"level":"PROXY_ALLOWED","source":"暂无稳定免费源","coverage_estimate":"<50%","available_now":False},"theme_heat": {"level":"NOT_AVAILABLE_YET","source":"需另类数据","coverage_estimate":"<10%","available_now":False},"social_heat": {"level":"NOT_AVAILABLE_YET","source":"需另类数据","coverage_estimate":"0%","available_now":False}}
