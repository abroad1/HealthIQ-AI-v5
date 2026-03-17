# ADR-007 — Clinician Summary Report (Patient-Delivered GP Document)

## Status
Proposed (v1)

## Context
HealthIQ ingests commercial laboratory blood panels and produces deterministic analytical outputs:
- signal results (Layer B)
- interaction chains (Layer B+)
- root cause hypotheses (Layer C compilation)
- intervention/monitoring outputs (separate, patient-facing)

Users commonly bring complex panels to time-constrained GP consultations. The GP has limited time and no familiarity with HealthIQ. A clinician-native summary document, delivered by the patient, can compress interpretation time and improve the quality of clinical discussion.

## Decision
We will produce a Clinician Summary Report (CSR) as a GP-facing document that arrives via the patient.

This CSR is:
- a deterministic renderer of existing pipeline outputs
- written in clinical register
- a structured discussion aid
- not a diagnosis or treatment recommendation

The CSR will not add new clinical reasoning. It will compile and present governed outputs.

## Scope (v1)
- One primary concern per report (derived deterministically).
- Structured page-one summary block (no free prose paragraphs).
- Hypothesis ranking for one or two primary abnormalities (initially homocysteine; expands via KB-S33b+).
- Confirmatory test suggestions with strict suppression when tests are already present in-panel with usable data.
- Full biomarker table appendix with lab ranges and units.

## Non-goals (v1)
- No medication recommendations
- No dosing changes
- No diagnosis confirmation
- No supplement recommendations
- No patient-facing coaching tone
- No frontend logic making clinical selection decisions

## Safety posture
- KB-S31 denylist applies to all CSR text fields.
- Clinician Language Style Guide v1 applies to all CSR text fields.
- Document contains:
  - a 2–3 line governance header (clinical register)
  - a single footer line per page (lightweight)

## Determinism requirements
- CSR must be reproducible for the same input panel and governed knowledge assets.
- All selection decisions (what appears on page one, which hypotheses, which tests) are made by a compiler against deterministic rules.
- Frontend renderer only renders the compiled contract.

## Interfaces / Dependencies
CSR consumes:
- `report_v1` (compiled summary from insight_graph)
- `signal_results`
- `interaction_summary` / `interaction_chains`
- `root_cause_v1` blocks (where present)

CSR does not require LLM inference at runtime.

## Implementation notes
- A Pydantic output contract defines CSR content.
- A compiler populates CSR contract fields from `report_v1` and supporting structures.
- A renderer outputs print-ready HTML/PDF based strictly on CSR contract.

## Rationale
This produces a “GP WOW” moment by providing a credible, fast-to-scan clinical differential and confirmatory test list, while avoiding clinical advice liability. It also drives awareness by organic distribution into clinical settings without direct NHS sales motion.

## Consequences
- Requires stable language and safety governance (style guide + denylist enforcement).
- Requires explicit suppression logic to avoid recommending already-present tests.
- Enables a dedicated frontend sprint (renderer) once enough root cause coverage exists beyond homocysteine.
