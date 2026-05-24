"""G14 Global Baseline adapter — provenance only, not decision authority."""
def load_g14_signal(ticker=None):
    return {"source": "Z-G14", "available": False, "role": "GLOBAL_BASELINE_ONLY",
            "not_duplicate_selection": True, "rank_bucket": None, "global_rank": None,
            "warnings": []}
