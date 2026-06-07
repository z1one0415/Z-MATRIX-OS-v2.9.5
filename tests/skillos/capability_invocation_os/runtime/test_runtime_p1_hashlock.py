from skillos.capability_invocation_os.runtime.hashlock import stable_hash_dict, stable_hash_text, verify_hash
class TestP1Hashlock:
    def test_stable(self): assert stable_hash_dict({"a":1}) == stable_hash_dict({"a":1})
    def test_different(self): assert stable_hash_dict({"a":1}) != stable_hash_dict({"b":2})
    def test_text(self): assert stable_hash_text("hello") == stable_hash_text("hello")
    def test_verify(self): h=stable_hash_text("test"); assert verify_hash(h,h) is True; assert verify_hash(h,"bad") is False
