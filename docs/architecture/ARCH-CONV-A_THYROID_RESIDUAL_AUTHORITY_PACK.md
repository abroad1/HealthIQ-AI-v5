# ARCH-CONV-A — Thyroid Residual Authority Pack

**Work ID:** `ARCH-CONV-A-THYROID-RESIDUAL-DISPOSITION-1`  
**Date (UTC):** 2026-08-08  
**Change type:** CONTENT  
**Risk:** HIGH  
**Companion register:** `docs/architecture/ARCH-CONV-A_THYROID_RESIDUAL_DISPOSITION_REGISTER.yaml`

This pack is a bounded **authority/disposition** artefact only. It does not implement runtime behaviour, activate or deactivate packages, compile WHY artefacts, author medical research, change intervention runtime, or change consumer wording.

---

## Stage 1A — Authority preflight

### Path substitution

| Prompt-cited path | Current authoritative path |
|---|---|
| `docs/architecture/ARCH-CONV-A_RESIDUAL_PROGRAMME_REPOSITORY_REALITY_RECONCILIATION.md` | `docs/audit-papers/ARCH-CONV-A_RESIDUAL_PROGRAMME_REPOSITORY_REALITY_RECONCILIATION.md` |

Hardening and independent inspection confirm the audit-papers path is the live document.

### Authority surfaces inspected

| Surface | Current authority used |
|---|---|
| Repository-reality reconciliation | `docs/audit-papers/ARCH-CONV-A_RESIDUAL_PROGRAMME_REPOSITORY_REALITY_RECONCILIATION.md` |
| Wave 1 Gate1/Gate2 thyroid decision | `docs/architecture/ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md` |
| Wave 1 medical decision register | `docs/architecture/ARCH-CONV-A_wave1_medical_decision_register.yaml` |
| MR-v2 activation ADR | `docs/architecture/ADR-THYROID-MR-V2-ACTIVATION-1.md` |
| Compiled WHY register | `knowledge_bus/governance/compiled_why_authority_register_v1.yaml` |
| Runtime activation register | `knowledge_bus/governance/package_runtime_activation_register_v1.yaml` |
| Medical frame identity index | `knowledge_bus/governance/medical_frame_identity_index_v1.yaml` |
| Domain-card thyroid allow/exclude | `backend/core/analytics/domain_score_assembler.py` |
| Intervention library | `knowledge_bus/interventions/intervention_library_v1.yaml` |
| THY-U5 source | `docs/discussion documents/HEALTHIQ_THYROID_ENDOCRINE_PRIORITISATION_RULESET_v0_1.md` |
| Empiric runtime load | fresh `SignalRegistry().get_all_signals()` on this branch |

No later document was found that **explicitly supersedes** ADR Decision 4 (“Keep deferred: TPOAb euthyroid … TgAb packages”) or Wave 1’s “No compilation or activation of `signal_tgab_high` / `signal_thyroid_tsh_context`.” PKG3 compiled the TPO euthyroid WHY artefact; that compile does **not** by itself clear the medical-activation deferral conflict (see STOP 1).

### Programme continuity register

No separate Stage-0 / programme-continuity register format requiring a disposition entry for this sprint was found. Continuity is carried by this pack + YAML register only. No continuity-register edit performed.

---

## Stage 1B — Reality / no-op check

Residuals remain unresolved. This is **not** `NO_OP_OR_REBASE_REQUIRED`.

Stale reconciliation claims corrected by this pass:

1. Reconciliation said TPOAb euthyroid was “Not compiled.” **False today** — compiled artefact and `COMPILED_ACTIVE` register row exist.
2. Reconciliation treated TgAb mainly as “promotion not research.” **Incomplete today** — medical deferral / Wave 1 non-authorisation still conflict with activation-register reachability (STOP 1).
3. TPOAb confirmatory gap is **two** gaps, not one wiring gap.

---

## Stage 1C — Intelligence preflight

No authorised changes to signal firing, thresholds, activation register, compiled WHY, packages, prioritisation, clinical concern construction, frontend, consumer narrative, or intervention runtime. Deliverables are authority documents only.

---

## STOP 1 determination (mandatory)

### Verdict

**STOP 1 is TRIGGERED.**

Prompt STOP condition 1: *current authority conflicts on whether a thyroid residual is active, deferred, rejected, or superseded.*

