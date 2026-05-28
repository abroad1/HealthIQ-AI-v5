# ARCH-R1 — Research Asset to Runtime Intelligence Architecture Review

**Date:** 2026-05-28  
**Author:** Claude Code (architecture review only — no code changes)  
**Status:** DRAFT FOR ARCHITECTURAL DECISION  
**Scope:** Read-only. No files modified.

---

## 1. Executive Verdict

HealthIQ has a broken intelligence pipeline. The research is good. The product surface is thin. The gap is structural, not minor, and it persists because there is no governed compile step that carries Pass 3 richness into the runtime layer that feeds Health Systems Cards.

**Recommended architecture:** Pass 3 remains the canonical upstream research source. Two governed compile steps produce downstream runtime views: (1) an extended signal package carrying marker-role semantics, (2) a new intelligence overlay carrying hypothesis frames, contradiction markers, confirmatory tests, and missing-data policy. Health Systems Cards consume from both. Root-cause hypothesis YAML transitions from hand-authored to compiled view over two phases. IDL gates all prose before it reaches retail users.

The immediate priority is not a new schema — it is the consumption gap: the assembler that builds Health Systems Card evidence currently reads nothing from any knowledge asset. That assembler (`wave1_subsystem_evidence.py`) must be replaced with one that reads from governed package intelligence. Everything else follows from fixing that one broken connection.

---

## 2. Current-State Map

### 2.1 Pass 3 → Runtime → UX (primary path)

```
Pass 3 JSON (153 specs, 9 batch files)
  → [KB-S24 ingestion sprint, manually run]
  → pkg signal_library.yaml
      - Carries: activation_logic, override_rules, explanation.{mechanism|biological_pathway|interpretation|implications|supporting_marker_roles}
      - Strips: supporting_markers[].role, relationship_kind, availability, rationale
      - Strips: ALL hypotheses, hypothesis_ranking, contradiction_markers, missing_data.policy
      - Strips: confirmatory_tests (from Pass 3)
      - Strips: evidence.sources citations
      - Note: newer KB-S52* packages carry structured supporting_metrics with role/availability/rationale;
        pkg_s24_* packages carry flat string lists only (schema_version 1.0.0)

  → SignalEvaluator (signal_evaluator.py)
      - Reads: activation_logic, activation_config, thresholds, override_rules
      - Reads: output.supporting_markers (flat list, for confidence scoring only)
      - DOES NOT READ: explanation.*, supporting_metrics[].role, relationship_kind
      - Fires SignalResult with explanation.* attached but NOT used downstream

  → domain_score_assembler.py
      - Computes: domain score, confidence tier from rail biomarker scores
      - DOES NOT consume: any explanation, any Pass 3 intelligence

  → wave1_subsystem_evidence.py
      - Reads: NOTHING from any KB asset
      - Uses: hard-coded Python dict (WAVE1_DOMAIN_SUBSYSTEM_DEFS) with 7 hand-written
        subsystem definitions and flat expected-marker tuples
      - Emits: SubsystemEvidenceV1 with evidence_role=None (always null)

  → ConsumerDomainScoreV1 / SubsystemEvidenceV1 DTOs
      - No hypothesis framing, no marker roles, no relationship semantics, no contradiction
        logic, no missing-data policy, no confirmatory tests

  → Frontend (Wave1DomainCards.tsx + Wave1SubsystemEvidenceSection.tsx)
      - Renders: domain score, band label, confidence tier, 5 narrative sentences
      - Renders: subsystem included/missing chips
      - CANNOT render: any Pass 3 intelligence (no DTO fields exist for it)
```

### 2.2 Root-cause hypothesis layer (parallel, independent)

```
40 hand-authored YAML files (KB-S33 + extensions)
  knowledge_bus/root_cause/hypotheses/*_hypotheses_v1.yaml
  Schema: {hypothesis_id, title, summary_template, evidence_for_rules, evidence_against_rules,
           missing_data_markers, confirmatory_tests}

  → root_cause_registry_v1.py (loads all YAML files)
  → root_cause_compiler_v1.py (evaluates rules against panel, produces WHY output)
  → IDL / narrative report (report_compiler_v1.py)
      - Surfaces in: report / narrative layer
      - DOES NOT surface in: Health Systems Cards / Wave 1 domain cards
```

**Key observation:** The root-cause hypothesis layer and the Pass 3 hypothesis layer are completely independent. They were authored separately, use different schemas, cover the same clinical territory, and have no validated cross-check. For signals where both exist (HbA1c, ALT, CRP, GGT, triglycerides, etc.), there is no governance preventing them from diverging.

---

## 3. Current Fragmentation Problems

The following 11 fragmentation problems are confirmed by direct source inspection and the 2026-05-28 investigations.

**P1 — Pass 3 → package translation is too lossy.**  
Of 14 distinct Pass 3 field groups, 7 are completely absent from any package file: hypotheses, hypothesis_ranking, contradiction_markers, missing_data.policy, caveats, per-hypothesis evidence_strength, and confirmatory_tests. This is not a schema gap to be patched incrementally; it is a fundamental gap between what was researched and what was compiled.

