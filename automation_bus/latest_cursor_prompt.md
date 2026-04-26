---
work_id: D-4
branch: feature/wave1-domain-refinement
risk_level: HIGH
execution_model: TWO_PHASE_START_FINISH
change_type: BEHAVIOUR
---

# D-4 — Wave 1 domain-card refinement

## Cursor agent

Use `healthiq-core-engine`.

This is mandatory.

---

## Objective

Refine the live Wave 1 domain-card experience for:

1. Cardiovascular health
2. Blood sugar control
3. Liver health

This sprint exists because UAT found the Wave 1 layer is directionally valuable but still has one refinement sprint’s worth of issues before broader use.

The purpose of this sprint is to improve:

- band/headline coherence
- collapsed-card clarity
- confidence/story alignment
- user-facing traceability
- removal of internal caveat leakage

Do not widen into Phase 2 domains.

---

## Branch requirement

Before doing anything else:

1. create and switch to this branch:
   `feature/wave1-domain-refinement`
2. confirm the branch name before implementation begins

If the branch already exists locally, check it out and confirm.

---

## Precondition

D-1, D-2, and D-3 must already exist on the current branch history or be cleanly available for this branch to build on.

Before implementation, restate:

- where D-3 frontend/backend output is being read from
- which exact Wave 1 UAT issues are being addressed in this sprint
- which issues are intentionally out of scope

If prior sprint output is missing or inconsistent, STOP and report.

---

## In scope

### Wave 1 only
- Cardiovascular health
- Blood sugar control
- Liver health

### Backend / contract refinement
1. Refine collapsed headline / summary logic so the visible first impression is coherent with:
   - band label
   - contributor pattern
   - confidence state
2. Prevent “Stable / broadly stable” wording from conflicting with active-risk or active-strain messaging where UAT showed that mismatch.
3. Remove internal caveat slug leakage from user-facing card presentation.
4. Improve collapsed traceability with a short evidence anchor phrase where needed.

### Frontend refinement
1. Update the Wave 1 cards to present the refined contract clearly.
2. Ensure internal caveat flags are not shown raw to users.
3. Keep the cards additive and limited to the three Wave 1 domains.

---

## Out of scope

- Phase 2 domains
- clinician PDF changes
- large results-page redesign
- full “What’s driving this” redesign
- scoring-engine overhaul
- confidence-tier model redesign beyond what is necessary for Wave 1 coherence
- any LLM-generated narrative layer

Do not widen scope.

---

## UAT findings this sprint must address

These are the specific UAT issues to solve:

### 1. Cardiovascular coherence issue
“Stable / broadly stable” clashes with:
- homocysteine/inflammation-led subtitle
- “accumulating vascular-risk signals”
- “warrant review” style consequence

### 2. Blood sugar coherence issue
“Stable / broadly stable” clashes with:
- impaired sugar/lipid handling subtitle
- “glycaemic strain” language
- limited confidence + missing markers

### 3. Internal caveat leakage
Liver card exposes internal-style caveat strings / engineering tokens to users.

### 4. Weak collapsed traceability
Users cannot quickly see what evidence domain cards are anchored to.

These issues are in scope.
Do not drift into unrelated page complaints unless directly required to solve the above.

---

## Required implementation outcomes

## A. Headline / band / pattern coherence

For cardiovascular and blood sugar cards:

1. Rework the collapsed `headline_sentence` logic so it does not say “broadly stable” when:
   - contributor or consequence language indicates active-risk / active-strain
   - confidence is materially limited and the subtitle implies dysfunction
2. Keep the result medically restrained and consumer-legible.
3. Do not simply make everything more alarming.
4. The collapsed line must read as one coherent story with:
   - band
   - contributor pattern
   - confidence

### Important
This may require adjusting sentence-template selection logic rather than the numeric score itself.
Do not recalibrate scores unless absolutely necessary and clearly justified.

---

## B. Confidence / story alignment

For cardiovascular especially:

1. Ensure the visible collapsed narrative does not imply one story while the confidence sentence clearly refers to a different evidence base without explanation.
2. If confidence is driven by lipid completeness but the card story is led by homocysteine/inflammation context, the visible wording must bridge that honestly.

The user should not feel:
- “the story says X”
- “confidence says Y”
- “I don’t know what this score is actually about”

---

## C. Remove internal caveat leakage

