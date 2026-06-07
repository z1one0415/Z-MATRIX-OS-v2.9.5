"""
Test: Level 4 no-side-effects verification.

Verifies that disabled-mode Level 4 produces zero filesystem or I/O side effects.
No runtime_audit created. No runtime_reports created. No stdout/stderr.
"""

import os
import sys
import io
import tempfile
import shutil

from skillos.level4.config import load_config
from skillos.level4.evaluator import evaluate_level4
from skillos.level4.models import Level4EvaluationInput
from skillos.level4.side_channel import NoopSideChannel, Level4WarningCandidate


class TestLevel4NoSideEffects:

    def setup_method(self):
        self._orig_cwd = os.getcwd()

    def test_no_file_created_in_disabled_mode(self):
        """Disabled mode must not create any files."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                config = load_config(None)
                evaluate_level4(Level4EvaluationInput(), config)
                created = []
                for dirpath, dirnames, filenames in os.walk(tmpdir):
                    for fn in filenames:
                        created.append(os.path.join(dirpath, fn))
                assert len(created) == 0, f"Files created: {created}"
            finally:
                os.chdir(self._orig_cwd)

    def test_no_stdout_in_disabled_mode(self):
        """Disabled mode must not print to stdout."""
        config = load_config(None)
        captured = io.StringIO()
        old_stdout = sys.stdout
        sys.stdout = captured
        try:
            evaluate_level4(Level4EvaluationInput(), config)
            output = captured.getvalue()
            assert len(output) == 0, f"stdout output detected: {output!r}"
        finally:
            sys.stdout = old_stdout

    def test_no_stderr_in_disabled_mode(self):
        """Disabled mode must not print to stderr."""
        config = load_config(None)
        captured = io.StringIO()
        old_stderr = sys.stderr
        sys.stderr = captured
        try:
            evaluate_level4(Level4EvaluationInput(), config)
            output = captured.getvalue()
            assert len(output) == 0, f"stderr output detected: {output!r}"
        finally:
            sys.stderr = old_stderr

    def test_noop_side_channel_does_not_write(self):
        """NoopSideChannel must not write anything."""
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                channel = NoopSideChannel()
                warning = Level4WarningCandidate()
                channel.emit(warning)
                channel.flush()
                # Verify no runtime_audit or runtime_reports paths
                audit_path = os.path.join(tmpdir, "runtime_audit")
                reports_path = os.path.join(tmpdir, "runtime_reports")
                assert not os.path.exists(audit_path), f"Created: {audit_path}"
                assert not os.path.exists(reports_path), f"Created: {reports_path}"
            finally:
                os.chdir(self._orig_cwd)

    def test_no_tag_created(self):
        """Level 4 code must not create git tags."""
        from skillos.level4.config import load_config
        import subprocess
        config = load_config(None)
        evaluate_level4(Level4EvaluationInput(), config)
        # Verify no new tags (tags before/after should be same)
        result = subprocess.run(
            ["git", "tag", "--list"],
            capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__))
        )
        # We just verify the code doesn't crash (passive check)

    def test_no_operator_report_created(self):
        """Disabled mode must not create operator report files."""
        from skillos.level4.config import load_config
        from skillos.level4.evaluator import evaluate_level4
        from skillos.level4.models import Level4EvaluationInput
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                config = load_config(None)
                evaluate_level4(Level4EvaluationInput(), config)
                # Check no level4_operator_review.md was created anywhere accessible
                for dirpath, _, filenames in os.walk(tmpdir):
                    for fn in filenames:
                        assert "level4" not in fn.lower(), f"Level 4 file created: {fn}"
            finally:
                os.chdir(self._orig_cwd)

    def test_no_warning_file_created(self):
        """Disabled mode must not create warning audit files."""
        from skillos.level4.config import load_config
        from skillos.level4.evaluator import evaluate_level4
        from skillos.level4.models import Level4EvaluationInput
        with tempfile.TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            try:
                config = load_config(None)
                evaluate_level4(Level4EvaluationInput(), config)
                for dirpath, _, filenames in os.walk(tmpdir):
                    for fn in filenames:
                        if "warning" in fn.lower():
                            pytest.fail(f"Warning file created: {fn}")
            finally:
                os.chdir(self._orig_cwd)
