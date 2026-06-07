"""Capability Invocation OS Runtime Config — default disabled."""
class RuntimeConfig:
    def __init__(self, source=None):
        self.runtime_enabled = False
        self.adapter_execution_enabled = False
        self.capability_execution_enabled = False
        if isinstance(source, dict):
            for k in ("CAPABILITY_OS_RUNTIME_ENABLED", "ADAPTER_EXECUTION_ENABLED", "CAPABILITY_EXECUTION_ENABLED"):
                v = source.get(k, False)
                setattr(self, k.lower().replace("capability_os_",""), v is True if isinstance(v, bool) else False)

def load_config(source=None):
    cfg = RuntimeConfig(source)
    if source is None or not isinstance(source, dict):
        return RuntimeConfig()
    return cfg

def env_override_detected():
    import os
    for k in ("CAPABILITY_OS_RUNTIME_ENABLED", "ADAPTER_EXECUTION_ENABLED", "CAPABILITY_EXECUTION_ENABLED"):
        v = os.environ.get(k)
        if v and v.lower() in ("true","1","yes","on"):
            return True
    return False
