# P1-13 — Staged PSI Activation-Readiness Gate and Integrity Validator

## 1. Executive summary

- **Why this sprint was run:** P1-10, P1-11 and P1-12 established a staged promoted-signal-intelligence (PSI) estate under `knowledge_bus/generated_pilot/` with compile manifests and `runtime_active: false`. Programme risk shifted from “can we promote?” to “what blocks future production opt-in?” P1-13 creates that governed gate.
- **Staged PSI estate audited:** 41 PSI files and 41 compile manifests across `p1_10_batch_a` (18), `p1_11_batch_b` (16) and `p1_12_batch_c` (7).
- **Validator/tooling added:** `backend/scripts/validate_staged_psi_activation_readiness.py` — report-only audit wrapping existing PSI structural validation, SSOT biomarker key checks, derived-marker dependency detection, compile-manifest integrity checks, production opt-in scan, and documented carry-forward overlays from P1-10/11/12 batch manifests.
- **Activation-readiness finding:** **0** artefacts classified `ACTIVATION_READY`; **41** blocked. Primary classification is `BLOCKED_MANIFEST_OR_HASH` for all 41 items because compile-manifest SHA-256 digests do not match current on-disk PSI bytes (line-ending / recompile drift after git commits). This sprint does not repair hashes — it reports them.
- **Top blockers (presence in blocker lists, not exclusive):** compile manifest hash mismatch (41); documented medical-review carry-forward (9); supporting non-canonical biomarker IDs (9); derived-marker dependency `transferrin_saturation` (7); primary non-canonical biomarker IDs (5); frame-authority carry-forward (4); system-mapping carry-forward (3).
- **Recommended next sprint:** **P1-14-MANIFEST-INTEGRITY-1** — recompile staged compile manifests without changing PSI medical content, then re-run this gate; parallel **P1-SSOT-BIOMARKER-ADJUDICATION-1** for `wbc`, `lym`, `plt`, `non_hdl` identity decisions.

## 2. Programme context

- **Eight-block beta-readiness:** P1-13 serves Block 6 (medical safety / governance), Block 7 (auditability / traceability) and Block 3 (Layer B intelligence substrate readiness) by separating staged promotion from runtime activation.
- **P1-10:** Established Batch A staged PSI factory pattern (18 PSI).
- **P1-11:** Batch B CBC/iron/oxygen promotion (16 PSI) with explicit deferrals.
- **P1-12:** Batch C deferred cohort re-adjudication (7 PSI promoted; hemoglobin and high-risk frames remain deferred at source level).
- **Why not a micro-sprint:** Activation readiness is estate-wide; partial fixes would hide cross-batch blockers and violate the promotion-not-activation boundary.
- **Why not runtime activation:** No production manifest opt-in, no loader changes, no scoring-policy or SSOT edits, no compiled-card activation.

## 3. Staged PSI estate inventory

| Batch | Path | PSI count |
|---|---|---|
| Batch A | `knowledge_bus/generated_pilot/p1_10_batch_a/` | 18 |
| Batch B | `knowledge_bus/generated_pilot/p1_11_batch_b/` | 16 |
| Batch C | `knowledge_bus/generated_pilot/p1_12_batch_c/` | 7 |
| **Total** | | **41** |

- **Compile manifests found:** 41 (one per PSI package directory).
- **Production package opt-ins scanned:** 20 packages under `knowledge_bus/packages/` have `promoted_signal_intelligence` opt-in; **none** match staged pilot package IDs — staged PSI remains non-runtime.
- **Limitations:** Validator reads SSOT and schema only; it does not adjudicate alias mappings (`lym`, `wbc`, `plt`). Carry-forward overlays are documentary flags from prior sprint manifests, not new medical decisions.

## 4. Integrity validator implementation

- **Script:** `backend/scripts/validate_staged_psi_activation_readiness.py` (new).
- **Checks performed:**
  - PSI YAML readability and forbidden root fields
  - Primary and supporting `biomarker_id` presence in SSOT keys (read-only)
  - Derived-marker dependency flag for `transferrin_saturation`
  - `signal_system` and `trigger_direction` against schema vocabulary
  - Existing `validate_promoted_signal_intelligence` structural validation (wrapped)
  - Compile manifest presence, `runtime_active: false`, `source_spec_id`, output hash consistency
  - Production manifest opt-in absence
  - Documented medical-review / frame-authority / system-mapping carry-forwards from P1-10/11/12
