# ARCH-CONV-CORRECT-1 — Layer C Boundary Closure Report

**Work ID:** `ARCH-CONV-CORRECT-1`
**Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Workstream:** WS4
**Authoritative defect list:** `docs/architecture/ARCH-CONV-FINAL_layer_c_boundary_and_leakage_inventory.md`

---

## 1. Boundary principle applied

Layer C may present, format and translate governed Layer B output. Where Layer C previously
made a medical decision, the decision was either relocated to the Layer B authority that
already owned it, or removed so the surface renders nothing rather than inventing a substitute.

No new frontend fallback was created. Where a governed field is absent, the affected surface is
suppressed or rendered neutral.

## 2. Closure matrix

| # | File / function | Was | Layer B authority now supplying it | Now | Status |
|---:|---|---|---|---|---|
| 1 | `resultsPageLayout.ts` · `pickSeverityPrimaryDriverCluster` | FE severity rank map + score tie-break chose the primary driver | `report_v1.top_findings[0]` under the governed ranking policy | Function removed | **CLOSED** |
| 2 | `resultsPageLayout.ts` · `pickHeroAlignedPrimaryDriver` | FE label-similarity threshold, then severity fallback | `meta.insight_graph.primary_driver_v1` | Replaced by `selectGovernedPrimaryDriver`, which resolves the governed record to a cluster by identity and returns `null` when unresolved | **CLOSED** |
| 3 | `resultsPageLayout.ts` · `pickTopDriverBiomarkers` | FE re-ranked markers by abnormality when the backend list was short | Governed driver marker order | Backend order only, truncated to three | **CLOSED** |
| 4 | `resultsPageLayout.ts` · `evidenceLevelFromCluster` / `evidenceFromInsight` | FE binned backend severity/confidence into clinical-sounding "evidence" labels | Provenance of the action line | Functions removed; static source labels (`ACTION_SOURCE_*`) describe where the line came from, and the card renders `Source:` rather than `Evidence:` | **CLOSED** |
| 5 | `results/page.tsx` cluster mapper | Substituted `confidence = 0.85` when the backend supplied none | Backend cluster confidence only | Passes `null`; `ClusterSummary` omits the confidence row entirely when it is absent | **CLOSED** |
| 6 | `BiomarkerDials.tsx` · `getDialColor` | Chose red/amber/green from the dial's numeric position when status was unknown | Backend biomarker `status` | Colour from status only; unknown status renders neutral grey | **CLOSED** |
| 7 | `LayerCInsightSection.tsx` | Re-ranked features by confidence and authored card prose inline | Layer B confidence acts as a presence gate only | Fixed display order from `LAYER_C_INSIGHT_DISPLAY_ORDER`; all prose moved to the governed copy module `app/lib/layerCInsightCopy.ts` | **CLOSED** |
| 8 | `ClusterInsightPanel.tsx` · `getClinicalRecommendations` | Generated urgency and lifestyle advice from cluster name/severity/confidence; also derived marker status from a raw score | n/a — no Layer B authority for FE-authored advice | Component deleted and removed from the clusters barrel export (grep-proved unused by any route, page or test before deletion) | **CLOSED** |
| 9 | `biomarkerPatternRelevance.ts` · `derivePatternRelevanceLine` | FE-authored lines connecting a marker to the lead pattern | `biomarker.contribution_context.factual_statement` | File deleted; the expansion renders backend contribution text and governed group names only | **CLOSED** |
| 10 | `SystemUnderstandingSection.tsx` blocks A–C | Templated medical framing inline | Governed names only (primary driver, balanced-systems topic, IDL retail label, marker labels) | Prose moved to `app/lib/systemUnderstandingCopy.ts`, which documents that the copy is fixed and non-personalised; the "often where X leads" phrasing was replaced with a factual restatement of the Layer B ranking | **CLOSED** (soft item) |
| 11 | `ClusterSummary.tsx` score colour helpers | FE numeric thresholds produced clinical colour coding | Backend `severity` band | `SEVERITY_TEXT_COLORS` / `SEVERITY_BAR_COLORS` keyed on the backend band; the cross-cluster average has no backend band and renders neutral | **CLOSED** (mild item) |
| 12 | `InsightsPanel.tsx` category sort | Re-ordered insights by severity then confidence | Backend emission order | Sort and `severityOrder` map removed | **CLOSED** (mild item) |

## 3. Items confirmed as not leaks

| File | Classification retained | Basis |
|---|---|---|
| `PrimaryFindingAndWhy.tsx`, `ClinicianReportRenderer.tsx`, `DeterministicNarrativeSurface.tsx` | PRESENTATION_ONLY | DTO pass-through / scrub and render |
| `RootCauseEvidenceSummary.tsx` | LEGITIMATE_TRANSLATION | Enum→phrase over backend-supplied evidence |
| `feR5aIdlPatternGuards.ts` | LEGITIMATE_TRANSLATION | Safety/visibility filter over IDL flags |
| `uploadReferenceRange.ts` | LEGITIMATE_TRANSLATION | Imported only by `upload/page.tsx`, `ParsedTable.tsx`, `EditDialog.tsx` and its own test — verified absent from the results/analysis path, so it has not become analysis scoring |

No safety-material `UNRESOLVED` item remains in the inventory.

## 4. Additive DTO carrying the governed decision

```text
InsightGraphV1.primary_driver_v1   (backend/core/contracts/insight_graph_v1.py)
PrimaryDriverAuthorityV1          (frontend/app/types/analysis.ts)
```

Built by `backend/core/analytics/primary_driver_authority_v1.py`, which projects
`report_v1.top_findings[0]` — already ranked under
`PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_V1` — onto the cluster identity Layer C renders,
using deterministic identity matching (lead system, then lead primary metric). It adds no
medical reasoning, reports `cluster_resolved: false` instead of guessing, and returns `None`
when there is no governed lead so Layer C suppresses the surface.

## 5. Failure behaviour verification

`frontend/tests/components/LayerCMedicalBoundary.test.tsx` proves, by rendering:

- a marker with no backend status is not coloured red or amber (neutral only);
- a marker whose value is outside its reference range but whose backend status is `normal`
  renders green — colour follows the backend, not the value;
- a cluster with no backend confidence renders no confidence claim;
- Layer C features render in the fixed order even when a later feature has higher confidence.

`frontend/tests/lib/resultsHeroAlignment.test.ts` proves `selectGovernedPrimaryDriver` returns
`null` when the governed record is absent, empty, or names a cluster that is not on the page —
no severity fallback.

## 6. Type and test status

- `npx tsc --noEmit` (run in `frontend/`) — exit code 0.
- Affected jest suites: `resultsHeroAlignment`, `LayerCMedicalBoundary`, `ClusterSummary`,
  `SystemUnderstandingSection` — pass.
- `BiomarkerDials.test.tsx::displays icon-only status badges per marker` fails on the expand-button
  count. This failure is **pre-existing**: the expand affordance requires an explainer,
  contribution context, related groups or interpretation, and the test fixture supplies none of
  those. The removed `patternRelevanceLine` field was also absent from that fixture, so this
  correction cannot have changed the outcome. Confirmed by running the same suite at the baseline
  SHA in a detached worktree, where it fails identically (1 failed, 9 passed). Recorded as an
  unresolved pre-existing test defect, not fixed here (out of scope).
