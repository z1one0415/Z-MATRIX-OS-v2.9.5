"""Cap OS Runtime Config — default disabled, strict bool True only."""
import os as _os

class RuntimeConfig:
    def __init__(self, source=None):
        self.runtime_enabled = False
        self.adapter_execution_enabled = False
        self.capability_execution_enabled = False
        if isinstance(source, dict):
            for k in ("CAPABILITY_OS_RUNTIME_ENABLED", "ADAPTER_EXECUTION_ENABLED", "CAPABILITY_EXECUTION_ENABLED"):
                v = source.get(k, False)
                setattr(self, k.lower().replace("capability_os_",""), v if isinstance(v, bool) and v is True else False)

def load_config(source=None): return RuntimeConfig(source) if isinstance(source, dict) else RuntimeConfig()
def is_runtime_enabled(config): return getattr(config, "runtime_enabled", False) is True
def is_adapter_execution_enabled(config): return getattr(config, "adapter_execution_enabled", False) is True
def is_capability_execution_enabled(config): return getattr(config, "capability_execution_enabled", False) is True
def env_override_detected():
    for k in ("CAPABILITY_OS_RUNTIME_ENABLED", "ADAPTER_EXECUTION_ENABLED", "CAPABILITY_EXECUTION_ENABLED"):
        v = _os.environ.get(k)
        if v and v.lower() in ("true","1","yes","on"): return True
    return False