Cursor **does not** select `PROMOTE_COMPILE` or `REMAIN_DEFERRED` (or any other product disposition) for the conflicted frames. Fixing the drift would be an out-of-scope runtime/governance change.

### Conflicted frames

| Activation key | Medical / Gate authority | Runtime / compile authority |
|---|---|---|
| `signal_tgab_high::inv_tgab_high_autoimmune_hypothyroid_pattern` | ADR Decision 4 keep deferred; Wave 1 “no compilation or activation” | Listed in `package_runtime_activation_register_v1.yaml:350-351`; `SignalRegistry` load shows `production_reachable` |
| `signal_tgab_high::inv_tgab_high_euthyroid_autoimmune_risk` | Same | Register `:352-353`; `production_reachable` |
| `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` | ADR Decision 4 keep deferred; identity index `promotion_state: deferred`, `runtime_authority_status: inactive` | Register `:360-361`; compiled WHY `COMPILED_ACTIVE` (`compiled_why_authority_register_v1.yaml:135-145`); `production_reachable`; parent `signal_tpo_ab_high` is on thyroid domain-card launch allowlist |

### Provenance note (not a disposition)

Register membership for these keys traces to commit `a260c53` (ARCH-CONV-E baseline activation snapshot), i.e. mechanical bootstrap rather than a later thyroid-specific re-ratification of ADR Decision 4. This matches the failure class previously seen for lipid rejected-but-loaded frames, but sits below `runtime_medical_authority_integrity_v1`’s explicit-prohibition token floor (“Keep deferred” is not `REJECTED` / `DO_NOT_ACTIVATE`).

### Layer conflict inside TPO euthyroid alone

- Identity index notes still describe the frame as deferred / not Anthony-ratified for promotion.
- PKG3 compile manifest states Gate C Anthony-ratified **compiled WHY**.
- ADR still says keep deferred for **activation**.

Compile ≠ activation ≠ domain-card emission. This pack records the conflict; it does not collapse the layers.

---

## Residual identity / source map

### 1–2. `signal_tgab_high` (two medical frames)

| Field | Hypothyroid pattern | Euthyroid autoimmune risk |
|---|---|---|
| Signal ID | `signal_tgab_high` | `signal_tgab_high` |
| Frame / source_spec_id | `inv_tgab_high_autoimmune_hypothyroid_pattern` | `inv_tgab_high_euthyroid_autoimmune_risk` |
| Package | `pkg_kb59_tgab_high_autoimmune_hypothyroid_pattern` | `pkg_kb59_tgab_high_euthyroid_autoimmune_risk` |
| Source research | `thyroid_antibodies_pass_3.json` (specs embedded; no split `inv_tgab_*.yaml` on disk) | Same Pass 3 JSON |
| Compiled WHY | Absent from compiled estate / authority register | Absent |
| Runtime activation register | Present | Present |
| Empiric load | Present, `production_reachable`, `has_validated_canonical_inv_spec=false` | Same |
| Domain-card allowlist | **Not** in `_THYROID_LAUNCH_SIGNAL_IDS` | Same |
| Prior medical decision | Deferred / non-authorised | Deferred / non-authorised |
| Proposed disposition | **Blocked — STOP 1** | **Blocked — STOP 1** |

Pass 3 / package content exists and is mappable 1:1 to the two activation keys. That is **not** permission to promote while STOP 1 is open. Fresh literature research is **not** required to explain the residual; governed medical **review of existing** Pass 3 content would be needed only after authority reconciliation authorises a promotion path.

### 3. `signal_tpo_ab_high` euthyroid variant

| Field | Value |
|---|---|
| Activation key | `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk` |
| Research | `inv_tpo_ab_high_euthyroid_autoimmune_risk.yaml` present |
| Compiled WHY | Present; register `COMPILED_ACTIVE` |
| Identity index | `deferred` / `inactive` |
| ADR | Keep deferred |
| Runtime | `production_reachable`; on `signal_tpo_ab_high` launch allowlist |
| Proposed disposition | **Blocked — STOP 1** |

Product scope has not been re-ratified in this sprint to force reactivation merely because research and a compiled artefact exist.

### 4. `signal_tpo_ab_high` hypothyroid confirmatory-test gaps (two rows)

Upstream investigation spec contains:

- `ct_repeat_thyroid_function_panel`
- `ct_thyroid_ultrasound`

(`inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml:83-87`)

Compiled artefact feeding runtime WHY has `confirmatory_tests: []` on both hypotheses (`inv_tpo_ab_high_autoimmune_hypothyroid_pattern.yaml:22,43`).

Intervention library has **zero** thyroid / TPO / antibody / confirmatory matches.

| Gap | Classification | Disposition | Next work class |
|---|---|---|---|
| Spec → compiled `confirmatory_tests` emptied | Clinical-intelligence **compilation completeness** gap | `SEPARATE_PRESENTATION_OR_INTERVENTION_WORK` (not a new research gap; not closed) | `PROMOTION_COMPILATION` |
| Compiled/spec content → intervention/next-step surface | **Presentation / intervention wiring** gap | `SEPARATE_PRESENTATION_OR_INTERVENTION_WORK` | `INTERVENTION_PRESENTATION` |

Do not smuggle either gap into TgAb promotion work.

### 5. TRAb / TSI

Independent search across SSOT biomarkers/aliases, packages, investigation specs, and compiled estate found **no** governed TRAb / TSI / TSH-receptor-antibody identity.

**Disposition:** `RESEARCH_REQUIRED`

Narrow research question for Medical Research lane (author nothing here):

> If product scope requires Graves'-specific confirmatory-marker guidance beyond biochemical thyrotoxicosis pattern already ratified, define governed biomarker identity, synonyms, and non-diagnostic follow-up-testing framing for TSH-receptor antibody (TRAb/TSI). Do not invent thresholds or disease claims in a disposition sprint.

### 6. `signal_thyroid_tsh_context`

Exclusion authority is **still closed** for consumer domain-card presentation:

- ADR Decision 3: keep excluded
- Wave 1: no compilation or activation
- `domain_score_assembler.py` `_THYROID_EXCLUDED_SIGNAL_IDS` still contains `signal_thyroid_tsh_context`

Precise runtime fact (not a reopening): the key remains listed in the activation register and loads as `production_reachable`. That two-layer split is longstanding bootstrap behaviour, not evidence that later authority reopened consumer presentation.

**Disposition:** `RETIRE_OR_SUBSUME` — **no further ARCH-CONV-A work** on this residual.

No architectural-review STOP for reopening was triggered.

### 7. THY-U5 — clinical follow-up vs disease naming

These are **different** decisions:

1. **Clinical follow-up capability** — whether HealthIQ may recommend discussing further testing / confirmatory evaluation in non-diagnostic language.
2. **Consumer disease naming** — whether HealthIQ may name or imply Hashimoto's disease, Graves' disease, or equivalent cause labels.

Existing ratified authority already constrains (2):

- Wave 1 global rule: no diagnosis of hypothyroidism, hyperthyroidism, Graves', Hashimoto's, or pituitary disease (`ARCH-CONV-A_wave1_thyroid_gate1_gate2_decision.md:38`).
- FT3-high boundary: do not imply Graves' or any other specific cause (`:113`).
- ADR non-negotiable: no Hashimoto's / autoimmune thyroid disease / hypothyroidism diagnosis from TPOAb alone (`ADR-THYROID-MR-V2-ACTIVATION-1.md:57`).

THY-U5 (`HEALTHIQ_THYROID_ENDOCRINE_PRIORITISATION_RULESET_v0_1.md:302`) remains an open **Blocking — communication** question and is **not** closed by the Wave 1 non-diagnosis rules alone if product later wants affirmative naming permission.

**Disposition:** `SEPARATE_PRESENTATION_OR_INTERVENTION_WORK`  
**Marker:** `ANTHONY_RATIFICATION_REQUIRED`  
**Next work class:** `GOVERNANCE_ONLY`  
No runtime wording changes in this sprint.

Recommended communication posture pending ratification (not implemented): preserve ratified non-diagnosis / non-implication bounds; treat clinical follow-up capability as a separate intervention/presentation track; do not treat THY-U5 as a research or compiled-WHY task.

---

## Required decision output

### A. Closed thyroid items

| Item | Disposition |
|---|---|
| `signal_thyroid_tsh_context` consumer-domain exclusion | `RETIRE_OR_SUBSUME` — no further ARCH-CONV-A work |
| Already ratified TSH / FT3 / FT4 Wave 1 frames | Out of scope; not reopened |
| TPOAb hypothyroid medical activation (ADR Decision 2) | Remains active; not a residual activation question |