**P2 — Package explanation.* is loaded but never routed to Health Systems Cards.**  
The five narrative prose fields (mechanism, biological_pathway, interpretation, implications, supporting_marker_roles) are faithfully preserved in pkg signal_library and loaded into SignalResult.explanation. SignalEvaluator attaches them. Nothing downstream reads them for Health Systems Cards. This is the clearest single wasted asset in the repo.

**P3 — wave1_subsystem_evidence.py reads no KB intelligence at all.**  
The assembler that populates Health Systems Card subsystem evidence is a 173-line Python file containing a hard-coded dictionary. It reads no package file, no Pass 3 file, no schema, no role data. It is the exact point where the intelligence pipeline breaks.

**P4 — evidence_role is permanently null.**  
`SubsystemEvidenceV1.evidence_role` was explicitly designed as the hook for future role information (`results.py:209`: "Optional role hint for future UI; null in DOMAIN-UX1C"). It has never been populated. The model supports it; the assembler ignores it; the frontend is ready to render it.

**P5 — Two competing hypothesis authorities with no cross-check governance.**  
For ~25 signals, both Pass 3 hypothesis frames and root_cause YAML hypotheses exist. They were authored independently and use incompatible schemas. There is no validation, no divergence check, and no governance process that reconciles them. They will silently diverge as either is updated.

**P6 — Marker role data exists in newer packages but is not consumed.**  
KB-S52* packages carry structured supporting_metrics with role, availability, and rationale. The signal_library schema v2.0.0 supports this. The SignalEvaluator loads it into SignalResult. Health Systems Card assembly does not use it. This is a consumption gap, not a data gap, for the newer package generation.

**P7 — Hard-coded subsystem maps contain confirmed defects.**  
`total_bilirubin` is a display_label_rail_only identity in biomarkers.yaml and should never appear in expected subsystem marker sets. It is permanently false-missing on every liver card. The `wave1_cv_vascular_strain` subsystem (CRP only) is housed under the cardiovascular card but CRP contributes to the inflammatory rail, not the cardiovascular rail — the label misleads users about what drives the cardiovascular score.

**P8 — Supporting marker roles are implicit, not emitted.**  
All Wave 1 subsystem markers are rendered identically regardless of whether they are score contributors, confidence contributors, contextual markers, or missing-for-confidence markers. The current model has no way to distinguish LDL (score driver) from homocysteine (contextual) from CRP (wrong rail entirely).

**P9 — Subsystem maps and domain scoring rails are architecturally decoupled without explanation.**  
The liver scoring rail is alt+ast only. The liver subsystem evidence shows alt, ggt, alp, albumin, bilirubin. The domain completeness reads "1 of 2" while the expanded subsystem view shows 5 included markers. Users cannot reconcile these two counts. Neither the DTO nor the frontend provides any bridging explanation.

**P10 — Promoted_signal_intelligence schema exists but no package uses it.**  
`knowledge_bus/schema/promoted_signal_intelligence_schema_v1.yaml` defines a richer signal contract including role. No current package directory contains a `promoted_signal_intelligence.yaml` file. This schema is dead weight unless a governed compile step creates these files.

**P11 — IDL does not receive structured intelligence.**  
The IDL layer governs what retail prose users see. But IDL currently receives narrative text (from signal_library explanation.* or from root_cause compiler output) — not structured hypothesis frames or contradiction semantics. This means IDL can only govern phrasing, not hypothesis-level interpretation logic. The safety gate is present but is working on impoverished inputs.

---

## 4. Source-of-Truth Assessment

