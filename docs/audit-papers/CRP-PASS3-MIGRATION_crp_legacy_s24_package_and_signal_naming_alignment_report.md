# CRP-PASS3-MIGRATION — CRP Legacy s24 Package and Signal Naming Alignment

**Work ID:** `CRP-PASS3-MIGRATION_crp_legacy_s24_package_and_signal_naming_alignment`  
**Branch:** `work/CRP-PASS3-MIGRATION-crp-legacy-s24-package-and-signal-naming-alignment`  
**Sprint type:** **Classification and guardrail** (not migration)  
**Status:** Closed for final audit (2026-05-31)

## Executive closure verdict

CRP-PASS3-MIGRATION is closed as a **classification and guardrail sprint**. It does **not** migrate runtime package authority.

The earlier sprint narrative implied a possible Pass 3 migration path for CRP-related signals. **Deeper provenance investigation superseded that premise:**

- `pkg_chronic_inflammation` is **runtime-loaded**, drives `signal_systemic_inflammation`, and is **not Pass 3–derived**.
- It is **study-derived / legacy-thin** (`study_04_chronic_inflammation.md`) and is **internally flagged** for Knowledge Bus re-review in `crp_runtime_authority_v1.yaml`.
- It must **not** be conflated with `signal_crp_high` or Batch 4 Pass 3 CRP frames.
- **No runtime behaviour changed** in this sprint (no SignalEvaluator, thresholds, scoring, frontend, or SSOT changes).

**Correct outcome:** governed classification + ARCH-RT-6 guards + carry-forwards for future KB/medical research work — **not** runtime migration.

## Architectural conclusion (authoritative)

| Signal | Runtime authority | Provenance type | Pass 3–derived? | Re-review / migration status |
|---|---|---|:---:|---|
| `signal_crp_high` | `pkg_s24_crp_high_inflammation` | `investigation_spec_v1_yaml_translation` | **No** (v1 YAML translation; Pass 3 frames exist in research only) | Pass 3 compile deferred — `CF-CRPPASS3-001` |
| `signal_systemic_inflammation` | `pkg_chronic_inflammation` (primary), `KBP-0001` (secondary frame) | `research_study_translation` | **No** | **Internal KB re-review required** — `CF-MRIMPROVE-001` |
| `signal_inflammation_crp_context` | `pkg_inflammation_crp_context` | `manual_context_anchor` | **No** | Optional KB re-review |

**`pkg_chronic_inflammation` (KBP-0005):**

- Has `signal_library.yaml` — **runtime-loaded** by `SignalRegistry`.
- Source: `knowledge_bus/research/study_04_chronic_inflammation.md` — **not** any Pass 3 JSON/YAML frame.
- **Retained** in runtime authority registry (not removed).
- **Not** semantically equivalent to `inv_crp_high_*` Pass 3 frames → **migration not authorised**.

## What this sprint delivered

1. **`knowledge_bus/governance/crp_runtime_authority_v1.yaml`** — provenance, Pass 3–derived flags, re-review status per signal and `pkg_chronic_inflammation`.
2. **`validate_crp_signal_authority`** — ARCH-RT-6 guard against authority drift and Pass 3 conflation.
3. **Regression tests** — `test_crp_pass3_migration_signal_authority.py`.
4. **Package estate audit** — preserved artefacts:
   - [CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md](./CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md)
   - [\_crp_pkg_audit_non_pass3.json](./_crp_pkg_audit_non_pass3.json)
5. **Carry-forward register** — `CF-ARCHLEG1-002` resolved (classified); `CF-MRIMPROVE-001` for non–Pass 3 runtime package KB re-review.

## What this sprint did not do

- No package pointer migration to Pass 3.
- No user-facing warnings or disclosure.
- No changes to `SignalEvaluator`, clinical thresholds, scoring rails, frontend, or SSOT.
- No removal of `pkg_chronic_inflammation` from runtime loading.

## Files changed (full sprint + closure)

- `knowledge_bus/governance/crp_runtime_authority_v1.yaml`
- `backend/core/knowledge/crp_signal_authority_v1.py`
- `knowledge_bus/packages/pkg_s24_crp_high_inflammation/package_manifest.yaml` (Pass 3 lineage metadata only)
- `backend/scripts/validate_day_one_architecture.py`
- `backend/tests/regression/test_crp_pass3_migration_signal_authority.py`
- `docs/sprints/launch_core_carry_forward_register.md`
- `docs/audit-papers/CRP-PASS3-MIGRATION_package_provenance_non_pass3_table.md`
- `docs/audit-papers/_crp_pkg_audit_non_pass3.json`

## Package estate summary (55 non–Pass 3 of 187 total)

| Metric | Count |
|---|---:|
| Total packages | 187 |
| Pass 3–sourced | 132 |
| Not Pass 3–sourced | 55 |
| Runtime-loaded | 186 |

See addendum table files for full non–Pass 3 inventory.

## Confirmations

- No clinical thresholds, scoring rails, SignalEvaluator mathematics, or SSOT changes.
- No raw Pass 3 runtime reads introduced.
- Hidden MED-REV-1 subsystem policy unchanged.
- Manual UAT not required.

## Final validation (closure re-run)

```powershell
python backend/scripts/validate_day_one_architecture.py
python -m pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q
python -m pytest backend/tests/regression/test_crp_pass3_migration_signal_authority.py -q
```

**Results:** PASS / PASS (11 tests)

## Remaining carry-forwards

- **CF-CRPPASS3-001** — Pass 3 compile for `signal_crp_high` frames only (separate from systemic inflammation)
- **CF-MRIMPROVE-001** — MED-RESEARCH-REVIEW-1 non–Pass 3 package revalidation cohort
- **CF-MRIMPROVE-002** — `pkg_kb45_*` batch JSON lineage
- **CF-MRIMPROVE-003** — Architecture-doc anchor packages
- **CF-MRIMPROVE-004** — `pkg_lipid_transport` provenance gap
- **CF-CHRONICINFL-001** — Future Pass 3 frame for `signal_systemic_inflammation` if promotion from study-derived model is ever authorised
- **CF-ARCHLEG1-001** / **CF-ARCHLEG1-004** — Root-cause programme / validator inventory
