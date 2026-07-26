# HealthIQ AI v5 — WHY Pilot Medical Review Decision Template

**Work ID:** `ARCH-CONV-GATE2_5`  
**Purpose:** Frame-level field set for the bounded WHY migration pilot (5 signals / 10 frames).  
**Authority note:** Completing medical-review fields is **not** production authorisation. **Anthony** must explicitly ratify before engineering implementation or promotion. GPT review alone is never production authority.

**Folder convention:** `docs/Medical Research Documents/` (repository standard).

**Ratified recording form (2026-07-26):** use **one consolidated five-signal review pack** containing **ten frame-level decisions**. Create separate detailed records only where risk, disagreement, or audit requirements justify them. This template defines the required fields for each frame-level decision inside that pack.

---

## How to use

1. Prefer a single consolidated pilot review pack covering all five signals / ten frames.
2. For each `activation_key`, complete every section below (inline in the pack). Use `NOT_APPLICABLE` where justified.
3. Select exactly one **Production disposition** per frame.
4. Record reviewer as **GPT — HealthIQ AI Head of Medical Research** and the review date.
5. Leave **Human ratification** blank until **Anthony** signs.
6. Do not implement or promote compiled assets until disposition is APPROVE_* (or RETIREMENT_CONFIRMATION_ONLY where applicable) **and** Anthony has explicitly ratified.
7. Create a separate detailed record only if risk, disagreement, or audit requirements require it; otherwise keep the frame decision in the consolidated pack.

Allowed production dispositions:

```text
APPROVE_FOR_COMPILED_PROMOTION
APPROVE_WITH_REVISIONS
REJECT
DEFER_PENDING_RESEARCH
RETIREMENT_CONFIRMATION_ONLY
```

---

## Decision record

### Frame identity

| Field | Value |
|---|---|
| signal_id | |
| activation_key | |
| source_spec_id | |
| package_id | |
| current WHY authority (compiled / legacy) | |
| legacy YAML path | |
| compiled hypothesis path (if any) | |
| work_id / review batch | |

### Medical interpretation

| Field | Value |
|---|---|
| Intended clinical meaning of this frame | |
| Primary marker / direction | |
| Distinguishing features vs peer frames in the same signal family | |
| Non-diagnostic / safety framing required | |

### Evidence summary

| Field | Value |
|---|---|
| Canonical investigation specification | path + status |
| Original source research | path + status |
| Supporting artefacts reviewed | |
| Conflicting evidence | none / describe |

### Causal limits

| Field | Value |
|---|---|
| What this frame may claim | |
| What this frame must not claim | |
| Required supporting / contradiction markers | |

### Consumer wording boundary

| Field | Value |
|---|---|
| Allowed consumer-facing intent | |
| Forbidden consumer wording | |
| Lead-finding eligibility notes | |

### Clinician wording boundary

| Field | Value |
|---|---|
| Allowed clinician / root-cause intent | |
| Forbidden clinician wording | |
| Differential / multi-frame handling notes | |

### Approved hypotheses

| hypothesis_id / statement | evidence basis | notes |
|---|---|---|
| | | |

### Rejected hypotheses

| hypothesis_id / statement | rejection reason |
|---|---|
| | |

### Uncertainty

| Field | Value |
|---|---|
| Residual uncertainty | |
| Whether uncertainty blocks promotion | yes / no |

### Confirmatory-test context

| Field | Value |
|---|---|
| Confirmatory tests / follow-ups that may be mentioned | |
| Tests that must not be recommended here | |

### Modifier compatibility

| Field | Value |
|---|---|
| Required context modifiers | |
| Known incompatible modifiers | |
| Binding status | bound / unbound / not required |

### Legacy-parity assessment

| Field | Value |
|---|---|
| Legacy YAML behaviour preserved / narrowed / superseded | |
| Dual-authority risk if promoted | |
| Retirement implications | |

### Production disposition

| Field | Value |
|---|---|
| Disposition (exactly one) | |
| Conditions / revisions required | |
| Blockers remaining | |

### Reviewer

| Field | Value |
|---|---|
| Reviewer identity | GPT — HealthIQ AI Head of Medical Research |
| Review role | Structured medical review (dual-gate, gate 1) |
| Review date (UTC) | |
| Artefact path for this completed record | Consolidated five-signal pack (or separate detailed record if justified) |

### Human ratification

| Field | Value |
|---|---|
| Human ratifier identity | Anthony |
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Ratification date (UTC) | |
| Notes | Required before any engineering implement/promote |

---

## Operating-model reminder (ratified 2026-07-26)

**Dual-gate:**

1. **Medical review:** GPT as HealthIQ AI Head of Medical Research records structured frame dispositions.
2. **Production ratification:** Anthony must explicitly ratify before engineering may implement or promote.

GPT review alone is never production authorisation.
