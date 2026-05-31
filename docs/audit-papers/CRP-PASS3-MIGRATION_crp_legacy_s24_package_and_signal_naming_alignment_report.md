# CRP-PASS3-MIGRATION — CRP Legacy s24 Package and Signal Naming Alignment

**Work ID:** `CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment`  
**Branch:** `work/CRP-PASS3-MIGRATION-crp-legacy-s24-package-and-signal-naming-alignment`  
**Status:** Complete (2026-05-31)

## Authority decision

**Outcome B + C (combined):** Pass 3 CRP investigation frames exist in `Batch_4_Pass_3.json` but are **not semantically compiled** into a runtime package equivalent to `pkg_s24_crp_high_inflammation`. Runtime authority for `signal_crp_high` **remains** the s24 translation from `inv_crp_high_inflammation_v1.yaml`, now **explicitly classified** in `knowledge_bus/governance/crp_runtime_authority_v1.yaml`.

**Outcome D:** `signal_crp_high` and `signal_systemic_inflammation` are **distinct clinical constructs**, not aliases:

| Signal | Role | Activation | Runtime package(s) | Root cause |
|---|---|---|---|---|
| `signal_crp_high` | Acute-phase CRP investigation | `lab_range_exceeded` | `pkg_s24_crp_high_inflammation` only | No |
| `signal_systemic_inflammation` | Chronic low-grade inflammation construct | `deterministic_threshold` | `KBP-0001`, `pkg_chronic_inflammation` (multi-frame via `activation_key`) | Yes — `systemic_inflammation_hypotheses_v1.yaml` |
| `signal_inflammation_crp_context` | CRP context escalation | `lab_range_exceeded` | `pkg_inflammation_crp_context` | No |

**Migration performed:** Metadata classification + validator/test guards. **Not performed:** Package pointer swap to Pass 3 (deferred — `CF-CRPPASS3-001`).

## Preflight inventory

### CRP-related signals (runtime libraries)

- `signal_crp_high` — `pkg_s24_crp_high_inflammation` (sole holder)
- `signal_systemic_inflammation` — `KBP-0001`, `pkg_chronic_inflammation`
- `signal_inflammation_crp_context` — `pkg_inflammation_crp_context`

### CRP-related packages

- `pkg_s24_crp_high_inflammation` — **active** runtime authority for `signal_crp_high`
- `pkg_inflammation_crp_context` — context signal only
- `KBP-0001` / `pkg_chronic_inflammation` — systemic inflammation frames

### Pass 3 specs (research only)

- `inv_crp_high_active_inflammatory_or_infective_state` — `Batch_4_Pass_3.json`
- `inv_crp_high_residual_cardiometabolic_inflammatory_risk` — `Batch_4_Pass_3.json`
- Legacy v1: `inv_crp_high_inflammation_v1.yaml` (translated to s24)

### User-facing surfaces (MED-REV-1/2)

- `wave1_cv_vascular_strain` — `hidden_v1`; CRP does not appear as scored subsystem
- Cardiovascular card — lipid-led (`wave1_cv_lipid_transport` scored)
- Root cause — `signal_systemic_inflammation` only (not `signal_crp_high`)

## Files changed

- `knowledge_bus/governance/crp_runtime_authority_v1.yaml` (new)
- `backend/core/knowledge/crp_signal_authority_v1.py` (new)
- `knowledge_bus/packages/pkg_s24_crp_high_inflammation/package_manifest.yaml`
- `backend/scripts/validate_day_one_architecture.py`
- `backend/tests/regression/test_crp_pass3_migration_signal_authority.py` (new)
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/audit-papers/CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment_report.md`

## Validator / test changes

- Added `validate_crp_signal_authority` to ARCH-RT-6 validator
- New regression module `test_crp_pass3_migration_signal_authority.py`

## Confirmations

- No clinical thresholds, scoring rails, SignalEvaluator mathematics, or SSOT changes
- No raw Pass 3 runtime reads introduced
- No hidden subsystem re-surfacing
- Manual UAT not required (no user-facing output path change)

## Tests run

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_crp_pass3_migration_signal_authority.py -q
python -m pytest backend/tests/regression/test_med_rev1_wave1_subsystem_visibility.py -q
python -m pytest backend/tests/regression/test_med_rev2_domain_card_copy_and_regeneration.py -q
```

**Results:** PASS / PASS / PASS / PASS / PASS

## Addendum — `pkg_chronic_inflammation` provenance investigation (pre-finalisation)

**Investigation date:** 2026-05-31  
**Scope:** Documentation-only audit; no runtime, threshold, scoring, or migration changes.

### Answers 1–4: `pkg_chronic_inflammation`

