"""Registry — P0: no real scan. Returns empty/placeholder."""
from typing import List, Dict

def list_registered_factor_adapters() -> List[str]:
    return ["factor_library_readonly_adapter_p0"]

def get_factor_adapter_registry_status() -> Dict[str, str]:
    return {"factor_library_readonly_adapter_p0": "disabled_default"}

def register_factor_library_adapter(*args, **kwargs) -> None:
    return None