1. Raw internal caveat flags / snake_case / engineering tokens must not be shown in the user-facing Wave 1 cards.
2. If caveat information is still useful to surface, convert it into safe user-facing language only if already supported by the contract and truthful.
3. Otherwise suppress it from the visible card.

Do not remove backend truth just to hide it.
The requirement is to stop leaking internal implementation language to the user.

---

## D. Improve collapsed traceability

For each Wave 1 domain card, add or refine a short collapsed evidence anchor so the user can more quickly understand what the card is reacting to.

Examples of the kind of thing intended:
- a short evidence cue
- a small anchor phrase
- a concise “based mainly on…” style signal

Do not add a large new section.
Do not redesign the whole card.
This is a compact traceability improvement only.

---

## Architectural constraints

### 1. Keep Wave 1 additive
Do not replace the broader results architecture.

### 2. Do not expose internal reasoning artifacts raw
No internal flags, slugs, or implementation tokens should appear in the customer-facing UI.

### 3. Keep deterministic assembly
All refinements must remain deterministic and grounded in the current backend/domain contract.

### 4. No false reassurance and no unnecessary alarm
This sprint is about coherence, not tone inflation.

### 5. Prefer narrow fixes
Solve the UAT issues with the smallest high-value changes.
Do not over-engineer.

---

## Files likely in scope

These are likely, not mandatory:

### Backend
- `backend/core/analytics/domain_narrative_wave1.py`
- `backend/core/analytics/domain_score_assembler.py`
- targeted backend tests if template selection or visible contract fields change

### Frontend
- `frontend/app/components/results/Wave1DomainCards.tsx`
- `frontend/app/(app)/results/page.tsx` only if minimally needed
- `frontend/app/types/analysis.ts` only if contract-safe additions are truly needed
- targeted frontend tests

---

## Files likely out of scope

Do not touch unless absolutely required and justified:

- clinician report surfaces
- PDF/export paths
- pricing / trends / actions / upload flows
- Phase 2 domain logic
- unrelated results components
- broad SSOT/scoring policy files

---

## Testing discipline

Do not run the full repository test suite.

Run only:

### Backend
1. targeted tests for headline/summary/coherence logic where touched
2. directly relevant existing Wave 1 backend tests

### Frontend
3. targeted tests for Wave 1 card rendering / caveat suppression / collapsed evidence anchors
4. type-check for touched contract/UI surfaces
5. bounded browser/UAT recheck on the same Wave 1 result path if practical

Before running tests, state:
- what you will run
- why it is relevant
- what broader suites you are deliberately excluding

---

## Acceptance criteria

This sprint is successful only if:

1. Cardiovascular collapsed card no longer reads as “stable” while simultaneously presenting active vascular-risk accumulation without a coherent bridge.
2. Blood sugar collapsed card no longer reads as “stable” while simultaneously presenting impaired handling / glycaemic strain without a coherent bridge.
3. User-facing internal caveat leakage is removed.
4. Each Wave 1 card has a clearer collapsed evidence anchor.
5. Scores remain deterministic and medically grounded.
6. No frontend exposure beyond the three Wave 1 domains is introduced.
7. Targeted tests pass.
8. Browser/UAT confirms the refined cards feel more coherent than D-3.

---

## Reporting requirements

When finished, report back in these sections:

### 1. Branch
- confirm branch name

### 2. Preflight restatement
- objective
- files touched
- files not touched
- exact UAT issues addressed

### 3. Requested changes made
- exact files changed
- what changed in backend logic
- what changed in frontend presentation
- how internal caveat leakage was handled
- how collapsed evidence traceability was improved

### 4. Coherence fixes
For cardiovascular and blood sugar separately:
- what the old issue was
- what changed
- why the new wording/logic is more coherent

### 5. Tests run
- exact tests
- results

### 6. Browser/UAT recheck
- what was rechecked
- whether the D-3 UAT issues now feel materially improved

### 7. Known limits intentionally deferred
- anything still left for later
- any remaining Wave 1 caveats

### 8. Uncommitted / not merged
- confirm work is not merged to `main`

---

## STOP conditions

STOP and report instead of widening scope if any of the following occurs:

1. Fixing coherence would require a broad score recalibration rather than narrow refinement.
2. Removing caveat leakage would require hiding contract truth in a misleading way.
3. Improving collapsed traceability would require a large results-page redesign.
4. A Phase 2 domain starts to creep into scope.
5. Clinician-facing outputs would need modification to complete this sprint.

If blocked, report:
- exact blocker
- affected files
- smallest safe remediation path