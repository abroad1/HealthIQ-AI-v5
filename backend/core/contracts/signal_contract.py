"""
Shared signal contract authority for runtime and validators.
"""

# Activation modes
ACTIVATION_MODE_THRESHOLD = "deterministic_threshold"
ACTIVATION_MODE_LAB_RANGE = "lab_range_exceeded"
ALLOWED_ACTIVATION_MODES = frozenset(
    {ACTIVATION_MODE_THRESHOLD, ACTIVATION_MODE_LAB_RANGE}
)

# Signal states and severity ranking
ALLOWED_SIGNAL_STATES = frozenset({"optimal", "suboptimal", "at_risk"})
STATE_RANK: dict[str, int] = {"optimal": 0, "suboptimal": 1, "at_risk": 2}

# Threshold operators
ALLOWED_THRESHOLD_OPERATORS = frozenset({"<", "<=", ">", ">=", "==", "range"})

# Override condition operators and types
ALLOWED_CONDITION_OPERATORS = frozenset({"<", "<=", ">", ">=", "=="})
ALLOWED_CONDITION_TYPES = frozenset({"any_of", "all_of"})

# Explanation metadata: expected keys only (still optional).
EXPLANATION_EXPECTED_KEYS = frozenset(
    {
        "mechanism",
        "biological_pathway",
        "interpretation",
        "implications",
        "supporting_marker_roles",
    }
)
