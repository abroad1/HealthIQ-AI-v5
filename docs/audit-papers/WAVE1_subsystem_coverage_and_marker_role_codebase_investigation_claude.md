# Wave 1 Subsystem Coverage and Marker Role Codebase Investigation

**Auditor:** Claude Code (independent — Cursor findings were not consulted before analysis; Cursor conclusion reviewed only at §12)  
**Scope:** Wave 1 subsystem evidence model — coverage, marker roles, duplication, false-missing, architectural fitness  
**Analysis reference:** `bb695d3c-453e-4e49-abff-ae80587b4248`  
**Git:** `main` @ `caf64cf`  
**Method:** Direct source reading of `wave1_subsystem_evidence.py`, `domain_score_assembler.py`, `scoring_policy.yaml`, `biomarkers.yaml`, `results.py`, `Wave1SubsystemEvidenceSection.tsx`, `Wave1DomainCards.tsx`, plus all authority documents listed in the task brief.

---

## 1. Executive Verdict

**The current Wave 1 subsystem evidence model is thin-but-acceptable for v1 only under strict wording controls — and one subsystem (Vascular strain context) has a label that meaningfully overstates its marker support.**

The structural problems are:

1. The liver domain has a genuine **two-tier architecture split** (scoring rail = alt+ast only; subsystem evidence = 5+ hepatic markers) with no user-visible explanation. This is the root of "1 of 2 expected markers" on the domain card while the expanded view shows ALT, GGT, ALP, Albumin, Bilirubin.

2. **"Vascular strain context" is a single-marker subsystem (CRP only) where CRP is not even on the cardiovascular scoring rail.** CRP belongs to the `inflammatory` rail in `scoring_policy.yaml`. The label overstates analytical depth.

3. **No marker role differentiation exists in the emitted data.** `evidence_role` is hardcoded `null` for every subsystem row (`results.py:210`, `wave1_subsystem_evidence.py:169`). Score contributors, confidence contributors, and contextual markers are presented identically in the UI.

4. One confirmed false-missing marker: `total_bilirubin` appearing as "Not uploaded" when `bilirubin` is present and scored — because `total_bilirubin` is a `display_label_rail_only` entry in `biomarkers.yaml` that should never have been placed in expected subsystem marker IDs.

5. `triglycerides` appears as an included marker in two domains (CV: Lipid transport; Blood sugar: Insulin and metabolic context) without any cross-system explanation.

These are all addressable within the current architecture. The model does not need wholesale redesign, but three specific interventions are warranted before further UX polish.

---

## 2. Strategic Authority Summary

From `docs/architecture/User Health to Systems Map_FINAL.md`:

- Visible sub-scores/subsystems only where **biologically distinct, understandable, supported by real deterministic logic, and not heavily overlapping**.
- **Liver health is explicitly named as a poor candidate for early splitting** if sub-scores are weakly supported.
- Risk 6 (§Key risks to avoid): "Do not show visible sub-scores unless they are genuinely distinct, biologically supportable, and not merely cosmetic splits."
- Cardiovascular is the **good candidate** for hierarchical sub-scores (lipid transport / vascular strain / homocysteine-related vascular risk) — matching the current Wave 1 model closely.
- Blood sugar and Liver are rated "Strong" and "Moderate to strong" at the domain level, but subdomain splitting is not specifically endorsed for these two.

**Application to current model:** The Cardiovascular sub-structure (3 subsystems) aligns well with the strategic authority. The Liver sub-structure is architecturally present but exposes the exact weak-support risk the authority document warned against: the "Liver processing context" subsystem lists 4 expected markers, while the scoring rail tracks only 2 (alt, ast), making subsystem evidence and domain completeness appear contradictory to a user.

---

## 3. Current Subsystem Definition Matrix

Source: `backend/core/analytics/wave1_subsystem_evidence.py` lines 27–86.  
Rail source: `backend/ssot/scoring_policy.yaml` lines 19–46.

