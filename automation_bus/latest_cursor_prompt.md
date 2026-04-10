---
work_id: FE-LAUNCH-INTEGRATION-B
branch: feature/fe-launch-integration-b-polish
risk_level: STANDARD
execution_model: TWO_PHASE_START_FINISH
change_type: MIXED
---

# FE-LAUNCH-INTEGRATION-B — Launch Polish and Surface Consistency

## Context

This is the second execution phase of **FE-LAUNCH-INTEGRATION**.

**FE-LAUNCH-INTEGRATION-A** is complete and established the structural coherence layer:

* upload and results are now aligned into the authenticated product shell
* frontend auth/journey truth is aligned with real analysis-start requirements
* `/analysis/[id]` now serves as the canonical saved-analysis reopen route, redirecting into the results surface
* dashboard/reports now align to the canonical route model
* the deterministic results hierarchy remains intact

The governing preflight concluded that launch integration should be split into:

* **FE-LAUNCH-INTEGRATION-A — coherence / journey / shell alignment**
* **FE-LAUNCH-INTEGRATION-B — launch polish**

The preflight also found that after structural coherence, the remaining gaps are mostly quality-of-experience and consistency issues, such as:

* upload technical debt
* copy inconsistency across landing / upload / results / reports
* weak or abrupt empty/error states
* small rough edges that make the product feel unfinished even though major flows now work

This sprint is **FE-LAUNCH-INTEGRATION-B only**.

It is **not**:

* OPS-S1
* backend reasoning work
* broad marketing-site redesign
* clinician workspace redesign
* auth-platform rewrite
* new analytical or narrative contracts

---

## Objective

Polish the now-coherent frontend product so key launch-facing surfaces feel consistent, intentional, and trustworthy, without changing the underlying analytical model or drifting into operations/compliance work.

This sprint must establish:

* cleaner, more consistent copy across the main launch-facing journeys
* removal or reduction of obvious outdated/deprecated UX debt in launch-critical surfaces
* better empty/error/degraded-state presentation where current UI still feels abrupt
* tighter “one product” feel across landing, upload, results, reports, and account-adjacent areas
* no change to backend analytical contracts or truth hierarchy

This sprint is about **product polish and consistency**, not structural re-architecture.

---

## Stage 1C — Launch Polish Preflight (MANDATORY)

Before editing files, explicitly verify and record:

1. the governing preflight is:

   * `docs/investigations/FE_LAUNCH_INTEGRATION_PREFLIGHT.md`

2. FE-LAUNCH-INTEGRATION-A is complete and the current repo reality is still:

   * core shell/journey/auth alignment is materially improved
   * upload/results now sit coherently in the product journey
   * canonical saved-analysis reopen route is established
   * remaining launch gaps are now primarily polish/consistency issues, not structural route/auth issues

3. before implementation, Cursor must explicitly verify and record:

   * which specific remaining launch-facing rough edges are still present in:

     * landing
     * upload
     * results
     * reports/history
     * dashboard
     * profile/settings where relevant
   * which are truly launch-facing and in scope
   * which are better deferred because they would widen into broader redesign

4. before implementation, Cursor must explicitly classify each candidate issue as one of:

   * copy/label inconsistency
   * empty/error/degraded-state weakness
   * deprecated or misleading UI debt
   * small navigation/interaction rough edge
   * out of scope

5. this sprint will **not**:

   * widen into OPS-S1
   * change backend reasoning or narrative generation
   * redesign the whole marketing site
   * rewrite auth architecture
   * redesign clinician report or deterministic results hierarchy
   * become an unconstrained “general tidy-up”

6. if the remaining issues are broader than a bounded polish sprint allows, STOP and report rather than quietly expanding scope

If any of the above is false:

* STOP
* report precisely
* do not proceed

---

## Scope (strict)

### REQUIRED IN SCOPE

#### 1. Copy and terminology alignment across core product journey

Primary likely surfaces:

* `frontend/app/page.tsx`
* `frontend/app/(app)/upload/page.tsx`
* `frontend/app/(app)/results/page.tsx`
* `frontend/app/(app)/dashboard/page.tsx`
* `frontend/app/(app)/reports/page.tsx`
* small adjacent components only if directly relevant

You must smooth out obvious copy inconsistencies across the main launch-facing journey.

Requirements:

* align terminology so users are not bounced between conflicting product concepts
* preserve the deterministic-vs-narrative truth boundary already established
* keep wording honest about what the product is doing
* do not drift into full marketing rewriting

This includes items such as:

* route/page headings
* CTAs
* helper text
* section labels
* small explanatory copy

---

#### 2. Upload-surface cleanup for launch credibility

Primary likely surfaces:

* `frontend/app/(app)/upload/page.tsx`
* directly adjacent upload components if strictly required

You must address the most obvious upload-surface launch rough edges that the preflight identified.

Examples may include:

* deprecated or confusing tabs/paths that should not remain visible in the launch-facing experience
* stale helper text
* rough or overly technical UX elements
* lingering debug/developer-facing presentation debt if still visible in the launch path

Requirements:

* keep cleanup bounded
* do not redesign the upload product from scratch
* preserve truthful data-entry and analysis-start behaviour

