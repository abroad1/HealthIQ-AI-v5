# HealthIQ AI — Deterministic Narrative Sprint Strategy (Final)

## 1. Purpose

This document defines the strategic sprint series required to move HealthIQ from a strong but fragmented deterministic interpretation stack toward a world-class deterministic narrative stack capable of supporting the benchmark AB gold-standard narrative.

This is not a frontend polish plan.
This is not a prompt-engineering plan.
This is not a generic “make the report nicer” plan.

It is a build strategy for the deterministic narrative support stack.

The central conclusion remains:

HealthIQ’s main gap is not raw biomarker data.
HealthIQ’s main gap is not only frontend presentation.
HealthIQ’s main gap is that it does not yet have the deterministic narrative asset and compiler layers needed to transform strong backend intelligence into a pathway-led, body-wide, clinically serious report of the standard captured in the benchmark narrative.

---

## 2. The deterministic narrative support stack

For planning purposes, the missing capability should be treated as a four-layer stack.

### 2.1 Data and contract layer

This layer holds the underlying structured inputs that narrative depends on, including:
- raw biomarker values and lab ranges
- questionnaire and lifestyle inputs
- ranked findings
- root-cause evidence blocks
- transition codes and prior-panel links
- cluster and system burdens
- confirmatory tests and actions

This layer is partly strong already, but has specific contract gaps.

### 2.2 Governed narrative asset layer

This layer holds the governed deterministic content assets that narrative compilers need, including:
- pathway explainers
- functional interpretation labels
- confidence / uncertainty phrasing templates
- monitoring and resolution criteria
- body-overview posture assets
- retail patient summary assets
- governed interpretation entities and IDL records

This is one of the main missing layers today.

### 2.3 Compiler and assembly layer

This layer consumes data/contracts and governed narrative assets, and compiles them into section outputs such as:
- body overview
- lead pathway explanation
- secondary pattern explanation
- longitudinal change
- next steps
- patient-facing summary
- clinician synthesis

This is the master missing layer.

### 2.4 Output and display layer

This layer surfaces the compiled deterministic outputs through:
- clinician report structures
- retail summary structures
- future frontend journey components

This layer should be revisited seriously only after the deterministic narrative outputs are materially stronger, though thin validation surfacing may run in parallel where useful.

---

## 3. What already exists and should be reused

The existing repo has substantial foundations. These should be reused, not rebuilt.

### 3.1 Canonical biomarker SSOT

The repo already has strong canonical biomarker identity support.

Key authority:
- `backend/ssot/biomarkers.yaml`

This provides canonical biomarker IDs, metadata, aliases, and context tags used throughout the stack.

### 3.2 Lab-shaped panel fixtures

The repo already has strong lab-shaped panel fixtures for AB/VR acceptance-style work.

Key authority:
- `backend/tests/fixtures/panels/ab_full_panel_with_ranges.json`
- `backend/tests/fixtures/panels/vr_full_panel_with_ranges.json`
- `backend/tests/fixtures/panels/panel_acceptance_profiles_v1.yaml`

These are not the same thing as SSOT scoring/range authority.
They are fixture authorities for acceptance harnesses.

### 3.3 Range and scoring authority

This must be treated carefully.
The repo is not a single unified “range infrastructure.”
There are distinct layers:
- SSOT metadata
- lab-provided reference ranges in fixtures/payloads
- scoring/range policy authority

Important repo reality:
ordinary analytes are often lab-range-sovereign in scoring paths, not backed by SSOT fallback scoring.

Key evidence:
- `backend/tests/test_scoring_lab_range_only.py`
- `backend/ssot/ranges.yaml`
- `backend/ssot/scoring_policy.yaml`

This distinction matters for future sprint design.

### 3.4 Questionnaire and lifestyle intake

The repo already captures much of the contextual data needed for narrative.

Key authority:
- `backend/ssot/questionnaire.json`
- `backend/ssot/lifestyle_registry.yaml`
- `backend/core/pipeline/questionnaire_mapper.py`
- `backend/core/analytics/lifestyle_modifier_engine.py`

The current weakness is not capture.
The weakness is deterministic interpretation joins.

### 3.5 Ranked lead logic and report structure

The repo already has deterministic ranking and structured report compilation foundations.

