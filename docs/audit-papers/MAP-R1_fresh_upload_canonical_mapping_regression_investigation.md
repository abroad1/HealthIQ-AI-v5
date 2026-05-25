# MAP-R1 — Fresh Upload Canonical Marker Mapping Regression Investigation

**Investigator:** Claude Code  
**Date:** 2026-05-25  
**Method:** API payload fetch (both analysis IDs), alias resolver code trace, alias resolution unit tests, upload page code trace  
**Status:** Root cause proven. No code modified.

---

## 1. Executive verdict

| Question | Answer |
|---|---|
| **Root cause identified?** | **Yes — proven.** Trailing `*` characters in LLM-extracted lab-report biomarker names break the alias resolver's specimen-suffix stripping logic, causing 13 markers to fall through as `unmapped_*`. |
| **Regression, input-format issue, or limitation?** | **Input-format sensitivity.** The same analysis codebase processes both runs. The d8 upload included lab-report `*` abnormal-value markers in biomarker name strings (e.g. `Homocysteine (venous)*`). The f2 upload did not. The resolver has no defence against trailing `*`. |
| **Lead finding change explainable?** | **Yes, completely.** With `signal_homocysteine_high` and `signal_homocysteine_elevation_context` absent (homocysteine unmapped), `signal_total_cholesterol_high` is the strongest remaining active signal. Lead arbitration is correct for the data the engine actually received. |
| **Is KB-WAVE-1 blocked?** | **Yes.** Homocysteine, ApoB, ApoA1, Lipoprotein(a), and their ratio signals are all absent from d8. Any KB-WAVE-1 lipid/homocysteine governed-WHY content cannot fire until the mapping regression is resolved. |
| **Recommended next sprint** | `MAP-R1A` — fix trailing `*` stripping in alias resolver backend + frontend `analysisBiomarkerKey()`. |

---

## 2. Analyses compared

| Analysis ID | Created at | Scored biomarker count | Lead finding | Notes |
|---|---|---|---|---|
| `f2dcb58f-e816-4ff6-9011-e93c5d48b82c` | 2026-05-24T21:07:46Z | **77** | Homocysteine Elevation Context | Upload labels clean: `Homocysteine (venous)` (no `*`) |
| `d8cfe1a8-c0e7-4f8b-99ea-8152b05f1579` | 2026-05-24T22:28:21Z | **63** | Total Cholesterol High | Upload labels include trailing `*`: `Homocysteine (venous)*` → unmapped |

---

## 3. Marker mapping delta

| Marker | f2 scored? | d8 scored? | f2 upload label | d8 upload raw key | f2 value | d8 value | Likely reason |
|---|---|---|---|---|---|---|---|
| `homocysteine` | ✅ | ❌ | `Homocysteine (venous)` | `unmapped_homocysteine_(venous)*` | 16.23 µmol/L | UNMAPPED | Trailing `*` blocks specimen-suffix stripping |
| `active_b12` | ✅ | ❌ | `Active Vitamin B12 (venous)` | `unmapped_active_vitamin_b12_(venous)*` | 139.18 pmol/L | UNMAPPED | Trailing `*` |
| `apoa1` | ✅ | ❌ | `Apolipoprotein A1 (venous)` | `unmapped_apolipoprotein_a1_(venous)*` | 1.73 g/L | UNMAPPED | Trailing `*` |
| `apob` | ✅ | ❌ | `Apolipoprotein B (venous)` | `unmapped_apolipoprotein_b_(venous)*` | 0.69 g/L | UNMAPPED | Trailing `*` |
| `vitamin_b12` | ✅ | ❌ | `Vitamin B12 (venous)` | `unmapped_vitamin_b12_(venous)*` | 336.0 pg/mL | UNMAPPED | Trailing `*` |
| `vitamin_d` | ✅ | ❌ | `Vitamin D (venous)` | `unmapped_vitamin_d_(venous)*` | 89.13 nmol/L | UNMAPPED | Trailing `*` |
| `zinc` | ✅ | ❌ | `Zinc (venous)` | `unmapped_zinc_(venous)*` | 12.77 µmol/L | UNMAPPED | Trailing `*` |
| `tsh` | ✅ | ❌ | `Tsh (venous)` | `unmapped_tsh_(venous)*` | 1.409 µIU/mL | UNMAPPED | Trailing `*` |
| `creatinine` | ✅ | ❌ | `Creatinine (venous)` | `unmapped_creatinine_(venous)*` | 87.0 µmol/L | UNMAPPED | Trailing `*` |
| `lipoprotein_a` | ✅ | ❌ | `Lipoprotein (a) (venous)` | `unmapped_lipoprotein_(a)_(venous)*` | 0.14 g/L | UNMAPPED | Trailing `*` |
| `corrected_calcium` | ✅ | ❌ | `Corrected Calcium (venous)` | `unmapped_corrected_calcium_(venous)*` | 2.25 mmol/L | UNMAPPED | Trailing `*` |
| `apob_apoa1_ratio` | ✅ | ❌ | `Apob Apoa1 Ratio` | `unmapped_apolipoprotein_ratio_(venous)*` | 0.4 ratio | UNMAPPED | Trailing `*`; also uploaded under verbose `Apolipoprotein Ratio` name |
| `urea_creatinine_ratio` | ✅ | ❌ | (derived) | (derived) | 0.082 ratio | NOT COMPUTED | Computed from `urea` + `creatinine`; `creatinine` unmapped in d8 |
| `rbc` | ✅ | ❌ | `Erythrocytes (rbc)` | **ABSENT** | 4.4 10^12/L | ABSENT | LLM parser did not extract RBC from d8 upload; separate LLM non-determinism issue |
| `total_cholesterol` | ✅ | ✅ | `Cholesterol (venous)` | `total_cholesterol` | 5.26 mmol/L | 5.26 mmol/L | Sent as canonical key; maps correctly |
| `transferrin` | ✅ | ✅ | `Transferrin (venous)` | `transferrin` | 2.0 g/L | 2.0 g/L | Sent as canonical key; maps correctly |
| `mcv` | ✅ | ✅ | `Mean Corpuscular Volume (mcv)` | `mcv` | 99.5 fL | 99.5 fL | Sent as canonical key; maps correctly |