| Asset | Current Role | Strength | Weakness | Should Be Authority For |
|---|---|---|---|---|
| **Pass 3 JSON** (153 specs, 9 files) | Upstream research source; read at KB compile time only; not at runtime | Complete schema v3.0.0 compliance; ranked hypotheses; contradiction markers; relationship_kind; per-marker rationale; evidence.sources with cited papers; full narrative; 100% field coverage | Not read at runtime; partially translated (7 of 14 field groups lost in pkg_s24_*); no automated bridge to root-cause YAML; not version-locked per-compile | **Canonical upstream research source and single compile-time authority for all downstream intelligence assets** |
| **pkg signal_library.yaml** (~132 packages) | Runtime signal activation + explanation prose | Activation logic, override rules, explanation.* prose preserved; validated by validate_signal_library.py; newer packages have structured supporting_metrics with role | schema_version 1.0.0 packages lack role/relationship_kind per marker; explanation.* loaded but not routed to domain cards; no hypothesis data; 7 of 14 Pass 3 field groups absent | **Runtime signal activation, threshold and override evaluation, and (when extended to v2.0.0) per-marker relationship semantics. Nothing more.** |
| **Root-cause hypothesis YAML** (40 files) | Deterministic WHY layer for root_cause_compiler_v1.py | Active; 40 files; feeds report compiler and IDL; well-governed schema v1 | Authored independently from Pass 3; incompatible schema; no cross-check with Pass 3 hypotheses; does not surface in Health Systems Cards; divergence is ungoverned and undetected | **Transitional: remain as root-cause compile authority for report/IDL until migrated to compiled view from Pass 3. Not the upstream source of truth.** |
| **IDL** | Retail prose safety gate | Governed prose; safety layer for retail UX | Receives prose (narrative text), not structured intelligence; cannot gate hypothesis-level or contradiction-level logic; not aware of hypothesis ranking or evidence strength | **Retail narrative safety gate only. Must eventually receive structured inputs to gate interpretation quality, not just phrasing.** |
| **wave1_subsystem_evidence.py hard-coded maps** | Wave 1 Health Systems Card subsystem structure | Simple, auditable Python | Disconnected from all KB intelligence; contains confirmed defects (total_bilirubin false-missing, wrong-rail CRP subsystem); evidence_role always null; not updatable without a code sprint | **Should be eliminated entirely. Replace with assembler that reads from governed package intelligence.** |
| **SubsystemEvidenceV1 / ConsumerDomainScoreV1 DTOs** | Frontend DTO contract | Clean boundary; frozen Pydantic models | Too flat for marker-role semantics; no hypothesis fields; no contradiction fields; no missing-data policy fields | **DTO boundary between backend intelligence and frontend rendering. Needs schema extension for marker roles. Future extension for hypothesis framing.** |
| **promoted_signal_intelligence_schema_v1.yaml** | Schema spec for richer signal contract | Defines role vocab; exists and is versioned | No package uses it; orphaned schema | **Dead weight. Decide: extend to cover intelligence overlay needs, or replace with the new intelligence overlay schema.** |

---

## 5. Architecture Options

| Option | Description | Pros | Cons | Risk | Long-term Fit | Recommendation |
|---|---|---|---|---|---|---|
| **A — Enrich pkg files until they become full runtime intelligence authority** | Add hypotheses[], contradiction_markers, relationship_kind, confirmatory_tests to signal_library schema and re-run all KB-S24/S52 ingestion for all affected packages | Single asset type; no new layer; uses existing validation pipeline | Signal_library becomes a multi-purpose YAML combining activation logic, evaluation rules, and full hypothesis graphs — three different concerns in one file. Two incompatible hypothesis lineages (Pass 3 vs root_cause v1 YAML) are forced to coexist in the same file. Schema migration touches 186+ files. Hypothesis graph is structurally complex for a YAML schema already governing evaluation logic | HIGH (schema migration at scale; risk of evaluation logic breakage) | Poor — oversized file; competing hypothesis lineages; the signal_library is the wrong home for hypothesis graphs | **Reject for hypothesis graph. Partial accept for relationship_kind + availability per supporting_metric (schema v2.0.0 extension only).** |
| **B — Keep Pass 3 canonical; compile two governed runtime views** | Pass 3 = canonical source. Compile 1: extend signal_library to v2.0.0 (relationship_kind, availability per supporting_metric). Compile 2: new intelligence overlay file per signal carrying hypothesis frames, contradiction_markers, confirmatory_tests, missing_data policy | Clean separation of concerns; each asset is purpose-fit; Pass 3 richness fully preserved; signal evaluator is untouched; intelligence overlay can be introduced incrementally | New intelligence overlay layer requires new schema, new loader, new validation, new governance sprint. The compile step is currently manual (KB sprints) — automation would be needed for scale | HIGH for intelligence overlay introduction; STANDARD for signal_library extension | **Best long-term architecture. Scales naturally. Each layer has one job.** | **Recommended** |
| **C — Separate Health Systems Card evidence layer beside packages** | Create per-domain card_evidence_*.yaml files compiled specifically for Health Systems Cards from Pass 3 | Targeted; does not touch signal evaluator | Introduces yet another asset type alongside packages; governance of card_evidence vs signal_library vs intelligence overlay becomes complex; card-specific compilation is a duplication of what intelligence overlay would do | STANDARD-HIGH | Poor — creates parallel track to Option B without the benefits of a unified intelligence layer | **Reject if Option B is chosen. Option C is subsumed by a card-aware intelligence overlay.** |
| **D — Merge root-cause hypotheses into pkg files** | Move root_cause hypothesis YAML content into signal_library packages | One consolidated package | Root_cause schema v1 is incompatible with Pass 3 hypothesis format. Merging two different hypothesis lineages into signal_library creates an unmaintainable mixed-lineage asset. Root_cause files were hand-authored with different medical review; merging them with Pass 3 without validated reconciliation would introduce clinical claims of unknown provenance | ARCHITECTURAL | Very poor — creates merged asset with two competing lineages and unclear authority | **Reject.** |
| **E — Keep current architecture; patch gaps incrementally** | Fix total_bilirubin false-missing, rename weak subsystem labels, populate explanation.* into domain card copy | Safe; minimal risk; immediate trust improvement | Does not address the fundamental intelligence utilisation gap; continues wasting Pass 3 richness; adds text to cards without structural intelligence; produces a richer card facade with the same thin backend | LOW | Poor as a final state; acceptable as an immediate bridge while architecture is agreed | **Do the immediate patches (F1, F2 below). But do not treat this as the final architecture.** |
| **F — Two-tier compile from Pass 3 as permanent architecture (proposed)** | Identical to Option B but with explicit governance model: Pass 3 is never read at runtime; signal_library = activation + marker semantics authority; intelligence overlay = interpretation authority; root_cause transitions to compiled view; Health Systems Card assembler reads from both signal_library and intelligence overlay | Best long-term pipeline; each layer has one clear responsibility; no duplicated authorities; governance is explicit and auditable | Requires two new governed compile sprints (signal_library v2.0.0 extension + intelligence overlay schema + compile); root-cause migration is phased work over multiple sprints | HIGH for full delivery; phaseable to STANDARD per sprint | **Best. This is Option B with a phased migration plan.** | **Recommended as the target architecture** |

