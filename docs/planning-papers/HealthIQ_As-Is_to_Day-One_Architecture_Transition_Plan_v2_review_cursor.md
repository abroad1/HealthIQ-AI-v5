# Second-Pass Architecture Review: As-Is to Day-One Transition Plan v2

**Document reviewed:** `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan_v2.md`  
**Reviewer:** Cursor  
**Date:** 2026-05-28  
**Prior review:** `ARCH-R1_transition_plan_architecture_review_cursor.md`  
**Verdict on WP readiness:** **Conditionally yes** — v2 is accurate enough to **author formal Automation Bus work packages for Phase 0–1 only**. Do **not** author implementation WPs (WP3+) until **ARCH-RT-1** closes the identity/registry decision and Phase 0 inventory names concrete pilots.

---

## Executive summary

v2 is a **material improvement** over v1. It correctly absorbs ADR-008, stops proposing a duplicate signal-intelligence schema, separates hypothesis and card artefacts, defers `activation_key` to an explicit decision, and sequences PSI gap closure before greenfield layers.

**The strategic route to day-one architecture is correct and launch-appropriate.**

Remaining gaps are **operational and codebase-specific**, not directional:

1. **`signal_id + spec_id` alone cannot fix multi-frame collapse** without registry and `SignalResult` contract changes — v2 is right to defer `activation_key`, but WP1 must not leave the decision ambiguous.
2. **No `source_spec_id` in package manifests today** — only `source_document` paths; provenance must be schema + compile enforced.
3. **PSI loader exists but is not in the orchestrator** — Phase 2 must treat “runtime consumption” as net-new wiring, not validation-only.
4. **Only PSI translator exists** — there is no governed `investigation_spec → signal_library` compiler yet; activation packages still come from sprint ingest scripts.
5. **WP7 (runtime shadow integration) is too broad** for one Automation Bus package.

**Bottom line:** Convert **WP0** and **WP1** to formal work packages now. Hold **WP2–WP9** until WP1 deliverables and Phase 0 inventory exist.

---

## 1. Does v2 correctly reflect PSI / ADR-008?

**Yes — substantially correct.**

| v2 claim | Codebase ground truth |
|---|---|
| PSI schema + translator exist | `promoted_signal_intelligence_schema_v1.yaml`, `investigation_spec_to_promoted_signal.py`, `signal_intelligence_translation_rules_v1.yaml` (LOCKED) |
| PSI excludes hypotheses/narrative | ADR-008 + schema `forbidden_root_keys`; translator docstring |
| PSI opt-in via manifest | `package_manifest.promoted_signal_intelligence`; ~20 `pkg_kb47_*` packages |
| PSI not production-consumed | `load_promoted_signal_intelligence_for_package` used in **validators/tests only** — **not** referenced from `orchestrator.py` or `signal_evaluator.py` |
| Do not create duplicate signal-intelligence artefact | Correct — aligns with KB-S52B translation contract |

**Minor inaccuracies to fix in v2 text (not blocking):**

- **§2.2 package generations:** v2 implies `pkg_s24_*` are the newer governed Pass 3 line. In practice **`pkg_kb52*` / `pkg_kb52d*` / `pkg_kb58*`** cite `*_Pass_3.json`; many **`pkg_s24_*`** are older translation tranches (e.g. CRP still on `inv_crp_high_inflammation_v1.yaml`). Inventory should classify by **manifest `source_document` + schema_version**, not prefix alone.
- **§2.3 “relationship_kind in PSI”:** Correct per translation rules; **not** in `signal_library` 2.0.0 supporting_metrics schema — v2 should state both layers explicitly.

---

## 2. Is accepting ADR-008 the right decision?

**Yes. Do not reverse without a new ADR and full estate impact analysis.**

Reasons:

1. **Separation of concerns is sound:** firing logic (packages), signal-layer semantics (PSI), WHY graphs (hypotheses), UX projection (card evidence), retail safety (IDL) are different change velocities and validators.
2. **Reversal would bloat `signal_library`** and recreate the lossy single-file translation the audits documented.
3. **ADR-008 already names the missing piece:** “adjacent hypothesis assets” — v2’s **compiled hypothesis artefact** is the correct completion of that ADR, not a contradiction.

