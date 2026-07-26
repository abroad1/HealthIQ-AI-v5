# HealthIQ AI v5 — WHY Pilot Medical Review Readiness (Gate 2.5)

**Work ID:** `ARCH-CONV-GATE2_5`  
**Branch:** `feature/arch-conv-gate2-5-medical-review-readiness`  
**Baseline HEAD (kernel start):** `9ce7853beaea2ba40eb3ed076483ab9ecedaea86`  
**change_type:** CONTENT  
**runtime_change:** NONE  
**Gate 2.5 decision:** **CONDITIONAL_GO**

This document does **not** approve or promote any medical asset, does **not** authorise Package 3B, and does **not** declare beta readiness.

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

| Role | Recorded value | Evidence status |
|---|---|---|
| Primary medical-review owner | **UNCONFIRMED** — prompt proposes `GPT Head of Medical Research` | String **does not exist** anywhere in current governance (`CLAUDE.md`, `AGENTS.md`, prior ADRs). Novel role expansion. |
| Review role (proposed by prompt) | Structured medical evidence review with APPROVE / REVISE / REJECT | Proposed in Gate 2.5 prompt only — **not previously ratified** |
| Decision authority | **UNCLEAR** until operating-model choice is ratified (see §2.1) | STOP condition 5 relevant |
| Human ratification authority | **Role exists** as Human final authority in Automation Bus / `CLAUDE.md`; **named person ABSENT** in repository | Do not invent a name |
| Engineering implementation owner | Cursor (`healthiq-core-engine`) — implements only **ratified** assets | Established sprint role |
| Independent audit owner | Claude Code / Kernel–Gate evidence path | Established governance roles |

### 2.1 Operating-model policy question (must be ratified separately)

Two distinct models are available. Gate 2.5 **does not** silently adopt either.

| Model | Description | Precedent |
|---|---|---|
| **(A) Dual-gate (existing pattern)** | Governance/agent performs coherence/completeness review; a **separately named clinical reviewer** performs genuine medical sign-off before compiled-hypothesis promotion | `BATCH2-MEDREVIEW-1` — “PASS (governance medical review only)”; zero frames cleared; defers to separate clinical sign-off |
| **(B) Prompt-proposed compressed model** | GPT conducts substantive medical evidence review and records APPROVE/REVISE/REJECT; human only ratifies that process was followed | **No prior ratification** in governance stack |

**Human project authority must explicitly choose (A) or (B) before Package 3B.** Choosing (B) is a new policy decision, not a background fact.

**Do not treat GPT review alone as production authorisation** under either model.

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

**Evidence-pack conclusion:** complete enough to **start** structured review for all 10 frames **if** ownership/capacity are confirmed, with enumerated gaps (6 missing standalone inv YAMLs recoverable from Batch JSON; shared legacy YAML; no compiled-WHY sign-off artefacts yet). Not complete enough to claim review already done.

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

**Estimated review units (descriptive only — not a capacity commitment):** 9 full frame reviews + 1 retirement confirmation. No FTE, calendar, or availability invented.

---

## 5. Review decision standard

Reusable template created at:

`docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_MEDICAL_REVIEW_DECISION_TEMPLATE.md`

Allowed frame decisions (template): APPROVE_FOR_COMPILED_PROMOTION / APPROVE_WITH_REVISIONS / REJECT / DEFER_PENDING_RESEARCH / RETIREMENT_CONFIRMATION_ONLY.

---

## 6. Capacity and programme viability

| Item | Status |
|---|---|
| Review owner confirmed | **NO** — role unconfirmed; GPT Head of Medical Research not ratified |
| Human ratifier confirmed | **NO** — named human medical ratifier absent (do not invent) |
| Review inputs complete | **PARTIAL** — usable with enumerated gaps (§3) |
| Estimated review units | 9 full + 1 retirement (descriptive) |
| Blocking research gaps | **None** that require inventing medical interpretation; extraction of missing inv YAMLs is optional engineering hygiene before Package 3B |
| Programme-window fit | **UNVERIFIABLE** without human capacity confirmation (Gate 0 unchanged) |
| Capacity conclusion | **NOT_READY** |

Safe reduction if Gate 2.5 conditions remain unmet (from Gate 0): reduce Package 3B to **vitamin_d_low legacy-retirement proof only**.

---

## 7. Gate 2.5 decision

### **CONDITIONAL_GO**

Architecture remains viable; pilot remains bounded at 5/10; Packages 1–2 gains stand. Package 3A machinery may proceed only for **non-medical** architecture work once human-authorised. **Package 3B content promotion must not begin** until every condition below is closed.

### Explicit conditions

1. **Operating-model ratification:** Human project authority chooses Model **(A)** or **(B)** in §2.1 and records that choice in a governed artefact.
2. **Named medical-review owner:** Confirm the primary reviewer identity (role and accountable agent/person) consistent with the chosen model.
3. **Named human production-ratification authority:** Confirm the human who must ratify production promotion of compiled WHY assets (distinct from GPT/agent review).
4. **Capacity confirmation:** Confirm that 9 full frame reviews + 1 retirement confirmation fit the ratified programme ceiling — without inventing dates; a written commitment is required.
5. **Evidence hygiene (recommended before Package 3B, not a Package 3 redesign):** Extract or attach standalone inv YAMLs for the 6 Batch-JSON-only pilot frames **or** explicitly accept Batch JSON as the canonical investigation source for those frames in the review pack.

### Why not GO / STOP / V6

| Alternative | Why not |
|---|---|
| GO | Owner, ratifier, and capacity are not evidenced; operating-model authority unclear |
| STOP | Architecture salvage remains credible; conditions are enumerable and do not require Package 3 redesign |
| V6 | No ratified kill criterion is met by these findings |

---

## 8. Forbidden claims (this gate)

- No medical asset APPROVE / promote
- No runtime / schema / package / hypothesis / prose / test changes
- No beta-readiness or architecture-completion declaration
- No invented reviewer availability, commitment, or dates