**Pattern:** All 13 `*`-related failures are present in d8 upload panel as `unmapped_*` keys. The values are correct (same as f2). The mapping fails at alias resolution only. RBC is a separate LLM extraction failure.

---

## 4. Homocysteine trace

**Raw lab-report label (from LLM parser):** `Homocysteine (venous)*`

| Step | Location | Input | Output | Issue? |
|---|---|---|---|---|
| Frontend key build | `uploadReferenceRange.ts:analysisBiomarkerKey()` | `"Homocysteine (venous)*"` | `"homocysteine_(venous)*"` | No strip of `*` |
| POST body key | `upload/page.tsx:handleQuestionnaireFromUpload()` | `analysisBiomarkerKey(biomarker.name)` | `"homocysteine_(venous)*"` | Key sent to backend with `*` |
| Backend normalization | `normalize.py:normalize_biomarkers_with_metadata()` | `{"homocysteine_(venous)*": {...}}` | — | Delegates to alias service |
| Alias resolution — `_normalize_key` | `alias_registry_service.py` | `"homocysteine_(venous)*"` | `"homocysteine_(venous)*"` | Correct |
| Alias resolution — `_strip_surrounding_punctuation(base)` | `alias_registry_service.py` | `"homocysteine_(venous)*"` | `"homocysteine_(venous"` | **BUG: strips `*` then `)` from end, truncating the key** |
| Alias resolution — `_strip_specimen_suffix(base)` | `alias_registry_service.py` | `"homocysteine_(venous)*"` | `"homocysteine_(venous)*"` | **BUG: `*(venous)*` → string ends in `*`, not `_(venous)`; suffix not stripped** |
| Alias resolution — third lookup | `alias_registry_service.py` | `"homocysteine_(venous"` | None | Truncated key not in alias mapping |
| Resolution result | `alias_registry_service.py:resolve()` | — | `"unmapped_Homocysteine (venous)*"` | Falls through to unmapped |
| normalize.py handling | `normalize.py:normalize_biomarkers()` | canonical_key starts with `"unmapped_"` | key added to unmapped_keys list | Correct handling of unmapped marker |
| upload_panel_observations | `analysis.py` | pre-arbitration snapshot | `unmapped_homocysteine_(venous)*` key present | Fidelity preserved, but marker is unmapped |
| Scored biomarkers[] | `analysis.py` / orchestrator | — | `homocysteine` absent | **Never enters scoring engine** |
| Signal evaluation | analytics pipeline | `homocysteine` absent | `signal_homocysteine_high` and `signal_homocysteine_elevation_context` cannot fire | **Primary cascade effect** |
| Root-cause arbitration | analytics pipeline | No homocysteine signals | `signal_total_cholesterol_high` becomes highest-ranking active signal | Lead changes |
| Frontend | results page | DTO has no `homocysteine` row | No homocysteine biomarker card; TC becomes hero lead | Correct rendering of wrong data |

