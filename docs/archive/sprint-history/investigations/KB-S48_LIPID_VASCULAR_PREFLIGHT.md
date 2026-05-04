# KB-S48 — Lipid / Vascular WHY Expansion (Preflight)

**Mode:** Read-only preflight only (no code changes, no prompts, no sprint start).  
**Date:** 2026-04-01  
**Basis:** Live repository state — `interaction_map_v1.yaml` (revision 1.1.1), `root_cause_compiler_v1.py`, `phenotype_map_v1.yaml`, `phenotype_expectations_v1.yaml`, `knowledge_bus/root_cause/hypotheses/`, adopted strategy v1.5, AB/VR full-panel fixtures, `SignalRegistry` enumeration (backend), `docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md`.

---

## What KB-S48 is trying to add to the application

Per **`docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md`** (Wave 1 — KB-S48):

- **Purpose:** Clinically important explanation in a commercially central **lipid / cardiovascular interpretation** domain.
- **Structural constraint (v1.5):** This must **not** be treated as a **pure hypothesis-only** task. The **interaction-map structure beneath `signal_lipid_transport_dysfunction`** must be **explicitly verified** and, if incomplete, **unblocked on a governed prerequisite path** before “convincing WHY” is claimed for lipids.

Operationally, closure of KB-S48 therefore implies:

1. **Deterministic WHY (`root_cause_v1`)** for governed lipid-related signal targets (at minimum the four named lipid transport / dyslipidaemia signals below), via hypothesis assets **and** compiler registration analogous to KB-S46.
2. **Coherent pathway structure** so that narrative / chain tooling that consumes `interaction_map_v1.yaml` can anchor a **lipid transport hub** (`signal_lipid_transport_dysfunction`) where the product and phenotype layer already expect it — **or** a deliberate, documented narrowing of scope if that hub is intentionally deferred.

---

## 1. Current runtime signal set (lipid / vascular pathway)

### 1.1 Minimum set requested (all **present** in `SignalRegistry`)

Verified via backend enumeration (`SignalRegistry.get_all_signals()`):

| `signal_id` | In registry |
|-------------|-------------|
| `signal_lipid_transport_dysfunction` | Yes |
| `signal_ldl_cholesterol_high` | Yes |
| `signal_hdl_cholesterol_low` | Yes |
| `signal_triglycerides_high` | Yes |

### 1.2 Related lipid panel signals (same registry pass)

**Additional IDs** whose names match lipid / cholesterol / lipoprotein patterns (21 total in that filter), including but not limited to:

`signal_total_cholesterol_high`, `signal_total_cholesterol_low`, `signal_non_hdl_high`, `signal_non_hdl_low`, `signal_tc_hdl_ratio_high`, `signal_tc_hdl_ratio_low`, `signal_lipoprotein_a_high`, `signal_apob_*`, `signal_apoa1_*`, `signal_lipid_imbalance`, **`signal_ldl_high`** (parallel naming to `signal_ldl_cholesterol_high`), **`signal_hdl_low`** (parallel to `signal_hdl_cholesterol_low`), `signal_hdl_cholesterol_high`.

**Sprint authoring implication:** packages and KPI wiring may use **`signal_ldl_high` / `signal_hdl_low`** vs canonical **`signal_ldl_cholesterol_high` / `signal_hdl_cholesterol_low`**. KB-S48 authoring must state which IDs are **in scope** for hypothesis registration and avoid silent drift between aliases.

### 1.3 “Vascular” beyond lipids

- **`interaction_map_v1.yaml`** includes **homocysteine** nodes (`signal_homocysteine_high`, `signal_homocysteine_elevation_context`) with **existing** hypothesis support (`hcy_hypotheses_v1.yaml` + `signal_homocysteine_elevation_context` in `_ROOT_CAUSE_TARGETS`).
- Registry also includes **`signal_vascular_inflammatory_stress`** (name-only relation to “vascular”; not expanded here).

KB-S48 as **lipid / vascular** in strategy language is **primarily lipid + cardiometabolic context**; **homocysteine WHY is already on a different, covered target.**

---

## 2. Hypothesis coverage and `compile_root_cause_v1`

### 2.1 Hypothesis assets on disk

Under **`knowledge_bus/root_cause/hypotheses/`** there are **six** files:

- `hcy_hypotheses_v1.yaml`
- `hba1c_hypotheses_v1.yaml`
- `alt_hypotheses_v1.yaml`
- `tsh_hypotheses_v1.yaml`
- `insulin_resistance_hypotheses_v1.yaml`
- `systemic_inflammation_hypotheses_v1.yaml`

**None** of these filenames correspond to lipid / dyslipidaemia targets (`lipid`, `ldl`, `hdl`, `triglyceride`, etc.).

### 2.2 Compiler targets (`_ROOT_CAUSE_TARGETS`)

In **`backend/core/analytics/root_cause_compiler_v1.py`**, registered targets are **only**:

1. `signal_homocysteine_elevation_context`
2. `signal_hba1c_high`
3. `signal_hepatic_alt_context`
4. `signal_thyroid_tsh_context`
5. `signal_insulin_resistance`
6. `signal_systemic_inflammation`

**Not registered:** `signal_lipid_transport_dysfunction`, `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low`, `signal_triglycerides_high` (nor the `signal_ldl_high` / `signal_hdl_low` aliases).

### 2.3 Where `compile_root_cause_v1` returns `None`

Implementation summary:

- The function builds `findings` by iterating **`_ROOT_CAUSE_TARGETS`** only.
- It **returns `None` if and only if `findings` is empty** (i.e. **no** registered target appears in `signal_results` with `signal_state` in `{"suboptimal", "at_risk"}`).

**Consequences for lipid pathways:**

- **Lipid signals firing alone** (no other registered WHY targets firing) → **`RootCauseV1` is `None`** — not because lipid rows are “skipped with content,” but because **lipids are not targets at all**.
- **Lipid signals + e.g. `signal_thyroid_tsh_context` firing** → output may be **non-`None`** due to **thyroid** (or other registered targets), while **lipid rows still have no lipid-specific findings**.

Signals **without** a registered loader are **not iterated**; there is **no partial finding** for them today.

| Signal | Registered hypothesis / loader | `compile_root_cause_v1` can emit a finding for it? |
|--------|--------------------------------|-----------------------------------------------------|
| `signal_lipid_transport_dysfunction` | No | No |
| `signal_ldl_cholesterol_high` | No | No |
| `signal_hdl_cholesterol_low` | No | No |
| `signal_triglycerides_high` | No | No |

---

## 3. Interaction-map maturity under `signal_lipid_transport_dysfunction`

### 3.1 `interaction_map_v1.yaml` (v1.1.1) — repo reality

**Nodes** include:

- `signal_triglycerides_high` (system: **metabolic**)
- `signal_ldl_cholesterol_high`, `signal_hdl_cholesterol_low` (system: **lipid_transport**)

**`signal_lipid_transport_dysfunction` does not appear as a node** and **does not appear in any `edges.from_signal` / `edges.to_signal`**.

**Edges involving lipid-named signals today:**

- `signal_triglycerides_high` → `signal_ggt_high` (metabolic → hepatic)
- Thyroid / TSH → `signal_ldl_cholesterol_high`, TSH → `signal_hdl_cholesterol_low`
- `signal_hdl_cholesterol_low` / `signal_ldl_cholesterol_high` → `signal_hba1c_high`

So the map has a **partial thyroid–lipid–glycaemia bridge** and **TG → GGT**, but **no hub** that ties the composite **`signal_lipid_transport_dysfunction`** into the same structure.

### 3.2 Preflight verdict (sprint readiness)

**Not materially complete** for a v1.5-compliant “structure beneath `signal_lipid_transport_dysfunction`” claim: the **named hub signal is absent** from the interaction map. A **bounded interaction-map (and/or governance) task** is a **prerequisite** unless the sprint **narrows KB-S48** to hypothesis-only for LDL/HDL/TG **and** formally **defers** the lipid-transport hub to another workpackage (explicit product decision — contradicts default v1.5 framing).

`docs/METABOLIC_PATHWAY_COVERAGE_AUDIT_2026-03-20.md` states “7 edges” for the lipid row; **preflight correction:** those counts align better with **phenotype-map edge documentation** than with **`signal_lipid_transport_dysfunction`** connectivity in **`interaction_map_v1.yaml`**.

---

## 4. Phenotype dependency

### 4.1 `phenotype_map_v1.yaml`

| Phenotype | Depends on lipid transport / lipids |
|-----------|--------------------------------------|
| **`ph_metabolic_early_ir_v1`** | **Required:** `signal_lipid_transport_dysfunction`, `signal_triglycerides_high`, `signal_hdl_cholesterol_low`. **Required edge (phenotype layer):** `signal_triglycerides_high` → `signal_lipid_transport_dysfunction` (**driver**, exploratory, **`requires_research_promotion: true`**), rationale ref: `knowledge_bus/phenotypes/rationales/ph_metabolic_early_ir_edge_tg_to_lipid_transport.md` (placeholder: pending research promotion). |
| **`ph_thyroid_lipid_disturbance_v1`** | **Required:** `signal_thyroid_tsh_context`, `signal_ldl_cholesterol_high`; edges to LDL/HDL from thyroid signals. |
| **`ph_hba1c_metabolic_stress_v1`** | **Optional:** `signal_lipid_transport_dysfunction`. |
| **`ph_tsh_axis_metabolic_v1`** | **Optional:** `signal_ldl_cholesterol_high`. |

**`chain_expectations.status`** for the lipid-heavy phenotypes above is **`pending`** where recorded in the excerpted sections.

### 4.2 `phenotype_expectations_v1.yaml` (harness)

