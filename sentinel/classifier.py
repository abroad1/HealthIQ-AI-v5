"""
Phase 1 Sentinel — changed-file risk classifier.

Maps a list of file paths to broad risk surfaces and a conservative risk level.
When uncertain, widens the recommendation rather than narrowing it.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

# Surface identifiers
SURFACE_PARSER_ALIAS_CANONICAL = "parser/alias/canonical"
SURFACE_SSOT_CANONICAL_AUTHORITY = "SSOT/canonical_authority"
SURFACE_ANALYTICS_SCORING_SIGNAL = "analytics/scoring/signal"
SURFACE_FRONTEND_TRUST = "frontend/trust"
SURFACE_PERSISTENCE_SNAPSHOT = "persistence/snapshot"
SURFACE_GOVERNANCE_CONTROL_PLANE = "governance/control_plane"
SURFACE_KNOWLEDGE_BUS_INTELLIGENCE = "knowledge_bus/intelligence"

RISK_HIGH = "HIGH"
RISK_STANDARD = "STANDARD"
RISK_LOW = "LOW"

# Test targets Sentinel selects per surface
SURFACE_TEST_MAP: dict[str, list[str]] = {
    SURFACE_PARSER_ALIAS_CANONICAL: [
        "backend/tests/regression/test_alias_canonical_sweep.py",
        "backend/tests/regression/test_ggt_alias_regression.py",
        "backend/tests/regression/test_bilirubin_alias_regression.py",
    ],
    SURFACE_SSOT_CANONICAL_AUTHORITY: [
        "backend/tests/regression/test_alias_canonical_sweep.py",
        "backend/tests/regression/test_ggt_alias_regression.py",
        "backend/tests/regression/test_bilirubin_alias_regression.py",
    ],
    SURFACE_ANALYTICS_SCORING_SIGNAL: [
        "backend/tests/regression/test_narrative_compiler_why_surface_regression.py",
        "backend/tests/regression/test_wave1_contradiction_status.py",
    ],
    SURFACE_FRONTEND_TRUST: [
        "backend/tests/regression/test_slug_leakage_regression.py",
    ],
    SURFACE_PERSISTENCE_SNAPSHOT: [
        "backend/tests/regression/test_persisted_result_replay_status.py",
    ],
    SURFACE_GOVERNANCE_CONTROL_PLANE: [],
    SURFACE_KNOWLEDGE_BUS_INTELLIGENCE: [],
}


@dataclass
class ClassifiedFile:
    path: str
    surface: str
    risk: str
    reason: str


@dataclass
class ClassificationResult:
    files: List[ClassifiedFile] = field(default_factory=list)

    @property
    def surfaces(self) -> List[str]:
        return sorted(set(f.surface for f in self.files))

    @property
    def max_risk(self) -> str:
        for level in (RISK_HIGH, RISK_STANDARD, RISK_LOW):
            if any(f.risk == level for f in self.files):
                return level
        return RISK_LOW

    @property
    def high_risk_files(self) -> List[ClassifiedFile]:
        return [f for f in self.files if f.risk == RISK_HIGH]

    def recommended_tests(self) -> List[str]:
        seen: set[str] = set()
        tests: List[str] = []
        for surface in self.surfaces:
            for t in SURFACE_TEST_MAP.get(surface, []):
                if t not in seen:
                    seen.add(t)
                    tests.append(t)
        return tests


# Rule table: (path_fragments, surface, risk, reason)
# More specific rules first. First match wins.
_RULES: list[tuple[list[str], str, str, str]] = [
    # HIGH — Intelligence Core and control-plane
    (["backend/core/pipeline/"],    SURFACE_ANALYTICS_SCORING_SIGNAL,   RISK_HIGH,     "Intelligence Core — pipeline"),
    (["backend/core/analytics/"],   SURFACE_ANALYTICS_SCORING_SIGNAL,   RISK_HIGH,     "Intelligence Core — analytics"),
    (["backend/core/scoring/"],     SURFACE_ANALYTICS_SCORING_SIGNAL,   RISK_HIGH,     "Intelligence Core — scoring"),
    (["backend/core/clustering/"],  SURFACE_ANALYTICS_SCORING_SIGNAL,   RISK_HIGH,     "Intelligence Core — clustering"),
    (["backend/core/knowledge/"],   SURFACE_KNOWLEDGE_BUS_INTELLIGENCE, RISK_HIGH,     "Knowledge loader — feeds Intelligence Core"),
    (["backend/ssot/"],             SURFACE_SSOT_CANONICAL_AUTHORITY,   RISK_HIGH,     "SSOT canonical authority"),
    (["backend/scripts/run_work_package.py"],    SURFACE_GOVERNANCE_CONTROL_PLANE, RISK_HIGH, "Execution kernel"),
    (["backend/scripts/golden_gate_local.py"],   SURFACE_GOVERNANCE_CONTROL_PLANE, RISK_HIGH, "Gate script"),
    (["backend/scripts/update_cursor_status.py"],SURFACE_GOVERNANCE_CONTROL_PLANE, RISK_HIGH, "Status writer"),
    (["automation_bus/"],           SURFACE_GOVERNANCE_CONTROL_PLANE,   RISK_HIGH,     "Automation Bus artefacts"),
    # KB packages — signal libraries feed intelligence; conservative HIGH
    (["knowledge_bus/packages/"],   SURFACE_KNOWLEDGE_BUS_INTELLIGENCE, RISK_HIGH,     "KB package (signal_library may be present)"),

    # STANDARD — canonical, parsing, persistence, frontend shaping
    (["backend/core/canonical/"],               SURFACE_PARSER_ALIAS_CANONICAL, RISK_STANDARD, "Canonical resolution layer"),
    (["backend/services/parsing/"],             SURFACE_PARSER_ALIAS_CANONICAL, RISK_STANDARD, "Parsing surface"),
    (["backend/core/dto/"],                     SURFACE_PERSISTENCE_SNAPSHOT,   RISK_STANDARD, "DTO builders — display decisions possible"),
    (["backend/core/insights/"],                SURFACE_ANALYTICS_SCORING_SIGNAL, RISK_STANDARD, "Insight synthesis — Layer B/C boundary"),
    (["backend/core/models/"],                  SURFACE_PERSISTENCE_SNAPSHOT,   RISK_STANDARD, "Persistence models"),
    (["backend/core/snapshot/"],                SURFACE_PERSISTENCE_SNAPSHOT,   RISK_STANDARD, "Snapshot layer"),
    (["frontend/lib/narrativeRuntimePresentation"], SURFACE_FRONTEND_TRUST,   RISK_STANDARD, "Narrative shaping function"),
    (["frontend/lib/primaryFindingShaping"],        SURFACE_FRONTEND_TRUST,   RISK_STANDARD, "Primary-finding shaping function"),
    (["frontend/app/components/results/"],          SURFACE_FRONTEND_TRUST,   RISK_STANDARD, "Frontend results components"),
    (["frontend/lib/"],                             SURFACE_FRONTEND_TRUST,   RISK_STANDARD, "Frontend lib — may contain shaping logic"),

    # LOW — UI primitives, layout, docs, research briefs
    (["frontend/app/components/ui/"],    SURFACE_FRONTEND_TRUST,             RISK_LOW, "UI primitives"),
    (["frontend/app/components/layout/"],SURFACE_FRONTEND_TRUST,             RISK_LOW, "Layout components"),
    (["frontend/lib/utils"],             SURFACE_FRONTEND_TRUST,             RISK_LOW, "Frontend utils"),
    (["docs/"],                          SURFACE_GOVERNANCE_CONTROL_PLANE,   RISK_LOW, "Documentation"),
    (["knowledge_bus/research/"],        SURFACE_KNOWLEDGE_BUS_INTELLIGENCE, RISK_LOW, "KB research briefs (read-only)"),
]


def classify_files(file_paths: List[str]) -> ClassificationResult:
    """Classify a list of changed file paths into risk surfaces."""
    result = ClassificationResult()
    for path in file_paths:
        normalised = path.replace("\\", "/")
        result.files.append(_classify_one(normalised))
    return result


def _classify_one(path: str) -> ClassifiedFile:
    for prefixes, surface, risk, reason in _RULES:
        for prefix in prefixes:
            if path.startswith(prefix) or ("/" + prefix.rstrip("/")) in path:
                return ClassifiedFile(path=path, surface=surface, risk=risk, reason=reason)
    # Conservative default: anything unrecognised gets STANDARD
    return ClassifiedFile(
        path=path,
        surface=SURFACE_GOVERNANCE_CONTROL_PLANE,
        risk=RISK_STANDARD,
        reason="Unrecognised path — conservative default (widened)",
    )