---

## 6. Recommended Target Architecture

```
┌──────────────────────────────────────────────────────────┐
│  UPSTREAM RESEARCH AUTHORITY                             │
│  Pass 3 investigation specs (9 batch files, 153 specs)   │
│  investigation_spec_contract_version: 3.0.0             │
│  investigation_spec_schema_v3.0.0.yaml validates these  │
│  [Never read at runtime. Read only at KB compile time.]  │
└──────────────────┬───────────────────────────────────────┘
                   │ KB compile sprint
         ┌─────────┴──────────┐
         ▼                    ▼
┌────────────────┐   ┌────────────────────────────────┐
│ SIGNAL PACKAGE │   │  INTELLIGENCE OVERLAY          │
│ (extended)     │   │  (new governed asset)          │
│                │   │                                │
│ signal_library │   │ per-signal .yaml or .json      │
│ schema v2.0.0  │   │ Carries:                       │
│                │   │  - ranked_hypotheses[]         │
│ Carries:       │   │    (physiological_claim,       │
│  - activation  │   │     evidence_strength,         │
│  - thresholds  │   │     caveats,                   │
│  - override    │   │     missing_data.policy)       │
│  - supporting  │   │  - contradiction_markers[]     │
│    _metrics[]  │   │  - confirmatory_tests[]        │
│    with role,  │   │  - hypothesis_ranking          │
│    relation-   │   │  - evidence.sources[]          │
│    ship_kind,  │   │                                │
│    availability│   │ Schema: intelligence_overlay   │
│  - explanation │   │   _schema_v1.yaml (new)        │
│    .* prose    │   │ Validated by:                  │
│                │   │   validate_intelligence        │
│ Validated by:  │   │   _overlay.py (new)            │
│  validate_     │   │                                │
│  signal_       │   │ [Not read by SignalEvaluator.  │
│  library.py    │   │  Read by assembler only.]      │
└───────┬────────┘   └───────────┬────────────────────┘
        │                        │
        │ runtime load           │ runtime load
        ▼                        ▼
┌──────────────────────────────────────────────────────────┐
│  SIGNAL EVALUATOR  (signal_evaluator.py) — unchanged     │
│  Reads: signal_library activation, thresholds, overrides │
│  Produces: SignalResult (with activated signals)         │
│  DOES NOT READ: intelligence overlay                     │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  HEALTH SYSTEMS CARD EVIDENCE ASSEMBLER (new/replacement)│
│  Replaces: wave1_subsystem_evidence.py hard-coded dict   │
│                                                          │
│  Reads from:                                             │
│   - signal_library (per-marker relationship_kind, role)  │
│   - intelligence_overlay (hypothesis frames, contradic-  │
│     tions, missing_data.policy, confirmatory_tests)      │
│  Reads: panel_biomarker_ids + scored_on_rail             │
│                                                          │
│  Produces: SubsystemEvidenceV1 with:                     │
│   - included/missing marker IDs (as today)               │
│   - per-marker evidence_role (relationship_kind from     │
│     signal_library supporting_metrics)                   │
│   - hypothesis framing (from intelligence overlay)       │
│   - [future] contradiction alerts                        │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  ROOT-CAUSE COMPILER (root_cause_compiler_v1.py)         │
│  PHASE 1 (now): reads hand-authored hypothesis YAML      │
│  PHASE 2 (future): reads compiled hypothesis view from   │
│   intelligence overlay — replaces hand-authored YAML     │
│   for signals where Pass 3 coverage is complete         │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  IDL / PRESENTATION SAFETY LAYER                         │
│  Current: governs retail prose text                      │
│  Future: receives structured intelligence inputs to gate │
│   hypothesis-level interpretation quality, not just      │
│   prose phrasing                                         │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  DTO BOUNDARY                                            │
│  ConsumerDomainScoreV1 + SubsystemEvidenceV1             │
│  Extended to carry per-marker role fields                │
│  Future: carry hypothesis framing                        │
└──────────────────┬───────────────────────────────────────┘
                   │
                   ▼
┌──────────────────────────────────────────────────────────┐
│  FRONTEND RENDERING BOUNDARY                             │
│  Wave1DomainCards.tsx + Wave1SubsystemEvidenceSection.tsx│
│  Renders only what the DTO emits                         │
│  No clinical logic, no role inference                    │
└──────────────────────────────────────────────────────────┘
```