- **Files changed:** validator script, unit tests, P1-13 docs/manifest, build register append, automation bus status.
- **Report-only rationale:** Staged PSI and compile manifests are immutable for this sprint; corrections are carry-forwards for future authority sprints.
- **Intentionally not decided:** `lym = lymphocytes_abs`, `wbc = white_blood_cells`, creation of `transferrin_saturation` in SSOT, leukocyte subsystem mapping resolution.

## 5. Activation-readiness matrix summary

| Classification (primary) | Count |
|---|---|
| ACTIVATION_READY | 0 |
| BLOCKED_MANIFEST_OR_HASH | 41 |

**Blocker presence counts** (items may carry multiple blockers; hash mismatch dominates primary classification):

| Blocker type | Items affected |
|---|---|
| Compile manifest hash mismatch | 41 |
| Documented medical-review carry-forward | 9 |
| Supporting non-canonical biomarker ID | 9 |
| Derived-marker dependency | 7 |
| Primary non-canonical biomarker ID | 5 |
| Documented frame-authority carry-forward | 4 |
| Documented system-mapping carry-forward | 3 |

**Hypothetical classification if hash integrity were resolved** (planning aid only — not executed):

| Classification | Count |
|---|---|
| ACTIVATION_READY | 22 |
| BLOCKED_BIOMARKER_IDENTITY | 9 |
| BLOCKED_DERIVED_MARKER_DEPENDENCY | 7 |
| BLOCKED_MEDICAL_REVIEW_REQUIRED | 3 |

## 6. Detailed blocker findings

### Compile manifest hash mismatch (41 items — manifest / reproducibility)

- **Affected:** All 41 staged PSI packages across three batches.
- **Reason:** `output_hashes_sha256.promoted_signal_intelligence.yaml` in compile manifests does not match SHA-256 of current PSI file bytes on disk.
- **Category:** Manifest / reproducibility (likely CRLF or post-commit byte drift).
- **Resolution path:** Dedicated manifest recompile sprint that updates hashes only — no PSI medical content edits.

### Primary non-canonical biomarker IDs (5 items — SSOT)

| Biomarker ID | Example package |
|---|---|
| `non_hdl` | Batch A lipid transport |
| `plt` | Batch B platelet patterns (×2) |
| `lym` | Batch C lymphopenia |
| `wbc` | Batch C reactive leukocytosis |

- **Resolution path:** SSOT biomarker identity adjudication sprint; validator reports only.

### Supporting non-canonical biomarker IDs (9 item-level hits — SSOT)

Includes `hgb`, `erythropoietin`, `jak2_v617f`, `rbc_count`, `wbc`, `wbc_total`, `lym` across iron, CBC and leukocyte packages.

- **Resolution path:** Align supporting marker IDs to canonical SSOT keys or defer activation until SSOT extends.

### Derived-marker dependency (7 items — runtime / SSOT)

- **Marker:** `transferrin_saturation` referenced as supporting marker in iron-panel staged PSI.
- **Resolution path:** Derived-metric runtime support review and SSOT authority decision — not guessed by validator.

### Medical-review carry-forward (9 items)

High-risk or cohort-sensitive frames from P1-11/12 manifests (homocysteine, iron panel, leukocyte shift packages).

- **Resolution path:** `P1-MED-REV-HEMATOLOGY-1` or equivalent medical sign-off sprint.

### Frame-authority carry-forward (4 items)

Iron panel packages with overlapping Batch B / Batch C frame reconciliation notes.

- **Resolution path:** Frame-authority reconciliation sprint before opt-in.

### System-mapping carry-forward (3 items)

Leukocyte shift packages (`neutrophil_pct`, `lym`, `wbc` primary frames).

- **Resolution path:** Subsystem mapping clarity sprint for leukocyte / hematologic routing.

## 7. Specific known carry-forwards

