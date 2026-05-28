# Pass 3 Research Asset Utilisation Investigation

**Date:** 2026-05-28  
**Scope:** Investigation only — no code, package, or runtime changes.  
**Corpus:** 9 `*_Pass_3.json` files (153 investigation specs) under `knowledge_bus/research/investigation_specs/multi_llm_research/`, compared to `knowledge_bus/packages/**`, governed schemas, and Wave 1 Health Systems Card runtime paths.

---

## 1. Executive verdict

**HealthIQ is only partially using Pass 3 research assets.**

| Layer | Utilisation | Summary |
|---|---|---|
| **Pass 3 → packages** | **Moderate (signal logic); weak (hypothesis graph)** | ~132 packages cite Pass 3 lineage. KB-S52* ingestion preserves activation, structured `supporting_metrics` (role, rationale, availability), override rules, `research_brief`, and `signal_library.explanation` (from Pass 3 `narrative`). **Hypotheses, contradiction markers, confirmatory tests, hypothesis ranking, and `relationship_kind` are not carried into standard packages.** |
| **Packages → runtime** | **Partial** | `SignalEvaluator` uses thresholds, lab-range activation, override rules, and flat `output.supporting_markers` for confidence only. **`supporting_metrics[].role` / `rationale` and `explanation.*` are loaded into `SignalResult` but not consumed by Health Systems Cards, subsystem evidence, IDL, or `report_compiler_v1` top findings.** |
| **Health Systems Cards** | **Weak vs Pass 3** | Subsystem evidence is a **hard-coded marker checklist** (`wave1_subsystem_evidence.py`), not package- or Pass-3-derived. **`evidence_role` is always `null`.** No per-marker roles, rationales, hypotheses, or narrative mechanism text on cards. |

**Bottom line:** Pass 3 is the richest authoritative research layer, but the product path for Wave 1 cards stops at coarse subsystem inclusion/missing lists. The “wow” content (ranked hypotheses, contradiction logic, missing-data policy, per-marker relationship semantics) exists in-repo but is largely **offline** relative to Health Systems Cards.

---

## 2. Pass 3 asset inventory

### 2.1 Corpus

| File | Spec count |
|---|---|
| `Batch_3_Pass_3.json` | 26 |
| `Batch_4_Pass_3.json` | 23 |
| `Batch_5_Pass_3.json` | 28 |
| `Batch_6_Pass_3.json` | 24 |
| `Batch_7_Pass_3.json` | 16 |
| `cbc_hematology_pass_3.json` | 22 |
| `lipid_derived_pass_3.json` | 7 |
| `thyroid_antibodies_pass_3.json` | 4 |
| `transferrin_pass_3.json` | 3 |
| **Total** | **153** |

Contract version: `investigation_spec_contract_version: 3.0.0` on all specs.

### 2.2 Recurring structured fields (153/153 specs unless noted)

| Field group | Presence | Role |
|---|---|---|
| `primary_marker` (`biomarker_id`, `rationale`, `signal_system`) | 100% | Primary trigger + consumer-safe framing |
| `trigger_direction` | 100% | high / low governance |
| `activation` + `states` | 100% | lab-range activation, baseline/escalation |
| `supporting_markers[]` | 100% | Per-marker: `biomarker_id`, `expected_direction`, **`role`**, **`relationship_kind`**, `availability`, **`rationale`** |
| `hypotheses[]` | 100% | Ranked frames: `hypothesis_id`, `rank`, **`physiological_claim`**, `evidence_strength`, `caveats[]`, **`missing_data.policy`**, `supporting_marker_refs[]`, **`contradiction_markers[]`** |
| `hypothesis_ranking` | 100% | Ordered hypothesis ids |
| `confirmatory_tests[]` | 100% | `test_id`, `rationale` |
| `override_rules[]` | 100% | Escalation logic + `source_refs` |
| `evidence` | 100% | `evidence_strength`, `sources[]`, `physiological_claim`, `threshold_notes` |
| `narrative` | 100% | `mechanism`, `biological_pathway`, `interpretation`, `implications`, **`supporting_marker_roles`** (prose) |

**Note:** `relationship_kind` values observed: `corroboration`, `mechanism`, `differential` (aligned with investigation-spec v3 enums).

### 2.3 Example richness (CRP — not fully ingested as Pass 3 packages)