---

#### 3. Empty / error / degraded-state polish in launch-facing journeys

Primary likely surfaces:

* dashboard/reports empty states
* upload/result launch-path feedback
* small route-level error messaging in the frontend
* narrative/report coexistence empty states only if still rough

You must improve the most user-visible weak states that currently make the product feel abrupt or unfinished.

Requirements:

* keep messaging calm, clear, and non-technical where possible
* do not hide real limitations
* do not introduce fake reassurance
* improve launch trust without changing underlying logic

This is not a global state-system redesign.
It is bounded launch polish.

---

#### 4. Cross-surface coherence checks

Likely surfaces:

* headings and summaries across dashboard / upload / results / reports / profile / settings
* navigation labels if directly needed
* small CTA alignment across these areas

You must ensure these major product surfaces feel like parts of one coherent product.

Requirements:

* no contradictory language between account and analysis areas
* no route labels that feel out of sync with current product structure
* no obvious stale wording left over from prior architecture phases if it affects launch quality

---

#### 5. Keep deterministic result hierarchy and clinician distinction intact

Primary likely surfaces:

* results page and nearby copy only if touched

You must preserve:

* hero priority
* trust strip role
* clinician report separation
* narrative as companion layer

This sprint must not undo FE-S2 or FE-LAUNCH-INTEGRATION-A discipline.

---

#### 6. Targeted regression coverage

Likely surfaces:

* frontend component tests
* integration/e2e assertions if current labels or launch-path states are updated
* small snapshot tests only if truly useful

You must add/update the minimum regression coverage needed to prove:

* launch-facing copy/labels now align with intended product framing
* upload no longer exposes the specific deprecated/rough elements selected for cleanup
* important empty/error/degraded states improved in bounded ways
* no structural/auth/backend contract regressions were introduced

Keep this targeted.
Do not turn this into a broad test rewrite.

---

### OPTIONAL / BOUNDED IN SCOPE

#### 7. Small interaction polish only if directly tied to launch-facing confusion

If a small interaction tweak is required to resolve a real launch-facing confusion point, that is acceptable.

Requirements:

* bounded
* directly tied to a verified issue from Stage 1C
* not a broad UX redesign

---

## OUT OF SCOPE (STRICT)

* No OPS-S1 or compliance work
* No backend reasoning or narrative changes
* No broad marketing-site rewrite
* No auth-platform rewrite
* No clinician report redesign
* No hero/trust/results hierarchy redesign
* No new analytical or narrative contracts
* No enterprise/commercial workflow redesign
* No unconstrained repo tidy-up

---

## Implementation constraints

### Polish only, not structural rework

Structural coherence was handled in FE-LAUNCH-INTEGRATION-A. This sprint should remain a refinement pass.

### Preserve truthfulness

Copy and polish must not overpromise or blur the deterministic/narrative boundary.

### Stay launch-facing

Only fix rough edges that materially affect how the current product feels to a launch user.

### No hidden scope creep

Do not use this sprint as a vehicle for unrelated frontend clean-up.

---

## Acceptance criteria

FE-LAUNCH-INTEGRATION-B is complete only if:

1. core launch-facing surfaces use more consistent and coherent wording
2. the upload surface no longer exposes the selected high-visibility rough/deprecated elements
3. the most important launch-facing empty/error/degraded states are improved in bounded ways
4. dashboard / upload / results / reports / account-adjacent surfaces feel more like one product
5. deterministic results hierarchy and clinician/narrative distinctions remain intact
6. targeted regression coverage proves the polish changes
7. no OPS, backend, auth-rewrite, or broad redesign scope is introduced

---

## STOP conditions

STOP immediately if:

* the selected polish issues require structural redesign rather than bounded refinement
* the work begins drifting into broad marketing rewrite or auth redesign
* the work begins altering deterministic result hierarchy or clinician-report separation
* the work begins widening into unrelated frontend tidy-up
* the only way to improve the launch feel is to invent product claims or hide real limitations

If any STOP condition triggers:

* halt
* report precisely
* do not widen the sprint

---

## Validation / evidence required

Before closure, provide evidence for:

* exact launch-facing surfaces polished
* exact copy/label/empty-state changes made
* exact upload cleanup performed
* exact cross-surface coherence issues resolved
* confirmation that deterministic result hierarchy remained intact
* tests added/updated
* files created/modified
* final git state

---

## Execution sequence (SOP aligned)

1. Kernel START
2. Complete Stage 1C Launch Polish Preflight
3. Implement bounded launch-facing copy/coherence polish
4. Clean selected upload-surface rough edges
5. Improve bounded empty/error/degraded states
6. Add/update targeted regression coverage
7. Validate locally
8. Kernel FINISH
9. Produce closure report

---

## Output

Provide:

* files created/modified
* launch-polish summary
* upload-cleanup summary
* empty/error-state summary
* cross-surface-coherence summary
* regression summary
* kernel finish status
* final git state

---

## Strategic intent

This sprint exists to:

> take the now-coherent frontend product and remove the most visible launch-facing rough edges so it feels more consistent, intentional, and trustworthy, without drifting into OPS work, backend changes, or broad redesign

Do not expand beyond that.