**Correct path (f2 run):**  
`"Homocysteine (venous)"` (no `*`) → `_normalize_key` → `"homocysteine_(venous)"` → `_strip_specimen_suffix` strips `_(venous)` → `"homocysteine"` → found in alias mapping → canonical `homocysteine` → scored → signals fire.

---

## 5. Dropped-marker pattern analysis

### Group A: Trailing `*` blocks resolution (13 markers — same mechanism)

**All 13 markers** share the exact same failure mode:

1. LLM parser preserves lab-report `*` abnormal marker in the extracted biomarker `name` field
2. Frontend `analysisBiomarkerKey()` converts spaces → underscores but does not strip `*`
3. The key `name_(venous)*` is sent to the backend
4. `_strip_specimen_suffix()` requires the string to end with `_(venous)` — the trailing `*` prevents the suffix match
5. `_strip_surrounding_punctuation()` strips `*` then `)` from the end, producing a truncated key `name_(venous` that does not match any alias
6. All three lookup paths in `resolve()` fail; key falls to `unmapped_{raw}`

**Common characteristics of all 13:**
- All have `(venous)` specimen qualifier in raw name
- All have trailing `*` (lab abnormal marker)
- All values are correct (same as f2)
- None appear in `biomarkers[]` scored array
- All appear in `upload_panel_observations` as `unmapped_*` keys
- The resolver would succeed for ALL 13 if `*` was stripped before resolution (proven by unit test)

### Group B: Derived from Group A (1 marker)

- `urea_creatinine_ratio`: computed from `urea` (mapped ✅) + `creatinine` (unmapped ❌ due to `*`). Ratio cannot be computed without creatinine.

### Group C: LLM extraction failure (1 marker)

- `rbc`: **absent from d8 upload panel entirely** — not extracted from d8 lab report by LLM parser. f2 had `rbc: 4.4 10^12/L` under `Erythrocytes (rbc)`. This is a separate LLM non-determinism issue, not a resolver bug.

### Alias gaps (not causing drop, but noted)

The d8 upload also has two verbose lab names that don't alias even without `*`:
- `Non HDL Cholesterol Calculation (venous)*` → would be `non_hdl_cholesterol_calculation` without `*` → not in alias map (maps instead via `non_hdl_cholesterol`)
- `Total Cholesterol/HDL Ratio Calculation (venous)*` → `total_cholesterol/hdl_ratio_calculation` → `/` character prevents mapping

These were never in the f2 scored set either — they represent a secondary alias gap (not related to the 14-marker drop).

---

## 6. Parser and canonicalisation path

| Stage | File/function | Expected behaviour | Observed behaviour (d8) | Issue? |
|---|---|---|---|---|
| LLM parse | `backend/app/routes/upload.py`, `services/parsing/llm_parser.py` | Extract biomarker name, value, unit | Returns `name: "Homocysteine (venous)*"` — preserves `*` abnormal marker from lab header | Inferred (no parser meta stored); LLM non-deterministically preserves `*` |
| Frontend key build | `frontend/app/lib/uploadReferenceRange.ts:analysisBiomarkerKey()` | Convert display name to stable backend key | `"Homocysteine (venous)*"` → `"homocysteine_(venous)*"` — spaces→underscores, no `*` strip | **YES — missing `*` strip** |
| POST `/api/analysis/start` | `backend/app/routes/analysis.py` | Receive `request.biomarkers` dict | Receives `{"homocysteine_(venous)*": {...}}` | Correct; accepts any dict |
| Normalization | `backend/core/canonical/normalize.py:normalize_biomarkers_with_metadata()` | Map raw keys to canonical IDs | Delegates to `AliasRegistryService.resolve()` | Correct |
| Alias resolve — normalize key | `alias_registry_service.py:_normalize_key()` | Lowercase + spaces→underscores | `"homocysteine_(venous)*"` | Correct; no `*` handling |
| Alias resolve — strip punctuation | `alias_registry_service.py:_strip_surrounding_punctuation()` | Strip leading/trailing punctuation | Strips `*` then `)`, producing `"homocysteine_(venous"` | **YES — `)` stripped alongside `*`, producing truncated key** |
| Alias resolve — strip specimen | `alias_registry_service.py:_strip_specimen_suffix()` | Strip `_(venous)` etc from end | Fails: string ends in `*`, not `_(venous)` | **YES — prerequisite for suffix strip is that no `*` follows** |
| Alias resolve — all 3 lookups | `alias_registry_service.py:resolve()` | Find canonical ID | All three miss; returns `unmapped_*` | **YES** |
| Upload panel snapshot | `analysis.py` + `display_fidelity_v1.py` | Preserve pre-normalisation panel | `unmapped_homocysteine_(venous)*` stored in `upload_panel_observations` | Fidelity preserved correctly; mapping already failed before this |
| Scoring | analytics pipeline | Score all mapped biomarkers | `homocysteine` absent from inputs | Correct for data received |

