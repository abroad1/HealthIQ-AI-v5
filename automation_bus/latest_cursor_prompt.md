---
work_id: WEDGE-METRICS-B
branch: feature/wedge-metrics-b-instrumentation-implementation
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# WEDGE-METRICS-B — Instrumentation Implementation

## Context

This is the second execution phase of the wedge-metrics lineage.

**WEDGE-METRICS-A** is complete and established:

* a bounded Phase 1 wedge event vocabulary
* explicit semantics for ambiguous actions
* payload minimisation rules
* a bounded collection posture
* privacy/consent/policy prerequisites for instrumentation
* honest classification of metrics as now / proxy / later
* a clear implementation handoff for the next sprint 

The governing preflight and contract work concluded that HealthIQ should now instrument the UK B2C wedge in a bounded way so the launch can be measured as a deliberate proof engine, not a waiting room.

This sprint is **WEDGE-METRICS-B only**.

It is **not**:

* BI/warehouse buildout
* experimentation platform work
* payment/billing implementation
* backend reasoning changes
* generic logging expansion outside the agreed wedge events
* fabricated segment logic
* fabricated clinician carry-through logic

---

## Objective

Implement the bounded launch instrumentation defined in WEDGE-METRICS-A so the core UK B2C wedge journey becomes measurable, while preserving privacy constraints and avoiding any drift into broad analytics infrastructure.

This sprint must establish:

* actual event wiring for the agreed launch-critical wedge events
* bounded payloads consistent with the governance contract
* a concrete collection path that matches the agreed collection posture
* truthful implementation of measurable-now metrics
* no fake implementation of deferred metrics

This sprint is about **event implementation**, not broad analytics architecture.

---

## Stage 1C — Instrumentation Preflight (MANDATORY)

Before editing files, explicitly verify and record:

1. the governing preflight is:

   * `docs/investigations/WEDGE_METRICS_PREFLIGHT.md`

2. the governing contract is:

   * `docs/product/WEDGE_EVENT_CONTRACT_AND_GOVERNANCE_PHASE1.md`
   * `docs/product/wedge_events_phase1.manifest.json`

3. the current repo reality is still:

   * no dedicated product analytics implementation is currently present
   * WEDGE-METRICS-A defined the event contract and governance boundaries
   * instrumentation must follow that contract exactly
   * deferred metrics such as paid conversion, segment split, and clinician carry-through are still not to be fabricated now

4. before implementation, Cursor must explicitly verify and record:

   * the exact agreed events to wire in this sprint
   * the exact current collection posture to implement against
   * the exact product surfaces where instrumentation will be added
   * whether any first-party endpoint or collection utility already exists and can be reused truthfully
   * whether any privacy/notice prerequisites from WEDGE-METRICS-A must be satisfied or documented before event emission is enabled

5. before implementation, Cursor must explicitly choose and record:

   * the concrete implementation pattern for event emission
   * the exact event payload fields per event, constrained by the contract
   * the exact handling of client-only versus server-truth events
   * the exact events that will remain deferred in this sprint

6. this sprint will **not**:

   * introduce raw biomarker values or detailed health payloads into analytics events
   * implement paid conversion tracking without real billing/product support
   * invent a standard-retail vs biohacker segment field if the product does not already capture it
   * label JSON export as clinician report download
   * widen into broad warehouse / dashboard / BI work
   * widen into experimentation, A/B testing, or pricing analytics

7. if truthful instrumentation cannot be implemented without violating the contract or privacy posture, STOP and report rather than improvising

If any of the above is false:

* STOP
* report precisely
* do not proceed

---

## Scope (strict)

### REQUIRED IN SCOPE

#### 1. Implement the agreed Phase 1 wedge event set

Primary likely surfaces:

