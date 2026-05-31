# Z-G16 v3 Query Bridge Closeout

Final Status: G16_3_QUERY_BRIDGE_READY

## Bridge Functions (8)
get_zg16_research_summary | get_zg16_layer_versions | get_zg16_changed_layers
get_zg16_layer_slice | get_zg16_source_health | get_zg16_source_attribution
get_zg16_all_sources | get_zg16_source_readiness

## Unified Envelope
All responses: {status, quality_status, production_allowed:false, external_api_used:false, shadowbroker_deployed:false, token_estimate, data}

## Source Readiness
SOURCE_READY | DATA_SOURCE_BLOCKED | LICENSE_REVIEW_REQUIRED | SOURCE_NOT_REGISTERED

## Gates
limit <= 100 enforced | source_unusable → DATA_SOURCE_BLOCKED | license_unknown → LICENSE_REVIEW_REQUIRED

## Test Matrix
tests/research_db/zg16: 6 tests (envelope, limit, source readiness ×4)

## Safety
External API: FALSE | ShadowBroker: FALSE | Production: BLOCKED
Runtime Ledgers: EMPTY

## Known Limitations
- Bridge is STUB: returns fixture/schema data only, no live aggregation
- Source readiness uses local JSONL/CSV, needs DB for production

## Next Allowed
G16-4: Agent Skill Invocation Bridge (invoke_skill → G16 wrappers)

## Forbidden
External API | ShadowBroker deploy | Production | Broker/runtime | Real trade
