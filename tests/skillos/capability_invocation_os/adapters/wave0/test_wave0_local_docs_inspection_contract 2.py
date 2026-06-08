from skillos.capability_invocation_os.adapters.wave0.local_docs_inspection import LocalDocsInspectionAdapterSkeleton
class TestDocs:
    def test_future(self): a=LocalDocsInspectionAdapterSkeleton().supported_future_actions(); assert "read_docs" in a; assert "file_mutation" not in a
    def test_deny(self): assert LocalDocsInspectionAdapterSkeleton().deny().action=="DENY"