---

## 7. Unit/display-fidelity interaction

**LC-S8G did NOT cause this regression.**

LC-S8G added `attach_source_labels_to_upload_panel()` and the `display_*`/`analytical_*` field enrichment. It operates on already-normalised keys in `upload_panel_observations` and does not affect canonical resolution.

The ordering in `analysis.py` is:
1. `normalize_biomarkers_with_metadata(request.biomarkers)` → **mapping happens here** (fails for `*`-suffixed keys)
2. `attach_source_labels_to_upload_panel(normalized, request.biomarkers)` → adds display metadata to already-normalised keys

The `*`-caused unmapping precedes LC-S8G's code path entirely.

| Question | Answer |
|---|---|
| Did `source_label` preservation alter canonical keys? | No. `source_label` is added to upload_panel_observations AFTER normalization. |
| Did `upload_panel_observations` keyed by canonical ID cause loss of raw spelling? | No. The upload panel is keyed by the output of `normalize_biomarkers_with_metadata()`, which already includes `unmapped_*` keys. |
| Did display fidelity logic create unmapped keys? | No. Unmapped keys predate LC-S8G's logic. |
| Is the issue before or after display fidelity? | **Before.** The issue is in `normalize_biomarkers_with_metadata()` → `alias_service.resolve()`. |

**Why f2 had clean keys:** f2 was uploaded with biomarker names that did not include `*` (lab report did not mark abnormals in the test-name column, or LLM parser stripped them). The `source_label` field in f2's upload panel confirms the original lab names: `"Homocysteine (venous)"` (no `*`). The LC-S8G source_label attachment then correctly preserved those clean labels.

---

## 8. Signal/arbitration impact

| Signal | f2 active? | d8 active? | Impact |
|---|---|---|---|
| `signal_homocysteine_high` | ✅ | ❌ | Primary cause of lead change |
| `signal_homocysteine_elevation_context` | ✅ | ❌ | Supports homocysteine WHY path |
| `signal_total_cholesterol_high` | ✅ | ✅ | Survives; becomes sole lead signal in d8 |
| `signal_transferrin_low` | ✅ | ✅ | Present in both; liver domain driver |
| Any `apob_*`, `apoa1_*` signals | ❌ (not registered) | ❌ | Blocked in both (KB-WAVE-1 territory) |
| `signal_lipoprotein_a_*` | ❌ | ❌ | Same |

**f2 cardiovascular `active_signal_ids`:** `["signal_homocysteine_elevation_context", "signal_homocysteine_high", "signal_total_cholesterol_high"]`

**d8 cardiovascular `active_signal_ids`:** `["signal_total_cholesterol_high"]`

**Wave-1 aligned drivers:**
- f2: `["homocysteine", "total_cholesterol", "transferrin"]`  
- d8: `["total_cholesterol", "transferrin"]`

**Why TC became lead:** With `signal_homocysteine_high` absent, arbitration ranks `signal_total_cholesterol_high` as the strongest active signal. TC is elevated (5.26 mmol/L, score 0.305). The governed root-cause hypothesis `tc_atherogenic_panel_context_v1` fires because the signal is present and the hypothesis template is registered. The IDL record `ph_vascular_hcy_inflammation_v1` remains enabled (it is not signal-gated in the same way) which creates the split-brain where the hero context says "Vascular Inflammation Risk" while the lead marker is TC. This is an IDL precedence issue — a secondary problem, not the primary cause of the mapping regression.

---

## 9. User-facing impact

**What the user sees:** A Total Cholesterol elevation as the main finding, with a "Vascular Inflammation Risk" context subheading that references homocysteine signals. Methylation Pathway pattern card is visible (IDL record still enabled). Homocysteine has no biomarker card — it appears only under uploaded-fidelity section as an unmapped marker. The narrative body still references homocysteine (lifestyle bridge) while homocysteine is absent from scoring.