`Batch_4_Pass_3.json` contains dedicated specs `inv_crp_high_active_inflammatory_or_infective_state` and `inv_crp_high_residual_cardiometabolic_inflammatory_risk` with neutrophil/ferritin/procalcitonin roles, ranked hypotheses, and contradiction markers. **No `pkg_kb*` package manifest references these spec ids.** Runtime `signal_crp_high` comes from legacy `pkg_s24_crp_high_inflammation` (pre–Pass 3 `inv_crp_high_inflammation_v1.yaml`).

---

## 3. Package propagation audit

**Package estate (signal libraries):** 186 packages; **142** at `library.schema_version: 2.0.0`; **132** manifests cite Pass 3 / `pass_3` as `source_document`.

| Pass 3 field | Present in pkg files? | Where? | Preserved fully/partially/lost? | Notes |
|---|---|---|---|---|
| `primary_marker` + `trigger_direction` | Yes | `signal_library.signals[].primary_metric`, `trigger_direction`, `description` | **Partial** | `rationale` often folded into `description`; `signal_system` → `system` |
| `supporting_markers[]` (structured) | Yes (2.0.0 pkgs) | `signal_library.supporting_metrics[]` | **Partial** | `role`, `expected_direction`, `availability`, `rationale` preserved; **`relationship_kind` lost** in `signal_library` |
| `relationship_kind` | Rarely | `promoted_signal_intelligence.yaml` (subset, e.g. `pkg_kb47_*`) | **Lost** for standard path | Not in `signal_library_schema`; loader **not called** in production pipeline |
| `hypotheses[]` | No | — | **Lost** | Not in package schema |
| `hypothesis_ranking` | No | — | **Lost** | — |
| `contradiction_markers` | No | — | **Lost** | — |
| `missing_data.policy` | No | — | **Lost** | Separate **`knowledge_bus/root_cause/hypotheses/*`** for ~40 signals (hand-authored v1, not Pass 3 compile-through) |
| `confirmatory_tests[]` | No | — | **Lost** from pkg | Governed registry `confirmatory_tests_v1.yaml` used by **root-cause compiler**, not ingested from Pass 3 |
| `override_rules` | Yes | `signal_library.override_rules` | **Mostly full** | 2.0.0 requires `source_refs` → `research_brief.sources` |
| `evidence.sources` | Yes | `research_brief.yaml` `sources[]` | **Full** (citation layer) | `source_id`, title, journal, year |
| `evidence.physiological_claim` | Yes | `research_brief.physiological_claim` | **Partial** | Often first-rank hypothesis claim, not all ranked claims |
| `evidence.evidence_strength` | Yes | `research_brief.evidence_strength` | **Partial** | Single strength per package, not per-hypothesis |
| `narrative.*` | Yes | `signal_library.explanation.*` | **Mostly full** | Maps `narrative.mechanism` → `explanation.mechanism`, etc.; `supporting_marker_roles` → `explanation.supporting_marker_roles` |
| `narrative` (standalone block) | No | — | **Merged** into `explanation` | — |
| `activation` / `states` | Yes | `activation_logic`, `activation_config`, threshold severities | **Full** for evaluation | — |
| Duplicate `signal_id` across specs | N/A | Multiple packages / duplicate overwrite | **Lossy** | e.g. three `signal_alt_high` Pass 3 specs → three packages; **evaluator keeps lexicographically last path** per `signal_id` |

**Legacy 1.0.0 packages (44):** flat `supporting_metrics` string lists (e.g. `pkg_s24_crp_high_inflammation`, `pkg_inflammation_crp_context`) — **no per-marker role/rationale** at package level.

---

## 4. Runtime utilisation audit

