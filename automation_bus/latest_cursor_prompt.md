---
work_id: OPS-S1A
branch: feature/ops-s1a-trust-uk-baseline
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# OPS-S1A — Trust and UK Baseline

## Context

This is the first execution phase of **OPS-S1 — Phase 1 Operational Readiness for UK B2C Launch**.

The governing OPS-S1 preflight concluded:

* OPS-S1 is now justified because the launch posture has been explicitly decided
* the correct delivery shape is:

  * **OPS-S1A — Trust and UK baseline**
  * **OPS-S1B — Operational evidence and controls**
* the biggest immediate launch blockers are:

  * trust/claims mismatch with the agreed UK-first posture
  * missing Privacy / Terms / Contact surfaces
  * lack of a minimum credible UK B2C transparency baseline in the launch-facing product

The agreed Phase 1 launch posture is:

* **market:** UK only
* **operating model:** B2C-primary
* **launch user:** self-directed retail user with an already-tested blood panel
* **data residency direction:** UK-hosted by default
* **minimum posture:** UK consumer health-data trust/compliance floor with strict non-diagnostic positioning
* **B2C role:** deliberate wedge / proof engine, not the long-term final model

This sprint is **OPS-S1A only**.

It is **not**:

* OPS-S1B operational evidence/control work
* HIPAA-led or US-first posture work
* enterprise/B2B procurement readiness
* backend reasoning changes
* broad marketing-site redesign
* medical-device positioning
* general legal drafting beyond what is required for launch-truth surfaces

---

## Objective

Bring the launch-facing trust and legal baseline into line with the agreed UK B2C Phase 1 posture so the product no longer makes unsupported, jurisdictionally wrong, or incomplete trust claims at the point of launch.

This sprint must establish:

* UK-appropriate trust/claims alignment on launch-facing surfaces
* real Privacy / Terms / Contact surfaces rather than placeholders
* consistent non-diagnostic positioning where launch-facing trust language requires it
* no mismatch between the product’s declared launch posture and what the user sees publicly
* no drift into broad ops/control work that belongs in OPS-S1B

This sprint is about **launch-truth and trust baseline**, not the full operational evidence stack.

---

## Stage 1C — Trust Baseline Preflight (MANDATORY)

Before editing files, explicitly verify and record:

1. the governing preflight is:

   * `docs/investigations/OPS_S1_PREFLIGHT.md`

2. the launch authority is:

   * `docs/HealthIQ_Phase1_Launch_Posture.md`
   * and any adopted/addendum strategy doc now serving as first-market authority

3. the current repo reality is still:

   * launch-facing UI includes trust/legal claims that are not yet fully aligned with the UK-first launch posture
   * Privacy / Terms / Contact surfaces are missing or placeholder
   * OPS-S1A should address trust/claims surfaces first, before OPS-S1B operational evidence/control artefacts

4. before implementation, Cursor must explicitly verify and record:

   * the exact launch-facing claims currently present
   * which claims are supportable now
   * which claims are risky, premature, or jurisdictionally mismatched
   * where placeholder legal/trust surfaces currently exist
   * what minimum UK B2C trust/legal surfaces are required for a credible launch baseline

5. before implementation, Cursor must explicitly choose and record:

   * the trust/claims posture to apply on the landing and launch-facing pages
   * the exact scope of Privacy / Terms / Contact implementation in this sprint
   * what content will be added as product-facing baseline vs what is deferred to OPS-S1B or later human/legal review

6. this sprint will **not**:

   * prove UK hosting/residency technically
   * deliver DPIA/subprocessor/runbook artefacts
   * redesign backend auth/analysis logic
   * become a broad marketing rewrite
   * make legal claims beyond what the agreed posture and repo reality can support
   * reopen the Phase 1 launch-posture decision

7. if a truthful trust baseline cannot be implemented without broader operational evidence than this sprint allows, STOP and report rather than papering over the gap with vague copy

If any of the above is false:

* STOP
* report precisely
* do not proceed

---

## Scope (strict)

### REQUIRED IN SCOPE

#### 1. Launch-facing trust/claims alignment

Primary likely surfaces:

* `frontend/app/page.tsx`
* `frontend/app/components/layout/Footer.tsx`
* any directly adjacent launch-facing trust/copy component strictly required
* auth screens only if trust-language alignment clearly requires it

You must align the most visible trust and compliance-facing language with the agreed UK B2C launch posture.

This includes reviewing and correcting launch-facing claims such as:

* HIPAA
* bank-level security
* medical-grade security
* diagnostic-sounding language
* overconfident trust/compliance wording
* any other launch-facing claims that are not supportable by the agreed Phase 1 baseline

Requirements:

* landing and other public-facing trust language must no longer contradict the UK-first posture
* the product must not imply a US/HIPAA-led launch posture if that is explicitly not the chosen Phase 1 path
* the product must not make stronger trust/compliance claims than the repo + launch posture can support
* wording should remain commercially credible, but truthful and bounded

This is a key trust-baseline deliverable.

---

#### 2. Privacy / Terms / Contact surfaces

Primary likely surfaces:

* frontend routes/pages for:

  * Privacy
  * Terms
  * Contact
* footer/header links that currently point to placeholders
* any small supporting components needed for those pages

You must replace placeholder legal/support links with real product-facing surfaces appropriate to the agreed Phase 1 launch posture.

Requirements:

* Privacy, Terms, and Contact links must no longer be dead/placeholder links
* each surface must be real, accessible, and coherent with the UK B2C launch posture
* content should provide a credible launch baseline for transparency and user trust
* do not over-engineer these into a legal-platform subsystem

Important:

* this sprint is allowed to create the product-facing baseline surfaces
* it is not required to solve every future legal nuance or enterprise requirement

---

#### 3. Non-diagnostic positioning consistency where launch trust requires it

Primary likely surfaces:

* landing and auth-adjacent copy
* any launch-facing results-entry/CTA language if clearly relevant
* any small trust/disclaimer blocks required by the agreed posture

You must ensure launch-facing wording does not drift into diagnostic or treatment-positioning language inconsistent with the agreed Phase 1 posture.

Requirements:

* do not imply the product is diagnosing, prescribing, or replacing clinicians
* maintain consistency with the already-established product truth that structured interpretation and clinician discussion are distinct
* do not add heavy disclaimers everywhere; apply this in a bounded, product-sensible way

---

#### 4. Bounded support/contact truthfulness

Primary likely surfaces:

* Contact page
* footer/header references
* auth or launch-facing help references if directly relevant

You must give users a truthful minimum support/contact path.

Requirements:

* there must be a real way for a launch user to understand how to contact the company
* do not leave “Contact” as a decorative placeholder
* keep this bounded to product-facing launch truth, not a full support platform

---

#### 5. Preserve existing product hierarchy and launch posture

Primary likely surfaces:

* landing page
* upload/results/account surfaces only if touched for trust/legal reasons

You must preserve:

* deterministic results hierarchy
* narrative as companion layer
* the agreed UK B2C launch posture
* B2C-first wedge framing

This sprint must not accidentally undermine the completed FE work or broaden the product model.

---

#### 6. Targeted regression coverage

Likely surfaces:

* frontend route/component tests
* link/render tests
* small content-presence tests if useful
* targeted e2e assertions only if genuinely needed

You must add/update the minimum regression coverage needed to prove:

* placeholder legal/support links are replaced with real surfaces
* launch-facing claims no longer use the specific risky or misaligned wording selected in Stage 1C
* trust/legal surfaces are reachable from the actual launch-facing UI
* no backend contract or analytical behaviour was changed

Keep this targeted.
Do not turn it into a general content-management or legal-document test suite.

---

### OPTIONAL / BOUNDED IN SCOPE

#### 7. Small trust-language helper/refactor only if needed

If a small bounded helper/component is needed to keep trust-language or footer/legal-link handling coherent, that is acceptable.

Requirements:

* explicit
* bounded
* directly tied to launch-truth surfaces
* not a broad website framework refactor

---

## OUT OF SCOPE (STRICT)

* No OPS-S1B operational evidence/control artefacts
* No DPIA/subprocessor/runbook implementation in this sprint
* No backend reasoning/narrative changes
* No broad marketing-site redesign
* No HIPAA-led or US-first launch posture work
* No enterprise procurement/security questionnaire work
* No medical-device positioning
* No full legal/compliance programme buildout
* No auth-platform rewrite
* No launch-posture re-decision

---

## Implementation constraints

### Truth over impressiveness

If a claim is not supportable under the agreed UK B2C posture, do not keep it just because it sounds strong.

### UK-first posture must be visible

Public-facing trust language must reflect the actual first-market choice.

### Product-facing legal baseline only

This sprint creates user-facing baseline surfaces, not the whole compliance machinery.

### Preserve completed product work

Do not disturb FE-LAUNCH-INTEGRATION, FE-S2, or deterministic result hierarchy without direct trust-baseline need.

### Stay bounded

If the work starts to look like OPS-S1B or a full website rewrite, it is out of scope.

---

## Acceptance criteria

OPS-S1A is complete only if:

1. launch-facing trust/compliance language is materially aligned to the agreed UK B2C Phase 1 posture
2. the key risky or jurisdictionally mismatched claims identified in Stage 1C are removed, qualified, or replaced appropriately
3. Privacy / Terms / Contact are real product-facing surfaces rather than placeholders
4. launch-facing wording is consistent with non-diagnostic positioning where required
5. a truthful minimum support/contact path exists
6. targeted regression coverage proves the trust-baseline changes
7. no OPS-S1B artefact work, backend reasoning changes, or broad redesign scope is introduced

---

## STOP conditions

STOP immediately if:

* the only way to make trust claims truthful is to add operational evidence/control work that clearly belongs in OPS-S1B
* legal/support surfaces cannot be made credible within a bounded sprint
* the work begins drifting into a broad marketing rewrite
* the work begins reintroducing stronger unsupported claims in different wording
* the work begins reopening launch-posture strategy or expanding into enterprise/us posture work

If any STOP condition triggers:

* halt
* report precisely
* do not widen the sprint

---

## Validation / evidence required

Before closure, provide evidence for:

* exact launch-facing claims changed
* exact Privacy / Terms / Contact surfaces added or wired
* exact links/routes updated from placeholders
* exact non-diagnostic/trust-language adjustments made
* confirmation that no backend analytical behaviour changed
* tests added/updated
* files created/modified
* final git state

---

## Execution sequence (SOP aligned)

1. Kernel START
2. Complete Stage 1C Trust Baseline Preflight
3. Align launch-facing trust/claims language
4. Implement/wire real Privacy / Terms / Contact surfaces
5. Apply bounded non-diagnostic/trust consistency fixes
6. Add/update targeted regression coverage
7. Validate locally
8. Kernel FINISH
9. Produce closure report

---

## Output

Provide:

* files created/modified
* trust-claims-alignment summary
* legal/support-surface summary
* non-diagnostic-positioning summary
* regression summary
* kernel finish status
* final git state

---

## Strategic intent

This sprint exists to:

> create the minimum credible UK B2C launch-facing trust and legal baseline for HealthIQ so the product no longer presents unsupported or misaligned trust/compliance signals before first-market launch

Do not expand beyond that.