| Domain | Subsystem ID | Subsystem Label | Expected Markers | Included on bb695d3c | Missing on bb695d3c | Source of Marker Set | Assessment |
|---|---|---|---|---|---|---|---|
| Cardiovascular | `wave1_cv_lipid_transport` | Lipid transport | total_cholesterol, ldl_cholesterol, hdl_cholesterol, triglycerides, tc_hdl_ratio | All 5 | None | Cardiovascular scoring rail (`scoring_policy.yaml` line 26) | **Sufficient — rail-aligned, complete** |
| Cardiovascular | `wave1_cv_homocysteine_pathway` | Homocysteine pathway | homocysteine | homocysteine | None | Manually authored (`wave1_subsystem_evidence.py:43–45`) | **Thin (single marker) but biologically distinct; acceptable when panel includes it; fragile on panels without homocysteine** |
| Cardiovascular | `wave1_cv_vascular_strain` | Vascular strain context | crp | crp | None | Manually authored — CRP only; NOT from CV scoring rail | **Weak: single marker from the inflammatory rail, not the cardiovascular rail. Label overstates depth. See §6.** |
| Blood sugar | `wave1_met_glycaemic_control` | Glycaemic control | glucose, hba1c | hba1c | glucose (true missing) | Metabolic scoring rail (`scoring_policy.yaml` line 22) — partial (insulin excluded) | **Acceptable — 2-marker glycaemic core; bb695d3c shows 1/2** |
| Blood sugar | `wave1_met_insulin_metabolic` | Insulin and metabolic context | insulin, triglycerides | triglycerides | insulin (true missing) | Partially from metabolic rail (insulin); triglycerides imported from CV rail context | **Thin on bb695d3c: 1 of 2 markers (only triglycerides), which alone does not establish an insulin/metabolic context — see §6** |
| Liver | `wave1_liv_enzyme_pattern` | Liver enzyme pattern | alt, ast, ggt | alt, ggt | ast (true missing) | Liver scoring rail (alt, ast) + GGT extension | **Acceptable — GGT extension adds clinical depth; 2/3 on this panel** |
| Liver | `wave1_liv_processing_context` | Liver processing context | alp, albumin, bilirubin, total_bilirubin | alp, albumin, bilirubin | total_bilirubin (false missing) | Manually authored — no SSOT rail anchor | **Has confirmed defect (total_bilirubin false missing); otherwise medically legitimate; all four markers are extended hepatic context markers, none on the scoring rail** |

---

## 4. Domain Completeness vs Subsystem Evidence

This is the most architecturally important finding in the investigation. It explains a confusing user-visible discrepancy.

### The split is real and mechanically traceable

**Domain completeness** (`evidence_completeness_numerator / evidence_completeness_denominator`) is calculated in `domain_score_assembler.py:340–355` via `_evidence_completeness_for_rail()`:

```python
data = _system_rail_data(hss, system_key)   # → health_system_scores["liver"]
bs = data.get("biomarker_scores")            # → markers scored on the SCORING RAIL only
scored_count = len(bs) if isinstance(bs, list) else 0
missing_count = len(missing_marker_ids)     # → _missing_for_rail() output
denominator = scored_count + missing_count
numerator = scored_count
```

The `liver` scoring rail (`scoring_policy.yaml` lines 43–46) defines only `["alt", "ast"]`. On bb695d3c, `ast` is not uploaded:
- `scored_count = 1` (alt only)
- `missing_count = 1` (ast)
- Result: **1 of 2**

**Subsystem evidence** is assembled separately in `wave1_subsystem_evidence.py` using `_partition_subsystem_markers()` against `panel_biomarker_ids | scored_on_rail`. The liver subsystem expected sets include:
- `wave1_liv_enzyme_pattern`: alt, ast, ggt — includes `ggt` which is **not on the liver scoring rail**
- `wave1_liv_processing_context`: alp, albumin, bilirubin, total_bilirubin — **none of these are on the liver scoring rail**

On bb695d3c, subsystem evidence includes ALT, GGT, ALP, Albumin, Bilirubin — 5 markers. Domain completeness shows 1/2. These are tracking different things (scoring rail vs extended hepatic marker pool), and this is nowhere explained in the UI.

### Does the UI make this clear?

**No.** The domain completeness panel ("1 of 2 expected markers included") and the expanded subsystem evidence (5 included markers across two subsystems) present contradictory counts with no bridging explanation. A user seeing "1 of 2" and then 5 included markers has no way to resolve this without external explanation. This is a copy and architecture communication gap, not a code defect.

### Is the split architecturally correct?

