# Wave 1 Subsystem Coverage and Marker Role Codebase Investigation

## 1. Executive verdict
Current Wave 1 subsystem implementation is **thin-but-acceptable only with careful wording**, not yet fully fit as a robust semantic model.

- **Cardiovascular** subsystem structure is relatively coherent for v1.
- **Blood sugar** and **liver** include thin or mixed-role subsystem evidence that can look semantically stronger than its scoring rail support.
- There is a known **false-missing equivalence issue** (`total_bilirubin` vs `bilirubin`) that is still model-level debt even after display-label patching.
- Subsystems currently present marker chips as a single evidence class, while the codebase mixes score-contributor, confidence, and context roles.

## 2. Strategic authority summary
From `docs/architecture/User Health to Systems Map_FINAL.md`, visible subdomains/subsystems should be shown only when they are:

- biologically distinct
- understandable to users
- supported by deterministic logic
- not heavily overlapping or cosmetic

The same authority explicitly positions:

- **Cardiovascular** as a strong candidate for hierarchical substructure
- **Liver** as a weaker early-splitting candidate if support is thin/fuzzy

This strategic rule is stricter than “can we render chips?”; it requires semantic coherence between score rail, confidence logic, and surfaced subsystem labels.

## 3. Current subsystem definition matrix

| Domain | Subsystem | Expected markers | Included on bb695d3c | Missing on bb695d3c | Source of marker set | Assessment |
|---|---|---|---|---|---|---|
| Cardiovascular | Lipid transport (`wave1_cv_lipid_transport`) | total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, tc_hdl_ratio | total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, tc_hdl_ratio | none | Manually authored in `wave1_subsystem_evidence.py` (not SSOT-derived), then partitioned by panel U rail-scored markers | Clearly sufficient for v1 |
| Cardiovascular | Homocysteine pathway (`wave1_cv_homocysteine_pathway`) | homocysteine | homocysteine | none | Manually authored subsystem map | Thin but acceptable if labelled carefully |
| Cardiovascular | Vascular strain context (`wave1_cv_vascular_strain`) | crp | crp | none | Manually authored subsystem map; overlaps inflammatory rail conceptually | Thin; label broader than marker support |
| Blood sugar control | Glycaemic control (`wave1_met_glycaemic_control`) | glucose, hba1c | hba1c | glucose | Manually authored subsystem map; aligns with metabolic core comments in `domain_score_assembler.py` | Thin but acceptable if caveated |
| Blood sugar control | Insulin and metabolic context (`wave1_met_insulin_metabolic`) | insulin, triglycerides | triglycerides | insulin | Manually authored subsystem map; mixed marker role (insulin + triglycerides) | Potentially misleading without role cues |
| Liver health | Liver enzyme pattern (`wave1_liv_enzyme_pattern`) | alt, ast, ggt | alt, ggt | ast | Manually authored subsystem map; wider than liver scoring rail | Thin-to-moderate; acceptable only with caveats |
| Liver health | Liver processing context (`wave1_liv_processing_context`) | alp, albumin, bilirubin, total_bilirubin | alp, albumin, bilirubin | total_bilirubin | Manually authored subsystem map; includes equivalence-duplicate key | Internally duplicated; contains false-missing risk |

## 4. Domain completeness vs subsystem evidence
Yes: the card can show narrower domain completeness while expanded subsystem evidence shows more included markers, because they use different evidence pools.

- Domain completeness (`evidence_completeness_numerator/denominator`) is derived in `domain_score_assembler.py` from:
  - **rail biomarker scores count**
  - plus **domain missing_marker_ids**
- Subsystem evidence in `wave1_subsystem_evidence.py` is derived from:
  - `included = (panel_biomarker_ids U scored_on_rail) AND expected_subsystem_markers`
  - where subsystem expected markers are manually authored, not tied to rail denominator definitions

Specific mismatch example:

- Liver rail in `scoring_policy.yaml` is only `alt` + `ast`.
- Liver subsystems surface `ggt`, `alp`, `albumin`, `bilirubin` (and `total_bilirubin` expected key).
- So user sees `1 of 2 expected markers` at domain level while also seeing multiple included subsystem markers.

