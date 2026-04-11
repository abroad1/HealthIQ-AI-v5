---
work_id: OPS-S1B
branch: feature/ops-s1b-operational-evidence-controls
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# OPS-S1B — Operational Evidence and Controls

## Context

This is the second execution phase of **OPS-S1 — Phase 1 Operational Readiness for UK B2C Launch**.

**OPS-S1A** is complete and established the launch-facing trust baseline:

* launch-facing trust/compliance language is now materially aligned to the agreed UK-first B2C posture
* real Privacy / Terms / Contact surfaces now exist
* non-diagnostic positioning is visible where launch trust requires it
* obvious trust-surface mismatches have been removed

The governing OPS-S1 preflight concluded that the correct delivery shape is:

* **OPS-S1A — Trust and UK baseline**
* **OPS-S1B — Operational evidence and controls**

The preflight found that the biggest remaining launch-critical gaps are now:

* no documented in-repo UK hosting / residency evidence
* no in-repo subprocessor / vendor inventory
* no DPIA or equivalent structured privacy-risk review artifact
* no documented data-flow artifact
* no minimum operational runbook / incident / backup / recovery / secrets baseline evidenced for launch
* wedge-metric readiness is important, but should not displace the trust/control baseline needed for launch credibility

This sprint is **OPS-S1B only**.

It is **not**:

* OPS-S1A trust-surface work
* backend reasoning/narrative changes
* broad infrastructure replatforming
* SOC 2 / ISO 27001 certification programme
* HIPAA-led or US-first operational posture
* enterprise/B2B procurement readiness
* broad product analytics implementation

---

## Objective

Create the minimum operational evidence and control artifacts needed to support a credible UK-first B2C launch, aligned with the agreed launch posture and without expanding into enterprise-grade compliance programmes or unrelated infrastructure work.

This sprint must establish:

* documented UK hosting / residency evidence or explicit hosting-position artifact
* subprocessor / vendor inventory for launch-relevant services
* DPIA or equivalent structured privacy-risk review artifact
* clear data-flow documentation for the launch product
* minimum operational control artifacts covering incident / backup / recovery / secrets / access expectations
* a bounded and honest operational baseline for Phase 1

This sprint is about **operational evidence and control baseline**, not certification or broad infra redesign.

---

## Stage 1C — Operational Evidence Preflight (MANDATORY)

Before editing files, explicitly verify and record:

1. the governing preflight is:

   * `docs/investigations/OPS_S1_PREFLIGHT.md`

2. the launch authority is:

   * `docs/HealthIQ_Phase1_Launch_Posture.md`
   * and any adopted/addendum strategy doc now serving as first-market authority

3. OPS-S1A is complete and the current repo reality is still:

   * trust-surface alignment has been completed
   * Privacy / Terms / Contact exist
   * the remaining launch-critical gaps are now operational evidence / controls rather than public-facing trust copy

4. before implementation, Cursor must explicitly verify and record:

   * what hosting / residency evidence is already present in repo, if any
   * what vendor/subprocessor evidence is already present in repo, if any
   * what privacy/compliance docs are already present vs missing
   * what operational control/runbook material is already present vs missing
   * which evidence artifacts are required for a minimum credible UK B2C Phase 1 launch

5. before implementation, Cursor must explicitly choose and record:

   * the exact artifact set to create/update in this sprint
   * the exact scope of operational controls to evidence now vs defer
   * the exact boundary between OPS-S1B baseline artifacts and later certification/enterprise work

6. this sprint will **not**:

   * promise UK hosting if the repo/ops reality cannot evidence it honestly
   * create fake compliance claims unsupported by deployment reality
   * widen into a full security certification programme
   * become a backend or infrastructure rewrite
   * become a full analytics implementation sprint
   * reopen the agreed launch posture

7. if the required evidence cannot be authored truthfully from current repo/known launch reality, STOP and report rather than fabricating operational confidence

