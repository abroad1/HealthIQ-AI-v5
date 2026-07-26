# HealthIQ AI v5 — WHY Pilot Medical Review Decision Template

**Work ID:** `ARCH-CONV-GATE2_5`  
**Purpose:** Reusable per-frame medical-review decision record for the bounded WHY migration pilot (5 signals / 10 frames).  
**Authority note:** Completing this template is **not** production authorisation. Human ratification is required before engineering promotion. GPT/agent review alone is never production authority.

**Folder convention:** `docs/Medical Research Documents/` (repository standard).

---

## How to use

1. Copy this template once per `activation_key`.
2. Fill every section. Use `NOT_APPLICABLE` where justified.
3. Select exactly one **Production disposition**.
4. Record reviewer and date.
5. Leave **Human ratification** blank until the named human ratifier signs.
6. Do not promote compiled assets until disposition is APPROVE_* **and** human ratification is complete under the Gate 2.5-ratified operating model.

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
| Reviewer identity | |
| Review role (governance coherence vs clinical sign-off) | |
| Review date (UTC) | |
| Artefact path for this completed record | |

### Human ratification

| Field | Value |
|---|---|
| Human ratifier identity | |
| Ratification decision | APPROVED / REJECTED / DEFERRED |
| Ratification date (UTC) | |
| Notes | |

---

## Operating-model reminder

Until Gate 2.5 condition §2.1 is closed:

- **Model A:** this template may be used for governance coherence review; a separate clinical sign-off step remains mandatory before promotion.
- **Model B:** only if explicitly ratified — GPT/agent may fill the medical sections; human ratification still required for production; GPT review alone is never enough.
