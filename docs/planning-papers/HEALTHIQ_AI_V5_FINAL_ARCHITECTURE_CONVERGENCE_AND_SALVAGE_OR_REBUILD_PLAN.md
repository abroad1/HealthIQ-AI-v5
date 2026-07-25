# HealthIQ AI v5 — Final Architecture Convergence and Salvage-or-Rebuild Plan

**Status:** Authoritative planning paper for programme execution  
**Purpose:** Give HealthIQ AI v5 one final bounded opportunity to reach a converged launch-critical architecture, with explicit package-level go/no-go decisions and a controlled v6 fallback if convergence fails.  
**Target location:** `docs/planning-papers/`  
**Applies to:** HealthIQ AI v5 architecture programme only  
**Does not authorise:** Controlled beta, prose generation, medical-content promotion, PSI wiring, or estate-wide migration

---

## 1. Executive decision

HealthIQ AI v5 will not be scrapped immediately.

It will also not enter another open-ended re-architecture programme.

Instead, v5 will undergo one final, bounded **architecture convergence programme** designed to answer a definitive question:

> Can the launch-critical HealthIQ AI estate reach a single-authority, frame-correct, provenance-honest architecture without uncontrolled scope growth or further generations of transitional architecture?

The programme will proceed through:

1. a viability and cohort-definition gate;
2. a bounded activation-frame identity package;
3. a bounded provenance and runtime-reachability package;
4. a bounded WHY migration proof with a separate medical-content track;
5. an independent final convergence audit.

Each implementation package must pass an independent go/no-go review before the next package begins.

If the programme breaches its kill criteria, v5 will be frozen and a controlled v6 migration will begin.

---

## 2. Basis for this plan

Independent Cursor and Claude Code reconciliation found broad agreement that:

- registry-level `activation_key` identity is implemented;
- five downstream launch-path consumers still contain frame-collapse risk;
- provenance honesty and disclosure controls exist;
- provenance-blocked packages can nevertheless remain runtime-reachable;
- the WHY estate contains one compiled hypothesis and 40 active legacy YAML hypotheses;
- compiled and legacy WHY are mutually exclusive per signal, but the transition remains incomplete;
- package-generation cohorts do not constitute two separate competing signal libraries;
- Wave 1 architecture acceptance was bounded and did not establish whole-estate convergence;
- controlled beta remains unauthorised.

The remaining defects are sufficiently bounded and identifiable to justify one final convergence attempt. They are not currently evidence of systemic codebase failure.

---

## 3. Programme principles

### 3.1 No eighth open-ended re-architecture

This programme must not become another broad architecture reset.

Every package must have:

- a fixed outcome;
- a bounded code or asset cohort;
- explicit non-goals;
- measurable acceptance criteria;
- named STOP conditions;
- an independent closure audit;
- a human go/no-go decision.

### 3.2 Launch-critical convergence first

The programme is limited to the cohort intended to support controlled-beta evaluation.

Whole-estate migration is not required unless repository reality proves that the launch-critical cohort cannot be isolated safely.

### 3.3 Architecture and medical content remain separate tracks

Engineering must prove that:

- a compiled WHY asset can be introduced;
- it can become the sole runtime authority for its signal/frame;
- the legacy authority can be retired safely;
- provenance and replay remain intact.

Medical review must separately approve:

- the WHY content;
- frame fit;
- evidence;
- limitations;
- clinician and consumer interpretation;
- any modifier or confirmatory-test wording.

Engineering success must not depend on unplanned medical-review throughput.

### 3.4 No classification-only completion for the beta cohort

For launch-critical assets, the final target is actual authority convergence.

`legacy-active`, `blocked`, `inferred`, or similar classifications may remain only where the relevant asset is outside the controlled-beta cohort or a formally accepted STOP decision excludes it from runtime.

### 3.5 No hidden product regression

Architecture hygiene must not silently remove currently relied-upon product behaviour.

Any decision to make an asset non-reachable must include:

- launch-relevance assessment;
- representative-output impact;
- golden-test impact;
- medical/product approval;
- explicit user-facing consequence.

---

## 4. Programme structure

