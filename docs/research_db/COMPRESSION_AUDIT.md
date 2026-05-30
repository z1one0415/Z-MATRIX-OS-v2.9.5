# Research OS V3 Compression Audit

Generated: 2026-05-30T11:29:07.101363+00:00

## Module Classification

| Package | Modules | Status | Rationale |
|---------|:--:|:--:|------|
| account_truth | ['account_truth/account_reconciler.py', 'account_truth/account_snapshot_normalizer.py', 'account_truth/account_truth_report.py', 'account_truth/capital_curve_builder.py', 'account_truth/cashflow_normalizer.py', 'account_truth/drawdown_calculator.py', 'account_truth/holding_pnl_builder.py', 'account_truth/import_audit.py', 'account_truth/missing_data_detector.py', 'account_truth/position_normalizer.py', 'account_truth/raw_import_schema.py', 'account_truth/trade_normalizer.py', 'account_truth/trade_quality_checker.py'] | CORE | Research pipeline essential |
| attribution | ['attribution/attribution_engine.py', 'attribution/attribution_packet.py', 'attribution/attribution_report.py', 'attribution/cost_attribution.py', 'attribution/outcome_reason_engine.py'] | CORE | Research pipeline essential |
| council | ['council/base_reviewer.py', 'council/consensus_engine.py', 'council/council_aggregator.py', 'council/council_packet.py', 'council/devil_reviewer.py', 'council/research_verdict.py', 'council/reviewers.py'] | CORE | Research pipeline essential |
| market_data | ['market_data/adjustment_factor_store.py', 'market_data/alpha_engine.py', 'market_data/benchmark_registry.py', 'market_data/market_data_guardrail.py', 'market_data/market_schema.py', 'market_data/net_return_engine.py', 'market_data/outcome_fixture_builder.py', 'market_data/outcome_horizon_engine.py', 'market_data/outcome_readiness_gate.py', 'market_data/outcome_schema.py', 'market_data/price_bar_store.py', 'market_data/return_engine.py', 'market_data/trading_calendar.py', 'market_data/trading_cost_engine.py'] | CORE | Research pipeline essential |
| master_data | ['master_data/alias_resolver.py', 'master_data/chain_node_mapper.py', 'master_data/chain_taxonomy.py', 'master_data/coverage_report.py', 'master_data/exchange_board_classifier.py', 'master_data/import_audit.py', 'master_data/industry_taxonomy.py', 'master_data/mapping_integrity_checker.py', 'master_data/mapping_snapshot.py', 'master_data/master_data_report.py', 'master_data/master_schema.py', 'master_data/sector_mapper.py', 'master_data/security_master.py', 'master_data/ticker_identity_resolver.py'] | CORE | Research pipeline essential |
| outcome_engine | ['outcome_engine/alpha_calculator.py', 'outcome_engine/forward_horizon.py', 'outcome_engine/outcome_schema.py'] | CORE | Research pipeline essential |
| replay | ['replay/experiment_registry.py', 'replay/replay_audit.py', 'replay/replay_dataset.py', 'replay/replay_manifest.py', 'replay/replay_report.py', 'replay/replay_runner.py'] | CORE | Research pipeline essential |
| alpha_factory | ['alpha_factory/alpha_ledger.py', 'alpha_factory/candidate_factor_generator.py', 'alpha_factory/factor_genome.py', 'alpha_factory/factor_graveyard.py', 'alpha_factory/factor_promotion.py', 'alpha_factory/factor_validator.py'] | OPTIONAL | Validation/enrichment layer |
| cockpit | ['cockpit/research_audit.py', 'cockpit/research_manifest.py', 'cockpit/research_packet.py', 'cockpit/research_pipeline.py', 'cockpit/research_session.py'] | OPTIONAL | Validation/enrichment layer |
| data_supply | ['data_supply/connector_registry.py', 'data_supply/corporate_actions.py', 'data_supply/data_lineage.py', 'data_supply/pit_store.py', 'data_supply/source_reliability.py'] | OPTIONAL | Validation/enrichment layer |
| decision_intelligence | ['decision_intelligence/decision_ledger.py', 'decision_intelligence/forecaster_score.py', 'decision_intelligence/prediction_tracker.py', 'decision_intelligence/thesis_library.py', 'decision_intelligence/v2/decision_v2_engine.py', 'decision_intelligence/v2/decision_v2_ledger.py', 'decision_intelligence/v2/decision_v2_report.py'] | OPTIONAL | Validation/enrichment layer |
| factor_foundation | ['factor_foundation/factor_metrics.py', 'factor_foundation/factor_report.py', 'factor_foundation/factor_snapshot.py'] | OPTIONAL | Validation/enrichment layer |
| portfolio | ['portfolio/marketplace.py', 'portfolio/portfolio_factory.py', 'portfolio/portfolio_ledger.py', 'portfolio/portfolio_validator.py'] | OPTIONAL | Validation/enrichment layer |
| portfolio_reality | ['portfolio_reality/portfolio_audit.py', 'portfolio_reality/portfolio_capacity.py', 'portfolio_reality/portfolio_drift.py', 'portfolio_reality/portfolio_liquidity.py', 'portfolio_reality/portfolio_report.py', 'portfolio_reality/portfolio_snapshot.py'] | OPTIONAL | Validation/enrichment layer |
| proving_ground | ['proving_ground/capacity_calibration.py', 'proving_ground/historical_reality_pack.py', 'proving_ground/regime_expansion.py', 'proving_ground/research_championship.py', 'proving_ground/turnover_reality.py', 'proving_ground/walk_forward_certifier.py'] | OPTIONAL | Validation/enrichment layer |
| validation | ['validation/alpha_stability_lab.py', 'validation/factor_decay_observatory.py', 'validation/portfolio_drift_engine.py', 'validation/regime_robustness.py', 'validation/research_truth_ledger.py'] | OPTIONAL | Validation/enrichment layer |
| validation_factory | ['validation_factory/capacity_engine.py', 'validation_factory/expanding_window_engine.py', 'validation_factory/paper_account.py', 'validation_factory/paper_fill_simulator.py', 'validation_factory/paper_nav_engine.py', 'validation_factory/paper_order_engine.py', 'validation_factory/paper_position_engine.py', 'validation_factory/regime_validation.py', 'validation_factory/rolling_window_engine.py', 'validation_factory/stress_lab.py', 'validation_factory/turnover_lab.py', 'validation_factory/walk_forward_runner.py'] | OPTIONAL | Validation/enrichment layer |
| root | ['data_source_capability.py', 'directory_registry.py', 'no_production_boundary.py', 'outcome_horizon_policy.py', 'pit_policy.py', 'promotion_policy.py', 'research_db_status.py', 'trust_level.py'] | SPECIALIZED | Advanced features |
| evolution | ['evolution/graph/entity_registry.py', 'evolution/graph/graph_query.py', 'evolution/graph/knowledge_graph.py', 'evolution/graph/relationship_engine.py', 'evolution/hypothesis/hypothesis_evolution.py', 'evolution/hypothesis/hypothesis_mutator.py', 'evolution/hypothesis/hypothesis_selector.py', 'evolution/meta/research_analyzer.py', 'evolution/meta/research_efficiency.py', 'evolution/meta/research_failure_engine.py', 'evolution/mining/pattern_miner.py', 'evolution/mining/pattern_ranker.py', 'evolution/mining/pattern_validator.py'] | SPECIALIZED | Advanced features |
| outcome_reality | ['outcome_reality/outcome_audit.py', 'outcome_reality/outcome_integrity.py', 'outcome_reality/outcome_report.py', 'outcome_reality/outcome_snapshot.py', 'outcome_reality/outcome_universe.py'] | SPECIALIZED | Advanced features |
| rol | ['rol/memory/lesson_extractor.py', 'rol/memory/memory_bank.py', 'rol/memory/pattern_library.py', 'rol/monitor/alert_engine.py', 'rol/monitor/monitor_engine.py', 'rol/monitor/threshold_registry.py', 'rol/registry/research_archive.py', 'rol/registry/research_registry.py', 'rol/registry/research_search.py', 'rol/registry/research_state_machine.py', 'rol/workflow/workflow_audit.py', 'rol/workflow/workflow_engine.py', 'rol/workflow/workflow_template.py'] | SPECIALIZED | Advanced features |

## Summary
- CORE: 7 packages (research pipeline backbone)
- OPTIONAL: 10 packages (enrichment/validation)
- SPECIALIZED: 4 packages (advanced features)

## Compression Recommendation
- No modules currently DEPRECATED
- Consider merging: validation + validation_factory + proving_ground → unified validation layer
- Golden Path uses only CORE packages → minimal viable Research OS = {CORE} packages