**When reversal might be considered (not recommended now):**

- If the team refuses to maintain a hypothesis compile pipeline and wants one package file per spec. That trades architectural clarity for ingest convenience and will fail at scale (153+ specs, multi-frame collisions).

**WP1 should record:** ADR-008 **accepted**; ADR-RT-003 defines hypothesis artefact as ADR-008 completion.

---

## 3. Is the artefact split correct?

**Yes. This is the correct day-one decomposition.**

| Artefact | Role | Verdict |
|---|---|---|
| **Packages (`signal_library` + `research_brief`)** | Signal **activation** / firing | Correct — `SignalRegistry` + `SignalEvaluator` already authoritative here |
| **PSI** | Signal-layer semantics (`relationship_kind`, supporting marker roles/rationales, contradiction roll-ups per PSI rules) | Correct — but must be **loaded at runtime** after Phase 2/8 |
| **Compiled hypothesis artefact** | WHY / root-cause input | Correct — cannot be PSI; root-cause uses `evidence_for_rules` shape today |
| **Health Systems Card evidence artefact** | UX projection (subsystem, visibility, card roles) | Correct — must not live in Python `WAVE1_DOMAIN_SUBSYSTEM_DEFS` long term |
| **IDL** | Presentation safety | Correct — already drives headlines via `domain_narrative_wave1` + IDL publisher |

**Join rule at runtime (v2 should add explicitly):**

```text
fired frame identity → activation package row (firing)
                    → PSI row (semantics, if manifest opts in)
                    → hypothesis artefact row(s) (WHY, by spec_id)
                    → card evidence row(s) (subsystem placement, by domain policy)
                    → IDL (retail wording for phenotype-level copy)
```

**Open design question in v2 (§4.4) is the right one:** direct consumption by `root_cause_compiler_v1` vs intermediate root-cause-shaped YAML. **Recommendation:** compiled hypothesis artefact as **canonical**; optional **thin compile** to existing root-cause YAML shape for one transition release, then delete hand YAML.

---

## 4. Is `activation_key` required, or can `signal_id + spec_id` suffice?

**`signal_id + spec_id` is necessary but not sufficient with the current codebase.**

Today:

- `SignalRegistry._load()` keys **`signals_by_id[signal_id]`** only; duplicates → lexicographic path overwrite (`signal_evaluator.py` lines 54–63).
- `SignalResult` has **`signal_id` only** — no `spec_id`, no `source_spec_id`, no `activation_key` (`backend/core/models/signal.py`).
- `compile_root_cause_v1` matches findings by **`signal_id`** on fired rows (`root_cause_compiler_v1.py` ~423–424).
- `interaction_map_v1.yaml` edges use **`signal_id`** only.
- `root_cause_registry_v1` registers targets by **`signal_id`** (duplicate `signal_id` entries forbidden; two homocysteine entries are **different** signal_ids sharing one YAML file).

**What `spec_id` alone solves:**

- Compile provenance in manifests and compile manifests.
- Hypothesis artefact indexing.
- Card evidence provenance.

**What `spec_id` does not solve without code changes:**

- Which of three `signal_alt_high` packages fires.
- Which activation thresholds/overrides apply when packages disagree.
- Which PSI document attaches to a fired result.

**Decision recommendation for ARCH-RT-1:**

| Option | Description | Fit |
|---|---|---|
| **A. `activation_key = spec_id`** | Registry keyed by `spec_id`; `signal_id` retained for interaction map grouping | **Preferred** — stable, 1:1 with investigation spec |
| B. `activation_key = f"{signal_id}::{spec_id}"` | Explicit composite | Acceptable if signal_id must remain primary in logs |
| C. Unique `signal_id` per spec | e.g. `signal_alt_high_hepatocellular` | **Avoid** — breaks interaction map, root-cause registry, golden fixtures |
| D. `signal_id + spec_id` without new key | Store spec_id on `SignalResult` only; registry still collapses | **Insufficient** |

