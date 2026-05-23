# LC-S13 — Lifestyle Propagation, Coherence Guard, Narrative Language Audit

**Work package:** LC-S13  
**Branch:** `scaffold/lc-s13-lifestyle-coherence-narrative`  
**Status:** Implementation complete (awaiting human review; not merged)  
**Gate A (scaffold definition approval):** Still DRAFT — sprint proceeded per explicit user directive.

---

## 1. Preflight results

| Check | Result |
|-------|--------|
| Branch | `scaffold/lc-s13-lifestyle-coherence-narrative` |
| Stash | Empty (no convenience stash; prior stash dropped in triage) |
| Work package token | `LC-S13` / branch match — kernel STARTED |
| Controlling docs | Present (`HealthIQ_AI_core_scaffold_completion_definition_v1.md`, FINAL plan) |
| Q-1/Q-2 questionnaire redesign | No active shape change on mapped `lifestyle_inputs`; proceeded on stable backend mapper |
| Cross-sprint guards | LC-S8F, LC-S8G, LC-S8D, LC-S10B, LC-S11A — all passed (2026-05-20 run) |

---

## 2. Lifestyle computation trace

```
questionnaire / lifestyle_inputs
  → LifestyleModifierEngine (system_modifiers, confidence_penalty per system)
  → lifestyle_interpretation_bridges_v1 (alcohol, renal, fasting)
  → AnalysisDTO.meta + AnalysisDTO.lifestyle
  → narrative_report_compiler_v1 (body_overview supplement)
  → consumer_domain_scores (unchanged biomarker truth)
```

---

## 3. `confidence_adjustments`

- Mapped from per-system `confidence_penalty` in orchestrator meta/DTO lifestyle artifact.
- With **complete core inputs** (PROFILE_LOW fixture), all penalties are **0.0** — expected; missing-input penalty is suppressed when `missing_core_inputs` is empty.
- PROFILE_HIGH can carry non-zero penalties when musculoskeletal core inputs are absent (e.g. sit/stand fields) — not surfaced as user-facing zeros; documented in regression test.
- **No wiring of meaningless zeros to frontend** — Scope A did not STOP; modifiers and bridges produce meaningful internal deltas.

---

## 4. Lifestyle bridges

| Bridge | Fires when (AB panel) | Surfaced to user (LC-S13) |
|--------|------------------------|---------------------------|
| `alcohol_methylation_macrocytosis` | ≥8 units/week + elevated homocysteine/MCV | Yes — governed paragraph |
| `hydration_activity_renal` | Low fluid and/or high activity + renal markers on panel | Yes — when active |
| `fasting_dietary_glycaemic` | Intermittent fasting + normal/low HbA1c | Yes — when questionnaire + labs align |

Raw `rationale_codes` remain in meta only; regression guards block leakage.

---

## 5. Sprint proceed / split

**Proceeded normally.** No LC-S13A/B split required — computation path is meaningful; propagation extended via `lifestyle_consumer_surface_v1.py`.

---

## 6. Files changed

| File | Change |
|------|--------|
| `backend/core/analytics/lifestyle_consumer_surface_v1.py` | **New** — governed consumer lifestyle paragraphs |
| `backend/core/analytics/narrative_report_compiler_v1.py` | Wire multi-bridge lifestyle supplement |
| `backend/core/analytics/report_compiler_v1.py` | Neutralise `_why_template` mock overclaim |
| `backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py` | **New** — LC-S13 regression pack |
| `sentinel/packs/lc_s10b_launch_core_protection_v1.json` | LC-S13 defect classes |
| `docs/audit-papers/LC-S13_lifestyle_coherence_narrative_notes.md` | This note |

**Forbidden paths not touched:** `knowledge_bus/**`, SSOT scoring/units, bus scripts.

---

## 7. Coherence guards added

- `test_lc_s13_domain_band_headline_polarity_guard` — stable/strong + high confidence + “not a simple all-clear” requires contributor conflict, risk-led IDL, or active signals.
- `test_lc_s13_blood_sugar_no_narrative_without_active_signals` — extends LC-S11A inactive-signal guard.
- Sentinel: `domain_band_headline_polarity_contradiction`, `domain_active_signal_false_claim`.

---

## 8. Narrative language findings

| Phrase | Action |
|--------|--------|
| `your measured` in `_why_template` | **Corrected** → “The main lab anchor on this panel…” |
| `your measured` in lifestyle metabolic disclaimer | **Corrected** → “lab values on this panel” |
| `your cardiovascular` in domain headlines | **Retained** — bounded panel copy, coherent with D-4 guards |
| Frontend `lcS4ResultsCopy.ts` AI disclosure | **Unchanged** — intentional product disclosure |

---

## 9. Sentinel updates

Added to `lc_s10b_launch_core_protection_v1.json`:

- `lifestyle_visible_payoff_missing`
- `lifestyle_bridge_internal_code_leakage`
- `domain_band_headline_polarity_contradiction`
- `domain_active_signal_false_claim`
- `mock_mode_personalisation_overclaim`
- `governance_label_user_visible_leakage`

All point to `backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py`.

---

## 10. Tests run

```text
python -m pytest backend/tests/regression/test_lc_s13_lifestyle_coherence_narrative.py -q  → PASS (9 tests)
python -m pytest backend/tests/regression/test_lc_s8f_phase_b_true_conversions.py -q      → PASS
python -m pytest backend/tests/regression/test_lc_s8g_uploaded_unit_display_fidelity.py -q  → PASS
python -m pytest backend/tests/regression/test_lc_s8d_unit_governance_sentinel.py -q        → PASS
python -m pytest backend/tests/regression/test_lc_s10b_launch_core_protection.py -q         → PASS
python -m pytest backend/tests/regression/test_lc_s11a_trust_blocker_correction.py -q       → PASS
```

Frontend not changed — no `npm` run required.

---

## 11. Residual risks

- Proving harness fingerprints (`latest_fingerprints.json`) still contain pre-LC-S13 “Your measured…” heads until harness is re-run and committed separately.
- Gate A scaffold definition remains DRAFT — human approval still required before programme sign-off.
- Renal/fasting bridges depend on questionnaire fields not always present in API-only runs.
- Browser UAT not executed; API/DTO evidence: contrasting profiles change `body_overview` and `system_modifiers` without biomarker value drift.

---

## 12. Recommendation for next sprint

1. Human approve Gate A scaffold definition.  
2. Re-run `launch_core_proving_harness.py` to refresh fingerprints after narrative wording change.  
3. Consider LC-S13B frontend surfacing of lifestyle block (if product wants dedicated UI section beyond `body_overview`).  
4. Optional: expose `confidence_adjustments` only when non-zero with governed explanation copy.

---

## API/DTO evidence (contrasting profiles, same AB panel)

- **Low profile:** minimal lifestyle paragraph count; no smoking copy.  
- **High profile:** `body_overview` includes smoking and/or alcohol governed text; `system_modifiers` differ; biomarker values identical between runs.  
- **Homocysteine lead:** unchanged on AB baseline (CHECK 6 family preserved via LC-S11A guards).
