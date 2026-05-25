# MAP-R1A — Star-Suffix Canonical Mapping Fix Notes

## 1. Preflight

| Check | Result |
|---|---|
| Branch | `mapping/map-r1a-star-suffix-canonical-fix` |
| Stash | Empty |
| Kernel | `MAP-R1A` STARTED |
| MAP-R1 investigation | Present |

## 2. MAP-R1 root-cause summary

Trailing `*` on LLM-extracted labels (e.g. `Homocysteine (venous)*`) prevented `_(venous)` specimen suffix stripping. `_strip_surrounding_punctuation()` then stripped `*` and `)`, truncating keys to `homocysteine_(venous` and yielding `unmapped_*`. d8 run scored 63 vs 77 markers; homocysteine signals absent; lead shifted to Total Cholesterol.

## 3. Mapping fix implemented

**Backend** (`alias_registry_service.py`):

- `_strip_abnormal_lab_marker_suffix()` — strips trailing `*`, `†`, and conservative `) H` / `) L` flags before normalisation.
- `resolve()` applies cleaning before `_normalize_key` and specimen suffix logic.
- `_strip_surrounding_punctuation()` no longer strips `(` / `)` to avoid truncating specimen keys.

**Frontend** (`uploadReferenceRange.ts`):

- `stripAbnormalLabMarkerSuffix()` + `analysisBiomarkerKey()` defence-in-depth (backend remains authoritative).

## 4. Frontend defence-in-depth

Yes — `stripAbnormalLabMarkerSuffix` exported and used in `analysisBiomarkerKey()`.

## 5. Affected markers tested

14 starred venous labels from sprint list + d8 Group A subset in regression test — all resolve to expected canonical IDs (see unit parametrized table).

## 6. Before / after alias examples

| Label | Before | After |
|---|---|---|
| `Homocysteine (venous)*` | `unmapped_Homocysteine (venous)*` | `homocysteine` |
| `Apolipoprotein B (venous)*` | `unmapped_...` | `apob` |
| `Lipoprotein (a) (venous)*` | `unmapped_...` | `lipoprotein_a` |
| `Homocysteine (venous)` | `homocysteine` | `homocysteine` (unchanged) |

## 7. d8 scored biomarker count restoration

Full end-to-end re-upload of d8 fixture not run in this session. **Lowest-layer proof:** all MAP-R1 Group A starred keys now resolve to canonical IDs (not `unmapped_*`), including `homocysteine`, `apob`, `apoa1`, `lipoprotein_a`, `creatinine`. Expect scored count to increase by ~13 when same panel is re-analysed.

## 8. Signal / arbitration impact

When starred labels map correctly, homocysteine and apolipoprotein markers re-enter the scored path; `signal_homocysteine_*` and lipid signals can fire again. Lead arbitration should become analytically plausible for the full marker set (requires re-run to confirm).

## 9. Tests added/updated

| File | Purpose |
|---|---|
| `backend/tests/unit/test_alias_service_star_suffix_stripping.py` | Parametrised canonical resolution |
| `backend/tests/regression/test_canonical_mapping_star_suffix_failure.py` | Sentinel + d8-style keys |
| `frontend/tests/lib/uploadReferenceRange.test.ts` | Frontend key stripping |

## 10. Sentinel

- `canonical_mapping_star_suffix_failure`
- `canonical_mapping_specimen_suffix_truncation`
- `canonical_mapping_known_marker_unmapped_after_star_suffix`

All → `test_canonical_mapping_star_suffix_failure.py`.

## 11. Residual risks

- LLM may omit markers entirely (e.g. d8 RBC) — separate from star suffix.
- Unusual abnormal suffix conventions not covered by `*` / `†` / `) H|L` may still fail.
- Full scored-count restoration requires re-analysis of d8 upload, not proven here.

## 12. KB-WAVE-1 readiness

**After merge + d8 re-upload verification:** KB-WAVE-1 is **unblocked at the mapping layer**. Content/DTO depth for biomarker cards remains a separate KB-WAVE scope. Do not start KB-WAVE-1 until human authorises next sprint.
