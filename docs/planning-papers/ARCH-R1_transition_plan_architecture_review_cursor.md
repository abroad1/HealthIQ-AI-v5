# Architecture Review: As-Is to Day-One Transition Plan

**Document reviewed:** `docs/planning-papers/HealthIQ_As-Is_to_Day-One_Architecture_Transition_Plan.md`  
**Reviewer:** Cursor (architecture challenge — no implementation)  
**Date:** 2026-05-28  
**Related:** `docs/architecture/ARCH-R1_research_asset_to_runtime_intelligence_architecture_review_cursor.md`, Pass 3 utilisation audits, ADR-008

---

## Executive summary

**Verdict:** The transition plan is **directionally correct and launch-appropriate**. It matches ARCH-R1 and the audit evidence. **It is not yet safe to convert to Automation Bus work packages** without reconciling existing governed assets (especially **Promoted Signal Intelligence / ADR-008**) and filling several runtime-adjacency gaps.

Treat the plan as the right *destination*, with material *under-specification* on what already exists and *over-specification* on net-new schemas/compilers that would duplicate locked contracts.

---

## 1. Is the proposed target architecture correct?

**Yes, with one structural refinement.**

The core chain is right:

```text
canonical research spec → validation → deterministic compile → governed runtime artefacts
→ thin loaders → DTOs → frontend render-only
```

That is the correct day-one posture given no live users and fragmented authorities today.

**Refinement:** The plan names a new **“Signal Intelligence Artefact”** as if greenfield. The repo already has a locked, governed equivalent:

| Plan term | Existing authority |
|---|---|
| Signal Intelligence Artefact | `promoted_signal_intelligence.yaml` + `promoted_signal_intelligence_schema_v1.yaml` (ADR-008, KB-S47d) |
| Translation rules | `signal_intelligence_translation_rules_v1.yaml` (LOCKED) |
| Translator | `backend/core/knowledge/investigation_spec_to_promoted_signal.py` |
| Signal Activation Artefact | `signal_library.yaml` + `research_brief.yaml` + `package_manifest.yaml` (Knowledge Bus package) |

ADR-008 explicitly **excludes** hypotheses and narrative from PSI and points them to **“adjacent hypothesis assets”** — which the transition plan correctly wants but does not name as the formal third compile target. The day-one model should be:

```text
investigation_spec v3
  ├─→ signal activation compile  → package (signal_library)     [firing]
  ├─→ signal intelligence compile → promoted_signal_intelligence   [signal-layer richness, incl. relationship_kind]
  ├─→ hypothesis compile          → compiled_hypotheses_v2         [WHY / root-cause input — NEW, missing today]
  └─→ card evidence compile       → wave1_health_system_evidence   [UX projection — NEW]
```

**Do not** introduce a parallel `signal_intelligence_schema_v1` that competes with PSI without an ADR superseding ADR-008.

---

## 2. Does it accurately reflect current codebase reality?

**Mostly yes on problems; partially wrong on “nothing exists yet.”**

### Accurate

- Pass 3 richness vs thin cards and manual `wave1_subsystem_evidence.py`.
- Packages are lossy and mixed maturity (142× schema 2.0.0, 44× 1.0.0; ~132 cite Pass 3).
- Root-cause YAML is hand-authored, overlaps Pass 3, feeds `root_cause_compiler_v1` / reports — **not** cards.
- `SignalEvaluator` uses activation/overrides; `explanation` and `supporting_metrics[].role` are orphaned for cards.
- `signal_id` collision with lexicographic overwrite in `SignalRegistry`.
- Frontend is render-only in intent; gap is backend DTO assembly.

### Incomplete or slightly wrong

| Topic | Plan says | Codebase reality |
|---|---|---|
| Signal intelligence | New compile product | **Already specified and implemented** for translation to PSI; **not loaded in production orchestrator** (~20 `pkg_kb47_*` have PSI on disk) |
| Ingest | Generic “compiler suite” | Sprint scripts exist (e.g. `kb_s47_batch2_ingest.py`); KB-S52B **translation/remap contracts** govern biomarker remaps (`fasting_glucose→glucose`) |
| Hypothesis path | “Compiled root-cause from signal intelligence” | PSI **forbids** hypotheses; root-cause today uses **different schema** (`evidence_for_rules`, etc.) — compile must be **spec → hypothesis artefact → root-cause**, not PSI → root-cause |
| CRP pilot | Same tier as HbA1c/ALT | Pass 3 has rich CRP specs; **runtime still uses legacy `pkg_s24_crp_high_inflammation`** — not Pass 3 lineage |
| IDL | Presentation layer | Correct, but **actively drives** card headlines via `domain_narrative_wave1` + `interpretation_display_layer_publish_v1` — coordination with card compile is unspecified |
| “No runtime intelligence assets” in Phase 0 | Freeze | **`interaction_map_v1.yaml`**, `phenotype_map_v1.yaml`, calibration registry, intervention/safety rules also shape report behaviour |

