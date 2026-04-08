# KB-S58 Preflight — Phenotype / Fixture / Regression Expansion

**work_id:** KB-S58-PREFLIGHT  
**mode:** READ_ONLY investigation (no implementation)  
**date:** 2026-04-08  
**evidence:** Repository paths cited below.

---

## 1. Executive summary

### Current maturity (phenotype / fixture / regression)

| Layer | Maturity | Evidence |
|-------|----------|----------|
| **Phenotype map (SSOT)** | **Moderate** — nine governed phenotypes in `knowledge_bus/phenotypes/phenotype_map_v1.yaml`; each lists `synthetic_fixture_refs`, `required_signals`, `required_edges`, and `chain_expectations.status` (`enforced` vs `pending`). | Map file (full roster below). |
| **Rationales & research refs** | **Partial** — rationales exist for edges under active review (vascular, renal, metabolic IR, iron, thyroid); research ref YAMLs exist for renal creatinine→urea, TSH→LDL, inflammation→hcy context. | `knowledge_bus/phenotypes/rationales/*.md`, `research_refs/*.yaml`. |
| **Fixtures** | **Strong for declared suite** — one JSON per phenotype under `backend/tests/fixtures/panels/phenotypes/`; filenames match `phenotype_map_v1.yaml` `synthetic_fixture_refs` and `phenotype_expectations_v1.yaml` `fixture_filename`. | Ten files under that directory including `phenotype_expectations_v1.yaml`. |
| **Expectation contract** | **Strong alignment, narrow enforcement** — `phenotype_expectations_v1.yaml` lists the same nine phenotypes as the map; only **two** declare `chain_coverage_status: "enforced"` (homocysteine-vascular pattern and renal stress); the rest are `pending` for chains with varying `must_fire` signal and root-cause assertions. | `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`. |
| **Regression harness (unit)** | **Present** — `backend/tests/unit/test_phenotype_suite_v1.py` runs `run_golden_panel` twice per phenotype, asserts determinism, `must_fire` / `must_not_fire`, and conditional chain + root-cause expectations. | Single test module grep-able as `test_phenotype_suite_v1_regression_harness`. |
| **Regression harness (automation gate)** | **Weak / disconnected** — `backend/scripts/run_baseline_tests.py` **does not** invoke `test_phenotype_suite_v1.py` (it runs canonical enforcement, retail explainer tests, and golden fixture collision tests only). `golden_gate_local.py` chains to that baseline script plus `verify_three_layer_pipeline.py`, which uses the **default** `golden_panel_160.json`, not phenotype panels. | `run_baseline_tests.py` command list; `verify_three_layer_pipeline.py` + `run_golden_panel._default_fixture_path()`. |
| **Map / interaction validators** | **Present** — `validate_phenotype_map.py`, `validate_interaction_map_v1.py`, and unit tests (`test_validate_phenotype_map.py`, `test_validate_interaction_map.py`) tie phenotype `required_edges` to `interaction_map_v1.yaml`. | Scripts under `backend/scripts/`; tests under `backend/tests/unit/`. |

### Key gaps (grounded)

1. **Gate vs suite:** The governed automation bus “infra-free” gate does **not** execute the phenotype regression harness; engineers can merge engine changes that break phenotype determinism or enforced phenotypes without the gate failing.
2. **Enforcement skew:** **Seven** of nine phenotypes remain `chain_expectations.status: "pending"` in the map **and** `chain_coverage_status: "pending"` in expectations — only homocysteine-inflammation and renal stress are fully chain-enforced in YAML. That is appropriate where interaction edges are immature, but it concentrates “hard” regression on two synthetic scenarios.
3. **Default golden ≠ phenotype breadth:** Three-layer verification proves coherence on a **large fixed panel**, not on per-phenotype clinical shapes or newer multi-signal constellations introduced or strengthened by recent waves (renal wiring, ranked ambiguity, etc. are only indirectly exercised).
4. **Strategic ID collision:** The adopted roadmap reuses the token **“KB-S58”** in two different lineages (CBC Pass‑3 ingestion parenthetical vs Wave 4 phenotype/fixture/regression wave). Authors must use **section heading meaning**, not numeric ID alone (`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` §13.0, §685–697).