Yes — it is intentional. The scoring rail is narrower than the subsystem evidence by design. The domain score tracks what the engine actually scores; the subsystem evidence tracks what is informationally relevant. But without copy that acknowledges this split, the mismatch creates confusion and undermines trust in the liver card specifically.

---

## 5. Marker Role Matrix

`evidence_role` exists in `SubsystemEvidenceV1` (`results.py:209`) but is always `null` — emitted as `null` in `wave1_subsystem_evidence.py:169`. The role assignments below are derived from scoring architecture, not from any emitted data.

| Domain | Subsystem | Marker | Inferred Role | Source of Role Assignment | Concern |
|---|---|---|---|---|---|
| Cardiovascular | Lipid transport | total_cholesterol | Score contributor | CV scoring rail (`scoring_policy.yaml:26`) | None |
| Cardiovascular | Lipid transport | ldl_cholesterol | Score contributor | CV scoring rail | None |
| Cardiovascular | Lipid transport | hdl_cholesterol | Score contributor | CV scoring rail | None |
| Cardiovascular | Lipid transport | triglycerides | Score contributor (CV) / Confidence contributor (Blood sugar) | CV rail + metabolic context | Cross-system role; creates subsystem duplication — see §8 |
| Cardiovascular | Lipid transport | tc_hdl_ratio | Score contributor (derived ratio) | CV rail | None |
| Cardiovascular | Homocysteine pathway | homocysteine | Contextual / confidence contributor | Not on any scoring rail | Biologically distinct; single-marker subsystem disappears entirely on panels without homocysteine |
| Cardiovascular | Vascular strain context | crp | Contextual marker — inflammatory rail, not CV rail | `scoring_policy.yaml` inflammatory system (`line 29–30`) | **Most significant role concern: implies CV scoring input but contributes only to inflammatory score (0.15 weight)** |
| Blood sugar | Glycaemic control | glucose | Score contributor | Metabolic rail | None |
| Blood sugar | Glycaemic control | hba1c | Score contributor | Metabolic rail | None |
| Blood sugar | Insulin and metabolic context | insulin | Score contributor | Metabolic rail | None; true missing on bb695d3c |
| Blood sugar | Insulin and metabolic context | triglycerides | Contextual / confidence proxy | Borrowed from CV rail; not on metabolic scoring rail | Cross-system: scores in CV rail, contextual in blood sugar subsystem |
| Liver | Liver enzyme pattern | alt | Score contributor | Liver scoring rail (`scoring_policy.yaml:46`) | None |
| Liver | Liver enzyme pattern | ast | Score contributor | Liver scoring rail | None; true missing on bb695d3c |
| Liver | Liver enzyme pattern | ggt | Confidence / contextual contributor | In `_HEP_CONFIDENCE_POOL`; not on liver scoring rail | GGT extends clinical depth but does not directly drive liver score |
| Liver | Liver processing context | alp | Confidence / contextual contributor | `_HEP_CONFIDENCE_POOL` (`domain_score_assembler.py:71`) | Clinically appropriate for hepatic context |
| Liver | Liver processing context | albumin | Confidence / contextual contributor | `_HEP_CONFIDENCE_POOL` | Appropriate; contributes to `_liver_confidence_tier_domain()` |
| Liver | Liver processing context | bilirubin | Confidence / contextual contributor | `_HEP_CONFIDENCE_POOL` | Appropriate |
| Liver | Liver processing context | total_bilirubin | **Non-existent marker (display_label_rail_only)** | `biomarkers.yaml:1578–1586` | **Should never appear as an expected subsystem marker; is always false-missing — confirmed defect** |

---

## 6. Thin Subsystem Review

### wave1_cv_vascular_strain — "Vascular strain context" (CRP only)

This is the most problematic subsystem label in the current model.

**The evidence:** `_WAVE1_CV_VASCULAR` at `wave1_subsystem_evidence.py:47–52` defines expected markers as `("crp",)` — a single marker.

**The problem:** CRP is assigned to the `inflammatory` rail in `scoring_policy.yaml` (lines 27–30), not the cardiovascular rail. The cardiovascular domain score is computed entirely from the lipid panel (total_cholesterol, ldl, hdl, triglycerides, tc_hdl_ratio). CRP has no connection to the cardiovascular score calculation. Placing CRP under a "Vascular strain context" subsystem inside the Cardiovascular health card implies it contributes to cardiovascular scoring — it does not.

