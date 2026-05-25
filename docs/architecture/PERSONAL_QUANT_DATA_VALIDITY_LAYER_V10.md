# Personal Quant Data Validity Layer v1.0

## 定位

本层不是机构级数据平台。只做个人级最小量化数据闭环。

## 原则

- 默认 local CSV / manual snapshot
- external API disabled by default
- outcome backfill 使用 trading-bar offset，不是自然日
- outcome backfill 不真实写 Z9
- backtest 只验证 paper entries，不生成交易
- paper ledger 不允许 BUY / SELL / AUTO_TRADE / MARKET_ORDER / BROKER_ORDER 等 token 出现在 paper_action 中
- 所有输出均为 paper-only / preview-only

## 组件

| 组件 | 功能 | 文件 |
|------|------|------|
| Data Fact Layer | 本地 CSV schema、加载、校验 | zmatrix/data_facts/ |
| Paper Trade Ledger | 纸面交易条目生成 | zmatrix/paper_trading/ledger.py |
| Outcome Backfill Runner | 基于本地价格历史的真实回填 | zmatrix/paper_trading/outcome_backfill_runner.py |
| Portfolio Exposure Calculation | 基于价格历史计算 beta/corr/drawdown | zmatrix/investment/portfolio_exposure_calculation.py |
| Lightweight Backtest | 角色维度的 paper entry 回测 | zmatrix/backtest/lightweight_backtest.py |
| Monthly Review | 月度汇总报告 | zmatrix/paper_trading/monthly_review.py |
