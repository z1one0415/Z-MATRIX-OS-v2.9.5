"""G14 Global Baseline Adapter — provenance only, not duplicate selection."""
def load_g14_baseline() -> dict:
    return {
        "source": "Z-G14", "available": False,
        "role": "GLOBAL_BASELINE_ONLY", "not_duplicate_selection": True,
        "universe_contract": {}, "global_rank": None, "rank_bucket": "UNKNOWN",
    }
