# KB-S52B Preflight — Hepatic / Thyroid Completion Follow-on

**Mode:** Read-only investigation (this artifact only). No implementation, prompts, or sprint execution.  
**Date:** 2026-04-04  
**Work ID:** KB-S52B-PREFLIGHT  
**Basis:** `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` (Wave 2 — KB-S52 lineage), `docs/investigations/KB-S52_PREFLIGHT.md`, live `knowledge_bus/interaction_maps/interaction_map_v1.yaml` (revision 1.1.3), `knowledge_bus/phenotypes/phenotype_map_v1.yaml`, `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml`, `backend/core/analytics/root_cause_compiler_v1.py`, `knowledge_bus/root_cause/hypotheses/`, `knowledge_bus/registries/confirmatory_tests_v1.yaml`, `knowledge_bus/packages/*/signal_library.yaml` (SignalRegistry source), AB/VR panel fixtures.

---

## 1. Executive summary

**After KB-S52 Tier 1:** The compiler already registers **`signal_ggt_high`**, **`signal_tsh_high`**, and **`signal_tsh_low`** with dedicated hypothesis assets (`ggt_high_hypotheses_v1.yaml`, `tsh_high_hypotheses_v1.yaml`, `tsh_low_hypotheses_v1.yaml`) and `_ROOT_CAUSE_TARGETS` tuples in `root_cause_compiler_v1.py`. Context compilers **`signal_hepatic_alt_context`** and **`signal_thyroid_tsh_context`** remain as before.

**What remains for “hepatic extension + thyroid completion” (KB-S52B scope):** the **closed exclusion set** from Tier 1 — hepatic composite/marker signals (metabolic stress, ALP, bilirubin framing) and thyroid hormone + autoimmune antibody signals — **still have no dedicated root-cause rows** when they fire in isolation or as primaries.

**Key structural gaps:** None of the eleven target IDs below appear as **`nodes`** in `interaction_map_v1.yaml` (revision 1.1.3). The map today ends with the thyroid→lipid→metabolic edges anchored on **`signal_thyroid_tsh_context`** / **`signal_tsh_high`** / **`signal_tsh_low`** and the metabolic→hepatic path on **`signal_ggt_high`** / **`signal_alt_high`**.

**Key WHY gaps:** No dedicated `*_hypotheses_v1.yaml` files and **no** `_ROOT_CAUSE_TARGETS` entries for any of the eleven signals in §3. `compile_root_cause_v1` therefore **does not** emit a `RootCauseFindingV1` for those `signal_id`s when they are the fired targets.

**Confirmatory constraint:** `confirmatory_tests_v1.yaml` remains small and **does not** define hepatic/thyroid tests keyed to the excluded signals. New hypotheses **must** reference **only** existing `test_id` values or the compiler raises `ValueError` (`root_cause_compiler_v1.py`, unknown `test_id` path). Richer panel-specific confirmatory rows are a **separate bounded prerequisite** if the charter requires them.

---

## 2. Remaining-signal inventory

**Runtime authority:** `SignalRegistry` loads every `knowledge_bus/packages/*/signal_library.yaml` (excluding `pkg_example`). The following packages define the listed `signal_id`s (duplicate `signal_id` across packages is resolved deterministically by path order in the registry loader).

### 2.1 Hepatic (remaining)

| `signal_id` | Present in package `signal_library.yaml` (runtime registry) |
|-------------|---------------------------------------------------------------|
| `signal_hepatic_metabolic_stress` | Yes — `pkg_hepatic_metabolic_stress/signal_library.yaml`, `KBP-0001/signal_library.yaml` |
| `signal_alp_high` | Yes — `pkg_kb52c_alp_high_cholestatic_pattern/`, `pkg_s24_alp_high_bone_biliary/` |
| `signal_alp_low` | Yes — `pkg_kb56_alp_low_*` (two packages) |
| `signal_bilirubin_high` | Yes — `pkg_kb52c_bilirubin_high_hepatobiliary_excretion_impairment/` |
| `signal_hyperbilirubinemia` | Yes — `pkg_kb45_bilirubin_high_hyperbilirubinemia/` |

**Note:** `signal_bilirubin_high` and `signal_hyperbilirubinemia` are **distinct** canonical IDs; charter should avoid treating them as interchangeable without an explicit product rule.

### 2.2 Thyroid (remaining)