- **`ph_metabolic_early_ir_v1`:** `must_fire` includes **`signal_lipid_transport_dysfunction`**; **`expected_root_cause.must_exist: false`**, `min_hypothesis_count: 0`. **Chain enforcement:** `must_exist: false`.
- **`ph_thyroid_lipid_disturbance_v1`:** `must_fire` **`signal_thyroid_tsh_context`** only; same **root cause / chain** looseness.

**Fixture example:** `backend/tests/fixtures/panels/phenotypes/ph_metabolic_early_ir_v1.json` drives TG high, HDL low, non-HDL abnormal — aligned with **signal firing**, not with **WHY or interaction-map completeness**.

### 4.3 Is phenotype “truth” ready for a pure WHY expansion?

**Partial.** Phenotypes **encode intent** and **synthetic firing**, but **explicitly defer** chain truth and **do not require root-cause artifacts** for lipid-led patterns. **WHY expansion** should plan **tightened expectations** only **after** governed map + hypothesis alignment; otherwise regressions will not distinguish “copy added” from “pathway correct.”

---

## 5. AB / VR relevance and live-output centrality

### 5.1 `ab_full_panel_with_ranges.json`

Lipid-related markers are **present** (e.g. `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`, `total_cholesterol`, `non_hdl_cholesterol`, `tc_hdl_ratio`, `lipoprotein_a`). Representative values in the checked excerpt:

- **LDL** above lab **max** (mild elevation) → likely **lipid abnormality surfacing** on real AB-style outputs.
- **Total cholesterol** slightly above **max**.
- **HDL** within range (not exercising **`signal_hdl_cholesterol_low`** on this fixture).
- **Triglycerides** low/normal (not exercising **`signal_triglycerides_high`**).

So AB **does** touch **LDL / total-chol-type** interpretation; it does **not** fully stress the **TG / low-HDL** limb of the early-IR phenotype on the same file.

### 5.2 `vr_full_panel_with_ranges.json`

Same marker keys exist; sample **LDL** checked was **within** the stated **max** on that excerpt — **weaker lipid “fire”** than AB for LDL on the inspected values. VR still carries **homocysteine** elevation (vascular context) which **does** exercise **existing** Hcy WHY, not lipid WHY.

### 5.3 Commercial / product readout

Lipid markers appear on **primary full-panel fixtures**, so **lipid signals are commercially visible** when labs are out of range. **Lipid-specific WHY** is **not** visible today because **compiler targets exclude lipids**.

---

## Recommended final sprint shape

| Option | When to use |
|--------|-------------|
| **`PURE_WHY`** | **Not recommended** as the default KB-S48 shape under **v1.5**: the strategy **requires** validating **`signal_lipid_transport_dysfunction`** structure first; that signal is **missing from `interaction_map_v1.yaml`**. |
| **`WHY_PLUS_BOUNDED_PREREQUISITE`** (**recommended**) | Add a **small, governed** package of work: (1) **interaction map**: add `signal_lipid_transport_dysfunction` as a **node** and **minimum necessary edges** (e.g. from TG and/or dyslipidaemia children, consistent with phenotype intent) **or** an explicit architecture note if the hub is intentionally non-graph; (2) **hypothesis asset(s)** + **`load_*`** + **`_ROOT_CAUSE_TARGETS`** entries for the **agreed signal IDs**; (3) optional follow-on: tighten **`phenotype_expectations_v1`** once map + WHY are stable. |

**Narrow alternative (only if explicitly scoped):** **WHY-only** for **`signal_ldl_cholesterol_high` / `signal_hdl_cholesterol_low` / `signal_triglycerides_high`** with **no** lipid-transport hub — must be **named as out-of-scope for v1.5 KB-S48** and tracked as a separate decision.

---

## Summary table

| Topic | Repo reality |
|-------|----------------|
| **Signals in scope (minimum)** | All four named signals exist at runtime; many related lipid IDs also exist — watch **alias pairs** (`ldl` vs `ldl_cholesterol`, etc.). |
| **Hypothesis / compiler** | **No** lipid hypothesis files; **no** lipid entries in `_ROOT_CAUSE_TARGETS`; **`compile_root_cause_v1` → `None`** whenever **no** registered target fires. |
| **Interaction map** | **No** `signal_lipid_transport_dysfunction`; partial **LDL/HDL/TG** connectivity only; **TG → lipid hub** exists in **phenotype map** as **pending promotion**, not in **interaction map**. |
| **Phenotypes** | **Strong dependency** on **`signal_lipid_transport_dysfunction`** for `ph_metabolic_early_ir_v1`; harness **does not yet require WHY** or chains. |
| **AB / VR** | **Partial** exercise: AB better for **elevated LDL/TC** on inspected values; **TG/HDL low** need **targeted fixtures** or asserts for full pathway stress. |

---

**Artifact path:** `docs/investigations/KB-S48_LIPID_VASCULAR_PREFLIGHT.md`