**What the label implies vs what it delivers:**
- Implies: a supported analytical construct connecting detected vascular strain to the cardiovascular domain score
- Delivers: one inflammation marker that has biological relevance to cardiovascular risk in clinical literature, but is architecturally decoupled from the cardiovascular score computation

**Strategic authority position:** `User Health to Systems Map_FINAL.md` lists CRP under cardiovascular health as a candidate contributing system ("vascular strain / inflammation"), which lends biological legitimacy. But the same document warns against cosmetic splits without real deterministic logic support. A single non-scoring-rail marker is at the boundary of that warning.

**Verdict:** "Vascular strain context" is too broad for a single inflammation marker that does not contribute to the cardiovascular score. On panels where CRP is absent, this entire subsystem renders as "0 included / 1 missing (Not uploaded)" — a subsystem that shows only absence for a label implying a significant construct. The label must be narrowed (e.g., "Inflammation context") or the subsystem should be suppressed when CRP is absent.

### wave1_met_insulin_metabolic — "Insulin and metabolic context" (when only triglycerides present)

On bb695d3c, insulin is absent, leaving only triglycerides as included. "Insulin and metabolic context" with only triglycerides delivers a weak evidence base for a subsystem named after insulin. Triglycerides is an indirect insulin-resistance proxy; the label implies insulin measurement. This is a copy problem as much as an evidence problem — the label anchors the subsystem to a marker that is absent from this panel.

### wave1_cv_homocysteine_pathway — "Homocysteine pathway" (single marker)

Biologically appropriate as a distinct one-marker pathway. But on panels without homocysteine, this subsystem renders as "0 included / 1 missing (Not uploaded)" — a gap advertisement rather than an evidence row. No other Wave 1 subsystem degrades this cleanly. This is acceptable for v1 if combined with a UI guard that suppresses or de-emphasises zero-evidence subsystems.

---

## 7. Available-but-Not-Shown Markers

For bb695d3c, the following markers contribute to domain logic but are invisible in subsystem evidence:

| Marker | Relevant to | Present in domain logic | In any subsystem | Concern |
|---|---|---|---|---|
| `total_protein` | Liver confidence | In `_HEP_CONFIDENCE_POOL` (`domain_score_assembler.py:79`) | **No** | Silently contributes to liver confidence tier; not shown in any evidence row |
| `globulin` | Liver confidence | In `_HEP_CONFIDENCE_POOL` (`domain_score_assembler.py:80`) | **No** | Same as above |
| `ggt` | Liver enzyme pattern | In `wave1_liv_enzyme_pattern` expected set | **Yes** | Correctly shown |
| `tyg_index` (derived) | Blood sugar confidence | Referenced in `_metabolic_blood_sugar_confidence_tier()` (`domain_score_assembler.py:282`) | **No** | Silently improves blood sugar confidence when present in derived_ratios; invisible in evidence chain |

Additionally: any non-HDL cholesterol derived ratio is referenced in `_cardiovascular_confidence_tier()` but not explicitly in any CV subsystem definition.

---

## 8. Duplicate / Equivalent Marker Audit

### triglycerides — appears in two subsystems

| Occurrence | Subsystem | Domain | Inferred Role |
|---|---|---|---|
| `wave1_cv_lipid_transport` | Lipid transport | Cardiovascular | Score contributor (CV scoring rail) |
| `wave1_met_insulin_metabolic` | Insulin and metabolic context | Blood sugar | Contextual proxy for insulin resistance |

**Is this legitimate?** Biologically yes — triglycerides are a CV lipid marker and an insulin-resistance proxy (TG:HDL ratio, TyG index). The cross-system appearance is not an error. However, presenting triglycerides as an "included" marker under both CV and blood sugar subsystems without explanation may confuse users who expect each marker to have a primary home. The duplication is intentional (`wave1_subsystem_evidence.py:64`) but unexPlained in the UI.

### bilirubin vs total_bilirubin

This is the confirmed false-missing defect (previously investigated in full in `WAVE1_subsystem_marker_equivalence_investigation.md`).

