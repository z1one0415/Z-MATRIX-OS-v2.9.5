"""Z9 Review Node registry — P0 static placeholder."""

def list_registered_z9_review_nodes() -> list:
    return []

def get_z9_review_node_registry_status() -> dict:
    return {"status": "DISABLED_DEFAULT_P0", "registered_nodes": 0}

def register_z9_review_node(name=None, node_instance=None) -> None:
    return None
