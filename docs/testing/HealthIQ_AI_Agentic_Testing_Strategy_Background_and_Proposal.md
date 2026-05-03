# HealthIQ AI — Agentic Automated Testing Strategy
## Background and Proposal Paper for Team Review

**Document status:** Draft for feedback and critique  
**Prepared for:** HealthIQ AI team  
**Role perspective:** Head of Testing Strategy  

---

## 1. Background

HealthIQ AI has now reached a level of product and architectural complexity where conventional feature-by-feature testing is no longer sufficient.

The platform is not simply rendering static health content. It is assembling customer-facing health interpretation from multiple deterministic layers, including:

- uploaded blood panel parsing
- biomarker alias normalisation
- canonical biomarker mapping
- questionnaire and lifestyle context
- deterministic signal logic
- confidence and missing-marker logic
- persisted result snapshots
- frontend domain-card rendering
- customer-facing narrative translation

Recent Wave 1 work on the customer-facing domain-card layer exposed a deeper testing issue. The visible problem was contradictory card content, where one section of a card could appear reassuring while another implied strain, risk, or clinician review.

That failure was not merely a copy issue. It revealed that different parts of the output were drawing from different authorities, with no single primary-pattern anchor controlling the customer-facing story. The architectural issue has now been substantially corrected, but the incident highlighted a broader concern.

HealthIQ AI does not only have isolated bugs. It has a growing testing breadth problem.

As more biomarkers, aliases, derived markers, signals, domain cards, and persisted outputs are added, the risk increases that defects will escape into UAT unless the testing strategy matures alongside the product.

---

## 2. Recent failure classes

Recent escaped or near-escaped failures include:

- GGT alias not mapping even though the marker was present in the payload
- bilirubin being present on the panel but shown as missing because of canonical-ID mismatch
- Wave 1 domain cards showing contradictory headline and consequence logic
- internal-style identifiers such as `total_bilirubin` leaking into user-facing UI
- backend/runtime fixes not affecting old analyses because persisted result snapshots remained frozen
- UAT finding credibility and trust failures not caught by narrower regression tests

These are not all the same type of bug. They cut across parsing, mapping, analytics, persistence, rendering, and user trust.

This means the test architecture must become broader than standard unit testing.

---

## 3. Core testing problem

The current testing model appears strongest where the system is narrowest:

- individual backend functions
- isolated validators
- specific regression checks
- targeted remediation tests

It is weaker where the product is broadest:

- full upload-to-result journeys
- live-like panels
- alias coverage across real lab formats
- stale persisted outputs
- customer-facing coherence
- cross-section authority alignment
- frontend trustworthiness

This creates a false-confidence risk.

A backend test may pass, but the customer may still see an output that is contradictory, stale, internally labelled, or clinically unconvincing.

For HealthIQ AI, the output surface itself must become a regression surface.

---

## 4. Strategic proposal

HealthIQ AI should develop an agentic automated testing model that continuously analyses the codebase, identifies relevant risk surfaces, proposes appropriate regression coverage, and helps mature the test suite as the product evolves.

This should not be a single autonomous testing agent.

It should be a governed multi-agent testing model aligned to the existing SOP philosophy:

> LLMs reason, inspect, propose, challenge, and generate.  
> Deterministic gates decide pass or fail.  
> No single agent owns the full lifecycle.

The goal is not to let an LLM decide whether the product is correct.

The goal is to use LLMs to improve test discovery, coverage design, and regression breadth, while preserving deterministic validation as the final authority.

---

## 5. Proposed multi-agent testing model

### 5.1 Test Strategist Agent

Purpose:

- identify product-level testing risks
- define required regression categories
- assess whether existing tests are too narrow
- maintain the testing strategy map

This agent asks:

> What could break, and what proof would we need before trusting this release?

---

### 5.2 Repo Analyst Agent

Purpose:

- inspect changed files
- map changes to affected runtime paths
- identify parser, analytics, persistence, API, or UI surfaces touched
- detect whether a change affects the Intelligence Core or customer-facing output

