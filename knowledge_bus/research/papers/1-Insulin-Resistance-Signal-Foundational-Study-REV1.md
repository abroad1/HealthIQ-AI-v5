# 1 — Lipid Transport Dysfunction Signal (Foundational Study) — REV1

**REV1 Status: CANONICAL REVIEW COMPLETE**
Paper maps to KBP-0003 (pkg_lipid_transport) as an UPDATE. All thresholds confirmed
consistent with existing package. Four new evidence sources added. One platform status
error corrected.

Source document: `knowledge_bus/research/papers/1-Insulin-Resistance-Signal-Foundational-Study.md`

---

## CANONICAL RESOLUTIONS

### 1. Filename mismatch

The file is named `1-Insulin-Resistance-Signal-Foundational-Study.md` but the content
is entirely about the **Lipid Transport Dysfunction Signal** (non-HDL-C primary axis,
TG secondary axis). This is a naming error in the paper itself.

**Resolution**: Paper maps to KBP-0003 (`pkg_lipid_transport` / `signal_lipid_transport_dysfunction`).
No new package required. Translation mode: UPDATE.

---

### 2. Platform status correction — remnant_cholesterol

KBP-0003 `research_brief.yaml` notes:
> "derived.remnant_cholesterol is introduced as a new optional derived metric (TC - LDL-C - HDL-C).
>  This metric does not currently exist in backend/core/analytics/ratio_registry.py."

`clinical_signoff.md` states: "Current implementation status: NOT present in
`backend/core/analytics/ratio_registry.py`"

**CORRECTION**: `remnant_cholesterol` IS in `ratio_registry.py` DERIVED_IDS.
- Line 30: `"remnant_cholesterol"` in DERIVED_IDS list
- Line 42: `"remnant_cholesterol": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol"]`
  in `_DERIVED_INPUTS`
- Lines 173–183: computed path (lab-supplied or derived from TC - LDL-C - HDL-C)

Formula confirmed: `TC - LDL-C - HDL-C` (all mmol/L). Conditional on LDL-C availability —
existing platform logic handles the conditional correctly.

**Action**: Update research_brief.yaml and clinical_signoff.md to reflect ✓ IN PLATFORM.

---

### 3. Platform status confirmation — non_hdl_cholesterol

`non_hdl_cholesterol` IS in `ratio_registry.py`:
- Line 29: in DERIVED_IDS list
- Line 40: `"non_hdl_cholesterol": ["total_cholesterol", "hdl_cholesterol"]`
- Lines 146–155: computed path (TC - HDL)

Already correctly used as `primary_metric` in KBP-0003 signal_library. No change needed.

---

### 4. Threshold confirmation — no changes

Paper 1 proposes identical thresholds to KBP-0003 current implementation:

| Tier | Metric | Paper 1 | KBP-0003 current | Status |
|------|--------|---------|-----------------|--------|
| Optimal | non_hdl_cholesterol | < 3.7 mmol/L | < 3.7 mmol/L | ✓ MATCH |
| Suboptimal | non_hdl_cholesterol | 3.7–5.69 mmol/L | 3.7–5.69 mmol/L | ✓ MATCH |
| At risk | non_hdl_cholesterol | ≥ 5.7 mmol/L | ≥ 5.7 mmol/L | ✓ MATCH |
| TG borderline | triglycerides | ≥ 1.7 → suboptimal | Documented as limitation | ✓ CONSISTENT |
| TG severe | triglycerides | ≥ 5.6 → at_risk | tg_severe_override ✓ | ✓ MATCH |

No threshold changes required in signal_library.yaml.

---

### 5. Remnant cholesterol flag threshold confirmation

Paper 1 confirms: RC ≥ 1.5 mmol/L → "high remnant burden" (~2-fold MI risk; Copenhagen
General Population Study; n=106,216). This is the same cut-off already documented in
KBP-0003 clinical_signoff.md evidence summary. No change needed.

---

### 6. New evidence sources — addition to research_brief.yaml

Paper 1 provides four evidence sources not yet in KBP-0003:

| Source | Type | N | Finding | Action |
|--------|------|---|---------|--------|
| TG/HDL-C ratio meta-analysis (2022) | Meta-analysis | 207,515 | Higher TG/HDL-C associated with CV events (13 studies) | ADD — supports tg_hdl_ratio as supporting metric |
| UK Biobank + Copenhagen PAD study (2022) | Prospective cohort | 302,167 (UK BB) | ApoB→PAD risk explained primarily by remnant cholesterol, not LDL-C | ADD — reinforces remnant_cholesterol rationale |
| REDUCE-IT (NEJM; n=8,179) | RCT | 8,179 | Icosapent ethyl reduced MACE in statin-treated patients with elevated TG (median follow-up 4.9yr) | ADD — contrasts PROMINENT; mechanism matters |
| VESALIUS-CV (NEJM 2026; n=12,257) | RCT | 12,257 | Evolocumab reduced first major CV events in high-risk patients without prior MI/stroke | ADD — confirms apoB/LDL-C pathway; 2026 outcome data |

**REDUCE-IT vs PROMINENT context note:**
Both are TG-targeting RCTs with divergent outcomes. PROMINENT (pemafibrate): TG down,
no CV event reduction, apoB/LDL-C increased slightly. REDUCE-IT (icosapent ethyl/EPA):
MACE reduced. Signal framing remains correct — "TG lowering ≠ risk reduction unless
apoB/non-HDL-C also improve" — because EPA mechanism extends beyond TG reduction
(anti-inflammatory, membrane stabilisation). The signal correctly treats non-HDL-C as
the primary outcome-anchored axis.

---

### 7. Signal design confirmation

Paper 1's full two-axis design matches KBP-0003 exactly:
- Primary: non-HDL-C (outcome-anchored, Lancet 2019)
- Secondary: TG (risk modifier, not outcome-anchored primary)
- TG 1.7 conditional upgrade limitation: already documented in clinical_signoff.md
- PROMINENT cautionary framing: already in research_brief.yaml and clinical_signoff.md
- HDL-C as substrate only (not protective target): already in clinical_signoff.md limitation #6

No signal_library.yaml changes required.

---

## SSOT STATUS

| Input | Status |
|-------|--------|
| `total_cholesterol` | ✓ biomarkers.yaml |
| `hdl_cholesterol` | ✓ biomarkers.yaml |
| `triglycerides` | ✓ biomarkers.yaml |
| `ldl_cholesterol` | ✓ biomarkers.yaml (optional) |
| `non_hdl_cholesterol` | ✓ ratio_registry.py (confirmed REV1) |
| `tg_hdl_ratio` | ✓ ratio_registry.py |
| `remnant_cholesterol` | ✓ ratio_registry.py (confirmed REV1 — corrects prior false gap claim) |

No SSOT gaps for KBP-0003.

---

## CHANGES REQUIRED IN KBP-0003

| File | Change | Type |
|------|--------|------|
| `research_brief.yaml` | Add 4 new sources (TG/HDL meta, PAD study, REDUCE-IT, VESALIUS-CV) | ADDITION |
| `research_brief.yaml` | Remove false "NOT in ratio_registry" note for remnant_cholesterol | CORRECTION |
| `research_brief.yaml` | Update notes to reflect both derived metrics confirmed in platform | CORRECTION |
| `clinical_signoff.md` | Correct "NOT present in ratio_registry.py" → "✓ IN PLATFORM" for remnant_cholesterol | CORRECTION |
| `signal_library.yaml` | No changes required | — |
| `package_manifest.yaml` | No changes required | — |

---

_REV1 completed 2026-03-10. Translation mode: UPDATE. KBP-0003 package corrections applied._