The as-is diagram in the plan is fair at a product level; it under-reports **governed translation infrastructure already paid for**.

---

## 3. Missing runtime dependencies, loaders, DTOs, schemas, tests, governance

### Runtime / loaders not in plan

- **`interaction_map_v1.yaml`** — `signal_interaction_builder.py`, `report_compiler_v1` chains; must stay consistent when `activation_key` / multi-frame signals change.
- **`phenotype_map_v1.yaml` + IDL** — severity and retail copy; card compile must not bypass IDL for surfaced prose.
- **`calibration_engine` / `calibration_registry`** — can alter burden/arbitration; not intelligence content but affects “what user sees.”
- **`load_confirmatory_tests_registry_v1`** — root-cause maps `test_id` → registry; Pass 3 `confirmatory_tests[]` need **compile-time mapping**, not ad hoc strings.
- **`root_cause_registry_v1` / `get_root_cause_targets()`** — explicit signal allowlist for WHY; full regeneration must update registry + compiled assets together.
- **`CanonicalResolver` / remap contract** — KB-S52B remaps; compilers must use same remap authority as ingest or parity will fail.
- **`knowledge_bus/current/active_package.json` / `latest_knowledge_status.json`** — promotion and estate status (KB SOP); regeneration WP must include promotion workflow.
- **`SignalRegistry` duplicate policy** — code change required for `activation_key`; plan mentions identity but not mandatory evaluator/registry refactor WP.

### Schemas / governance already locked (plan should reference, not replace)

- `investigation_spec_schema_v3.0.0.yaml`
- `promoted_signal_intelligence_schema_v1.yaml`
- `signal_intelligence_translation_rules_v1.yaml`
- `signal_library_schema.yaml` (1.3.0)
- `research_brief_schema.yaml`
- `translation_contract_v3_to_package_KB-S52B_v1.yaml`
- `intelligence_model_schema_v1.yaml` — optional path per ADR-008 (hypotheses-in-package); **no manifests use it today**, but schema exists

### Validators (plan lists new scripts; should extend)

- **Authoritative package gate:** `validate_knowledge_package.py` (not only new per-artefact scripts).
- **Upstream:** `validate_investigation_spec.py` — KB SOP: **not** auto-invoked by package validator; plan should require explicit CI step or hook.
- **Existing:** `validate_promoted_signal_intelligence.py`, `validate_signal_library.py`.

### Tests / Sentinel

- Existing: `test_domain_ux1c_governed_subsystem_evidence.py` (sentinel class names), `test_promoted_signal_intelligence_kb_s47d.py`, golden/persisted fixtures (`lc_s20_ab_launch_core_v1.json`), `sentinel/packs/escaped_defects_v1.json` registration pattern.
- Plan’s Sentinel list is good but should require **registration in `escaped_defects_v1.json`** (or successor pack) per existing LC-S16 pattern.
- Missing guard concept: **`psi_runtime_loader_absent_while_package_has_psi`** (today PSI is validated but not consumed — architectural debt).

### DTOs

- `SubsystemEvidenceV1` — `evidence_role` exists, always null; plan should say **extend/version** (`SubsystemEvidenceV2` or schema version on card), not only “extend ConsumerDomainScoreV1.”
- `SignalResult.explanation` — already in pipeline; plan should decide **wire vs deprecate** to avoid a fifth orphan.
- `RootCauseV1` / `ReportV1` — report path unchanged in phases 5–6 ordering; good, but contract impact should be listed.

---

## 4. Are the proposed artefact boundaries right?