**Conclusion:** Plan v2 is right not to assume `activation_key` upfront, but WP1 **must not** approve full regeneration on “spec_id in manifest only.” Either introduce **`activation_key` (recommended: equal to `spec_id`)** or **unique signal_ids per spec** with a governed interaction-map migration.

---

## 5. What must change in `SignalRegistry` to stop silent collapse?

**Minimum change set (behavioural, HIGH risk):**

1. **Registry key**
   - Replace `signals_by_id: Dict[str, Dict]` with `signals_by_activation_key: Dict[str, Dict]` where `activation_key` comes from package manifest or signal row (`source_spec_id` / `spec_id`).
   - Maintain optional index `signal_id → List[activation_key]` for interaction-map consumers.

2. **Load policy**
   - **Forbid** silent overwrite: on duplicate `activation_key`, **fail closed at load** (validator + registry) or emit structured conflict report at compile time.
   - On duplicate `signal_id` across different `activation_key`s: **allowed** in target state.

3. **`SignalEvaluator.evaluate_all`**
   - Evaluate **every** activation entry (or every entry whose primary metric is on panel).
   - Emit **one `SignalResult` per fired activation_key**, each carrying:
     - `activation_key`
     - `signal_id` (family)
     - `source_spec_id`
     - `package_id` / `_source_path` (provenance)

4. **Version hash**
   - `SignalRegistry.version` / `package_hash` must incorporate **activation_key** set, not `signal_id` set only — or InsightGraph replay stamps become misleading.

5. **Downstream consumers (must be enumerated in WP1 blast-radius)**
   - `signal_interaction_builder.py` — may need to map edges to families or to specific activation_keys.
   - `report_compiler_v1` top findings — today sorts by `signal_id`.
   - `root_cause_compiler_v1` — should key findings by **`source_spec_id` or `activation_key`**, not `signal_id` alone.
   - `interpretation_display_layer_publish_v1` — phenotype `required_signals` lists use `signal_id`.
   - Golden / persisted fixtures under `backend/tests/fixtures/persisted_results/`.

6. **Validators**
   - `validate_knowledge_package.py`: require **`source_spec_id`** (or `spec_id`) per package; enforce unique `activation_key` across estate.
   - Compile-time collision report before promotion.

**Sentinel:** `signal_registry_silent_signal_id_collapse_forbidden` — static test that fails if `_load` still uses last-path-wins on `signal_id` only.

---

## 6. Correct transition path for `root_cause_registry_v1.py`

**Current state (accurate in v2):**

- `ROOT_CAUSE_TARGET_SPECS`: frozen tuple of `(signal_id, loader, asset_filename)` — **manual**, LC-S18 hybrid, **no auto-discovery**.
- Loaders in `load_root_cause_hypotheses.py` read hand YAML from `knowledge_bus/root_cause/hypotheses/`.
- Compiler: for each target `signal_id`, find fired row with **exact** `signal_id` match; load hypotheses via loader.

**Target transition (phased):**

| Phase | Registry | Compiler input |
|---|---|---|
| **T0 (now–inventory)** | Manual tuple unchanged | Hand YAML |
| **T1 (hypothesis pilot)** | Add **parallel** entries pointing at compiled artefact loader for 1–2 pilots; keep manual for rest | A/B: hand vs compiled for same `signal_id` in shadow |
| **T2 (generated registry)** | Replace tuple with **`root_cause_registry_v1.yaml`** generated from compile index: `activation_key` → artefact path + `signal_id` family | Compiler loads compiled artefact by key |
| **T3 (retire)** | Remove manual loaders; `validate_root_cause_registry` ensures every target has compiled artefact + hash | Hand YAML archived |

**Critical registry design choices for WP1 / WP6:**

1. **Registry key should migrate from `signal_id` to `activation_key`** (or `(signal_id, source_spec_id)`), matching §5. Homocysteine’s two signal_ids (`signal_homocysteine_high` vs `signal_homocysteine_elevation_context`) are a **precedent** for family-level WHY routing — document whether both map to one hypothesis artefact set or two.

