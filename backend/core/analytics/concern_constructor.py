"""
CLIN-PRIORITY-CORE-1 — Concern construction service (six-domain Checkpoint 2).

Consumes already-fired signal results and biomarker values; constructs
ConsolidatedConcernSet. Does not change SignalEvaluator / activation.
Never calls fib_4 for fibrosis classification. Never computes CV-risk %.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence, Set, Tuple

from core.analytics.concern_helpers import (
    biomarker_value,
    build_finding,
    is_high,
    is_low,
    keys_matching,
    pregnancy_known,
    range_bounds,
    synthetic_key,
    tier0_flags,
    x_uln,
)
from core.analytics.prioritisation_registry import (
    LoadedPrioritisationPackage,
    load_prioritisation_package,
)
from core.models.clinical_finding import ClinicalFinding, ConsolidatedConcernSet

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
_ANC_SIGNAL_PREFIXES = ("signal_anc_", "signal_neutrophil_")
_WCC_SIGNAL_PREFIXES = ("signal_wcc_", "signal_wbc_")
_CRP_SIGNAL_PREFIXES = ("signal_crp_",)
_RENAL_SIGNAL_PREFIXES = (
    "signal_potassium_",
    "signal_k_",
    "signal_sodium_",
    "signal_na_",
    "signal_creatinine_",
    "signal_egfr_",
    "signal_calcium_",
    "signal_urea_",
    "signal_magnesium_",
)
_THYROID_SIGNAL_PREFIXES = ("signal_tsh_", "signal_ft4_", "signal_free_t4_", "signal_tpo_")
_LIPID_SIGNAL_PREFIXES = (
    "signal_triglyceride_",
    "signal_tg_",
    "signal_cholesterol_",
    "signal_tc_",
    "signal_non_hdl_",
    "signal_ldl_",
    "signal_hdl_",
    "signal_hba1c_",
    "signal_b12_",
    "signal_vitamin_d_",
)

URGENCY_RANK = {"same_day": 0, "within_days": 1, "within_weeks": 2, "routine": 3}


@dataclass
class PanelContext:
    biomarkers: Dict[str, Any]
    lab_ranges: Dict[str, Any]
    signal_results: List[Any]
    derived: Dict[str, Any]
    context: Dict[str, Any]
    priors: Dict[str, Any]
    compile_run_id: Optional[str]
    package: LoadedPrioritisationPackage

    # Hepatic analytes
    alt: Optional[float] = None
    ast: Optional[float] = None
    alp: Optional[float] = None
    ggt: Optional[float] = None
    bili: Optional[float] = None
    albumin: Optional[float] = None
    inr: Optional[float] = None

    # Haematology
    platelets: Optional[float] = None
    mcv: Optional[float] = None
    hb: Optional[float] = None
    anc: Optional[float] = None
    wcc: Optional[float] = None

    # Iron / inflammatory
    ferritin: Optional[float] = None
    tsat: Optional[float] = None
    tsat_derived: bool = False
    iron: Optional[float] = None
    tibc: Optional[float] = None
    transferrin: Optional[float] = None
    crp: Optional[float] = None

    # Renal / electrolyte
    potassium: Optional[float] = None
    sodium: Optional[float] = None
    creatinine: Optional[float] = None
    egfr: Optional[float] = None
    urea: Optional[float] = None
    magnesium: Optional[float] = None
    calcium_total: Optional[float] = None
    adjusted_calcium: Optional[float] = None
    albumin_for_ca: Optional[float] = None

    # Thyroid
    tsh: Optional[float] = None
    ft4: Optional[float] = None
    ft3: Optional[float] = None
    tpo: Optional[float] = None

    # Cardiometabolic / nutritional
    tg: Optional[float] = None
    tc: Optional[float] = None
    non_hdl: Optional[float] = None
    ldl: Optional[float] = None
    hdl: Optional[float] = None
    hba1c: Optional[float] = None
    b12: Optional[float] = None
    vitamin_d: Optional[float] = None

    # Ranges / flags populated in from_inputs
    alt_uln: Optional[float] = None
    ast_uln: Optional[float] = None
    alp_uln: Optional[float] = None
    ggt_uln: Optional[float] = None
    bili_uln: Optional[float] = None
    alb_lrl: Optional[float] = None
    plt_lrl: Optional[float] = None
    mcv_lrl: Optional[float] = None
    mcv_uln: Optional[float] = None
    ferritin_lrl: Optional[float] = None
    ferritin_uln: Optional[float] = None
    transferrin_lrl: Optional[float] = None
    crp_uln: Optional[float] = None
    anc_lrl: Optional[float] = None
    wcc_lrl: Optional[float] = None
    tsh_lrl: Optional[float] = None
    tsh_uln: Optional[float] = None
    ft4_lrl: Optional[float] = None
    ft4_uln: Optional[float] = None
    ft3_uln: Optional[float] = None
    tpo_uln: Optional[float] = None
    b12_lrl: Optional[float] = None
    b12_uln: Optional[float] = None

    sex: Optional[str] = None
    sex_assumption: Optional[str] = None

    hepatic_keys: List[str] = field(default_factory=list)
    plt_keys: List[str] = field(default_factory=list)
    mcv_keys: List[str] = field(default_factory=list)
    ferritin_keys: List[str] = field(default_factory=list)
    hb_keys: List[str] = field(default_factory=list)
    anc_keys: List[str] = field(default_factory=list)
    wcc_keys: List[str] = field(default_factory=list)
    crp_keys: List[str] = field(default_factory=list)
    renal_keys: List[str] = field(default_factory=list)
    thyroid_keys: List[str] = field(default_factory=list)
    lipid_keys: List[str] = field(default_factory=list)

    # Cross-domain state set during domain builds
    hepatic_present: bool = False
    hepatic_pattern: Optional[ClinicalFinding] = None
    nest_ferritin_under_hepatic: bool = False
    nest_mcv_mild_under_hepatic: bool = False
    iron_deficiency_anaemia: bool = False
    haem_same_day: bool = False
    suppress_haem_f1: bool = False
    suppress_mild_macrocytosis: bool = False
    suppress_macrocytosis_finding: bool = False
    suppress_mild_thrombocytopenia: bool = False
    suppress_lipid_finding: bool = False
    nest_lipid_under_thyroid: bool = False
    nest_macro_under_thyroid: bool = False
    crp_contextual_to_haem: bool = False
    calcium_insufficient_data: bool = False
    pancytopenia_finding: bool = False
    b12_aetiology_for_haem: bool = False

    @classmethod
    def from_inputs(
        cls,
        signal_results: Optional[Sequence[Any]],
        biomarkers: Optional[Dict[str, Any]],
        lab_ranges: Optional[Dict[str, Any]],
        derived: Optional[Dict[str, Any]],
        priors: Optional[Dict[str, Any]],
        context: Optional[Dict[str, Any]],
        package: LoadedPrioritisationPackage,
    ) -> "PanelContext":
        biomarkers = dict(biomarkers or {})
        lab_ranges = dict(lab_ranges or {})
        signal_results = list(signal_results or [])
        derived = dict(derived or {})
        context = dict(context or {})
        priors_merged = dict(priors or {})
        if isinstance(context.get("priors"), dict):
            priors_merged.update(context["priors"])

        ctx = cls(
            biomarkers=biomarkers,
            lab_ranges=lab_ranges,
            signal_results=signal_results,
            derived=derived,
            context=context,
            priors=priors_merged,
            compile_run_id=package.stamp.compile_run_id,
            package=package,
        )
        ctx._load_values()
        ctx._load_keys()
        ctx._precompute_consolidation()
        return ctx

    def _load_values(self) -> None:
        b = self.biomarkers
        self.alt = biomarker_value(b, "alt")
        self.ast = biomarker_value(b, "ast")
        self.alp = biomarker_value(b, "alp")
        self.ggt = biomarker_value(b, "ggt")
        self.bili = biomarker_value(b, "bilirubin")
        self.albumin = biomarker_value(b, "albumin")
        self.inr = biomarker_value(b, "inr")

        self.platelets = biomarker_value(b, "platelets")
        if self.platelets is None:
            self.platelets = biomarker_value(b, "plt")
        self.mcv = biomarker_value(b, "mcv")
        self.hb = biomarker_value(b, "hgb")
        if self.hb is None:
            self.hb = biomarker_value(b, "hb")
        self.anc = biomarker_value(b, "anc")
        self.wcc = biomarker_value(b, "wcc")

        self.ferritin = biomarker_value(b, "ferritin")
        self.tsat = biomarker_value(b, "tsat")
        if self.tsat is None:
            self.tsat = biomarker_value(b, "transferrin_saturation")
        self.iron = biomarker_value(b, "iron")
        self.tibc = biomarker_value(b, "tibc")
        if self.tsat is None and self.iron is not None and self.tibc is not None and self.tibc > 0:
            self.tsat = (self.iron / self.tibc) * 100.0
            self.tsat_derived = True
        self.transferrin = biomarker_value(b, "transferrin")
        self.crp = biomarker_value(b, "crp")

        self.potassium = biomarker_value(b, "potassium")
        if self.potassium is None:
            self.potassium = biomarker_value(b, "k")
        self.sodium = biomarker_value(b, "sodium")
        if self.sodium is None:
            self.sodium = biomarker_value(b, "na")
        self.creatinine = biomarker_value(b, "creatinine")
        self.egfr = biomarker_value(b, "egfr")
        self.urea = biomarker_value(b, "urea")
        self.magnesium = biomarker_value(b, "magnesium")
        self.calcium_total = biomarker_value(b, "calcium")
        self.adjusted_calcium = biomarker_value(b, "adjusted_calcium")
        self.albumin_for_ca = self.albumin

        self.tsh = biomarker_value(b, "tsh")
        self.ft4 = biomarker_value(b, "free_t4")
        if self.ft4 is None:
            self.ft4 = biomarker_value(b, "ft4")
        self.ft3 = biomarker_value(b, "free_t3")
        if self.ft3 is None:
            self.ft3 = biomarker_value(b, "ft3")
        self.tpo = biomarker_value(b, "tpo")

        self.tg = biomarker_value(b, "triglycerides")
        if self.tg is None:
            self.tg = biomarker_value(b, "tg")
        self.tc = biomarker_value(b, "total_cholesterol")
        if self.tc is None:
            self.tc = biomarker_value(b, "tc")
        self.non_hdl = biomarker_value(b, "non_hdl")
        self.ldl = biomarker_value(b, "ldl")
        self.hdl = biomarker_value(b, "hdl")
        self.hba1c = biomarker_value(b, "hba1c")
        self.b12 = biomarker_value(b, "b12")
        self.vitamin_d = biomarker_value(b, "vitamin_d")

        lr = self.lab_ranges
        _, self.alt_uln = range_bounds(lr, "alt")
        _, self.ast_uln = range_bounds(lr, "ast")
        _, self.alp_uln = range_bounds(lr, "alp")
        _, self.ggt_uln = range_bounds(lr, "ggt")
        _, self.bili_uln = range_bounds(lr, "bilirubin")
        self.alb_lrl, _ = range_bounds(lr, "albumin")
        self.plt_lrl, _ = range_bounds(lr, "platelets")
        if self.plt_lrl is None:
            self.plt_lrl, _ = range_bounds(lr, "plt")
        self.mcv_lrl, self.mcv_uln = range_bounds(lr, "mcv")
        self.ferritin_lrl, self.ferritin_uln = range_bounds(lr, "ferritin")
        self.transferrin_lrl, _ = range_bounds(lr, "transferrin")
        _, self.crp_uln = range_bounds(lr, "crp")
        self.anc_lrl, _ = range_bounds(lr, "anc")
        if self.anc_lrl is None:
            self.anc_lrl = 1.5
        self.wcc_lrl, _ = range_bounds(lr, "wcc")
        if self.wcc_lrl is None:
            self.wcc_lrl = 4.0
        self.tsh_lrl, self.tsh_uln = range_bounds(lr, "tsh")
        if self.tsh_lrl is None:
            self.tsh_lrl = 0.27
        if self.tsh_uln is None:
            self.tsh_uln = 4.2
        self.ft4_lrl, self.ft4_uln = range_bounds(lr, "free_t4")
        if self.ft4_lrl is None:
            self.ft4_lrl, self.ft4_uln = range_bounds(lr, "ft4")
        if self.ft4_lrl is None:
            self.ft4_lrl, self.ft4_uln = 12.0, 22.0
        _, self.ft3_uln = range_bounds(lr, "free_t3")
        if self.ft3_uln is None:
            self.ft3_uln = 6.8
        _, self.tpo_uln = range_bounds(lr, "tpo")
        self.b12_lrl, self.b12_uln = range_bounds(lr, "b12")
        if self.b12_lrl is None:
            self.b12_lrl, self.b12_uln = 180.0, 900.0

        sex_raw = self.context.get("sex") or self.context.get("biological_sex")
        if isinstance(sex_raw, str) and sex_raw.strip():
            s = sex_raw.strip().lower()
            if s in {"m", "male"}:
                self.sex = "male"
            elif s in {"f", "female"}:
                self.sex = "female"
            else:
                self.sex = None
        else:
            self.sex = None

    def _load_keys(self) -> None:
        sr = self.signal_results
        self.hepatic_keys = keys_matching(sr, _HEPATIC_SIGNAL_PREFIXES)
        self.plt_keys = keys_matching(sr, _PLT_SIGNAL_PREFIXES)
        self.mcv_keys = keys_matching(sr, _MCV_SIGNAL_PREFIXES)
        self.ferritin_keys = keys_matching(sr, _FERRITIN_SIGNAL_PREFIXES)
        self.hb_keys = keys_matching(sr, _HB_SIGNAL_PREFIXES)
        self.anc_keys = keys_matching(sr, _ANC_SIGNAL_PREFIXES)
        self.wcc_keys = keys_matching(sr, _WCC_SIGNAL_PREFIXES)
        self.crp_keys = keys_matching(sr, _CRP_SIGNAL_PREFIXES)
        self.renal_keys = keys_matching(sr, _RENAL_SIGNAL_PREFIXES)
        self.thyroid_keys = keys_matching(sr, _THYROID_SIGNAL_PREFIXES)
        self.lipid_keys = keys_matching(sr, _LIPID_SIGNAL_PREFIXES)

    def _precompute_consolidation(self) -> None:
        """Cross-domain absorption flags before domain builders run."""
        anaemia_flag, _, _ = self.anaemia()
        ferritin_low = is_low(self.ferritin, self.ferritin_lrl)
        mcv_band = self.mcv_band()
        mild_macro = mcv_band == "mild_macrocytosis"
        any_macro = bool(mcv_band and "macro" in mcv_band)
        b12_low = self.b12 is not None and self.b12_lrl is not None and self.b12 < self.b12_lrl
        b12_in_range = (
            self.b12 is not None
            and self.b12_lrl is not None
            and self.b12_uln is not None
            and self.b12_lrl <= self.b12 <= self.b12_uln
        )
        tsh_abnormal = self.tsh is not None and (
            self.tsh > self.tsh_uln or self.tsh < self.tsh_lrl
        )
        lipid_elevated = any(
            v is not None and v > lim
            for v, lim in (
                (self.tc, 5.0),
                (self.non_hdl, 4.0),
                (self.ldl, 3.0),
                (self.tg, 2.3),
            )
        )
        crp_high = (
            is_high(self.crp, self.crp_uln)
            if self.crp_uln is not None
            else (self.crp is not None and self.crp > 5)
        )
        if ferritin_low and anaemia_flag:
            self.suppress_haem_f1 = True
            self.iron_deficiency_anaemia = True
        if b12_low and (anaemia_flag or any_macro):
            self.suppress_haem_f1 = True
            self.suppress_macrocytosis_finding = True
        if b12_in_range and any_macro:
            self.suppress_macrocytosis_finding = True
        if tsh_abnormal and mild_macro:
            # THY-AS-11 dual-role; do not absorb when other Tier-1 domains present (XD-AS-10)
            if not (self.egfr is not None and self.egfr < 60):
                self.nest_macro_under_thyroid = True
                self.suppress_mild_macrocytosis = True
                self.suppress_macrocytosis_finding = True
        specialist_lipid = (self.tc is not None and self.tc > 9.0) or (
            self.non_hdl is not None and self.non_hdl > 7.5
        )
        if tsh_abnormal and lipid_elevated and not specialist_lipid:
            ft4_low = (
                self.ft4 is not None
                and self.ft4_lrl is not None
                and self.ft4 < self.ft4_lrl
            )
            # CN-AS-10: overt hypo + lipid — both stand as CN-F3 + THY-F1
            if not (ft4_low and self.tsh is not None and self.tsh >= 10):
                self.nest_lipid_under_thyroid = True
                self.suppress_lipid_finding = True
            else:
                self.context["_promote_lipid_with_overt_thyroid"] = True
        if crp_high and self.platelets is not None and self.platelets < 50:
            self.crp_contextual_to_haem = True
        if b12_low:
            self.b12_aetiology_for_haem = True
        alb_absent = self.context.get("albumin_absent") is True or (
            self.albumin is None and "albumin" not in self.biomarkers
        )
        if (
            self.adjusted_calcium is None
            and self.calcium_total is not None
            and (alb_absent or self.albumin is None)
        ):
            self.calcium_insufficient_data = True

    def anaemia(self) -> Tuple[bool, Optional[str], List[str]]:
        """Return (is_anaemic, severity_note, caveats). Sex-absent uses female threshold + assumption."""
        if self.hb is None:
            return False, None, []
        caveats: List[str] = []
        if self.sex == "male":
            threshold = 130.0
        elif self.sex == "female":
            threshold = 120.0
        else:
            threshold = 120.0
            self.sex_assumption = "female_threshold_applied"
            caveats.append("sex_absent_female_threshold_assumption_stated")
        if self.hb < threshold:
            sev = "severe" if self.hb < 70 else "mild"
            if self.sex is None:
                # XD-AS-20b: indeterminate + stated assumption
                return True, "indeterminate", caveats
            return True, sev, caveats
        return False, None, caveats

    def mcv_band(self) -> Optional[str]:
        if self.mcv is None or self.mcv_uln is None:
            if self.mcv is not None and self.mcv_lrl is not None and self.mcv < self.mcv_lrl:
                return "microcytosis"
            return None
        if self.mcv > self.mcv_uln:
            if self.mcv <= 105:
                return "mild_macrocytosis"
            if self.mcv <= 115:
                return "moderate_macrocytosis"
            return "marked_macrocytosis"
        if self.mcv_lrl is not None and self.mcv < self.mcv_lrl:
            return "microcytosis"
        return None


@dataclass
class DomainBuild:
    findings: List[ClinicalFinding] = field(default_factory=list)
    nested_labels: List[str] = field(default_factory=list)
    domain_notes: List[str] = field(default_factory=list)
    no_concern: bool = False
    no_concern_notes: List[str] = field(default_factory=list)


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


def _bf(ctx: PanelContext, **kwargs: Any) -> ClinicalFinding:
    kwargs.setdefault("compile_run_id", ctx.compile_run_id)
    return build_finding(**kwargs)


# ---------------------------------------------------------------------------
# Hepatic
# ---------------------------------------------------------------------------


def build_hepatic(ctx: PanelContext) -> DomainBuild:
    out = DomainBuild()
    alt, ast, alp, ggt, bili = ctx.alt, ctx.ast, ctx.alp, ctx.ggt, ctx.bili
    albumin, inr = ctx.albumin, ctx.inr
    platelets, mcv, hb = ctx.platelets, ctx.mcv, ctx.hb
    ferritin, tsat, transferrin = ctx.ferritin, ctx.tsat, ctx.transferrin

    x_alt = x_uln(alt, ctx.alt_uln)
    x_ast = x_uln(ast, ctx.ast_uln)
    x_alp = x_uln(alp, ctx.alp_uln)
    x_bili = x_uln(bili, ctx.bili_uln)

    alt_high = is_high(alt, ctx.alt_uln)
    ast_high = is_high(ast, ctx.ast_uln)
    alp_high = is_high(alp, ctx.alp_uln)
    ggt_high = is_high(ggt, ctx.ggt_uln)
    bili_high = is_high(bili, ctx.bili_uln)
    albumin_low = is_low(albumin, ctx.alb_lrl)
    platelets_low = is_low(platelets, ctx.plt_lrl)
    anaemia_flag, _, _ = ctx.anaemia()
    transferrin_low = is_low(transferrin, ctx.transferrin_lrl)

    alp_present = alp is not None and ctx.alp_uln is not None
    alp_absent = "alp" not in ctx.biomarkers and alp is None
    if ctx.context.get("alp_absent") is True:
        alp_absent = True
        alp_present = False
    ggt_present = ggt is not None
    ggt_absent = ctx.context.get("ggt_absent") is True or (
        "ggt" not in ctx.biomarkers and ggt is None
    )

    r_value: Optional[float] = None
    r_class: Optional[str] = None
    if (
        not alp_absent
        and alt is not None
        and alp is not None
        and ctx.alt_uln
        and ctx.alp_uln
        and alt_high
        and alp_high
    ):
        r_value = (alt / ctx.alt_uln) / (alp / ctx.alp_uln)
        r_class = _r_classification(r_value)
    elif alt_high and not alp_high and not alp_absent:
        r_class = "hepatocellular"

    ast_alt_ratio: Optional[float] = None
    if ast is not None and alt is not None and alt > 0:
        ast_alt_ratio = ast / alt

    abnormal_hepatic = any([alt_high, ast_high, alp_high, ggt_high, bili_high])
    enzyme_abnormal = any([alt_high, ast_high, alp_high, ggt_high])
    synthetic = abnormal_hepatic and (
        albumin_low or (inr is not None and inr > 1.5 and not ctx.context.get("anticoagulated"))
    )

    nested_labels: List[str] = []
    missing_notes: List[str] = []
    caveats: List[str] = []
    prohibited: List[str] = []
    if albumin is None and inr is None and enzyme_abnormal:
        missing_notes.append("albumin_inr_not_assessable")
    if ast is None and alt_high:
        caveats.append("confidence_reduced_ast_absent")

    pattern_keys = list(ctx.hepatic_keys)
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

    isolated_alp = (
        alp_high
        and not alt_high
        and not ast_high
        and not bili_high
        and (ggt is not None and not ggt_high or ggt_absent)
    )
    isolated_ggt = ggt_high and not alt_high and not ast_high and not alp_high and not bili_high
    isolated_bili = bili_high and not alt_high and not ast_high and not alp_high and not ggt_high

    platelets_below_50 = platelets is not None and platelets < 50
    fibrosis_dominant = (
        ast_alt_ratio is not None
        and ast_alt_ratio > 1
        and platelets_low
        and not platelets_below_50
        and not alp_high
        and not bili_high
        and not ggt_high
        and (
            not alt_high
            or (x_alt is not None and x_alt < 3)  # mild ALT absorbed into F5 (XD-AS-18)
        )
    )

    hepatic_pattern: Optional[ClinicalFinding] = None

    if synthetic:
        keys = pattern_keys or [synthetic_key("HEP-F4", "synthetic_dysfunction")]
        t0 = tier0_flags(True)
        hepatic_pattern = _bf(
            ctx,
            domain="hepatic",
            finding_type="HEP-F4",
            label="hepatic_synthetic_dysfunction",
            keys=keys,
            biomarkers=pattern_biomarkers + (["albumin"] if albumin_low else []),
            urgency="same_day",
            severity="severe",
            tier=0,
            role="principal_concern",
            caveats=["albumin_non_hepatic_cause_mandatory"] if albumin_low else [],
            prohibited=["assert_albumin_cause_hepatic_without_exclusion"],
            rule_ids=["HEP-F4", "HEP-LEAD-1", "XD-T0-2"],
            actionability="immediate",
            missing_data_notes=missing_notes,
            **t0,
        )
    elif isolated_alp:
        origin = "non_hepatic_likely" if (ggt_present and not ggt_high) else "undetermined"
        keys = pattern_keys or [synthetic_key("HEP-F7", "isolated_alp")]
        hepatic_pattern = _bf(
            ctx,
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
            missing_data_notes=(["ggt_absent"] if ggt_absent else []),
            missing_data_state="not_assessable" if ggt_absent else "none",
        )
    elif isolated_ggt:
        keys = pattern_keys or [synthetic_key("HEP-F8", "isolated_ggt")]
        if ggt is not None and ggt <= 100:
            urg, tier = "routine", 2
        else:
            urg, tier = "within_weeks", 1
        hepatic_pattern = _bf(
            ctx,
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
        )
    elif isolated_bili and not anaemia_flag:
        keys = pattern_keys or [synthetic_key("HEP-F6", "gilbert_pattern")]
        marked_bili = (x_bili is not None and x_bili >= 3) or (
            bili is not None and bili >= 50
        )
        if marked_bili:
            urg_b, tier_b, action_b = "within_weeks", 1, "discuss_investigate"
        else:
            urg_b, tier_b, action_b = "routine", 2, "reassurance_available"
        hepatic_pattern = _bf(
            ctx,
            domain="hepatic",
            finding_type="HEP-F6",
            label="isolated_hyperbilirubinaemia_gilbert_pattern",
            keys=keys,
            biomarkers=["bilirubin"],
            urgency=urg_b,
            severity=None,
            tier=tier_b,
            role="principal_concern",
            caveats=["split_bilirubin_if_unmeasured"],
            prohibited=["assert_gilberts_without_conjugated_fraction"],
            rule_ids=["HEP-F6", "HEP-IND-4"],
            actionability=action_b,
            missing_data_notes=["conjugated_fraction_unmeasured"],
            missing_data_state="not_assessable",
        )
    elif isolated_bili and anaemia_flag:
        keys = sorted(set(pattern_keys + ctx.hb_keys)) or [
            synthetic_key("HEP-BILI-ANAEMIA", "haemolysis_consider")
        ]
        hepatic_pattern = _bf(
            ctx,
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
        )
        # Anaemia is constituent of the hepatic haemolysis-consider finding (HEP-AS-7)
        ctx.suppress_haem_f1 = True
    elif alt_high and alp_absent:
        keys = pattern_keys or [synthetic_key("HEP-F9", "pattern_undetermined")]
        urg, tier = _urgency_and_tier_from_enzyme(x_alt, x_ast, alt, ast)
        t0 = tier0_flags(True) if urg == "same_day" else {}
        hepatic_pattern = _bf(
            ctx,
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
            rule_ids=["HEP-F9", "HEP-IND-1"],
            actionability="discuss_investigate",
            **t0,
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
        if r_class == "hepatocellular" or (r_class is None and alt_high and not alp_high):
            ftype, label = "HEP-F1", "consolidated_hepatocellular_enzyme_elevation"
        elif r_class == "cholestatic":
            ftype, label = "HEP-F2", "cholestatic_injury_pattern"
        elif r_class == "mixed":
            ftype, label = "HEP-F3", "mixed_injury_pattern"
        else:
            ftype, label = "HEP-F1", "consolidated_hepatocellular_enzyme_elevation"

        keys = pattern_keys or [synthetic_key(ftype, "enzyme_pattern")]
        for bid in pattern_biomarkers:
            nested_labels.append(f"{bid}_abnormal")

        urg, tier = _urgency_and_tier_from_enzyme(x_alt, x_ast, alt, ast)
        hys_law = (
            ((x_alt is not None and x_alt >= 3) or (x_ast is not None and x_ast >= 3))
            and x_bili is not None
            and x_bili >= 2
            and (x_alp is None or x_alp < 2)
        )
        if hys_law:
            urg, tier = "same_day", 0
            ftype, label = "HEP-F1", "consolidated_hepatocellular_enzyme_elevation"

        # Severity from the worse of ALT/AST (XD-AS-3 marked via AST)
        sev_candidates = [
            _severity_alt_ast(x_alt, alt),
            _severity_alt_ast(x_ast, ast),
        ]
        order = {"mild": 1, "moderate": 2, "marked": 3, "severe": 4}
        sev = None
        for candidate in sev_candidates:
            if candidate is None:
                continue
            if sev is None or order.get(candidate, 0) > order.get(sev, 0):
                sev = candidate
        if hys_law:
            sev = "severe"

        t0 = tier0_flags(True) if urg == "same_day" else {}
        action = "immediate" if urg == "same_day" else "discuss_investigate"
        if urg == "within_weeks" and tier == 1:
            prohibited.append("describe_as_urgent_merely_because_tier1")
        hepatic_pattern = _bf(
            ctx,
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
            rule_ids=["HEP-CONS-1", "HEP-P2", "XD-HEP-FLOOR-1", ftype],
            nested_labels=nested_labels,
            actionability=action,
            confidence="reduced_ast_absent" if ast is None and alt_high else None,
            **t0,
        )

    # HEP-F5 fibrosis — never fib_4
    fibrosis: Optional[ClinicalFinding] = None
    fibrosis_pattern = False
    if ast_alt_ratio is not None and ast_alt_ratio > 1:
        fibrosis_pattern = True
    if platelets_low and not platelets_below_50 and (abnormal_hepatic or fibrosis_pattern):
        fibrosis_pattern = True
    if (
        ast_alt_ratio is not None
        and ast_alt_ratio > 1
        and platelets is not None
        and platelets_low
        and not platelets_below_50
    ):
        fibrosis_pattern = True

    if fibrosis_pattern and not platelets_below_50:
        f5_meta = ctx.package.finding_types.get("HEP-F5", {})
        prov_key = str(
            f5_meta.get("biomarker_derived_provenance_key")
            or synthetic_key("HEP-F5", "ast_alt_platelets_pattern")
        )
        keys = sorted(set(ctx.hepatic_keys + ctx.plt_keys + [prov_key]))
        fibrosis = _bf(
            ctx,
            domain="hepatic",
            finding_type="HEP-F5",
            label="suspected_advanced_fibrosis",
            keys=keys,
            biomarkers=[
                b
                for b in ("ast", "alt", "platelets")
                if biomarker_value(ctx.biomarkers, b) is not None
            ],
            urgency="within_weeks",
            severity="ast_alt_gt_1_plus_platelets",
            tier=1,
            role="principal_concern",
            prohibited=["fib_4_computed", "fib_4_displayed"],
            quarantine_flags=["XD-QUAR-1", "R3"],
            dependency_flags=["REGULATORY_DEPENDENCY_R3"],
            rule_ids=["HEP-F5", "XD-QUAR-1"],
            actionability="investigate",
        )
        # Platelets absorbed into HEP-F5 when >=50 (HEP-AS-10); independent only if <50
        if platelets_low:
            ctx.suppress_mild_thrombocytopenia = True

    # Ferritin nesting decision (IRIN owns overload emission)
    ferritin_high = is_high(ferritin, ctx.ferritin_uln)
    if ferritin_high and (tsat is None or tsat <= 45) and hepatic_pattern is not None:
        ctx.nest_ferritin_under_hepatic = True

    mcv_band = ctx.mcv_band()
    if mcv_band == "mild_macrocytosis" and hepatic_pattern is not None:
        ctx.nest_mcv_mild_under_hepatic = True

    if hepatic_pattern is not None:
        extra = list(hepatic_pattern.nested_constituent_labels)
        if ctx.nest_mcv_mild_under_hepatic:
            extra.append("mcv_mild_macrocytosis")
        if transferrin_low:
            extra.append("transferrin_low")
        if ctx.nest_ferritin_under_hepatic:
            extra.append("ferritin_contextual")
        if extra != list(hepatic_pattern.nested_constituent_labels):
            hepatic_pattern = hepatic_pattern.model_copy(
                update={"nested_constituent_labels": extra}
            )
        out.findings.append(hepatic_pattern)
        ctx.hepatic_pattern = hepatic_pattern
        ctx.hepatic_present = True

    if fibrosis is not None:
        if hepatic_pattern is None:
            out.findings.append(fibrosis)
            ctx.hepatic_present = True
        else:
            sev = hepatic_pattern.severity_band
            if sev in {"marked", "severe"}:
                # XD-AS-3: platelets nested under hepatic, not independent F5/HAEM
                extra = list(hepatic_pattern.nested_constituent_labels)
                if "platelets_contextual" not in extra:
                    extra.append("platelets_contextual")
                hepatic_pattern = hepatic_pattern.model_copy(
                    update={"nested_constituent_labels": extra}
                )
                for i, f in enumerate(out.findings):
                    if f.finding_id == hepatic_pattern.finding_id or (
                        f.finding_type == hepatic_pattern.finding_type
                        and f.domain == "hepatic"
                    ):
                        out.findings[i] = hepatic_pattern
                        break
                ctx.hepatic_pattern = hepatic_pattern
                ctx.suppress_mild_thrombocytopenia = True
            elif fibrosis_dominant:
                # Mild enzyme + fibrosis pattern → F5 alone (XD-AS-18)
                out.findings = [
                    f
                    for f in out.findings
                    if not (
                        f.domain == "hepatic"
                        and f.finding_type.startswith("HEP-F")
                        and f.finding_type != "HEP-F5"
                    )
                ]
                out.findings.append(fibrosis)
                ctx.hepatic_pattern = None
                ctx.hepatic_present = True
            else:
                out.findings.append(fibrosis)

    hepatic_panel_present = any(
        biomarker_value(ctx.biomarkers, bid) is not None
        for bid in ("alt", "ast", "alp", "ggt", "bilirubin", "albumin")
    )
    if not out.findings and hepatic_panel_present and not abnormal_hepatic:
        out.no_concern = True
        out.no_concern_notes = ["normal_enzymes_do_not_exclude_fibrosis_cirrhosis"]
        out.domain_notes.append("must_not_state_liver_is_healthy")

    return out


# ---------------------------------------------------------------------------
# Iron / inflammatory
# ---------------------------------------------------------------------------


def build_iron(ctx: PanelContext) -> DomainBuild:
    out = DomainBuild()
    ferritin = ctx.ferritin
    tsat = ctx.tsat
    crp = ctx.crp
    ferritin_high = is_high(ferritin, ctx.ferritin_uln)
    ferritin_low = is_low(ferritin, ctx.ferritin_lrl)
    ferritin_in_range = (
        ferritin is not None
        and not ferritin_high
        and not ferritin_low
        and ctx.ferritin_lrl is not None
        and ctx.ferritin_uln is not None
    )
    crp_high = is_high(crp, ctx.crp_uln) if ctx.crp_uln is not None else (
        crp is not None and crp > 5
    )
    anaemia_flag, _, anaemia_caveats = ctx.anaemia()
    platelets_below_50 = ctx.platelets is not None and ctx.platelets < 50

    # CRP + platelets <50 → haem primary, CRP contextual (IRIN-OV-5)
    crp_contextual_only = crp_high and platelets_below_50

    # Low ferritin + low Hb → IRIN-F2; suppress separate HAEM-F1
    if ferritin_low and anaemia_flag:
        keys = sorted(set(ctx.ferritin_keys + ctx.hb_keys)) or [
            synthetic_key("IRIN-F2", "iron_deficiency_anaemia")
        ]
        biomarkers = ["ferritin", "hgb"]
        nested = []
        mcv_band = ctx.mcv_band()
        if mcv_band:
            nested.append(mcv_band)
            biomarkers.append("mcv")
        out.findings.append(
            _bf(
                ctx,
                domain="iron_inflammatory",
                finding_type="IRIN-F2",
                label="iron_deficiency_anaemia",
                keys=keys,
                biomarkers=biomarkers,
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                nested_labels=nested,
                prohibited=["separate_haem_f1_with_iron_deficiency_anaemia"],
                rule_ids=["IRIN-F2", "IRIN-OV-3"],
                actionability="investigate",
                caveats=anaemia_caveats,
            )
        )
        ctx.iron_deficiency_anaemia = True
        ctx.suppress_haem_f1 = True

    # TSAT>45 + raised ferritin → IRIN-F3 (never HEP-F10)
    elif ferritin_high and tsat is not None and tsat > 45:
        keys = sorted(set(ctx.ferritin_keys + ctx.hepatic_keys)) or [
            synthetic_key("IRIN-F3", "possible_iron_overload")
        ]
        out.findings.append(
            _bf(
                ctx,
                domain="iron_inflammatory",
                finding_type="IRIN-F3",
                label="possible_iron_overload",
                keys=keys,
                biomarkers=["ferritin", "transferrin_saturation"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="co_lead" if ctx.hepatic_present else "principal_concern",
                quarantine_flags=["disease_name_haemochromatosis", "R4"],
                prohibited=[
                    "name_haemochromatosis",
                    "name_haemochromatosis_to_consumer",
                    "magnitude_promote_ferritin",
                ],
                rule_ids=["IRIN-F3", "IRIN-OV-1", "IRIN-OV-7"],
                actionability="discuss_investigate",
                caveats=["tsat_derived"] if ctx.tsat_derived else None,
            )
        )

    # Raised ferritin, TSAT absent/underivable → IRIN-F8
    elif ferritin_high and tsat is None:
        keys = ctx.ferritin_keys or [synthetic_key("IRIN-F8", "ferritin_tsat_indeterminate")]
        out.findings.append(
            _bf(
                ctx,
                domain="iron_inflammatory",
                finding_type="IRIN-F8",
                label="raised_ferritin_tsat_indeterminate",
                keys=keys,
                biomarkers=["ferritin"],
                urgency="within_weeks",
                severity="indeterminate",
                tier=1,
                role="principal_concern",
                severity_indeterminate=True,
                missing_data_state="indeterminate_severity",
                missing_data_notes=[
                    "tsat_absent_and_underivable",
                    "tsat_requested",
                    "both_states_stated",
                ],
                prohibited=["default_to_inflammatory", "default_to_inflammatory_without_tsat"],
                rule_ids=["IRIN-F8"],
                actionability="investigate",
            )
        )

    # TSAT<=45 + ferritin high → IRIN-F4 unless nested under hepatic (IRIN-OV-6)
    elif ferritin_high and tsat is not None and tsat <= 45:
        if ctx.nest_ferritin_under_hepatic or ctx.hepatic_present:
            # absorbed — no independent IRIN-F3/F4
            pass
        else:
            keys = ctx.ferritin_keys or [synthetic_key("IRIN-F4", "raised_ferritin")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="iron_inflammatory",
                    finding_type="IRIN-F4",
                    label="raised_ferritin_inflammatory_or_dysmetabolic",
                    keys=keys,
                    biomarkers=["ferritin", "transferrin_saturation"],
                    urgency="routine",
                    severity="low",
                    tier=2,
                    role="principal_concern",
                    prohibited=["present_overload_concern_with_low_tsat"],
                    rule_ids=["IRIN-F4", "IRIN-OV-2"],
                    actionability="monitor",
                    caveats=["tsat_derived"] if ctx.tsat_derived else None,
                )
            )

    # In-range ferritin + CRP high + anaemia → IRIN-F5
    if ferritin_in_range and crp_high and anaemia_flag and not ctx.iron_deficiency_anaemia:
        keys = sorted(set(ctx.ferritin_keys + ctx.crp_keys + ctx.hb_keys)) or [
            synthetic_key("IRIN-F5", "masked_iron_deficiency")
        ]
        out.findings.append(
            _bf(
                ctx,
                domain="iron_inflammatory",
                finding_type="IRIN-F5",
                label="masked_iron_deficiency_inflammatory",
                keys=keys,
                biomarkers=["ferritin", "crp", "hgb"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                prohibited=["report_iron_status_as_normal", "report_iron_status_normal"],
                rule_ids=["IRIN-F5", "IRIN-OV-4"],
                actionability="investigate",
            )
        )
        ctx.suppress_haem_f1 = True

    # Isolated / persistent CRP
    if crp_high and not crp_contextual_only:
        persistent = False
        crp_history = ctx.priors.get("crp_history")
        if isinstance(crp_history, list) and len(crp_history) >= 3:
            persistent = True
        crp_priors = ctx.priors.get("crp")
        if isinstance(crp_priors, list) and len(crp_priors) >= 2:
            persistent = True
        elif isinstance(crp_priors, dict) and crp_priors.get("persistent"):
            persistent = True
        elif ctx.context.get("crp_persistent") is True:
            persistent = True

        already_f5 = any(f.finding_type == "IRIN-F5" for f in out.findings)
        if not already_f5:
            if persistent:
                keys = ctx.crp_keys or [synthetic_key("IRIN-F7", "persistent_inflammation")]
                out.findings.append(
                    _bf(
                        ctx,
                        domain="iron_inflammatory",
                        finding_type="IRIN-F7",
                        label="persistent_unexplained_inflammation",
                        keys=keys,
                        biomarkers=["crp"],
                        urgency="within_weeks",
                        severity="persistence_based",
                        tier=1,
                        role="principal_concern",
                        prohibited=["promote_on_height_alone"],
                        rule_ids=["IRIN-F7"],
                        actionability="investigate",
                    )
                )
            else:
                # Avoid duplicate if only supporting other findings without standalone need
                iron_primary = any(
                    f.finding_type in {"IRIN-F2", "IRIN-F3", "IRIN-F4", "IRIN-F5", "IRIN-F8"}
                    for f in out.findings
                )
                if not iron_primary:
                    keys = ctx.crp_keys or [synthetic_key("IRIN-F6", "raised_crp")]
                    out.findings.append(
                        _bf(
                            ctx,
                            domain="iron_inflammatory",
                            finding_type="IRIN-F6",
                            label="raised_crp",
                            keys=keys,
                            biomarkers=["crp"],
                            urgency="routine",
                            severity=None,
                            tier=2,
                            role="principal_concern",
                            prohibited=["escalate_isolated_crp_to_tier1"],
                            rule_ids=["IRIN-F6"],
                            actionability="monitor",
                        )
                    )
    elif crp_high and (crp_contextual_only or ctx.crp_contextual_to_haem):
        out.domain_notes.append("crp_contextual_to_haematology")
        ctx.crp_contextual_to_haem = True

    # Low ferritin without anaemia
    if ferritin_low and not anaemia_flag and not ctx.iron_deficiency_anaemia:
        keys = ctx.ferritin_keys or [synthetic_key("IRIN-F1", "iron_deficiency")]
        out.findings.append(
            _bf(
                ctx,
                domain="iron_inflammatory",
                finding_type="IRIN-F1",
                label="iron_deficiency_without_anaemia",
                keys=keys,
                biomarkers=["ferritin"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                rule_ids=["IRIN-F1"],
                actionability="investigate",
            )
        )

    iron_panel = any(
        biomarker_value(ctx.biomarkers, bid) is not None
        for bid in ("ferritin", "tsat", "iron", "tibc", "crp")
    )
    if (
        not out.findings
        and iron_panel
        and not ferritin_high
        and not ferritin_low
        and not crp_high
    ):
        out.no_concern = True
        out.no_concern_notes = [
            "normal_ferritin_does_not_exclude_deficiency_with_inflammation"
        ]

    return out


# ---------------------------------------------------------------------------
# Haematology
# ---------------------------------------------------------------------------


def build_haematology(ctx: PanelContext) -> DomainBuild:
    out = DomainBuild()
    platelets = ctx.platelets
    anc = ctx.anc
    wcc = ctx.wcc
    anaemia_flag, anaemia_sev, anaemia_caveats = ctx.anaemia()
    mcv_band = ctx.mcv_band()

    plt_lrl = ctx.plt_lrl if ctx.plt_lrl is not None else 150.0
    platelets_low = platelets is not None and platelets < plt_lrl
    platelets_below_50 = platelets is not None and platelets < 50
    platelets_below_20 = platelets is not None and platelets < 20
    anc_low = anc is not None and anc < ctx.anc_lrl
    anc_severe = anc is not None and anc < 0.5
    wcc_low = wcc is not None and wcc < ctx.wcc_lrl
    differential_absent = anc is None and (
        ctx.context.get("differential_absent") is True or "anc" not in ctx.biomarkers
    )

    lineages = 0
    if anaemia_flag:
        lineages += 1
    if platelets_low:
        lineages += 1
    if anc_low:
        lineages += 1

    # Multi-lineage (≥2) — unless severe thrombocytopenia alone path for HAEM-AS-1
    if lineages >= 2 and not platelets_below_20:
        keys = sorted(
            set(ctx.hb_keys + ctx.plt_keys + ctx.anc_keys + ctx.mcv_keys)
        ) or [synthetic_key("HAEM-F10", "multi_lineage")]
        biomarkers = []
        nested = []
        if anaemia_flag:
            biomarkers.append("hgb")
            nested.append("anaemia")
        if platelets_low:
            biomarkers.append("platelets")
            nested.append("thrombocytopenia")
        if anc_low:
            biomarkers.append("anc")
            nested.append("neutropenia")
        if mcv_band:
            nested.append(mcv_band)
            biomarkers.append("mcv")
        if lineages >= 3:
            urg, tier, sev = "same_day", 0, "severe_three_lineage"
            t0 = tier0_flags(True)
            ctx.haem_same_day = True
            ctx.pancytopenia_finding = True
        else:
            urg, tier, sev = "within_days", 1, "multi_lineage"
            t0 = {}
        if ctx.b12_aetiology_for_haem:
            nested.append("b12_aetiology")
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F10",
                label="multi_lineage_cytopenia",
                keys=keys,
                biomarkers=biomarkers,
                urgency=urg,
                severity=sev,
                tier=tier,
                role="principal_concern",
                nested_labels=nested,
                caveats=["no_film_standing_limitation"],
                prohibited=["present_as_separate_low_tier_cytopenias"],
                rule_ids=["HAEM-F10", "HAEM-OV-1", "XD-AS-8"],
                actionability="immediate" if urg == "same_day" else "investigate",
                **t0,
            )
        )
        return out

    # Severe thrombocytopenia <20 → HAEM-F4 same_day (HAEM-AS-1)
    if platelets_below_20:
        keys = ctx.plt_keys or [synthetic_key("HAEM-F4", "severe_thrombocytopenia")]
        t0 = tier0_flags(True)
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F4",
                label="severe_thrombocytopenia",
                keys=keys,
                biomarkers=["platelets"],
                urgency="same_day",
                severity="severe",
                tier=0,
                role="principal_concern",
                caveats=["pseudothrombocytopenia_confirmation_mandatory", "no_film_standing_limitation"],
                prohibited=["assert_count_genuine_or_artefact_without_repeat"],
                rule_ids=["HAEM-F4", "HAEM-U-SD-1", "HAEM-AS-1"],
                actionability="immediate",
                **t0,
            )
        )
        ctx.haem_same_day = True
        # Separate mild anaemia does not compete
        if anaemia_flag and not ctx.suppress_haem_f1:
            keys_a = ctx.hb_keys or [synthetic_key("HAEM-F1", "mild_anaemia")]
            nested = []
            if mcv_band:
                nested.append(mcv_band)
            out.findings.append(
                _bf(
                    ctx,
                    domain="haematology",
                    finding_type="HAEM-F1",
                    label="mild_anaemia",
                    keys=keys_a,
                    biomarkers=["hgb"] + (["mcv"] if mcv_band else []),
                    urgency="within_weeks",
                    severity="mild",
                    tier=1,
                    role="independent_secondary",
                    nested_labels=nested,
                    caveats=anaemia_caveats,
                    rule_ids=["HAEM-F1", "HAEM-AS-1"],
                )
            )
        return out

    # Platelets <50 → HAEM-PLT (HEP-AS-14 boundary)
    if platelets_below_50:
        keys = ctx.plt_keys or [synthetic_key("HAEM-PLT", "thrombocytopenia")]
        t0 = tier0_flags(True)
        # Platelets 20–49: within_days clinically, but <50 with hepatic → same-day eligible
        # Approval HEP-AS-14 / HAEM-U-D-1: below 50 urgent; keep Tier 0 same_day for pathway
        nested_plt = []
        if ctx.crp_contextual_to_haem:
            nested_plt.append("crp_contextual")
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-PLT",
                label="thrombocytopenia_below_50",
                keys=keys,
                biomarkers=["platelets"],
                urgency="same_day",
                severity="moderate_to_severe",
                tier=0,
                role="principal_concern",
                nested_labels=nested_plt,
                prohibited=["absorb_platelets_below_50"],
                rule_ids=["HAEM-U-D-1", "HEP-AS-14"],
                actionability="haem_urgency",
                **t0,
            )
        )
        ctx.haem_same_day = True

    # ANC <0.5 → HAEM-F6 same_day
    if anc_severe:
        keys = ctx.anc_keys or [synthetic_key("HAEM-F6", "severe_neutropenia")]
        t0 = tier0_flags(True)
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F6",
                label="severe_neutropenia",
                keys=keys,
                biomarkers=["anc"],
                urgency="same_day",
                severity="severe",
                tier=0,
                role="principal_concern",
                caveats=["ancestry_not_captured_no_adjustment", "ancestry_not_captured_no_adjustment_xd_anc_1"],
                prohibited=["adjust_anc_for_presumed_ancestry", "adjust_band_for_presumed_ancestry"],
                rule_ids=["HAEM-F6", "HAEM-U-SD-3", "XD-ANC-1"],
                actionability="immediate",
                **t0,
            )
        )
        ctx.haem_same_day = True

    # Low WCC without differential → HAEM-F7 + insufficient_data neutrophils
    if wcc_low and differential_absent and not anc_severe:
        keys = ctx.wcc_keys or [synthetic_key("HAEM-F7", "low_wcc")]
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F7",
                label="leucopenia_or_low_wcc",
                keys=keys,
                biomarkers=["wcc"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                missing_data_state="insufficient_data",
                missing_data_notes=[
                    "neutrophil_question_insufficient_data",
                    "neutrophils_insufficient_data_differential_required",
                ],
                prohibited=[
                    "report_neutrophils_normal",
                    "infer_neutrophil_count_from_total",
                    "infer_neutrophils_from_total_wcc",
                ],
                rule_ids=["HAEM-F7", "HAEM-IND-2", "HAEM-AS-6"],
                actionability="investigate",
            )
        )

    # Mild/moderate thrombocytopenia not already covered / not absorbed into HEP-F5
    if (
        platelets_low
        and not platelets_below_50
        and lineages < 2
        and not ctx.suppress_mild_thrombocytopenia
    ):
        keys = ctx.plt_keys or [synthetic_key("HAEM-F4", "thrombocytopenia")]
        if platelets is not None and platelets < 100:
            urg, tier, sev = "within_weeks", 1, "mild"
        else:
            urg, tier, sev = "within_weeks", 1, "borderline"
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F4",
                label="thrombocytopenia",
                keys=keys,
                biomarkers=["platelets"],
                urgency=urg,
                severity=sev,
                tier=tier,
                role="principal_concern",
                rule_ids=["HAEM-F4"],
            )
        )

    # Anaemia (HAEM-F1) with MCV as constituent — not if IRIN-F2 absorbed
    if anaemia_flag and not ctx.suppress_haem_f1 and lineages < 2:
        keys = sorted(set(ctx.hb_keys + ctx.mcv_keys)) or [
            synthetic_key("HAEM-F1", "anaemia")
        ]
        nested = []
        biomarkers = ["hgb"]
        missing = []
        if mcv_band == "microcytosis":
            nested.extend(["microcytic", "mcv_microcytic"])
            biomarkers.append("mcv")
        elif mcv_band and "macro" in mcv_band:
            nested.append(mcv_band)
            biomarkers.append("mcv")
        if ctx.ferritin is None:
            missing.append("ferritin_not_assessable")
        # Severe anaemia Hb52 → within_days NOT same_day (XD-AS-22 / A5)
        sex_indeterminate = anaemia_sev == "indeterminate" or ctx.sex is None
        if anaemia_sev == "severe" or (ctx.hb is not None and ctx.hb < 70 and not sex_indeterminate):
            urg, tier, sev = "within_days", 1, "severe"
        else:
            urg, tier, sev = "within_weeks", 1, anaemia_sev
        if sex_indeterminate:
            missing.append("sex_assumption_stated")
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F1",
                label="anaemia",
                keys=keys,
                biomarkers=biomarkers,
                urgency=urg,
                severity=sev if not sex_indeterminate else None,
                tier=tier,
                role="principal_concern",
                nested_labels=nested,
                caveats=anaemia_caveats,
                missing_data_notes=missing,
                missing_data_state="indeterminate_severity" if sex_indeterminate else (
                    "not_assessable" if missing else "none"
                ),
                severity_indeterminate=sex_indeterminate,
                prohibited=(
                    (["same_day_anaemia_claim"] if urg == "within_days" else [])
                    + (["silent_sex_default"] if sex_indeterminate else [])
                ) or None,
                dependency_flags=["QUESTIONNAIRE_DEPENDENCY"] if sex_indeterminate else None,
                rule_ids=["HAEM-F1", "HAEM-AS-2", "XD-AS-22", "XD-AS-20b"],
                actionability="investigate",
            )
        )

    # Macrocytosis — HAEM-F2
    if (
        mcv_band
        and "macro" in mcv_band
        and not anaemia_flag
        and not ctx.suppress_macrocytosis_finding
    ):
        above_mild = mcv_band in {"moderate_macrocytosis", "marked_macrocytosis"}
        if above_mild and not ctx.suppress_macrocytosis_finding:
            keys = ctx.mcv_keys or [synthetic_key("HAEM-F2", "macrocytosis")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="haematology",
                    finding_type="HAEM-F2",
                    label="macrocytosis_above_mild_band",
                    keys=keys,
                    biomarkers=["mcv"],
                    urgency="within_weeks",
                    severity="marked" if mcv_band == "marked_macrocytosis" else "moderate",
                    tier=1,
                    role="independent_secondary",
                    prohibited=["attach_mcv_as_context_above_mild_band"],
                    rule_ids=["HAEM-S-2", "HEP-AS-13"],
                )
            )
        elif ctx.nest_mcv_mild_under_hepatic or ctx.suppress_mild_macrocytosis:
            pass  # nested under hepatic or thyroid
        else:
            keys = ctx.mcv_keys or [synthetic_key("HAEM-F2", "isolated_mild_macrocytosis")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="haematology",
                    finding_type="HAEM-F2",
                    label="isolated_mild_macrocytosis",
                    keys=keys,
                    biomarkers=["mcv"],
                    urgency="routine",
                    severity="mild",
                    tier=2,
                    role="principal_concern",
                    prohibited=["apply_hepatic_tier1_floor_to_mcv"],
                    rule_ids=["HAEM-F2", "HAEM-AS-3", "XD-HEP-FLOOR-2"],
                )
            )
    elif mcv_band == "microcytosis" and not anaemia_flag:
        keys = ctx.mcv_keys or [synthetic_key("HAEM-F3", "isolated_microcytosis")]
        out.findings.append(
            _bf(
                ctx,
                domain="haematology",
                finding_type="HAEM-F3",
                label="isolated_microcytosis",
                keys=keys,
                biomarkers=["mcv"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                rule_ids=["HAEM-F3"],
            )
        )

    return out


# ---------------------------------------------------------------------------
# Renal / electrolyte
# ---------------------------------------------------------------------------


def _aki_from_priors(ctx: PanelContext) -> bool:
    prior = ctx.priors.get("creatinine")
    if not isinstance(prior, dict) or ctx.creatinine is None:
        return False
    prior_val = prior.get("value")
    days_ago = prior.get("days_ago")
    if prior_val is None or days_ago is None:
        return False
    try:
        prior_f = float(prior_val)
        days = float(days_ago)
    except (TypeError, ValueError):
        return False
    if prior_f <= 0:
        return False
    rise = ctx.creatinine - prior_f
    pct = (rise / prior_f) * 100.0
    if days <= 7 and pct >= 50:
        return True
    if days <= 2 and rise >= 26:
        return True
    return False


def _stable_ckd_g3a(ctx: PanelContext) -> bool:
    if ctx.egfr is None or not (45 <= ctx.egfr <= 59):
        return False
    prior = ctx.priors.get("egfr") or ctx.priors.get("creatinine")
    if not isinstance(prior, dict):
        return False
    months = prior.get("months_ago")
    if months is None and prior.get("days_ago") is not None:
        try:
            months = float(prior["days_ago"]) / 30.0
        except (TypeError, ValueError):
            months = None
    if months is None or float(months) < 3:
        return False
    prior_egfr = prior.get("value") if "egfr" in str(prior.get("biomarker", "egfr")) else prior.get("egfr")
    if prior_egfr is None and ctx.priors.get("egfr"):
        prior_egfr = ctx.priors["egfr"].get("value")
    if prior_egfr is None:
        # Accept similar prior creatinine/eGFR marked similar
        return bool(prior.get("similar") or prior.get("stable"))
    try:
        return abs(float(prior_egfr) - ctx.egfr) <= 5
    except (TypeError, ValueError):
        return bool(prior.get("similar") or prior.get("stable"))


def build_renal(ctx: PanelContext) -> DomainBuild:
    out = DomainBuild()
    k = ctx.potassium
    na = ctx.sodium
    egfr = ctx.egfr
    creat = ctx.creatinine
    urea = ctx.urea
    adj_ca = ctx.adjusted_calcium
    ca_total = ctx.calcium_total
    alb = ctx.albumin_for_ca
    tg = ctx.tg

    reduced_egfr = egfr is not None and egfr < 60
    electrolyte_findings: List[ClinicalFinding] = []

    # Hyperkalaemia
    if k is not None and k >= 5.5:
        if k >= 6.0:
            # More serious tier wins (XD-AS-31): same_day Tier 0 even if severity moderate
            urg, tier = "same_day", 0
            sev = "severe" if k >= 6.5 else "moderate"
            t0 = tier0_flags(True)
        elif k >= 5.5:
            urg, tier, sev = "within_days", 1, "mild"
            t0 = {}
        keys = ctx.renal_keys or [synthetic_key("RE-F3", "hyperkalaemia")]
        if reduced_egfr and k >= 6.0:
            ftype, label = "RE-F9", "renal_impairment_with_hyperkalaemia"
            rule_ids = ["RE-F9", "RE-OV-2", "RE-A-WORD-1"]
        else:
            ftype, label = "RE-F3", "hyperkalaemia"
            rule_ids = ["RE-F3", "RE-A-WORD-1", "XD-AS-31"]
        electrolyte_findings.append(
            _bf(
                ctx,
                domain="renal_electrolyte",
                finding_type=ftype,
                label=label,
                keys=keys,
                biomarkers=["potassium"] + (["egfr"] if reduced_egfr else []),
                urgency=urg,
                severity=sev,
                tier=tier,
                role="principal_concern",
                caveats=["artefact_safe_wording", "artefact_safe_wording_mandatory", "must_not_assert_genuine_or_artefact_without_repeat"],
                prohibited=[
                    "assert_genuine_or_artefact_without_repeat",
                    "mild_consequence_language",
                    "cap_same_day_urgency_at_moderate_severity",
                    "downgrade_tier0",
                    "omit_finding",
                ],
                rule_ids=rule_ids,
                actionability="immediate" if urg == "same_day" else "discuss",
                **t0,
            )
        )

    # Hypokalaemia
    if k is not None and k < 3.5:
        if k < 2.5:
            urg, tier, sev = "same_day", 0, "severe"
            t0 = tier0_flags(True)
        elif k <= 3.4:
            # XD-AS-21: K 3.0-3.4 mild within_weeks Tier 2
            urg, tier, sev = "within_weeks", 2, "mild"
            t0 = {}
        else:
            urg, tier, sev = "within_weeks", 2, "mild"
            t0 = {}
        caveats = ["magnesium_companion_requested"] if ctx.magnesium is None else []
        missing = []
        if ctx.magnesium is None or ctx.context.get("magnesium_absent"):
            missing.append("magnesium_requested_as_companion")
        keys = ctx.renal_keys or [synthetic_key("RE-F4", "hypokalaemia")]
        electrolyte_findings.append(
            _bf(
                ctx,
                domain="renal_electrolyte",
                finding_type="RE-F4",
                label="hypokalaemia",
                keys=keys,
                biomarkers=["potassium"],
                urgency=urg,
                severity=sev,
                tier=tier,
                role="principal_concern",
                caveats=caveats,
                missing_data_notes=missing,
                missing_data_state="not_assessable" if missing else "none",
                prohibited=["mild_consequence_language"] if urg == "same_day" else None,
                rule_ids=["RE-F4", "XD-AS-21", "RE-IND-5"],
                **t0,
            )
        )

    # Hyponatraemia / hypernatraemia
    if na is not None:
        if na < 125:
            urg, tier, sev = "same_day", 0, "profound"
            t0 = tier0_flags(True)
            caveats = []
            if tg is not None and tg > 20:
                caveats.extend(["pseudohyponatraemia", "pseudohyponatraemia_caveat_tg_gt_20"])
            keys = ctx.renal_keys or [synthetic_key("RE-F5", "hyponatraemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F5",
                    label="profound_hyponatraemia",
                    keys=keys,
                    biomarkers=["sodium"],
                    urgency=urg,
                    severity=sev,
                    tier=tier,
                    role="principal_concern",
                    caveats=caveats,
                    missing_data_notes=["chronicity_unknown"],
                    missing_data_state="not_assessable",
                    rule_ids=["RE-F5", "RE-U-SD-3"],
                    actionability="immediate",
                    **t0,
                )
            )
        elif na <= 129:
            caveats = []
            if tg is not None and tg > 20:
                caveats.extend(["pseudohyponatraemia", "pseudohyponatraemia_caveat_tg_gt_20"])
            keys = ctx.renal_keys or [synthetic_key("RE-F5", "hyponatraemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F5",
                    label="moderate_hyponatraemia",
                    keys=keys,
                    biomarkers=["sodium"],
                    urgency="within_days",
                    severity="moderate",
                    tier=1,
                    role="principal_concern",
                    caveats=caveats,
                    rule_ids=["RE-F5"],
                )
            )
        elif na <= 133:
            keys = ctx.renal_keys or [synthetic_key("RE-F5", "mild_hyponatraemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F5",
                    label="mild_hyponatraemia",
                    keys=keys,
                    biomarkers=["sodium"],
                    urgency="within_weeks",
                    severity="mild",
                    tier=1,
                    role="principal_concern",
                    caveats=["j_labelled_departure_from_uk_no_investigation"],
                    rule_ids=["RE-F5", "RE-U-W-2", "RE-AS-10"],
                )
            )
        elif na >= 155:
            t0 = tier0_flags(True)
            keys = ctx.renal_keys or [synthetic_key("RE-F6", "hypernatraemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F6",
                    label="severe_hypernatraemia",
                    keys=keys,
                    biomarkers=["sodium"],
                    urgency="same_day",
                    severity="severe",
                    tier=0,
                    role="principal_concern",
                    rule_ids=["RE-F6"],
                    **t0,
                )
            )
        elif na >= 146:
            sev_na = "mild" if na <= 150 else "moderate"
            keys = ctx.renal_keys or [synthetic_key("RE-F6", "hypernatraemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F6",
                    label="hypernatraemia",
                    keys=keys,
                    biomarkers=["sodium"],
                    urgency="within_days",
                    severity=sev_na,
                    tier=1,
                    role="principal_concern",
                    caveats=["j_labelled_rule"],
                    rule_ids=["RE-F6", "HYPERNA-J1"],
                )
            )

    # Calcium — require adjusted_calcium; never invent Payne constants
    if adj_ca is not None:
        if adj_ca > 3.0:
            t0 = tier0_flags(True)
            keys = ctx.renal_keys or [synthetic_key("RE-F7", "hypercalcaemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F7",
                    label="severe_hypercalcaemia",
                    keys=keys,
                    biomarkers=["adjusted_calcium"],
                    urgency="same_day",
                    severity="severe",
                    tier=0,
                    role="principal_concern",
                    rule_ids=["RE-F7", "RE-U-SD-4"],
                    **t0,
                )
            )
        elif adj_ca >= 2.65:
            keys = ctx.renal_keys or [synthetic_key("RE-F7", "mild_hypercalcaemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F7",
                    label="mild_hypercalcaemia",
                    keys=keys,
                    biomarkers=["adjusted_calcium"],
                    urgency="within_days",
                    severity="mild",
                    tier=1,
                    role="principal_concern",
                    rule_ids=["RE-F7", "RE-U-D-3", "RE-AS-8"],
                )
            )
        elif adj_ca < 1.9:
            t0 = tier0_flags(True)
            keys = ctx.renal_keys or [synthetic_key("RE-F8", "hypocalcaemia")]
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F8",
                    label="severe_hypocalcaemia",
                    keys=keys,
                    biomarkers=["adjusted_calcium"],
                    urgency="same_day",
                    severity="severe",
                    tier=0,
                    role="principal_concern",
                    rule_ids=["RE-F8"],
                    **t0,
                )
            )
        elif adj_ca < 2.2:
            keys = ctx.renal_keys or [synthetic_key("RE-F8", "hypocalcaemia")]
            nested = []
            prohibited = []
            if ctx.vitamin_d is not None and ctx.vitamin_d < 25:
                nested.append("vitamin_d_contributor")
                nested.append("vitamin_d_deficiency_contributor")
            elif ctx.vitamin_d is not None and ctx.vitamin_d <= 50:
                nested.append("vitamin_d_limited_context")
                prohibited.append("describe_as_proven_deficiency")
            elif ctx.vitamin_d is not None and ctx.vitamin_d > 50:
                prohibited.append("nest_vitd_as_aetiological_contributor")
            electrolyte_findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F8",
                    label="hypocalcaemia",
                    keys=keys,
                    biomarkers=["adjusted_calcium"],
                    urgency="within_weeks",
                    severity="mild",
                    tier=1,
                    role="principal_concern",
                    caveats=["symptom_conditional_caveat", "symptom_conditional_emergency"],
                    nested_labels=nested,
                    prohibited=prohibited or None,
                    rule_ids=["RE-F8", "XD-VITD-2"],
                )
            )
    elif ctx.calcium_insufficient_data or (
        ca_total is not None and adj_ca is None and (alb is None or ctx.context.get("albumin_absent"))
    ):
        # Insufficient data — NOT a finding (RE-AS-7 / XD-AS-16 / XD-AS-34)
        out.domain_notes.append("calcium_insufficient_data_albumin_required")
        out.domain_notes.append("present_uncorrected_calcium_as_finding")
        ctx.calcium_insufficient_data = True

    # AKI
    if _aki_from_priors(ctx):
        t0 = tier0_flags(True)
        keys = ctx.renal_keys or [synthetic_key("RE-F1", "aki")]
        out.findings.append(
            _bf(
                ctx,
                domain="renal_electrolyte",
                finding_type="RE-F1",
                label="acute_kidney_injury",
                keys=keys,
                biomarkers=["creatinine"],
                urgency="same_day",
                severity="aki_50pct_rise_7d",
                tier=0,
                role="principal_concern",
                rule_ids=["RE-F1", "RE-T1", "RE-OV-3"],
                actionability="immediate",
                **t0,
            )
        )
    elif reduced_egfr or (creat is not None and egfr is None):
        # Avoid duplicate if RE-F9 already covers renal+K
        has_f9 = any(f.finding_type == "RE-F9" for f in electrolyte_findings)
        if _stable_ckd_g3a(ctx):
            keys = ctx.renal_keys or [synthetic_key("RE-F2", "stable_ckd_g3a")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F2",
                    label="stable_ckd_g3a",
                    keys=keys,
                    biomarkers=["egfr"],
                    urgency="routine",
                    severity="G3a",
                    tier=2,
                    role="principal_concern",
                    missing_data_notes=["acr_unavailable_staging_incomplete"],
                    missing_data_state="not_assessable",
                    rule_ids=["RE-F2", "RE-S-2", "RE-AS-5"],
                    actionability="monitor",
                )
            )
        elif not has_f9 and egfr is not None and egfr < 60:
            # RE-F10: no prior → within_weeks Tier 1, AKI not assessable
            keys = ctx.renal_keys or [synthetic_key("RE-F10", "egfr_undetermined")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F10",
                    label="reduced_egfr_undetermined_chronicity",
                    keys=keys,
                    biomarkers=["egfr"] + (["creatinine"] if creat is not None else []),
                    urgency="within_weeks",
                    severity=None,
                    tier=1,
                    role="principal_concern",
                    missing_data_state="not_assessable",
                    missing_data_notes=["aki_not_assessable", "aki_not_assessable_no_prior"],
                    prohibited=["present_as_chronic", "present_as_chronic_without_baseline"],
                    rule_ids=["RE-F10", "RE-IND-1", "RE-AS-4"],
                    actionability="investigate",
                )
            )
        elif creat is not None and egfr is None and not has_f9:
            keys = ctx.renal_keys or [synthetic_key("RE-F10", "creat_undetermined")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="renal_electrolyte",
                    finding_type="RE-F10",
                    label="reduced_egfr_undetermined_chronicity",
                    keys=keys,
                    biomarkers=["creatinine"],
                    urgency="within_weeks",
                    severity=None,
                    tier=1,
                    role="principal_concern",
                    missing_data_state="not_assessable",
                    missing_data_notes=["aki_not_assessable", "aki_not_assessable_no_prior"],
                    prohibited=["present_as_chronic", "present_as_chronic_without_baseline"],
                    rule_ids=["RE-F10", "RE-IND-1"],
                )
            )

    # eGFR 60-89 alone → NOT CKD
    if egfr is not None and 60 <= egfr <= 89:
        out.domain_notes.append("egfr_60_89_not_ckd_without_other_markers")
        out.domain_notes.append("classify_egfr_60_89_as_ckd_without_markers")

    # Urea alone → Tier 3 contextual, NOT independent finding (RE-CONS-3 / RE-AS-11)
    creat_normal = creat is None or (
        creat is not None and creat < 110 and (egfr is None or egfr >= 60)
    )
    if urea is not None and urea > 7.5 and creat_normal and not reduced_egfr:
        out.domain_notes.append("urea_contextual_only")
        out.domain_notes.append("urea_contextual_only_not_independent_finding")
        out.domain_notes.append("present_urea_as_renal_impairment")

    out.findings.extend(electrolyte_findings)

    renal_panel = any(
        biomarker_value(ctx.biomarkers, bid) is not None
        for bid in ("potassium", "sodium", "creatinine", "egfr", "urea", "adjusted_calcium", "calcium")
    )
    actionable = [
        f
        for f in out.findings
        if f.role not in {"contextual", "insufficient_data", "supporting_evidence"}
    ]
    if not actionable and renal_panel and not reduced_egfr and not electrolyte_findings:
        if ctx.calcium_insufficient_data:
            pass  # insufficient-data path is not no_concern
        else:
            out.no_concern = True
            out.no_concern_notes = ["aki_could_not_be_assessed_without_prior"]
            out.domain_notes.append("must_not_state_kidneys_working_normally")

    return out


# ---------------------------------------------------------------------------
# Thyroid
# ---------------------------------------------------------------------------


def build_thyroid(ctx: PanelContext) -> DomainBuild:
    out = DomainBuild()
    tsh, ft4, ft3, tpo = ctx.tsh, ctx.ft4, ctx.ft3, ctx.tpo
    if tsh is None:
        return out

    tsh_high = tsh > ctx.tsh_uln
    tsh_low = tsh < ctx.tsh_lrl
    ft4_present = ft4 is not None
    ft4_high = ft4_present and ctx.ft4_uln is not None and ft4 > ctx.ft4_uln
    ft4_low = ft4_present and ctx.ft4_lrl is not None and ft4 < ctx.ft4_lrl
    ft4_normal = ft4_present and not ft4_high and not ft4_low
    ft3_high = ft3 is not None and ctx.ft3_uln is not None and ft3 > ctx.ft3_uln
    tpo_high = tpo is not None and (
        (ctx.tpo_uln is not None and tpo > ctx.tpo_uln) or tpo > 34
    )

    finding: Optional[ClinicalFinding] = None
    nested: List[str] = []
    if tpo_high:
        nested.append("tpo_contextual")
        nested.append("tpo_positive_contextual")
    if ctx.nest_lipid_under_thyroid:
        nested.append("lipid_secondary_cause_context")
    if ctx.nest_macro_under_thyroid:
        nested.append("macrocytosis_context")

    preg = pregnancy_known(ctx.context)

    if tsh_high and ft4_low:
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F1",
            label="overt_hypothyroidism",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F1", "overt_hypo")],
            biomarkers=["tsh", "free_t4"],
            urgency="within_weeks",
            severity="overt",
            tier=1,
            role="principal_concern",
            nested_labels=nested,
            rule_ids=["THY-F1", "THY-OV-1"],
            actionability="treat",
        )
    elif tsh_high and ft4_normal:
        if tsh >= 10:
            urg, tier, sev = "within_weeks", 1, "intermediate"
            caveats = ["nice_two_occasion_requirement"]
        else:
            urg, tier, sev = "routine", 2, "lower"
            caveats = []
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F2",
            label="subclinical_hypothyroidism",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F2", "subclinical_hypo")],
            biomarkers=["tsh", "free_t4"],
            urgency=urg,
            severity=sev,
            tier=tier,
            role="principal_concern",
            nested_labels=nested,
            caveats=caveats,
            prohibited=["present_tpo_as_independent_finding"],
            rule_ids=["THY-F2", "THY-OV-2", "THY-CONS-2"],
        )
    elif tsh_high and not ft4_present:
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F5",
            label="indeterminate_thyroid_axis_abnormality",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F5", "indeterminate")],
            biomarkers=["tsh"],
            urgency="within_weeks",
            severity="indeterminate",
            tier=1,
            role="principal_concern",
            severity_indeterminate=True,
            missing_data_state="indeterminate_severity",
            missing_data_notes=[
                "both_states_stated",
                "both_states_named",
                "free_t4_requested",
                "must_not_default_to_subclinical",
            ],
            prohibited=["default_to_subclinical", "worst_case_inference", "infer_worst_case"],
            nested_labels=nested,
            rule_ids=["THY-F5", "THY-IND-1", "THY-AS-4"],
            actionability="investigate",
        )
    elif tsh_low and (ft4_high or ft3_high):
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F3",
            label="overt_hyperthyroidism",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F3", "overt_hyper")],
            biomarkers=["tsh"] + (["free_t4"] if ft4_present else []) + (["free_t3"] if ft3 else []),
            urgency="within_weeks",
            severity="overt",
            tier=1,
            role="principal_concern",
            rule_ids=["THY-F3", "THY-OV-3"],
            actionability="treat",
        )
    elif tsh_low and ft4_normal:
        missing = []
        if ft3 is None:
            missing.append("t3_toxicosis_not_assessable")
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F4",
            label="subclinical_hyperthyroidism",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F4", "subclinical_hyper")],
            biomarkers=["tsh", "free_t4"],
            urgency="within_weeks",
            severity=None,
            tier=1,
            role="principal_concern",
            missing_data_notes=missing,
            missing_data_state="not_assessable" if missing else "none",
            rule_ids=["THY-F4", "THY-IND-3"],
            actionability="investigate",
        )
    elif tsh_low and not ft4_present:
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F5",
            label="indeterminate_thyroid_axis_abnormality",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F5", "indeterminate_hyper")],
            biomarkers=["tsh"],
            urgency="within_weeks",
            severity="indeterminate",
            tier=1,
            role="principal_concern",
            severity_indeterminate=True,
            missing_data_state="indeterminate_severity",
            missing_data_notes=["both_states_stated", "both_states_named", "free_t4_requested"],
            prohibited=["infer_worst_case"],
            rule_ids=["THY-F5", "THY-IND-2"],
        )
    elif (tsh_high and ft4_high) or (tsh_low and ft4_low):
        finding = _bf(
            ctx,
            domain="thyroid_endocrine",
            finding_type="THY-F6",
            label="discordant_thyroid_axis",
            keys=ctx.thyroid_keys or [synthetic_key("THY-F6", "discordant")],
            biomarkers=["tsh", "free_t4"],
            urgency="within_days",
            severity=None,
            tier=1,
            role="principal_concern",
            prohibited=["auto_explain_discordant_pattern", "auto_explain_discordant_thyroid"],
            rule_ids=["THY-F6", "THY-OV-4", "THY-CONS-3"],
            actionability="specialist_interpretation",
        )

    if finding is not None:
        if preg:
            finding = finding.model_copy(
                update={
                    "withheld": True,
                    "dependency_flags": sorted(
                        set(list(finding.dependency_flags) + ["QUESTIONNAIRE_DEPENDENCY"])
                    ),
                    "prohibited_behaviours_asserted": sorted(
                        set(
                            list(finding.prohibited_behaviours_asserted)
                            + [
                                "silently_suppress_pregnancy_domain",
                                "silently_suppress_thyroid_in_pregnancy",
                            ]
                        )
                    ),
                }
            )
        out.findings.append(finding)
    elif not tsh_high and not tsh_low and ft4_normal:
        out.no_concern = True
        out.no_concern_notes = ["biotin_illness_distortion_caveat"]
        out.domain_notes.append("must_not_state_thyroid_normal_without_caveat")

    return out


# ---------------------------------------------------------------------------
# Cardiometabolic / nutritional
# ---------------------------------------------------------------------------


def build_cardiometabolic(ctx: PanelContext) -> DomainBuild:
    out = DomainBuild()
    tg, tc, non_hdl = ctx.tg, ctx.tc, ctx.non_hdl
    hba1c, b12, vitd = ctx.hba1c, ctx.b12, ctx.vitamin_d
    mcv_band = ctx.mcv_band()
    anaemia_flag, _, _ = ctx.anaemia()

    # TG >20 → CN-F1 same_day Tier 0
    if tg is not None and tg > 20:
        t0 = tier0_flags(True)
        caveats = ["pancreatitis_framing_mandatory", "alcohol_unassessed"]
        nest_dys = False
        if hba1c is not None and hba1c < 48:
            caveats.append("hba1c_excludes_poor_glycaemic_control")
        elif hba1c is not None and hba1c >= 48:
            caveats.append("dysglycaemia_plausible_secondary_cause")
            caveats.append("dysglycaemia_plausible_secondary_cause_not_downgraded")
            nest_dys = True
        keys = ctx.lipid_keys or [synthetic_key("CN-F1", "severe_hypertriglyceridaemia")]
        nested_f1 = ["dysglycaemia_secondary_cause"] if nest_dys else []
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F1",
                label="severe_hypertriglyceridaemia",
                keys=keys,
                biomarkers=["triglycerides"] + (["hba1c"] if nest_dys else []),
                urgency="same_day",
                severity="severe",
                tier=0,
                role="principal_concern",
                caveats=caveats,
                nested_labels=nested_f1,
                prohibited=[
                    "frame_as_cardiovascular_urgency",
                    "downgrade_despite_secondary_cause",
                ],
                rule_ids=["CN-F1", "CN-OV-1", "CN-OV-5"],
                actionability="immediate",
                **t0,
            )
        )
        ctx.context["_cn_f1_nests_dysglycaemia"] = nest_dys

    # One consolidated lipid finding — never CV-risk %
    lipid_abnormal = False
    specialist = (tc is not None and tc > 9.0) or (non_hdl is not None and non_hdl > 7.5)
    elevated = False
    if tc is not None and tc > 5.0:
        elevated = True
        lipid_abnormal = True
    if non_hdl is not None and non_hdl > 4.0:
        elevated = True
        lipid_abnormal = True
    if ctx.ldl is not None and ctx.ldl > 3.0:
        elevated = True
        lipid_abnormal = True
    if tg is not None and 2.3 <= tg <= 20:
        elevated = True
        lipid_abnormal = True

    risk_factors_present = bool(
        ctx.context.get("risk_factors")
        or ctx.context.get("family_history_premature_chd")
        or ctx.context.get("cv_risk_factors_complete")
    )

    skip_lipid = ctx.suppress_lipid_finding or (tg is not None and tg > 20)
    risk_absent = bool(
        ctx.context.get("risk_factors_absent")
        or ctx.context.get("family_history_absent")
    )
    full_risk = bool(
        ctx.context.get("full_risk_factor_set")
        or ctx.context.get("cv_risk_factors_complete")
        or risk_factors_present
    )
    multi_fraction = sum(
        1
        for b in ("total_cholesterol", "non_hdl", "ldl", "hdl", "triglycerides", "tc", "tg")
        if biomarker_value(ctx.biomarkers, b) is not None
    ) >= 3

    if not skip_lipid and specialist:
        keys = ctx.lipid_keys or [synthetic_key("CN-F2", "fh_pattern")]
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F2",
                label="possible_familial_hypercholesterolaemia_pattern",
                keys=keys,
                biomarkers=[
                    b
                    for b in ("total_cholesterol", "non_hdl")
                    if biomarker_value(ctx.biomarkers, b) is not None
                ],
                urgency="within_weeks",
                severity="nice_threshold",
                tier=1,
                role="principal_concern",
                prohibited=["compute_cv_risk_percent"],
                quarantine_flags=["cardiovascular_risk", "R2"],
                rule_ids=["CN-F2", "CN-OV-2"],
                actionability="specialist_assessment",
            )
        )
    elif not skip_lipid and lipid_abnormal and not specialist:
        # CN-F9 only when risk-factor set explicitly absent / indeterminate
        if risk_absent or (not full_risk and not multi_fraction):
            keys = ctx.lipid_keys or [synthetic_key("CN-F9", "indeterminate_lipid_risk")]
            out.findings.append(
                _bf(
                    ctx,
                    domain="cardiometabolic_nutritional",
                    finding_type="CN-F9",
                    label="indeterminate_lipid_risk",
                    keys=keys,
                    biomarkers=[
                        b
                        for b in ("total_cholesterol", "non_hdl", "ldl", "hdl", "triglycerides")
                        if biomarker_value(ctx.biomarkers, b) is not None
                    ],
                    urgency="routine",
                    severity="not_computable",
                    tier=2,
                    role="principal_concern",
                    missing_data_notes=["fh_not_assessable", "risk_factors_incomplete"],
                    missing_data_state="not_assessable",
                    prohibited=["compute_cv_risk_percent"],
                    quarantine_flags=["cardiovascular_risk", "R2"],
                    rule_ids=["CN-F9"],
                    actionability="monitor",
                )
            )
        else:
            keys = ctx.lipid_keys or [synthetic_key("CN-F3", "elevated_lipid")]
            promote = bool(ctx.context.get("_promote_lipid_with_overt_thyroid") or full_risk)
            urg3, tier3 = ("within_weeks", 1) if promote else ("routine", 2)
            out.findings.append(
                _bf(
                    ctx,
                    domain="cardiometabolic_nutritional",
                    finding_type="CN-F3",
                    label="elevated_lipid_finding",
                    keys=keys,
                    biomarkers=[
                        b
                        for b in ("total_cholesterol", "non_hdl", "ldl", "hdl", "triglycerides")
                        if biomarker_value(ctx.biomarkers, b) is not None
                    ],
                    urgency=urg3,
                    severity="nice_threshold" if full_risk else None,
                    tier=tier3,
                    role="principal_concern",
                    prohibited=[
                        "present_separate_fraction_concerns",
                        "present_four_separate_fraction_concerns",
                        "compute_cv_risk_percent",
                    ],
                    quarantine_flags=["cardiovascular_risk", "R2"],
                    rule_ids=["CN-F3", "CN-CONS-1"],
                    actionability="monitor" if tier3 == 2 else "investigate",
                )
            )

    # Attach thyroid secondary-cause nest on lipid if thyroid abnormal
    thy_abnormal = ctx.tsh is not None and (
        ctx.tsh > ctx.tsh_uln or ctx.tsh < ctx.tsh_lrl
    )
    if thy_abnormal and out.findings:
        for i, f in enumerate(out.findings):
            if f.finding_type in {"CN-F2", "CN-F3", "CN-F9"}:
                nested = list(f.nested_constituent_labels) + ["thyroid_secondary_cause_context"]
                out.findings[i] = f.model_copy(update={"nested_constituent_labels": nested})

    # HbA1c ≥48 → CN-F4 no diabetes claim (unless nested under CN-F1)
    if hba1c is not None and hba1c >= 48 and not ctx.context.get("_cn_f1_nests_dysglycaemia"):
        keys = ctx.lipid_keys or [synthetic_key("CN-F4", "dysglycaemia")]
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F4",
                label="dysglycaemia",
                keys=keys,
                biomarkers=["hba1c"],
                urgency="within_weeks",
                severity="diagnostic_range",
                tier=1,
                role="principal_concern",
                prohibited=[
                    "assert_diabetes_from_single_result",
                    "assert_diabetes_diagnosis_from_single_result",
                ],
                caveats=["confirmation_required"],
                rule_ids=["CN-F4", "CN-AS-6"],
                actionability="investigate",
            )
        )
    elif (
        hba1c is not None
        and hba1c >= 42
        and not ctx.context.get("_cn_f1_nests_dysglycaemia")
    ):
        keys = ctx.lipid_keys or [synthetic_key("CN-F4", "ndh")]
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F4",
                label="non_diabetic_hyperglycaemia",
                keys=keys,
                biomarkers=["hba1c"],
                urgency="routine",
                severity="ndh_range",
                tier=2,
                role="principal_concern",
                prohibited=["assert_diabetes_diagnosis_from_single_result"],
                rule_ids=["CN-F4"],
            )
        )

    # B12 rules
    b12_low = b12 is not None and ctx.b12_lrl is not None and b12 < ctx.b12_lrl
    b12_in_range = (
        b12 is not None
        and ctx.b12_lrl is not None
        and ctx.b12_uln is not None
        and ctx.b12_lrl <= b12 <= ctx.b12_uln
    )
    if ctx.pancytopenia_finding and b12_low:
        # B12 as aetiology within haem finding — not competing (CN-OV-7)
        out.domain_notes.append("b12_aetiology_within_haematology_pancytopenia")
    elif b12_low and (anaemia_flag or (mcv_band and "macro" in mcv_band)):
        keys = ctx.lipid_keys or [synthetic_key("CN-F5", "b12_deficiency")]
        nested = []
        if anaemia_flag:
            nested.append("anaemia")
        if mcv_band:
            nested.append(mcv_band)
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F5",
                label="b12_deficiency",
                keys=keys,
                biomarkers=["b12"] + (["hgb"] if anaemia_flag else []) + (["mcv"] if mcv_band else []),
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                nested_labels=nested,
                rule_ids=["CN-F5", "CN-OV-6"],
                actionability="investigate",
            )
        )
        ctx.suppress_haem_f1 = True
    elif b12_low:
        keys = ctx.lipid_keys or [synthetic_key("CN-F5", "b12_deficiency")]
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F5",
                label="b12_deficiency",
                keys=keys,
                biomarkers=["b12"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                rule_ids=["CN-F5"],
            )
        )
    elif b12_in_range and mcv_band and "macro" in mcv_band:
        keys = ctx.lipid_keys or [synthetic_key("CN-F7", "functional_b12")]
        out.findings.append(
            _bf(
                ctx,
                domain="cardiometabolic_nutritional",
                finding_type="CN-F7",
                label="functional_b12_concern",
                keys=keys,
                biomarkers=["b12", "mcv"],
                urgency="within_weeks",
                severity=None,
                tier=1,
                role="principal_concern",
                prohibited=["report_b12_as_normal_given_context"],
                rule_ids=["CN-F7", "CN-OV-8"],
                actionability="investigate",
            )
        )

    # Vitamin D per XD-VITD — skip independent CN-F8 when nested under hypocalcaemia
    hypoca = ctx.adjusted_calcium is not None and ctx.adjusted_calcium < 2.2
    if vitd is not None:
        if vitd < 25:
            if hypoca:
                # Nested under RE-F8; no independent CN-F8 (XD-AS-28)
                pass
            else:
                keys = ctx.lipid_keys or [synthetic_key("CN-F8", "vitamin_d_deficiency")]
                out.findings.append(
                    _bf(
                        ctx,
                        domain="cardiometabolic_nutritional",
                        finding_type="CN-F8",
                        label="vitamin_d_deficiency",
                        keys=keys,
                        biomarkers=["vitamin_d"],
                        urgency="routine",
                        severity=None,
                        tier=2,
                        role="principal_concern",
                        prohibited=["supplementation_dose", "tier1_escalation_from_vitd"],
                        rule_ids=["CN-F8", "XD-VITD"],
                        actionability="monitor",
                    )
                )
        elif vitd <= 50:
            out.domain_notes.append("vitamin_d_25_50_no_independent_finding")
            out.domain_notes.append("vitamin_d_contextual_only")
            out.domain_notes.append("describe_as_proven_deficiency")
        # >50: no concern

    cn_panel = any(
        biomarker_value(ctx.biomarkers, bid) is not None
        for bid in (
            "triglycerides",
            "tg",
            "total_cholesterol",
            "tc",
            "non_hdl",
            "hba1c",
            "b12",
            "vitamin_d",
        )
    )
    if not out.findings and cn_panel:
        out.no_concern = True
        out.no_concern_notes = [
            "normal_lipid_does_not_exclude_cv_risk",
            "normal_b12_does_not_exclude_functional_deficiency",
        ]

    return out


# ---------------------------------------------------------------------------
# Lead selection
# ---------------------------------------------------------------------------


def select_leads(
    findings: List[ClinicalFinding],
) -> Tuple[List[ClinicalFinding], List[str], List[str], str, bool]:
    visible = [
        f
        for f in findings
        if f.role
        not in {"contextual", "supporting_evidence", "insufficient_data", "modifier"}
        and not (f.withheld and f.role == "contextual")
    ]
    # Withheld pregnancy thyroid still visible for presentation
    visible_sorted = sorted(
        visible,
        key=lambda f: (
            int(f.concern_tier),
            URGENCY_RANK.get(f.urgency_time_band, 9),
            f.finding_type,
            f.finding_id,
        ),
    )

    lead_ids: List[str] = []
    co_lead_ids: List[str] = []
    presentation_mode = "principal"
    no_forced_lead = False

    if not visible_sorted:
        return findings, lead_ids, co_lead_ids, presentation_mode, no_forced_lead

    top_tier = visible_sorted[0].concern_tier
    top_band = visible_sorted[0].urgency_time_band
    same_band = [
        f
        for f in visible_sorted
        if f.concern_tier == top_tier and f.urgency_time_band == top_band
    ]

    f4 = [f for f in same_band if f.finding_type == "HEP-F4"]
    if f4:
        lead_ids = [f4[0].finding_id]
    elif top_band == "same_day" and len(same_band) > 1:
        # Co-equal group — all as co_leads; no manufactured solo lead
        lead_ids = [same_band[0].finding_id]
        co_lead_ids = [f.finding_id for f in same_band[1:]]
        presentation_mode = "co_lead"
    elif len(same_band) >= 3 and top_band != "same_day":
        no_forced_lead = True
        presentation_mode = "no_forced_lead"
        lead_ids = []
        co_lead_ids = []
    elif len(same_band) == 2 and same_band[0].domain != same_band[1].domain:
        lead_ids = [same_band[0].finding_id]
        co_lead_ids = [same_band[1].finding_id]
        presentation_mode = "co_lead"
    elif len(same_band) == 2 and {"HEP-F1", "IRIN-F3"} <= {
        same_band[0].finding_type,
        same_band[1].finding_type,
    }:
        lead_ids = [same_band[0].finding_id]
        co_lead_ids = [same_band[1].finding_id]
        presentation_mode = "co_lead"
    else:
        lead_ids = [same_band[0].finding_id]

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
                        "prohibited_behaviours_asserted": sorted(
                            set(
                                list(f.prohibited_behaviours_asserted)
                                + [
                                    "manufacture_co_leads_by_cross_domain_severity",
                                    "suppress_third_to_satisfy_display",
                                ]
                            )
                        ),
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

    # Haem same_day + hepatic non-same → haem leads on time band
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

    return findings, lead_ids, co_lead_ids, presentation_mode, no_forced_lead


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------


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

    Checkpoint 2: hepatic, haematology, renal/electrolyte, iron/inflammatory,
    thyroid/endocrine, cardiometabolic/nutritional.
    """
    pkg = package or load_prioritisation_package()
    stamp = pkg.stamp
    ctx = PanelContext.from_inputs(
        signal_results, biomarkers, lab_ranges, derived, priors, context, pkg
    )

    fib_4_computed = False
    fib_4_displayed = False
    quarantine_notes = [
        "XD-QUAR-1: FIB-4 not used for fibrosis finding authority",
        "CV-risk quarantine: not computed as finding in this package",
    ]
    if "fib_4" in ctx.derived:
        quarantine_notes.append("fib_4 present in derived inputs but ignored for findings")

    hepatic = build_hepatic(ctx)
    iron = build_iron(ctx)
    haem = build_haematology(ctx)
    renal = build_renal(ctx)
    thyroid = build_thyroid(ctx)
    cardio = build_cardiometabolic(ctx)

    findings: List[ClinicalFinding] = []
    domain_notes: List[str] = []
    no_concern_notes: List[str] = []

    for block in (hepatic, iron, haem, renal, thyroid, cardio):
        findings.extend(block.findings)
        domain_notes.extend(block.domain_notes)
        no_concern_notes.extend(block.no_concern_notes)

    # Drop insufficient_data from competitive finding set for no_concern calc
    competitive = [
        f
        for f in findings
        if f.role not in {"insufficient_data", "contextual", "supporting_evidence"}
    ]

    no_concern = False
    if not competitive:
        # Aggregate panel-level no-concern when any domain declared it and nothing competitive
        if any(
            b.no_concern
            for b in (hepatic, iron, haem, renal, thyroid, cardio)
        ):
            no_concern = True
            domain_notes.append("must_not_imply_disease_excluded_beyond_panel_scope")
        elif not findings:
            no_concern = False
    if ctx.calcium_insufficient_data:
        # Ensure note present even if other findings exist (XD-AS-9)
        if "calcium_insufficient_data_albumin_required" not in domain_notes:
            domain_notes.append("calcium_insufficient_data_albumin_required")

    findings, lead_ids, co_lead_ids, presentation_mode, no_forced_lead = select_leads(
        findings
    )

    findings = sorted(
        findings,
        key=lambda f: (
            int(f.concern_tier),
            URGENCY_RANK.get(f.urgency_time_band, 9),
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
        no_concern_notes=sorted(set(no_concern_notes)),
        domain_notes=sorted(set(domain_notes)),
        fib_4_computed=fib_4_computed,
        fib_4_displayed=fib_4_displayed,
        quarantine_notes=quarantine_notes,
    )