| Field / concept | Runtime-used? | File/path | Used for what? | Gap |
|---|---|---|---|---|
| Pass 3 JSON directly | **No** | — | Not loaded at runtime | Research/archive + ingest source only |
| `signal_library` activation + overrides | **Yes** | `backend/core/analytics/signal_evaluator.py` | Fires signals, states, confidence inputs | Not surfaced on Health Systems Cards |
| `supporting_metrics[].role` / `rationale` | **No** | Loaded in YAML only | — | Roles not in `SignalResult` model |
| `relationship_kind` | **No** | — | — | Not in evaluator or DTOs |
| `explanation.*` | **Stored only** | `SignalResult.explanation` in evaluator output → `insight_graph.signal_results` | Serialized in graph; **no Health Systems / report consumer** | Rich text never shown on Wave 1 cards |
| `output.supporting_markers` (flat ids) | **Yes** | `signal_evaluator.py`, `interpretation_display_layer_publish_v1.py` | Confidence + IDL supporting summary (humanized names) | No role-specific copy |
| `research_brief` | **No** (direct) | Validators / lifecycle only | Package promotion gate | Not in analysis DTO |
| `hypotheses` (Pass 3) | **No** | — | — | — |
| Root-cause `hypotheses/*.yaml` | **Yes** (subset) | `root_cause_compiler_v1.py`, `report_compiler_v1.py` | Layer C / narrative report hypotheses | **Separate asset** from Pass 3; limited coverage vs 153 specs |
| `assemble_wave1_subsystem_evidence` | **Yes** | `wave1_subsystem_evidence.py` → `domain_score_assembler.py` | Included/missing marker lists per subsystem | **Manual map**, not package-driven |
| `SubsystemEvidenceV1.evidence_role` | **Always null** | `wave1_subsystem_evidence.py` | Reserved field | Pass 3 roles never populated |
| `ConsumerDomainScoreV1` narrative | **Yes** | `domain_narrative_wave1.py`, IDL registry | Headlines, anchors, next steps | **IDL/static**, not Pass 3 per-marker evidence |
| `promoted_signal_intelligence.yaml` | **No** | `load_promoted_signal_intelligence.py` (tests only) | — | Contains `relationship_kind` for KB47 tranche but unused in pipeline |
| Frontend subsystem UI | **Partial** | `Wave1SubsystemEvidenceSection.tsx` | Labels for included/missing markers | No rationale, roles, or mechanism |

---

## 5. Health Systems Card opportunity analysis

Wave 1 cards today combine: **scoring rail score**, **IDL-driven sentences**, **active signal ids**, and **subsystem checklists**. Pass 3 could materially upgrade:

| Pass 3 asset | Card / subsystem opportunity | Current state |
|---|---|---|
| **Marker roles** (`corroborator`, `mechanism_marker`, `differential_marker`) | Tag each included marker in a subsystem (e.g. CRP = “inflammatory context” under vascular strain) | Only flat chip list |
| **`relationship_kind`** | Drive icon/copy: corroboration vs mechanism vs differential | Not in packages (standard) or UI |
| **Per-marker `rationale`** | Tooltip or expand row under subsystem | Lost at UI; partially in pkg 2.0.0 only |
| **Hypothesis ranking** | “Most likely read” vs “alternative read” on expanded card | Not compiled to runtime for cards |
| **`physiological_claim`** | Evidence anchor / contributor sentences per subsystem | IDL uses static phenotype copy |
| **`contradiction_markers`** | “Why we’re not over-calling X” — trust builder | Absent |
| **`missing_data.policy`** | Governed copy when markers missing (vs “Not uploaded” only) | Generic missing chips |
| **`confirmatory_tests`** | Actionable next-step panel | Root-cause path only; not subsystem |
| **`narrative` mechanism / pathway / interpretation / implications** | Expanded subsystem or card body | In `explanation` on signals but **not wired to frontend** |
| **`supporting_marker_roles`** (prose) | Single subsystem summary paragraph | Available in pkg `explanation` but unused |

### 5.1 Marker examples vs current subsystem evidence

| Marker / context | Pass 3 richness | Current Health Systems Card |
|---|---|---|
| **CRP** (vascular / inflammatory) | Batch 4: acute vs cardiometabolic residual frames; ferritin/neutrophil/procalcitonin; contradictions | Subsystem lists `crp` only; signal from **legacy** `pkg_s24_crp_high_inflammation` (WBC/neutrophil overrides, no Pass 3 hypotheses) |
| **Homocysteine** | Batch 6: B12/folate/mcv mechanisms + renal clearance spec; ranked hypotheses | Subsystem shows `homocysteine` chip only; `signal_homocysteine_high` may **overwrite** across packages; root-cause uses separate `hcy_hypotheses_v1.yaml` |
| **Triglycerides** (metabolic / CV) | Multiple specs (HbA1c IR context, HDL patterns, ALT steatosis corroborator) | Listed under lipid transport + insulin subsystem; **no IR mechanism copy** on card |
| **ALT / AST / GGT / ALP / albumin / bilirubin** | Batch 5: hepatocellular vs steatotic vs muscle-source **distinct Pass 3 specs** with CK/ALP contradictions | Liver subsystems are marker buckets only; **three `signal_alt_high` packages compete** at evaluator; no hypothesis/contradiction UX |
| **HbA1c / glucose / insulin** | Batch 3/6/7: glycation bias, IR pattern, confirmatory repeat testing | Glycaemic subsystem + insulin context chips; rich Pass 3 in `pkg_kb52d_hba1c_pct_*` **not shown** on card |

---

## 6. Examples of underused research richness