| `signal_id` | Present in package `signal_library.yaml` |
|-------------|--------------------------------------------|
| `signal_free_t3_high` | Yes — `pkg_kb47_free_t3_high_t3_predominant_thyrotoxicosis/` |
| `signal_free_t3_low` | Yes — `pkg_kb47_free_t3_low_low_t3_syndrome/` |
| `signal_free_t4_high` | Yes — `pkg_kb47_free_t4_high_thyrotoxicosis_context/` |
| `signal_free_t4_low` | Yes — `pkg_kb47_free_t4_low_thyroid_hormone_deficiency/` |
| `signal_tgab_high` | Yes — `pkg_kb59_tgab_high_*` (two packages) |
| `signal_tpo_ab_high` | Yes — `pkg_kb59_tpo_ab_high_*` (two packages) |

### 2.3 Interaction map presence (structural, not runtime)

**None** of the eleven IDs appear under `nodes:` in `interaction_map_v1.yaml` (grep pass on current file; nodes list includes `signal_ggt_high`, `signal_alt_high`, `signal_tsh_*`, `signal_thyroid_tsh_context`, lipids, iron, homocysteine, etc., but **not** the KB-S52B remainder).

---

## 3. WHY coverage table

**Compiler rule:** `compile_root_cause_v1` builds findings **only** for tuples in `_ROOT_CAUSE_TARGETS` (`root_cause_compiler_v1.py`). A fired signal **not** in that list produces **no** finding for that signal.

| signal | Runtime exists (SignalRegistry) | Dedicated WHY YAML in `knowledge_bus/root_cause/hypotheses/` | Registered in `_ROOT_CAUSE_TARGETS` | `compile_root_cause_v1` emits finding when this signal fires (suboptimal/at_risk)? |
|--------|----------------------------------|----------------------------------------------------------------|----------------------------------------|-------------------------------------------------------------------------------------|
| `signal_hepatic_metabolic_stress` | Yes | No | No | **No** |
| `signal_alp_high` | Yes | No | No | **No** |
| `signal_alp_low` | Yes | No | No | **No** |
| `signal_bilirubin_high` | Yes | No | No | **No** |
| `signal_hyperbilirubinemia` | Yes | No | No | **No** |
| `signal_free_t3_high` | Yes | No | No | **No** |
| `signal_free_t3_low` | Yes | No | No | **No** |
| `signal_free_t4_high` | Yes | No | No | **No** |
| `signal_free_t4_low` | Yes | No | No | **No** |
| `signal_tgab_high` | Yes | No | No | **No** |
| `signal_tpo_ab_high` | Yes | No | No | **No** |

**Indirect coverage:** `alt_hypotheses_v1.yaml` and `tsh_hypotheses_v1.yaml` (and Tier 1 assets for GGT / TSH high/low) reference markers such as AST, free T4, etc. That **does not** substitute for **signal-ID-targeted** findings when e.g. **`signal_free_t4_low`** or **`signal_alp_high`** fires **without** the context or Tier-1 targets firing.

---

## 4. Interaction-map assessment

### 4.1 What exists today (relevant excerpt)

- **Hepatic on map:** `signal_ggt_high`, `signal_alt_high` (with metabolic and inflammatory edges).  
- **Thyroid on map:** `signal_thyroid_tsh_context`, `signal_tsh_high`, `signal_tsh_low` (with lipid and metabolic edges).

### 4.2 What is missing

All **eleven** KB-S52B remainder signals: **no nodes**, **no edges**.

### 4.3 Mandatory vs optional map work

| Goal | Map work |
|------|----------|
| **Tier-1-style local WHY** — hypotheses grounded in **markers**, **fired_signals** rules, and existing edges only as **optional** context (same pattern as `ggt_high_hypotheses_v1` / `tsh_high_hypotheses_v1`) | **Optional** — no new nodes/edges required to register WHY targets. |
| **Truthful claims that depend on graph topology** (e.g. “this signal sits in pathway X as validated by `interaction_map_v1`”) | **Mandatory** — add **nodes** and **minimum necessary edges**, and align **`phenotype_map_v1.yaml` `required_edges`** where validators tie edges to phenotype governance (see KB-S52 preflight §5–6). |
| **Composite hepatic or thyroid–hormone / autoimmune “systems” framing** implied as **cross-signal chains** in the product sense | **Mandatory** for graph-backed truth; otherwise hypotheses must **avoid** implying map-validated pathways and stay **marker- and signal-local** (or explicitly reference only signals already on the map). |

**Optional additions (illustrative, not prescriptive):** edges from existing metabolic nodes to **`signal_hepatic_metabolic_stress`** if that ID is promoted to a node; ALP/bilirubin links to hepatic or inflammatory nodes; FT3/FT4/antibody links into the existing thyroid–lipid subgraph — **each** requires governance (phenotype `required_edges` / validation rules), not free-form YAML.

