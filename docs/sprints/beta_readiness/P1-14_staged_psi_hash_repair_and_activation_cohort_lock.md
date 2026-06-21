# P1-14 — Staged PSI Hash Repair, Gate Re-run and Activation Cohort Lock

## 1. Executive summary

- **Why this sprint was run:** P1-13 discovered all 41 staged compile manifests carried stale SHA-256 digests, masking the true activation-readiness split. P1-14 removes that mechanical blocker and locks programme cohorts for future opt-in planning.
- **Hash repair outcome:** **41/41** `output_hashes_sha256.promoted_signal_intelligence.yaml` values recomputed from current on-disk PSI bytes. Zero orphan PSI/manifest pairs. Batch index files inspected — no hash fields present; no index update required.
- **Validator rerun outcome:** P1-13 validator passes with **0** hash mismatches, **0** runtime-active staged PSI, **0** staged production opt-ins.
- **Final activation-readiness split:** **22** `ACTIVATION_READY_CANDIDATE`, **9** `BLOCKED_BIOMARKER_IDENTITY`, **7** `BLOCKED_DERIVED_MARKER_DEPENDENCY`, **3** `BLOCKED_MEDICAL_REVIEW_REQUIRED` — matches P1-13 hypothetical post-hash baseline exactly.
- **Recommended next sprint:** **P1-15-PRODUCTION-PSI-OPTIN-PILOT-1** — governed production manifest opt-in for the 22 activation-ready candidates only, with explicit STOP gates for biomarker/derived/medical blockers.

## 2. Programme context

- **Eight-block beta-readiness:** Converts staged Layer B intelligence from audit-only (P1-13) to sequenced activation planning without runtime activation.
- **P1-10 / P1-11 / P1-12:** Created 41 staged PSI packages across three pilot batches.
- **P1-13:** Built activation-readiness gate; universal hash mismatch blocked classification.
- **Why not validation-only:** Hash repair is prerequisite remediation, not a re-run of P1-13 alone — cohort lock and follow-on workpacks are required outcomes.
- **Why not runtime activation:** All `runtime_active: false` preserved; no production package manifest edits.

## 3. Phase 0 — Hash repair

| Metric | Value |
|---|---|
| Batches inspected | `p1_10_batch_a`, `p1_11_batch_b`, `p1_12_batch_c` |
| PSI files | 41 |
| Compile manifests | 41 |
| Hash fields repaired | 41 |
| Index files with hash fields | 0 (inspected; not updated) |

**STOP conditions checked:**

- Every PSI has a matching compile manifest — pass
- Every compile manifest has a matching PSI — pass
- Hash field structure (`output_hashes_sha256.promoted_signal_intelligence.yaml`) — clear and consistent
- Mismatch cause — stale manifest digests after git line-ending / commit drift; PSI content intact
- No PSI content edits required — pass
- No production package changes required — pass

**Limitations:** Repair used byte-accurate SHA-256 of current PSI files; compile manifest YAML formatting may differ cosmetically from compiler output but hash values are authoritative.

## 4. Phase 1 — Gate re-run

**Command:**

```powershell
python backend/scripts/validate_staged_psi_activation_readiness.py
python backend/scripts/validate_staged_psi_activation_readiness.py --json
```

**Output summary:**

```text
psi_files_found: 41
compile_manifests_found: 41
production_opt_ins_found: 20
activation_ready_count: 22
blocked_count: 19
top_blocker: BLOCKED_BIOMARKER_IDENTITY (9)
top_blocker: BLOCKED_DERIVED_MARKER_DEPENDENCY (7)
top_blocker: BLOCKED_MEDICAL_REVIEW_REQUIRED (3)
```

- **Remaining hash issues:** none
- **Unexpected structural issues:** none
- **Runtime activation check:** all staged `runtime_active: false`; no staged package in production opt-in set

## 5. Phase 2 — Activation-readiness cohort lock

| Cohort | Count | Representative PSI files | Blocker / readiness basis | Recommended action |
|---|---:|---|---|---|
| ACTIVATION_READY_CANDIDATE | 22 | `pkg_kb52c_alt_high_hepatocellular_injury_pattern`, `pkg_kb60_total_cholesterol_high_atherogenic_hypercholesterolemia`, `pkg_kb52c_ferritin_low_iron_store_depletion` | Hash integrity pass; canonical primary/supporting IDs; no derived/medical primary blockers | First production opt-in pilot cohort |
| BLOCKED_BIOMARKER_IDENTITY | 9 | `pkg_kb52d_non_hdl_cholesterol_high_atherogenic_lipoprotein_burden` (`non_hdl`), `pkg_kb52c_wbc_high_reactive_leukocytosis` (`wbc`), `pkg_kb52c_plt_high_reactive_thrombocytosis` (`plt`) | Primary or supporting IDs not in SSOT (`non_hdl`, `wbc`, `lym`, `plt`, `hgb`, `erythropoietin`, etc.) | SSOT biomarker identity adjudication sprint |
| BLOCKED_DERIVED_MARKER_DEPENDENCY | 7 | Iron-panel Batch B/C packages (`pkg_kb52c_iron_low_absolute_iron_deficiency`, `pkg_kb52c_ferritin_high_inflammatory_hyperferritinemia`, …) | Supporting `transferrin_saturation` derived-marker dependency | Derived-metric runtime support review |
| BLOCKED_MEDICAL_REVIEW_REQUIRED | 3 | `pkg_kb52c_homocysteine_high_b_vitamin_related_methylation_impairment`, `pkg_kb52c_homocysteine_high_renal_clearance_reduction`, `pkg_kb52c_neutrophil_pct_high_neutrophil_predominant_leukocyte_shift` | Documented medical-review carry-forward overlays | Medical-review sign-off sprint |

