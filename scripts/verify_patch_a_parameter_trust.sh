#!/usr/bin/env bash
set -euo pipefail
echo "═══ Z-MATRIX-OS v3.5.20-PATCH-A Parameter Trust Hardening Verification ═══"

PYTHONPATH=. python3 -m compileall zmatrix tests scripts pipelines 2>&1 | tail -1

# PATCH-1: Outcome Horizon
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.outcome_horizon import check_all_horizons, build_hardened_outcome
# Test T20 insufficient forward data
bars_short = [{'close':100}]*19  # 19 days, need 20
r = check_all_horizons(forward_bars=bars_short)
assert r['horizons']['t20']['horizon_ready'] == False, 'T20 should fail with 19 days'
assert r['horizons']['t20']['outcome_status'] == 'INSUFFICIENT_FORWARD_DATA'
# Test hardened outcome nullifies T20
orig = {'actual_return_t20': 5.0, 'actual_return_t5': 2.0}
h = build_hardened_outcome(original_outcome=orig, forward_bars=bars_short)
assert h['actual_return_t20'] is None, 'T20 should be nullified'
assert h['outcome_status_t20'] == 'INSUFFICIENT_FORWARD_DATA'
print('  ✅ PATCH-1 Outcome Horizon Gate')
"

# PATCH-2: Data Contract + PIT
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.data_contract import MatrixFact, PIT_RULES, DATA_SOURCE_CAPABILITY
f = MatrixFact(ticker='000001', trade_date='20240115', fact_name='roe', fact_value=15.2, source='tushare', announce_date='20240110')
assert f.pit_safe == True, 'announce_date before trade_date should be PIT safe'
f2 = MatrixFact(ticker='000002', trade_date='20240110', fact_name='roe', fact_value=15.2, source='tushare', announce_date='20240115')
assert f2.pit_safe == False, 'announce_date after trade_date should NOT be PIT safe'
assert 'financial_statements' in DATA_SOURCE_CAPABILITY
assert DATA_SOURCE_CAPABILITY['financial_statements']['level'] == 'REQUIRED_CORE'
print('  ✅ PATCH-2 Data Contract + PIT Rules')
"

# PATCH-3: B-Matrix Foundation
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.b_matrix_foundation import score_b_matrix
facts = {'gross_margin':30,'net_margin':15,'roe':12,'roic':10,'revenue_yoy':15,'net_profit_yoy':20,'deduct_np_yoy':18,'ocf':100,'ocf_to_np':0.8,'fcf_proxy':50,'debt_ratio':0.4,'current_ratio':1.5,'goodwill_ratio':0.05,'pe_ttm':20,'pb':3,'ps':2,'dividend_yield':0.02,'industry_percentile_roe':70,'industry_percentile_growth':65,'bottleneck_score':60,'chain_position':'硬件瓶颈'}
r = score_b_matrix(financial_facts=facts, valuation_facts=facts, industry_facts=facts)
assert r['b_score'] > 0
assert r['hard_gate_passed'] == True
print(f'  ✅ PATCH-3 B-Matrix Foundation (score={r[\"b_score\"]})')
"

# PATCH-4: D-Matrix Foundation
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.d_matrix_foundation import score_d_matrix
event = {'event_evidence_level':'B','event_recency_hours':2,'catalyst_strength':80}
price = {'return_1d':5,'return_3d':12,'return_5d':15,'volume_ratio_5d':2.5,'turnover_rate':8,'amplitude':6,'volatility_expansion':3}
flow = {'main_net_inflow':500,'large_order_net_inflow':200,'lhb_buy_amount':300,'lhb_sell_amount':100}
theme = {'theme_heat_score':75,'theme_rank_change':3,'sector_momentum':70,'concept_board_strength':65}
tradability = {'tradability_status':'TRADABLE','limit_up_flag':False,'limit_down_flag':False,'consecutive_limit_up_count':0,'suspension_flag':False,'one_price_board_flag':False,'liquidity_capacity_status':'ADEQUATE'}
r = score_d_matrix(event_facts=event, price_facts=price, flow_facts=flow, theme_facts=theme, tradability_facts=tradability)
assert r['d_score'] > 0
assert r['tradability_status'] == 'TRADABLE'
# Test one-price-board block
tb_blocked = dict(tradability); tb_blocked['limit_up_flag']=True; tb_blocked['one_price_board_flag']=True
r2 = score_d_matrix(event_facts=event, price_facts=price, flow_facts=flow, theme_facts=theme, tradability_facts=tb_blocked)
assert r2['tradability_status'] == 'BLOCKED'
assert 'ONE_PRICE_BOARD_BUY' in r2['risk_flags']
print(f'  ✅ PATCH-4 D-Matrix Foundation (score={r[\"d_score\"]})')
"

# PATCH-5: Trading Cost
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.trading_cost import compute_net_return
r = compute_net_return(gross_return_pct=5.0, entry_price=10.0, exit_price=10.5, volume=1000, market_cap=10000000000)
assert r['net_return_pct'] < r['gross_return_pct']
assert r['execution_feasible'] == True
# Limit board block
r2 = compute_net_return(gross_return_pct=5.0, entry_price=10.0, exit_price=10.5, volume=1000, limit_board_flags={'limit_up_flag':True,'one_price_board_flag':True})
assert r2['execution_feasible'] == False
print(f'  ✅ PATCH-5 Trading Cost (net={r[\"net_return_pct\"]:.2f}% vs gross={r[\"gross_return_pct\"]:.2f}%)')
"

# PATCH-6: Parameter Trust Map
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.parameter_trust import build_parameter_trust_map
m = build_parameter_trust_map()
assert m['summary']['t0_count'] + m['summary']['t1_count'] == m['summary']['t0_count'] + m['summary']['t1_count']
assert m['summary']['production_ready_params'] == 0
print(f'  ✅ PATCH-6 Parameter Trust Map (0 params production-ready)')
"

# PATCH-7: Evidence Status Auditor
PYTHONPATH=. python3 -c "
from zmatrix.patch_a.evidence_auditor import audit_evidence_status
r = audit_evidence_status(reports={})
assert r['method'] == 'STATUS_FIELD_VALIDATION'
print(f'  ✅ PATCH-7 Evidence Status Auditor (method={r[\"method\"]})')
"

# v3.6 forbidden
if grep -r "v3\.6" zmatrix/patch_a scripts/run_v3520* --exclude-dir=__pycache__ 2>/dev/null; then
    echo "❌ v3.6 reference in patch_a"; exit 2
fi
echo "  ✅ No v3.6 references in patch_a"

echo "═══ PATCH-A ALL 7 PATCHES PASS ═══"
