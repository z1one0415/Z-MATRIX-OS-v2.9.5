"""Cap OS Runtime Config — all enabled functions return False in current phase.
Strict True requests are recorded but NEVER enable runtime.
Kill switch always overrides. No env override bypass."""
import os as _os

class RuntimeConfig:
    def __init__(self, source=None):
        self._runtime_requested = False
        self._adapter_execution_requested = False
        self._capability_execution_requested = False
        if isinstance(source, dict):
            for flag, key in [
                ("_runtime_requested", "CAPABILITY_OS_RUNTIME_ENABLED"),
                ("_adapter_execution_requested", "ADAPTER_EXECUTION_ENABLED"),
                ("_capability_execution_requested", "CAPABILITY_EXECUTION_ENABLED"),
            ]:
                v = source.get(key, False)
                setattr(self, flag, v if isinstance(v, bool) and v is True else False)

def load_config(source=None):
    return RuntimeConfig(source) if isinstance(source, dict) else RuntimeConfig()

def is_runtime_requested(config):
    try: return getattr(config, "_runtime_requested", False) is True
    except: return False

def is_adapter_execution_requested(config):
    try: return getattr(config, "_adapter_execution_requested", False) is True
    except: return False

def is_capability_execution_requested(config):
    try: return getattr(config, "_capability_execution_requested", False) is True
    except: return False

def is_runtime_enabled(config):
    return False

def is_adapter_execution_enabled(config):
    return False

def is_capability_execution_enabled(config):
    return False

def env_override_detected():
    for k in ("CAPABILITY_OS_RUNTIME_ENABLED", "ADAPTER_EXECUTION_ENABLED", "CAPABILITY_EXECUTION_ENABLED"):
        v = _os.environ.get(k)
        if v and v.lower() in ("true","1","yes","on"):
            return True
    return False
