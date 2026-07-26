# ARCH-CONV-CORRECT-1 — MCV Frame Co-Service Design

**Work ID:** `ARCH-CONV-CORRECT-1`
**Branch:** `feature/arch-conv-correct-1-e2e-authority-layerc`
**Workstream:** WS3
**Family:** `signal_mcv_high`

---

## 1. Problem restated

Three MCV frames could fire and serve WHY simultaneously on one panel:

```text
signal_mcv_high::inv_mcv_high_macrocytosis                      (anchor)
signal_mcv_high::inv_mcv_high_megaloblastic_macrocytosis        (specific)
signal_mcv_high::inv_mcv_high_nonmegaloblastic_macrocytosis     (specific)
```

On the audited live case that produced anchor + megaloblastic + non-megaloblastic WHY at once,
including a hepatic/alcohol differential while GGT and ALT were both in range.

## 2. What the ratified pack already decided

No new medical policy was created. The rules below are transcriptions of Gate C dispositions
in `docs/Medical Research Documents/HEALTHIQ_AI_V5_WHY_PILOT_CONSOLIDATED_MEDICAL_REVIEW.md`:

| Frame | Ratified disposition | Rule implemented |
|---|---|---|
| 5 — anchor | Non-specific morphology anchor or fallback only; no cause may be ranked from MCV alone; must not duplicate WHY when a specific frame is supported | Anchor serves `morphology_context` only, restricted to `mcv_high_anchor_pattern_v1`, and validated against forbidden causal terms |
| 6 — megaloblastic | APPROVE_WITH_REVISIONS — "Require corroborating B12/folate evidence" | Serves causally only when folate, vitamin B12 or active B12 is low/borderline |
| 7 — non-megaloblastic | APPROVE_WITH_REVISIONS — "Require cause-specific evidence gates; no inferred alcohol or marrow diagnosis" | Serves causally only when GGT or ALT is above range |
| Combined pattern | Not present in the pack | Two specific frames may not co-serve; the family falls back to anchor context |

Gate markers are the frames' own governed markers, taken from each package's
`signal_library.yaml` (hematinic markers for Frame 6; the `expected_direction: high`
hepatic differential/corroborator markers for Frame 7).

## 3. Implementation

### Policy artefact

```text
knowledge_bus/governance/frame_co_service_policy_v1.yaml
```

Declares, per family: the anchor (with `why_role`, allowed hypothesis IDs and forbidden causal
terms), each specific frame with its `evidence_gate`, `combined_pattern_authorised: false`, and
the resolution table. Each rule records its `ratified_basis`.

### Resolver

```text
backend/core/knowledge/frame_co_service_v1.py
```

`resolve_family_co_service(...)` returns `{activation_key: SERVE_CAUSAL | SERVE_CONTEXT | SUPPRESS}`.
It fails closed: a malformed or missing policy raises, and unknown or missing evidence is not
treated as support.

### Consumption

`backend/core/analytics/root_cause_compiler_v1.py` resolves the family before compiling
findings, then:

- drops `SUPPRESS` frames entirely (no finding, no hypotheses);
- stamps `why_role` on the emitted finding;
- for a `SERVE_CONTEXT` anchor, asserts the compiled artefact carries only the allowed
  hypothesis ID and no forbidden causal term, raising rather than emitting a causal anchor.

### DTO

`RootCauseFindingV1` gains one additive field, `why_role` (`causal` | `morphology_context`),
which carries the already-governed Layer B decision to Layer C. No medical reasoning moved
into DTO assembly.

## 4. Resolution table

| Panel evidence | Anchor | Megaloblastic | Non-megaloblastic |
|---|---|---|---|
| Neither gate satisfied | `morphology_context` | suppressed | suppressed |
| Hematinic gate only | `morphology_context` | `causal` | suppressed |
| Hepatic gate only | `morphology_context` | suppressed | `causal` |
| Both gates satisfied | `morphology_context` | suppressed | suppressed |

The "both satisfied" row follows Frame 5's ratified fallback role: with no governed combined
pattern, the safe output is morphology context rather than a speculative choice between causes.

## 5. Verified matrix (probe + regression suite)

| Case | Panel delta from the audited UAT panel | Result |
|---|---|---|
| Anchor only | none | anchor `morphology_context`; no causal MCV WHY |
| Megaloblastic supported | `folate = 2.1` | megaloblastic `causal`; anchor context; non-mega suppressed |
| Non-megaloblastic supported | `ggt = 120.0` | non-mega `causal`; anchor context; mega suppressed |
| Ambiguous | `folate = 2.1`, `ggt = 120.0` | anchor context only; no causal MCV WHY |

## 6. Observation recorded, not silently closed

The specific MCV frames still **fire as signals** when MCV is above range, so they remain
visible as ranked rows in `report_v1.top_findings`. Their signal-level interpretation text is
non-causal (Frame 7's reads "High MCV in this pattern is a useful differential clue rather than
a diagnosis on its own"), and after this correction they contribute no causal WHY unless their
ratified evidence gate is satisfied.

Moving the gate from WHY service to signal activation would change activation rules for
approved frames, which STOP Gate A/B explicitly reserves for a separate authorisation. It is
therefore recorded as a limitation in the verification report, not implemented here.

## 7. STOP Gate B assessment

| Condition | Assessment |
|---|---|
| Requires new medical policy beyond the ratified review | **No** — every rule cites a Gate C disposition |
| Specific-frame evidence gates unavailable in Layer B | **No** — gate markers and reference ranges are already in the compiler's context; status is computed with the existing `_marker_status` / `_direction_match` helpers |
| Layer C owns the only suppression mechanism | **No** — suppression is now a Layer B decision, and Layer C receives `why_role` |

Gate B not triggered.