This agent asks:

> Given this change, which parts of the product are at risk?

---

### 5.3 Test Author Agent

Purpose:

- draft missing tests
- create synthetic panels
- extend fixture panels
- create browser/UAT scripts
- add regression tests for escaped defects

This agent asks:

> What concrete tests should now exist?

---

### 5.4 Adversarial Reviewer Agent

Purpose:

- challenge whether proposed tests prove the right thing
- identify shallow tests that only assert implementation details
- check for missing negative cases
- check whether fixtures are realistic enough
- challenge false confidence

This agent asks:

> Could this still fail in production even if these tests pass?

---

### 5.5 Deterministic Test Gate

Purpose:

- run the selected test suite
- produce immutable evidence
- decide pass/fail mechanically
- block unsafe releases

This is not an LLM role.

The deterministic gate asks:

> Did the required tests pass against the current code and fixtures?

---

## 6. Required test layers

HealthIQ AI should mature toward the following testing layers.

### 6.1 Parser and alias coverage

Covers:

- biomarker aliases
- canonical IDs
- lab name variants
- punctuation/casing differences
- unit variants
- live payload replay
- present-but-missing defects

Purpose:

To prevent failures such as GGT and bilirubin being present in a panel but not correctly recognised.

---

### 6.2 Deterministic engine coverage

Covers:

- signal firing
- score assembly
- primary-pattern selection
- confidence logic
- missing-marker logic
- consequence selection
- contradiction suppression

Purpose:

To prove that the analytical engine produces one coherent structured truth.

---

### 6.3 Narrative coherence coverage

Covers:

- headline vs consequence alignment
- summary vs detail alignment
- reassuring vs risk language
- clinician-review language only when justified
- no orphaned or stale narrative fragments

Purpose:

To prevent customer-facing contradiction within the same card or page.

---

### 6.4 Persisted-result and snapshot coverage

Covers:

- old analysis snapshots
- new analysis generation
- stale result behaviour
- snapshot version visibility
- regeneration paths where applicable

Purpose:

To ensure code fixes do not give false confidence when old persisted outputs remain frozen.

---

### 6.5 Frontend trust-surface coverage

Covers:

- no internal slugs or identifiers in UI
- no impossible-looking values shown without handling
- missing markers displayed clearly
- confidence improvers accurate
- page-level and card-level sections using aligned authorities

Purpose:

To protect customer trust in the visible product.

---

### 6.6 End-to-end realistic panel coverage

Covers:

- upload to result
- AB/VR fixture panels
- clean/reassuring panels
- liver, lipid, inflammation, renal and metabolic panels
- partial panels
- messy real-world lab formats

Purpose:

To prove that the assembled product works, not just isolated components.

---

## 7. Test asset strategy

### 7.1 Synthetic panels

Synthetic panels should be used for precision.

They are best for:

- forcing a specific signal state
- testing thresholds
- testing missing-marker logic
- testing contradiction handling
- proving narrow analytical paths

---

### 7.2 Fixture panels

Fixture panels should be used for realism.

They are best for:

- representative customer blood panels
- AB/VR acceptance coverage
- multi-domain interpretation
- confidence and missing-marker behaviour
- repeatable product-level regression

---

### 7.3 Persisted-result fixtures

Persisted fixtures should be used for snapshot risk.

They are best for:

- old result replay
- frozen output detection
- migration/regeneration testing
- frontend behaviour against stored outputs

---

### 7.4 UI/rendering tests

UI tests should be used for customer trust.

They are best for:

- internal label leakage
- contradictory sections
- value formatting problems
- missing or broken card sections
- responsive layout sanity

---

### 7.5 UAT scripts

UAT should be used for final product confidence, not basic defect discovery.

They are best for:

- readability
- credibility
- user journey quality
- business acceptance
- final release confidence

---

## 8. Proposed release confidence model

Before customer-facing changes are accepted, HealthIQ AI should require evidence across five gates.

### Gate 1 — deterministic correctness

