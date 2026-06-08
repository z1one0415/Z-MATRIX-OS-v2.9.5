from skillos.capability_invocation_os.adapters.wave0.config import load,is_wave0_enabled,is_github_readonly_enabled,is_document_generation_enabled,is_local_docs_inspection_enabled,is_report_reading_enabled
from skillos.capability_invocation_os.adapters.wave0.kill_switch import ks
class TestDisabled:
    def test_disabled(self):
        c=load(); assert is_wave0_enabled(c) is False; assert is_github_readonly_enabled(c) is False; assert is_document_generation_enabled(c) is False; assert is_local_docs_inspection_enabled(c) is False; assert is_report_reading_enabled(c) is False
    def test_kill_switch(self):
        k = ks()
        assert k.master is True
