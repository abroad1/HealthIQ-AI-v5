# Research to Runtime Traceability Matrix

**Work package:** ARCH-RT-0  
**Generated:** 2026-05-28

## Legend

| Status | Meaning |
|--------|---------|
| **LINKED** | Repo evidence shows direct artefact chain |
| **MISSING** | Expected link absent |
| **UNKNOWN** | Not verified in this sprint |
| **BATCH_JSON_ONLY** | Provenance stops at batch file; no per-frame manifest index |
| **LEGACY_RETAINED_CANDIDATE** | Parallel legacy package path |
| **BLOCKED_PENDING_SPEC_EXTRACTION** | Batch source; `spec_id` not on package manifest |

## Matrix

| From → To | Status | Evidence / notes |
|-----------|--------|------------------|
| investigation spec → package | **LINKED** (31 s24) | `source_document` → `inv_*.yaml` on `pkg_s24_*` |
| investigation spec → package | **BATCH_JSON_ONLY** (142) | `source_document` → `*.json`; no `source_spec_id` on manifest |
| investigation spec → package | **MISSING** (kb52c frames) | Multiple packages per batch frame; no reverse index file |
| investigation spec → PSI | **LINKED** (20 kb47) | PSI `investigation_spec_id` field |
| investigation spec → PSI | **MISSING** (166 other pkgs) | No PSI file |
| investigation spec → root-cause YAML | **MISSING** | No automated spec → YAML compile |
| investigation spec → card evidence | **MISSING** | Card markers hard-coded in `wave1_subsystem_evidence.py` |
| package → SignalRegistry | **LINKED** | All `pkg_*/signal_library.yaml` except `pkg_example` |
| package → SignalRegistry (collision) | **LEGACY_RETAINED_CANDIDATE** | Lexicographic overwrite; see collision inventory |
| signal → DTO | **LINKED** | `SignalResult` in `InsightGraph` → `assemble_consumer_domain_scores_v1` |
| signal → DTO (provenance) | **MISSING** | No `spec_id` / `activation_key` on `SignalResult` today |
| DTO → frontend component | **LINKED** | `ConsumerDomainScoreV1` / `SubsystemEvidenceV1` → `Wave1DomainCards.tsx` |
| root-cause YAML → report/WHY | **LINKED** | `root_cause_compiler_v1.py` via registry |
| root-cause YAML → investigation spec | **MISSING** | Manual registry mapping |
| PSI → SignalEvaluator | **MISSING** | PSI runtime-dead |
| IDL → domain narrative | **LINKED** | `domain_narrative_wave1.py` |
| interaction map → signal family | **UNKNOWN** | Family-level keys; frame policy undecided until ARCH-RT-2 |

## Worked example: ALT high

| Step | Status | Detail |
|------|--------|--------|
| Spec | **LINKED** | `inv_alt_high_hepatocellular_injury_v1.yaml` + frames in `Batch_5_Pass_3.json` |
| Packages | **LINKED** | 4 packages share `signal_alt_high` |
| PSI | **MISSING** | kb52c/s24 packages have no PSI |
| Root-cause YAML | **UNKNOWN** | `alt_hypotheses_v1.yaml` exists; registry link to kb52c frames not verified |
| Card evidence | **MISSING** | `alt` in enzyme subsystem only; not spec-driven |
| Registry winner | **LINKED** | `pkg_s24_alt_high_hepatocellular_injury` (lexicographic) |
| Frontend | **LINKED** | Subsystem markers from DTO |

## Worked example: Homocysteine

| Step | Status | Detail |
|------|--------|--------|
| Spec | **LINKED** | `inv_homocysteine_high_metabolic.yaml` + kb52c batch frames |
| Packages | **LINKED** | 3× `signal_homocysteine_high` + 1× `signal_homocysteine_elevation_context` |
| Root-cause | **LINKED** | Both homocysteine signal ids → `hcy_hypotheses_v1.yaml` |
| Registry winner (`signal_homocysteine_high`) | **LINKED** | `pkg_s24_homocysteine_high_metabolic` |

## Uncertainty register

1. Per-frame `spec_id` inside batch JSON not extracted to machine-readable index in this sprint.  
2. `KBP-0001` package traceability not mapped.  
3. Translator test coverage against full estate: **UNKNOWN** (spot-check only via script inventory).