### B. Promotion-ready thyroid items

**None asserted in this sprint.**

TgAb and TPOAb euthyroid would be the natural promotion candidates **only after** STOP 1 authority reconciliation. Asserting `PROMOTE_COMPILE` now would pick the runtime/compile side of the conflict.

### C. Research-required thyroid items

| Item | Disposition |
|---|---|
| TRAb / TSI (TSH-receptor antibody) | `RESEARCH_REQUIRED` — genuine absence |

### D. Separate product / presentation items

| Item | Disposition |
|---|---|
| TPOAb hypothyroid confirmatory_tests compile-emptying | Compilation completeness; separate from intervention wiring |
| TPOAb hypothyroid → intervention library wiring | Presentation/intervention track |
| THY-U5 disease naming | Governance/communication; `ANTHONY_RATIFICATION_REQUIRED` |

### E. Ratification questions (Anthony)

1. **STOP 1 / deferred-but-reachable thyroid antibodies:** Should medical ADR/Wave 1 deferral be enforced by removing or withholding TgAb + TPOAb euthyroid from production reachability, or has a later (currently undocumented) activation decision superseded ADR Decision 4?
2. **THY-U5:** May consumer output ever name Hashimoto's or Graves', or must product remain permanently within non-diagnosis / non-implication bounds already ratified?

### F. Recommended next implementation package (exactly one)

**Proposed work ID:** `THYROID-DEFERRED-RUNTIME-AUTHORITY-INTEGRITY-1`  
**Class:** `GOVERNANCE_ONLY` (runtime register / loader alignment with ratified medical deferral — or explicit re-ratification if deferral is intentionally lifted)

**In scope (recommended):** reconcile activation-register / SignalRegistry reachability for:

- `signal_tgab_high::*`
- `signal_tpo_ab_high::inv_tpo_ab_high_euthyroid_autoimmune_risk`

against ADR Decision 4 + Wave 1 non-authorisations + identity-index deferred status; add integrity coverage if “Keep deferred” must become machine-enforceable.

**Out of scope for that next package:** TgAb WHY compilation, TRAb/TSI research authorship, intervention-library wiring, consumer disease-naming copy, reopening TSH/FT3/FT4 logic.

---

## Explicit non-scope confirmation

This sprint did **not**:

- compile TgAb or any thyroid WHY
- activate/deactivate signals
- edit activation or compiled-WHY registers
- edit package signal logic or thresholds
- add TRAb/TSI to SSOT
- conduct new literature research
- change intervention runtime or frontend copy
- reopen ratified TSH/FT3/FT4 logic or the FT3/TSH firing fix
- alter cross-domain prioritisation
- fold iron/haematology or other ARCH-CONV-A domains into this pack

---

## Success criteria status

| Criterion | Status |
|---|---|
| Residuals re-verified against current main | Met |
| No obsolete Wave-1 assumption carried unexamined | Met (reconciliation staleness corrected) |
| TgAb explicit governed disposition | **Blocked by STOP 1** — conflict documented; no side chosen |
| TPOAb euthyroid explicit governed disposition | **Blocked by STOP 1** — conflict documented; no side chosen |
| TPOAb confirmatory gap classified | Met — two distinct gaps |
| TRAb/TSI confirmed gap or existing authority | Met — `RESEARCH_REQUIRED` |
| `signal_thyroid_tsh_context` closed or escalated | Met — closed for ARCH-CONV-A |
| Follow-up capability separated from disease naming | Met |
| THY-U5 resolved or precise Anthony question | Met — `ANTHONY_RATIFICATION_REQUIRED` |
| No runtime behaviour changes | Met |
| Exactly one next package recommended | Met |

---

## Escalation banner

```text
STOP_1_TRIGGERED — ARCH-CONV-A-THYROID-RESIDUAL-DISPOSITION-1
Deferred medical authority conflicts with runtime activation reachability for
signal_tgab_high (both frames) and signal_tpo_ab_high euthyroid frame.
Cursor did not select PROMOTE_COMPILE or REMAIN_DEFERRED.
GPT architectural review + Anthony approval required before those dispositions
or any runtime remediation.
```
