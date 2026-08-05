"""
CLIN-PRIORITY-CORE-1 — Concern construction service (hepatic Checkpoint 1).

Consumes already-fired signal results and biomarker values; constructs
ConsolidatedConcernSet. Does not change SignalEvaluator / activation.
Never calls fib_4 for fibrosis classification.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from core.analytics.prioritisation_registry import (
    LoadedPrioritisationPackage,
    load_prioritisation_package,
)
from core.models.clinical_finding import (
    CLINICAL_FINDING_CONTRACT_VERSION,
    CLINICAL_FINDING_RULESET_VERSION,
    ClinicalFinding,
    ConsolidatedConcernSet,
    FindingProvenance,
    FindingRelationship,
    RuleCitation,
    make_finding_id,
)

_HEPATIC_SIGNAL_PREFIXES = (
    "signal_alt_",
    "signal_alp_",
    "signal_ggt_",
    "signal_bilirubin_",
    "signal_albumin_",
    "signal_hepatic_",
)
_PLT_SIGNAL_PREFIXES = ("signal_platelets_", "signal_plt_")
_MCV_SIGNAL_PREFIXES = ("signal_mcv_",)
_FERRITIN_SIGNAL_PREFIXES = ("signal_ferritin_",)
_HB_SIGNAL_PREFIXES = ("signal_hgb_", "signal_hb_", "signal_haemoglobin_")


def _num(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, dict):
        for key in ("value", "measurement", "result"):
            if key in value:
                return _num(value[key])
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _biomarker_value(biomarkers: Dict[str, Any], biomarker_id: str) -> Optional[float]:
    if biomarker_id not in biomarkers:
        # common aliases
        aliases = {
            "hb": ("hgb", "haemoglobin", "hemoglobin"),
            "hgb": ("hb", "haemoglobin", "hemoglobin"),
            "tsat": ("transferrin_saturation", "transferrin_sat"),
            "transferrin_saturation": ("tsat", "transferrin_sat"),
            "platelets": ("plt", "platelet_count"),
            "plt": ("platelets", "platelet_count"),
        }
        for alt in aliases.get(biomarker_id, ()):
            if alt in biomarkers:
                return _num(biomarkers[alt])
        return None
    return _num(biomarkers[biomarker_id])


def _range_bounds(
    lab_ranges: Dict[str, Any], biomarker_id: str
) -> Tuple[Optional[float], Optional[float]]:
    row = lab_ranges.get(biomarker_id)
    if row is None:
        aliases = {
            "hb": ("hgb", "haemoglobin"),
            "hgb": ("hb", "haemoglobin"),
            "tsat": ("transferrin_saturation",),
            "transferrin_saturation": ("tsat",),
            "platelets": ("plt",),
            "plt": ("platelets",),
        }
        for alt in aliases.get(biomarker_id, ()):
            row = lab_ranges.get(alt)
            if row is not None:
                break
    if not isinstance(row, dict):
        return None, None
    lo = row.get("min", row.get("low", row.get("lrl")))
    hi = row.get("max", row.get("high", row.get("uln")))
    lo_f = _num(lo)
    hi_f = _num(hi)
    return lo_f, hi_f


def _x_uln(value: Optional[float], uln: Optional[float]) -> Optional[float]:
    if value is None or uln is None or uln <= 0:
        return None
    return value / uln


def _is_high(value: Optional[float], uln: Optional[float]) -> bool:
    if value is None or uln is None:
        return False
    return value > uln


def _is_low(value: Optional[float], lrl: Optional[float]) -> bool:
    if value is None or lrl is None:
        return False
    return value < lrl


def _activation_key(row: Any) -> str:
    if isinstance(row, dict):
        return str(row.get("activation_key") or "").strip()
    return str(getattr(row, "activation_key", "") or "").strip()


def _signal_id(row: Any) -> str:
    if isinstance(row, dict):
        return str(row.get("signal_id") or "").strip()
    return str(getattr(row, "signal_id", "") or "").strip()


def _keys_matching(signal_results: Sequence[Any], prefixes: Tuple[str, ...]) -> List[str]:
    out: List[str] = []
    for row in signal_results or []:
        key = _activation_key(row)
        sid = _signal_id(row)
        hay = f"{sid}::{key}" if sid and key else (key or sid)
        if any(hay.startswith(p) or sid.startswith(p) or key.startswith(p) for p in prefixes):
            if key:
                out.append(key)
            elif sid:
                out.append(sid)
    return sorted(set(out))


def _severity_alt_ast(x: Optional[float], absolute: Optional[float]) -> Optional[str]:
    if absolute is not None and absolute > 1000:
        return "severe"
    if x is None:
        return None
    if x >= 10:
        return "severe"
    if x >= 5:
        return "marked"
    if x >= 3:
        return "moderate"
    if x > 1:
        return "mild"
    return None


def _severity_alp(x: Optional[float]) -> Optional[str]:
    if x is None:
        return None
    if x >= 2:
        return "significant"
    if x > 1:
        return "mild"
    return None


def _urgency_and_tier_from_enzyme(
    x_alt: Optional[float],
    x_ast: Optional[float],
    alt: Optional[float],
    ast: Optional[float],
) -> Tuple[str, int]:
    x = None
    for candidate in (x_alt, x_ast):
        if candidate is not None:
            x = candidate if x is None else max(x, candidate)
    abs_max = None
    for candidate in (alt, ast):
        if candidate is not None:
            abs_max = candidate if abs_max is None else max(abs_max, candidate)
    if (x is not None and x >= 10) or (abs_max is not None and abs_max > 1000):
        return "same_day", 0
    if x is not None and x >= 5:
        return "within_days", 1
    if x is not None and x > 1:
        return "within_weeks", 1
    return "within_weeks", 1


def _r_classification(r: Optional[float]) -> Optional[str]:
    if r is None:
        return None
    if r >= 5:
        return "hepatocellular"
    if r > 2 and r < 5:
        return "mixed"
    return "cholestatic"


def _build_finding(
    *,
    domain: str,
    finding_type: str,
    label: str,
    keys: List[str],
    biomarkers: List[str],
    urgency: str,
    severity: Optional[str],
    tier: int,
    role: str,
    presentation_state: str = "principal",
    missing_data_state: str = "none",
    missing_data_notes: Optional[List[str]] = None,
    caveats: Optional[List[str]] = None,
    prohibited: Optional[List[str]] = None,
    serious_result_state: str = "not_applicable",
    release_gate_status: str = "RELEASE_AUTHORISED",
    withheld: bool = False,
    rule_ids: Optional[List[str]] = None,
    nested_labels: Optional[List[str]] = None,
    quarantine_flags: Optional[List[str]] = None,
    dependency_flags: Optional[List[str]] = None,
    confidence: Optional[str] = None,
    actionability: Optional[str] = None,
    severity_indeterminate: bool = False,
    compile_run_id: Optional[str] = None,
) -> ClinicalFinding:
    cleaned_keys = sorted({k for k in keys if k})
    if not cleaned_keys:
        raise ValueError(f"{finding_type} requires constituent_activation_keys")
    finding_id = make_finding_id(domain, finding_type, cleaned_keys)
    citations = [
        RuleCitation(rule_id=rid, evidence_label=None)
        for rid in (rule_ids or [])
    ]
    return ClinicalFinding(
        finding_id=finding_id,
        domain=domain,
        finding_type=finding_type,
        label=label,
        constituent_activation_keys=cleaned_keys,
        constituent_biomarker_ids=sorted(set(biomarkers)),
        urgency_time_band=urgency,  # type: ignore[arg-type]
        severity_band=severity,
        severity_indeterminate=severity_indeterminate,
        concern_tier=tier,  # type: ignore[arg-type]
        role=role,  # type: ignore[arg-type]
        presentation_state=presentation_state,  # type: ignore[arg-type]
        clinical_significance=None,
        actionability=actionability,
        interpretive_confidence=confidence,
        missing_data_state=missing_data_state,  # type: ignore[arg-type]
        missing_data_notes=list(missing_data_notes or []),
        caveats=list(caveats or []),
        prohibited_behaviours_asserted=list(prohibited or []),
        serious_result_state=serious_result_state,  # type: ignore[arg-type]
        release_gate_status=release_gate_status,  # type: ignore[arg-type]
        withheld=withheld,
        provenance=FindingProvenance(
            clinical_rule_ids=list(rule_ids or []),
            contract_version=CLINICAL_FINDING_CONTRACT_VERSION,
            ruleset_version=CLINICAL_FINDING_RULESET_VERSION,
            compile_run_id=compile_run_id,
            rule_citations=citations,
        ),
        relationships=[],
        nested_constituent_labels=list(nested_labels or []),
        quarantine_flags=list(quarantine_flags or []),
        dependency_flags=list(dependency_flags or []),
    )


def construct_clinical_concern_set(
    signal_results: Optional[Sequence[Any]],
    biomarkers: Optional[Dict[str, Any]],
    lab_ranges: Optional[Dict[str, Any]],
    derived: Optional[Dict[str, Any]] = None,
    priors: Optional[Dict[str, Any]] = None,
    context: Optional[Dict[str, Any]] = None,
    *,
    package: Optional[LoadedPrioritisationPackage] = None,
) -> ConsolidatedConcernSet:
    """
    Construct the governed clinical concern set for the current result snapshot.

    Checkpoint 1 implements the hepatic pilot (+ minimal stubs for HEP-AS-8/9/13/14).
    """
    del priors  # reserved for longitudinal Checkpoint / RE-AS-* later
    pkg = package or load_prioritisation_package()
    stamp = pkg.stamp
    biomarkers = dict(biomarkers or {})
    lab_ranges = dict(lab_ranges or {})
    signal_results = list(signal_results or [])
    derived = dict(derived or {})
    context = dict(context or {})

    # Hard quarantine: never use fib_4 for finding construction
    fib_4_computed = False
    fib_4_displayed = False
    quarantine_notes = [
        "XD-QUAR-1: FIB-4 not used for fibrosis finding authority",
        "CV-risk quarantine: not computed as finding in this package",
    ]
    if "fib_4" in derived:
        # Presence in derived dict from ratio_registry is allowed; we must not consume it.
        quarantine_notes.append("fib_4 present in derived inputs but ignored for findings")

    alt = _biomarker_value(biomarkers, "alt")
    ast = _biomarker_value(biomarkers, "ast")
    alp = _biomarker_value(biomarkers, "alp")
    ggt = _biomarker_value(biomarkers, "ggt")
    bili = _biomarker_value(biomarkers, "bilirubin")
    albumin = _biomarker_value(biomarkers, "albumin")
    inr = _biomarker_value(biomarkers, "inr")
    platelets = _biomarker_value(biomarkers, "platelets")
    if platelets is None:
        platelets = _biomarker_value(biomarkers, "plt")
    mcv = _biomarker_value(biomarkers, "mcv")
    hb = _biomarker_value(biomarkers, "hgb")
    if hb is None:
        hb = _biomarker_value(biomarkers, "hb")
    ferritin = _biomarker_value(biomarkers, "ferritin")
    tsat = _biomarker_value(biomarkers, "tsat")
    if tsat is None:
        tsat = _biomarker_value(biomarkers, "transferrin_saturation")
    transferrin = _biomarker_value(biomarkers, "transferrin")

    _, alt_uln = _range_bounds(lab_ranges, "alt")
    _, ast_uln = _range_bounds(lab_ranges, "ast")
    _, alp_uln = _range_bounds(lab_ranges, "alp")
    _, ggt_uln = _range_bounds(lab_ranges, "ggt")
    _, bili_uln = _range_bounds(lab_ranges, "bilirubin")
    alb_lrl, _ = _range_bounds(lab_ranges, "albumin")
    plt_lrl, _ = _range_bounds(lab_ranges, "platelets")
    if plt_lrl is None:
        plt_lrl, _ = _range_bounds(lab_ranges, "plt")
    _, mcv_uln = _range_bounds(lab_ranges, "mcv")
    hb_lrl, _ = _range_bounds(lab_ranges, "hgb")
    if hb_lrl is None:
        hb_lrl, _ = _range_bounds(lab_ranges, "hb")
    _, ferritin_uln = _range_bounds(lab_ranges, "ferritin")
    transferrin_lrl, _ = _range_bounds(lab_ranges, "transferrin")

    x_alt = _x_uln(alt, alt_uln)
    x_ast = _x_uln(ast, ast_uln)
    x_alp = _x_uln(alp, alp_uln)
    x_bili = _x_uln(bili, bili_uln)

    alt_high = _is_high(alt, alt_uln)
    ast_high = _is_high(ast, ast_uln)
    alp_high = _is_high(alp, alp_uln)
    ggt_high = _is_high(ggt, ggt_uln)
    bili_high = _is_high(bili, bili_uln)
    albumin_low = _is_low(albumin, alb_lrl)
    platelets_low = _is_low(platelets, plt_lrl)
    mcv_high = _is_high(mcv, mcv_uln)
    anaemia = _is_low(hb, hb_lrl)
    ferritin_high = _is_high(ferritin, ferritin_uln)
    transferrin_low = _is_low(transferrin, transferrin_lrl)

    alp_present = alp is not None and alp_uln is not None
    alp_absent = "alp" not in biomarkers and alp is None
    # Explicit absent marker from fixtures
    if context.get("alp_absent") is True:
        alp_absent = True
        alp_present = False

    ggt_present = ggt is not None
    ggt_absent = context.get("ggt_absent") is True or (
        "ggt" not in biomarkers and ggt is None
    )

    hepatic_keys = _keys_matching(signal_results, _HEPATIC_SIGNAL_PREFIXES)
    plt_keys = _keys_matching(signal_results, _PLT_SIGNAL_PREFIXES)
    mcv_keys = _keys_matching(signal_results, _MCV_SIGNAL_PREFIXES)
    ferritin_keys = _keys_matching(signal_results, _FERRITIN_SIGNAL_PREFIXES)
    hb_keys = _keys_matching(signal_results, _HB_SIGNAL_PREFIXES)

    # R-value for pattern only (never urgency/severity).
    # Both ALT and ALP must be assessable; when only ALT/AST is high and ALP is
    # not high, qualitative pattern is hepatocellular (do not mis-label via R).
    r_value: Optional[float] = None
    r_class: Optional[str] = None
    if (
        not alp_absent
        and alt is not None
        and alp is not None
        and alt_uln
        and alp_uln
        and alt_high
        and alp_high
    ):
        r_value = (alt / alt_uln) / (alp / alp_uln)
        r_class = _r_classification(r_value)
    elif alt_high and not alp_high and not alp_absent:
        r_class = "hepatocellular"
    elif alp_high and not alt_high and not ast_high:
        r_class = None  # isolated ALP handled as HEP-F7

    # AST:ALT ratio for HEP-F5 — never fib_4
    ast_alt_ratio: Optional[float] = None
    if ast is not None and alt is not None and alt > 0:
        ast_alt_ratio = ast / alt

    findings: List[ClinicalFinding] = []
    domain_notes: List[str] = []

    abnormal_hepatic = any([alt_high, ast_high, alp_high, ggt_high, bili_high])
    enzyme_abnormal = any([alt_high, ast_high, alp_high, ggt_high])

    # --- Synthetic dysfunction HEP-F4 (outranks injury when present) ---
    synthetic = abnormal_hepatic and (
        albumin_low or (inr is not None and inr > 1.5 and not context.get("anticoagulated"))
    )
    # --- Enzyme / bilirubin pattern findings (HEP-CONS-1 consolidation) ---
    hepatic_pattern_finding: Optional[ClinicalFinding] = None

    nested_labels: List[str] = []
    missing_notes: List[str] = []
    caveats: List[str] = []
    prohibited: List[str] = []

    if albumin is None and inr is None and enzyme_abnormal:
        missing_notes.append("albumin_inr_not_assessable")
    if ast is None and alt_high:
        caveats.append("confidence_reduced_ast_absent")

    # Collect activation keys for enzyme consolidation
    pattern_keys = list(hepatic_keys)
    pattern_biomarkers: List[str] = []
    for bid, flag in (
        ("alt", alt_high),
        ("ast", ast_high),
        ("alp", alp_high),
        ("ggt", ggt_high),
        ("bilirubin", bili_high),
    ):
        if flag:
            pattern_biomarkers.append(bid)

    # Isolated ALP with normal GGT → HEP-F7 (reclassified)
    isolated_alp = (
        alp_high
        and not alt_high
        and not ast_high
        and not bili_high
        and (ggt is not None and not ggt_high or ggt_absent)
    )
    # Isolated GGT
    isolated_ggt = ggt_high and not alt_high and not ast_high and not alp_high and not bili_high
    # Isolated bilirubin
    isolated_bili = bili_high and not alt_high and not ast_high and not alp_high and not ggt_high

    # Fibrosis-dominant near-range pattern (HEP-AS-10): AST:ALT>1 + low platelets
    # with ALT not high — do not also emit a mild AST enzyme injury finding.
    platelets_below_50 = platelets is not None and platelets < 50
    fibrosis_dominant = (
        ast_alt_ratio is not None
        and ast_alt_ratio > 1
        and platelets_low
        and not platelets_below_50
        and not alt_high
        and not alp_high
        and not bili_high
        and not ggt_high
    )

    if synthetic:
        keys = pattern_keys or [
            "clinical_prioritisation::HEP-F4:synthetic_dysfunction"
        ]
        if albumin_low:
            pattern_biomarkers.append("albumin")
        urg, tier = "same_day", 0
        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F4",
            label="hepatic_synthetic_dysfunction",
            keys=keys,
            biomarkers=pattern_biomarkers + (["albumin"] if albumin_low else []),
            urgency=urg,
            severity="severe",
            tier=tier,
            role="principal_concern",
            caveats=["albumin_non_hepatic_cause_mandatory"] if albumin_low else [],
            prohibited=["assert_albumin_cause_hepatic_without_exclusion"],
            serious_result_state="tier_0_withheld",
            release_gate_status="SPECIFICATION_ONLY",
            withheld=True,
            rule_ids=["HEP-F4", "HEP-LEAD-1", "XD-T0-2"],
            dependency_flags=["TIER_0_PATHWAY_DEPENDENCY"],
            actionability="immediate",
            compile_run_id=stamp.compile_run_id,
            missing_data_notes=missing_notes,
        )
    elif isolated_alp:
        origin = "non_hepatic_likely" if (ggt_present and not ggt_high) else "undetermined"
        keys = pattern_keys or ["clinical_prioritisation::HEP-F7:isolated_alp"]
        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F7",
            label=f"isolated_raised_alp_{origin}",
            keys=keys,
            biomarkers=["alp"] + (["ggt"] if ggt_present else []),
            urgency="within_weeks",
            severity=_severity_alp(x_alp) or "significant",
            tier=1,
            role="reclassified",
            caveats=["origin_undetermined"] if origin == "undetermined" else [],
            prohibited=["assume_hepatic_origin_without_ggt"],
            rule_ids=["HEP-F7", "HEP-IND-3"],
            actionability="investigate_non_hepatic",
            compile_run_id=stamp.compile_run_id,
            missing_data_notes=(["ggt_absent"] if ggt_absent else []),
            missing_data_state="not_assessable" if ggt_absent else "none",
        )
    elif isolated_ggt:
        keys = pattern_keys or ["clinical_prioritisation::HEP-F8:isolated_ggt"]
        if ggt is not None and ggt <= 100:
            urg, tier = "routine", 2
        else:
            urg, tier = "within_weeks", 1
        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F8",
            label="isolated_raised_ggt",
            keys=keys,
            biomarkers=["ggt"],
            urgency=urg,
            severity=None,
            tier=tier,
            role="principal_concern",
            rule_ids=["HEP-F8", "HEP-GGT-1"],
            compile_run_id=stamp.compile_run_id,
        )
    elif isolated_bili and not anaemia:
        keys = pattern_keys or ["clinical_prioritisation::HEP-F6:gilbert_pattern"]
        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F6",
            label="isolated_hyperbilirubinaemia_gilbert_pattern",
            keys=keys,
            biomarkers=["bilirubin"],
            urgency="routine",
            severity=None,
            tier=2,
            role="principal_concern",
            caveats=["split_bilirubin_if_unmeasured"],
            prohibited=["assert_gilberts_without_conjugated_fraction"],
            rule_ids=["HEP-F6", "HEP-IND-4"],
            actionability="reassurance_available",
            compile_run_id=stamp.compile_run_id,
            missing_data_notes=["conjugated_fraction_unmeasured"],
            missing_data_state="not_assessable",
        )
    elif isolated_bili and anaemia:
        keys = sorted(set(pattern_keys + hb_keys)) or [
            "clinical_prioritisation::HEP-BILI-ANAEMIA:haemolysis_consider"
        ]
        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F6",
            label="hyperbilirubinaemia_with_anaemia_haemolysis_consider",
            keys=keys,
            biomarkers=["bilirubin", "hgb"],
            urgency="within_weeks",
            severity=None,
            tier=1,
            role="principal_concern",
            prohibited=["dismiss_haemolysis"],
            rule_ids=["HEP-AS-7"],
            actionability="discuss_investigate",
            compile_run_id=stamp.compile_run_id,
        )
    elif alt_high and alp_absent:
        # HEP-F9 — pattern undetermined
        keys = pattern_keys or ["clinical_prioritisation::HEP-F9:pattern_undetermined"]
        urg, tier = _urgency_and_tier_from_enzyme(x_alt, x_ast, alt, ast)
        if urg == "same_day":
            serious = "tier_0_withheld"
            gate = "SPECIFICATION_ONLY"
            withheld = True
            deps = ["TIER_0_PATHWAY_DEPENDENCY"]
        else:
            serious = "not_applicable"
            gate = "RELEASE_AUTHORISED"
            withheld = False
            deps = []
        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F9",
            label="non_classifiable_hepatic_abnormality",
            keys=keys,
            biomarkers=["alt"],
            urgency=urg,
            severity=_severity_alt_ast(x_alt, alt),
            tier=tier,
            role="principal_concern",
            severity_indeterminate=True,
            missing_data_state="indeterminate_severity",
            missing_data_notes=["pattern_not_assessable_r_not_computed", "alp_absent"],
            prohibited=["call_hepatocellular_without_alp"],
            serious_result_state=serious,
            release_gate_status=gate,
            withheld=withheld,
            rule_ids=["HEP-F9", "HEP-IND-1"],
            dependency_flags=deps,
            actionability="discuss_investigate",
            compile_run_id=stamp.compile_run_id,
        )
    elif (
        not fibrosis_dominant
        and (
            alt_high
            or ast_high
            or (alp_high and not isolated_alp)
            or (bili_high and enzyme_abnormal)
        )
    ):
        # Consolidated enzyme pattern HEP-CONS-1 → F1/F2/F3
        if r_class == "hepatocellular" or (r_class is None and alt_high and not alp_high):
            ftype, label = "HEP-F1", "consolidated_hepatocellular_enzyme_elevation"
        elif r_class == "cholestatic":
            ftype, label = "HEP-F2", "cholestatic_injury_pattern"
        elif r_class == "mixed":
            ftype, label = "HEP-F3", "mixed_injury_pattern"
        else:
            ftype, label = "HEP-F1", "consolidated_hepatocellular_enzyme_elevation"

        keys = pattern_keys or [
            f"clinical_prioritisation::{ftype}:enzyme_pattern"
        ]
        # Nested constituent labels for multi-analyte panels (XD-AS-25 style)
        for bid in pattern_biomarkers:
            nested_labels.append(f"{bid}_abnormal")

        urg, tier = _urgency_and_tier_from_enzyme(x_alt, x_ast, alt, ast)
        # Hy's law check (combination only — no standalone bili Tier 0)
        if (
            ((x_alt is not None and x_alt >= 3) or (x_ast is not None and x_ast >= 3))
            and x_bili is not None
            and x_bili >= 2
            and (x_alp is None or x_alp < 2)
        ):
            urg, tier = "same_day", 0

        sev = _severity_alt_ast(x_alt if x_alt is not None else x_ast, alt if alt is not None else ast)
        if urg == "same_day":
            serious = "tier_0_withheld"
            gate = "SPECIFICATION_ONLY"
            withheld = True
            deps = ["TIER_0_PATHWAY_DEPENDENCY"]
            action = "immediate"
        else:
            serious = "not_applicable"
            gate = "RELEASE_AUTHORISED"
            withheld = False
            deps = []
            action = "discuss_investigate"

        if urg == "within_weeks" and tier == 1:
            prohibited.append("describe_as_urgent_merely_because_tier1")

        hepatic_pattern_finding = _build_finding(
            domain="hepatic",
            finding_type=ftype,
            label=label,
            keys=keys,
            biomarkers=pattern_biomarkers,
            urgency=urg,
            severity=sev,
            tier=tier,
            role="principal_concern",
            missing_data_notes=missing_notes,
            missing_data_state="not_assessable" if missing_notes else "none",
            caveats=caveats,
            prohibited=prohibited
            + (["urgent_diagnostic_claim"] if urg != "same_day" else []),
            serious_result_state=serious,
            release_gate_status=gate,
            withheld=withheld,
            rule_ids=["HEP-CONS-1", "HEP-P2", "XD-HEP-FLOOR-1", ftype],
            nested_labels=nested_labels,
            dependency_flags=deps,
            actionability=action,
            confidence="reduced_ast_absent" if ast is None and alt_high else None,
            compile_run_id=stamp.compile_run_id,
        )

    # --- HEP-F5 fibrosis (AST:ALT > 1 and/or low platelets) — NO fib_4 ---
    fibrosis: Optional[ClinicalFinding] = None
    # Platelets < 50 → independent haem finding, not absorbed into F5
    fibrosis_pattern = False
    if ast_alt_ratio is not None and ast_alt_ratio > 1:
        # Near-range / in-range still produces finding (HEP-AS-10)
        fibrosis_pattern = True
    if platelets_low and not platelets_below_50 and (abnormal_hepatic or fibrosis_pattern):
        fibrosis_pattern = True
    # HEP-AS-10: AST:ALT>1 + platelets (even near range)
    if (
        ast_alt_ratio is not None
        and ast_alt_ratio > 1
        and platelets is not None
        and platelets_low
        and not platelets_below_50
    ):
        fibrosis_pattern = True

    if fibrosis_pattern and not platelets_below_50:
        f5_meta = pkg.finding_types.get("HEP-F5", {})
        prov_key = str(
            f5_meta.get("biomarker_derived_provenance_key")
            or "clinical_prioritisation::HEP-F5:ast_alt_platelets_pattern"
        )
        keys = sorted(set(hepatic_keys + plt_keys + [prov_key]))
        # If a stronger enzyme pattern already exists at marked+, F5 may be secondary
        fibrosis = _build_finding(
            domain="hepatic",
            finding_type="HEP-F5",
            label="suspected_advanced_fibrosis",
            keys=keys,
            biomarkers=[b for b in ("ast", "alt", "platelets") if _biomarker_value(biomarkers, b) is not None],
            urgency="within_weeks",
            severity="ast_alt_gt_1_plus_platelets",
            tier=1,
            role="principal_concern",
            prohibited=["fib_4_computed", "fib_4_displayed"],
            quarantine_flags=["XD-QUAR-1", "R3"],
            dependency_flags=["REGULATORY_DEPENDENCY_R3"],
            rule_ids=["HEP-F5", "XD-QUAR-1"],
            actionability="investigate",
            compile_run_id=stamp.compile_run_id,
        )

    # --- HEP-F10 iron overload vs contextual ferritin ---
    iron_finding: Optional[ClinicalFinding] = None
    ferritin_contextual = False
    if ferritin_high and tsat is not None and tsat > 45:
        keys = sorted(set(ferritin_keys + hepatic_keys)) or [
            "clinical_prioritisation::HEP-F10:iron_overload"
        ]
        iron_finding = _build_finding(
            domain="hepatic",
            finding_type="HEP-F10",
            label="possible_iron_overload_hepatic_context",
            keys=keys,
            biomarkers=["ferritin", "transferrin_saturation"],
            urgency="within_weeks",
            severity=None,
            tier=1,
            role="co_lead",
            rule_ids=["HEP-F10"],
            actionability="discuss_investigate",
            compile_run_id=stamp.compile_run_id,
        )
    elif ferritin_high and (tsat is None or tsat <= 45) and hepatic_pattern_finding is not None:
        ferritin_contextual = True

    # --- Haematology stubs for HEP-AS-13 / HEP-AS-14 ---
    haem_findings: List[ClinicalFinding] = []
    mcv_mild = False
    mcv_above_mild = False
    if mcv_high and mcv_uln is not None and mcv is not None:
        # Mild: >ULN to 105; above mild if >105
        if mcv <= 105:
            mcv_mild = True
        else:
            mcv_above_mild = True

    if mcv_above_mild:
        keys = mcv_keys or ["clinical_prioritisation::HAEM-F2:macrocytosis"]
        haem_findings.append(
            _build_finding(
                domain="haematology",
                finding_type="HAEM-F2",
                label="macrocytosis_above_mild_band",
                keys=keys,
                biomarkers=["mcv"],
                urgency="within_weeks",
                severity="marked" if mcv is not None and mcv > 115 else "moderate",
                tier=1,
                role="independent_secondary",
                prohibited=["attach_mcv_as_context_above_mild_band"],
                rule_ids=["HAEM-S-2", "HEP-AS-13"],
                compile_run_id=stamp.compile_run_id,
            )
        )
    elif mcv_mild and hepatic_pattern_finding is not None:
        # Nest as contextual under hepatic — do not create independent finding
        pass
    elif mcv_mild and hepatic_pattern_finding is None:
        keys = mcv_keys or ["clinical_prioritisation::HAEM-F2:isolated_mild_macrocytosis"]
        haem_findings.append(
            _build_finding(
                domain="haematology",
                finding_type="HAEM-F2",
                label="isolated_mild_macrocytosis",
                keys=keys,
                biomarkers=["mcv"],
                urgency="routine",
                severity="mild",
                tier=2,
                role="principal_concern",
                rule_ids=["HAEM-F2", "XD-HEP-FLOOR-2"],
                compile_run_id=stamp.compile_run_id,
            )
        )

    if platelets_below_50:
        keys = plt_keys or ["clinical_prioritisation::HAEM-PLT:thrombocytopenia"]
        haem_findings.append(
            _build_finding(
                domain="haematology",
                finding_type="HAEM-PLT",
                label="thrombocytopenia_below_50",
                keys=keys,
                biomarkers=["platelets"],
                urgency="same_day",
                severity="moderate_to_severe",
                tier=0,
                role="principal_concern",
                presentation_state="principal",
                prohibited=["absorb_platelets_below_50"],
                serious_result_state="tier_0_classified",
                release_gate_status="SPECIFICATION_ONLY",
                withheld=True,
                rule_ids=["HAEM-U-D-1", "HEP-AS-14"],
                dependency_flags=["TIER_0_PATHWAY_DEPENDENCY"],
                actionability="haem_urgency",
                compile_run_id=stamp.compile_run_id,
            )
        )

    # Assemble findings list
    if hepatic_pattern_finding is not None:
        # Attach contextual nest labels
        extra_nested = list(hepatic_pattern_finding.nested_constituent_labels)
        if mcv_mild:
            extra_nested.append("mcv_mild_macrocytosis")
        if transferrin_low:
            extra_nested.append("transferrin_low")
        if ferritin_contextual:
            extra_nested.append("ferritin_contextual")
        if extra_nested != list(hepatic_pattern_finding.nested_constituent_labels):
            hepatic_pattern_finding = hepatic_pattern_finding.model_copy(
                update={"nested_constituent_labels": extra_nested}
            )
        findings.append(hepatic_pattern_finding)

    # Fibrosis: only as separate finding when no enzyme pattern, OR when enzyme
    # severity is below marked (HEP-LEAD-2). When enzyme pattern is marked+ it
    # outranks; still keep F5 only if it is the sole hepatic signal (HEP-AS-10).
    if fibrosis is not None:
        if hepatic_pattern_finding is None:
            findings.append(fibrosis)
        else:
            sev = hepatic_pattern_finding.severity_band
            if sev not in {"marked", "severe"}:
                # Both can exist; lead selection decides
                findings.append(fibrosis)

    if iron_finding is not None:
        findings.append(iron_finding)

    findings.extend(haem_findings)

    # No-concern hepatic panel
    no_concern = False
    no_concern_notes: List[str] = []
    hepatic_panel_present = any(
        _biomarker_value(biomarkers, b) is not None
        for b in ("alt", "ast", "alp", "ggt", "bilirubin", "albumin")
    )
    if not findings and hepatic_panel_present and not abnormal_hepatic:
        no_concern = True
        no_concern_notes = ["normal_enzymes_do_not_exclude_fibrosis_cirrhosis"]
        domain_notes.append("must_not_state_liver_is_healthy")

    # Lead / co-lead / no_forced_lead selection (no technical_tiebreak)
    visible = [f for f in findings if f.role not in {"contextual", "supporting_evidence"}]
    # Sort by tier asc, then urgency rank, then finding_type for determinism
    urgency_rank = {"same_day": 0, "within_days": 1, "within_weeks": 2, "routine": 3}
    visible_sorted = sorted(
        visible,
        key=lambda f: (
            int(f.concern_tier),
            urgency_rank.get(f.urgency_time_band, 9),
            f.finding_type,
            f.finding_id,
        ),
    )

    lead_ids: List[str] = []
    co_lead_ids: List[str] = []
    presentation_mode = "principal"
    no_forced_lead = False

    if visible_sorted:
        # HEP-LEAD-1: F4 outranks injury at equal tier
        top_tier = visible_sorted[0].concern_tier
        top_band = visible_sorted[0].urgency_time_band
        same_band = [
            f
            for f in visible_sorted
            if f.concern_tier == top_tier and f.urgency_time_band == top_band
        ]

        # Prefer HEP-F4 within band
        f4 = [f for f in same_band if f.finding_type == "HEP-F4"]
        if f4:
            lead_ids = [f4[0].finding_id]
        elif top_band == "same_day" and len(same_band) > 1:
            # Same-day multi-domain co-equal group — no internal ranking beyond time band
            # Haematology same-day with hepatic within_days → haem leads on time band
            lead_ids = [same_band[0].finding_id]
            if len(same_band) > 1:
                co_lead_ids = [f.finding_id for f in same_band[1:]]
                presentation_mode = "co_lead"
        elif len(same_band) >= 3:
            no_forced_lead = True
            presentation_mode = "no_forced_lead"
            lead_ids = []
            co_lead_ids = []
        elif len(same_band) == 2 and same_band[0].domain != same_band[1].domain:
            # Ordinary co-lead eligible (HEP-AS-9)
            lead_ids = [same_band[0].finding_id]
            co_lead_ids = [same_band[1].finding_id]
            presentation_mode = "co_lead"
        elif len(same_band) == 2 and {same_band[0].finding_type, same_band[1].finding_type} == {
            "HEP-F1",
            "HEP-F10",
        } or (
            len(same_band) == 2
            and "HEP-F10" in {same_band[0].finding_type, same_band[1].finding_type}
        ):
            lead_ids = [same_band[0].finding_id]
            co_lead_ids = [same_band[1].finding_id]
            presentation_mode = "co_lead"
        else:
            lead_ids = [same_band[0].finding_id]

        # Update presentation_state / roles on findings
        updated: List[ClinicalFinding] = []
        lead_set = set(lead_ids)
        co_set = set(co_lead_ids)
        for f in findings:
            if no_forced_lead and f.finding_id in {x.finding_id for x in same_band}:
                updated.append(
                    f.model_copy(
                        update={
                            "presentation_state": "no_forced_lead",
                            "role": "independent_secondary",
                        }
                    )
                )
            elif f.finding_id in lead_set:
                updated.append(
                    f.model_copy(
                        update={
                            "presentation_state": "principal",
                            "role": "principal_concern",
                        }
                    )
                )
            elif f.finding_id in co_set:
                updated.append(
                    f.model_copy(
                        update={
                            "presentation_state": "co_lead",
                            "role": "co_lead",
                        }
                    )
                )
            else:
                updated.append(f)
        findings = updated

        # Cross-domain: platelets <50 same-day outranks hepatic within_days on time band
        haem_same_day = [
            f for f in findings if f.domain == "haematology" and f.urgency_time_band == "same_day"
        ]
        hepatic_non_same = [
            f for f in findings if f.domain == "hepatic" and f.urgency_time_band != "same_day"
        ]
        if haem_same_day and hepatic_non_same:
            lead_ids = [haem_same_day[0].finding_id]
            co_lead_ids = [hepatic_non_same[0].finding_id]
            presentation_mode = "co_lead"
            refreshed: List[ClinicalFinding] = []
            for f in findings:
                if f.finding_id == lead_ids[0]:
                    refreshed.append(
                        f.model_copy(
                            update={
                                "presentation_state": "principal",
                                "role": "principal_concern",
                            }
                        )
                    )
                elif f.finding_id in co_lead_ids:
                    refreshed.append(
                        f.model_copy(
                            update={
                                "presentation_state": "co_lead",
                                "role": "co_lead",
                            }
                        )
                    )
                else:
                    refreshed.append(f)
            findings = refreshed

    # Deterministic ordering: tier, urgency, finding_id
    findings = sorted(
        findings,
        key=lambda f: (
            int(f.concern_tier),
            urgency_rank.get(f.urgency_time_band, 9),
            f.finding_type,
            f.finding_id,
        ),
    )

    return ConsolidatedConcernSet(
        contract_version=stamp.contract_version,
        ruleset_version=stamp.ruleset_version,
        compile_run_id=stamp.compile_run_id,
        prioritisation_package_version=stamp.package_version,
        prioritisation_package_hash=stamp.package_hash,
        findings=findings,
        lead_finding_ids=lead_ids,
        co_lead_finding_ids=co_lead_ids,
        presentation_mode=presentation_mode,  # type: ignore[arg-type]
        no_forced_lead=no_forced_lead,
        no_concern=no_concern,
        no_concern_notes=no_concern_notes,
        domain_notes=domain_notes,
        fib_4_computed=fib_4_computed,
        fib_4_displayed=fib_4_displayed,
        quarantine_notes=quarantine_notes,
    )
