# KB-S52 Preflight — Wave 2 Remaining Workpackage (v1.5 aligned)

**Mode:** Read-only investigation (no implementation, prompts, or sprint execution).  
**Date:** 2026-04-04  
**Basis:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`, `knowledge_bus/interaction_maps/interaction_map_v1.yaml` (revision 1.1.3), `backend/core/analytics/root_cause_compiler_v1.py`, `knowledge_bus/root_cause/hypotheses/`, `knowledge_bus/phenotypes/phenotype_map_v1.yaml`, `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`, `SignalRegistry` (backend), `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`, `ab_full_panel_with_ranges.json` (spot-check).

---

## Naming clarity (avoid scope drift)

| Label | Meaning |
|--------|---------|
| **KB-S52 (this preflight)** | **WHY Expansion 4: Hepatic Extension + Thyroid Completion** — Wave 2 strategic workpackage. |
| **KB-S52C / KB-S52D** | **Historical ingestion / remap lineage** (Wave A/B packages `pkg_kb52c_*`, `pkg_kb52d_*`). Strategy marks Batch 3–4 ingestion **complete**; that is **not** the same deliverable as **KB-S52 WHY Expansion 4**. |

This document addresses **KB-S52 WHY Expansion 4** only.

---

## 1. Executive summary

**Strategic intent (v1.5):** KB-S52 exists to **deepen hepatic and thyroid explanation beyond current partial coverage** and to **strengthen system-level reasoning** in those control systems, consistent with Wave 2’s goal to reason more convincingly across **hepatic** and **thyroid** alongside iron/oxygen (already advanced by KB-S50).

**Current maturity:**

| Layer | Hepatic domain | Thyroid domain |
|--------|----------------|----------------|
| **Runtime signals** | **Strong breadth** — multiple hepatic-related IDs (e.g. `signal_ggt_high`, `signal_alt_high`, `signal_hepatic_alt_context`, `signal_hepatic_metabolic_stress`, ALP/bilirubin/hyperbilirubinemia signals). **No** standalone `signal_ast_*` ID (AST appears as a **biomarker** in ALT hypotheses, not as a fired signal ID). | **Strong breadth** — `signal_thyroid_tsh_context`, `signal_tsh_high` / `signal_tsh_low`, free T3/T4 high/low, antibody signals. |
| **Interaction map** | **Partial** — `signal_ggt_high` and `signal_alt_high` are **nodes** with **metabolic/inflammatory** edges; **`signal_hepatic_metabolic_stress`**, **`signal_alp_high` / low**, **bilirubin / hyperbilirubinemia** signals are **not** map nodes. | **Partial** — `signal_tsh_high`, `signal_tsh_low`, `signal_thyroid_tsh_context` are **nodes** with **lipid/metabolic** edges; **free T3/T4** and **antibody** signals are **not** on the map. |
| **WHY (`root_cause_v1`)** | **Narrow** — only **`signal_hepatic_alt_context`** is in `_ROOT_CAUSE_TARGETS` (`alt_hypotheses_v1.yaml`). **`signal_ggt_high`** and other hepatic IDs have **no** dedicated hypothesis assets or compiler registration. | **Narrow** — only **`signal_thyroid_tsh_context`** is in `_ROOT_CAUSE_TARGETS` (`tsh_hypotheses_v1.yaml`). **`signal_tsh_high`**, **`signal_tsh_low`**, and **hormone/antibody** signals have **no** dedicated hypothesis assets or compiler registration. |
| **Phenotype** | Harness expects **`signal_hepatic_alt_context`** for `ph_hepatic_alt_inflammatory_v1` with **enforced** root-cause for that target; **GGT-led** and **composite hepatic stress** patterns lack dedicated phenotype rows beyond what is implied by metabolic phenotypes. | Harness expects **`signal_thyroid_tsh_context`** for thyroid phenotypes with **enforced** root-cause; **isolated TSH high/low** or **FT3/FT4**-led framing is **not** separately scaffolded. |

**Key gaps:** (1) **Leaf and composite hepatic/thyroid signals** fire at runtime but **do not** emit **signal-specific** WHY findings. (2) **Interaction map** does not yet reflect **full** hepatic marker surface or **thyroid hormone / antibody** layers. (3) **`validate_interaction_map_v1`** ties **new edges** to **`phenotype_map_v1.yaml` `required_edges`** — any structural expansion remains **governed**. (4) **`confirmatory_tests_v1.yaml`** remains **small** (~13 tests, no hepatic/thyroid-specific panel entries) — same **constraint** as KB-S48/KB-S50 unless a **separate** registry sprint is authorised (out of scope for this preflight’s implementation assumptions).

---

## 2. Domain definition (what KB-S52 is trying to build)

Per **v1.5** — **KB-S52 — WHY Expansion 4: Hepatic Extension + Thyroid Completion**:

- **Purpose:** Deepen **hepatic** and **thyroid** explanation **beyond** today’s **partial** coverage.  
- **Strategic value:** Stronger **system-level** reasoning in **important control systems**.  
- **Wave 2 fit:** Supports the wave goal that the application should **cover hepatic and thyroid reasoning more convincingly** (together with iron/oxygen, product shell, etc.).

**Concrete product interpretation (for sprint authoring):**

- **Hepatic extension:** Move from **ALT-context-only** WHY toward **additional governed targets** (e.g. **GGT-first**, **ALP**, **bilirubin / cholestatic framing**, **`signal_hepatic_metabolic_stress`**) as charter allows — without conflating **ingestion** (KB-S52C/D) with **WHY**.  
- **Thyroid completion:** Move from **TSH-context-only** WHY toward **TSH high/low** and optionally **FT3/FT4** (and, if in charter, **antibody**) **signal-level** reasoning, aligned to map and phenotype governance.

---

## 3. Signal inventory (canonical IDs — registry pass)

### 3.1 Hepatic-related (representative filter: hepatic, ggt, alt, bilirubin, alp, liver)

| `signal_id` | On `interaction_map_v1` nodes? |
|-------------|-----------------------------------|
| `signal_hepatic_alt_context` | No (context signal; edges involve `signal_alt_high`) |
| `signal_alt_high` | Yes |
| `signal_ggt_high` | Yes |
| `signal_hepatic_metabolic_stress` | **No** |
| `signal_alp_high` | **No** |
| `signal_alp_low` | **No** |
| `signal_bilirubin_high` | **No** |
| `signal_hyperbilirubinemia` | **No** |

**Note:** No **`signal_ast_high`** (or similar) in registry; **AST** is used inside **`alt_hypotheses_v1`** as a **marker**, not as a primary `_ROOT_CAUSE_TARGETS` key.

### 3.2 Thyroid-related (representative filter: thyroid, tsh, t3, t4, tgab, tpo)

| `signal_id` | On `interaction_map_v1` nodes? |
|-------------|-----------------------------------|
| `signal_thyroid_tsh_context` | Yes |
| `signal_tsh_high` | Yes |
| `signal_tsh_low` | Yes |
| `signal_free_t3_high` / `signal_free_t3_low` | **No** |
| `signal_free_t4_high` / `signal_free_t4_low` | **No** |
| `signal_tgab_high` | **No** |
| `signal_tpo_ab_high` | **No** |

---

## 4. WHY coverage (`_ROOT_CAUSE_TARGETS` + hypothesis assets)

**Registered with dedicated hypothesis YAML + compiler tuple:**

| Signal | Hypothesis asset | Finding when fired alone (suboptimal/at_risk)? |
|--------|------------------|--------------------------------------------------|
| `signal_hepatic_alt_context` | `alt_hypotheses_v1.yaml` | **Yes** |
| `signal_thyroid_tsh_context` | `tsh_hypotheses_v1.yaml` | **Yes** |

**Not registered (no dedicated Tier for KB-S52 domain leaves in compiler):**  
All other IDs in §3 — including **`signal_ggt_high`**, **`signal_hepatic_metabolic_stress`**, **`signal_tsh_high`**, **`signal_tsh_low`**, ALP/bilirubin/free hormone/antibody signals — **do not** produce their **own** `RootCauseFindingV1` rows today.

**Partial interpretation:** Existing **ALT** and **TSH context** hypotheses already reference **GGT**, **AST**, **free_t4**, etc. as **markers**; that is **not** a substitute for **signal-ID-targeted** WHY when **`signal_ggt_high`** or **`signal_tsh_high`** fires **without** the context wrapper firing.

---

## 5. Interaction-map assessment

**Revision:** 1.1.3 (current).

**Hepatic-relevant structure today:**

- Metabolic → **GGT** / **ALT**; **ALT** / **GGT** → **CRP**; links into inflammatory → vascular chain.  
- **No** nodes for **`signal_hepatic_metabolic_stress`**, **ALP**, **bilirubin** classes.  
- **No** “hub” equivalent to lipid/iron **context** nodes for **composite hepatic stress** (unless future sprint introduces one under governance).

**Thyroid-relevant structure today:**

- **Thyroid TSH context** and **TSH high/low** → **LDL** / **HDL** → **HbA1c** (lipid–metabolic bridge).  
- **No** edges involving **free T3/T4** or **antibody** signals (they are **not** map nodes).

**Structural gap summary:** KB-S52 **completion** in the **structural** sense likely requires **either** (a) **new nodes + edges** with matching **`phenotype_map` `required_edges`**, or (b) a **deliberately narrow** charter that adds **hypothesis-only** registration for signals **already** on the map **without** claiming new chains.

---

## 6. Phenotype alignment

**Present:**

- **`ph_hepatic_alt_inflammatory_v1`** — requires **`signal_hepatic_alt_context`**; **`phenotype_expectations_v1.yaml`** enforces **root_cause** for **`signal_hepatic_alt_context`**.  
- **`ph_tsh_axis_metabolic_v1`**, **`ph_thyroid_lipid_disturbance_v1`** — centre **`signal_thyroid_tsh_context`**; expectations enforce **root_cause** for that target where configured.  
- Metabolic phenotypes reference **ALT** / **GGT** edges that **already exist** on the interaction map.

**Mismatch / opportunity:**

- **GGT-high** and **TSH-high/low**-led panels can **fire** without **`signal_hepatic_alt_context`** or **`signal_thyroid_tsh_context`**, yielding **no** dedicated WHY finding for those **fired** rows.  
- **No** phenotype row **requires** `signal_ggt_high` or `signal_tsh_high` **as the** `expected_root_cause.applies_to_signal_id` target today (by design of current expectations).

**New scaffolding:** Optional **minimal** phenotypes (stubs) for **GGT-led** or **TSH-leaf** patterns would **mirror** KB-S50 overload stub **only if** the charter explicitly includes phenotype work; otherwise KB-S52 can remain **hypothesis + compiler (+ optional map)** only.

---

## 7. AB / VR relevance

**AB full panel** includes **ALT, GGT, bilirubin, free_t4, TSH** (and related thyroid markers in a full lab). That makes hepatic and thyroid domains **commercially visible** on real-style panels.

**Reasoning depth:** Where only **leaf** signals fire (e.g. **GGT** without ALT context), **root_cause_v1** may still be **populated** by **other** targets (e.g. lipids, iron) but **not** by a **hepatic/thyroid-specific** finding for that leaf — **gap is user-visible** for “why is GGT/TSH abnormal?” style questions.

---

## 8. Structural integrity (SSOT / schema / pipeline)

**Can KB-S52 be executed without SSOT, schema, or core pipeline changes?**

- **Often yes** for a **minimal** slice: **new hypothesis YAMLs** + **`load_root_cause_hypotheses.py`** + **`root_cause_compiler_v1.py`** only — matching KB-S46/KB-S48/KB-S50 patterns — **provided** **`confirmatory_tests` references stay within** `confirmatory_tests_v1.yaml` (no registry expansion per current governance discipline).  
- **No** if the charter requires **new interaction-map edges**: **`phenotype_map_v1.yaml`** must **authorize** those edges for **`validate_interaction_map_v1`** — that is **not** SSOT/schema/pipeline, but it is **bounded structural** work.  
- **Pipeline / evaluator** changes are **not** required **merely** to register new `_ROOT_CAUSE_TARGETS` **if** signals already evaluate correctly.

---

## 9. Recommendation

### 9.1 Sprint shape

**`EXTENSION_PLUS_BOUNDED_PREREQUISITE`** **as the default** authoring stance for KB-S52 **as named in v1.5** (“extension **+ completion**”), because:

1. **Completion** implies going **beyond** the two **context** compilers already in place.  
2. **True** “thyroid completion” and **hepatic extension** **either** need **map/phenotype alignment** for new chains **or** an explicit **narrowing** of the workpackage to **hypothesis-only** for **already-mapped** signals.

**`PURE_EXTENSION`** is appropriate **only** if the **authorised charter explicitly limits** KB-S52 to:

- adding **hypothesis assets + `_ROOT_CAUSE_TARGETS`** for a **closed list** of **already-mapped** signals (e.g. **`signal_ggt_high`**, **`signal_tsh_high`**, **`signal_tsh_low`** only), **without** claiming new interaction chains or new phenotype stubs.

### 9.2 Suggested signals in scope (for charter freeze — illustrative)

**Tier 1 (high leverage, already on interaction map, no new map nodes required for basic WHY):**

- `signal_ggt_high`  
- `signal_tsh_high`  
- `signal_tsh_low`  

**Tier 2 (hepatic extension — likely needs map + phenotype governance **if** chains are claimed):**

- `signal_hepatic_metabolic_stress`  
- `signal_alp_high` (and/or `signal_alp_low` if charter includes)  
- `signal_bilirubin_high` / `signal_hyperbilirubinemia` (pick **one** canonical framing in charter to avoid duplication)  

**Tier 3 (thyroid completion — hormone / antibody layer):**

- `signal_free_t4_high` / `signal_free_t4_low`  
- `signal_free_t3_high` / `signal_free_t3_low`  
- `signal_tgab_high`, `signal_tpo_ab_high` (only if charter includes autoimmune framing)

### 9.3 Additional structural work

| If sprint goal includes… | Prerequisite |
|----------------------------|--------------|
| **New interaction-map edges** | Update **`phenotype_map_v1.yaml` `required_edges`** (or research promotion path) so **`validate_interaction_map_v1` PASS**. |
| **New phenotype stubs** | **`phenotype_map_v1.yaml`** + fixture + **`phenotype_expectations_v1.yaml`** (minimal, KB-S50-style). |
| **Richer confirmatory tests** | **Separate** governed registry work (**not** assumed inside KB-S52 unless explicitly in scope). |

---

## 10. Audit doc note

`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` **predates** KB-S48/KB-S50; its **hepatic/thyroid** rows understate current **lipid/iron/inflammation** WHY progress. Use **this preflight + live `_ROOT_CAUSE_TARGETS`** for KB-S52 planning.

---

**Artifact path:** `docs/investigations/KB-S52_PREFLIGHT.md`
