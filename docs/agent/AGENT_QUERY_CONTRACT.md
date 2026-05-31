# Agent Query Contract

## Functions
get_research_summary() | get_layer_versions() | get_changed_layers() | get_layer_slice() | query_case() | query_event_window() | query_factor() | query_hypotheses()

## Token Budget Rules
- Full scan forbidden by default | Default limit <= 100
- Every query returns token_estimate | Over budget → NEED_NARROWER_QUERY
