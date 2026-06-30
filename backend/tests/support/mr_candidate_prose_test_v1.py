"""
MR-BATCH-001B candidate prose test pathway ONLY.

Loads candidate prose assets from the sprint docs pack for test/demo composition.
Must NOT be imported from production runtime paths (orchestrator, retail assembly, compilers).

Candidate/test isolation: callers must pass candidate_test_mode=True.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

import yaml

PROHIBITED_GENERIC_WORDING: tuple[str, ...] = (
    "General education only",
    "Discuss any concerns",
    "Speak to your doctor",
    "Consult your healthcare provider",
    "Seek medical advice",
)

MARKER_STATE_ASSET_TYPES: frozenset[str] = frozenset(
    {
        "marker_in_range_context_explainer",
        "marker_high_context_explainer",
        "marker_low_context_explainer",
        "marker_borderline_context_explainer",
    }
)

MARKER_STATE_RANGE_VALUES: frozenset[str] = frozenset(
    {"in_range", "high", "low", "borderline"}
)


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def default_mr_batch_001b_pack_path() -> Path:
    return (
        _repo_root()
        / "docs"
        / "sprints"
        / "beta_readiness"
        / "MR-BATCH-001B_candidate_prose_assets.yaml"
    )


def _require_candidate_test_mode(candidate_test_mode: bool) -> None:
    if not candidate_test_mode:
        raise RuntimeError(
            "MR-BATCH-001B candidate prose pack requires candidate_test_mode=True "
            "(test/demo pathway only; not for production runtime)"
        )


def _normalise_biomarker_scope(scope: object) -> str:
    text = str(scope or "").strip().lower()
    if not text:
        return ""
    token = text.split("/")[0].strip()
    for prefix in ("biomarker_id:", "scope:"):
        if token.startswith(prefix):
            token = token[len(prefix) :].strip()
    return token.replace(" ", "_")


@dataclass(frozen=True)
class CandidateProseAsset:
    raw: Dict[str, Any]

    @property
    def asset_id(self) -> str:
        return str(self.raw.get("asset_id") or "")

    @property
    def asset_type(self) -> str:
        return str(self.raw.get("asset_type") or "")

    @property
    def scope(self) -> str:
        return str(self.raw.get("scope") or "")

    @property
    def biomarker_scope(self) -> str:
        return _normalise_biomarker_scope(self.scope)

    @property
    def range_state(self) -> str:
        return str(self.raw.get("range_state") or "")

    @property
    def review_status(self) -> str:
        return str(self.raw.get("review_status") or "")

    @property
    def context_dependencies(self) -> Dict[str, Any]:
        row = self.raw.get("context_dependencies")
        return dict(row) if isinstance(row, dict) else {}

    @property
    def interpretive_limitations(self) -> List[str]:
        rows = self.raw.get("interpretive_limitations")
        if not isinstance(rows, list):
            return []
        return [str(x) for x in rows if str(x).strip()]


@dataclass
class MrBatch001bCandidatePack:
    path: Path
    batch_id: str
    assets: List[CandidateProseAsset] = field(default_factory=list)

    def by_id(self, asset_id: str) -> Optional[CandidateProseAsset]:
        for asset in self.assets:
            if asset.asset_id == asset_id:
                return asset
        return None

    def select(
        self,
        *,
        biomarker_id: Optional[str] = None,
        range_state: Optional[str] = None,
        asset_type: Optional[str] = None,
        asset_id: Optional[str] = None,
    ) -> Optional[CandidateProseAsset]:
        if asset_id:
            return self.by_id(asset_id)
        for asset in self.assets:
            if biomarker_id and asset.biomarker_scope != biomarker_id:
                continue
            if range_state is not None and asset.range_state != range_state:
                continue
            if asset_type is not None and asset.asset_type != asset_type:
                continue
            return asset
        return None

    def all_prose_text(self) -> str:
        chunks: List[str] = []
        for asset in self.assets:
            chunks.append(extract_prose_text(asset.raw))
        return "\n".join(chunks)


def load_mr_batch_001b_candidate_pack(
    path: Optional[Path] = None,
    *,
    candidate_test_mode: bool = False,
) -> MrBatch001bCandidatePack:
    _require_candidate_test_mode(candidate_test_mode)
    pack_path = path or default_mr_batch_001b_pack_path()
    if not pack_path.exists():
        raise FileNotFoundError(f"MR-BATCH-001B candidate pack not found: {pack_path}")
    raw = yaml.safe_load(pack_path.read_text(encoding="utf-8")) or {}
    if not isinstance(raw, dict):
        raise ValueError("MR-BATCH-001B candidate pack root must be a mapping")
    assets_raw = raw.get("assets") or []
    if not isinstance(assets_raw, list):
        raise ValueError("MR-BATCH-001B candidate pack assets must be a list")
    assets = [CandidateProseAsset(raw=row) for row in assets_raw if isinstance(row, dict)]
    return MrBatch001bCandidatePack(
        path=pack_path,
        batch_id=str(raw.get("batch_id") or "MR-BATCH-001B"),
        assets=assets,
    )


def extract_prose_text(asset: Dict[str, Any]) -> str:
    prose = asset.get("prose_content")
    if not isinstance(prose, dict):
        return ""
    parts: List[str] = []
    for key in (
        "title",
        "body",
        "retail",
        "overview",
        "display_title",
        "additive_fragment",
        "caution_when_absent",
        "interpretive_limit",
        "interpretive_caution",
        "lead_block",
        "clinician",
    ):
        val = prose.get(key)
        if isinstance(val, str) and val.strip():
            parts.append(val.strip())
    return "\n".join(parts)


@dataclass(frozen=True)
class ComposedCandidateProse:
    biomarker_id: Optional[str]
    range_state: Optional[str]
    asset_ids: List[str]
    sections: List[str]
    interpretive_limitations: List[str]

    @property
    def rendered(self) -> str:
        body = "\n\n".join(self.sections)
        if self.interpretive_limitations:
            limits = "\n".join(f"- {line}" for line in self.interpretive_limitations)
            body = f"{body}\n\n[Interpretive limitations]\n{limits}"
        return body.strip()


def compose_marker_state_prose(
    pack: MrBatch001bCandidatePack,
    *,
    biomarker_id: str = "",
    range_state: str = "",
    include_base: bool = True,
    include_marker_state: bool = True,
    modifier_asset_ids: Optional[Sequence[str]] = None,
    missing_marker_asset_ids: Optional[Sequence[str]] = None,
    pathway_asset_id: Optional[str] = None,
    resilience_asset_id: Optional[str] = None,
) -> ComposedCandidateProse:
    """
    Hybrid minimum viable composition for test inspection:
    base + marker-state + optional modifiers/caveats/pathway/resilience.
    """
    asset_ids: List[str] = []
    sections: List[str] = []
    limitations: List[str] = []

    if include_base and biomarker_id:
        base = pack.select(biomarker_id=biomarker_id, asset_type="base_biomarker_explainer")
        if base:
            asset_ids.append(base.asset_id)
            sections.append(f"[base] {extract_prose_text(base.raw)}")
            limitations.extend(base.interpretive_limitations)

    type_by_state = {
        "in_range": "marker_in_range_context_explainer",
        "high": "marker_high_context_explainer",
        "low": "marker_low_context_explainer",
        "borderline": "marker_borderline_context_explainer",
    }
    if include_marker_state and biomarker_id and range_state:
        marker_type = type_by_state.get(range_state)
        if marker_type:
            marker = pack.select(
                biomarker_id=biomarker_id,
                range_state=range_state,
                asset_type=marker_type,
            )
            if marker:
                asset_ids.append(marker.asset_id)
                sections.append(f"[{range_state}] {extract_prose_text(marker.raw)}")
                limitations.extend(marker.interpretive_limitations)

    for mid in modifier_asset_ids or ():
        mod = pack.by_id(mid)
        if mod:
            asset_ids.append(mod.asset_id)
            sections.append(f"[modifier] {extract_prose_text(mod.raw)}")
            limitations.extend(mod.interpretive_limitations)

    for mid in missing_marker_asset_ids or ():
        caveat = pack.by_id(mid)
        if caveat:
            asset_ids.append(caveat.asset_id)
            sections.append(f"[missing-marker] {extract_prose_text(caveat.raw)}")
            limitations.extend(caveat.interpretive_limitations)

    if pathway_asset_id:
        pathway = pack.by_id(pathway_asset_id)
        if pathway:
            asset_ids.append(pathway.asset_id)
            sections.append(f"[pathway] {extract_prose_text(pathway.raw)}")
            limitations.extend(pathway.interpretive_limitations)

    if resilience_asset_id:
        resilience = pack.by_id(resilience_asset_id)
        if resilience:
            asset_ids.append(resilience.asset_id)
            sections.append(f"[resilience] {extract_prose_text(resilience.raw)}")
            limitations.extend(resilience.interpretive_limitations)

    return ComposedCandidateProse(
        biomarker_id=biomarker_id,
        range_state=range_state,
        asset_ids=asset_ids,
        sections=sections,
        interpretive_limitations=limitations,
    )


def validate_pack_governance(pack: MrBatch001bCandidatePack) -> List[str]:
    """Return list of governance violations (empty if OK)."""
    violations: List[str] = []
    for asset in pack.assets:
        if asset.review_status != "CANDIDATE":
            violations.append(f"{asset.asset_id}: review_status={asset.review_status!r}")
        if asset.asset_type in MARKER_STATE_ASSET_TYPES:
            if asset.range_state not in MARKER_STATE_RANGE_VALUES:
                violations.append(f"{asset.asset_id}: invalid range_state={asset.range_state!r}")
            if not asset.context_dependencies:
                violations.append(f"{asset.asset_id}: missing context_dependencies")
            if not asset.interpretive_limitations:
                violations.append(f"{asset.asset_id}: missing interpretive_limitations")
        prose = extract_prose_text(asset.raw)
        for phrase in PROHIBITED_GENERIC_WORDING:
            if phrase.lower() in prose.lower():
                violations.append(f"{asset.asset_id}: prohibited phrase {phrase!r}")
    return violations