2. **`get_root_cause_targets()`** today returns loaders — new pattern: `get_root_cause_targets()` returns **artefact paths** or **loader factories** bound to compiled files.

3. **Do not** auto-discover from orphan packages (registry docstring forbids this) until compile manifest defines the estate.

4. **Confirmatory tests:** compiled artefact must map Pass 3 `test_id` → `confirmatory_tests_v1.yaml` at compile time; registry validation already depends on registry IDs.

**v2 Phase 7 actions are correct;** add explicit deliverable: `knowledge_bus/root_cause/registry/root_cause_targets_v2.yaml` (generated).

---

## 7. Safest first pilot candidate (after inventory)

**Agree with v2: do not hardcode HbA1c/CRP/ALT/homocysteine in WP3.**

Recommended inventory-driven pilot sequence:

### WP3 — Single-frame PSI / provenance pilot

**Select from Phase 0 with scoring:**

| Criterion | Favour |
|---|---|
| Single `spec_id` ↔ one package ↔ one `signal_id` | Avoids registry collision in pilot |
| Pass 3 lineage in `source_document` | Proves compile chain |
| Missing PSI or manifest opt-in gap | Proves Phase 2 value |
| Already has 2.0.0 `signal_library` | Reduces legacy noise |

**Strong candidates (pending inventory confirmation):**

- **`inv_ldl_high_atherogenic_ldl_burden`** or similar **single-frame lipid** spec — often one package, Card-relevant, PSI likely missing on kb52 estate.
- **`inv_hba1c_pct_high_chronic_hyperglycemia_diabetes`** — use only for **translator parity** (already ingested to `pkg_kb52d_*`), not as “gap” pilot — good for **determinism regression**, weak as “gap closure”.

**Defer:**

- **CRP** — Pass 3 specs exist; runtime authority is **legacy `pkg_s24_crp_high_inflammation`** — pilot bundles activation regen + registry + retirement (too large for WP3).
- **Homocysteine** — dual `signal_id` + dual registry rows + Pass 3 multi-spec; belongs in WP4/6.
- **ALT** — reserved for **WP4 multi-frame identity** per v2 (correct).

### WP5 — Card evidence pilot

**Prefer `wave1_met_glycaemic_control`** (HbA1c + glucose) **if** inventory shows clean Pass 3 linkage and medical review allows one scored subsystem. Alternative: **lipid transport only** if cardiovascular is medically approved as sole scored subsystem per `healthiq_wave1_health_systems_subsystem_medical_review.md`.

---

## 8. Still missing from v2 (loaders, DTOs, schemas, validators, manifests, Sentinels)

### Runtime loaders (not named or under-specified)

| Loader | Status |
|---|---|
| PSI runtime loader (package-scoped or estate index) | **Missing from orchestrator** — must be WP7 deliverable |
| Compiled card evidence loader | Planned Phase 6/8 — OK |
| Compiled hypothesis loader | Planned Phase 7/8 — OK |
| **`investigation_spec → signal_library` compiler loader** | **Not in v2** — only PSI translator exists; activation compile is separate WP |
| Estate index / `active_package` pointer update | Mentioned briefly — needs `run_knowledge_package.py` + `latest_knowledge_status.json` workflow in WP8 |

### DTOs

| Item | Gap |
|---|---|
| `SubsystemEvidenceV1` | Extend to **v2** or `card_schema_version` bump — plan lists fields but not versioning policy |
| `SignalResult` | **Must** add `activation_key`, `source_spec_id` — not in v2 DTO section |
| `InsightGraph.signal_results` | Dict rows — contract doc for new fields |
| `ReportV1` / `RootCauseFindingV1` | May need `source_spec_id` on findings if WHY becomes frame-specific |
| `ConsumerDomainScoreV1` | `subsystems` list — OK |

### Schemas