| Artefact | Verdict |
|---|---|
| **Canonical research spec** | Correct — `investigation_spec` v3 / Pass 3 corpus; file layout may change. |
| **Signal activation artefact** | Correct — **package `signal_library`** scope only (firing). |
| **Signal intelligence artefact** | **Rename/align to existing PSI**; do not create a second contract. |
| **Compiled root-cause artefact** | Correct, but input is **hypothesis compile from spec**, not PSI alone. |
| **Health Systems Card evidence artefact** | Correct and necessary — **separate projection**; must not live in `signal_library`. |
| **IDL / presentation safety** | Correct — gates retail prose; must consume compiled facts, not author mechanism text. |
| **DTO boundary** | Correct. |

### Card evidence vs projection from signal intelligence

**Card evidence should be a compiled projection from canonical research (and domain mapping policy), not only from PSI.**

Reasons:

- PSI lacks hypotheses, narrative, and per-hypothesis `missing_data.policy`.
- Card needs **domain/subsystem grouping** (not in spec per signal).
- Card needs **visibility tiers** (medical review) — presentation/compile policy, not signal-layer.
- PSI is valuable for **marker-level** `relationship_kind` + rationale when a frame fires; card loader can **join** fired `activation_key` → PSI row + card artefact row.

Recommended join at runtime:

```text
fired activation_key → PSI (marker semantics) + card artefact (subsystem placement, visibility, card_role)
```

---

## 5. Is the identity model sufficient?

**Conceptually yes; operationally under-specified.**

| ID | Assessment |
|---|---|
| `research_spec_id` / `spec_id` | **Required.** Must become package primary key for compile outputs (`source_spec_id` in manifest). |
| `signal_id` | Keep as **activation family** — not unique frame identity. |
| `activation_key` | **Required** for registry — suggest `f"{spec_id}"` or `f"{signal_id}::{spec_id}"` until ADR defines format. |
| `hypothesis_id` | Sufficient within hypothesis artefact. |
| `artefact_id` | Vague — specify per artefact type (`compile_manifest.compile_id`, output path hash). |

**Gaps to add before WP lock:**

- **Package directory naming** — today `pkg_*` often encodes one frame; collision is at **registry** not folder.
- **Derived metrics** (`hba1c_pct` vs `hba1c`, ratios) — identity must include **remap contract** keys.
- **IDL `internal_id`** vs `spec_id` — mapping table for phenotype-driven headlines vs frame-level evidence (avoid two retail authorities).

Rule “no silent collapse” is correct; **cannot be enforced without `SignalRegistry` / evaluator refactor** — must be its own HIGH-risk WP, not buried in Phase 7.

---

## 6. Retire cleanly vs retain for parity

### Retain temporarily (parity / adjudication only)

| Asset | Why keep |
|---|---|
| Hand-authored `knowledge_bus/root_cause/hypotheses/*_v1.yaml` | Diff against compiled hypotheses; report behaviour baseline |
| `wave1_subsystem_evidence.py` manual maps | Diff against card artefact; UX regression |
| Legacy packages (`pkg_s24_*`, 1.0.0 flat supporting lists, pre–Pass 3 CRP) | Evaluator baseline until regenerated |
| Current `signal_library` 2.0.0 packages without PSI | Activation parity during compile rollout |
| `SignalResult.explanation` population | Compare orphan vs new card/PSI surfacing |
| Golden panels / `replay_manifest` fixtures | Determinism proof |

### Retire as runtime authority after gate (not delete files immediately)

| Asset | Condition |
|---|---|
| Manual subsystem maps | Card artefact wired + sentinels green |
| Hand-authored root-cause YAML | Compiled coverage + clinical sign-off on divergence report |
| Packages without `source_spec_id` | Regenerated or explicitly marked `legacy_retained` in estate manifest |
| Lexicographic `signal_id`-only registry | `activation_key` registry live |

### Do not retire without explicit decision

- **IDL records** — still needed; evolve, don’t replace with card artefact prose.
- **`interaction_map_v1.yaml`** — regenerate or validate against new signal identities.
- **Scoring rails / clusters** — out of scope; plan correctly avoids changing them.

---

## 7. Safest first compiler pilot

**Not the plan’s four-marker basket as Phase 3’s first compile.**

### Pilot A (lowest risk, proves governance) — PSI parity, single spec

