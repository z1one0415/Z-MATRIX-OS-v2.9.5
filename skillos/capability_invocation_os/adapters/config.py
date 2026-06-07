"""Adapter Framework Config — all enabled functions return False."""
class AdapterConfig:
    def __init__(self,source=None):
        self._framework_requested=False; self._registration_requested=False; self._execution_requested=False; self._zmatrix_adapters_requested=False
        if isinstance(source,dict):
            for flag,key in [("_framework_requested","ADAPTER_FRAMEWORK_ENABLED"),("_registration_requested","ADAPTER_REGISTRATION_ENABLED"),("_execution_requested","ADAPTER_EXECUTION_ENABLED"),("_zmatrix_adapters_requested","ZMATRIX_MODULE_ADAPTERS_ENABLED")]:
                v=source.get(key,False); setattr(self,flag,v if isinstance(v,bool) and v is True else False)
def load_config(s=None): return AdapterConfig(s) if isinstance(s,dict) else AdapterConfig()
def is_requested(flag,c): return getattr(c,flag,False) is True if c else False
def is_adapter_framework_enabled(c): return False
def is_adapter_registration_enabled(c): return False
def is_adapter_execution_enabled(c): return False
def is_zmatrix_module_adapters_enabled(c): return False
def env_override_detected():
    import os as _o
    for k in ("ADAPTER_FRAMEWORK_ENABLED","ADAPTER_REGISTRATION_ENABLED","ADAPTER_EXECUTION_ENABLED","ZMATRIX_MODULE_ADAPTERS_ENABLED"):
        v=_o.environ.get(k)
        if v and v.lower() in ("true","1","yes","on"): return True
    return False