| Schema | v2 | Gap |
|---|---|---|
| `compile_manifest_schema_v1` | Phase 3 | OK |
| `health_system_card_evidence_schema_v1` | Phase 6 | OK |
| `compiled_hypothesis_schema_v1` | Phase 7 | OK |
| **`package_manifest` provenance fields** | Implied | **No `source_spec_id` in schema today** — add in ARCH-RT-1 |
| `signal_library` 2.1.0 (`relationship_kind`, `source_spec_id` on signal row) | Not explicit | Optional if PSI is semantic authority |

### Validators

| Validator | Gap |
|---|---|
| `validate_investigation_spec.py` on all Pass 3 files | **CI hook not specified** — add to WP2 |
| **`validate_compiled_artefacts.py`** (orchestrator) | Not in v2 — avoid five orphan scripts |
| Package promotion without manifest hash | WP3 — OK |
| **`validate_signal_registry_collision.py`** | Not listed — add at WP4 |

### Manifests

v2 asks “per artefact, per run, or estate-level?” — **Recommend:**

```text
Per compile run:  knowledge_bus/compiled/manifests/<compile_id>.yaml
Per artefact:     embedded source_spec_id + content hash inside artefact
Estate index:     knowledge_bus/compiled/estate_index_v1.yaml  (latest pointers + hashes)
```

Single estate-level manifest alone is insufficient for debugging pilot diffs.

### Sentinel guards (add to v2 §9)

| Guard | Why |
|---|---|
| `psi_present_but_not_loaded_in_orchestrator` | Tracks known debt until WP7 |
| `signal_registry_signal_id_last_path_wins` | Blocks target architecture |
| `package_missing_source_spec_id` | Launch blocker |
| `compiled_card_evidence_python_map_authority` | Post-cutover |
| `investigation_spec_runtime_read_in_core` | Scan `backend/core` for Pass_3 paths |
| `confirmatory_test_id_unregistered` | At hypothesis compile |
| `retail_prose_not_idl_governed` | Field allowlist on DTOs surfaced to FE |

Register in `sentinel/packs/escaped_defects_v1.json` per existing LC-S16 pattern.

### Other runtime adjacencies still thin in v2

- **`interaction_map_v1.yaml`** regeneration policy when `activation_key` lands.
- **`phenotype_map_v1.yaml`** / IDL `required_signals` alignment with new firing identities.
- **`calibration_engine`** — correctly in non-goals; note it can change visible severity without intelligence content changes.
- **`narrative_report_compiler_v1` / Layer C** — hypothesis surfacing path for reports vs cards.
- **`consumer_prose_safety_v1`** — card `rationale_short` must pass sanitizer.
- **Golden replay / `replay_manifest`** — WP8 must require determinism gate.
- **`translation_remap_contract_KB-S52B_v1.yaml`** — in Phase 3 manifest fields — good; enforce in all compilers.

---

## 9. Phases too broad for single Automation Bus work packages

| WP / Phase | Assessment |
|---|---|
| **WP0 / Phase 0** | Appropriate size (CONTENT/STANDARD) |
| **WP1 / Phase 1** | Appropriate (HIGH, MIXED) — gate for everything else |
| **WP2 / Phase 2** | OK if scoped to PSI gap + manifest schema only |
| **WP3 / Phase 3** | OK — single pilot |
| **WP4 / Phase 4** | OK — ALT / multi-frame only |
| **WP5 / Phase 5** | Borderline — split **5a schema+validator** / **5b one subsystem compile+loader+DTO+FE** if Automation Bus requires smaller diffs |
| **WP6 / Phase 6** | Borderline — split **hypothesis schema+compile** vs **root-cause registry transition pilot** |
| **WP7 / Phase 7** | **Too broad** — combines PSI runtime, card loader, hypothesis loader, DTOs, shadow mode, regression fixtures, Sentinel registration. **Split into 7a loaders+DTO**, **7b shadow+golden**, **7c sentinel+QA** |
| **WP8 / Phase 8** | Inherently large — acceptable as one WP only with **sub-milestones** (packages → PSI opt-in → card estate → hypothesis estate → registry → retirement) |
| **WP9 / Phase 9** | Appropriate (CONTENT audit) |

