---
work_id: CLIN-PRIORITY-RESULT-REGEN-1
branch: feature/clin-priority-result-regen-1
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# CLIN-PRIORITY-RESULT-REGEN-1 — Governed Result Regeneration and Trend Supersession

## Objective

Implement the minimum complete governed result-regeneration architecture so that any future code change capable of altering a user’s personalised analysis, clinical findings, prioritisation, interpretation, or clinically meaningful user-facing narrative can make earlier results eligible for refresh without mutating historic records.

This package explicitly includes:

- one persisted user-entered clinical chronology field, `result_date`;
- a canonical backend-owned trend/history selection path;
- result supersession lineage;
- frontend migration away from client-side trend authority.

Once a stale result is refreshed, only the refreshed result may contribute to trend and longitudinal analysis for that original uploaded result.

## Governing product policy

1. Historic results remain immutable and accessible.
2. Any deployed change capable of changing personalised analytical output must advance a governed analysis-policy version.
3. Results created under an earlier analysis-policy version become `stale`, not `incompatible`, where they remain renderable and regenerable.
4. Existing stale-result wording and refresh UX must be reused unless repository evidence proves it cannot represent this policy.
5. Refresh creates a new analysis result from the original stored source data. It must not overwrite the original result.
6. The refreshed result retains the original user-entered **result date**.
7. The result date is the single user-entered clinical chronology date. It may represent:
   - the blood sample date; or
   - where unavailable, the report date.
8. Upload and processing timestamps remain system metadata only and must not be requested from the user.
9. After successful refresh:
   - the stale result remains available for audit/history;
   - the stale result is excluded from trend display and longitudinal calculations;
   - the refreshed result becomes the sole active trend/longitudinal representative for that original uploaded result;
   - the refreshed result occupies the same chronological position using the unchanged result date.
10. Repeated refresh must not create duplicate active trend points. The newest valid refreshed version becomes active and earlier versions remain superseded history.
11. Purely technical changes that cannot alter personalised analytical output must not advance the analysis-policy version.

## Authority boundaries

This package must not:

- change any clinical prioritisation rule;
- change signal activation, thresholds, severity, urgency, tiering, consolidation, lead/co-lead selection, or longitudinal medical rules;
- change the approved historic-result retention principle;
- create a second result-status authority;
- create a frontend-only inference for whether a result is stale;
- invent new user-facing wording unless existing wording is demonstrably insufficient and the package is formally re-scoped;
- delete historic analysis records;
- use upload timestamp or regeneration timestamp for clinical trend placement;
- create multiple user-entered date fields.

The backend must remain the sole authority for:

- analysis-policy version;
- `current`, `stale`, and `incompatible` classification;
- regeneration eligibility;
- supersession lineage;
- active-versus-superseded trend participation.

The frontend must render server-provided state only.

## Required Stage 1A authority preflight

Before implementation, verify and cite the current repository authority paths for:

1. result versioning and stale/incompatible classification;
2. persisted-result compatibility;
3. regeneration eligibility and regeneration execution;
4. historic-result retention and immutable-snapshot policy;
5. analysis result persistence and result-date storage;
6. trend and longitudinal analysis query/selection paths;
7. frontend stale-result banner and refresh action;
8. any existing supersession, lineage, replacement, or active-version fields.

Confirm that no parallel authority already exists for analysis-policy versioning or trend supersession.

If authority is ambiguous, STOP before implementation.

## Required Stage 1B reality check

Confirm the current baseline still exhibits all of the following:

- a pre-`CLIN-PRIORITY-CORE-1` result can be classified `current` while lacking `clinical_concern_set`;
- such a result does not expose the existing refresh option;
- current trend/longitudinal selection does not already exclude superseded result versions;
- no governed general analysis-policy version currently covers all personalised-output changes.

If any item is already fully solved, re-scope or cancel the relevant part rather than implementing duplicate logic.

## Required implementation outcomes

### A. Single user-entered result date

