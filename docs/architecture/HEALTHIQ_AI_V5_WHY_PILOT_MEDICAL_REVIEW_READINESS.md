# HealthIQ AI v5 — WHY Pilot Medical Review Readiness (Gate 2.5)

**Work ID:** `ARCH-CONV-GATE2_5`  
**Branch:** `feature/arch-conv-gate2-5-medical-review-readiness`  
**Baseline HEAD (kernel start):** `9ce7853beaea2ba40eb3ed076483ab9ecedaea86`  
**change_type:** CONTENT  
**runtime_change:** NONE  
**Initial Gate 2.5 decision:** **CONDITIONAL_GO**  
**Post-ratification status (2026-07-26):** **CONDITIONS 1–4 CLOSED** — ownership, dual-gate model, named ratifier, and pilot capacity confirmed by human project authority. Pre-review engineering prerequisites remain (§7.2).

This document does **not** approve or promote any medical asset, does **not** authorise Package 3B content promotion, and does **not** declare beta readiness.

---

## 1. Exact pilot cohort (confirmed)

Reconciled to Gate 0 `HEALTHIQ_AI_V5_WHY_MIGRATION_PILOT_COHORT.md` without addition or removal.

**Totals:** **5** signal families / **10** live activation frames (verified in production `SignalRegistry` at Gate 2.5).

| # | signal_id | activation_key | source_spec_id | package_id | current WHY authority | legacy YAML | compiled hypothesis | consumer surface | clinician surface | medical review type required |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | signal_vitamin_d_low | `signal_vitamin_d_low::inv_vitamin_d_low_deficiency` | inv_vitamin_d_low_deficiency | pkg_s24_vitamin_d_low_deficiency | **compiled** (`RUNTIME_PROMOTED_COMPILED_SIGNAL_IDS`); legacy YAML still on disk | `knowledge_bus/root_cause/hypotheses/vitamin_d_low_hypotheses_v1.yaml` | AVAILABLE — `knowledge_bus/compiled/hypotheses/signal_vitamin_d_low.yaml` | Not in `_LEAD_SIGNAL_HINTS` | Compiled root-cause branch | RETIREMENT_CONFIRMATION_ONLY |
| 2a | signal_homocysteine_high | `signal_homocysteine_high::inv_homocysteine_high_b_vitamin_related_methylation_impairment` | inv_homocysteine_high_b_vitamin_related_methylation_impairment | pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment | **legacy** shared `hcy_hypotheses_v1.yaml` | `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml` | none | Lead hint (family) | Legacy root-cause registry | FULL_NEW_MEDICAL_REVIEW |
| 2b | signal_homocysteine_high | `signal_homocysteine_high::inv_homocysteine_high_metabolic` | inv_homocysteine_high_metabolic | pkg_s24_homocysteine_high_metabolic | legacy (same YAML) | same | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 2c | signal_homocysteine_high | `signal_homocysteine_high::inv_homocysteine_high_renal_clearance_reduction` | inv_homocysteine_high_renal_clearance_reduction | pkg_kb52c_homocysteine_high_renal_clearance_reduction | legacy (same YAML) | same | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 3a | signal_mcv_high | `signal_mcv_high::inv_mcv_high_macrocytosis` | inv_mcv_high_macrocytosis | pkg_s24_mcv_high_macrocytosis | **legacy** `mcv_high_hypotheses_v1.yaml` | `knowledge_bus/root_cause/hypotheses/mcv_high_hypotheses_v1.yaml` | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 3b | signal_mcv_high | `signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis` | inv_mcv_high_megaloblastic_macrocytosis | pkg_kb52c_mcv_high_megaloblastic_macrocytosis | legacy (same) | same | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 3c | signal_mcv_high | `signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis` | inv_mcv_high_nonmegaloblastic_macrocytosis | pkg_kb52c_mcv_high_nonmegaloblastic_macrocytosis | legacy (same) | same | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 4 | signal_free_t3_low | `signal_free_t3_low::inv_free_t3_low_low_t3_syndrome` | inv_free_t3_low_low_t3_syndrome | pkg_kb47_free_t3_low_low_t3_syndrome | **legacy** `free_t3_low_hypotheses_v1.yaml` | `knowledge_bus/root_cause/hypotheses/free_t3_low_hypotheses_v1.yaml` | none | Lead hint | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 5a | signal_tpo_ab_high | `signal_tpo_ab_high::inv_tpo_ab_high_autoimmune_hypothyroid_pattern` | inv_tpo_ab_high_autoimmune_hypothyroid_pattern | pkg_kb59_tpo_ab_high_autoimmune_hypothyroid_pattern | **legacy** `tpo_ab_high_hypotheses_v1.yaml` | `knowledge_bus/root_cause/hypotheses/tpo_ab_high_hypotheses_v1.yaml` | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |
| 5b | signal_tpo_ab_high | `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` | inv_tpo_ab_high_euthyroid_autoimmune_risk | pkg_kb59_tpo_ab_high_euthyroid_autoimmune_risk | legacy (same) | same | none | Lead hint (family) | Legacy | FULL_NEW_MEDICAL_REVIEW |