- **Spec:** one investigation spec with existing KB ingest parity, e.g. `inv_hba1c_pct_high_chronic_hyperglycemia_diabetes` → `pkg_kb52d_hba1c_pct_high_chronic_hyperglycemia_diabetes`.
- **Action:** Run `investigation_spec_to_promoted_signal.py` + compare to existing `signal_library` / `research_brief` / optional PSI on disk.
- **No runtime wiring.**
- **Proves:** manifests, hashes, remap contract, validator integration.

### Pilot B (proves new artefact) — Card evidence for one subsystem

- **Scope:** `wave1_met_glycaemic_control` only (HbA1c + glucose), visibility tiers, roles from Pass 3 + medical review policy.
- **No** hypothesis sentences on retail surface in pilot — roles + `rationale_short` + `missing_policy_line` only.

### Pilot C (proves identity) — ALT multi-frame

- **Three** `spec_id`s sharing `signal_alt_high` → three `activation_key`s + three activation compiles.
- **Proves** collision fix before CRP/regeneration.

### Defer from first pilot

- **CRP** — Pass 3 specs exist but **no Pass 3–lineage package** in production; pilot forces activation compile + registry change together (higher blast radius).
- **Homocysteine** — duplicate `signal_homocysteine_high` frames + separate `signal_homocysteine_elevation_context` / root-cause asset naming — adjudicate identity first.
- **Full root-cause compile** — after hypothesis artefact schema exists; not Phase 3.

---

## 8. Missing STOP conditions, Sentinels, validators, manifests

### STOP conditions to add

- **No new `signal_intelligence_schema` without ADR superseding ADR-008.**
- **No compile output that bypasses `translation_remap_contract_KB-S52B_v1.yaml`.**
- **No Phase 5+ card prose without IDL/sanitiser pass.**
- **No `activation_key` registry change without interaction map review.**
- **No root-cause switch with &lt;N% of `get_root_cause_targets()` covered by compiled assets** (define N in WP).
- **No package promotion without `validate_knowledge_package` + compile manifest hash match.**
- **No deletion of legacy YAML until divergence report signed.**

### Sentinel / guards to add (plus escaped_defects registration)

| Guard | Why |
|---|---|
| `investigation_spec_runtime_read_forbidden` | Plan has concept — implement as static/orchestrator scan |
| `signal_registry_signal_id_only_collision` | Detect duplicate `signal_id` across packages without `activation_key` |
| `psi_present_but_not_in_runtime_contract` | Until loader exists, track debt |
| `compiled_card_evidence_manual_map_authority` | Block `_WAVE1_DOMAIN_SUBSYSTEM_DEFS` as authority post-cutover |
| `hypothesis_asset_pass3_hash_drift` | Spec hash vs compiled hypothesis hash |
| `confirmatory_test_id_not_in_registry` | Compile-time |
| `retail_prose_bypasses_idl` | Static scan on DTO fields allowed in frontend |

### Compile manifest gaps

- Add: `remap_contract_version`, `translation_rules_version`, `target_package_id`, `activation_key`, `spec_id` per output row.
- Add: **parent compile_id** when card artefact derives from multiple specs.
- Wire manifest into `latest_knowledge_status.json` or estate record per KB SOP.

### Validator gaps

- Single **`validate_compiled_artefacts.py`** orchestrator calling per-schema validators (avoid 5 disconnected entrypoints without aggregation).
- CI: **`validate_investigation_spec` on all Pass 3 files** on every research change.

---

## 9. Overcomplicated, under-specified, or wrong

### Overcomplicated

- **New `signal_intelligence_schema_v1` + `compile_research_to_signal_intelligence.py`** duplicating PSI — use existing translator + extend promotion/loader instead.
- **Nine sequential WPs** — fine for governance, but WP3–WP4 can merge after Pilot A if PSI is accepted as the intelligence compile target for signal-layer fields.
- **Separate `compile_signal_intelligence_to_root_cause.py`** — wrong direction; hypothesis artefact is the hub.

### Under-specified

- Reconciliation with **ADR-008**, KB-S47d, KB-S52B contracts.
- **`activation_key` implementation** in `SignalRegistry` / `SignalEvaluator` / `InsightGraph` serialization.
- **Promotion pipeline** (`run_knowledge_package.py`, active package pointer).
- **Interaction map + phenotype map** regeneration rules.
- **Medical review → visibility tier** compile policy document (plan references tiers but not authority file).
- **Card role translation table** (package role → card role) — referenced in Phase 4, should be Phase 2 deliverable.
- **Replay/golden determinism** for full pipeline post-regeneration.
- **Automation Bus classification** per WP (`change_type`, evidence capture) — only implied.