If any of the above is false:

* STOP
* report precisely
* do not proceed

---

## Scope (strict)

### REQUIRED IN SCOPE

#### 1. UK hosting / residency evidence artifact

Primary likely surfaces:

* new docs under `docs/ops/` or `docs/compliance/`
* config/environment documentation surfaces
* any existing deployment/config docs that need bounded update

You must create a truthful artifact describing the launch hosting/residency position for Phase 1.

Requirements:

* reflect the agreed **UK-hosted by default** direction only to the extent it can be evidenced honestly
* explicitly distinguish:

  * confirmed deployment/hosting facts
  * chosen launch posture assumptions
  * items still requiring operational provisioning/verification outside repo
* do not overclaim technical guarantees the repo cannot prove

This artifact should make the launch hosting story reviewable and auditable.

---

#### 2. Vendor / subprocessor inventory

Primary likely surfaces:

* new docs under `docs/ops/` or `docs/compliance/`
* supporting references to current vendor/config usage in repo

You must create a bounded launch-relevant vendor/subprocessor inventory.

Requirements:

* include only vendors/services actually relevant to the launch product and its operation
* distinguish roles clearly, e.g.:

  * hosting / database / auth
  * analytics if present
  * email/contact if relevant
  * other launch-relevant infrastructure/services
* identify what each service does in the launch stack
* keep this practical and launch-oriented, not a giant enterprise procurement pack

This is a minimum transparency/governance artifact, not a full legal register.

---

#### 3. DPIA or equivalent privacy-risk review artifact

Primary likely surfaces:

* new doc under `docs/compliance/` or equivalent

You must create a structured privacy-risk review artifact suitable for the agreed UK B2C Phase 1 posture.

Requirements:

* it must be explicit, structured, and launch-oriented
* it must cover the actual launch product model:

  * upload blood results
  * store/process health-related data
  * provide structured interpretation
  * provide downloadable clinician report
* it must identify key risks, mitigations, and open items honestly
* it must not pretend to be a regulator-approved formal instrument if it is an internal artifact

Call it DPIA or equivalent only if that is honest for the artifact being produced.

---

#### 4. Data-flow documentation

Primary likely surfaces:

* new architecture/ops/compliance doc
* bounded updates to existing docs only if strictly required

You must document the launch-relevant data flow clearly enough that privacy/security/ops decisions are reviewable.

Requirements:

* show the main lifecycle of launch-relevant data at a practical level
* include:

  * user input/upload
  * analysis processing
  * persistence/history
  * account/auth relationship where relevant
  * clinician report / downloadable output if relevant
* distinguish code-backed flow from externally provisioned infra assumptions where necessary
* keep the document readable and operationally useful

This does not need to be a perfect enterprise data map, but it must be good enough for Phase 1 launch governance.

---

#### 5. Minimum operational control baseline artifacts

Primary likely surfaces:

* new docs under `docs/ops/`
* bounded updates to existing runbook/checklist docs if present

You must create the minimum operational control artifact set for Phase 1 launch, covering at least the agreed baseline areas where the preflight found no evidence.

Likely topics include:

* incident response baseline
* backup / recovery baseline
* secrets/config handling expectations
* access-control expectations
* launch-day operational checklist or equivalent minimal runbook

Requirements:

* keep these artifacts bounded and practical
* clearly separate:

  * implemented product behaviour
  * operational process expectation
  * open dependencies requiring human/ops completion before launch
* do not overstate maturity
* do not create an enterprise security manual

---

#### 6. Honest boundary and open-items documentation

Across all created artifacts, you must explicitly document what remains outside Phase 1 scope or still requires non-repo completion.

Requirements:

* no false sense of completeness
* open items must be visible
* distinctions between:

  * completed in repo
  * documented requirement
  * operational dependency
    must be explicit

This is critical for trust.

---

#### 7. Targeted regression / validation coverage

Likely surfaces:

* lightweight validation of required docs/routes if applicable
* doc index references if your repo conventions support them
* no heavy test suite required unless existing patterns make it appropriate

You must provide the minimum validation evidence needed to show:

* required artifacts were created
* artifact set is internally coherent with the agreed launch posture
* no backend analytical behaviour changed
* no unsupported trust claims were reintroduced through ops artifacts

Keep this bounded and proportionate.

---

### OPTIONAL / BOUNDED IN SCOPE

#### 8. Minimal wedge-metric governance note only if needed

If a short artifact is needed to state what launch metrics remain to be instrumented later, that is acceptable.

Requirements:

* this must remain a governance note, not a product analytics implementation
* it should clarify what is deferred beyond OPS-S1B
* do not let this consume the sprint

---

## OUT OF SCOPE (STRICT)

* No OPS-S1A trust-surface rewrite
* No backend reasoning/narrative changes
* No broad infra replatforming
* No SOC 2 / ISO 27001 certification programme
* No HIPAA-led or US-first posture work
* No B2B procurement readiness programme
* No full analytics/product-instrumentation implementation
* No launch-posture re-decision
* No pretending that human/legal/ops signoff is fully replaced by documents alone

---

## Implementation constraints

### Evidence must be honest

Only claim what can be supported by repo reality or clearly labeled operational decisions.

### Phase 1 baseline only

This sprint should produce the minimum credible UK B2C operational artifact set, not a mature enterprise compliance programme.

### Open items must stay visible

Do not hide unresolved operational dependencies.

### Product logic untouched

No analytical, reasoning, or results-hierarchy work belongs in this sprint.

### Keep it usable

Artifacts should be useful to humans planning launch, not just written to satisfy process.

---

## Acceptance criteria

OPS-S1B is complete only if:

1. a launch-relevant UK hosting/residency evidence artifact exists
2. a bounded vendor/subprocessor inventory exists
3. a structured privacy-risk review artifact exists
4. launch-relevant data-flow documentation exists
5. minimum operational control baseline artifacts exist for Phase 1
6. open items and operational dependencies are documented honestly
7. no backend reasoning, infra-rewrite, certification-programme, or analytics-implementation scope is introduced

---

## STOP conditions

STOP immediately if:

* the sprint cannot produce truthful operational evidence without pretending facts not in evidence
* required artifacts depend on external unknowns that make the docs misleading
* the work begins drifting into broad infra/security programme buildout
* the work begins substituting documentation for actual unresolved strategic decisions
* the work begins widening into analytics implementation or backend product work

If any STOP condition triggers:

* halt
* report precisely
* do not widen the sprint

---

## Validation / evidence required

Before closure, provide evidence for:

* exact operational artifacts created/updated
* exact hosting/residency position documented
* exact vendor/subprocessor inventory scope
* exact privacy-risk/data-flow artifacts created
* exact operational baseline/runbook artifacts created
* exact open items/dependencies documented
* confirmation that no backend analytical behaviour changed
* files created/modified
* final git state

---

## Execution sequence (SOP aligned)

1. Kernel START
2. Complete Stage 1C Operational Evidence Preflight
3. Create hosting/residency evidence artifact
4. Create vendor/subprocessor inventory
5. Create privacy-risk and data-flow artifacts
6. Create minimum operational control baseline artifacts
7. Add/update bounded validation evidence
8. Validate locally
9. Kernel FINISH
10. Produce closure report

---

## Output

Provide:

* files created/modified
* hosting/residency-evidence summary
* vendor/subprocessor summary
* privacy-risk/data-flow summary
* operational-controls summary
* open-items/dependencies summary
* regression/validation summary
* kernel finish status
* final git state

---

## Strategic intent

This sprint exists to:

> create the minimum credible operational evidence and control baseline needed to support a UK-first B2C HealthIQ launch, without drifting into enterprise certification work, backend changes, or false operational certainty

Do not expand beyond that.
