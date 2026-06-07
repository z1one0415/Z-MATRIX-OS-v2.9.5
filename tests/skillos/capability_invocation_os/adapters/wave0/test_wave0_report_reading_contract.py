from skillos.capability_invocation_os.adapters.wave0.report_reading import ReportReadingAdapterSkeleton
class TestReport:
    def test_future(self): a=ReportReadingAdapterSkeleton().supported_future_actions(); assert "parse_report" in a; assert "report_write" not in a
    def test_deny(self): assert ReportReadingAdapterSkeleton().deny().action=="DENY"
