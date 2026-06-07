from skillos.capability_invocation_os.adapters.wave0.github_readonly import GitHubReadOnlyAdapterSkeleton
class TestGitHub:
    def test_future_actions(self): a=GitHubReadOnlyAdapterSkeleton().supported_future_actions(); assert "fetch_file" in a; assert "merge_branch" not in a
    def test_forbidden(self): f=GitHubReadOnlyAdapterSkeleton().forbidden_actions(); assert "create_file" in f; assert "delete_file" in f
    def test_deny(self): assert GitHubReadOnlyAdapterSkeleton().deny().action=="DENY"
    def test_no_write(self): assert "create_file" not in GitHubReadOnlyAdapterSkeleton().supported_future_actions()