---

## 7. Package File Decision

Package files (`signal_library.yaml`) should be extended to schema version 2.0.0 where not already done, and should remain the **sole runtime authority for signal activation and per-marker relationship semantics**.

They should NOT be:
- The home for hypothesis graphs. The hypothesis graph (ranked frames, contradiction markers, missing-data policy) is structurally incompatible with a YAML file that must also govern evaluation logic. These are different purposes and different governance rhythms.
- A merged store of Pass 3 + root_cause hypothesis content. Two incompatible lineages cannot share a schema without creating an unmaintainable asset.

The `pkg_s24_*` files that use schema_version 1.0.0 (flat `supporting_metrics` string list) should be re-ingested at the next appropriate KB sprint to carry structured supporting_metrics with `role`, `relationship_kind`, and `availability`. This is a governed compile step, not a hand-edit.

The `explanation.*` prose fields in signal_library are correctly placed and correctly compiled from Pass 3 narrative. The gap is in consumption: nothing routes them to Health Systems Cards. The new assembler must consume them alongside the intelligence overlay.

---

## 8. Pass 3 Decision

Pass 3 remains the **canonical upstream research source**. It is not deprecated. It is not read at runtime.

The correct permanent role of Pass 3:
- **Source of truth** for all clinical claims, hypothesis frames, relationship semantics, evidence citations, and confirmatory test rationale in the system
- **Compile-time input** to two downstream views: extended signal_library and intelligence overlay
- **Versioned and locked** at each KB sprint; compile outputs must be traceable to specific Pass 3 spec IDs
- **Not the upstream for root_cause YAML** today, but should become so in phase 2 as root_cause YAML transitions to compiled view

Pass 3 should not be:
- Migrated to a new canonical research format. The investigation_spec_contract_version 3.0.0 schema is well-structured and complete. The problem is not the research format; it is the compile pipeline.
- Read directly at runtime by any evaluator, assembler, or report compiler. Raw research JSON at runtime violates Layer B determinism and introduces uncontrolled schema changes.
- Deprecated after compile. It is the upstream evidence base. If a compile output is challenged, the resolution is in Pass 3.

---

## 9. Root-Cause Hypothesis Decision

### Current state
40 hand-authored YAML files using schema v1 (`summary_template`, `evidence_for_rules`, `evidence_against_rules`, `missing_data_markers`, `confirmatory_tests`). Authored in KB-S33. Independently from Pass 3. No validated cross-check.

### The problem
For ~25 signals, Pass 3 and root_cause YAML both claim hypothesis authority. The clinical content overlaps but is not identical. Pass 3 has `physiological_claim` (present-tense mechanistic statement) where root_cause v1 has `summary_template` (interpretive pattern framing). These are not equivalent. Pass 3 has `contradiction_markers`; root_cause v1 has no equivalent concept. Pass 3 has `evidence_strength` per hypothesis; root_cause v1 has it at the hypothesis level but with different granularity.

### Decision

**Phase 1 (now — do not break the working root-cause layer):**  
Keep all 40 root_cause YAML files in place. Do not modify them. They feed root_cause_compiler_v1.py which feeds IDL. This is the only functional hypothesis-to-user pipeline in the product today. Do not disrupt it.

**Phase 2 (medium-term):**  
For signals where Pass 3 coverage is complete, create a governed compile step that produces root_cause-compatible hypothesis YAML from the intelligence overlay. Validate that compiled hypotheses match or supersede the hand-authored files. Replace hand-authored files one signal at a time with reviewed compiled views. Keep the original files archived under `knowledge_bus/root_cause/hypotheses/legacy/`.

**Phase 3 (long-term):**  
root_cause_compiler_v1.py reads from intelligence overlay directly. Hand-authored YAML is fully deprecated. Divergence between root_cause and Pass 3 is structurally impossible because root_cause is compiled from the same source.

**Standing requirement in the meantime:**  
Any change to root_cause YAML files for signals where a Pass 3 spec also exists must be flagged in the work package front matter as requiring cross-check against Pass 3. This is a governance note, not a schema enforcement. It must become a Sentinel guard in phase 2.

---

## 10. Health Systems Card Evidence Decision

Health Systems Cards must eventually receive the following from governed backend sources. The table below defines what the cards need, where the data should come from, and what is currently missing.

