---
work_id: WEDGE-METRICS-A
branch: feature/wedge-metrics-a-event-contract-governance
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# WEDGE-METRICS-A — Event Contract and Governance

## Context

This is the first execution phase of the wedge-metrics lineage.

The governing preflight concluded:

* wedge-metrics work is justified now
* the correct delivery shape is:

  * **WEDGE-METRICS-A — event contract and governance**
  * **WEDGE-METRICS-B — instrumentation implementation**
* the repo currently has no real product analytics layer
* most wedge metrics are missing or only indirectly inferable
* because this is a UK-first B2C health-data product, instrumentation must not be improvised without first defining the event contract, privacy boundaries, and vendor/collection posture 

The agreed Phase 1 launch posture is:

* UK only
* B2C-primary
* self-directed retail user with an already-tested blood panel
* two B2C user groups:

  * standard retail
  * technical / biohacker
* B2C as deliberate wedge / proof engine
* clinician report as a secondary exposure channel into real clinical conversations

This sprint is **WEDGE-METRICS-A only**.

It is **not**:

* full instrumentation implementation
* full BI/warehouse setup
* experimentation platform buildout
* billing/payment implementation
* backend reasoning changes
* generic logging work outside wedge metrics

---

## Objective

Define the minimum event contract, governance rules, and privacy/collection posture required to measure the UK B2C wedge truthfully and safely, so instrumentation can be implemented in a bounded follow-on sprint.

This sprint must establish:

* named event vocabulary for the launch-critical wedge journey
* clear event semantics for core actions
* data-minimisation rules for event payloads
* a bounded analytics collection posture
* privacy/consent/update implications that must be handled before instrumentation
* explicit classification of which metrics are in-scope now vs deferred

This sprint is about **measurement definition and governance**, not event wiring.

---

## Stage 1C — Event Contract Preflight (MANDATORY)

Before editing files, explicitly verify and record:

1. the governing preflight is:

   * `docs/investigations/WEDGE_METRICS_PREFLIGHT.md`

2. the launch authority is:

   * `docs/HealthIQ_Phase1_Launch_Posture.md`
   * `docs/HealthIQ_AI_Strategic-Vision-and-12-Month-Sprint-Plan_v1.5_FINAL_ADOPTED_First_Market_Addendum.md`
   * any docs now serving as sprint-plan authority for Phase 1 launch

3. the current repo reality is still:

   * no dedicated product analytics SDK/pipeline is present
   * most wedge metrics are missing or only partially inferable
   * event contract and privacy/vendor posture should be defined before instrumentation
   * segment measurement and clinician-report measurement semantics are not yet cleanly defined

4. before implementation, Cursor must explicitly verify and record:

   * the exact product journeys to be covered by the initial wedge event contract
   * the exact metrics that are:

     * measurable now with bounded implementation
     * blocked pending later product/business work
     * definitional only for now
   * the exact current surfaces where future instrumentation is most likely to land

5. before implementation, Cursor must explicitly choose and record:

   * the proposed event vocabulary
   * the proposed payload-minimisation rules
   * the proposed collection posture:

     * first-party only
     * third-party
     * hybrid
   * the exact privacy/consent implications that must be documented before instrumentation

6. this sprint will **not**:

   * wire events into the app
   * add an analytics SDK
   * implement billing or checkout
   * create a warehouse/BI stack
   * invent segment logic that the product does not yet capture
   * widen into backend reasoning or product redesign

7. if a truthful event contract cannot be defined without broader unresolved privacy/business decisions, STOP and report rather than guessing

If any of the above is false:

* STOP
* report precisely
* do not proceed

---

## Scope (strict)

### REQUIRED IN SCOPE

#### 1. Define the Phase 1 wedge event vocabulary

Primary likely surfaces:

* new docs under `docs/ops/` or `docs/product/`
* possibly a small shared schema doc location if repo conventions support it

You must define the named events for the minimum wedge journey.

At minimum, the contract should address events such as:

* registration completion
* login success
* upload start
* upload completion / parse success
* analysis start
* analysis success / failure
* results viewed
* clinician report viewed
* clinician report exported / shared / downloaded, with explicit semantics
* historical result reopened
* repeat upload / repeat panel behaviour, if eventable directly

Requirements:

* event names must be explicit and consistent
* event meaning must be clear
* avoid ambiguous overlap between similar actions
* do not define a giant future-proof taxonomy; keep it launch-bounded

---

#### 2. Define event semantics for ambiguous product actions

Primary likely surfaces:

* the same contract/governance docs
* possibly a companion glossary section

The preflight identified specific ambiguity around things like clinician-report “download” because the current product has view/export/share behaviours rather than one clearly defined download path.

You must resolve these semantics for the launch wedge.

Requirements:

* distinguish clearly between:

  * report viewed
  * result export/download
  * share action
  * reopened saved result
* do not label an event in a way the current product does not actually support
* if an important business metric cannot yet be represented honestly, mark it as deferred or proxy-only

---

#### 3. Define payload minimisation and privacy rules

Primary likely surfaces:

* governance docs
* possibly cross-reference to OPS docs/privacy surfaces

You must define what event payloads are allowed to contain for Phase 1.

Requirements:

* do not include raw biomarker values in product analytics payloads
* do not include unnecessary health content in event payloads
* use the minimum identifiers and metadata needed for wedge measurement
* clearly state prohibited payload content
* if user segmentation is to be measured later, document how that should be handled or deferred

This is critical because HealthIQ is handling health-related data under a UK B2C posture.

---

#### 4. Define analytics collection posture

Primary likely surfaces:

* governance doc(s)
* cross-reference to OPS-S1 docs if needed

You must choose and document the collection posture for the next sprint to build against.

Examples:

* first-party only event collection
* privacy-reviewed third-party collection
* hybrid with strict boundaries

Requirements:

* the choice must be explicit
* it must match the Phase 1 trust/compliance posture
* if vendor choice is still open, document the permitted boundary instead of pretending it is decided
* do not let this sprint drift into actual vendor integration

---

#### 5. Define privacy / consent / policy implications for instrumentation

Primary likely surfaces:

* governance doc(s)
* bounded updates or references to existing OPS docs/privacy surfaces if needed

You must document what has to be true before instrumentation is turned on.

Requirements:

* identify whether privacy notice updates are required
* identify whether analytics consent is required or must be reviewed
* identify whether vendor/subprocessor inventory updates would be required for third-party analytics
* distinguish:

  * can be done now
  * must be reviewed before implementation
  * deferred

This sprint should make the next implementation sprint safer.

---

#### 6. Classify Phase 1 metrics as now / later / proxy

You must explicitly classify the key wedge metrics.

At minimum address:

* paid conversion
* repeat upload / repeat panel behaviour
* retention / return usage
* clinician report usage
* clinician carry-through / discussion with clinician
* segment differences
* trust/usefulness signals
* enterprise-relevant proof points

Requirements:

* identify which are measurable in the next sprint
* which require a proxy
* which are blocked pending later product/business work
* do not pretend all desired metrics are ready now

---

#### 7. Produce a bounded instrumentation handoff for WEDGE-METRICS-B

You must leave a clear handoff for the next sprint.

Requirements:

* likely touched surfaces
* event names to wire
* payload rules
* excluded fields
* privacy prerequisites
* unresolved open items

This should make WEDGE-METRICS-B straightforward to author.

---

#### 8. Targeted validation evidence

Likely surfaces:

* lightweight tests if repo conventions support doc/schema validation
* otherwise bounded evidence through artifact set and internal consistency

You must provide the minimum validation evidence needed to show:

* required artifact(s) were created
* event vocabulary is internally coherent
* privacy boundaries are explicit
* no backend analytical behaviour changed

Keep this bounded and proportionate.

---

### OPTIONAL / BOUNDED IN SCOPE

#### 9. Minimal machine-readable event schema only if truly useful

If a very small machine-readable event schema artifact would clearly help the follow-on sprint, that is acceptable.

Requirements:

* bounded
* launch-only
* must match the human-readable governance doc
* do not build a full analytics platform contract prematurely

---

## OUT OF SCOPE (STRICT)

* No event wiring or analytics SDK integration
* No full BI/warehouse programme
* No experimentation framework
* No payment/billing implementation
* No backend reasoning changes
* No broad product analytics redesign
* No reopening launch posture
* No fake precision on user segmentation or clinician carry-through

---

## Implementation constraints

### Define only what you can defend

If an event or metric cannot be described truthfully from current product reality, defer it or mark it proxy-only.

### Privacy first

This is a health-data product. Event payloads and collection posture must stay minimal and defensible.

### Launch-bounded

Do not create a giant taxonomy for imagined future products.

### Leave implementation-ready guidance

This sprint should reduce ambiguity for WEDGE-METRICS-B, not just produce abstract notes.

### Product behaviour untouched

No application logic or instrumentation should be added in this sprint.

---

## Acceptance criteria

WEDGE-METRICS-A is complete only if:

1. a bounded Phase 1 wedge event vocabulary is defined
2. ambiguous business/product actions are given explicit event semantics
3. payload minimisation and prohibited data rules are documented
4. the analytics collection posture is explicitly defined or bounded
5. privacy/consent/policy prerequisites for instrumentation are documented
6. key wedge metrics are classified as now / proxy / later honestly
7. a clear handoff exists for WEDGE-METRICS-B without any actual instrumentation being introduced

---

## STOP conditions

STOP immediately if:

* event definitions require unresolved strategy decisions beyond the agreed launch posture
* privacy/consent implications make any current event contract misleading
* the work begins drifting into instrumentation implementation
* the work begins inventing segment logic or paid-conversion logic the current product does not support
* the only way to complete the artifact is to overclaim metric readiness

If any STOP condition triggers:

* halt
* report precisely
* do not widen the sprint

---

## Validation / evidence required

Before closure, provide evidence for:

* exact artifact(s) created
* exact event vocabulary defined
* exact ambiguous action semantics resolved
* exact payload minimisation rules defined
* exact collection posture chosen or bounded
* exact now / proxy / later metric classification
* exact handoff for WEDGE-METRICS-B
* confirmation that no application logic changed
* final git state

---

## Execution sequence (SOP aligned)

1. Kernel START
2. Complete Stage 1C Event Contract Preflight
3. Define wedge event vocabulary
4. Define event semantics for ambiguous actions
5. Define payload/privacy/collection rules
6. Classify metrics as now / proxy / later
7. Produce WEDGE-METRICS-B handoff
8. Add/update bounded validation evidence
9. Kernel FINISH
10. Produce closure report

---

## Output

Provide:

* files created/modified
* event-vocabulary summary
* event-semantics summary
* payload/privacy summary
* collection-posture summary
* metric-classification summary
* WEDGE-METRICS-B handoff summary
* validation summary
* kernel finish status
* final git state

---

## Strategic intent

This sprint exists to:

> define the minimum trustworthy event contract and measurement governance needed to make the UK B2C launch wedge measurable, without prematurely implementing analytics or compromising the product’s privacy and trust posture

Do not expand beyond that.