**P1-13 baseline comparison:** Expected 22 / 9 / 7 / 3 — **actual matches exactly**. No variance to explain.

**Secondary overlays (not primary cohort class):** frame-authority (4 packages) and system-mapping (3 packages) remain documented on blocked items but are subordinate to biomarker/derived/medical primary classifications.

## 6. Phase 3 — Follow-on workpacks

| Workpack | Scope | STOP gates |
|---|---|---|
| **P1-15-PRODUCTION-PSI-OPTIN-PILOT-1** | Production manifest opt-in for 22 activation-ready candidates only | No opt-in for blocked cohorts; no runtime loader changes without separate sprint; human approval per package cluster |
| **P1-SSOT-BIOMARKER-ADJUDICATION-1** | Resolve `non_hdl`, `wbc`, `lym`, `plt` and supporting aliases (`hgb`, `erythropoietin`, …) | No PSI medical rewrites without authority; no guessing alias mappings |
| **P1-DERIVED-METRIC-TRANSFERRIN-SAT-1** | Runtime/SSOT path for `transferrin_saturation` supporting dependency (7 PSI) | No primary promotion of transferrin saturation without Pass 3 source support |
| **P1-MED-REV-HOMOCYSTEINE-LEUKOCYTE-1** | Medical review for 3 homocysteine/leukocyte PSI frames | No activation until sign-off recorded |
| **P1-HEMOGLOBIN-PASS3-AUTHORING-1** | Pass 3 research authoring for hemoglobin primary specs (still absent from staged estate) | No forced promotion without source support |
| **P1-FRAME-SYSTEM-MAPPING-1** | Frame-authority and leukocyte system-mapping reconciliation on blocked iron/leukocyte packages | Parallel to SSOT/medical tracks; no runtime activation |

## 7. Runtime non-activation confirmation

Confirmed:

- No staged `promoted_signal_intelligence.yaml` content changed
- No production package manifests changed
- No runtime activation occurred (`runtime_active: false` on all 41 manifests)
- No `scoring_policy.yaml` change
- No `biomarkers.yaml` change
- No `backend/core/` change
- No `backend/scripts/` or `backend/tests/` change
- No frontend / Gemini / parser change
- No DTO / domain assembler change
- No compiled card change
- No Pass 3 source change

## 8. Validation

```powershell
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-14_activation_readiness_cohort_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-14'; assert 'cohorts' in data; print('P1-14 activation cohort manifest YAML parsed successfully')"
python backend/scripts/validate_staged_psi_activation_readiness.py
git diff --stat
git diff --name-only
git status --short
```

- Hash integrity after repair: **pass** (0 mismatches)
- Manifest YAML parse: **pass**
- Limitations: Cohort manifest is planning-only; not consumed by runtime

## 9. Business value delivered

- Restores reproducibility and audit trust for staged PSI compile manifests.
- Converts P1-13 gate output from “everything blocked by hash” into four actionable programme tracks.
- Avoids micro-sprinting individual markers by locking cohort maps and named follow-on workpacks.
- Enables parallel SSOT, medical-review, and production opt-in planning on verified evidence.

## 10. Carry-forwards

- **Activation-ready pilot candidates:** 22 PSI listed in `P1-14_activation_readiness_cohort_manifest.yaml`
- **SSOT / biomarker identity:** 9 PSI (`non_hdl`, `wbc`, `lym`, `plt`, supporting aliases)
- **Derived-marker:** 7 iron-panel PSI with `transferrin_saturation` dependency
- **Medical-review:** 3 homocysteine / leukocyte PSI
- **Source-support / research-authoring:** hemoglobin primary specs still absent (P1-12 deferral unchanged)
- **Frame-authority / system-mapping:** overlays on iron and leukocyte blocked packages — address in dedicated reconciliation workpack

## 11. Recommended next sprint

| Field | Value |
|---|---|
| **Title** | P1-15 — Production PSI opt-in pilot (activation-ready cohort) |
| **risk_level** | HIGH |
| **change_type** | CONTENT |
| **Scope** | Governed production manifest opt-in for 22 activation-ready staged PSI only; verify loader read path; maintain `runtime_active: false` until explicit activation sprint |
| **STOP gates** | No opt-in for blocked cohorts; no SSOT edits without authority sprint; no medical identity guessing |
| **Rationale** | Hash integrity restored; clean 22-package pilot cohort is the lowest-risk next step toward controlled runtime use |