| Question | Finding |
|---|---|
| **1. Source** | `knowledge_bus/research/study_04_chronic_inflammation.md` (research study markdown). Manifest: `package_manifest.yaml` line `source_document`. Also `research_brief.yaml` cites the same study. |
| **2. Pass 3 references?** | **No.** Manifest has no `source_spec_id`, no `pass3_research_frames`, no Pass 3 JSON path. ARCH-RT-5D classifies as `architecture_doc_source_blocked` (study markdown cohort). |
| **3. Built from Pass 3?** | **No.** Not applicable. |
| **4. Actual build path** | **Research-study translation (manual/creation)** — KBP-0005 / KB-S45e governed threshold model for `signal_systemic_inflammation`. **Not** generated from any Pass 3 investigation frame. |

**Correction to a common misconception:** `pkg_chronic_inflammation` **does** include `signal_library.yaml` (one signal: `signal_systemic_inflammation`) and **is runtime-loaded** by `SignalRegistry` (distinct `activation_key` from KBP-0001 via `inv_chronic_inflammation` vs KBP-0001 package id).

**Pass 3 relationship (indirect only):**

- `Batch_4_Pass_3.json` contains **two** frames for `signal_crp_high` (`inv_crp_high_active_inflammatory_or_infective_state`, `inv_crp_high_residual_cardiometabolic_inflammatory_risk`), not for `signal_systemic_inflammation`.
- No investigation spec in `knowledge_bus/research/investigation_specs/**` declares `signal_id: signal_systemic_inflammation`.
- Chronic metabolic inflammation framing in Pass 3 is embedded in **CRP-high** residual-risk narrative, not as a separate governed package for the systemic-inflammation construct.

**Classification:** `research_study_translation` / **legacy thin pre-v3 context** (`package_estate_KB-S49_v1.yaml`).  
**Migration:** **Not authorised** — semantic equivalence to any Pass 3 frame is **not proven**; KBP-0005 thresholds (RIR ≥2.0 mg/L) differ materially from KBP-0001 and from `signal_crp_high` lab-range logic.

### Answers 5–6: Full package estate audit (`knowledge_bus/packages/**`)

| Metric | Count |
|---|---:|
| Total packages | **187** |
| Pass 3–sourced (`*Pass_3*.json` / `*pass_3*.json` in `source_document`) | **132** |
| Not Pass 3–sourced | **55** |
| Unknown / ambiguous provenance | **11** (10 `investigation-spec-collection-batch*.json` + 1 `provenance_gap`) |
| With `signal_library.yaml` | **187** |
| Without `signal_library.yaml` | **0** |
| Runtime-loaded (non-empty signals, excl. `pkg_example`) | **186** |
| Research/context-only (no runtime signals) | **0** |

**Non–Pass 3 cohort breakdown:**

| Provenance class | Count | Examples |
|---|---:|---|
| `investigation_spec_v1_yaml` | 31 | All `pkg_s24_*` including `pkg_s24_crp_high_inflammation` |
| `pass3_batch_or_json` | 132 | `pkg_kb52c_*`, `pkg_kb47_*`, `pkg_kb58_*`, … |
| `architecture_doc_blocked` | 8 | `pkg_inflammation_crp_context`, `pkg_homocysteine_elevation_context`, … |
| `research_study_markdown` | 3 | `pkg_chronic_inflammation`, `pkg_insulin_resistance`, `pkg_hepatic_metabolic_stress` |
| `unknown_ambiguous` | 10 | `pkg_kb45_*` → batch JSON collections |
| `legacy_retained_with_justification` | 1 | `KBP-0001` |
| `provenance_gap` | 1 | `pkg_lipid_transport` |
| `retire_candidate` | 1 | `pkg_example` |

**Full table (55 non–Pass 3 packages):** see [CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md](./CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md).  
Machine-readable rows: [\_crp_pkg_audit_non_pass3.json](./_crp_pkg_audit_non_pass3.json).

### Impact on CRP-PASS3-MIGRATION authority decision

The sprint correctly treats:

- `signal_crp_high` → `pkg_s24` + Pass 3 CRP frames (deferred compile: `CF-CRPPASS3-001`)
- `signal_systemic_inflammation` → **study-derived KBP-0005** + KBP-0001 multi-frame — **separate track**, not a Pass 3 migration candidate in this sprint

**Paused:** Any YAML “correction” that would reclassify `pkg_chronic_inflammation` as Pass 3–sourced without a dedicated Pass 3 frame.

## Remaining carry-forwards

- **CF-CRPPASS3-001** — Compile Pass 3 CRP frames (`signal_crp_high`) to governed runtime package
- **CF-CHRONICINFL-001** — Create Pass 3 investigation frame + compile path for `signal_systemic_inflammation` (study_04 / KBP-0005 cohort); do not conflate with `signal_crp_high` Pass 3 frames
- **CF-MRIMPROVE-001** — Study-derived package cohort (`pkg_chronic_inflammation`, `pkg_insulin_resistance`, `pkg_hepatic_metabolic_stress`) — Pass 3 spec alignment programme
- **CF-MRIMPROVE-002** — Pre–Pass 3 `pkg_kb45_*` batch JSON lineage — map to Pass 3 or retire
- **CF-ARCHLEG1-001** — Root-cause YAML vs compiled promotion programme
- **CF-ARCHLEG1-004** — Root-cause promotion inventory validator (partial)