Key authority:
- `backend/ssot/arbitration_registry.yaml`
- `backend/core/analytics/report_compiler_v1.py`
- `backend/core/contracts/report_v1.py`
- `backend/core/contracts/clinician_report_v1.py`

This is a major strength.
The missing layer is richer narrative compilation on top of it.

### 3.6 Root-cause and confirmatory-test infrastructure

The homocysteine domain in particular is already relatively strong.

Key authority:
- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`
- `backend/core/analytics/root_cause_compiler_v1.py`
- `backend/core/contracts/root_cause_v1.py`
- `knowledge_bus/registries/confirmatory_tests_v1.yaml`

This is one of the strongest existing deterministic domains in the repo.

### 3.7 Cluster and system grouping foundations

The repo already has governed cluster/system structures covering the benchmark’s main body domains.

Key authority:
- `backend/ssot/clusters.yaml`
- `backend/ssot/system_burden_registry.yaml`
- `backend/core/analytics/calibration_engine.py`

These support system-level reasoning, but do not yet constitute a narrative reassurance layer.

### 3.8 Longitudinal infrastructure foundations

The repo already has prior-snapshot linking and transition-code support.

Key authority:
- `backend/core/analytics/snapshot_linker.py`
- `backend/core/analytics/state_transition_engine.py`
- `backend/core/contracts/state_transition_v1.py`

This is a real foundation, but it is not sufficient yet for benchmark-grade longitudinal narration.

### 3.9 IDL and interpretation display layer foundations

The IDL exists as a governed interpretation display authority, but it should not be overstated.

Key authority:
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`
- `backend/core/analytics/interpretation_display_layer_publish_v1.py`

This gives governed display records and short `why_it_matters` support.
It does **not** yet provide the narrative depth required by the benchmark.

---

## 4. What is actually missing

The missing layers are now clear.

### 4.1 No deterministic narrative compiler layer

This is the master gap.

The current compiler stack produces structured ranked JSON and clinician-report structures.
It does not produce pathway-led prose or benchmark-style narrative sections.

Key evidence:
- `backend/core/analytics/report_compiler_v1.py`
- `backend/artifacts/golden_runs/20260405T085509Z/narrative.txt`

The latter confirms that current runtime narrative output is placeholder quality, not benchmark-grade deterministic narrative.

### 4.2 No body-overview / panel-posture compiler

There is no governed compiler that can say, deterministically:
- the background physiology is calm
- this is not broad metabolic deterioration
- one narrower unresolved inefficiency stands out

The inputs exist.
The compiler does not.

Key anchors:
- `backend/ssot/clusters.yaml`
- `backend/ssot/system_burden_registry.yaml`
- `backend/core/analytics/calibration_engine.py`

### 4.3 No lifestyle-to-pathway interpretation joins

Lifestyle intake exists, but the deterministic narrative joins do not.

Important examples:
- alcohol → one-carbon / methylation / macrocytosis context
- hydration → renal interpretation context
- weight loss / fasting → glycaemic improvement context

Key anchors:
- `backend/ssot/lifestyle_registry.yaml`
- `backend/core/analytics/lifestyle_modifier_engine.py`

The alcohol → methylation link is a confirmed missing bridge.

### 4.4 Longitudinal numeric-delta contract gap

This is not a tentative issue.
It is a real architectural gap today.

For benchmark-style prose such as “creatinine 110 → 87”, current snapshot linking is insufficient because prior snapshots preserve only safe status/score metadata, not raw values.

Key evidence:
- `backend/core/analytics/snapshot_linker.py`
- `backend/core/contracts/insight_graph_v1.py`

Sprint N-3 must therefore make an explicit architectural decision:
- either preserve raw prior values in a safe longitudinal contract
- or accept that benchmark-style numeric delta narration remains impossible

### 4.5 No pathway-grade explainer assets

The repo lacks governed pathway-grade prose assets for the benchmark’s strongest explanatory moves, especially:
- methylation / one-carbon metabolism
- lipid transport architecture

Existing signal descriptions and one-line IDL `why_it_matters` fields are not enough.