Current UI wording does not fully explain that distinction, so users can interpret this as inconsistency rather than “score rail vs context-depth split.”

## 5. Marker role matrix

| Domain | Subsystem | Marker | Role | Source | Concern |
|---|---|---|---|---|---|
| Cardiovascular | Lipid transport | total_cholesterol | Score contributor | CV rail + subsystem map | Low concern |
| Cardiovascular | Lipid transport | ldl_cholesterol | Score contributor | CV rail + subsystem map | Low concern |
| Cardiovascular | Lipid transport | hdl_cholesterol | Score contributor | CV rail + subsystem map | Low concern |
| Cardiovascular | Lipid transport | triglycerides | Score contributor and context bridge (also metabolic) | CV rail + subsystem map | Cross-domain duplication ambiguity |
| Cardiovascular | Lipid transport | tc_hdl_ratio | Score contributor (derived ratio) | CV rail + subsystem map | Low concern |
| Cardiovascular | Homocysteine pathway | homocysteine | Contextual/adjacent contributor (not in CV scoring rail list) | Manual subsystem map | Thin single-marker subsystem |
| Cardiovascular | Vascular strain context | crp | Contextual marker (inflammatory semantics, not CV rail biomarker list) | Manual subsystem map | Label broader than support |
| Blood sugar | Glycaemic control | hba1c | Score contributor | Metabolic core (`_MET_CORE`) + subsystem map | Low concern |
| Blood sugar | Glycaemic control | glucose (missing) | Missing-for-confidence and score-contributor missing | Metabolic core + subsystem map | High semantic weight but absent |
| Blood sugar | Insulin and metabolic context | triglycerides | Contextual enhancer (also CV rail marker) | `_MET_ENHANCERS` comment + subsystem map | Mixed role not disclosed in UI |
| Blood sugar | Insulin and metabolic context | insulin (missing) | Missing-for-confidence enhancer | `_MET_ENHANCERS` + subsystem map | Important missing marker hidden inside mixed subsystem |
| Liver | Enzyme pattern | alt | Score contributor | Liver rail + subsystem map | Low concern |
| Liver | Enzyme pattern | ast (missing) | Missing score contributor | Liver rail + subsystem map | High importance missing |
| Liver | Enzyme pattern | ggt | Context/confidence contributor | Domain hepatic confidence pool + subsystem map | Role not explicit |
| Liver | Processing context | alp | Context/confidence contributor | Domain hepatic confidence pool + subsystem map | Role not explicit |
| Liver | Processing context | albumin | Context/confidence contributor | Domain hepatic confidence pool + subsystem map | Role not explicit |
| Liver | Processing context | bilirubin | Context/confidence contributor | Domain hepatic confidence pool + subsystem map | Canonical vs rail alias ambiguity nearby |
| Liver | Processing context | total_bilirubin (missing) | Unclear/duplicate key; effectively equivalence proxy | Manual subsystem map + rail-only SSOT row | False-missing risk |

## 6. Thin subsystem review

- **Vascular strain context = CRP only**: too broad a label for single-marker evidence; this is thin and can be misread as robust substructure.
- **Blood sugar insulin/metabolic context**: combines one missing key marker (insulin) and one cross-domain marker (triglycerides), which is useful but semantically mixed.
- **Liver processing context**: conceptually broad and currently polluted by an equivalence duplicate (`bilirubin` + `total_bilirubin` expected).
- **Liver as split domain**: strategic source warns liver is weaker for early splitting unless support is strong; current implementation is borderline and copy-dependent.

## 7. Available-but-not-shown markers
Confirmed from code and prior bb695d3c UAT/equivalence audits:

- No confirmed additional **uploaded + scored** cardiovascular markers omitted from current subsystems were found in the available bb695d3c evidence artifacts.
- No confirmed additional **uploaded + scored** blood sugar markers omitted beyond shown/missing (`hba1c`, `triglycerides`, missing `glucose`, missing `insulin`) were found.
- No confirmed additional **uploaded + scored** liver markers omitted beyond shown/missing (`alt`, `ggt`, `albumin`, `alp`, `bilirubin`, missing `ast`, false-missing `total_bilirubin`) were found.

