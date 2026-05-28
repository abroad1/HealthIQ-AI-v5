# Wave 1 Subsystem Marker Equivalence Investigation

## 1. Executive verdict

**Verdict:** **Isolated bilirubin / `total_bilirubin` defect**, not a wider Wave 1 equivalence defect.

- **Type:** subsystem mapping + canonical identity mismatch (not stale data, not frontend label-only issue).
- **Observed behavior:** `total_bilirubin` is expected by `wave1_liv_processing_context`, while the parsed/scored canonical marker is `bilirubin`.
- **Impact:** `total_bilirubin` is rendered as missing even when `Bilirubin Total (Venous)` is present and scored as `bilirubin`.
- **Scope:** In this analysis (`bb695d3c`), all other Wave 1 expected markers behave correctly (true missings: glucose, insulin, AST).
- **Architecture note:** There is **no generic subsystem-level satisfies/equivalence layer**; only a liver-specific equivalence helper exists in domain assembly (not subsystem partitioning).

---

## 2. Trigger example: Bilirubin Total

### Evidence chain

| Step | Observed value |
|---|---|
| Source/upload row | `Bilirubin Total (venous)` value `17` unit `µmol/L` range `5–21` |
| Parsed/canonical upload key | `bilirubin` |
| Scored biomarker payload marker | `biomarker_name: "bilirubin"` (score `1.0`, status `optimal`) |
| Subsystem expected marker | `total_bilirubin` also expected in `wave1_liv_processing_context` (`alp`, `albumin`, `bilirubin`, `total_bilirubin`) |
| Subsystem included output | `albumin`, `alp`, `bilirubin` |
| Subsystem missing output | `total_bilirubin` |

### Is this a real defect?

**Yes (real false-positive missing marker).**

- From user/product perspective, uploaded **Bilirubin Total** should satisfy the subsystem requirement.
- Current subsystem partition logic performs exact ID matching only; it does not treat `bilirubin` as satisfying `total_bilirubin`.

---

## 3. Full Wave 1 subsystem mapping audit

| Domain | Subsystem | Expected marker ID | Present in scored payload? | Equivalent marker present? | Rendered as missing? | Concern? |
|---|---|---|---|---|---|---|
| Cardiovascular | Lipid transport | `total_cholesterol` | Yes | No | No | No |
| Cardiovascular | Lipid transport | `ldl_cholesterol` | Yes | No | No | No |
| Cardiovascular | Lipid transport | `hdl_cholesterol` | Yes | No | No | No |
| Cardiovascular | Lipid transport | `triglycerides` | Yes | No | No | No |
| Cardiovascular | Lipid transport | `tc_hdl_ratio` | Yes | No | No | No |
| Cardiovascular | Homocysteine pathway | `homocysteine` | Yes | No | No | No |
| Cardiovascular | Vascular strain context | `crp` | Yes | No | No | No |
| Blood sugar | Glycaemic control | `glucose` | No | No | Yes | No (true missing) |
| Blood sugar | Glycaemic control | `hba1c` | Yes | No | No | No |
| Blood sugar | Insulin and metabolic context | `insulin` | No | No | Yes | No (true missing) |
| Blood sugar | Insulin and metabolic context | `triglycerides` | Yes | No | No | No |
| Liver | Liver enzyme pattern | `alt` | Yes | No | No | No |
| Liver | Liver enzyme pattern | `ast` | No | No | Yes | No (true missing) |
| Liver | Liver enzyme pattern | `ggt` | Yes | No | No | No |
| Liver | Liver processing context | `alp` | Yes | No | No | No |
| Liver | Liver processing context | `albumin` | Yes | No | No | No |
| Liver | Liver processing context | `bilirubin` | Yes | No | No | No |
| Liver | Liver processing context | `total_bilirubin` | No | **Yes (`bilirubin`)** | **Yes** | **Yes (false-positive missing)** |

---

## 4. Rail-only / display-only marker audit

`backend/ssot/biomarkers.yaml` currently has **one** entry with `display_label_rail_only: true`:

| Marker ID | Why it exists | Can appear in subsystem expected markers? | Canonical equivalent | Can subsystem layer recognise equivalent today? |
|---|---|---|---|---|
| `total_bilirubin` | DOMAIN-LABEL1 label authority patch to emit governed display label “Total Bilirubin” without changing canonical alias behavior | **Yes** (currently in Wave 1 liver subsystem expected set) | `bilirubin` (canonical parser/scoring identity) | **No** (subsystem partition is exact-ID only) |

**Conclusion:** `display_label_rail_only` itself is not inherently broken, but using such keys in expected-marker logic creates equivalence risk unless subsystem matching supports it.

---

## 5. Missing-marker false-positive audit

Health Systems Card missing markers on `bb695d3c`:

| Missing marker shown | Truly absent? | Equivalent uploaded/scored marker exists? | Result |
|---|---|---|---|
| `glucose` | Yes | No | Correct missing |
| `insulin` | Yes | No | Correct missing |
| `ast` | Yes | No | Correct missing |
| `total_bilirubin` | **No** | **Yes (`bilirubin`)** | **False-positive missing** |

---

