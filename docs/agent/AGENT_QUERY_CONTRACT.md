# Agent Query Contract

## Query Functions
- get_research_summary() — compact system summary
- get_layer_versions() — all layer version hashes
- get_changed_layers(since_versions) — diff
- get_layer_slice(layer_ids, limit=100) — targeted read
- query_case(case_id)
- query_event_window(target_id, start, end)
- query_factor(factor_id)
- query_hypotheses(filters)

## Token Budget Rules
- Full scan forbidden by default
- Default limit <= 100
- Every query returns token_estimate
- Over budget → NEED_NARROWER_QUERY