Add one canonical persisted field:

`result_date`

Product meaning:

- normally the date the blood sample was taken;
- where that is unavailable, the date shown on the laboratory report.

Rules:

- this is the only date the user is asked to provide for clinical chronology;
- it must be stored on the analysis record or another single canonical persisted model identified during hardening;
- it must flow through API/DTO/frontend types without creating competing date fields;
- it determines trend and longitudinal placement;
- regeneration must copy it unchanged;
- system timestamps such as upload, creation, completion, and regeneration timestamps remain automatic audit metadata and must not be shown as alternative user-entered clinical dates.

Existing analyses require a bounded migration/backfill policy:

- where the repository already preserves an equivalent user-supplied date in payload or metadata, deterministically backfill from that source;
- where no such source exists, use the existing analysis `created_at` date as a legacy fallback classification only, without representing it as a confirmed blood-sample date;
- record the provenance of the populated date as `user_entered`, `legacy_equivalent_source`, or `legacy_created_at_fallback`;
- do not ask users to enter additional dates during regeneration.

Stage D must verify the least invasive schema and migration path. This schema addition and bounded migration are explicitly authorised by this package and are not a STOP condition unless repository evidence shows destructive or ambiguous data rewriting would be required.

### B. Governed analysis-policy version

Introduce or extend one canonical analysis-policy version that represents the personalised analytical behaviour used to generate a result.

It must cover changes capable of affecting:

- signal outputs;
- clinical findings;
- concern consolidation;
- severity, urgency, tier or prioritisation;
- lead/co-lead/no-forced-lead selection;
- longitudinal interpretation;
- WHY/root-cause output;
- scoring or derived analytical outputs;
- clinically meaningful questionnaire/context interpretation;
- clinically meaningful narrative assembly or presentation policy.

Do not maintain an indefinitely growing list of field-specific stale checks as the primary architecture.

The implementation must preserve existing specialised stale reasons where they remain useful for diagnosis or remediation, but the analysis-policy version must be the broad governing trigger for personalised-output change.

### C. Current-result stamping

Newly generated results must persist the current analysis-policy version through the existing governed persistence path.

The stamp must be deterministic, backend-owned, and available to the result-versioning classifier.

### D. Historic-result classification

A stored result generated under an earlier analysis-policy version must be classified:

- `stale` when still renderable and regenerable;
- `incompatible` only under the existing compatibility rules.

Do not relabel results `incompatible` merely because their personalised analysis is out of date.

The existing missing-`clinical_concern_set` case must be covered by the new policy.

### E. Regeneration behaviour

Regeneration must:

- use the preserved original source data;
- create a new immutable analysis/result record;
- preserve the original user-entered `result_date`;
- record lineage to the result it supersedes;
- leave the prior result intact;
- return the refreshed result as the active version for that original upload/result lineage.

Do not introduce additional user-entered dates.

### F. Backend trend and longitudinal authority

Create one canonical backend-owned trend/history selection path because repository preflight has confirmed that no such authority currently exists and the frontend presently selects and sorts completed analyses itself.

This package explicitly authorises:

- a backend query/service/DTO path that returns trend-eligible analyses;
- lineage-aware exclusion of superseded result versions;
- ordering and placement by `result_date`;
- frontend migration away from `useTrendData.ts` / `trendComparison.ts` as decision authorities.

Trend and longitudinal selection must use only the active result version for each original result lineage.

Required behaviour:

- before refresh, the stale result may remain the only available result but must not be silently represented as current;
- after successful refresh, the stale version is excluded from trend display and longitudinal calculations;
- the refreshed version is included at the unchanged original `result_date`;
- repeated refresh yields one active trend point, not duplicates;
- separate genuinely distinct uploaded results sharing the same result date must not be incorrectly collapsed;
- lineage identity, not date alone, determines replacement.

### G. Frontend behaviour

Reuse the existing stale-result banner, wording, and refresh control.