---

## 5. Phenotype alignment

### 5.1 `phenotype_map_v1.yaml`

- **No** phenotype **`required_signals`** or **`optional_signals`** list includes any of the eleven remainder IDs.  
- Hepatic phenotype rows centre **`signal_hepatic_alt_context`** (`ph_hepatic_alt_inflammatory_v1`) or use **`signal_alt_high`** / **`signal_ggt_high`** only inside **`required_edges`** / optional signals on **other** phenotypes (e.g. `ph_hba1c_metabolic_stress_v1` optional `signal_hepatic_alt_context`).  
- Thyroid rows centre **`signal_thyroid_tsh_context`**; **`signal_tsh_high`** appears as optional signal and in **`required_edges`** (`ph_tsh_axis_metabolic_v1`, `ph_thyroid_lipid_disturbance_v1`).  
- **No** autoimmune or free-T3/T4-led phenotype entries.

### 5.2 `phenotype_expectations_v1.yaml`

- Expectations enforce **root_cause** for **`signal_hepatic_alt_context`**, **`signal_thyroid_tsh_context`**, **`signal_hba1c_high`**, and the homocysteine phenotype — **not** for the eleven remainder signals.  
- Tier 1 targets **`signal_ggt_high`**, **`signal_tsh_high`**, **`signal_tsh_low`** are **not** given dedicated `expected_root_cause.applies_to_signal_id` rows in this file (same pattern as KB-S52 preflight: optional stub would be a **separate** charter item).

### 5.3 Can this follow-on avoid phenotype changes?

**Yes**, for a **bounded WHY-only** sprint: new hypothesis assets + loaders + `_ROOT_CAUSE_TARGETS` only, **without** claiming new phenotype recognition or chain enforcement.

**Phenotype / fixture additions become required** if the charter promises **harness enforcement**, **phenotype-level** recognition of ALP/bilirubin/FT3/FT4/antibody-led patterns, or **chain_expectations** tied to new edges.

---

## 6. Confirmatory-test constraint

**Registry:** `knowledge_bus/registries/confirmatory_tests_v1.yaml` (updated_at 2026-03-26) defines a **fixed** `tests:` list. Compiler behaviour: any `confirmatory_tests` entry in a hypothesis **must** resolve to a known `test_id` (`root_cause_compiler_v1.py`).

**Assessment:** **Insufficient** for rich, signal-specific confirmatory panels (ALP isoforms, fractionated bilirubin, repeat thyroid antibodies, etc.) — those **`test_id`s do not exist** today.

**Partial / workable:** Tier 1 already reused **`test_liver_ggt_alt_ast_v1`** and **`test_thyroid_tsh_ft4_v1`** plus generic monitoring tests (`test_crp_repeat_v1`, etc.). The same **reuse + suppression semantics** (markers already on panel) can support a **minimal** KB-S52B hypothesis set **without** registry edits.

**Blocked:** Any hypothesis line that **requires** new `test_id` strings **blocks** compilation until a **separate registry sprint** adds them (governed CONTENT/MIXED work, not silent edits).

---

## 7. Structural integrity (SSOT / schemas / scoring / pipeline)

| Layer | Required for hypothesis-only KB-S52B? |
|-------|--------------------------------------|
| **New hypothesis YAML + `load_root_cause_hypotheses` loaders + `_ROOT_CAUSE_TARGETS`** | **Yes** (this is the core deliverable). |
| **SSOT biomarker / signal definitions** | **No** — signals already exist in package libraries. |
| **Core pipeline / evaluator** | **No** — only if evaluation bugs are discovered (out of preflight scope). |
| **Scoring / arbitration** | **No** for WHY registration alone. |
| **`interaction_map_v1.yaml` + phenotype `required_edges`** | **Only if** the charter includes graph-backed claims or phenotype chain enforcement (**bounded prerequisite**). |
| **`confirmatory_tests_v1.yaml`** | **Only if** hypotheses need **new** `test_id`s (**bounded prerequisite**). |

**Sprint shape label:**

- **`PURE_EXTENSION`** — Add governed hypothesis assets + compiler registration for an agreed subset of the eleven signals, **reusing only existing** `test_id`s, **without** interaction-map or phenotype fixture changes and **without** implying map-validated multi-hop chains.  
- **`EXTENSION_PLUS_BOUNDED_PREREQUISITE`** — Same as above **plus** one or more of: (1) new interaction-map nodes/edges + phenotype governance alignment, (2) phenotype map/fixture/expectations for new patterns, (3) confirmatory registry expansion.

