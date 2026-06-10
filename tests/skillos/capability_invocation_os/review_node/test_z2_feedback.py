"""Tests for Z2 feedback."""
from skillos.capability_invocation_os.review_node.models import Z2FeedbackCandidate
from skillos.capability_invocation_os.review_node.z2_feedback import build_z2_feedback_candidate

def test_feedback_builds():
    feedback = build_z2_feedback_candidate(None)
    assert feedback is not None

def test_feedback_default_readonly():
    feedback = build_z2_feedback_candidate(None)
    assert hasattr(feedback, "source_z2_report_node_id")

def test_feedback_no_auto_patch():
    feedback = build_z2_feedback_candidate(None)
    assert not hasattr(feedback, "auto_patch_z2_report")

def test_feedback_no_memory_write():
    feedback = build_z2_feedback_candidate(None)
    assert not hasattr(feedback, "persistent_memory_write")

def test_feedback_no_broker():
    feedback = build_z2_feedback_candidate(None)
    assert not hasattr(feedback, "broker_instruction")