| ID | In biomarkers.yaml | Role | Parsed as | In subsystem expected |
|---|---|---|---|---|
| `bilirubin` | Yes (canonical, line 1558) | Scoreable canonical identity | `bilirubin` | Yes — correctly |
| `total_bilirubin` | Yes (`display_label_rail_only: true`, line 1578) | Label-only display key; not a parseable identity | N/A | Yes — **incorrectly** |

`biomarkers.yaml:1582` explicitly states: "canonical lab identity is bilirubin". Including this display-only key in expected subsystem markers causes `total_bilirubin` to always appear as "Not uploaded" regardless of whether bilirubin is scored. This is a permanent false-positive defect in the current state.

---

## 9. False Missing Marker Audit

All confirmed false-missing markers on bb695d3c:

| Missing marker shown | Subsystem | Truly absent? | Equivalent present? | Verdict |
|---|---|---|---|---|
| `total_bilirubin` | `wave1_liv_processing_context` | **No** | `bilirubin` present and scored (optimal) | **Confirmed false-missing — defect** |

All other missing markers on bb695d3c are confirmed true-missing:

| Missing marker shown | Subsystem | Verdict |
|---|---|---|
| `glucose` | Glycaemic control | True missing — not uploaded on this panel |
| `insulin` | Insulin and metabolic context | True missing — not uploaded on this panel |
| `ast` | Liver enzyme pattern | True missing — not uploaded on this panel |

**Domain-level completeness note:** The liver card's "1 of 2" completeness is not a false-missing — it accurately reflects the liver scoring rail (alt + ast). The confusion is architectural (scoring rail scope vs subsystem evidence scope), not a marker identity defect.

---

## 10. Fix Options

| Option | Description | Pros | Cons | Risk | Recommendation |
|---|---|---|---|---|---|
| **A** | Keep current maps; improve copy — add UI explanatory text distinguishing scoring completeness from evidence breadth; add bridging language near "1 of 2" for liver | No backend risk; immediate trust improvement for liver completeness confusion | Does not fix false-missing; does not fix role confusion | Low | **Recommended as immediate action — copy/label gap** |
| **B** | Narrow/rename weak subsystems — rename `wave1_cv_vascular_strain` to better reflect CRP-only scope; rename `wave1_met_insulin_metabolic` label when insulin is absent | Reduces misleading label surface | Frontend may need dynamic or static copy changes | Low | **Recommended in combination with A** |
| **C** | Expand subsystem marker maps — add more biologically justified markers (e.g. GGT already in expected set; could add total_protein if clinical justification established) | Better evidence coverage | Requires care not to misrepresent non-scoring markers as score contributors | Low-Medium | **Selective only; GGT is already correct in enzyme pattern — do not expand without clinical governance** |
| **D** | Add marker roles — populate `evidence_role` field for each emitted subsystem marker row as `score_contributor` / `confidence_contributor` / `contextual` | Resolves role confusion structurally; enables role-differentiated UI rendering | New surface area; needs governance, contract update, tests | Medium | **Recommended as Wave 1.5 or Wave 2 — not a launch blocker** |
| **E** | Suppress empty subsystems — hide `wave1_cv_vascular_strain` when CRP is absent; hide `wave1_cv_homocysteine_pathway` when homocysteine is absent | Prevents zero-evidence subsystem rendering | Subsystems appear/disappear across panels; may reduce perceived coverage | Low | **Acceptable as UI guard, not as a fix for underlying label problem** |
| **F** | Fix total_bilirubin false-missing — remove `total_bilirubin` from `wave1_liv_processing_context` expected_marker_ids; expected set becomes `("alp", "albumin", "bilirubin")` | Fixes confirmed defect; prevents permanent false-positive on every liver card | Point fix only; does not solve future equivalence risks | Low | **Strongly recommended — confirmed defect, Option A in prior investigation** |
| **G** | Redesign subsystem model — introduce governed equivalence layer, marker roles, domain/subsystem split documentation in DTO | Future-proof architecture | Significant scope; risks stalling v1 improvements | High | **Deferred to Wave 2 or post-commercial launch** |

---

## 11. Recommended Next Work Packages

Two independent work packages are warranted. They can be sequenced or run in parallel.

### WP1 — False-missing fix (confirmed defect)