```text
Gate 0 — Cohort and viability definition
        ↓
Package 1 — Activation-frame identity closure
        ↓
Independent Gate 1 — GO / CORRECT / STOP / V6
        ↓
Package 2 — Provenance and runtime-reachability closure
        ↓
Independent Gate 2 — GO / CORRECT / STOP / V6
        ↓
Package 3A — WHY migration architecture proof
        +
Package 3B — Governed medical-content pilot
        ↓
Independent final convergence audit
        ↓
PASS: retain v5 and begin medical-content readiness
FAIL: freeze v5 and begin controlled v6 migration
```

Packages 3A and 3B are coordinated tracks, not independent micro-sprints. The architecture track must not invent or approve medical content, and the medical-content track must not change runtime architecture.

---

## 5. Gate 0 — Cohort and viability definition

### Product outcome

Define the exact controlled-beta architecture cohort and determine whether the proposed convergence programme is practically executable before runtime work begins.

### Required outputs

Create a governed inventory containing:

- launch-critical signal families;
- activation keys and source specification identities;
- packages currently capable of firing;
- multi-frame families reaching the five identified consumer surfaces;
- provenance status and source lineage;
- current user-facing or golden-output relevance;
- WHY authority type;
- medical-review requirement;
- migration complexity;
- proposed inclusion or exclusion from the beta cohort.

### Required decisions

Gate 0 must decide:

1. Which signals and activation frames belong to the proposed controlled-beta cohort?
2. Which provenance-blocked packages are currently runtime-reachable?
3. Which are currently relied upon in representative outputs?
4. Which require specification extraction?
5. Which may safely become non-reachable?
6. What is the exact WHY pilot cohort?
7. What medical-review capacity is available for that pilot?
8. What programme time, cost and scope ceilings apply?

### Gate 0 acceptance criteria

- [ ] Controlled-beta architecture cohort is explicitly enumerated.
- [ ] All five identity surfaces have live-exposure evidence.
- [ ] Provenance-blocked runtime cohort is enumerated.
- [ ] Product impact of possible runtime suppression is known.
- [ ] WHY pilot cohort is bounded.
- [ ] Medical-review ownership and capacity are confirmed.
- [ ] Scope-growth and follow-on limits are approved.
- [ ] No implementation package is authorised without this gate.

### Gate 0 STOP conditions

STOP and reconsider v6 if:

- the launch-critical cohort cannot be isolated;
- reliable current-state counts cannot be produced;
- canonical research sources cannot be identified for a material proportion of the intended cohort;
- the programme requires estate-wide migration before any bounded cohort can be made safe;
- no credible medical-review route exists for the WHY pilot.

---

## 6. Package 1 — Activation-frame identity closure

### Product outcome

Ensure every launch-path consumer that ranks, joins, groups, selects or explains signals preserves activation-frame identity.

### Verified starting scope

The package must assess and, where required, correct:

- `interpretation_display_layer_publish_v1.py`;
- `domain_score_assembler.py`;
- `narrative_report_compiler_v1.py`;
- `intervention_selector_v1.py`;
- `signal_interaction_builder.py`.

The interaction builder must be assessed specifically for:

- graph-node identity;
- confidence lookup;
- family-level versus frame-level aggregation;
- output metadata that appears frame-aware while internal logic remains `signal_id`-keyed.

### Rules

- Preserve all frames unless an approved policy explicitly selects one.
- Do not invent a clinical priority rule.
- Do not use frontend logic to resolve medical identity.
- Do not expand into provenance, WHY content, PSI, prose or estate regeneration.
- Intentional family-level aggregation must be explicit and non-destructive.

### Acceptance criteria

- [ ] No launch-path consumer silently collapses distinct activation frames.
- [ ] `signal_interaction_builder.py` core node/confidence logic is genuinely frame-safe.
- [ ] Any intentional family-level aggregation is governed and tested.
- [ ] Existing single-frame behaviour remains compatible.
- [ ] Multi-frame golden and adversarial cases pass.
- [ ] Architecture and identity gates pass.
- [ ] Independent audit confirms the five-surface obligation is closed.

### Gate 1 decision

After independent audit:

```text
GO       — proceed to Package 2
CORRECT  — one bounded correction only
STOP     — convergence approach no longer credible
V6       — freeze v5 and begin migration
```

More than one unplanned mandatory correction package triggers the programme kill criteria.

---

## 7. Package 2 — Provenance and runtime-reachability closure

### Product outcome

