# KB-S50 Preflight — WHY Expansion 3: Iron / Oxygen + Iron Overload Phenotype

**Mode:** Read-only investigation (no code, prompts, or work-package execution).  
**Date:** 2026-04-04  
**Basis:** Live repository — `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, `knowledge_bus/interaction_maps/interaction_map_v1.yaml` (revision 1.1.2), `backend/core/analytics/root_cause_compiler_v1.py`, `knowledge_bus/root_cause/hypotheses/`, `knowledge_bus/phenotypes/phenotype_map_v1.yaml`, `backend/tests/fixtures/panels/phenotypes/*`, `SignalRegistry` (backend), `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`, `knowledge_bus/registries/confirmatory_tests_v1.yaml`.

---

## 1. Executive summary

**Maturity today:** Iron and oxygen transport are **materially present in the signal layer** (multiple canonical IDs, including post–KB-S61 transferrin signals) and **partially present in the interaction map** as a **ferritin → haemoglobin → MCV** chain with **CRP ↔ ferritin** modulation. **Contextual and overload frames** (`signal_iron_deficiency_context`, `signal_iron_overload_context`, `signal_oxygen_transport_capacity`) exist at **runtime** but are **not nodes** in `interaction_map_v1.yaml`, and **no iron/oxygen signal is registered in `_ROOT_CAUSE_TARGETS`**, so **`compile_root_cause_v1` produces no iron-specific findings** when those signals fire (unless another unrelated WHY target also fires).

**Key gaps:**

| Layer | Gap |
|--------|-----|
| **WHY** | No dedicated hypothesis YAMLs for iron/oxygen signals; **no** `_ROOT_CAUSE_TARGETS` entries. |
| **Interaction map** | No hub nodes for **iron deficiency context**, **iron overload**, **oxygen transport capacity**, **ferritin high**, or **transferrin**; **phenotype-governed** edge **CRP → `signal_iron_deficiency_context`** is documented in `phenotype_map_v1.yaml` but **absent** from the interaction map (placeholder rationale pending promotion). |
| **Phenotype** | **Deficiency + inflammation** pattern exists (`ph_iron_deficiency_inflammation_v1`); **no** dedicated **iron overload** phenotype or synthetic fixture in repo. Harness **does not require** root-cause for iron phenotype (`expected_root_cause.must_exist: false`). |
| **Confirmatory tests registry** | **No** iron/ferritin/transferrin-specific `test_id` entries (unlike lipid TyG panel tests). Authors must reuse **FBC/B12/folate/MMA**-style tests or accept **minimal** confirmatory lists — same class of constraint as KB-S48 hardening. |

**KB-S48 pattern analogue:** Lipids required a **bounded interaction-map prerequisite** because a hub signal was missing from the map while phenotypes depended on it. Iron repeats that pattern for **`signal_iron_deficiency_context`** (and similarly for **overload / oxygen capacity** if those are treated as first-class reasoning anchors). **Recommendation: `WHY_PLUS_BOUNDED_PREREQUISITE`**, not a pure hypothesis sprint.

---

## 2. Signal inventory

### 2.1 Runtime signals (`SignalRegistry` — iron / oxygen / red-cell filter)

Enumeration used keyword substrings: `iron`, `ferritin`, `hemoglobin`, `hemat`, `oxygen`, `transferrin`, `saturation`, `anemia`, `mcv`, `rdw`, `erythro`.

| Canonical `signal_id` | Notes |
|---------------------|--------|
| `signal_iron_deficiency_context` | Context wrapper; **phenotype-required** for `ph_iron_deficiency_inflammation_v1`. |
| `signal_iron_overload_context` | Context wrapper; strategic overload frame; **no** phenotype fixture today. |
| `signal_oxygen_transport_capacity` | Oxygen transport framing; **not** on interaction map. |
| `signal_ferritin_low` | On interaction map; edges to Hb / MCV. |
| `signal_ferritin_high` | **Not** on interaction map. |
| `signal_hemoglobin_low` | On interaction map. |
| `signal_hematocrit_low` | **Not** on interaction map. |
| `signal_mcv_high` | On interaction map. |
| `signal_rdw_cv_high` | **Not** on interaction map. |
| `signal_rdw_sd_high` | **Not** on interaction map. |
| `signal_transferrin_high` | KB-S61 packages; **not** on interaction map. |
| `signal_transferrin_low` | KB-S61 packages; **not** on interaction map. |

**Derived / saturation:** Packages reference biomarker **`transferrin_saturation`** in research text; there is **no** separate `signal_transferrin_saturation_*` ID in the filtered registry list above (saturation may contribute to **context** signals via package logic — sprint author should confirm in evaluator paths).

**Actively firing:** Signals are **registered** and will fire when packages and lab data satisfy thresholds; no preflight execution run was performed. **Fixtures:** synthetic `ph_iron_deficiency_inflammation_v1.json` is built to exercise **iron deficiency + CRP**; AB/VR full panels include **ferritin, iron, haemoglobin, haematocrit, transferrin** biomarkers.

---

## 3. WHY coverage table

`_ROOT_CAUSE_TARGETS` ( `root_cause_compiler_v1.py` ) currently ends with lipid KB-S48 entries; **none** of the iron/oxygen IDs below are registered.

| Signal | Hypothesis YAML (dedicated) | Registered in compiler | `compile_root_cause_v1` finding when this signal fires alone? |
|--------|---------------------------|-------------------------|----------------------------------------------------------------|
| `signal_iron_deficiency_context` | No | No | No |
| `signal_iron_overload_context` | No | No | No |
| `signal_oxygen_transport_capacity` | No | No | No |
| `signal_ferritin_low` | No | No | No |
| `signal_ferritin_high` | No | No | No |
| `signal_hemoglobin_low` | No | No | No |
| `signal_hematocrit_low` | No | No | No |
| `signal_mcv_high` | No | No | No |
| `signal_rdw_cv_high` / `signal_rdw_sd_high` | No | No | No |
| `signal_transferrin_high` / `signal_transferrin_low` | No | No | No |

**Partial / indirect:** `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` states ferritin is referenced in `hcy_hypotheses_v1.yaml`; **current `knowledge_bus/root_cause/hypotheses/` has no `ferritin` string matches** — treat that audit row as **stale** for Hcy. **No** full WHY path for iron exists today.

**Compiler `None` behaviour:** `compile_root_cause_v1` returns **`None` only when the findings list is empty** (i.e. **no** registered target is `suboptimal` / `at_risk`). Iron-only panels therefore yield **`None`** unless another registered target also fires.

---

## 4. Interaction-map assessment

**File:** `knowledge_bus/interaction_maps/interaction_map_v1.yaml` (v1.1.2).

**Iron-related nodes present:** `signal_ferritin_low`, `signal_hemoglobin_low`, `signal_mcv_high` (hematologic / other).

**Iron-related edges present (Pathway 2):**

- `signal_ferritin_low` → `signal_hemoglobin_low` (driver, consensus)  
- `signal_hemoglobin_low` → `signal_mcv_high` (co_occurrence)  
- `signal_ferritin_low` → `signal_mcv_high` (consequence)  
- `signal_crp_high` → `signal_ferritin_low` (co_occurrence, exploratory)

**Missing for coherent “iron / oxygen” reasoning (structural):**

- **No** `signal_iron_deficiency_context`, `signal_iron_overload_context`, or `signal_oxygen_transport_capacity` **nodes**.  
- **No** edges involving **`signal_ferritin_high`**, **`signal_transferrin_high` / `signal_transferrin_low`**, **`signal_hematocrit_low`**, **RDW** signals.  
- **No** edge matching phenotype **`signal_crp_high` → `signal_iron_deficiency_context`** (governed in `phenotype_map_v1.yaml` with `requires_research_promotion: true` and rationale placeholder).

**Validator constraint (KB-S48 lesson):** New edges must appear in **`phenotype_map_v1.yaml` `required_edges`** (or equivalent governance) or `validate_interaction_map_v1` will **fail** uncovered edges. Any KB-S50 map expansion must stay **minimal** and **phenotype-aligned**.

---

## 5. Phenotype alignment

### 5.1 `phenotype_map_v1.yaml`

- **`ph_iron_deficiency_inflammation_v1`:** Requires **`signal_iron_deficiency_context`** + **`signal_crp_high`**. Documents **CRP → iron deficiency context** (research promotion), **ferritin → Hb**, **Hb → MCV**, **ferritin → MCV**, **CRP → ferritin**. **`chain_expectations.status: pending`**.  
- **Iron overload phenotype:** **None** in `phenotype_map_v1.yaml` (matches `METABOLIC_PATHWAY_COVERAGE_AUDIT` gap).

### 5.2 Fixtures and harness

- **Fixture:** `backend/tests/fixtures/panels/phenotypes/ph_iron_deficiency_inflammation_v1.json` — low ferritin, low iron, high CRP, low Hb.  
- **`phenotype_expectations_v1.yaml`:** `must_fire` includes **`signal_iron_deficiency_context`**; **`expected_root_cause.must_exist: false`**; chains **not** enforced.

### 5.3 Gap vs runtime

Phenotype logic **expects** a **context** signal and **inflammation coupling**; the interaction map **does not** yet include the **CRP → iron deficiency context** edge or a **hub node** for that context. **Overload** and **oxygen capacity** lack phenotype scaffolding.

---

## 6. AB / VR and commercial relevance

- **AB (`ab_full_panel_with_ranges.json`):** Includes **ferritin, iron, haemoglobin, haematocrit, transferrin** (and related CBC context). Example excerpt: **transferrin** at **2.0 g/L** vs lab **min 2.15** (borderline low); **ferritin** in-range on the same fixture — so the harness **can** touch transferrin/iron biology but **does not** guarantee iron deficiency or overload storytelling.  
- **VR:** Same marker keys present.  
- **Commercial:** Full blood panels commonly include **FBC + ferritin + iron studies**; **WHY absence** for iron means the product can **surface signals** without **governed root-cause narrative** for those targets.

---

## 7. Strategic alignment (v1.5)

From **`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`** — **KB-S50**:

- **Purpose:** Deepen **iron and oxygen-transport reasoning**, including **overload** and **deficiency** frames.  
- **Strategic value:** Common domain, phenotype relevance, **important current gap**.

Wave 2 also expects the application to **reason more credibly across iron** and **oxygen transport** — consistent with treating **`signal_oxygen_transport_capacity`** and **overload context** as first-class, not optional afterthoughts.

---

## 8. Recommendation

### 8.1 Sprint shape

**`WHY_PLUS_BOUNDED_PREREQUISITE`**

**Rationale:** Match **KB-S48**: hypothesis assets + compiler registration **alone** do not fix **missing interaction-map hubs** and **phenotype-documented edges** that the validator governs. A **minimal** map step (nodes + edges already allowed or promoted via phenotype/research path) should precede or ship in the **same** bounded tranche as WHY, so reasoning is **structurally coherent** and **phenotype-aligned**.

**Not recommended as default:** **`PURE_WHY`** — unless KB-S50 is **explicitly narrowed** to **only** signals already on the map (`ferritin_low`, `hemoglobin_low`, `mcv_high`) and **defers** context/overload/oxygen/transferrin to later workpackages (would **under-deliver** v1.5 wording).

### 8.2 Exact signals in scope (proposal for sprint author)

**Tier A — strategic anchors (WHY + map/phenotype alignment):**

- `signal_iron_deficiency_context`  
- `signal_iron_overload_context`  
- `signal_oxygen_transport_capacity`  

**Tier B — high-traffic leaf / chain signals (WHY):**

- `signal_ferritin_low`, `signal_ferritin_high`  
- `signal_hemoglobin_low`  
- `signal_transferrin_high`, `signal_transferrin_low`  

**Tier C — optional / follow-on (WHY or deferred):**

- `signal_hematocrit_low`, `signal_mcv_high`, `signal_rdw_cv_high`, `signal_rdw_sd_high` — already partially **map-connected** for ferritin/Hb/MCV; **MCV/RDW** may be **supporting** hypotheses rather than primary `_ROOT_CAUSE_TARGETS` if sprint scope must stay tight.

Sprint author should **freeze** Tier A+B in the work package charter to avoid uncontrolled growth.

### 8.3 Iron overload phenotype: introduce or defer?

| Option | When |
|--------|------|
| **Introduce in KB-S50 (bounded)** | If v1.5 **overload** intent is in charter: add **`ph_iron_overload_*`** (or equivalent) **+** synthetic fixture **+** minimal `phenotype_map` / `phenotype_expectations` rows **only** as explicitly scoped — still **governed**, not speculative biology. |
| **Defer** | If KB-S50 is **WHY + map only** for deficiency/oxygen first: **defer** dedicated overload phenotype to **KB-S50b** or Wave 2 follow-on, but **still** add **`signal_iron_overload_context`** WHY assets if overload framing is required elsewhere. |

**Preflight recommendation:** **Do not defer overload reasoning entirely** if KB-S50 title and v1.5 **explicitly** include overload — either **minimal phenotype scaffolding** **or** **overload WHY-only** with **map node** in the same bounded prerequisite. **Defer** a **rich** overload phenotype suite (multiple patterns) if it risks scope creep.

### 8.4 Confirmatory registry

Expect **reuse** of `test_full_blood_count_indices_v1`, B12/folate/MMA tests, and similar **until** a **separate governed registry sprint** adds iron-panel `test_id`s (registry change is **out of scope** for this preflight document but is a **planning dependency** for hypothesis authoring).

---

## 9. Audit doc staleness note

`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` **predates** KB-S46/KB-S48 lipid and inflammation WHY work; its **iron** row is still broadly right on **missing iron WHY**, but **systemic inflammation / lipid** columns are **obsolete**. KB-S50 planning should **re-verify** against **current** `_ROOT_CAUSE_TARGETS` and **this** preflight, not the audit alone.

---

**Artifact path:** `docs/investigations/KB-S50_IRON_OXYGEN_PREFLIGHT.md`