### Wrong or risky as written

- **Phase 3 builds “research → signal intelligence compiler” from scratch** — conflicts with locked `investigation_spec_to_promoted_signal.py`.
- **Phase 6 “compile root-cause from signal intelligence”** — PSI cannot supply full WHY graph; must compile from **spec hypotheses** into root-cause-shaped rules (or replace root-cause compiler input contract).
- **“Controlled replacement” without parallel-run window** — even with no users, recommend **shadow mode**: compiled artefacts drive diff dashboards before flip (internal QA).
- **Risk level on ARCH-RT-0 as STANDARD** — inventory touching Intelligence Core paths may still be CONTENT-only; OK, but traceability matrix must include orchestrator — classify accurately.

---

## 10. What to change before formal Automation Bus work packages

### A. Reconcile with existing governance (mandatory)

1. Add **“ADR-008 alignment”** section to the transition plan: PSI = signal intelligence artefact; extend, don’t reinvent.
2. Add explicit **hypothesis artefact** as first-class compile output (ADR-008 “adjacent hypothesis assets”).
3. State **package = signal activation artefact** in naming throughout WPs.

### B. Fix compile graph in the plan

Replace:

```text
compile_signal_intelligence_to_root_cause.py
```

With:

```text
compile_research_to_hypothesis_artefact.py
compile_hypothesis_artefact_to_root_cause_input.py  # or unify root-cause schema with hypothesis artefact
compile_research_to_promoted_signal_intelligence.py  # wrap existing module
compile_research_to_signal_activation_package.py     # signal_library + research_brief
compile_research_to_health_system_card_evidence.py   # domain projection + visibility policy
```

### C. Reorder phases slightly

| Order | Rationale |
|---|---|
| Phase 0–2 | Keep |
| **Phase 2b** | `activation_key` + registry ADR (blocks honest pilot) |
| Phase 3 | **PSI + activation parity pilot** (HbA1c single spec) |
| Phase 4 | Card evidence pilot (one subsystem) |
| Phase 5 | Runtime loaders (PSI optional join + card artefact) |
| Phase 6 | Hypothesis/root-cause replacement |
| Phase 7 | Full regeneration |
| Phase 8 | Launch gate |

### D. Narrow WP sequence for Automation Bus

| WP | Objective |
|---|---|
| **ARCH-RT-0** | Traceability matrix + legacy inventory (unchanged) |
| **ARCH-RT-1** | Identity + ADR (`activation_key`, `spec_id`, registry policy) |
| **ARCH-RT-2** | Compiled artefact schemas: hypothesis v2, card evidence v1, compile manifest; **PSI schema reference only** |
| **KB-COMPILER-1** | Activation + PSI compile parity (existing translator + new package compiler) — pilot HbA1c |
| **ARCH-RT-4** | Card evidence compile + validation — pilot glycaemic subsystem |
| **ARCH-RT-5** | Runtime loaders + DTO v2 + frontend render |
| **ARCH-RT-6** | Hypothesis compile + root-cause switch + divergence |
| **ARCH-RT-7** | Full regeneration + legacy retirement |
| **ARCH-RT-8** | Launch gate audit |

### E. Add explicit “non-goals” to every MIXED/BEHAVIOUR WP

- Scoring rails, cluster weights, unit conversion, reference ranges, IDL copy changes (unless presentation-only).

### F. Product/medical gate

- Bind card compile to **`healthiq_wave1_health_systems_subsystem_medical_review.md`** visibility tiers before retail hypothesis/contradiction text.

---

## Bottom line

| Question | Answer |
|---|---|
| Correct route to day-one architecture? | **Yes** — this is the right pre-launch correction. |
| Safe to implement as written? | **Not yet** — reconcile with PSI/ADR-008, fix hypothesis compile chain, narrow pilot, add registry/orchestrator/adjacency work. |
| Biggest risk if unchanged? | **Duplicate compilers and authorities** beside locked KB-S47d assets, while still not loading PSI or card intelligence at runtime. |

The transition plan should be adopted as the **strategic transition**, then revised into Automation Bus work packages that **extend governed assets already in the repo** rather than describing a greenfield compiler suite that ignores them.

---

*Investigation and architecture review only. No code, packages, work packages, or merges were created or modified.*