| Topic | P1-13 finding |
|---|---|
| `lym` identity | Reported as non-canonical primary (Batch C) and supporting ID elsewhere; no mapping applied |
| `wbc` identity / SSOT | Reported as non-canonical primary in reactive leukocytosis PSI; `white_blood_cells` is canonical SSOT key |
| `transferrin_saturation` | Seven iron-panel PSI files flag derived-marker supporting dependency |
| Leukocyte system mapping | Three packages carry documented system-mapping review overlay |
| High-risk haematology medical-review cohort | Nine packages retain medical-review overlay from prior batch manifests |
| Haemoglobin Pass 3 source-support gap | No staged hemoglobin PSI in estate (P1-12 deferred); gate confirms absence — not a P1-13 defect |

## 8. Runtime non-activation confirmation

Confirmed for this sprint:

- No PSI artefacts activated (`runtime_active` remains false in all compile manifests; no edits made)
- No production package manifests changed
- No `scoring_policy.yaml` change
- No `biomarkers.yaml` change
- No `backend/core/` change
- No frontend / Gemini / parser change
- No DTO / domain assembler change
- No compiled runtime card change
- No Pass 3 or investigation-spec source change
- No staged PSI or staged compile manifest content modified

## 9. Validation

```powershell
python backend/scripts/validate_staged_psi_activation_readiness.py
python backend/scripts/validate_staged_psi_activation_readiness.py --json
python -m pytest backend/tests/unit/test_validate_staged_psi_activation_readiness.py -q
python -c "import yaml; from pathlib import Path; p=Path('docs/sprints/beta_readiness/P1-13_staged_psi_activation_readiness_manifest.yaml'); data=yaml.safe_load(p.read_text(encoding='utf-8')); assert data['work_id']=='P1-13'; assert 'items' in data; print('P1-13 activation-readiness manifest YAML parsed successfully')"
git diff --stat
git diff --name-only
git status --short
```

- **Validator output:** 41 PSI, 41 manifests, 0 activation-ready, 41 blocked, top blocker `BLOCKED_MANIFEST_OR_HASH (41)`.
- **Unit tests:** 6 passed (`test_validate_staged_psi_activation_readiness.py`).
- **Limitations:** Hash mismatch blocks mask downstream classifications in primary `activation_readiness` field; manifest includes hypothetical counts if hash integrity resolved.

## 10. Business value delivered

- Enables safe future production opt-in by inventorying blockers before runtime wiring.
- Prevents staged PSI identity gaps and manifest drift from becoming silent runtime defects.
- Supports parallel medical review and codebase readiness workstreams without micro-sprinting individual markers.
- Establishes repeatable report-only gate tooling for every future staged batch.

## 11. Carry-forwards

**Medical-review decisions**

- Homocysteine, iron-panel, leukocyte-shift medical-review overlays (9 packages)

**SSOT / biomarker identity decisions**

- `wbc`, `lym`, `plt`, `non_hdl` primary IDs; supporting aliases (`hgb`, `wbc_total`, etc.)

**Derived-marker decisions**

- `transferrin_saturation` runtime support for seven iron-panel PSI files

**Frame-authority decisions**

- Iron panel frame reconciliation (4 packages)

**Production opt-in readiness**

- Manifest hash integrity must be restored before opt-in sprint
- 22 packages would reach `ACTIVATION_READY` classification only after hash fix and absent other blockers

**Validator/tooling improvements**

- Optional `--ignore-hash-for-classification` planning mode (future — not in scope)
- Wire gate into CI as non-blocking report for staged batches

## 12. Recommended next sprint

| Field | Value |
|---|---|
| **Title** | P1-14 — Staged compile manifest integrity recompile + SSOT biomarker adjudication prep |
| **risk_level** | HIGH |
| **change_type** | MIXED |
| **Scope** | Recompute compile manifest hashes for all 41 staged PSI packages without altering PSI medical content; publish hash integrity report; open SSOT adjudication work package for `wbc`/`lym`/`plt`/`non_hdl` |
| **STOP gates** | No PSI medical edits; no production opt-in; no runtime activation; medical identity mappings require human authority |
| **Rationale** | Hash mismatch is the universal primary blocker; resolving it exposes the true 22/9/7/3 activation-readiness split for downstream sprint planning |