For every launch-critical package, ensure that it either:

1. has explicit, defensible research lineage and remains runtime-reachable; or
2. is non-claimable and non-reachable by explicit governed decision.

### Scope

The package must reconcile:

- package manifest provenance;
- `source_spec_id`;
- investigation-spec extraction and attachment;
- provenance status;
- signal-registry loading;
- scoring and ranking reachability;
- report and replay disclosure;
- launch-critical package inventories.

### Required pre-change assessment

For every provenance-blocked package:

- Can it currently load?
- Can it currently fire?
- Can it rank as a top finding?
- Has it appeared in representative or golden outputs?
- Is it required for the controlled-beta cohort?
- Can canonical lineage be reconstructed?
- What happens if it is suppressed?

### Rules

- Do not invent source identities.
- Do not equate inferred directory lineage with explicit specification lineage.
- Do not silently remove a currently relied-upon signal.
- Do not force all package generations into one estate-wide migration.
- Runtime reachability must agree with the package’s governed eligibility status.

### Acceptance criteria

- [ ] Every launch-critical reachable package has explicit lineage.
- [ ] Every launch-critical package without explicit lineage is non-reachable.
- [ ] No beta-claim-blocked package can fire or rank.
- [ ] Any suppression is medically and product-approved.
- [ ] Golden outputs have been reviewed for intended changes.
- [ ] Registry, provenance gates, DTOs and replay evidence agree.
- [ ] Independent audit confirms no blocked-but-reachable launch-critical assets remain.

### Gate 2 STOP conditions

STOP and consider v6 if:

- canonical lineage cannot be reconstructed without invention;
- runtime exclusion causes broad, poorly understood product loss;
- the launch-critical cohort cannot be separated from the wider package estate;
- the package expands into estate-wide regeneration;
- more than one additional mandatory architecture package emerges.

---

## 8. Package 3A — WHY migration architecture proof

### Product outcome

Prove that v5 can replace legacy WHY authority cleanly for a bounded representative launch-critical cohort.

### Architecture scope

For the agreed pilot cohort:

- compile governed hypothesis artefacts;
- attach explicit source lineage;
- preserve frame identity;
- promote compiled authority deterministically;
- remove the corresponding legacy YAML from runtime authority;
- prove rollback, parity, auditability and replay;
- enforce one authority per signal/frame.

### Rules

- Do not attempt all 40 legacy hypotheses in one package.
- Do not write or approve medical content.
- Do not delete legacy YAML before compiled promotion and parity evidence.
- Do not retain overlapping active authority for the same signal/frame.
- Classification-only does not count as success for the pilot cohort.

### Acceptance criteria

- [ ] Exact pilot cohort is documented.
- [ ] Compiled artefacts use approved medical content from Package 3B.
- [ ] One runtime authority exists per pilot signal/frame.
- [ ] Corresponding legacy authority is retired from runtime.
- [ ] No hidden fallback remains.
- [ ] Determinism, provenance, replay and rollback pass.
- [ ] Root-cause and clinician-report tests pass.
- [ ] Independent audit confirms the migration mechanism is scalable.

---

## 9. Package 3B — Governed medical-content pilot

### Product outcome

Provide the medically approved WHY content required by the Package 3A pilot without converting the architecture programme into an undefined content-production programme.

### Scope

For the exact pilot cohort:

- review canonical research;
- define frame-specific hypotheses;
- approve consumer interpretation boundaries;
- approve clinician interpretation boundaries;
- define uncertainty and limitations;
- approve confirmatory-test context where relevant;
- document rejection or unresolved status.

### Rules

- MR-BATCH-001B remains benchmark/test-only.
- No content is promoted because it is structurally convenient.
- Medical review and engineering approval remain separate.
- The medical pipeline must record evidence, disagreement and final authority.

### Acceptance criteria

- [ ] Every promoted pilot asset has explicit medical approval.
- [ ] Every claim traces to approved research.
- [ ] Consumer and clinician boundaries are defined.
- [ ] Rejected or unresolved content remains non-production.
- [ ] Review completion fits the approved programme window.

### Medical-review viability trigger

If the pilot cannot obtain the required review within the agreed programme window, pause the programme and decide whether to:

- reduce the cohort;
- revise the content pipeline;
- defer the affected signal;
- or trigger the v6 decision.