---

## 8. AB / VR and commercial relevance

**Biomarkers present** in `ab_full_panel_with_ranges.json` and `vr_full_panel_with_ranges.json` include **`alp`**, **`bilirubin`**, **`ggt`**, **`free_t3`**, **`free_t4`**, **`tsh`**, **`tgab`**, **`tpo_ab`** (path-level grep). Those panels are therefore **commercially representative** for thyroid and hepatic marker visibility.

**Signal-level / WHY visibility:** When primary user concern maps to a **remainder** signal (e.g. ALP-high primary without ALT context), **`root_cause_v1.findings`** may still be populated from **other** targets, but **not** with a **dedicated** finding for that primary — same class of gap KB-S52 preflight described for GGT/TSH before Tier 1.

**Fixture expansion:** Not **required** for a WHY-only follow-on; **strategically useful** later if AB/VR are formalised to assert specific firing combinations for ALP/bilirubin/hormone/antibody scenarios (aligns with Wave 3 KB-S53 direction in v1.5).

---

## 9. Recommendation

### 9.1 Sprint shape

**Default:** **`PURE_EXTENSION`** — mirror KB-S52 Tier 1 mechanics for the **eleven** excluded signals: one or more `*_hypotheses_v1.yaml` files, loaders, `_ROOT_CAUSE_TARGETS` rows, strict reuse of existing **`test_id`** values, and **no** implied map-topology claims.

**Use `EXTENSION_PLUS_BOUNDED_PREREQUISITE`** only if the authored charter explicitly includes map nodes/edges, phenotype scaffolding, and/or confirmatory registry rows.

### 9.2 Recommended signals in scope (for charter freeze)

**Minimum closed list (matches exclusion set):**

- Hepatic: `signal_hepatic_metabolic_stress`, `signal_alp_high`, `signal_alp_low`, `signal_bilirubin_high`, `signal_hyperbilirubinemia` — charter should **pick bilirubin framing** (`signal_bilirubin_high` vs `signal_hyperbilirubinemia` vs both with non-overlapping hypotheses) to avoid duplicate user-facing narratives.  
- Thyroid: `signal_free_t3_high`, `signal_free_t3_low`, `signal_free_t4_high`, `signal_free_t4_low`, `signal_tgab_high`, `signal_tpo_ab_high`.

**Out of scope for this preflight:** changing Tier 1 registrations (`signal_ggt_high`, `signal_tsh_high`, `signal_tsh_low`) unless a defect review says otherwise.

### 9.3 Combined vs split

**`COMBINED`** — One follow-on workpackage is **governable** if both domains stay **hypothesis-only** with the same mechanical pattern and shared confirmatory constraints.

**`SPLIT_HEPATIC_THYROID`** — Prefer if **prerequisites diverge** (e.g. hepatic charter adds map/cholestasis edges while thyroid stays WHY-only, or bilirubin work requires registry expansion but hormone work does not).

**Suggested default:** **`COMBINED`** for **`PURE_EXTENSION`**; reassess **`SPLIT_HEPATIC_THYROID`** if the charter picks **`EXTENSION_PLUS_BOUNDED_PREREQUISITE`** on one side only.

---

## 10. Source pointers (verification)

| Artifact | Role |
|----------|------|
| `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md` | Wave 2 KB-S52 purpose — hepatic + thyroid depth |
| `docs/investigations/KB-S52_PREFLIGHT.md` | Prior domain inventory; note Tier 1 superseded WHY rows for GGT/TSH |
| `backend/core/analytics/root_cause_compiler_v1.py` | `_ROOT_CAUSE_TARGETS` — authoritative compiler registration |
| `knowledge_bus/root_cause/hypotheses/` | Dedicated YAML assets (none for KB-S52B list) |
| `knowledge_bus/interaction_maps/interaction_map_v1.yaml` | Nodes/edges — revision 1.1.3 |
| `knowledge_bus/phenotypes/phenotype_map_v1.yaml` | Phenotype signals and `required_edges` |
| `backend/tests/fixtures/panels/phenotypes/phenotype_expectations_v1.yaml` | Harness root-cause expectations |
| `knowledge_bus/registries/confirmatory_tests_v1.yaml` | Allowed `test_id` universe for hypotheses |
| `backend/core/analytics/signal_evaluator.py` | SignalRegistry package discovery |
| `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`, `vr_full_panel_with_ranges.json` | AB/VR biomarker coverage |

---

**Artifact path:** `docs/investigations/KB-S52B_HEPATIC_THYROID_COMPLETION_PREFLIGHT.md`