| Missed asset | Example | Current UI weakness | Potential product value |
|---|---|---|---|
| Ranked hypotheses | `inv_alt_high_hepatocellular_injury_pattern` (Batch 5) | Liver card shows ALT present, not *why* vs muscle source | “Most consistent with hepatocellular injury; CK elevation would shift read” |
| Contradiction markers | CRP + normal neutrophils (Batch 4 `inv_crp_high_active_*`) | High CRP may feel alarming without nuance | Reduces false alarm; builds clinical credibility |
| `missing_data.policy` | HbA1c + low hemoglobin bias spec (Batch 3) | Missing markers = “Not uploaded” only | “If hemoglobin not available, HbA1c may overstate glycaemia” |
| `relationship_kind` + rationale | Triglycerides as `mechanism_marker` for HbA1c IR (Batch 3) | TG appears in two subsystems as anonymous chip | Explains *role* in glycaemic vs lipid story |
| `supporting_marker_roles` prose | Homocysteine pkg `explanation.supporting_marker_roles` | Not rendered anywhere in results UI | One-sentence “how markers work together” under subsystem |
| Dedicated Pass 3 CRP specs | `inv_crp_high_residual_cardiometabolic_inflammatory_risk` | Vascular subsystem only lists CRP | Links CRP to cardiometabolic context on CV card |
| Multi-spec `signal_alt_high` | Steatotic vs hepatocellular vs exertional | Single evaluator winner; card unaware of alternates | Pattern-specific liver narrative when expanded |
| Confirmatory tests | Pass 3 `ct_repeat_hba1c_with_glucose_confirmation` | Not on Wave 1 card next steps | Clear, governed follow-up suggestions |

---

## 7. Architecture options

| Option | Description | Pros | Cons | Risk | Recommendation |
|---|---|---|---|---|---|
| **A. Packages only** | Continue current ingest; improve UI from existing `signal_library` | Minimal schema churn; uses promoted assets | Cannot recover lost Pass 3 fields without re-ingest; subsystem still manual | Low | **Insufficient** for subsystem/role goals |
| **B. Extend packages** | Add governed fields to `signal_library` / new `subsystem_evidence.yaml` per domain | Single runtime authority; validators enforce shape | Large ingest/backfill; duplicate `signal_id` policy needed | Medium | **Recommended direction** if staying package-centric |
| **C. Compile Pass 3 → runtime evidence layer** | New governed DTO compiled from Pass 3 (or extended pkg) for cards only | Preserves hypotheses/contradictions; clear provenance | New contract + pipeline stage; must not fork narrative authority | Medium–High | **Best for “wow”** if hypotheses/contradictions required on cards |
| **D. Pass 3 reference only** | Keep Pass 3 for research QA | Zero runtime risk | No product gain | None | **Reject** given sprint goals |
| **E. Hybrid (B + selective C)** | Extend 2.0.0 packages for roles/rationale; compile hypothesis subgraph to `root_cause` or card DTO | Phased delivery; reuses root-cause compiler patterns | Two paths to keep aligned | Medium | **Pragmatic sprint default** |

**Recommended architecture: E (Hybrid), trending to B with a card-facing compile artifact.**

Principles:
1. **Do not** read raw Pass 3 JSON in production orchestrator.
2. **Extend** governed package contract (or a single `wave1_subsystem_evidence_v2.yaml` compiled from Pass 3) for roles, rationales, and subsystem copy.
3. **Keep** `SignalEvaluator` deterministic; separate **display compile** from **fire logic**.
4. Align duplicate `signal_id` policy (disambiguate package signals or namespace by `spec_id`).

---

## 8. Recommended next work package

| Attribute | Proposal |
|---|---|
| **work_id** | `DOMAIN-UX1D-pass3-subsystem-evidence-compile` (or `KB-S63-pass3-card-evidence-ingest`) |
| **Risk level** | **Medium** — touches `knowledge_bus/` ingest contract and `backend/core/analytics/wave1_subsystem_evidence.py` + DTO; **not** signal firing logic if scoped correctly |
| **Files likely touched** | `knowledge_bus/schema/signal_library_schema.yaml` (or new `wave1_subsystem_evidence_schema_v1.yaml`), selected `knowledge_bus/packages/pkg_kb52*/signal_library.yaml` (ingest regeneration), `backend/core/analytics/wave1_subsystem_evidence.py`, `backend/core/models/results.py` (`SubsystemEvidenceV1`), `backend/core/analytics/domain_score_assembler.py`, `frontend/app/components/results/Wave1SubsystemEvidenceSection.tsx`, `frontend/app/types/analysis.ts`, regression tests under `backend/tests/regression/test_domain_ux1c_*` |
| **Implementation principle** | **Compile once, serve many:** deterministic build step maps Pass 3 (or 2.0.0 pkg) → governed subsystem rows with `marker_id`, `display_role`, `relationship_kind`, `rationale_short`, optional `subsystem_summary` from `explanation.supporting_marker_roles`. Wave 1 cards **read compiled artifact only** at runtime. |
| **What must not change** | Scoring rails, cluster engines, signal activation thresholds, IDL phenotype registry semantics, medical claims without governance review, frontend-invented narrative |