**v2 prohibition (§10 item 11):** “Do not write work packages until second-pass review confirms baseline” — **this review confirms baseline for WP0–1 only.**

---

## 10. Launch blockers if unresolved

Even with no live users, treat these as **architecture launch blockers**:

1. **Unresolved multi-frame `signal_id` collapse** in `SignalRegistry`.
2. **Active runtime authority** still `wave1_subsystem_evidence.py` manual maps.
3. **Hand-authored root-cause YAML** still sole WHY input with no compiled replacement path in production.
4. **Packages without provenance** (`source_spec_id` or governed `legacy_retained` classification).
5. **CRP (and similar) legacy package** still authoritative while richer Pass 3 specs are uncompiled/unpromoted.
6. **PSI opt-in estate incomplete** where signal-layer semantics are required for card/report claims.
7. **No compile manifest + hash validation** on promoted active estate.
8. **Retail card copy** from research compile bypassing IDL / `consumer_prose_safety_v1`.
9. **Interaction map / phenotype map / root-cause registry** stale relative to new identity model.
10. **No traceability audit** proving spec → artefact → DTO → component for each user-visible claim (Phase 10 deliverable).

**Not launch blockers (but must be scheduled):**

- Full 153-spec regeneration (can trail pilot cutover if pilots prove architecture).
- Every marker having card roles on day one (visibility `hidden_v1` is acceptable per medical review).

---

## 11. Changes required before converting plan to Automation Bus WPs

1. **Add §5.1 decision outcome template** to WP1: chosen keying (`activation_key = spec_id` recommended), `SignalResult` fields, interaction-map policy.
2. **Add explicit “activation compile” WP** between WP2 and WP3: `investigation_spec → signal_library + research_brief` (not only PSI).
3. **Fix §2.2 package generation description** (kb52* vs s24*).
4. **Split WP7** in the work-package sequence table.
5. **Specify manifest storage** (per-run + estate index) in Phase 3 deliverables.
6. **Add `package_manifest_schema` update** for `source_spec_id`, `activation_key`, `compile_manifest_ref`.
7. **Add CI:** `validate_investigation_spec` on `*_Pass_3.json` on research changes.
8. **Clarify WP5 card pilot selection rule** — inventory scorecard, reference medical review visibility tiers.
9. **Remove ambiguity:** “Phase 2 may include code” — all MIXED phases require Automation Bus SOP with evidence capture.

---

## 12. Answers to v2 §11 review questions (checklist)

| # | Question | Answer |
|---|---|---|
| 1 | PSI / ADR-008 reflected? | **Yes**, with minor package-generation wording fix |
| 2 | Accept ADR-008? | **Yes** |
| 3 | Artefact split correct? | **Yes** |
| 4 | `activation_key` vs `signal_id + spec_id`? | **`signal_id + spec_id` insufficient alone; introduce `activation_key` (prefer `= spec_id`)** |
| 5 | SignalRegistry changes? | See §5 above |
| 6 | `root_cause_registry_v1` path? | Generated registry from compiled index; phased loaders; see §6 |
| 7 | Pilot after inventory? | Single-frame LDL-like gap for WP3; glycaemic subsystem for card WP5; ALT for WP4 |
| 8 | Missing loaders/DTOs? | See §8 |
| 9 | Manifest granularity? | Per-run + estate index |
| 10 | Missing STOP conditions? | PSI-orchestrator, registry collision, CI spec validation |
| 11 | Phases too broad? | **WP7, WP8** — split milestones |
| 12 | Launch blockers? | See §10 |

---

## Final verdict

| Question | Verdict |
|---|---|
| Is v2 the correct route? | **Yes** |
| Accurate enough for Automation Bus WPs? | **Yes for WP0–1; conditional for WP2+ pending WP1** |
| Should implementation start immediately? | **No** — complete inventory + identity ADR first |

v2 is **ready to drive governance and work-package authoring** for the inventory and decision phases. It is **not** yet ready to author a single “runtime integration” mega-WP without the splits and codebase-specific additions above.

---

*Architecture review only. No code, work packages, or merges were created or modified.*