| Intelligence field | Cards need it for | Source in target architecture | Current state | Gap |
|---|---|---|---|---|
| **Per-marker role** (`score_contributor` / `confidence_support` / `context_marker` / `missing_for_confidence` / `optional_deeper`) | Distinguish which markers drove the score vs which add confidence vs which are optional | signal_library supporting_metrics.relationship_kind → backend translation layer → SubsystemEvidenceV1 per-marker role | `evidence_role` always null | **Highest priority gap** |
| **relationship_kind** (`mechanism`, `corroboration`, `severity`, `differential`, `exclusion`) | Show users why each marker is relevant to this signal | signal_library supporting_metrics.relationship_kind (v2.0.0 packages) | Not in pkg_s24_*; present in newer packages but not consumed | **Priority 1** |
| **Hypothesis framing** (rank 1 physiological_claim) | Show the most likely clinical interpretation context | intelligence_overlay ranked_hypotheses[0].physiological_claim | Not in any package; not surfaced anywhere in cards | **Medium-term** |
| **Contradiction alert** | Warn user that a specific marker on their panel changes the interpretation | intelligence_overlay contradiction_markers | Not in any package; not surfaced | **Medium-term** |
| **Missing-data policy** | Explain what additional markers would strengthen the interpretation | intelligence_overlay hypotheses[].missing_data.policy | Not surfaced; confidence tier is currently a coarse label without specific guidance | **Medium-term** |
| **Confirmatory tests** (card-level) | Show what would improve confidence in this specific interpretation | intelligence_overlay confirmatory_tests | Not in card DTO | **Medium-term** |
| **Evidence strength** | Grade the confidence behind each hypothesis | intelligence_overlay hypotheses[].evidence_strength | Not surfaced | **Long-term** |
| **Explanation prose** (mechanism/pathway) | Provide biological context sentence | signal_library explanation.mechanism → already loaded | Loaded into SignalResult but not routed to card DTO | **Near-term routing fix** |

**Short-form consumption rule for cards:**  
Cards must receive marker roles from the backend assembler reading governed package data. Cards must NOT infer roles from marker names, from scoring rail membership, or from frontend heuristics. If the role is not in a governed source, it is not shown.

---

## 11. Governance and Validation Implications

The following schemas, validators, compile checks, and Sentinel guards are required by the recommended architecture:

| Asset | Required governance item | Status |
|---|---|---|
| `signal_library.yaml` extended to v2.0.0 | `validate_signal_library.py` must enforce structured `supporting_metrics` objects when schema_version >= 2.0.0 | Schema spec exists; validator may need update for structured objects |
| intelligence_overlay (new) | New `intelligence_overlay_schema_v1.yaml` defining hypothesis_frames, contradiction_markers, confirmatory_tests, missing_data_policy | Does not exist yet |
| intelligence_overlay (new) | New `validate_intelligence_overlay.py` | Does not exist yet |
| Pass 3 → intelligence_overlay compile | Compile script must be deterministic and traceable (spec_id in overlay must cite source Pass 3 spec_id) | Does not exist yet |
| root_cause cross-check | Sentinel guard: if a signal has both a root_cause YAML and an intelligence overlay, flag divergence in physiological_claim | Does not exist yet |
| SubsystemEvidenceV1 extension | Schema change to `results.py` — add per-marker role field to included_markers rows | `evidence_role` exists at subsystem level (wrong granularity); per-marker role field at marker level needed |
| wave1_subsystem_evidence.py replacement | Regression tests must confirm that the new assembler produces identical included/missing partition results as the current hard-coded version | Test suite: `test_domain_ux1c_governed_subsystem_evidence.py` must be extended |
| IDL | When intelligence overlay prose reaches IDL, IDL must validate against its existing content boundaries | `RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md` governs this |

---

## 12. Migration Plan

### Immediate safety patches (do now, independent of architecture agreement)

**Patch 1 — total_bilirubin false-missing fix**  
Proposed work_id: `WAVE1-EQUIV1`  
Remove `total_bilirubin` from `_WAVE1_LIV_PROCESSING.expected_marker_ids` in `wave1_subsystem_evidence.py`. Expected set becomes `("alp", "albumin", "bilirubin")`. Update regression tests. This is a confirmed defect that should not wait for architecture decisions.  
Risk: LOW.

**Patch 2 — weak subsystem label corrections**  
Proposed work_id: `WAVE1-UX2`  
Rename `wave1_cv_vascular_strain` label from "Vascular strain context" to "Inflammation context". Add one-line copy explanation near liver domain completeness counter. This is a copy and label change only. Risk: LOW.

### Short-term bridge (after architecture agreed)

**Bridge 1 — signal_library v2.0.0 re-ingestion for pkg_s24_* packages**  
Re-ingest the pkg_s24_* packages (currently schema_version 1.0.0 with flat supporting_metrics) to carry structured supporting_metrics with `role`, `relationship_kind`, and `availability` populated from Pass 3.  
Risk: STANDARD-HIGH (touches 20+ pkg signal_library files; schema change requires validator update).  
Prerequisite: validate_signal_library.py updated to enforce structured supporting_metrics in v2.0.0.

**Bridge 2 — route explanation.* prose to domain card copy**  
The most immediately accessible Pass 3 content is already in signal_library (`explanation.mechanism`, `biological_pathway`, etc.). Route this through the assembler and DTO so that a biological mechanism sentence appears on the domain card. This is an assembler routing change, not a new schema.  
Risk: STANDARD (touches domain_score_assembler.py and ConsumerDomainScoreV1 DTO — IDL review required for any prose that reaches retail users).

