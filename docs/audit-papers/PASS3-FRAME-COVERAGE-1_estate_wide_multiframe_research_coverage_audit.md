# PASS3-FRAME-COVERAGE-1 — Estate-Wide Multi-Frame Research Coverage Audit

**Work ID:** `PASS3-FRAME-COVERAGE-1_estate_wide_multiframe_research_coverage_audit`  
**Date:** 2026-06-02  
**SOP:** AUTOMATION_BUS_SOP_v1.3.1

---

## Executive verdict

**PASS (governance audit only).** All **55** packages in `pass3_legacy_package_mapping_plan_v1.yaml` are classified for frame-coverage risk. The estate shows widespread **multi-frame Pass_3 research** (52/55 with more than one matched spec) and **material edge-case-loss risk** when promoting legacy packages without frame adjudication. **Bulk ROUTE_A promotion must pause** except for a small cohort with documented divergence acceptance (6 packages). Creatinine is the reference pattern, not the sole scope. **No runtime, package, or frontend changes.**

---

## Artefacts inspected

| Artefact | Path |
|----------|------|
| KB-MAP-1 mapping plan | `knowledge_bus/governance/pass3_legacy_package_mapping_plan_v1.yaml` |
| Medical frame identity index | `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` |
| Creatinine adjudication | `knowledge_bus/governance/creatinine_multiframe_authority_decision_v1.yaml` |
| Context modifier catalogue | `knowledge_bus/governance/context_modifier_catalogue_draft_v1.yaml` |
| Pass_3 promotion register | `knowledge_bus/governance/pass3_promotion_decision_register_v1.yaml` |
| Runtime packages (read-only) | `knowledge_bus/packages/**` (`signal_library.yaml` override counts) |
| Audit output | `knowledge_bus/governance/pass3_frame_coverage_audit_v1.yaml` |
| Expansion candidates | `knowledge_bus/governance/medical_frame_identity_expansion_candidates_v1.yaml` |
| Builder script | `backend/scripts/build_pass3_frame_coverage_audit.py` |

---

## Estate-level methodology

1. Load the **55-package cohort** from KB-MAP-1 (authoritative register).
2. For each package, inherit route, Pass_3 spec list, and `multiple_pass3_frames` flag from the mapping plan.
3. **Read-only** inspect `knowledge_bus/packages/<package_id>/signal_library.yaml` where present to count **legacy override rules** (proxy for unmapped frame/escalation logic).
4. Classify `frame_coverage_status`, `edge_case_loss_risk`, and `promotion_safety_status` using route-priority rules (ROUTE_C → ROUTE_G → ROUTE_E → ROUTE_B → ROUTE_A → ROUTE_D/F), with **creatinine** and **high-risk** overrides from prior adjudication.
5. Emit machine-readable audit YAML and this report.

**Medical boundary:** Classifications describe **risk of losing valid edge-case reasoning**, not clinical truth. No package files were modified.

---

## 55-package cohort summary

| Metric | Value |
|--------|-------|
| Packages audited | 55 |
| With Pass_3 primary-biomarker match | 55 |
| With `multiple_pass3_frames` (KB-MAP-1) | 39 |
| With Pass_3 spec count > 1 (audit) | 52 |

### Frame coverage status (`summary_counts`)

| Status | Count |
|--------|------:|
| `pass3_multiple_frames_need_adjudication` | 36 |
| `pass3_partial_legacy_frames_not_fully_represented` | 16 |
| `legacy_contains_valid_unmapped_frame` | 1 |
| `legacy_likely_scaffold_or_retire_candidate` | 1 |
| `unclear_requires_manual_review` | 1 |
| `pass3_complete_for_known_frames` | 0 |

### Promotion safety status

| Status | Count |
|--------|------:|
| `blocked_pending_frame_adjudication` | 40 |
| `blocked_pending_pass3_enrichment` | 7 |
| `safe_after_documented_divergence_acceptance` | 6 |
| `blocked_pending_provenance_recovery` | 1 |
| `retire_candidate` | 1 |

### Edge-case-loss risk