The frontend must not:

- calculate policy-version mismatch;
- infer supersession;
- decide which result participates in trends;
- use upload or processing dates for trend placement.

## Required evidence and tests

At minimum, add regression coverage for:

1. current-policy result remains `current`;
2. older-policy renderable result becomes `stale`;
3. older-policy result with preserved source data exposes regeneration;
4. incompatible-result behaviour remains unchanged;
5. missing `clinical_concern_set` legacy result is no longer classified `current`;
6. refresh preserves the original `result_date`;
7. refresh creates a new analysis/result identity;
8. original result remains stored and accessible;
9. refreshed result records supersession lineage;
10. stale/superseded result is excluded from trend output;
11. refreshed result appears once in trends at the original result date;
12. repeated refresh still produces only one active trend point;
13. two separate uploads with the same result date remain separate trend observations;
14. existing waist-remediation, completeness-policy, replay-manifest, and compatibility rules remain green;
15. frontend stale-result banner continues to render from backend status only;
16. no clinical-priority, signal, threshold, or concern-construction behaviour changes.

Use canonical existing test modules where available. Stage D must identify exact test paths before hardening completes.

## Migration and existing data

A bounded migration is authorised only for introducing `result_date` and supporting supersession/trend authority.

Requirements:

- no historic analysis payload may be deleted or overwritten;
- lineage should be explicit on newly regenerated results;
- existing non-regenerated analyses may be treated as singleton active lineages;
- deterministic `result_date` backfill must follow the hierarchy defined in Required Outcome A;
- migration must be idempotent, auditable, and reversible;
- any record that cannot be populated under that hierarchy must be reported and left unmodified rather than guessed.

STOP only if the migration would require clinical interpretation, destructive rewriting, or an additional user-entered date.

## STOP conditions

STOP and escalate if:

- current repository has more than one plausible result-versioning authority;
- more than one competing backend trend authority would be created;
- implementing supersession requires deleting or mutating historic results;
- `result_date` cannot be added and populated using the authorised bounded migration/fallback policy without destructive or clinically misleading rewriting;
- regeneration cannot reuse the original stored source data;
- a new user-entered date appears necessary;
- a clinical or product rule must be invented;
- existing wording cannot represent the stale/refresh state and new consumer wording would be required;
- same-date distinct uploads cannot be distinguished without a new identity decision;
- the change requires altering clinical prioritisation, signal activation, thresholds, or longitudinal medical rules;
- test evidence cannot prove one active trend point per original result lineage;
- the work expands beyond the explicitly authorised result-date schema, analysis-policy versioning, regeneration lineage, backend trend selection, and frontend trend rewire.

## Out of scope

- new clinical-priority logic;
- new trend algorithms;
- new medical thresholds;
- questionnaire redesign;
- new consumer copy;
- deletion of historic results;
- estate-wide regeneration;
- manual data repair unrelated to this package;
- changes to raw biomarker interpretation;
- changes to the single user-entered result-date model.

## Completion evidence

Produce:

- implementation and verification report;
- before/after examples for a pre-CLIN-PRIORITY result;
- result-version classification evidence;
- regeneration lineage evidence;
- trend output evidence proving stale replacement without duplicate points;
- changed-file classification;
- regression results;
- explicit confirmation that clinical rules and signal activation are unchanged.

## Hardening instruction

Re-harden work_id: CLIN-PRIORITY-RESULT-REGEN-1 — verify source content and produce evidence checklist

The prior hardening blockers are explicitly resolved as follows:

1. This package authorises adding and persisting the single `result_date` field, with the bounded migration/fallback policy above.
2. This package authorises creation of a new canonical backend trend/history selection path and frontend migration away from client-side trend authority.

Claude must apply the Automation Bus SOP v1.3.1 Stage 2A–2C requirements, including file-and-line citations for every authority path and exact canonical test paths.

Do not execute implementation until hardening status is `HARDENED` and the kernel has issued the active execution token.