The engine produces expected structured outputs for controlled test inputs.

### Gate 2 — mapping completeness

Known panel markers resolve correctly to canonical biomarker IDs.

### Gate 3 — narrative coherence

Customer-facing cards and page sections tell one coherent story.

### Gate 4 — persistence safety

Stored analyses and new analyses behave predictably and honestly.

### Gate 5 — customer trust

The UI contains no internal labels, impossible-looking values, stale outputs, unexplained contradictions, or misleading confidence statements.

A customer-facing release should not be considered safe just because backend unit tests pass.

---

## 9. How this fits the existing SOP model

The proposed testing model fits HealthIQ AI’s current governance philosophy.

The existing SOP model already separates responsibilities across:

- GPT as architecture authority
- Claude as hardening and audit reviewer
- Cursor as implementer
- Kernel as lifecycle enforcer
- Gate as deterministic verifier
- Human as final merge authority

An agentic testing suite should follow the same principle.

No single LLM should be able to:

- define the test strategy
- write the tests
- review its own work
- decide whether the product is safe
- approve release confidence

Instead, the testing system should use role separation, adversarial review, deterministic execution, and immutable evidence.

This is especially important because HealthIQ AI is a deterministic health-analysis platform with long-term clinical-grade ambitions.

---

## 10. Recommended maturity path

### Phase 1 — Testing architecture inventory

Create a map of current tests by layer:

- parser/alias
- canonical ID
- signal logic
- domain card assembly
- persistence
- frontend rendering
- E2E journeys
- UAT scripts

Output:

- current coverage map
- missing coverage map
- escaped-defect regression list

---

### Phase 2 — Known defect regression pack

Turn recent escaped defects into permanent regression coverage.

Initial candidates:

- GGT alias mapping
- bilirubin canonical-ID mismatch
- contradictory Wave 1 card logic
- internal slug leakage
- stale persisted result behaviour
- confidence-improver marker coverage errors

Output:

- permanent escaped-defect regression pack

---

### Phase 3 — Agentic test planner prototype

Build a lightweight agentic planner that can:

- inspect changed files
- classify risk surfaces
- recommend required test categories
- identify whether fixture, synthetic, persistence, UI or E2E tests are needed

Output:

- proposed test-selection report per change

---

### Phase 4 — Deterministic gate integration

Wire selected tests into the existing gate model so that relevant regression suites are run before completion or merge.

Output:

- test evidence attached to sprint/release confidence

---

### Phase 5 — Continuous maturation model

Every escaped UAT defect should be classified and converted into a permanent regression asset.

Output:

- self-improving test suite
- defect taxonomy
- release confidence dashboard

---

## 11. Key design principle

The testing suite should mature in the same direction as the product.

As HealthIQ AI becomes more complex, the test model must become more intelligent, broader, and more adversarial.

However, intelligence in test planning must not replace deterministic proof.

The target model is:

> Agentic test planning.  
> Multi-LLM challenge and review.  
> Deterministic execution.  
> Immutable evidence.  
> Human-controlled release authority.

This is the right testing direction for a platform where correctness, coherence, and trust are all part of the product.

---

## 12. Open questions for team feedback

1. Which current test layers already exist and are reliable?
2. Which escaped defects should become the first permanent regression pack?
3. Should persisted-result testing become mandatory for all customer-facing output changes?
4. What fixture panels should become canonical release gates?
5. How should we classify UI trust failures within the Automation Bus risk model?
6. Where should agentic test-planning evidence live?
7. Should test-selection reports become mandatory before customer-facing sprints complete?

---

## 13. Proposed conclusion

HealthIQ AI should not rely on manual UAT or narrow regression tests to catch broad product-quality failures.

The platform now requires a governed, multi-layer, agent-assisted testing model that can grow with the codebase.

The purpose is not simply to increase test volume.

The purpose is to ensure that every customer-facing result can be trusted as a coherent, current, correctly mapped, deterministically generated output of the HealthIQ AI engine.

