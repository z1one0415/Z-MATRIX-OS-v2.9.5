
# Z2天师 Hermes Research Kernel Workspace Factor Package

## A组 — 16 Verified Local IC Factors

| # | ID | Name | Formula | Direction | IC | IC Status | Source |
|---|-----|------|---------|-----------|----|-----------|--------|
| 1 | F04 | RESIDUAL_MOMENTUM | cumulative_return(t-20,t-5) | ALPHA | 0.032 | verified | price_bars |
| 2 | F10 | LOW_VOLATILITY | 1/(1+std(daily_returns,20)*100) | RISK | -0.041 | verified | price_bars |
| 3 | F11 | SHORT_TERM_REVERSAL | -return(t-5,t) | ALPHA | -0.028 | verified | price_bars |
| 4 | F21 | TREND_PERSISTENCE | consecutive_same_direction_ratio_20d | ALPHA | 0.045 | verified | price_bars |
| 5 | F24 | VOL_COMPRESSION | 1.0-std(recent_5d)/std(full_20d) | ALPHA | 0.038 | verified | price_bars |
| 6 | F30 | VOL_PRICE_CONFIRM | corr(daily_returns,volume_changes) | ALPHA | 0.029 | verified | price_bars |
| 7 | F31 | DOWNSIDE_TAIL | -max_drawdown_20d | RISK | -0.035 | verified | price_bars |
| 8 | F53 | ATTENTION_SPIKE | (vol_5d/vol_20d)*abs(ret_5d) | ALPHA | 0.042 | verified | price_bars |
| 9 | F54 | CROWDING_RISK | volume_zscore+high_vol_days*0.2 | RISK | -0.033 | verified | price_bars |
| 10 | F55 | SENTIMENT_DECAY | -(current_vol_ratio-peak_vol_ratio) | RISK | -0.026 | hypothesis | price_bars |
| 11 | F56 | MONEY_FLOW | sum(CLV*volume_5d)/sum(volume_5d) | ALPHA | 0.036 | verified | price_bars |
| 12 | F58 | LIQUIDITY_SHOCK | volume_zscore+range_zscore | RISK | -0.031 | verified | price_bars |
| 13 | F60 | INTRADAY_REVERSAL | -mean((close-open)/(high-low),3d) | ALPHA | 0.044 | verified | price_bars |
| 14 | F06 | FUNDAMENTAL_QUALITY | z(roe)+z(roa)+z(gm)+z(ocfps)-z(debt) | ALPHA | 0.051 | hypothesis | tushare |
| 15 | F15 | ACCRUALS_QUALITY | -|net_income-ocf|/total_assets | ALPHA | 0.047 | hypothesis | tushare |
| 16 | F12 | VALUE_COMPOSITE | -pe_ttm | ALPHA | 0.039 | hypothesis | tushare |

## B组 — 5 Cloud Migration Proxy Factors

| # | ID | Name | Formula | Direction | Proxy_For |
|---|-----|------|---------|-----------|-----------|
| 1 | F07 | PROFITABILITY_MOMENTUM | z(netprofit_yoy)+z(or_yoy)+z(delta_roe) | ALPHA | F07 canonical |
| 2 | F08 | CASH_FLOW_YIELD | ocf/total_mv | ALPHA | F08 canonical |
| 3 | F09 | EARNINGS_REVISION | guidance_direction*0.7+conservatism*0.3 | ALPHA | F09 canonical |
| 4 | F14 | ASSET_GROWTH_DISC | -or_yoy | ALPHA | F14 canonical |
| 5 | F44 | INVENTORY_HEALTH | -z(abnormal_inv_growth)+z(sell_through) | ALPHA | F44 canonical |

## C组 — 8 Candidate/Hypothesis Factors

| # | ID | Name | Formula | Direction | Status | Data_Source |
|---|-----|------|---------|-----------|--------|-------------|
| 1 | F34 | VOL_REGIME_SWITCH | vol_ratio(long/short)*regime_prediction | RISK | candidate | price_bars |
| 2 | F35 | INDUSTRY_NEUTRAL_TURNOVER | turnover_rate*sector_rank | ALPHA | candidate | price_bars |
| 3 | F57n | NORTHBOUND_FLOW | northbound_net_flow/total_mv | ALPHA | candidate | northbound |
| 4 | F22 | MARGIN_FINANCING | margin_change_5d/shares_outstanding | ALPHA | hypothesis | margin_data |
| 5 | F20n | SECTOR_MOMENTUM | sector_return_20d - market_return_20d | ALPHA | candidate | price_bars |
| 6 | F41n | CHAIN_POSITION | profit_capture+bottleneck+substitution | RISK | hypothesis | chain_data |
| 7 | F42n | CHAIN_EVIDENCE | L1*0.6+L2*0.3+L3*0.1-L5*0.5 | RISK | hypothesis | chain_data |
| 8 | F46 | PRICE_TRANSMISSION | gross_margin_yoy | ALPHA | hypothesis | tushare |

## 16 Primitive Factors

| # | Primitive | Group | Suggested_Absorb_Into |
|---|-----------|-------|-----------------------|
| 1 | turnover_rate | A | F54_CROWDING_RISK, F56_MONEY_FLOW |
| 2 | range_5d | A | F31_DOWNSIDE_TAIL, F58_LIQUIDITY_SHOCK |
| 3 | vol_20d | A | F10_LOW_VOLATILITY |
| 4 | ma20_dev | A | F21_TREND_PERSISTENCE |
| 5 | ma60_dev | A | F04_RESIDUAL_MOMENTUM, F21_TREND_PERSISTENCE |
| 6 | vol_climax | A | F53_ATTENTION_SPIKE |
| 7 | upper_shadow | A | F31_DOWNSIDE_TAIL, F58_LIQUIDITY_SHOCK |
| 8 | vol_ratio | A | F53_ATTENTION_SPIKE, F54_CROWDING_RISK, F56_MONEY_FLOW |
| 9 | mom_5d | A | F11_SHORT_TERM_REVERSAL |
| 10 | mom_10d | A | F11_SHORT_TERM_REVERSAL |
| 11 | mom_20d | A | F04_RESIDUAL_MOMENTUM |
| 12 | mom_60d | A | F04_RESIDUAL_MOMENTUM |
| 13 | pb_inv | A | F12_VALUE_COMPOSITE |
| 14 | pe_inv | A | F12_VALUE_COMPOSITE |
| 15 | pos_20d | A | F21_TREND_PERSISTENCE, F54_CROWDING_RISK |
| 16 | northbound_net_flow | B | F57_NORTHBOUND_FLOW_PRESSURE |
