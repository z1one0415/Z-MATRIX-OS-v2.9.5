import pytest
from skillos.capability_invocation_os.runtime.config import load_config, is_runtime_requested, is_runtime_enabled, env_override_detected
from skillos.capability_invocation_os.runtime.router import route
from skillos.capability_invocation_os.runtime.models import InvocationRequest
from skillos.capability_invocation_os.runtime.guard import run_guard_pipeline
from skillos.capability_invocation_os.runtime.kill_switch import kill_switch
class TestRuntimeDisabledDefault:
    def test_runtime_never_enabled(self): assert is_runtime_enabled(load_config(None)) is False
    def test_non_bool_requested_false(self): c=load_config({"CAPABILITY_OS_RUNTIME_ENABLED":1}); assert is_runtime_requested(c) is False
    def test_env_override_not_enabling(self): assert env_override_detected() is False
    def test_router_denies_by_default(self): r=route(InvocationRequest()); assert r.action=="DENY"
    def test_guard_continues_disabled(self): r=run_guard_pipeline(InvocationRequest()); assert r.action=="CONTINUE"
    def test_kill_switch_all_disabled(self): assert kill_switch.master_disable is True