Investigation constraint:

- Live API payload extraction for this environment could not be completed (`/api/analysis/result` auth/500 path during this run), so this section is limited to codebase logic plus existing bb695d3c UAT/equivalence evidence already in repo docs.

## 8. Duplicate/equivalent markers

- **`bilirubin` vs `total_bilirubin`**
  - Canonical identity is `bilirubin` (alias registry).
  - Subsystem expected list also includes `total_bilirubin`.
  - This creates duplicate-equivalence semantics and can produce false missing.
  - Current label fix (`Total Bilirubin`) does not fully solve semantic duplication in subsystem expectations.

- **`triglycerides` appears in cardiovascular and blood sugar subsystems**
  - This is plausibly legitimate cross-system evidence (lipid and metabolic coupling), not necessarily a defect.
  - But UI has no role tags, so repetition can look accidental rather than intentional bridge evidence.

- Other repeats:
  - No additional high-impact duplicate-equivalence cases were confirmed in current Wave 1 subsystem map from inspected code/docs.

## 9. False missing markers
Confirmed false-missing marker on bb695d3c:

| Missing marker shown | True missing? | Why |
|---|---|---|
| total_bilirubin | No (false missing) | Canonical scored marker is `bilirubin`; subsystem matching is exact-id and treats `total_bilirubin` as separate expected key |

Confirmed true missing markers on bb695d3c:

- `glucose`
- `insulin`
- `ast`

## 10. Fix options

| Option | Description | Pros | Cons | Risk | Recommendation |
|---|---|---|---|---|---|
| A | Keep current maps and improve copy | Fast; low engineering scope | Does not resolve model ambiguity or false-missing mechanics | Low/Medium | Necessary but insufficient alone |
| B | Narrow/rename weak subsystems | Better semantic honesty (e.g., CRP-only context labels) | Requires copy + contract coordination | Medium | Strong near-term improvement |
| C | Expand subsystem marker maps | Can reduce thinness where evidence exists | Risks cosmetic expansion if not biologically justified | Medium/High | Do selectively, evidence-first |
| D | Add marker roles | Makes score vs confidence vs context explicit | Contract/UI complexity increases | Medium | High-value structural improvement |
| E | Hide weak subsystems | Prevents over-claiming | Loses evidence transparency in near term | Medium | Consider for liver/CRP-only if wording cannot carry safely |
| F | Add equivalence/satisfies rules | Fixes false missing and duplicate identity semantics | Needs governed matching design and tests | Medium | Strongly recommended (targeted) |
| G | Redesign subsystem model before further UX polish | Long-term clean architecture | Slower delivery; blocks incremental wins | High | Use only if D/F cannot be layered incrementally |

## 11. Recommended next work package

- **Proposed work_id:** `WAVE1-SUBSYS-R1_marker_roles_and_equivalence`
- **Risk level:** HIGH (MIXED, because DTO semantics and deterministic evidence interpretation behavior are touched)
- **Likely files touched:**
  - `backend/core/analytics/wave1_subsystem_evidence.py`
  - `backend/core/models/results.py`
  - `backend/core/analytics/domain_score_assembler.py` (only if alignment fields are added)
  - `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
  - `frontend/app/types/analysis.ts`
  - `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx`
  - audit docs under `docs/audit-papers/`
- **Must not change:**
  - scoring thresholds or rail weights
  - unit conversion behavior
  - reference range logic
  - Knowledge Bus content
  - IDL records
  - core signal activation logic

Pragmatic sequence:

1. Add explicit marker roles (`score_contributor`, `confidence_contributor`, `contextual`, `missing_for_confidence`) to subsystem DTO.
2. Add governed equivalence/satisfies handling for known identity pairs (starting with bilirubin).
3. Tighten subsystem labels where support is thin.
4. Re-audit bb695d3c and one additional contrasting analysis before wider UX polish.