**Phased acceptance criteria:**
1. At least one Wave 1 subsystem (e.g. `wave1_cv_vascular_strain`) shows role + rationale for CRP when present.
2. `evidence_role` populated from governed compile (never frontend-guessed).
3. No new runtime dependency on raw `*_Pass_3.json`.
4. Documented duplicate-`signal_id` handling for homocysteine/ALT families.

---

## 9. STOP conditions

Do **not** implement the following without explicit governance / medical review:

1. **Loading `*_Pass_3.json` directly in the orchestrator** — bypasses package validation and remap contracts (e.g. KB-S52B `fasting_glucose→glucose`).
2. **Frontend-authored marker roles or mechanism text** — violates Intelligence Core / AGENTS.md frontend-shell rules.
3. **Surfacing all ranked hypotheses on retail cards without safety filtering** — hypothesis count and contradiction strength need governed templates.
4. **Collapsing duplicate `signal_id` packages silently** without product decision — current lexicographic overwrite hides alternate Pass 3 frames (ALT, homocysteine, HbA1c).
5. **Replacing root-cause hypothesis YAML with ad-hoc Pass 3 paste** — two authorities will diverge; require single compile pipeline.
6. **Using `promoted_signal_intelligence` in production without schema + loader wiring** — today it is validation/test-only.
7. **Expanding subsystem maps by manual hard-coding only** — reproduces today’s thin evidence without using existing pkg `explanation` / Pass 3 compile.

---

## Appendix A — Key code references

Subsystem assembly (manual map, `evidence_role=None`):

```159:170:backend/core/analytics/wave1_subsystem_evidence.py
        rows.append(
            SubsystemEvidenceV1(
                subsystem_id=spec.subsystem_id,
                subsystem_label=spec.subsystem_label,
                included_marker_ids=included,
                missing_marker_ids=missing,
                included_markers=_labels_for_marker_ids(included),
                missing_markers=_labels_for_marker_ids(missing),
                status_label=None,
                evidence_role=None,
                source_trace=spec.source_trace,
            )
        )
```

Signal evaluator stores `explanation` but does not use roles from `supporting_metrics`:

```431:465:backend/core/analytics/signal_evaluator.py
            output = signal.get("output", {})
            supporting_markers = []
            if isinstance(output, dict) and isinstance(output.get("supporting_markers"), list):
                supporting_markers = [str(x) for x in output["supporting_markers"] if str(x).strip()]
            explanation = signal.get("explanation")
            if not isinstance(explanation, dict):
                explanation = None
            ...
            result = SignalResult(
                ...
                supporting_markers=supporting_markers,
                explanation=explanation,
            )
```

Pass 3 → package example (HbA1c): hypotheses remain in JSON only; narrative maps to `explanation`:

```82:91:knowledge_bus/packages/pkg_kb52d_hba1c_pct_high_chronic_hyperglycemia_diabetes/signal_library.yaml
  explanation:
    mechanism: HbA1c rises as hemoglobin is exposed to higher average glucose concentrations over
      erythrocyte lifespan.
    ...
    supporting_marker_roles: Glucose corroborates glycemia, triglycerides provide metabolic context,
      and hemoglobin helps detect red-cell conditions that can bias HbA1c.
```

---

## Appendix B — Role authority assessment

| Question | Assessment |
|---|---|
| Should Pass 3 `role` + `relationship_kind` + `rationale` feed card roles? | **Yes** — semantically aligned with `signal_library.supporting_metrics` (2.0.0) but **`relationship_kind` must be added to governed schema** or compiled from Pass 3. |
| Do packages preserve enough alone? | **Partial** — 2.0.0 has role + rationale; missing relationship_kind, hypotheses, contradictions. 1.0.0 legacy pkgs still in production mix. |
| Return to Pass 3 as runtime authority? | **No** — use Pass 3 as **compile source**, packages as **runtime authority**. |
| New runtime evidence DTO? | **Optional but valuable** — extend `SubsystemEvidenceV1` with governed marker-role rows rather than overloading `SignalResult`. |

---

*End of investigation.*
