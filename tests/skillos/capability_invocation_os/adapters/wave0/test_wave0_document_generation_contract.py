from skillos.capability_invocation_os.adapters.wave0.document_generation import DocumentGenerationAdapterSkeleton
class TestDocGen:
    def test_outputs(self): o=DocumentGenerationAdapterSkeleton().supported_future_outputs(); assert "markdown" in o; assert "filesystem_write" not in o
    def test_deny(self): assert DocumentGenerationAdapterSkeleton().deny().action=="DENY"
