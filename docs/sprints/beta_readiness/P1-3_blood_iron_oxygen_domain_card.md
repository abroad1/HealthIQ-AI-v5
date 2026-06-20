# P1-3 — Blood / Iron / Oxygen Domain Card

## 1. Summary

Implemented the second missing launch-core domain — **blood / iron / oxygen** — as a bounded Wave 1 consumer domain row (`wave1_blood_iron_oxygen`) with compiled subsystem evidence, existing cbc scoring-rail integration, and non-diagnostic narrative copy.

**Implemented:**
- Compiled card evidence: `wave1_bio_oxygen_carrying_capacity`
- Domain assembler wiring in `domain_score_assembler.py`
- Subsystem evidence routing in `wave1_subsystem_evidence.py`
- Blood / iron / oxygen narrative helpers in `domain_narrative_wave1.py`
- Replay contract update in `persisted_replay_contract_v1.py`
- Targeted unit/regression tests

**Out of scope (per sprint):**
- New scoring bands for iron, ferritin, transferrin, RBC indices, B12, or folate
- Launch-visible CBC / iron signal activation (frame adjudication backlog)
- TIBC / UIBC (absent from SSOT)
- Frontend changes
- Gemini / Layer C medical reasoning
- Pass 3 promotion or KB package source changes
- Full blood / iron / oxygen prose/pathway explainer estate (P2 carry-forward)

## 2. P1-1 evidence used

- P1-1 §5.2 confirmed in-scope biomarkers: haemoglobin, haematocrit, ferritin (optional card context), RBC indices in SSOT but without scoring bands
- Existing cbc scoring rail covers haemoglobin and haematocrit only (`scoring_policy.yaml:47-50`)
- P1-2 pattern reused for compiled card + domain assembler + subsystem routing
- KB-S57 blocker report read: no new CBC-family signal activation in this sprint

## 3. Runtime changes

| Area | Change |
|---|---|
| `knowledge_bus/compiled/` | Oxygen-carrying card YAML + compile manifest; estate index entry |
| `health_system_card_evidence.py` | Register `wave1_bio_oxygen_carrying_capacity` subsystem |
| `wave1_subsystem_evidence.py` | Add `wave1_blood_iron_oxygen` domain order |
| `domain_score_assembler.py` | Fifth domain block; empty launch signal allowlist pending adjudication |
| `domain_narrative_wave1.py` | Non-diagnostic blood / iron / oxygen headline, contributor, consequence, next-step copy |
| `persisted_replay_contract_v1.py` | Add `wave1_blood_iron_oxygen` to Wave 1 domain id set |
| `scoring_policy.yaml` | **Unchanged** — reuses existing cbc rail |
| Tests | `test_p1_3_blood_iron_oxygen_domain_card.py`; updates to assembler and UX1C regression tests |

## 4. Safety boundaries

- Non-diagnostic wording throughout (no anaemia, iron deficiency, bleeding, haemochromatosis, or cancer claims)
- Lab-provided reference ranges remain authoritative via existing scoring engine rules
- Blocked / unadjudicated CBC and iron signals excluded from `active_signal_ids` via empty launch allowlist
- WBC / platelet signals excluded from domain signal predicate (not on allowlist)
- No Gemini, no frontend inference, no fallback parser logic

## 5. Tests and validation

**Commands run:**
```powershell
python -m pytest backend/tests/unit/test_p1_3_blood_iron_oxygen_domain_card.py backend/tests/unit/test_p1_2_kidney_domain_card.py backend/tests/unit/test_domain_score_assembler_v1.py backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py backend/tests/regression/test_signal_authority_collision_enforcement.py backend/tests/unit/test_health_system_card_evidence_arch_rt5b.py -q
```

**Result:** Targeted tests passed before kernel finish.

**Full golden gate:** Invoked at kernel finish.

## 6. Carry-forwards

- **P2 prose:** retail explainers for haematocrit, RBC indices, iron, transferrin, B12, folate; dedicated blood/iron/oxygen pathway explainer
- **P3 safety:** CBC tranche signal adjudication; ferritin / haemoglobin frame promotion; iron-deficiency IDL wiring only after medical review
- **P5 UX:** frontend Wave 1 card rendering for fifth domain (render-only; no new medical logic)
- **Scoring:** iron / ferritin / transferrin bands if product requires scored subsystem depth beyond cbc rail
- **Next domain:** P1-4 thyroid / energy regulation per programme sequencing