### Medium-term architecture correction

**Medium 1 — intelligence overlay schema + compile**  
Define `intelligence_overlay_schema_v1.yaml`. Write `validate_intelligence_overlay.py`. Write a deterministic compile script from Pass 3 → intelligence overlay YAML, one file per primary signal. Review compiled content through IDL before marking any overlay as production-ready.  
Risk: HIGH (new KB asset type, new schema, new governance sprint). Must go through Automation Bus as HIGH.

**Medium 2 — replace wave1_subsystem_evidence.py assembler**  
Replace the hard-coded Python dict with a governed assembler that reads from signal_library (for relationship_kind per supporting_metric) and from intelligence overlay (for hypothesis framing and contradiction alerts). Extend SubsystemEvidenceV1 to carry per-marker role fields.  
Risk: HIGH (touches Intelligence Core adjacent layer; requires regression test suite coverage).

**Medium 3 — root_cause phase 2 transition**  
For signals with complete Pass 3 + intelligence overlay coverage, generate compiled root_cause YAML from intelligence overlay. Validate against existing hand-authored YAML. Replace hand-authored files under governance. Add Sentinel cross-check guard.  
Risk: STANDARD per signal batch.

### Long-term research-to-runtime pipeline

**Long 1 — root_cause_compiler_v1.py reads from intelligence overlay**  
Once intelligence overlay compilation is stable and validated for all 40 current root_cause signals, migrate root_cause_compiler to read from intelligence overlay directly. Retire hand-authored YAML.

**Long 2 — IDL receives structured inputs**  
IDL currently governs prose. Extend IDL to receive structured intelligence fields (hypothesis_id, physiological_claim, evidence_strength, contradiction_rationale) so it can gate interpretation quality, not just phrasing. This closes the final gap where IDL is a safety gate working on impoverished inputs.

---

## 13. Risks and Trade-offs

| Risk | Description | Mitigation |
|---|---|---|
| **Intelligence overlay becomes another duplicate authority** | If the intelligence overlay is introduced without a strict compile-from-Pass-3 requirement, teams will hand-author overlay files that diverge from Pass 3, creating a third independent hypothesis authority | Enforce: every intelligence overlay file must carry a `source_spec_ids[]` field citing the Pass 3 specs it was compiled from. Validator rejects overlay files without this traceability. Sentinel checks for drift. |
| **Signal_library v2.0.0 migration at scale** | Re-ingesting 20+ pkg_s24_* packages with structured supporting_metrics is a governed HIGH sprint. A schema error propagated across all files could break SignalEvaluator validation | Migrate in batches. Validate each batch before proceeding. Keep v1.0.0 files in place until v2.0.0 equivalents are validated. |
| **root_cause YAML and intelligence overlay divergence during transition** | During the transition phase, both hand-authored root_cause YAML and intelligence overlay will exist for the same signals | The Sentinel cross-check guard (§11) must be created before the intelligence overlay is compiled, not after. |
| **Evidence_role field ambiguity** | `SubsystemEvidenceV1.evidence_role` is currently at the subsystem level (one role string per subsystem). What is needed is per-marker role. Extending the wrong level would require a later breaking change | Extend `MarkerDisplayLabelV1` (not `SubsystemEvidenceV1.evidence_role`) with a `marker_role` field. The subsystem-level `evidence_role` field can then be deprecated or repurposed as a summary role. |
| **IDL prose from Pass 3 carries clinical risk if not reviewed** | Pass 3 narrative fields (`implications`, `interpretation`) may contain directive clinical language that does not meet HealthIQ's retail-safe framing standards | All Pass 3 narrative content must pass IDL review before routing to retail-facing DTOs. The intelligence overlay compile step must include an IDL-review gate, not just a schema validation gate. |
| **Product benefit is real but medium-term** | The full intelligence pipeline (marker roles + hypothesis framing + contradiction alerts) requires 3–5 governed work packages before it changes what users see | The immediate patches (total_bilirubin fix, subsystem label corrections) deliver user trust improvements in days. The architecture work delivers differentiation over months. Sequence accordingly. |
| **Two competing hypothesis authorities (Pass 3 and root_cause YAML) for ~25 signals** | Until phase 2 migration is complete, any clinical claim in root_cause YAML that contradicts Pass 3 is undetected | Sentinel guard for cross-check must be created as early as possible. Until then, any sprint that modifies root_cause YAML for a signal with Pass 3 coverage must include a manual cross-check step. |

---

## 14. Recommended Next Work Package

Architecture agreement must precede the following recommendation. Do not begin until this document has been reviewed and the target architecture confirmed.

**Recommended first work package after architecture agreement:**