### Whether KB-S58 (phenotype / fixture / regression wave) is justified **now**

**Yes.** Recent delivery expanded the governed runtime estate (renal promotion and interaction-map completion per map notes, clustering/scoring/policy work, persistence, frontend consumption). The repo already invested in a **nine-phenotype synthetic suite** and a **unit-level harness**, but the **automation gate does not run it**, and most phenotypes remain **deliberately pending** for chain-level enforcement. Closing that disconnect is exactly the anti-drift purpose described in the roadmap for this wave.

---

## 2. Strategy interpretation — what KB-S58 is *actually* supposed to do

**Primary source:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`.

### 2.1 Disambiguation: two “KB-S58” mentions

| Location | Meaning |
|----------|---------|
| §13.0 + §685–686 (under KB-S55 / Batch 5 narrative) | **Historical ingestion lineage:** text states Pass 3 ingestion for CBC was executed under a label rendered as “KB-S58” **in the Batch 5 note** — i.e. **ingestion/breadth**, not phenotype regression. |
| §695–697 (**Historical lineage: KB-S58 — Phenotype / Fixture / Regression Expansion**) | **Structural-truth wave:** “strengthen phenotype truth, fixtures, and regression coverage across the enlarged estate” — **anti-drift**, multi-signal testability. |

**This preflight addresses only the §695–697 meaning.** The roadmap explicitly warns that v1.4 sprint IDs do not map one-to-one to current repo sprints (§13.0).

### 2.2 What “Phenotype / Fixture / Regression Expansion” means here

| Phrase | Meaning in roadmap context |
|--------|----------------------------|
| **Phenotype truth** | Governed definitions in `phenotype_map_v1.yaml`: required signals/edges, evidence basis, `chain_expectations`, linkage to synthetic fixtures — so “what counts as a phenotype” is SSOT, not ad hoc tests. |
| **Fixtures** | JSON panels under `backend/tests/fixtures/panels/phenotypes/` that instantiate those definitions for deterministic runs. |
| **Regression expansion** | Broader **automated** guarantees that the enlarged engine does not silently drift on multi-signal outputs (chains, root-cause blocks, signal firing) — commensurate with Wave 4 “stronger scaffolding” (§678–683). |

### 2.3 Capability unlocked

**Trustworthy multi-signal regression:** ability to ship engine, map, and compiler changes knowing that **named clinical patterns** (not only the monolithic golden panel) remain **deterministic** and meet **declared** signal/chain/root-cause bars where `enforced`.

### 2.4 Combination nature

This wave is **explicitly a combination**: phenotype map + fixtures + regression harness are already co-designed in-repo (`phenotype_map_v1.yaml` ↔ `phenotype_expectations_v1.json` ↔ JSON fixtures ↔ unit harness). KB-S58 is **not** “only map expansion” or “only fixtures”; it is **closing gaps between declared intent and what the gate actually runs**, and **raising** `pending` → `enforced` where interaction-map evidence supports it.

---

## 3. Phenotype audit (`phenotype_map_v1.yaml`)

### 3.1 Phenotypes present (nine)

| `phenotype_id` | `chain_expectations.status` (map) | `synthetic_fixture_refs` |
|----------------|-------------------------------------|----------------------------|
| `ph_vascular_hcy_inflammation_v1` | **enforced** | `ph_vascular_hcy_inflammation_v1.json` |
| `ph_renal_stress_v1` | **enforced** | `ph_renal_stress_v1.json` |
| `ph_metabolic_early_ir_v1` | **pending** | `ph_metabolic_early_ir_v1.json` |
| `ph_thyroid_lipid_disturbance_v1` | **pending** | `ph_thyroid_lipid_disturbance_v1.json` |
| `ph_iron_deficiency_inflammation_v1` | **pending** | `ph_iron_deficiency_inflammation_v1.json` |
| `ph_iron_overload_v1` | **pending** | `ph_iron_overload_v1.json` |
| `ph_hba1c_metabolic_stress_v1` | **pending** | `ph_hba1c_metabolic_stress_v1.json` |
| `ph_hepatic_alt_inflammatory_v1` | **pending** | `ph_hepatic_alt_inflammatory_v1.json` |
| `ph_tsh_axis_metabolic_v1` | **pending** | `ph_tsh_axis_metabolic_v1.json` |

### 3.2 Pending vs enforced (expectations YAML mirror)

`phenotype_expectations_v1.yaml` matches: **enforced** chain coverage for `ph_vascular_hcy_inflammation_v1` and `ph_renal_stress_v1` only; all others `chain_coverage_status: "pending"`. Several pending phenotypes still assert **signal firing** and, for hba1c / hepatic / tsh cases, **root_cause `must_exist`** with minimum hypothesis counts — i.e. **partial** enforcement.

### 3.3 Recent change signal (renal)

`ph_renal_stress_v1` map entry explicitly references **KB-S56A/B** (edge promotion, interaction map, root-cause loaders) in `evidence_notes` — repo state reflects **post‑renal-wave** scaffolding; renal is **not** “missing from map” but is one of only two chain-enforced phenotypes, so **relative** coverage weight on renal + homocysteine is high.

### 3.4 Obvious coverage gaps

| Gap type | Detail |
|----------|--------|
| **Present** | Full 9-phenotype map + fixtures + expectation rows + unit harness. |
| **Partial** | Seven phenotypes pending chain enforcement; iron overload stub; exploratory edges flagged for future promotion in map comments. |
| **Missing (vs enlarged estate)** | Phenotype suite does not add panels covering **every** newly promoted Wave C / ingestion marker; suite is **synthetic clinical patterns**, not exhaustive biomarker enumeration. **Clinician AB/VR JSON** is a separate fixture family (not exhaustively cross-walked here; see KB-S53 investigations for AB/VR formalisation). |

---

## 4. Fixture and regression audit

### 4.1 Fixtures

- **Dedicated phenotype fixtures:** `backend/tests/fixtures/panels/phenotypes/*.json` (nine phenotype JSONs) — all **synthetic** small panels (e.g. `ph_renal_stress_v1.json` is three renal markers + minimal user block).
- **Default golden / three-layer:** `backend/tests/fixtures/golden_panel_160.json` — **broad** synthetic panel; used by `verify_three_layer_pipeline.py`, not substituted per phenotypes.
- **reports:** `backend/tests/fixtures/reports/` (clinician AB/VR) — separate contract; not the same as phenotype suite (no duplication required for this preflight conclusion).

### 4.2 Regression protections today

| Protection | Catches… | Does not catch… |
|------------|----------|-----------------|
| `test_phenotype_suite_v1.py` | Non-determinism per phenotype; wrong firing for `must_fire` / `must_not_fire`; enforced chain presence/confidence/signal inclusion; root cause counts where `must_exist`. | **Anything not in the nine fixtures**; not run in `run_baseline_tests.py`. |
| `verify_three_layer_pipeline.py` | Layer-3 / card / burden invariants on **golden_panel_160**. | Per-phenotype constellation drift. |
| `run_baseline_tests.py` (gate) | Canonical-only, retail explainer registry, golden collision, explainer unit tests. | Phenotype chains/root-cause. |
| `validate_interaction_map_v1.py` + tests | Phenotype `required_edges` covered in `interaction_map_v1.yaml`. | Runtime numeric thresholds or hypothesis text drift. |
| `validate_phenotype_map.py` + tests | Map schema/orphan signals. | Engine output semantics. |

### 4.3 Weak points (after recent delivery)

- **Regression gap:** strongest multi-phenotype harness is **optional** in developer workflow; **absent** from automation bus baseline gate.
- **Expectation staleness risk:** `phenotype_expectations_v1.yaml` `updated_at: "2026-03-15"` — may predate minor engine tweaks; not inherently wrong, but **worth validating** when promoting more phenotypes to `enforced`.
- **Renal:** adequately represented **for the declared renal phenotype** (enforced chain + root cause expectations + tight synthetic fixture); **not** a guarantee that **all** renal-adjacent package or interaction subtrees are phenotype-guarded.

---

## 5. Post-recent-delivery gap assessment (repo evidence only)

| Recent delivery | Phenotype/regression implication |
|-----------------|-----------------------------------|
| **Renal wave (KB-S56 lineage per map notes)** | Map + expectations + fixture **do** enforce `ph_renal_stress_v1`; **minimal** in the sense of a **3-marker** synthetic panel, but **not** “uncovered” in the suite. |
| **Ranked ambiguity / runtime policy / scoring** | **Not** asserted in `phenotype_expectations_v1.yaml`; **partial** protection via three-layer golden run (cluster/system cards) — **weak** coupling to phenotype JSON suite. |
| **Persistence / FE results** | Out of scope for KB-S58 definition; **no** requirement to expand phenotype suite for UI. |
| **Interaction-map edits** | **Partially** guarded by validate_interaction_map + phenotype required edges; **full runtime** behaviour still needs phenotype or golden-level assertions for regressions that validators miss. |

---

## 6. Recommendation — governed shape

### Final recommendation label

**SPLIT_INTO_PHENOTYPE_FIXTURE_AND_REGRESSION_PHASES**

### Rationale (concise)

- **Phase 1 — Regression / gate integration (must be mergeable on its own):** Add `test_phenotype_suite_v1.py` (or equivalent consolidated pytest entry) to `run_baseline_tests.py` / `golden_gate_local.py` so the **declared** suite is **non-optional** for governed finishes. Optionally publish a short **coverage matrix** (phenotype_id → enforced dimensions: signals / chains / root-cause / deterministic).
- **Phase 2 — Map + expectation + fixture promotion:** Sequentially promote **pending** phenotypes to **`enforced`** where `interaction_map_v1.yaml` and research refs satisfy validate scripts and product intent — avoid folding gate wiring and large expectation bumps into one undisciplined diff.

This split respects roadmap anti-drift intent for Wave 4 without violating the spirit of “avoid micro-sprint fragmentation” (two **sequential governed phases**, each with a single exit criterion).

**Alternative considered:** **PROCEED_AS_ONE_BOUNDED_SPRINT** — acceptable only if the sprint charter explicitly orders **(1) gate wiring first, (2) then at most one phenotype promotion**, with a hard scope cap; otherwise merge risk and review blur increase.

**Not chosen:** **DO_NOT_PROCEED_NO_CLEAR_GAP** — incorrect; gate bypass of phenotype suite is a **verified** structural gap.

### If proceeding — likely touched surfaces

- `backend/scripts/run_baseline_tests.py` (and/or `golden_gate_local.py` checklist)
- `backend/tests/unit/test_phenotype_suite_v1.py` (split parametrisation / performance only if needed)
- `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`
- `knowledge_bus/phenotypes/phenotype_map_v1.yaml`
- Possibly `knowledge_bus/interaction_maps/interaction_map_v1.yaml` when promoting edges
- Docs: short “phenotype gate” note under `docs/` or automation_bus readme (governance only)

---

## 7. Boundary check — out of scope for KB-S58 (phenotype/fixture/regression wave)

Per roadmap separation of Wave 4 threads (§668–708), KB-S58 **structural** lineage should **exclude**:

- **Frontend** visualisation, FE-PAGES, FE-ACCOUNT (parallel roadmap items; not prerequisites for phenotype gate honesty).
- **New retail explainer** copy or registry expansion (**separate** enforcement path already in `run_baseline_tests.py`).
- **Unrelated package ingestion** or “Batch N” breadth unless a phenotype **explicitly** requires new markers for an enforced constellation (preflight should re-justify).
- **Broad reporting-policy redesign** beyond what is needed to assert **existing** `report_v1.root_cause_v1` fields in expectations.
- **General engine redesign** not justified by failing phenotype expectations or validator evidence.

---

## 8. Required chat outputs (summary)

| Item | Value |
|------|--------|
| **Artifact** | `docs/investigations/KB_S58_PREFLIGHT.md` |
| **Executive summary** | Suite of nine phenotypes + unit harness is **mature**; automation **gate omits** that harness; **seven** phenotypes remain chain-**pending**; roadmap **KB-S58** label collides with ingestion history — use §695–697 definition. **Proceed** with structural hardening. |
| **Final recommendation** | **SPLIT_INTO_PHENOTYPE_FIXTURE_AND_REGRESSION_PHASES** |

---

*End of preflight — READ_ONLY; no repo mutations beyond this document.*
