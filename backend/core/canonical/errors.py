"""
Canonical boundary exceptions.
"""


class CanonicalCollisionError(Exception):
    """
    Raised when multiple raw biomarker inputs resolve to the same canonical ID.
    Fatal at the normalization boundary; no fallback.
    """

    def __init__(
        self,
        *,
        canonical_id: str,
        raw_markers: list[str],
        reason: str = "multiple_raw_inputs_resolve_to_same_canonical_id",
    ):
        self.canonical_id = canonical_id
        self.raw_markers = raw_markers
        self.reason = reason
        super().__init__(
            f"Canonical collision: {canonical_id} from raw markers {raw_markers} ({reason})"
        )

    def to_collision_dict(self) -> dict:
        """Deterministic dict for error payloads."""
        return {
            "canonical_id": self.canonical_id,
            "raw_markers": sorted(self.raw_markers),
            "reason": self.reason,
        }
