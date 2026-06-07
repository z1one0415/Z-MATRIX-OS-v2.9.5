"""
Level 4 side-channel delivery.

P0: NoopSideChannel — default disabled, no-op, no file handles.
No call to runtime_audit/ or runtime_reports/ paths.
No caller-visible output. No exception leak.
"""

from skillos.level4.models import Level4WarningCandidate


class Level4SideChannel:
    """
    Base side-channel interface for Level 4 warning delivery.

    P0: no-op implementation. No files written. No stdout/stderr.
    No network. No production paths.
    """

    def emit(self, warning: Level4WarningCandidate) -> None:
        """
        Emit a single warning to the side channel.

        P0: no-op. Does not write, does not print, does not raise.
        """
        pass

    def flush(self) -> None:
        """
        Flush any buffered warnings.

        P0: no-op. No file handles to flush.
        """
        pass


class NoopSideChannel(Level4SideChannel):
    """
    Strict no-op side channel.

    Default for disabled mode. Guarantees zero side effects.
    No file handles created. No directories created.
    """

    def emit(self, warning: Level4WarningCandidate) -> None:
        return None

    def flush(self) -> None:
        return None


def create_side_channel(config) -> Level4SideChannel:
    """
    Factory for side-channel instance.

    P0: always returns NoopSideChannel regardless of config.
    Enabled-path side channels NOT IMPLEMENTED in P0.
    """
    return NoopSideChannel()
