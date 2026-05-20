Use this for Claude Code.

````text
LC-S12A — Forensic Architecture Audit of HealthIQ AI

Role:
You are acting as an uncompromising senior enterprise medical-software architect.

This is an investigation-only audit.

Do not modify code.
Do not modify tests.
Do not create implementation changes.
Do not refactor.
Do not “fix” anything.
Create only the audit report requested below.

Purpose:
Perform a forensic architecture audit of the HealthIQ AI application and answer one central question:

Has the last year of development produced an architecturally serious, enterprise-grade medical interpretation platform, or is the product structurally weak and at risk of becoming an unsellable prototype?

The audit must be direct, evidence-based, and unsentimental.

Do not flatter the team.
Do not soften findings.
Do not assume that because something has many files, tests, or documents it is architecturally good.
Do not judge only whether tests pass.
Judge whether the application is structurally capable of becoming a credible, scalable, governed medical intelligence product.

Repo root:
C:\Users\abroa\HealthIQ-AI-v5

Output report:
C:\Users\abroa\HealthIQ-AI-v5\docs\audit-papers\LC-S12A_forensic_architecture_audit.md

---

# Strategic context

HealthIQ AI is intended to become a UK-first, clinically credible, deterministic blood-test interpretation platform.

The intended product is not a generic LLM wrapper. It should be a governed health intelligence system where:

- uploaded blood results are parsed and normalised
- lab-derived reference ranges are preserved
- biomarkers are canonicalised safely
- deterministic Layer B analytical logic generates structured truth
- Knowledge Bus assets provide governed interpretation depth
- Layer C carries that truth into user-facing narrative without inventing unsupported analysis
- the frontend presents a coherent, commercially credible, understandable report
- future expansion is additive, not a rebuild

The team has recently completed significant work around:

- UK/SI unit governance
- Phase B true conversions
- uploaded-unit display fidelity
- launch-core proving checks
- Sentinel guardrails
- lifestyle/statin visible-payoff checks
- trust-blocker correction
- Knowledge Bus package development

This audit must assess whether those moving parts now form a coherent architecture or whether the application is still brittle, over-complicated, incoherent, or built on weak foundations.

---

# Key documents to read first

Read these if present:

```text
docs/planning-papers/healthiq_launch_core_transformation_plan_FINAL.md
docs/audit-papers/LC-S11_forensic_human_uat_audit.md
docs/audit-papers/LC-S11A_trust_blocker_correction_notes.md
docs/audit-papers/LC-S10B_protection_of_proven_slice_notes.md
docs/audit-papers/LC-S8F_phase_b_true_conversion_implementation_notes.md
docs/audit-papers/LC-S8G_uploaded_unit_display_fidelity_notes.md
docs/audit-papers/LC-S9_launch_core_human_proving_closeout_review.md
docs/audit-papers/launch-core-proving/PROVING_REPORT.md
docs/audit-papers/launch-core-proving/latest_fingerprints.json
````

Also inspect the core repo structure, especially:

```text
backend/
frontend/
knowledge_bus/
sentinel/
automation_bus/
docs/
```

---

# Audit scope

You must assess the application across these dimensions.

## 1. Overall architecture

Assess whether the application has a clear architecture or whether it is a collection of patches.

Review:

* backend structure
* frontend structure
* Knowledge Bus structure
* SSOT structure
* Sentinel/test structure
* Automation Bus workflow
* DTO/contracts
* boundaries between parsing, canonicalisation, scoring, analytics, narrative, and UI

Questions:

* Are responsibilities cleanly separated?
* Are there clear layers?
* Are boundaries enforced or just documented?
* Is there duplicated authority?
* Are there hidden fallback paths?
* Is the current architecture understandable to a future engineering team?
* Could a competent team take this codebase forward, or would they likely recommend a rewrite?

## 2. Medical-governance architecture

Assess whether the app is safe enough in shape for clinical/medical interpretation work.

Review:

* biomarker SSOT
* unit registry
* scoring policy
* reference-range handling
* lab-derived range policy
* signal logic
* Knowledge Bus packages
* domain/system mappings
* WHY assets
* missing-data logic
* caveat handling

Questions:

* Is the system genuinely governed?
* Are clinical claims traceable to assets?
* Are unit conversions safe?
* Are lab-derived ranges preserved?
* Are unsupported claims blocked?
* Are false positives/false alarms structurally prevented?
* Are clinical meanings mixed with presentation copy?
* Is there a clear distinction between scoring, signal firing, and explanation?

## 3. Layer B analytical core

Assess the deterministic analytical engine.

Review:

```text
backend/core/analytics/**
backend/core/scoring/**
backend/core/units/**
backend/core/pipeline/**
backend/core/dto/**
backend/ssot/**
```

Questions:

* Does Layer B produce reliable structured truth?
* Is the analytical state machine coherent?
* Are scoring and signal firing understandable?
* Are directionality problems likely to recur?
* Are derived biomarkers handled safely?
* Are unit conversions integrated in the right place?
* Is the engine too brittle?
* Are there global scoring assumptions that will create future clinical errors?
* Are signals sufficiently governed, or are some just threshold wrappers?

## 4. Knowledge Bus architecture

Assess whether the Knowledge Bus is real intellectual infrastructure or decorative documentation.

Review:

```text
knowledge_bus/packages/**
knowledge_bus/**
docs related to Knowledge Bus
```

Questions:

* Are `pkg_*` assets well structured?
* Are they actually consumed by runtime?
* Are they rich enough to support interpretation?
* Are signal libraries, research briefs, and WHY assets coherent?
* Is there a reliable path from asset → signal → payload → frontend?
* Are there orphaned assets?
* Are there runtime paths using generic fallback instead of Knowledge Bus assets?
* Does Knowledge Bus expansion look additive, or will every new package require custom wiring?
* Is the Knowledge Bus suitable for enterprise-scale medical content governance?

## 5. Layer B → Layer C contract

Assess whether the narrative/display layer is properly governed.

Questions:

* Is there a real structured payload from Layer B to Layer C?
* Or is the system still passing large flat string blobs?
* Can Layer C be prevented from adding unsupported interpretation?
* Are fields clearly marked as preserved vs polishable?
* Is Layer C currently composed or assembled?
* Can Gemini/LLM generation be safely introduced later?
* Are user-facing narratives traceable to deterministic evidence?

## 6. Frontend/product architecture

Assess the frontend as a product experience and as software.

Review:

```text
frontend/app/**
frontend/tests/**
```

Questions:

* Is the frontend mostly rendering governed backend truth?
* Or is it doing logic it should not?
* Are biomarker dials, domain cards, narrative sections, advanced sections, and uploaded-panel fidelity coherent?
* Are display units and labels handled safely?
* Is the current results page commercially credible?
* Is the frontend architecture capable of supporting a polished report experience?
* Or is it likely to need a substantial redesign?
* Is there too much technical/internal language exposed?
* Are sections ordered in a way a human understands?

## 7. Testing and Sentinel architecture

Assess whether the test estate provides real confidence.

Review:

```text
backend/tests/**
frontend/tests/**
sentinel/**
automation_bus/**
```

Questions:

* Are tests protecting real behaviours or just implementation details?
* Is Sentinel meaningful or performative?
* Are escaped defects being converted into guardrails?
* Are there brittle tests tied to exact wording?
* Are there missing high-value integration tests?
* Are there stale fixtures?
* Are Unicode/unit issues likely to recur?
* Is the current test framework enough for clinical-trust software?
* What test gaps would block investor-grade confidence?

## 8. Automation Bus / workflow architecture

Assess the multi-agent workflow.

Questions:

* Is the GPT → Cursor → Claude → human workflow producing controlled progress?
* Is it too bureaucratic?
* Are SOPs adding safety or creating ceremony?
* Are prompts compensating for weak architecture?
* Is branch/work-package governance sound?
* Are audit artefacts useful or accumulating as dead paperwork?
* Could a future team operate this workflow efficiently?

## 9. Scalability and maintainability

Assess whether the app can scale from launch-core to hundreds of biomarkers and broader reports.

Questions:

* Can new biomarkers be added safely?
* Can new signal packages be added safely?
* Can new diseases/systems be added without rewriting?
* Can reference-range variation across labs be handled?
* Can future medication/lifestyle modifiers scale?
* Can the frontend handle deeper/richer reports?
* Can the codebase support multiple developers?
* Are there architectural choke points?
* Are naming conventions consistent?
* Is there excessive coupling?

## 10. Commercial readiness

Assess whether this is becoming a sellable product.

Questions:

* Is the analytical engine differentiated?
* Is the current UI/report experience sellable?
* Would a clinician trust it?
* Would a consumer understand it?
* Would an investor see a serious platform or a hacked prototype?
* What are the biggest risks to product credibility?
* What must be fixed before external pilots?
* What can wait?

---

# Required scoring

Give a brutally honest score from 1–10 for each category:

| Category                   | Score /10 | Rationale |
| -------------------------- | --------: | --------- |
| Overall architecture       |           |           |
| Medical governance         |           |           |
| Layer B analytical core    |           |           |
| Knowledge Bus              |           |           |
| Layer B → Layer C contract |           |           |
| Frontend architecture      |           |           |
| Product/user experience    |           |           |
| Testing/Sentinel           |           |           |
| Maintainability            |           |           |
| Scalability                |           |           |
| Commercial readiness       |           |           |

Then give:

```text
Overall architecture grade:
A / B / C / D / E / F
```

Use this grading standard:

* A = enterprise-grade foundation, needs normal product hardening
* B = strong foundation with some architectural debt
* C = viable but uneven; needs targeted restructuring
* D = prototype with serious architectural debt
* E = fragile demo system; major rebuild likely
* F = not worth continuing without rebuild

Do not inflate the grade.

---

# Specific judgement required

You must answer these directly:

1. Is HealthIQ AI architecturally worth continuing?
2. Is it closer to an enterprise-grade platform or a patched prototype?
3. Which parts are genuinely strong?
4. Which parts are weak or dangerous?
5. Would you recommend continuing to build on this codebase?
6. Would you recommend a partial rebuild? If so, what part?
7. Would you recommend a full rebuild? If not, why not?
8. What are the top five architectural risks?
9. What are the top five product risks?
10. What should the next three sprints be if the goal is commercial readiness?

---

# Required report structure

Create:

```text
C:\Users\abroa\HealthIQ-AI-v5\docs\audit-papers\LC-S12A_forensic_architecture_audit.md
```

Use this structure:

```md
# LC-S12A — Forensic Architecture Audit

## 1. Executive verdict

Include:
- overall grade
- blunt summary
- whether the product is worth continuing
- whether a rebuild is recommended

## 2. Sources inspected

List files/folders/docs inspected.

## 3. Architecture map

Describe the actual application architecture as discovered.

Include:
- ingestion/parsing
- unit normalisation
- scoring
- signal firing
- Knowledge Bus
- Layer B payload
- Layer C/report composition
- frontend rendering
- tests/Sentinel
- Automation Bus

## 4. Category scores

Use the required scoring table.

## 5. What is genuinely strong

Be specific. Do not flatter.

## 6. What is weak, brittle, or dangerous

Be specific. Include examples.

## 7. Medical-governance assessment

Assess clinical safety shape, traceability, reference ranges, units, signal governance, and risks.

## 8. Layer B analytical-core assessment

Assess deterministic engine quality.

## 9. Knowledge Bus assessment

Assess whether assets are real, used, scalable, and rich enough.

## 10. Layer B → Layer C contract assessment

Assess payload quality, narrative governance, flat strings vs structured payload, LLM readiness.

## 11. Frontend/product assessment

Assess current frontend architecture and user-facing product quality.

## 12. Testing/Sentinel assessment

Assess real protection value, blind spots, fixture issues, and regression quality.

## 13. Automation/workflow assessment

Assess whether the GPT/Cursor/Claude workflow is helping or hiding weak architecture.

## 14. Maintainability and scalability

Assess whether future developers could scale this.

## 15. Commercial readiness

Assess what would happen if this were shown to:
- a consumer
- a clinician
- an investor
- a technical due-diligence team

## 16. Rebuild judgement

State one of:
- continue on current codebase
- targeted partial rebuild
- major partial rebuild
- full rebuild recommended

Explain exactly why.

## 17. Top risks

### Top five architectural risks

### Top five product risks

## 18. Recommended next three sprints

Give:
- work ID
- purpose
- why it matters
- what not to do

## 19. Final recommendation

Direct final advice to the product owner.
```

---

# Audit rules

* Be blunt.
* Be evidence-based.
* Quote file paths and examples.
* Do not confuse quantity of code/docs/tests with quality.
* Do not assume the app is good because recent sprints passed.
* Do not assume the app is bad because the frontend is weak.
* Distinguish between bad architecture and bad presentation.
* Distinguish between fixable debt and rebuild-level debt.
* Identify where the product is genuinely differentiated.
* Identify where it is commercially embarrassing.
* Do not recommend polishing weak architecture.
* Do not recommend rebuild unless truly justified.
* Do not write generic software-audit filler.
* Every major claim must be tied to codebase evidence.

```
```
