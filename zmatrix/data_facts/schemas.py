"""Data Fact Layer schemas v1.0 — 标准数据契约"""
PRICE_BAR_FIELDS = ["date","ticker","open","high","low","close","volume","adj_close"]
FINANCIAL_SNAPSHOT_FIELDS = ["date","ticker","revenue_growth","net_profit_growth","deducted_net_profit_growth","gross_margin","operating_cashflow","roe","debt_ratio","valuation_percentile","pe","pb","ps","market_cap"]
SECTOR_CHAIN_FIELDS = ["ticker","industry","sector","chain","theme","style_factor"]
PAPER_LEDGER_FIELDS = ["paper_id","ticker","role","entry_date","entry_price","paper_action","reason","target_horizon","max_loss_plan","invalidation_condition","created_at"]
OUTCOME_FIELDS = ["paper_id","ticker","entry_date","actual_return_t5","actual_return_t20","actual_return_t60","max_drawdown_t20","max_drawdown_t60","outcome_status","error_type","review_note"]

ALL_SCHEMAS = {
    "price_bars": PRICE_BAR_FIELDS,
    "financial_snapshot": FINANCIAL_SNAPSHOT_FIELDS,
    "sector_chain": SECTOR_CHAIN_FIELDS,
    "paper_ledger": PAPER_LEDGER_FIELDS,
    "outcome": OUTCOME_FIELDS,
}

def validate_row(schema_name: str, row: dict) -> list[str]:
    errors = []
    fields = ALL_SCHEMAS.get(schema_name, [])
    for f in fields:
        if f not in row:
            errors.append(f"MISSING_FIELD:{f}")
    return errors