**Post-PKG2 note:** `signal_free_t3_low` package provenance is now `EXPLICIT_SPEC` / production-reachable (Gate 0 assumed BLOCKED until Package 2). Cohort membership unchanged.

**No silent expansion:** androgen panel and remaining ~35 legacy YAML assets remain excluded per Gate 0.

---

## 2. Medical-review ownership

### 2.0 Human ratification record (2026-07-26) — CLOSED

| Decision | Recorded value |
|---|---|
| Operating model | **Dual-gate APPROVED** |
| Gate 1 — medical review | **GPT** acting as **HealthIQ AI Head of Medical Research** performs the structured medical review (APPROVE / REVISE / REJECT frame dispositions) |
| Gate 2 — production ratification | **Anthony** is the named human project authority and production ratifier |
| Capacity | **Confirmed** for the bounded five-signal / ten-frame WHY pilot |
| Review artefact form | One **consolidated five-signal review pack** containing **ten frame-level decisions**; separate detailed records only where risk, disagreement, or audit requirements justify them |
| Engineering rule | Engineering may implement or promote **only** decisions that have completed medical review **and** been **explicitly ratified by Anthony** |
| GPT alone | **Never** production authorisation |

### 2.1 Role table (post-ratification)

| Role | Recorded value | Evidence status |
|---|---|---|
| Primary medical-review owner | **GPT** — HealthIQ AI Head of Medical Research | **CLOSED** — human decision 2026-07-26 |
| Review role | Structured medical evidence review with APPROVE / REVISE / REJECT | **CLOSED** under dual-gate |
| Decision authority (medical review gate) | GPT as Head of Medical Research | **CLOSED** |
| Human ratification authority | **Anthony** — project authority and production ratifier | **CLOSED** — named 2026-07-26 |
| Engineering implementation owner | Cursor (`healthiq-core-engine`) — implements only **Anthony-ratified** assets | Established sprint role |
| Independent audit owner | Claude Code / Kernel–Gate evidence path | Established governance roles |

### 2.2 Operating model (ratified)

| Gate | Owner | Function |
|---|---|---|
| **1 — Medical review** | GPT (HealthIQ AI Head of Medical Research) | Structured evidence review; records frame dispositions in the consolidated pilot pack |
| **2 — Production ratification** | Anthony | Explicit human ratification required before any engineering implementation or promotion |

Precedent alignment: dual-gate keeps medical review and production authorisation as **separately gated** steps (same separation principle as `BATCH2-MEDREVIEW-1`, with GPT now named in the medical-review seat and Anthony named as ratifier).

---

## 3. Evidence-pack completeness (per frame)

Legend: AVAILABLE / MISSING / STALE / CONFLICTING / NOT_APPLICABLE

