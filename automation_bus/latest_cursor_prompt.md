---
work_id: EIGHT-BLOCK-PROGRAMME-1
branch: work/EIGHT-BLOCK-PROGRAMME-1-comparison-and-roadmap
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# EIGHT-BLOCK-PROGRAMME-1 — Cursor/Claude Comparison and Multi-Sprint Beta-Readiness Programme

## Objective

Create the canonical comparison and programme recommendation paper for HealthIQ AI’s path from current internal-validation state to controlled beta readiness.

This is a documentation-only planning sprint.

Do not change runtime code.
Do not change tests.
Do not change frontend behaviour.
Do not change backend behaviour.
Do not implement any roadmap item.
Do not implement Gemini.
Do not alter existing audits except if adding a one-line cross-reference is explicitly justified.
Do not create branches/forks other than the specified work branch.

The purpose is to compare the Cursor and Claude eight-block estate audits, incorporate the late-document addendum and the new layer-boundary reconciliation ADR, and produce a sequenced multi-sprint programme that avoids reinventing existing work.

---

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull
git status --short
git switch -c work/EIGHT-BLOCK-PROGRAMME-1-comparison-and-roadmap
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## Critical architectural rule

This sprint must use the reconciled layer model from:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
```

The roadmap must be built around this canonical model:

```text
Layer A:
Ingestion, parsing, canonicalisation and factual normalisation.

Layer B:
Deterministic medical intelligence, WHY/root-cause, hierarchy, surfacing decisions, clinician report, biomarker/system interpretation, evidence/counter-evidence, boilerplate/prose asset selection, safety, provenance and traceability.

Layer C:
Presentation and translation only. Layer C renders and communicates governed Layer B outputs. If Gemini is used, it is an optional constrained presentation/translation component inside Layer C, not the analytical engine.
```

Future sprint recommendations must not assign Layer B responsibilities to Layer C, Gemini, the frontend, or presentation code.

---

## Required authoritative inputs

Read these before writing the paper:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_LATE_DOCUMENT_ADDENDUM_2026-06-17.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CURSOR_2026-06-17.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_ESTATE_AUDIT_CLAUDE_2026-06-17.md
docs/strategy/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/architecture/ADR_WP2_layer_b_layer_c_contract_path_b.md
backend/core/contracts/narrative_payload_v1.py
docs/architecture/LAUNCH-CORE-3_result_versioning_replay_and_regeneration_policy.md
docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-16.md
docs/testing/INTERNAL_UAT_RESULTS_PAGE_FULL_AUDIT_6bcbf1de_2026-06-17_r2.md
docs/audit-papers/LAYER-BOUNDARY-RECONCILIATION-1_layer_boundary_reconciliation.md
docs/AUTHORITY_MAP.md
```

Supporting inputs to inspect where relevant:

```text
docs/architecture/RETAIL_EXPLAINER_CONTENT_BOUNDARIES_v1.md
docs/intelligence/DOMAIN_NARRATIVE_CONTRACT_WAVE1.md
docs/intelligence/PRIMARY_CONCERN_AND_RANKED_AMBIGUITY_POLICY_v1.md
docs/frontend/HealthIQ_Final_Results_Journey_Recommendation_Paper_v6.md
docs/testing/HealthIQ_AI_Background_Testing_Operating_Model_v1.md
docs/testing/HealthIQ_AI_Phase_1_Sentinel_Execution_Brief.md
docs/testing/healthiq_sentinel_phase1_implementation_report.md
knowledge_bus/governance/day_one_launch_estate_gate_v1.yaml
backend/ssot/retail_explainer_v1/registry.yaml
backend/ssot/scoring_policy.yaml
```

---

## Required output file

Create:

```text
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
```

Do not overwrite the Cursor audit, Claude audit, r1/r2 layer index, late-document addendum, or ADR.

---

## Required output structure

Use this structure exactly.

