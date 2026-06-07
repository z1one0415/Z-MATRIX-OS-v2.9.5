import pytest
from skillos.capability_invocation_os.runtime.config import load_config, RuntimeConfig, env_override_detected
from skillos.capability_invocation_os.runtime.router import route
from skillos.capability_invocation_os.runtime.models import InvocationRequest
from skillos.capability_invocation_os.runtime.guard import run_guard_pipeline
from skillos.capability_invocation_os.runtime.kill_switch import kill_switch

class TestRuntimeDisabledDefault:
    def test_config_default_disabled(self):
        cfg = load_config(None)
        assert cfg.runtime_enabled is False
        assert cfg.adapter_execution_enabled is False
        assert cfg.capability_execution_enabled is False
    def test_non_bool_disabled(self):
        cfg = load_config({"CAPABILITY_OS_RUNTIME_ENABLED": 1})
        assert cfg.runtime_enabled is False
    def test_env_override_not_enabling(self):
        assert env_override_detected() is False
    def test_router_denies_by_default(self):
        r = route(InvocationRequest())
        assert r.action == "DENY"
    def test_guard_continues_disabled(self):
        r = run_guard_pipeline(InvocationRequest())
        assert r.action == "CONTINUE"
    def test_kill_switch_all_disabled(self):
        assert kill_switch.master_disable is True