| activation_key (short) | inv YAML | source research | legacy WHY YAML | runtime output examples | activation-frame def | existing MR decisions | limitations/safety | tests/fixtures | provenance identity |
|---|---|---|---|---|---|---|---|---|---|
| vitamin_d_low_deficiency | AVAILABLE (`…_v1.yaml`) | AVAILABLE | AVAILABLE (on disk; dual-path risk) | AVAILABLE (compiled path tests) | AVAILABLE | AVAILABLE as architecture retirement case (not new content MR) | AVAILABLE (compiled mutual-exclusion rules) | AVAILABLE | AVAILABLE (compiled path) |
| hcy b_vitamin… | MISSING standalone | AVAILABLE (`Batch_6_Pass_3.json` + brief) | AVAILABLE (shared) | PARTIAL fixtures | AVAILABLE (package) | STALE/PARTIAL (MED-REV visibility ≠ compiled-WHY) | AVAILABLE in research/brief | AVAILABLE (family) | BLOCKED class (non-kb47) |
| hcy metabolic | AVAILABLE | AVAILABLE | AVAILABLE (shared) | PARTIAL | AVAILABLE | STALE/PARTIAL | AVAILABLE | AVAILABLE | SOURCE_DOCUMENT_DERIVED |
| hcy renal… | MISSING standalone | AVAILABLE (Batch_6 + brief) | AVAILABLE (shared) | PARTIAL | AVAILABLE | STALE/PARTIAL | AVAILABLE | AVAILABLE | BLOCKED class |
| mcv macrocytosis | AVAILABLE | AVAILABLE | AVAILABLE | AVAILABLE (clinician fixtures) | AVAILABLE | PARTIAL historical haematology notes | AVAILABLE | AVAILABLE | SOURCE_DOCUMENT_DERIVED |
| mcv megaloblastic… | MISSING standalone | AVAILABLE (Batch_6 + brief) | AVAILABLE | AVAILABLE | AVAILABLE | PARTIAL | AVAILABLE | AVAILABLE | BLOCKED class |
| mcv nonmegaloblastic… | MISSING standalone | AVAILABLE (Batch_6 + brief) | AVAILABLE | AVAILABLE | AVAILABLE | PARTIAL | AVAILABLE | AVAILABLE | BLOCKED class |
| free_t3 low_t3_syndrome | AVAILABLE (PKG2 extract) | AVAILABLE (`Batch_2_Pass_3.json`) | AVAILABLE | PARTIAL | AVAILABLE | AVAILABLE constraints (`thyroid_blood_marker_interpretation_clinical_signoff.md`; Batch_2 context review) — **not** compiled-WHY sign-off | AVAILABLE | AVAILABLE | **EXPLICIT_SPEC** post-PKG2 |
| tpo autoimmune_hypothyroid | MISSING standalone | AVAILABLE (`thyroid_antibodies_pass_3.json` + brief) | AVAILABLE | PARTIAL | AVAILABLE | PARTIAL thyroid activation MR history | AVAILABLE | AVAILABLE | SOURCE_DOCUMENT_DERIVED |
| tpo euthyroid_autoimmune_risk | MISSING standalone | AVAILABLE (pass_3 + brief; PSI absent) | AVAILABLE | PARTIAL | AVAILABLE | MISSING frame in `medical_frame_identity_index_v1.yaml` | AVAILABLE | AVAILABLE | SOURCE_DOCUMENT_DERIVED |

**Evidence-pack conclusion:** ownership/capacity are now confirmed. Structured medical review may proceed for frames whose pre-review prerequisites in §7.2 are met. Enumerated gaps remain engineering prerequisites (6 missing standalone inv YAMLs; missing `inv_tpo_ab_high_euthyroid_autoimmune_risk` index entry). Not complete enough to claim review already done.

---

## 4. Review workload

| Work class | Frames | Count |
|---|---|---:|
| RETIREMENT_CONFIRMATION_ONLY | vitamin_d_low | **1** |
| FULL_NEW_MEDICAL_REVIEW | hcy×3, mcv×3, free_t3×1, tpo×2 | **9** |
| LIGHT_REVIEW | — | **0** |
| RESEARCH_GAP | — | **0** (canonical research present in Batch JSON / inv / briefs; standalone inv extraction is engineering, not new medical invention) |
| BLOCKED | — | **0** at Gate 2.5 asset level |

**Signal-level totals (Gate 0 language):** 4 signals requiring new compiled-WHY medical review + 1 retirement confirmation.

**Review units:** 9 full frame reviews + 1 retirement confirmation within the bounded pilot. **Capacity for this bound is confirmed** (human decision 2026-07-26).

---

## 5. Review decision standard

Reusable per-frame fields live in:

`docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_DECISION_TEMPLATE.md`

**Ratified artefact form (2026-07-26):** medical review for this pilot is recorded as **one consolidated five-signal review pack** containing **ten frame-level decisions**. Separate detailed records are created only where risk, disagreement, or audit requirements justify them. The template supplies the required frame-level field set inside that pack.