```text
# HealthIQ AI — Eight-Block Beta Readiness Comparison and Programme Recommendation

## 1. Executive summary

Provide a CEO-level summary:
- current maturity
- strongest assets
- biggest risks
- what has now been clarified
- why the estate should not be rebuilt from memory
- whether the product is beta-ready
- what the next programme must achieve

## 2. Evidence base

List the exact documents used:
- Cursor audit
- Claude audit
- late-document addendum
- layer architecture authority index r2
- layer-boundary ADR
- Strategic Vision v1.5
- User Health to Systems Map
- UAT R1 and R2
- any other major supporting documents

For each document:
- file path
- authority status
- why it matters
- which blocks it supports

## 3. Corrected canonical layer model

Summarise the reconciled model from ADR-LAYER-BOUNDARY-RECONCILIATION-1.

Must explicitly state:
- Layer B owns WHY/root-cause
- Layer B owns surfacing and suppression
- Layer B owns clinician report
- Layer B owns deterministic boilerplate/prose asset selection
- Layer C is presentation/translation only
- Gemini is optional and constrained, not the analytical engine
- frontend remains render-only

## 4. Cursor vs Claude comparison

Create a structured comparison table.

For each of the eight blocks, compare:
- Cursor assessment
- Claude assessment
- agreement
- disagreement
- GPT/programme interpretation
- evidence confidence
- whether late documents changed the conclusion

## 5. Reconciled eight-block maturity assessment

For each block, provide:
- maturity: NONE / LOW / MEDIUM / HIGH
- evidence confidence
- existing assets
- implementation state
- documentation state
- main gaps
- beta relevance
- Layer B relevance
- Layer C/presentation relevance
- reuse priority

Blocks:
1. Core health systems model
2. Subsystems and depth model
3. Layer B deterministic intelligence, WHY, clinician report and boilerplate prose estate
4. Layer C presentation / translation layer, including constrained Gemini
5. Results page / UX product layer
6. Medical safety, research provenance and governance
7. Auditability, reproducibility and regulatory-grade traceability
8. Phenotype panels, edge-case estate and beta validation gates

## 6. Key conclusions that are now settled

Include at least:
- User Health to Systems Map is the systems taxonomy authority
- Strategic Vision v1.5 §2.3 is strategic north star for layer responsibilities
- ADR-LAYER-BOUNDARY-RECONCILIATION-1 governs future layer vocabulary
- Layer B is the medical intelligence and WHY layer
- Layer C is presentation/translation only
- Gemini is inactive for narrative and should not be activated before Layer B substrate and tests are ready
- not externally beta-ready
- no full estate re-audit is required
- implementation should begin from existing assets, not rebuilt models

## 7. Stale or superseded findings

Identify findings in Cursor or Claude audits that are stale or superseded.

Must include:
- Claude’s “6 HIGH UAT defects unresolved” finding should be updated by the R2 UAT evidence if R2 confirms HIGH issues fixed/downgraded
- any difference in package count if Cursor says 186 and Claude says 187
- any date correction from the R2 UAT audit
- any wording changed by late-document addendum
- any remaining uncertainty that should be checked before implementation

## 8. Reusable asset inventory

Create a reusable asset inventory grouped by:

### Systems and subsystems
- User Health to Systems Map
- scoring policy
- Wave 1 assembler
- compiled health system cards
- packages for thyroid, iron, renal, etc.

### Layer B / WHY / clinician report / prose
- ClinicianReportV1
- NarrativePayloadV1
- root cause assets
- IDL
- retail explainer registry
- pathway explainers
- interpretation entities
- domain narrative contracts

### Layer C / presentation
- Layer boundary ADR
- existing narrative presentation components
- Gemini validator / prohibited actions
- results page components

### Safety / provenance
- Knowledge Bus promotion protocol
- research-to-runtime traceability
- package provenance
- output authority provenance
- lab-range tests
- consumer prose safety

### Auditability
- ReplayManifestV1
- result_versioning
- stale/incompatible banner
- LAUNCH-CORE-3
- replay sentinel packs

### Testing / beta validation
- AB/VR/golden panels
- phenotype fixtures
- Sentinel packs
- suppression tests
- UAT reports

For each asset:
- file path
- what it already gives us
- which future sprint should reuse it
- whether it is authoritative, supporting, runtime, test or research evidence

## 9. Programme principles

Define principles for the roadmap.

Must include:
- no Gemini before Layer B brief/prose/test substrate is ready
- no UX polish before core architecture and hierarchy are stable
- no new systems taxonomy from scratch
- no frontend medical inference
- no fallback parser logic
- no global/default ranges where lab ranges exist
- preserve research provenance
- keep beta framing internal until explicitly approved by the CEO
- every implementation sprint must trace to existing authority
- prefer outcome-based sprint packages, not unnecessary micro-sprints

## 10. Recommended multi-sprint programme

Produce a sequenced programme of approximately 12–20 sprints.

Group them into phases:

### Phase 0 — Immediate governance and evidence consolidation
Purpose: ensure the roadmap starts from correct authorities.

### Phase 1 — Systems and subsystem completion
Purpose: complete the missing launch-core domains and minimum subsystem depth.

### Phase 2 — Layer B substrate expansion
Purpose: complete WHY, clinician report, boilerplate/explainer and prose-selection estate.

### Phase 3 — Safety, provenance and auditability hardening
Purpose: preserve medical credibility and reproducibility.

### Phase 4 — Layer C presentation and constrained Gemini
Purpose: implement presentation/translation only after Layer B is ready.

### Phase 5 — Results page / UX redesign
Purpose: build the consumer experience around the stable architecture.

### Phase 6 — Beta validation and test estate
Purpose: prove behaviour across phenotypes, panels, edge cases and lifestyle contexts.

For each proposed sprint include:
- sprint title
- objective
- block(s) supported
- layer(s) touched
- key inputs
- expected outputs
- dependency order
- risk level
- stop gates
- why it is sequenced here

Important:
- Use `CONTENT`, `BEHAVIOUR` or `MIXED` terminology correctly if referring to future Automation Bus prompts.
- Do not use `DOCS` as a change_type.
- Do not write full implementation prompts for each sprint; this is a programme recommendation.

## 11. Recommended first three sprints

Give a concrete recommendation for the first three sprints only.

For each:
- why it comes first
- what it should produce
- what it must not do
- whether it is docs/content only or implementation
- whether Claude audit / GPT review is required

## 12. Beta-readiness decision gates

Define the major gates before controlled beta.

Include:
- domain coverage gate
- Layer B evidence/prose gate
- Layer C/Gemini gate
- medical safety/provenance gate
- auditability/replay gate
- UX trust gate
- phenotype/edge-case test gate
- security/secrets gate
- CEO/human approval gate

## 13. Risks and dependencies

List:
- major risks
- sequencing dependencies
- where over-fragmentation would hurt
- where bundling would be unsafe
- where documentation must precede code
- where clinical/medical review is needed

## 14. Final recommendation

Conclude with:
- whether to proceed with the programme
- what the first work package should be
- what must not be done next
- what decision the CEO needs to make
```