## 6. Code-path analysis

### Parser/canonical output

- Alias registry maps `Bilirubin Total`, `Bilirubin Total (Venous)`, `Total Bilirubin` to canonical `bilirubin` in `backend/ssot/biomarker_alias_registry.yaml`.
- `AliasRegistryService.resolve()` returns canonical IDs; `display_label_rail_only` rows are explicitly skipped from alias registration.

### Scoring payload marker IDs

- Analysis payload emits `biomarkers[].biomarker_name = "bilirubin"` with display label `Bilirubin Total (venous)` and optimal score.

### Subsystem included/missing partition

- `backend/core/analytics/wave1_subsystem_evidence.py` defines liver processing expected IDs as:
  - `("alp", "albumin", "bilirubin", "total_bilirubin")`
- `_partition_subsystem_markers()` logic:
  - `included = (panel_biomarker_ids ∪ scored_on_rail) ∩ expected`
  - `missing = expected − included`
- This is exact set intersection; no equivalence/satisfies mapping.

### Label emission

- `_marker_display_label_map()` uses `CanonicalResolver.load_biomarkers()` and can emit “Total Bilirubin” label for `total_bilirubin` because of SSOT row.
- This affects label rendering, not marker matching.

### Frontend render

- `Wave1SubsystemEvidenceSection` renders backend-provided `included_marker_ids` and `missing_marker_ids` as-is.
- No frontend equivalence reconciliation exists (correctly, by architecture).

### Important contrast

- `domain_score_assembler.py` includes a **liver-specific** helper `_liver_panel_has_bilirubin_coverage()` that treats either ID as satisfying coverage for domain-level logic.
- That helper is **not used** in `wave1_subsystem_evidence.py`.

---

## 7. Root cause

Primary root cause is a **canonical identity vs subsystem expected-ID mismatch**:

- Canonical parser/scoring identity: `bilirubin`
- Subsystem expected-ID list includes both `bilirubin` and rail-only `total_bilirubin`
- Matching logic is exact-ID only (no satisfies/equivalence)
- Result: `total_bilirubin` remains missing even when `bilirubin` is present

Not root cause:

- Not label-authority failure (labels are governed and correct)
- Not stale data (payload consistently shows `bilirubin` present)
- Not frontend display bug (frontend faithfully renders DTO)

---

## 8. Fix options

| Option | Description | Pros | Cons | Risk | Recommendation |
|---|---|---|---|---|---|
| A | Change Wave 1 subsystem expected marker from `total_bilirubin` to canonical `bilirubin` (or remove duplicate expectation) | Simple, low blast radius, aligns subsystem with parser/scoring canonical IDs | Point fix only; does not solve future equivalence classes | Low | **Strongly recommended for immediate correction** |
| B | Add governed subsystem satisfies/equivalence mapping (`total_bilirubin` satisfied by `bilirubin`) | Scalable for future equivalent IDs; explicit governance | More design and contract surface; needs tests/contracts and ownership rules | Medium | **Recommended as strategic follow-up** if more equivalence cases appear |
| C | Register `total_bilirubin` as canonical alias equivalent in alias/canonical layer | Might reduce mismatch in some paths | Conflicts with DOMAIN-LABEL1 rationale; risks alias collisions and canonical ambiguity | Medium/High | **Not recommended** |
| D | Keep current behavior | No engineering work | Continues false-positive missing marker and trust damage | High product risk | **Not recommended** |
| E | Keep expected IDs but normalize subsystem matching through canonical resolver before partition | Reduces hard-coded exceptions; uses existing canonical layer | Still needs policy for one-to-many equivalence; canonical resolver alone may not capture “satisfies” semantics | Medium | Viable alternative to B if designed carefully |

---

## 9. Recommended next work package

If fix approved:

- **work_id:** `WAVE1-EQUIV1_subsystem_marker_equivalence_guard`
- **risk level:** Low-to-Medium
- **files likely touched:**
  - `backend/core/analytics/wave1_subsystem_evidence.py`
  - `backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py`
  - (optionally) a new governed equivalence config file if Option B chosen
- **exact fix principle:**
  - Preserve canonical parser identity.
  - Ensure subsystem expected-marker matching does not report false missing when governed equivalent canonical marker exists.
  - Keep label authority path unchanged.
- **what must not change:**
  - No scoring threshold changes.
  - No alias collision-prone canonical remapping.
  - No frontend-side marker inference.
  - No IDL/root-cause behavior changes.

---

## 10. STOP conditions

Do **not** do any of the following in this investigation or follow-up implementation without explicit approval:

- Do not change scoring policy, rail scoring, or confidence formulas.
- Do not alter alias behavior globally to force canonical identity changes.
- Do not patch frontend to “hide” backend missing markers.
- Do not add ad-hoc hardcoded equivalence exceptions outside governed mapping.
- Do not modify Knowledge Bus or narrative content as a workaround.
- Do not merge or start implementation from this report.

---

### Investigation summary

This is **not** a stale-data or display-only problem. It is a **real subsystem marker-equivalence defect**, currently **isolated to `total_bilirubin` vs `bilirubin`** in Wave 1 liver subsystem evidence for this panel.