* `frontend/app/state/authStore.ts`
* `frontend/app/(auth)/login/page.tsx`
* `frontend/app/(auth)/register/page.tsx`
* `frontend/app/(app)/upload/page.tsx`
* `frontend/app/state/analysisStore.ts`
* `frontend/app/(app)/results/page.tsx`
* `frontend/app/(app)/analysis/[id]/page.tsx`
* any small shared analytics utility/module strictly required
* optional minimal backend endpoint only if the chosen collection posture requires first-party event receipt

You must implement the measurable-now event set defined in WEDGE-METRICS-A.

At minimum, this should cover the bounded agreed events such as:

* `wedge_auth_register_completed`
* `wedge_auth_register_failed`
* `wedge_auth_login_success`
* `wedge_auth_login_failed`
* `wedge_upload_started`
* `wedge_upload_parse_completed`
* `wedge_upload_parse_failed`
* `wedge_questionnaire_submitted`
* `wedge_analysis_started`
* `wedge_analysis_completed`
* `wedge_analysis_failed`
* `wedge_results_viewed`
* `wedge_clinician_report_viewed`
* `wedge_results_export_json_clicked`
* `wedge_results_share_link_clicked`
* `wedge_analysis_reopened_from_history`

Requirements:

* implementation must match the contract naming exactly unless a justified correction is required
* do not add speculative extra events
* if a specific event cannot be emitted truthfully from current product behaviour, document and defer it rather than faking it

---

#### 2. Respect event semantics exactly

Primary likely surfaces:

* instrumentation utility and event call sites
* results page / report interactions
* history/reopen flow

You must preserve the semantics established in WEDGE-METRICS-A.

Critical requirements:

* **do not** label JSON export as clinician report download
* **do not** collapse view/export/share into one vague clinician-report event
* if `wedge_results_viewed` uses an `entry` property, implement only the values defined by the contract
* if repeat upload remains proxy/server-side rather than evented directly, do not force an event-based version now

The event vocabulary must remain trustworthy.

---

#### 3. Implement bounded payload minimisation

Primary likely surfaces:

* shared analytics/event utility
* event call sites
* optional first-party event receipt path if needed

You must ensure payloads follow the minimisation rules from WEDGE-METRICS-A.

Requirements:

* no raw biomarker values
* no questionnaire answers
* no clinician-report narrative text
* no JWTs/tokens
* no unnecessary health detail
* only the minimum identifiers/metadata allowed by the contract

If a field is not clearly allowed, leave it out.

---

#### 4. Implement the agreed collection posture

Primary likely surfaces:

* shared analytics utility
* env/config surfaces
* optional backend or API path if first-party collection is chosen
* any docs/config updates strictly required to reflect the implementation

You must implement instrumentation in a way that matches the agreed collection posture from WEDGE-METRICS-A.

Requirements:

* if the posture is first-party, implement first-party only
* if the posture allows a bounded third-party path and it is actually chosen now, it must remain within the approved privacy/vendor boundaries
* if vendor choice was still open, do not smuggle in a new vendor without explicit support from the contract/governance docs
* implementation must remain reviewable and bounded

---

#### 5. Preserve explicit deferrals

You must keep the deferred metrics deferred unless the repo reality has changed and the contract is amended.

At minimum, preserve as deferred or proxy-only:

* paid conversion without billing/product support
* standard retail vs biohacker segment split without a real captured field
* clinician carry-through / “discussed with clinician”
* trust/usefulness survey metrics unless a specific bounded capture mechanism is explicitly added and justified

Requirements:

* no false completeness
* no hidden product-model changes just to satisfy analytics ambition

---

#### 6. Add bounded documentation / implementation notes

Likely surfaces:

* docs/product/
* docs/ops/ if needed
* small implementation note or README update if current repo conventions support it

You must update the relevant docs so the implemented instrumentation remains aligned with the contract.

Requirements:

* note which events are now live
* note which remain deferred
* note any implementation-specific decisions needed for operation or debugging
* keep this bounded; do not create a giant analytics handbook

---

#### 7. Targeted regression / validation coverage

Likely surfaces:

* frontend tests for event emission utilities
* integration tests for key flows
* minimal backend tests only if a first-party endpoint is added
* no broad analytics platform test suite

You must add/update the minimum regression coverage needed to prove:

* agreed events fire from the intended surfaces
* deferred events are not misrepresented as live
* JSON export is not labelled as clinician report download
* payload minimisation rules are respected in implementation
* no backend analytical behaviour changed

Keep this targeted and proportionate.

---

### OPTIONAL / BOUNDED IN SCOPE

#### 8. Minimal first-party event receipt path only if truly required

If the chosen collection posture requires a small first-party event receipt path, that is acceptable.

Requirements:

* bounded
* minimal schema
* no broad telemetry platform
* no drift into operational warehouse work

#### 9. Minimal debug/verification tooling only if needed

If a tiny bounded way to verify instrumentation in non-production environments is needed, that is acceptable.

Requirements:

* bounded
* no developer-noise leakage into user-facing product
* not a full analytics console

---

## OUT OF SCOPE (STRICT)

* No BI/warehouse platform
* No experimentation framework
* No payment/billing implementation
* No fabricated paid-conversion event
* No fabricated user-segment measurement
* No fabricated clinician carry-through measurement
* No backend reasoning changes
* No broad logging expansion unrelated to the wedge metrics
* No launch-posture re-decision

---

## Implementation constraints

### Contract first

The event contract from WEDGE-METRICS-A is authoritative.

### Privacy and minimisation are non-negotiable

This is a UK B2C health-data product. Event payloads must stay narrow.

### Measure only what is real

If the product does not support it yet, defer it.

### Keep the scope launch-bounded

This sprint is to measure the launch wedge, not to build a company-wide analytics platform.

### Product behaviour should not change beyond instrumentation

Do not alter analytical logic, truth hierarchy, or clinician-report semantics.

---

## Acceptance criteria

WEDGE-METRICS-B is complete only if:

1. the agreed measurable-now wedge events are actually instrumented
2. event names and semantics match the WEDGE-METRICS-A contract
3. payloads respect the documented minimisation rules
4. implementation matches the agreed collection posture
5. deferred metrics remain explicitly deferred and are not faked in code
6. bounded docs/implementation notes are updated to reflect what is now live
7. targeted regression coverage proves the implementation without introducing broader analytics scope

---

## STOP conditions

STOP immediately if:

* implementation requires deviating from the event contract without explicit amendment
* collection posture cannot be implemented without introducing unresolved privacy/vendor risk
* the only way to show progress is to fake blocked metrics
* the work begins drifting into warehouse/BI/experimentation platform buildout
* the work begins altering product semantics just to produce analytics events

If any STOP condition triggers:

* halt
* report precisely
* do not widen the sprint

---

## Validation / evidence required

Before closure, provide evidence for:

* exact events implemented
* exact surfaces instrumented
* exact payload fields per event or event family
* exact collection path used
* exact deferred metrics preserved
* exact docs/notes updated
* exact tests added/updated
* confirmation that no backend analytical behaviour changed
* final git state

---

## Execution sequence (SOP aligned)

1. Kernel START
2. Complete Stage 1C Instrumentation Preflight
3. Implement the agreed measurable-now event set
4. Enforce payload minimisation and event semantics
5. Implement the agreed collection posture
6. Update bounded docs/implementation notes
7. Add/update targeted regression coverage
8. Validate locally
9. Kernel FINISH
10. Produce closure report

---

## Output

Provide:

* files created/modified
* implemented-events summary
* instrumented-surfaces summary
* payload/collection summary
* deferred-metrics summary
* docs/notes summary
* regression summary
* kernel finish status
* final git state

---

## Strategic intent

This sprint exists to:

> make the UK B2C launch wedge measurably real by implementing the bounded event instrumentation defined in WEDGE-METRICS-A, without compromising privacy, overclaiming metric readiness, or expanding into a broad analytics platform

Do not expand beyond that.