| Field | Value |
|---|---|
| **Proposed work_id** | `WAVE1-EQUIV1_subsystem_bilirubin_false_missing_fix` |
| **Risk level** | LOW |
| **change_type** | BEHAVIOUR (modifies subsystem partition output — `total_bilirubin` no longer emitted as missing) |
| **Files likely touched** | `backend/core/analytics/wave1_subsystem_evidence.py` — remove `total_bilirubin` from `_WAVE1_LIV_PROCESSING.expected_marker_ids`; update expected tuple to `("alp", "albumin", "bilirubin")`; `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py` — update assertions |
| **What must not change** | Scoring policy, alias registry, canonical bilirubin identity, `total_bilirubin` label authority for display purposes, IDL/root-cause behavior |
| **Notes** | `WAVE1_subsystem_marker_equivalence_investigation.md` fully specifies this fix (Option A of that document). Prior investigation is the authoritative source. |

### WP2 — Subsystem label and copy alignment (UX trust gap)

| Field | Value |
|---|---|
| **Proposed work_id** | `WAVE1-UX2_subsystem_label_completeness_copy_alignment` |
| **Risk level** | LOW |
| **change_type** | CONTENT (copy and label changes; no analytical logic changes) |
| **Files likely touched** | `backend/core/analytics/wave1_subsystem_evidence.py` — rename `wave1_cv_vascular_strain` label (e.g., "Inflammation context"); compiler narrative files for liver confidence sentence; `frontend/app/components/results/Wave1DomainCards.tsx` — add explanatory copy near domain completeness counter |
| **What must not change** | Scoring rails, subsystem IDs and expected marker sets (except WP1), IDL records, domain score computation, any backend analytical logic |
| **Notes** | Specifically: (1) rename "Vascular strain context" to something that does not imply cardiovascular scoring input; (2) add one-line explanation near "1 of 2" liver completeness: scoring completeness tracks core liver markers; expanded evidence shows additional hepatic context markers; (3) fix liver confidence_sentence to not list already-included markers as "needed" (GGT/ALP/albumin contradiction noted in UAT) |

---

## 12. Independent Verdict on Cursor's Conclusion

Cursor concluded the model is "thin-but-acceptable only with careful wording" with four primary concerns. My findings, derived independently from source files:

| Cursor concern | My finding | Agreement |
|---|---|---|
| CRP-only "Vascular strain context" | Confirmed — and severity escalated. CRP is not on the CV scoring rail at all (it is on the `inflammatory` rail). "Careful wording" alone is insufficient; the label must change or the subsystem must be renamed. | **Partial: confirmed, but higher severity than Cursor rated** |
| Mixed score/confidence/context roles | Confirmed — `evidence_role` is hardcoded `null`; no differentiation is emitted. Architecture supports adding roles as a future improvement. | **Confirmed** |
| Liver domain completeness not aligning with subsystem evidence | Confirmed and mechanically explained — scoring rail = alt+ast only (2 markers); subsystem evidence = broader hepatic pool (5+ markers). Intentional architecture, but unexplained to users. | **Confirmed** |
| bilirubin / total_bilirubin false missing | Confirmed. Root cause: `total_bilirubin` is `display_label_rail_only: true` in `biomarkers.yaml:1578` and should never appear in expected subsystem marker IDs. | **Confirmed** |

**Additional concerns not surfaced by Cursor as primary findings:**

| Concern | Detail |
|---|---|
| `total_protein` and `globulin` in liver confidence pool but invisible in subsystems | These silently influence `_liver_confidence_tier_domain()` without appearing in any evidence row visible to the user |
| "Insulin and metabolic context" label when only triglycerides is included | Subsystem name anchors to absent insulin; only triglycerides shown — already present in the CV card |
| TyG index silently improves blood sugar confidence tier | Referenced in `_metabolic_blood_sugar_confidence_tier()` but not represented in any subsystem; invisible evidence improvement |

**Overall verdict:** Cursor's conclusion is directionally correct. All four primary concerns are independently verified. The word "acceptable" is conditional on WP1 (false-missing defect fix) and WP2 (label/copy alignment) being completed before commercial use. Without those two, the current state carries material trust risk specifically on partial-evidence liver panels and on any panel where the label "Vascular strain context" appears alongside thin or absent CRP evidence.

---

*Investigation complete. No repository code modified.*
