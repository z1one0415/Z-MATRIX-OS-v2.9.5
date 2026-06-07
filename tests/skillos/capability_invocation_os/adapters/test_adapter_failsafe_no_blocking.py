from skillos.capability_invocation_os.adapters.failsafe import degrade_to_no_adapter, degrade_to_docs_only, degrade_to_manual_review, deny_adapter_execution
class TestAdapterFailsafeNoBlocking:
    def test_no_adapter(self): assert degrade_to_no_adapter().action == "DENY_NOOP"
    def test_docs_only(self): assert degrade_to_docs_only().action == "DEGRADE_DOCS_ONLY"
    def test_manual_review(self): assert degrade_to_manual_review().action == "DEGRADE_MANUAL_REVIEW"
    def test_deny_execution(self): assert deny_adapter_execution().action == "DENY"
    def test_none_blocked(self):
        for r in [degrade_to_no_adapter(),degrade_to_docs_only(),degrade_to_manual_review(),deny_adapter_execution()]: assert r.action != "BLOCKED"
