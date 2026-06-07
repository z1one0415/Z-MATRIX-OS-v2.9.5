from skillos.capability_invocation_os.adapters.wave0.failsafe import degrade_to_noop,degrade_to_plan_only,degrade_to_manual_review,deny_wave0_adapter
class TestFailsafe:
    def test_noop(self): assert degrade_to_noop().action=="DENY_NOOP"
    def test_no_blocking(self):
        for r in [degrade_to_noop(),degrade_to_plan_only(),degrade_to_manual_review(),deny_wave0_adapter()]: assert r.action != "BLOCKED"