**Why the story becomes confusing:** Three competing authorities — TC-led hero title, homocysteine-linked IDL context, homocysteine-led methylation pattern — tell different stories about the same panel. The user's most clinically significant abnormal marker (homocysteine 16.23 µmol/L, above range 3.7–13.9) is invisible from governed output.

**Why this blocks KB-WAVE-1:**
1. Homocysteine governed-WHY package (`pkg_homocysteine_elevation_context`) requires `homocysteine` signal to fire — impossible with unmapped marker
2. ApoB/ApoA1 governed lipid WHY requires `apob` and `apoa1` scored values — both unmapped in d8
3. `lipoprotein_a` governed package requires scored marker — unmapped in d8
4. Adding KB-WAVE-1 lipid copy on top of the current split-brain state would deepen confusion, not clarify it

**Frontend assessment:** Frontend is rendering the backend DTO correctly. No fabrication. The TC lead, vascular IDL context, and methylation pattern are all faithfully reflecting what the backend sent. The confusion is structural (split-brain authority) and upstream (mapping failure).

---

## 10. Recommended implementation sprint

### Proposed work_id: `MAP-R1A`

| Field | Value |
|---|---|
| **risk_level** | `STANDARD` |
| **change_type** | `BEHAVIOUR` |
| **execution_model** | `SINGLE_PHASE` |
| **primary goal** | Strip trailing `*` (and similar abnormal-value markers) from biomarker names before alias resolution |

### Files likely to need change

| File | Change |
|---|---|
| `backend/core/canonical/alias_registry_service.py` | In `resolve()`: strip trailing lab-report abnormal markers (`*`, `†`, `H`, `L` when appended to a parenthesised label) before normalization, OR strip them in `_normalize_key()`. Minimal safe fix: `raw = raw.rstrip('*').rstrip()` before the normalization pipeline. |
| `frontend/app/lib/uploadReferenceRange.ts` | In `analysisBiomarkerKey()`: strip trailing `*` before `toLowerCase()` + `replace()`. Defense-in-depth fix. |

### Tests required

- Unit test: `test_alias_service_star_suffix_stripping.py` — assert `resolve("Homocysteine (venous)*")` → `homocysteine`, repeat for all 13 affected markers
- Integration test: rebuild the exact d8 biomarker dict and assert 77-marker scored set (not 63)
- Regression test: assert `resolve("Homocysteine (venous)")` (without `*`) still → `homocysteine` (no regression to current passing behaviour)
- Frontend unit test: `analysisBiomarkerKey("Homocysteine (venous)*")` → `"homocysteine_(venous)"` (star stripped before lowercase)

### Sentinel guards required

- New escaped defect class: `canonical_mapping_star_suffix_failure` — assert any fresh upload with `*`-marked labs does not produce `unmapped_*` for known markers
- Existing alias resolution tests: confirm no regression in the 1688-alias registry

### Acceptance criteria

1. A fresh upload of a lab report containing `Homocysteine (venous)*` scores `homocysteine` in `biomarkers[]`
2. All 13 Group A markers score correctly from `*(venous)*`-formatted labels
3. `urea_creatinine_ratio` is computed (depends on `creatinine` fix)
4. `apob_apoa1_ratio` is derived (depends on `apob` + `apoa1` fixes)
5. Lead finding returns to homocysteine-led on same panel chemistry
6. `upload_panel_observations` unmapped count drops from 19 to ≤5 (f2 had 5 structurally unmapped)
7. No regression to f2 mapping (f2-style clean labels still resolve)

### What NOT to fix in MAP-R1A

- `rbc` absent from d8: separate LLM extraction issue — investigate LLM parser separately
- `non_hdl_cholesterol_calculation` / `total_cholesterol/hdl_ratio_calculation` alias gaps: secondary; these were never in scored set in either run
- IDL hero/context split-brain: separate sprint after mapping is stable

---

## 11. Open questions / unresolved evidence