---

## Important interpretation rules

### Do not overstate beta readiness

The product is not externally beta-ready.

Use language such as:

```text
continued internal validation
controlled internal product validation
future controlled beta readiness
```

Do not imply external users should access the product now.

### Do not treat Layer C as logic

Any sprint involving Layer C must be presentation/translation only.

Layer C must not:

* determine findings
* determine hierarchy
* determine WHY
* determine surfacing
* activate/suppress signals
* inspect raw biomarkers outside Layer B brief
* create new medical claims
* override Layer B

### Do not make Gemini the product brain

Gemini may only be recommended after:

* NarrativePayloadV1/Layer B brief is confirmed sufficient
* boilerplate/prose substrate is available
* output schema exists
* anti-hallucination tests exist
* validator/gate is working
* CEO approves activation path

### Do not bury the boilerplate point

The programme must clearly recognise that HealthIQ’s “wow” experience should come mostly from governed Layer B boilerplate/prose modules selected deterministically by Layer B, not from Gemini improvising long reports.

Layer B must support:

* biomarker-level explainers triggered by result state
* system-level explainers triggered by system state
* pathway explainers
* lifestyle-context explainers
* missing-marker explainers
* counter-evidence explainers
* clinician report sections
* safe consumer wording

Layer C presents these assets; it does not decide them.

---

## Validation requirements

Because this is docs/content only:

```powershell
git diff --stat
git diff --name-only
```

Expected changed file:

```text
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
```

No code files may change.

If `docs/AUTHORITY_MAP.md` is updated to register this paper, explain why. Otherwise leave it unchanged.

---

## Required final report

Return:

```text
- branch name
- files created/updated
- summary of comparison conclusion
- recommended first three sprints
- whether any conclusions changed from Cursor/Claude audits
- whether any stale findings were corrected
- confirmation no code files changed
- validation output
- git status --short
```

Do not merge until GPT architectural review and human approval.

---

## Acceptance criteria

This work is complete only if:

```text
1. The paper uses ADR-LAYER-BOUNDARY-RECONCILIATION-1 as the governing layer model.

2. Cursor and Claude audit findings are compared, not merely pasted.

3. Late-discovered documents are incorporated.

4. Stale findings are clearly identified.

5. The resulting programme is sequenced and dependency-aware.

6. The first three recommended sprints are clear.

7. The roadmap does not assign Layer B responsibilities to Layer C, Gemini or frontend.

8. The programme avoids reinventing systems/subsystems/prose assets already found.

9. The output is useful for CEO-level roadmap decision-making.

10. No runtime code, test code, frontend code or backend code is changed.
```
