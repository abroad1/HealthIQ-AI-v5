# ARCH-CONV-FINAL — Layer C Boundary and Leakage Inventory

**Work ID:** `ARCH-CONV-FINAL-AUDIT`  
**Branch:** `audit/arch-conv-final-programme`  
**Baseline HEAD:** `522873428882d9f47093e283a3ab31dc16fcd684`  
**Independence:** Fresh frontend/code scan (not prior FE audit reports as proof)

---

## Classification legend

| Class | Meaning |
|---|---|
| PRESENTATION_ONLY | Format/layout/scrub only |
| LEGITIMATE_TRANSLATION | Enum→label / assembly within supplied boundaries |
| BOUNDARY_LEAK | FE/Layer C invents or re-decides medical meaning |
| UNRESOLVED | Needs policy confirmation |

Any **BOUNDARY_LEAK** or safety-material **UNRESOLVED** blocks programme PASS.

---

## Inventory (material items)

| file | function/component | input | logic | output | classification | required action |
|---|---|---|---|---|---|---|
| `frontend/app/lib/resultsPageLayout.ts` | `pickSeverityPrimaryDriverCluster` | clusters severity/score | FE severity rank map + score tie-break | primary driver | **BOUNDARY_LEAK** | Consume backend-ranked lead only |
| `frontend/app/lib/resultsPageLayout.ts` | `pickHeroAlignedPrimaryDriver` | clusters + IDL | Alignment threshold then severity | hero driver | **BOUNDARY_LEAK** | Prefer Wave1/backend lead |
| `frontend/app/lib/resultsPageLayout.ts` | `pickTopDriverBiomarkers` | biomarker status | FE ranks abnormal/border when incomplete | top markers | **BOUNDARY_LEAK** | Backend order only |
| `frontend/app/lib/resultsPageLayout.ts` | `evidenceLevelFromCluster` | confidence/severity | FE bins evidence labels | evidence copy | **BOUNDARY_LEAK** | Display backend labels |
| `frontend/app/(app)/results/page.tsx` | cluster mapper | missing confidence | Invents **`0.85`** | ClusterSummary | **BOUNDARY_LEAK** | Pass through unknown |
| `frontend/app/components/biomarkers/BiomarkerDials.tsx` | `getDialColor` | dial % | Invents red/yellow from position | clinical colour | **BOUNDARY_LEAK** | Colour from backend status only |
| `frontend/app/components/results/LayerCInsightSection.tsx` | collect/sort + cards | layer_c_features | Re-ranks by confidence; invents explanations | insight cards | **BOUNDARY_LEAK** | Render backend-ordered prose only |
| `frontend/app/components/clusters/ClusterInsightPanel.tsx` | `getClinicalRecommendations` | severity/name/score | Invents urgency/lifestyle advice | clinical recommendations | **BOUNDARY_LEAK** | Quarantine/delete (exported; not on live import path) |
| `frontend/app/lib/biomarkerPatternRelevance.ts` | `derivePatternRelevanceLine` | driver + groups | FE-authored causal-ish lines | expansion prose | **BOUNDARY_LEAK** | Backend contribution text only |
| `frontend/app/components/results/SystemUnderstandingSection.tsx` | Blocks A–C | primaryDriver/IDL | Template medical framing | educational copy | **BOUNDARY_LEAK** (soft) | Governed copy only |
| `frontend/app/components/clusters/ClusterSummary.tsx` | score colour helpers | numeric score | FE clinical colour thresholds | visual risk coding | **BOUNDARY_LEAK** (mild) | Backend band/status |
| `frontend/app/components/insights/InsightsPanel.tsx` | category sort | severity/confidence | FE re-order | display order | **BOUNDARY_LEAK** (mild) | Preserve backend order |
| `frontend/app/components/results/PrimaryFindingAndWhy.tsx` | renderer | clinician_report | Pass-through DTO | Section 3 | PRESENTATION_ONLY | Keep |
| `frontend/app/components/results/RootCauseEvidenceSummary.tsx` | state phrase + render | hypotheses | Enum→phrase; shows backend evidence | WHY walkthrough | LEGITIMATE_TRANSLATION | Keep |
| `frontend/app/components/results/ClinicianReportRenderer.tsx` | renderer | clinician_report | Display only | clinician view | PRESENTATION_ONLY | Keep |
| `frontend/app/components/results/DeterministicNarrativeSurface.tsx` | narrative cards | narrative_report_v1 | Scrub + render | narrative | PRESENTATION_ONLY | Keep |
| `frontend/app/lib/feR5aIdlPatternGuards.ts` | safe IDL filter | IDL flags | Safety/visibility filter | visible IDL | LEGITIMATE_TRANSLATION | Keep |
| `frontend/app/lib/uploadReferenceRange.ts` | band match | upload values | Pre-analysis range assist | upload review | LEGITIMATE_TRANSLATION | Must not become analysis scoring |

---

## Summary counts

| Classification | Count (material scan) |
|---|---:|
| BOUNDARY_LEAK | ≥10 (including mild/soft) |
| PRESENTATION_ONLY / LEGITIMATE_TRANSLATION | Majority of results renderers |
| ACTIVE Layer B medical activation in FE | Not found |
| WHY hypothesis selection from raw labs in FE | Not found |

---

## Verdict for programme PASS gate (audit, at baseline SHA)

**Layer C medical-decision boundary is not closed.**  
Hardest live-path leaks: primary-driver arbitration, invented confidence, dial colour invention, LayerCInsightSection prose/ranking.

No substantive corrections implemented in this audit package (forbidden). Recommend bounded FE correction package after UAT confirmation.

---

## ARCH-CONV-CORRECT-1 closure status (added by the correction package)

**Work ID:** `ARCH-CONV-CORRECT-1` · **Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`

All 12 `BOUNDARY_LEAK` rows above (including the mild/soft ones) are **CLOSED**. Row-by-row
evidence, the Layer B authority now supplying each decision, and the failure behaviour when a
governed field is missing are recorded in:

```text
docs/architecture/ARCH-CONV-CORRECT-1_layer_c_boundary_closure_report.md
```

| Row | Closure |
|---|---|
| `pickSeverityPrimaryDriverCluster` | Removed |
| `pickHeroAlignedPrimaryDriver` | Replaced by `selectGovernedPrimaryDriver` consuming `meta.insight_graph.primary_driver_v1` |
| `pickTopDriverBiomarkers` | Backend marker order only |
| `evidenceLevelFromCluster` / `evidenceFromInsight` | Removed; card now shows action provenance (`Source:`) |
| `results/page.tsx` invented `0.85` | Passes `null`; confidence row omitted when absent |
| `getDialColor` | Backend status only; unknown → neutral |
| `LayerCInsightSection` | Fixed display order + governed copy module |
| `ClusterInsightPanel.getClinicalRecommendations` | Component deleted and unexported |
| `derivePatternRelevanceLine` | File deleted; backend contribution text only |
| `SystemUnderstandingSection` blocks A–C | Governed copy module |
| `ClusterSummary` score colour helpers | Backend severity band |
| `InsightsPanel` category sort | Backend order preserved |

`uploadReferenceRange.ts` re-verified as `LEGITIMATE_TRANSLATION`: imported only by the upload
and preview surfaces, absent from the results/analysis path.

No safety-material `UNRESOLVED` item remains. Enforcement is executable via
`backend/scripts/validate_arch_conv_correct1_gate.py` (WS4 block) plus
`frontend/tests/components/LayerCMedicalBoundary.test.tsx`.

This closure does **not** by itself grant programme PASS: a human UAT re-check of the live page
remains outstanding, and the residual limitations in the correction reports still apply.
