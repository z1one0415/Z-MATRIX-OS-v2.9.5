# Research OS V3 Capability Map

Generated: 2026-05-30T11:29:07.101363+00:00
Packages: 21 | Modules: 160

## Package Dependency Matrix

| Package | Modules | LOC | Key Modules | Dependencies |
|---------|:--:|:--:|------|------|
| account_truth | 13 | 457 | account_reconciler, account_snapshot_normalizer, account_truth_report, capital_curve_builder, cashflow_normalizer +8 |  |
| alpha_factory | 6 | 230 | alpha_ledger, candidate_factor_generator, factor_genome, factor_graveyard, factor_promotion +1 |  |
| attribution | 5 | 230 | attribution_engine, attribution_packet, attribution_report, cost_attribution, outcome_reason_engine |  |
| cockpit | 5 | 161 | research_audit, research_manifest, research_packet, research_pipeline, research_session |  |
| council | 7 | 227 | base_reviewer, consensus_engine, council_aggregator, council_packet, devil_reviewer +2 | from  |
| data_supply | 5 | 289 | connector_registry, corporate_actions, data_lineage, pit_store, source_reliability |  |
| decision_intelligence | 7 | 262 | decision_ledger, forecaster_score, prediction_tracker, thesis_library, v2/decision_v2_engine +2 | from  |
| evolution | 13 | 265 | graph/entity_registry, graph/graph_query, graph/knowledge_graph, graph/relationship_engine, hypothesis/hypothesis_evolution +8 | from  |
| factor_foundation | 3 | 179 | factor_metrics, factor_report, factor_snapshot |  |
| market_data | 14 | 595 | adjustment_factor_store, alpha_engine, benchmark_registry, market_data_guardrail, market_schema +9 |  |
| master_data | 14 | 1206 | alias_resolver, chain_node_mapper, chain_taxonomy, coverage_report, exchange_board_classifier +9 |  |
| outcome_engine | 3 | 154 | alpha_calculator, forward_horizon, outcome_schema | market_data |
| outcome_reality | 5 | 708 | outcome_audit, outcome_integrity, outcome_report, outcome_snapshot, outcome_universe |  |
| portfolio | 4 | 144 | marketplace, portfolio_factory, portfolio_ledger, portfolio_validator |  |
| portfolio_reality | 6 | 620 | portfolio_audit, portfolio_capacity, portfolio_drift, portfolio_liquidity, portfolio_report +1 |  |
| proving_ground | 6 | 263 | capacity_calibration, historical_reality_pack, regime_expansion, research_championship, turnover_reality +1 |  |
| replay | 6 | 194 | experiment_registry, replay_audit, replay_dataset, replay_manifest, replay_report +1 |  |
| rol | 13 | 298 | memory/lesson_extractor, memory/memory_bank, memory/pattern_library, monitor/alert_engine, monitor/monitor_engine +8 |  |
| root | 8 | 379 | data_source_capability, directory_registry, no_production_boundary, outcome_horizon_policy, pit_policy +3 |  |
| validation | 5 | 242 | alpha_stability_lab, factor_decay_observatory, portfolio_drift_engine, regime_robustness, research_truth_ledger |  |
| validation_factory | 12 | 404 | capacity_engine, expanding_window_engine, paper_account, paper_fill_simulator, paper_nav_engine +7 | from  |

## Architecture Layers

```
Layer 6: Evolution — hypothesis_evolution, pattern_mining, meta_research
Layer 5: Operations (ROL) — registry, monitor, workflow, memory
Layer 4: Decision Intelligence — thesis, decision, prediction, forecaster, v2 market/calibration
Layer 3: Portfolio — factory, reality(capacity/liquidity/drift), validation
Layer 2: Research — account_truth, master_data, market_data, outcome, attribution, replay
Layer 1: Foundation — council, alpha_factory, factor_foundation, cockpit
Layer 0: Governance — constitution, policies, guardrails
```

## Input→Output Chain
| Module | Input | Output |
|--------|-------|--------|
| account_truth | Trade CSV | Capital curve, PnL ledger |
| master_data | Security CSV | SecurityMaster, Industry mapping |
| market_data | Price CSV | DailyPriceBar, TradingCalendar |
| outcome_engine | Signal date + Calendar | T20/T60 readiness |
| attribution | Gross return + benchmark | Market/Industry/Selection alpha |
| replay | Dataset slices | ReplayResult + audit hash |
| council | Experiment context | CouncilDecision + minority report |
| decision_v2 | Prediction entries | PredictionMarket + Calibration + Ranking |
| evolution | Entity graph | Pattern discovery + Hypothesis mutation |