| Field | Value |
|---|---|
| **Proposed work_id** | `KB-WAVE2-OVL1` or equivalent (KB SOP determines final ID) |
| **Title** | Intelligence overlay schema + compile pilot for 3 Wave 1 signals (HbA1c, CRP, ALT) |
| **Risk level** | HIGH (BEHAVIOUR/MIXED — introduces new KB asset type consumed by report/card assembly layer) |
| **Objective** | Define `intelligence_overlay_schema_v1.yaml`. Write `validate_intelligence_overlay.py`. Compile intelligence overlay YAML for 3 pilot signals from Pass 3 (hba1c_high, crp_high, alt_high). These 3 signals have complete Pass 3 coverage, active root_cause YAML, and direct Wave 1 card relevance. Review compiled content through IDL. Do NOT connect to assembler yet — compile only. |
| **Files likely touched** | `knowledge_bus/schema/intelligence_overlay_schema_v1.yaml` (new); `backend/scripts/validate_intelligence_overlay.py` (new); `knowledge_bus/intelligence_overlays/signal_hba1c_high_overlay.yaml` (new); `signal_crp_high_overlay.yaml` (new); `signal_alt_high_overlay.yaml` (new) |
| **What must not change** | `signal_evaluator.py`, `wave1_subsystem_evidence.py`, `root_cause_compiler_v1.py`, `results.py`, any existing pkg signal_library files, IDL content, frontend components |

**Rationale for HbA1c, CRP, ALT as pilots:**  
- HbA1c: two competing hypothesis frames (chronic hyperglycemia vs iron-deficiency bias) with direct clinical relevance to users; both exist in Pass 3; root_cause YAML only covers chronic hyperglycemia; CRP: strongest cross-system relevance (cardiovascular, liver, metabolic); most non-specific signal; highest risk if hypothesis framing is incorrect; best test of IDL review gate. ALT: 3 distinct Pass 3 specs (hepatocellular, metabolic/steatotic, muscle-source); differential framing is the primary product value; muscle-source differential is currently entirely absent.

**Preceding that work package, in the same sprint or a prior sprint:**

| Field | Value |
|---|---|
| **Proposed work_id** | `WAVE1-EQUIV1` (already specified in prior investigation) |
| **Title** | Fix total_bilirubin false-missing defect in wave1_subsystem_evidence.py |
| **Risk level** | LOW |
| **What it does** | Remove `total_bilirubin` from `_WAVE1_LIV_PROCESSING.expected_marker_ids`; update tests |

---

## 15. STOP Conditions

The following changes must not be made until the architecture described in this document is reviewed and agreed:

1. **Do not load Pass 3 JSON files at runtime.** Pass 3 is a KB compile-time source. Loading raw research JSON in the analytical pipeline violates Layer B determinism, creates an uncontrolled schema coupling, and bypasses all KB governance.

2. **Do not infer marker roles in `wave1_subsystem_evidence.py` from scoring rail membership or string matching.** If LDL is on the scoring rail, it is a score contributor — but that inference must come from a governed backend translation layer, not from a Python conditional inside the assembler. Roles must come from governed package data or from the intelligence overlay.

3. **Do not add Pass 3 narrative prose to domain card DTO fields (`consequence_sentence`, `headline_sentence`) without IDL review.** Pass 3 `narrative.implications` contains clinical language written for research framing, not retail consumer safety. Routing it directly to retail copy bypasses IDL governance.

4. **Do not create a new hand-authored role mapping file or a manually maintained card_evidence YAML.** Every new "authority" that is not compiled from Pass 3 is a new duplicate. There are already too many.

5. **Do not treat Pass 3 hypothesis frames and root_cause hypothesis YAML as equivalent.** The schemas are incompatible (`physiological_claim` ≠ `summary_template`; Pass 3 has `contradiction_markers`, root_cause v1 does not). A governed translation sprint is required before Pass 3 hypothesis frames can be processed by `root_cause_compiler_v1.py`.

6. **Do not stuff the full hypothesis graph into signal_library.yaml.** The signal_library is the activation and signal-semantics authority. Adding ranked hypotheses with contradiction graphs, missing-data policies, and confirmatory tests to signal_library schema creates an unmaintainable file that mixes evaluation logic with interpretive intelligence.

7. **Do not extend SubsystemEvidenceV1.evidence_role (subsystem-level field) for per-marker roles.** The existing `evidence_role` field is at the wrong granularity — one string per subsystem, not one role per marker. Extending this field would require a subsequent breaking change. Per-marker roles must be added to `MarkerDisplayLabelV1` as a `marker_role` optional field.

8. **Do not begin intelligence overlay compilation without an agreed schema and validator.** Compiling overlay files before the schema is locked will produce unvalidated assets that cannot be governed or Sentinel-guarded.

9. **Do not allow the intelligence overlay to be hand-authored for any signal that has a complete Pass 3 spec.** Hand-authored overlays for signals with Pass 3 coverage create a third independent hypothesis authority. The overlay must be compiled from Pass 3 for those signals.

10. **Do not modify the root_cause_compiler_v1.py to read from intelligence overlay until the overlay has been compiled, validated, IDL-reviewed, and approved for at minimum 10 signals.** Switching the live root-cause compiler to a new asset before sufficient overlay coverage exists would break the WHY layer for most signals.

---

*End of ARCH-R1 review. No repository code modified.*