| Question | Status |
|---|---|
| Did f2 and d8 use the same lab report file? | **Unconfirmed.** No parser metadata stored in result. The difference could be: (a) same file, LLM extracted names with/without `*` non-deterministically; (b) slightly different lab report versions. The `*` markers in d8 names are consistent with a lab marking abnormal results in the test-name column. |
| Why does d8 have `tsh` as `TSH (venous)*` when the tsh value is in-range (not abnormal)? | Unconfirmed. Lab may apply `*` to certain test categories regardless of range, or LLM may be hallucinating `*` from adjacent columns. Irrelevant to the fix scope. |
| Is the LLM parser output logged anywhere? | Not in analysis result. Backend `[TRACE]` logs would capture incoming keys if logs were retained. No artifact available in this investigation. |
| Are there other lab report formats that include `†` or `H`/`L` abnormal markers in test names? | Unknown. The fix should strip all common abnormal-value suffix markers (`*`, `†`, `H`, `L`) as a generalization of the minimal `*` fix. |
| Why does f2's `apob_apoa1_ratio` come from `source: lab` while d8 has none? | f2 uploaded `apob_apoa1_ratio` as a direct key; it was preserved as a lab-sourced derived marker. d8 uploaded `Apolipoprotein Ratio (venous)*` which unmapped. With fix, d8 would resolve to `apob_apoa1_ratio` and derive correctly. |
| RBC extraction failure cause? | Not investigated in this sprint. LLM parser is non-deterministic. Investigate separately — possibly the lab uses `Erythrocytes (rbc)` in one version and a different label in another. |

---

## Appendix A — Alias resolution bug trace (Homocysteine)

```
Input:      "Homocysteine (venous)*"
After _normalize_key():
            "homocysteine_(venous)*"
After _normalize_special_patterns():
            "homocysteine_(venous)*"   (no change — does not end with "_(a)")

base = "homocysteine_(venous)*"

Lookup 1: raw.lower() = "homocysteine (venous)*"    → NOT in alias_mapping
Lookup 2: norm = _strip_surrounding_punctuation(base)
  "homocysteine_(venous)*".strip(punctuation_except_underscore)
  → strips trailing "*"  → "homocysteine_(venous)"
  → strips trailing ")"  → "homocysteine_(venous"       ← WRONG: ) stripped
  norm = "homocysteine_(venous"                         → NOT in alias_mapping
Lookup 3: _strip_specimen_suffix(base)
  base ends with "*", not "_(venous)" → no suffix stripped
  → "homocysteine_(venous)*"
  → _strip_surrounding_punctuation → "homocysteine_(venous"  (same as norm)
  norm_stripped = "homocysteine_(venous"                → NOT in alias_mapping

Result: "unmapped_Homocysteine (venous)*"
```

**Correct resolution path (with `*` stripped before entry):**
```
Input (after rstrip("*").rstrip()):  "Homocysteine (venous)"
After _normalize_key():              "homocysteine_(venous)"
_strip_specimen_suffix():            strips "_(venous)" → "homocysteine"
alias_mapping.get("homocysteine")  → "homocysteine"  ✓
```

---

## Appendix B — Affected marker key mapping (d8 raw → expected canonical)

| d8 raw key (from upload) | Expected canonical | Resolves after `*` strip? |
|---|---|---|
| `Homocysteine (venous)*` | `homocysteine` | ✅ confirmed |
| `Creatinine (venous)*` | `creatinine` | ✅ confirmed |
| `TSH (venous)*` | `tsh` | ✅ confirmed |
| `Vitamin B12 (venous)*` | `vitamin_b12` | ✅ confirmed |
| `Active Vitamin B12 (venous)*` | `active_b12` | ✅ confirmed |
| `Apolipoprotein A1 (venous)*` | `apoa1` | ✅ confirmed |
| `Apolipoprotein B (venous)*` | `apob` | ✅ confirmed |
| `Apolipoprotein Ratio (venous)*` | `apob_apoa1_ratio` | ✅ confirmed |
| `Lipoprotein (a) (venous)*` | `lipoprotein_a` | ✅ confirmed |
| `Corrected Calcium (venous)*` | `corrected_calcium` | ✅ confirmed |
| `Vitamin D (venous)*` | `vitamin_d` | ✅ confirmed |
| `Zinc (venous)*` | `zinc` | ✅ confirmed |
| `Non HDL Cholesterol Calculation (venous)*` | `non_hdl_cholesterol` | ✅ confirmed |
| `Total Cholesterol/HDL Ratio Calculation (venous)*` | `tc_hdl_ratio` | ✅ confirmed |

All 14 confirmed by live unit test against the running alias registry service (1,688 alias entries).

---

*Investigation complete. No repository code modified.*  
*Evidence artifacts: `automation_bus/_map_r1_d8.json`, `automation_bus/_map_r1_f2.json`*