| Risk | Count |
|------|------:|
| high | 23 |
| medium | 24 |
| low | 6 |
| none_detected | 1 |
| unknown | 1 |

---

## Route distribution (KB-MAP-1)

| Route | Count |
|-------|------:|
| ROUTE_C — multiple Pass_3 frames adjudication | 35 |
| ROUTE_A — exact signal match compile candidate | 13 |
| ROUTE_B — primary biomarker, signal mapping | 3 |
| ROUTE_D — legacy accepted with rationale | 1 |
| ROUTE_E — provenance recovery | 1 |
| ROUTE_F — retire candidate | 1 |
| ROUTE_G — manual medical review | 1 |

---

## Multi-frame risk summary

Most runtime legacy packages sit on **ROUTE_C** or carry **multiple Pass_3 investigation specs** for the same primary biomarker. Promoting or retiring a package using only one spec risks collapsing:

- distinct Pass_3 frames (e.g. ALT injury vs steatosis vs muscle source),
- legacy **override/escalation rules** (e.g. creatinine eGFR/K+, ALT Hy's Law),
- or parallel signal families (e.g. `signal_crp_high` vs `signal_systemic_inflammation`).

---

## Packages safe for continued promotion (conditional)

**6** packages: `safe_after_documented_divergence_acceptance` — single-spec ROUTE_A with ≤1 legacy override rule detected (e.g. `pkg_s24_neutrophils_high_neutrophilia`, `pkg_s24_urate_high_metabolic`, `pkg_s24_urea_high_renal`, `pkg_s24_vitamin_d_low_deficiency`, and related). Promotion still requires **documented frame selection**, not blind compile.

**0** packages: `safe_for_route_a_promotion` without documentation gate.

---

## Packages blocked pending frame adjudication

**40** packages — predominantly ROUTE_C, ROUTE_D, ROUTE_G, and high-risk ROUTE_C (CRP, ALT, apoB, etc.).

---

## Packages blocked pending Pass_3 enrichment

**7** packages — including **`pkg_s24_creatinine_high_renal`** (pattern case) and ROUTE_A packages with **≥2 legacy override rules** not clearly mapped to Pass_3 frames (e.g. ferritin low, hba1c high, TSH packages).

---

## Packages needing medical review

**Requires_medical_review: true** on **majority** of ROUTE_C, ROUTE_G, creatinine, and multi-override ROUTE_A entries. See `pass3_frame_coverage_audit_v1.yaml` per-package flags.

---

## Worked example 1 — Creatinine high (pattern)

| Layer | Finding |
|-------|---------|
| Pass_3 | `inv_creatinine_high_reduced_glomerular_filtration` in kb52c; UACR override |
| Legacy s24 | eGFR &lt; 60 and potassium &gt; 5.2 overrides — **not** in kb52c |
| Route label | ROUTE_A (misleading without override audit) |
| Classification | `pass3_partial_legacy_frames_not_fully_represented`, **high** edge-case risk |
| Promotion | **blocked_pending_pass3_enrichment** — see `creatinine_multiframe_authority_decision_v1.yaml`, CF-CREATININE-001 |

---

## Worked example 2 — ROUTE_C: `pkg_s24_alt_high_hepatocellular_injury`

| Field | Value |
|-------|-------|
| Pass_3 frames | 3 (`hepatocellular_injury`, `steatotic_liver`, `muscle/exertional`) |
| Legacy overrides | 3 (`or_alt_hepatocellular_severity`, `or_alt_impaired_function` / Hy's Law, `or_alt_mixed_cholestatic`) |
| Risk | **high** — legacy escalation rules encode frame richness not reduced to one Pass_3 compile |
| Action | Adjudicate frames, map overrides to Pass_3 or index, then compile |

---

## Worked example 3 — ROUTE_A: `pkg_s24_ferritin_low_iron_deficiency`

| Field | Value |
|-------|-------|
| KB-MAP-1 | ROUTE_A exact match to `inv_ferritin_low_iron_store_depletion` |
| Pass_3 estate | Also lists high ferritin / overload specs for same biomarker |
| Legacy overrides | **3** rules in `signal_library.yaml` |
| Verdict | **Not** safe for naive ROUTE_A promotion — `pass3_partial_legacy_frames_not_fully_represented`, enrichment before pilot |

---

## Estate-level questions (explicit answers)

1. **Multiple Pass_3 frames same primary biomarker?** — **39** (KB-MAP-1 `multiple_pass3_frames`); **52** with &gt;1 matched spec id in audit.
2. **Legacy override logic not clearly in Pass_3?** — **16** partial + **7** enrichment-blocked ROUTE_A; creatinine is canonical example.
3. **Safe for ROUTE_A without edge-case loss?** — **0** unconditional; **6** with documented divergence acceptance only.
4. **Require Pass_3 enrichment before retirement/activation?** — **7** enrichment-blocked + creatinine estate pattern.
5. **Require medical review?** — **40+** frame-adjudication blocked; ROUTE_G chronic inflammation; most ROUTE_C.
6. **Most at-risk of frame collapse?** — Creatinine, CRP/s24, ALT, ferritin high/low, apoB, KBP-0001 multi-signal baseline.
7. **Prioritise after creatinine?** — ALT, CRP (`signal_crp_high`), ferritin family, apoB (see `medical_frame_identity_expansion_candidates_v1.yaml`).
8. **Expand identity index beyond creatinine?** — **Yes**, before bulk promotion — at least top 6 families in expansion candidates file.
9. **Context modifier catalogue gaps?** — Adequate for creatinine pattern; **no new classes required** for this audit; binding deferred (CF-CONTEXT-MOD-2).
10. **Promotion work to pause?** — **Bulk ROUTE_A wave** and any package with `blocked_pending_frame_adjudication` or `blocked_pending_pass3_enrichment` (47 of 55).

---

## Implications for KB-UTIL package promotion

- Do not treat ROUTE_A as “safe by label.”
- Require **frame coverage audit row** per package before compile/promote.
- Creatinine pilot path is **blocked** for enrichment (CF-CREATININE-001), not reopened.

---

## Implications for medical frame identity index

- Creatinine index is **exemplar only** (4 frames).
- Expand index to **ALT, CRP, ferritin, apoB** families before promotion (CF-PASS3FRAME-001).

---

## Implications for context modifier governance

- Catalogue is sufficient for audit classification; **runtime binding** remains CONTEXT-MOD-2.
- Creatinine modifiers documented; no catalogue schema change required.

---

## Carry-forward updates

| ID | Update |
|----|--------|
| CF-CREATININE-001 | Remains **Open** — audit confirms enrichment gate |
| CF-CRPPASS3-001 | Remains **Open** — audit: `pkg_s24_crp_high_inflammation` high risk, frame adjudication |
| CF-CHRONICINFL-001 | Remains **Open** — ROUTE_G confirmed |
| CF-MRIMPROVE-004 | Remains **Open** — ROUTE_E `pkg_lipid_transport` |
| CF-CONTEXT-MOD-2 | Remains **Open** |
| CF-MRIMPROVE-002 / 003 | Remain **Deferred** — ROUTE_C context packages in audit |
| **CF-PASS3FRAME-001** | **Added** — expand identity index to high-risk families |
| **CF-PASS3FRAME-002** | **Added** — Pass_3 enrichment queue (7+ enrichment-blocked) |
| **CF-PASS3FRAME-003** | **Added** — promotion pause list (47 blocked packages) |

---

## Recommended next sprint

**PASS3-FRAME-INDEX-2** — expand `medical_frame_identity_index_v1.yaml` for ALT and CRP families using audit + medical review gates (non-runtime).

---

## Validation output (actual)

```
validation_status: PASS
errors: 0
index_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\medical_frame_identity_index_v1.yaml

validation_status: PASS
errors: 0
catalogue_path: C:\Users\abroa\HealthIQ-AI-v5\knowledge_bus\governance\context_modifier_catalogue_draft_v1.yaml

day_one_architecture_validation: PASS

....                                                                     [100%]
...........                                                              [100%]
..........                                                               [100%]
```

---

## Runtime boundary confirmation

No changes to `knowledge_bus/packages/*`, SignalEvaluator, SignalRegistry, loaders, frontend, or SSOT.