Key anchors:
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`
- `backend/ssot/retail_explainer_v1/registry.yaml`

### 4.6 No functional interpretation and confidence narrative layer

The repo can structure evidence, confidence, missing data, and confirmatory tests.
It cannot yet compile these into benchmark-grade narrative such as:
- “this is not simple deficiency but incomplete pathway efficiency”
- “confidence is moderate because…”
- “what would improve confidence is…”

Key anchors:
- `knowledge_bus/root_cause/hypotheses/hcy_hypotheses_v1.yaml`
- `backend/core/contracts/root_cause_v1.py`

### 4.7 Missing governed interpretation assets for the benchmark

This is no longer a probable gap.
It is a confirmed gap.

The current governed interpretation stack does **not** cleanly provide:
- a methylation-first / homocysteine-macrocytosis interpretation entity
- a protective lipid transport context entity
- a cross-system vascular synthesis entity combining homocysteine and lipid context

Key anchors:
- `knowledge_bus/phenotypes/phenotype_map_v1.yaml`
- `knowledge_bus/interpretation_display_layer_v1/idl_records_v1.yaml`

### 4.8 No retail patient summary compiler

The benchmark makes clear that a patient-facing executive summary is needed as its own asset class.
That asset class does not yet exist.

The repo has biomarker-level educational prose, not a cross-system retail summary layer.

Key anchor:
- `backend/ssot/retail_explainer_v1/registry.yaml`

---

## 5. Merged adjudicated conclusion

The main gap is not raw data.
The main gap is not frontend presentation alone.
The main gap is that HealthIQ does not yet have the deterministic narrative asset and compiler stack needed to turn strong backend intelligence into the kind of pathway-led report captured in the benchmark.

The correct strategic direction is therefore:
1. design the deterministic narrative compiler architecture
2. define the specific governed narrative asset classes it needs
3. patch contract gaps, especially longitudinal raw-value support
4. build the compiler outputs
5. revisit frontend seriously only once those outputs are materially stronger

Thin validation surfacing may continue in parallel where useful.
Major UX polish should wait.

---

## 6. Challenge questions for sprint planning

Any sprint sequence should be challenged against these questions before approval:

1. Does it distinguish clearly between:
   - data/contract gaps
   - governed content gaps
   - compiler gaps
   - display-layer gaps?

2. Does it settle governed interpretation entities before too much explanatory prose and compiler logic is authored around them?

3. Does it make an explicit decision on longitudinal raw-value preservation?

4. Does it define where the narrative compiler lives?
   - extend `report_compiler_v1.py`
   - or create a separate compiler module?

5. Does it define the output contracts?
   - new `NarrativeReportV1`?
   - extension of `ClinicianReportV1` / `ReportV1`?

6. Does it distinguish between content-authoring sprints that can remain docs-only and HIGH-risk compiler/contract sprints that will hit SOP gates?

7. Does it avoid major frontend redesign before deterministic runtime is strong enough?

---

## 7. SOP governance note

This repo operates under SOP v1.3.1.
Several of the proposed narrative sprints will classify as HIGH-risk if they touch core contracts, pipeline assembly, or analytics/compiler code.

In particular, likely HIGH-risk areas include:
- `backend/core/contracts/`
- `backend/core/analytics/`
- `backend/core/pipeline/`

This means sprints such as N-2, N-3, and N-8 are likely to require:
- Claude audit
- GPT architectural review
- dual approval

By contrast, if scoped correctly, some governed content-authoring work under `knowledge_bus/` may qualify as docs/content-only work and avoid unnecessary control-plane friction.

This must be recognised in planning up front.

---

## 8. Recommended sprint series

### Sprint N-1 — Narrative target lock and authority map

Purpose:
Freeze the benchmark narrative as the target-state authority and convert the reverse-engineering work into one approved support matrix.

Outputs:
- approved benchmark narrative authority
- approved merged reverse-engineering matrix
- approved list of missing deterministic asset classes
- naming/authority decisions for new narrative asset classes

This is the strategic lock sprint.

### Sprint N-2 — Narrative compiler architecture design

Purpose:
Design the deterministic narrative compiler architecture before any major implementation work begins.

This sprint must explicitly answer:
- does the new compiler extend `backend/core/analytics/report_compiler_v1.py` or live separately?
- what is the output contract called?
- how does it relate to `ReportV1` and `ClinicianReportV1`?
- what inputs does it consume from root cause, cluster/system burden, longitudinal state, lifestyle context, and governed narrative assets?
- what sections are in v1 scope versus later scope?

This is the master architecture sprint.

Likely risk classification:
HIGH, if architecture decisions touch compiler and contract authority.

### Sprint N-3 — Longitudinal contract upgrade

Purpose:
Resolve the longitudinal contract gap decisively.

This sprint must explicitly decide whether HealthIQ will preserve raw prior/current values in a safe longitudinal contract.
If yes, implement the contract support needed for benchmark-style numeric delta narration.
If no, formally limit benchmark ambitions in that domain.

Likely scope:
- raw-value preservation decision
- longitudinal contract extension
- numeric delta support
- persistence / improvement support
- deterministic longitudinal prose inputs

Likely risk classification:
HIGH.

### Sprint N-4 — Lifestyle-to-interpretation bridge assets

Purpose:
Create governed deterministic joins from questionnaire/lifestyle context into interpretation logic.

Likely first targets:
- alcohol → methylation / macrocytosis / homocysteine context
- hydration → renal interpretation context
- weight loss / fasting → glycaemic improvement context

This is the first sprint that makes collected lifestyle context narratively useful.

### Sprint N-5a — Governed interpretation entity extensions

Purpose:
Define the new governed interpretation entities required by the benchmark before broader explainer/compiler work is authored.

Likely first assets:
- methylation / homocysteine / macrocytosis entity
- protective lipid transport context entity
- optional cross-system vascular synthesis entity

This sprint may touch:
- phenotype map
- IDL records
- root-cause/hypothesis alignment

This is intentionally earlier than in the prior draft to avoid building explainers and compiler logic against unsettled target entities.

### Sprint N-5b — Pathway explainer asset pack v1

Purpose:
Author governed pathway-grade explainer assets for the first benchmark domains, once the core entities are settled.

Likely first assets:
- methylation / one-carbon metabolism
- lipid transport / cholesterol handling
- additional system explainers only if clearly needed

These should be deterministic source assets, not frontend prose.

### Sprint N-6 — Functional interpretation, confidence, and monitoring assets

Purpose:
Build governed assets for:
- functional reading labels
- “why this matters beyond itself”
- confidence / uncertainty phrasing
- clarification / confirmatory logic narrative
- monitoring / resolution criteria

This is where the report begins to sound intelligent rather than merely structured.

### Sprint N-7 — Deterministic retail and clinician summary assets

Purpose:
Define and author the summary-layer assets that sit above and below the full narrative.

Likely outputs:
- patient-facing summary compiler inputs
- richer clinician synthesis inputs
- hierarchy / so-what / what-to-do-next assets

This should remain downstream of N-2 and N-5a/N-5b so that summaries are built on settled entities and explanation assets.

### Sprint N-8 — Deterministic narrative compiler implementation v1

Purpose:
Implement the first real deterministic narrative compiler using the new asset stack.

Likely outputs:
- body overview block
- lead pathway narrative
- secondary pattern narrative
- longitudinal section
- practical next-steps section
- patient summary output
- richer clinician synthesis output

N-8 must not begin full implementation until the required schema/entity decisions from N-2 and N-5a are settled.

Likely risk classification:
HIGH.

### Sprint N-9 — AB benchmark runtime validation

Purpose:
Run the AB benchmark end to end and compare real deterministic output against the saved benchmark narrative.

Outputs:
- supportability review
- narrative misses and logic misses
- residual missing asset list
- decision on whether output is strong enough for controlled surfacing

### Sprint N-10 — Frontend re-entry and narrative surfacing

Purpose:
Re-enter the frontend seriously only after deterministic runtime outputs are materially stronger.

Important clarification:
This does **not** forbid all frontend work before N-10.
Thin validation surfacing and bounded contract checks may continue in parallel where useful.

What is deferred is major UX polish or major journey redesign.
That should wait until the deterministic runtime can support it properly.

---

## 9. Immediate practical recommendation

The next move is:
1. approve this strategy as the planning authority
2. use it to author the first strategic work package around N-1 and N-2
3. treat N-3 as an explicit contract decision sprint, not a vague future clean-up
4. ensure all future sprint briefs are repo-grounded and SOP-aware from the start

---

## 10. Final statement

HealthIQ now has enough evidence to stop treating the narrative problem as a vague frontend or writing problem.

The work ahead is clear:
HealthIQ must build a deterministic narrative support stack.

That means:
- stronger governed interpretation entities
- richer governed narrative assets
- explicit longitudinal contract support
- deterministic compiler layers
- and only then serious frontend narrative surfacing

That is the correct path from the current backend to a world-class deterministic blood-analysis experience.