Medical-review delay alone does not prove that v5 architecture is unsalvageable, but it may prove that the proposed convergence programme is not executable as designed.

---

## 10. Final independent convergence audit

Cursor and Claude Code must independently verify the final state.

The audit must establish:

- one active medical authority per launch-critical activation frame;
- no residual frame collapse;
- explicit lineage for every reachable launch-critical signal;
- no provenance-blocked launch-critical package remains reachable;
- no pilot-cohort legacy WHY remains active;
- no hidden fallback or competing authority exists;
- package and architecture inventories match the live repository;
- architecture gates and relevant tests pass;
- no new compulsory architecture package is concealed as a carry-forward.

The audit must not accept:

- “accepted with conditions”;
- “legacy-active but classified” for the pilot cohort;
- “launch honest” without authority convergence;
- BUILD-register claims without code evidence;
- documentation-only closure.

### Final decisions

```text
PASS
Retain v5 and proceed to the medical-content and prose readiness programme.

CONDITIONAL PASS
Only where remaining items are non-launch-critical, explicitly deferred and do not create duplicate authority.

FAIL
Freeze v5 architecture changes and initiate controlled v6 migration.
```

---

## 11. Programme kill criteria

The v5 convergence programme must stop if any of the following occurs.

### 11.1 Cohort-isolation failure

The launch-critical cohort cannot be separated without uncontrolled whole-estate changes.

### 11.2 Canonical-lineage failure

A material proportion of the intended beta cohort cannot be tied to genuine canonical research authority without inventing provenance.

The permitted threshold must be set at Gate 0.

### 11.3 Authority-retirement failure

For the approved WHY pilot, legacy authority cannot be removed without retaining overlapping or competing authority for the same signal/frame.

### 11.4 Cross-layer authority duplication

The same medical decision for the same signal/frame remains authoritatively implemented in multiple runtime layers and cannot be centralised cleanly.

Non-overlapping transitional paths do not trigger this criterion by themselves.

### 11.5 Scope-growth ceiling

Trigger a stop and v6 review if:

- more than one unplanned mandatory architecture package emerges; or
- any package expands by more than 25% beyond its approved material scope without explicit human reauthorisation.

### 11.6 Time and cost ceiling

Gate 0 must define the maximum programme duration and engineering/medical-review budget.

Exceeding either ceiling requires a formal continue-versus-v6 decision. It may not be waived informally.

### 11.7 Medical-review viability failure

The bounded WHY pilot cannot obtain adequate medical review within the approved programme window and no safe cohort reduction is available.

### 11.8 Independent-assurance failure

Cursor and Claude Code materially disagree after remediation about:

- active medical authority;
- runtime reachability;
- frame preservation;
- provenance;
- or legacy retirement.

---

## 12. Controlled v6 fallback

If the programme fails, v5 will be frozen except for essential safety maintenance.

v6 must use a controlled strangler migration, not a wholesale copy or blank-sheet rewrite.

```text
build a canonical compiler and runtime core
→ select one medically approved signal cohort
→ migrate explicit research authority and frame identity
→ prove deterministic parity and provenance
→ switch runtime authority
→ retire the corresponding v5 path
→ repeat by governed cohort
```

Only assets meeting all of the following may migrate:

- canonical research lineage;
- explicit activation-frame identity;
- medical approval;
- deterministic tests;
- known runtime purpose;
- no unresolved competing authority.

Existing v5 assets must not be imported merely because they currently exist.

---

## 13. Explicit non-goals

This plan does not authorise:

- controlled beta;
- public launch;
- prose library generation;
- promotion of MR-BATCH-001B;
- PSI runtime wiring;
- estate-wide activation compilation;
- estate-wide WHY migration;
- frontend redesign;
- Gemini activation;
- undocumented carry-forwards;
- automatic progression between packages.

---

## 14. Programme completion condition

The programme is complete only when one of two outcomes is formally recorded:

### Outcome A — v5 retained

Independent evidence confirms that the launch-critical estate has converged and v5 can safely proceed to medical-content readiness.

### Outcome B — v5 frozen

The kill criteria are met, the convergence attempt is closed without further remediation cycles, and controlled v6 migration is authorised.

There is no third outcome in which v5 enters another indefinite architecture-improvement programme.