Allowed frame decisions: APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

---

## 6. Capacity and programme viability

| Item | Status |
|---|---|
| Review owner confirmed | **YES** — GPT as HealthIQ AI Head of Medical Research |
| Human ratifier confirmed | **YES** — Anthony |
| Review inputs complete | **PARTIAL** — usable with enumerated pre-review prerequisites (§7.2) |
| Estimated review units | 9 full + 1 retirement (bounded pilot) |
| Blocking research gaps | **None** that require inventing medical interpretation |
| Programme-window fit | **CONFIRMED** for the bounded five-signal / ten-frame WHY pilot (human decision 2026-07-26) |
| Capacity conclusion | **READY** (ownership + capacity conditions closed) |

Safe reduction if later review/promotion blockers appear: reduce Package 3B to **vitamin_d_low legacy-retirement proof only** (Gate 0 fallback unchanged).

---

## 7. Gate 2.5 decision status

### 7.1 Initial decision (package completion): **CONDITIONAL_GO**

Architecture remained viable; pilot bounded at 5/10; Packages 1–2 gains stood.

### 7.2 Condition closure (human decisions 2026-07-26)

| # | Original condition | Status |
|---|---|---|
| 1 | Operating-model ratification | **CLOSED** — dual-gate approved |
| 2 | Named medical-review owner | **CLOSED** — GPT as HealthIQ AI Head of Medical Research |
| 3 | Named human production ratifier | **CLOSED** — Anthony |
| 4 | Capacity confirmation | **CLOSED** — confirmed for bounded 5-signal / 10-frame pilot |
| 5 | Evidence hygiene for Batch-JSON-only frames | **DECISION CLOSED / WORK OUTSTANDING** — must extract standalone inv YAMLs using the **byte-identical method established in ARCH-CONV-PKG2** (not optional acceptance of Batch JSON alone) |

**Additional pre-review / pre-promotion prerequisite (ratified 2026-07-26):**

| Prerequisite | Status |
|---|---|
| Add missing `inv_tpo_ab_high_euthyroid_autoimmune_risk` entry to `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` before that frame is reviewed or promoted | **WORK OUTSTANDING** (not executed in this documentation update) |

### 7.3 What is now authorised vs not

| Item | Status |
|---|---|
| Gate 2.5 ownership / ratification / capacity conditions | **CLOSED** |
| Package **3A** (non-medical WHY architecture machinery) | **MAY BEGIN** when separately started under Automation Bus — not started by this update |
| Package **3B** content promotion / compiled WHY activation | **NOT authorised** until medical review completes and Anthony explicitly ratifies |
| Any medical asset APPROVE / promote in this update | **No** |

### 7.4 Six frames requiring PKG2-style inv extraction (work outstanding)

| source_spec_id | Expected standalone path |
|---|---|
| inv_homocysteine_high_b_vitamin_related_methylation_impairment | `knowledge_bus/research/investigation_specs/inv_homocysteine_high_b_vitamin_related_methylation_impairment.yaml` |
| inv_homocysteine_high_renal_clearance_reduction | `knowledge_bus/research/investigation_specs/inv_homocysteine_high_renal_clearance_reduction.yaml` |
| inv_mcv_high_megaloblastic_macrocytosis | `knowledge_bus/research/investigation_specs/inv_mcv_high_megaloblastic_macrocytosis.yaml` |
| inv_mcv_high_nonmegaloblastic_macrocytosis | `knowledge_bus/research/investigation_specs/inv_mcv_high_nonmegaloblastic_macrocytosis.yaml` |
| inv_tpo_ab_high_autoimmune_hypothyroid_pattern | `knowledge_bus/research/investigation_specs/inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml` |
| inv_tpo_ab_high_euthyroid_autoimmune_risk | `knowledge_bus/research/investigation_specs/inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml` |

Method: byte-identical Pass-3 frame extraction as established in `ARCH-CONV-PKG2` (no invented `source_spec_id`; no medical reinterpretation).

---

## 8. Forbidden claims (this gate / this update)

- No medical asset APPROVE / promote
- No runtime / schema / package / hypothesis / prose / test / production-behaviour changes in this documentation update
- No beta-readiness or architecture-completion declaration
- No start of Package 3A inside this update
