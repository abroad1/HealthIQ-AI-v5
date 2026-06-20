---
work_id: P1-1
branch: work/P1-1-launch-core-domain-build-materials-map
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: CONTENT
---

# P1-1 — Launch-Core Domain Build-Materials Map

## Objective

Create the first implementation-readiness map for the three missing launch-core domains in the HealthIQ AI beta-readiness programme:

```text
1. Blood / iron / oxygen
2. Thyroid / energy regulation
3. Kidney function
```

This sprint is discovery and mapping only.

It must identify what already exists in the repository and what still needs to be built before any runtime implementation sprint begins.

The output must enable the team to decide which missing launch-core domain should be implemented first in P1-2, based on evidence, readiness, safety, provenance and testability.

---

## Critical scope rule

This is not an implementation sprint.

Do not change runtime code.
Do not change backend code.
Do not change frontend code.
Do not change tests.
Do not change parser logic.
Do not change scoring logic.
Do not change Knowledge Bus packages.
Do not promote Pass 3 material.
Do not activate or suppress signals.
Do not alter reference ranges.
Do not touch Gemini.
Do not touch Layer C presentation logic.
Do not create new clinical interpretation logic.
Do not infer missing assets from memory.

This sprint creates a map only.

---

## Branch and state checks

Start from `main`.

```powershell
git switch main
git pull
git status --short
git switch -c work/P1-1-launch-core-domain-build-materials-map
```

Do not proceed if the working tree is dirty.

Confirm the Automation Bus active work package/state file if required by SOP.

---

## First authority document

Read this first:

```text
docs/strategy/beta_readiness/HEALTHIQ_AI_BETA_READINESS_DEFINITIVE_STRATEGY_FINAL_2026-06-20.md
```

This is the authoritative beta-readiness build strategy baseline.

P1-1 must follow its programme sequencing, layer model, delivery principles, and beta-readiness constraints.

---

## Additional authority and reference documents

Read these before writing the map:

```text
docs/architecture/ADR-LAYER-BOUNDARY-RECONCILIATION-1.md
docs/strategy/eight_block_beta_readiness/EIGHT_BLOCK_BETA_READINESS_COMPARISON_AND_PROGRAMME_RECOMMENDATION_2026-06-18.md
docs/strategy/LAYER_ARCHITECTURE_AUTHORITY_INDEX_2026-06-17_r2.md
docs/architecture/User Health to Systems Map_FINAL.md
docs/AUTHORITY_MAP.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Then inspect relevant supporting material as needed, including but not limited to:

```text
backend/ssot/scoring_policy.yaml
backend/core/analytics/domain_score_assembler.py
backend/core/analytics/wave1_subsystem_evidence.py
backend/core/contracts/narrative_payload_v1.py
backend/core/analytics/report_compiler_v1.py
backend/core/analytics/root_cause_compiler_v1.py
backend/ssot/retail_explainer_v1/registry.yaml
knowledge_bus/
knowledge_bus/compiled/
knowledge_bus/pathway_explainers_v1/
backend/tests/
docs/testing/
docs/intelligence/
docs/architecture/
```

If a listed path does not exist, record that honestly in the output.

Do not fabricate evidence.

---

## Required output file

Create:

```text
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
```

This file is the primary deliverable.

Do not update the final strategy document.

Do not update `AUTHORITY_MAP.md`.

---

## Required report structure

Use this structure exactly.

````markdown
# P1-1 — Launch-Core Domain Build-Materials Map

## 1. Executive summary

Briefly state:
- what was mapped;
- whether each missing domain appears implementation-ready;
- which domain looks safest to implement first;
- the main blockers/carry-forwards;
- whether any evidence was missing or ambiguous.

## 2. Scope and non-goals

State that this sprint maps build materials only.

Confirm explicitly:
- no runtime code changed;
- no tests changed;
- no frontend changed;
- no parser/scoring/report/Gemini logic changed;
- no signals activated;
- no packages promoted.

## 3. Authority documents used

List each authority document read and how it informed the mapping.

Must include:
- final definitive strategy baseline;
- Layer Boundary Reconciliation ADR;
- programme recommendation paper;
- layer authority index r2;
- User Health to Systems Map;
- scoring policy if inspected;
- build deliverable register.

## 4. Domain readiness summary table

Create one table comparing:

| Domain | Current implementation status | Package/spec evidence | Biomarker coverage clarity | Signal safety clarity | Subsystem readiness | Prose/explainer readiness | Test readiness | Overall readiness | Recommended sequencing |
|---|---|---|---|---|---|---|---|---|---|

Domains:
- Blood / iron / oxygen
- Thyroid / energy regulation
- Kidney function

Use ratings:
- Strong
- Partial
- Weak
- Unknown

Do not overstate readiness.

## 5. Blood / iron / oxygen build-materials map

Include:

### 5.1 Existing packages and research material
- Knowledge Bus packages found
- Pass 3 / investigation-spec references found
- compiled card/evidence material found
- pathway explainer material found

### 5.2 Biomarker scope
Map candidate biomarkers, including where found.

Likely examples to check:
- haemoglobin
- haematocrit
- red blood cell count
- MCV
- MCH
- MCHC
- RDW
- ferritin
- serum iron
- transferrin
- transferrin saturation
- TIBC/UIBC if present
- B12 / folate only if relevant to oxygen/blood interpretation and supported by existing assets

Only include markers supported by repo evidence.

### 5.3 Signal and interpretation status
For each relevant signal/pattern found:
- active / inactive / blocked / unknown
- source path
- safety notes
- whether medical review appears required before runtime use

### 5.4 Subsystem candidates
Identify possible subsystem groupings from existing assets only.

Possible examples:
- oxygen carrying capacity
- iron storage
- iron transport
- red-cell indices
- nutrient-linked red cell production

Do not invent subsystem names if no support exists.

### 5.5 Prose, explainer and clinician-report assets
Map existing:
- retail explainer entries
- pathway explainers
- clinician report sections
- narrative payload support
- missing-marker/counter-evidence wording if present

### 5.6 Tests and fixtures
Map any relevant:
- unit tests
- fixtures
- phenotype panels
- golden panels
- Sentinel packs
- UAT evidence

### 5.7 Gaps and carry-forwards
List what is missing before implementation.

### 5.8 Implementation-readiness judgement
State whether this domain should be considered a candidate for P1-2 and why.

## 6. Thyroid / energy regulation build-materials map

Use the same subsection pattern as Section 5.

Check carefully for:
- TSH
- free T4
- free T3
- thyroid antibody markers if present
- context-dependent thyroid patterns
- FT3 low constraints
- medical review outcomes
- blocked/gated thyroid signals

Do not casually recommend activating context-dependent thyroid signals.

## 7. Kidney function build-materials map

Use the same subsection pattern as Section 5.

Check carefully for:
- creatinine
- eGFR
- urea
- electrolytes where relevant
- albumin/creatinine ratio only if present
- renal filtration / kidney function assets
- age/context caveats
- non-diagnostic safety wording

Do not create diagnostic CKD language unless already governed and safe.

## 8. Cross-domain findings

Identify:
- shared assets;
- shared gaps;
- common missing test patterns;
- common missing prose/explainer needs;
- cross-domain dependency risks;
- potential domain interaction issues.

## 9. Recommended first implementation domain for P1-2

Recommend one of:

```text
Blood / iron / oxygen
Thyroid / energy regulation
Kidney function
````

Base the recommendation only on:

* asset readiness;
* package/spec support;
* biomarker clarity;
* signal safety;
* testability;
* prose/explainer availability;
* implementation risk;
* need for clinical review.

If the evidence does not support selecting a domain yet, say so and recommend the smallest additional mapping/hygiene step required.

## 10. Recommended P1-2 scope

If a domain is recommended, propose a safe P1-2 scope.

Include:

* what P1-2 should implement;
* what it must not implement;
* STOP gates;
* likely `change_type`;
* likely `risk_level`;
* required audit/review path.

## 11. Carry-forwards for later sprints

Group carry-forwards by:

### P1 domain implementation

* items to resolve during P1-2/P1-3/P1-4

### P2 Layer B prose/explainer substrate

* prose/explainer gaps to feed into P2-1

### P3 safety/provenance/auditability

* provenance/test/safety gaps to feed into Phase 3

### P5 UX/results page

* display/UX implications to defer until Layer B outputs are stable

## 12. Final recommendation

State:

* whether P1-2 can safely proceed;
* which domain should go first;
* whether P2-1 should run before, after, or in parallel;
* what the next prompt should be.

````

---

## Mapping rules

### Evidence discipline

Every mapped item must include a source path.

Acceptable evidence examples:

```text
backend/...
knowledge_bus/...
docs/...
architecture/...
tests/...
````

Do not rely on memory.

Do not infer that an asset exists because the product ought to have it.

If there is ambiguity, mark it as ambiguous.

### Package count discipline

The final strategy records approximately 186–187 Knowledge Bus packages, with exact count to be verified by P1-1.

If counting packages, report:

* command used;
* count found;
* whether it matches or explains the 186/187 discrepancy.

Do not treat the count discrepancy as a blocker unless it affects the missing-domain map.

### Layer discipline

All domain interpretation belongs to Layer B.

Do not propose:

* Layer C medical reasoning;
* frontend interpretation;
* Gemini compensation for missing Layer B assets;
* runtime reading of raw Pass 3 material.

### Clinical safety discipline

For thyroid, androgen-adjacent, DHEA-S-adjacent, renal, anaemia, iron or oxygen-related signals:

* identify safety/caution flags;
* do not recommend activation without source support;
* record medical review dependencies where present or likely required.

### Lab-range discipline

Record whether domain implementation appears dependent on lab-provided reference ranges.

Do not recommend global/default ranges where lab ranges exist.

---

## Build programme register requirement

At closure, update:

```text
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Append a short entry for P1-1 using this format:

```markdown
## P1-1 — Launch-core domain build-materials map

**Status:** Complete / Partial / Blocked  
**Date closed:** <YYYY-MM-DD>  
**Programme block(s):** Block 1 Core health systems model; Block 2 Subsystems and depth model; Block 3 Layer B intelligence/prose substrate  

### Delivered / ticked off
- <what this sprint completed against the beta-readiness programme>
- <major mapping decision or readiness outcome>

### Carry-forwards
- <what still needs to be done later>
- <known gaps exposed by this sprint>

### Blockers / risks
- <only material blockers or risks that affect future work>

### Recommended next sprint
- <next work package recommendation>
```

Keep the register entry short.

Do not list every file touched.

Do not duplicate the full P1-1 report.

---

## Expected changed files

Expected:

```text
docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md
docs/sprints/beta_readiness/BUILD_DELIVERABLE_REGISTER.md
```

Bus files may also change as part of SOP lifecycle.

No other files should be changed.

If another documentation file must be changed, explain why before doing it if the workflow allows; otherwise record it in the final report.

---

## Validation

Run:

```powershell
git diff --stat
git diff --name-only
git status --short
```

Confirm only expected documentation/governance files changed.

No tests are required because this is documentation/mapping only.

If any code/test/frontend/backend/runtime files changed, stop and report failure.

---

## Required final report

Return:

```text
- branch name
- primary report path
- build register updated: yes/no
- high-level readiness judgement for each domain
- recommended first implementation domain for P1-2
- main carry-forwards
- blockers/risks
- confirmation no runtime/code/test/frontend/backend files changed
- validation output
- git status --short
```

Do not merge until GPT architectural review and human approval.

---

## Acceptance criteria

This work is complete only if:

```text
1. The P1-1 map exists at:
   docs/sprints/beta_readiness/P1-1_launch_core_domain_build_materials_map.md

2. The map covers all three missing launch-core domains:
   - blood / iron / oxygen
   - thyroid / energy regulation
   - kidney function

3. Each domain has evidence-backed mapping of:
   - packages/research material
   - biomarker scope
   - signal/interpretation status
   - subsystem candidates
   - prose/explainer assets
   - tests/fixtures
   - gaps/carry-forwards
   - implementation-readiness judgement

4. The report recommends a first implementation domain for P1-2, or explains why no safe recommendation can yet be made.

5. The report does not invent missing assets or infer from memory.

6. The report does not recommend Gemini, frontend inference, fallback parsing, global/default range substitution, or Layer C medical reasoning.

7. The build deliverable register is updated with a short P1-1 entry.

8. No runtime code, backend code, frontend code, parser logic, scoring logic, report logic, tests, Knowledge Bus packages, Pass 3 promotion artefacts, Gemini files or Layer C runtime files are changed.
```
