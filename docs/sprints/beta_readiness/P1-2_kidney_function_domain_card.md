# P1-2 — Kidney Function Domain Card

## 1. Summary

Implemented the first missing launch-core domain — **kidney function** — as a bounded Wave 1 consumer domain row (`wave1_kidney`) with compiled subsystem evidence, scoring-rail integration, and non-diagnostic narrative copy.

**Implemented:**
- Compiled card evidence: `wave1_ren_glomerular_filtration`
- Domain assembler wiring in `domain_score_assembler.py`
- Subsystem evidence routing in `wave1_subsystem_evidence.py`
- Kidney narrative helpers in `domain_narrative_wave1.py`
- Scoring policy: eGFR `low_only_concern` directionality retained; eGFR system scoring deferred (audit correction)
- Targeted unit/regression tests

**Out of scope (per sprint):**
- ACR/UACR standalone signal activation
- Urea signal launch visibility (frame-index not adjudicated)
- Frontend changes
- Gemini / Layer C medical reasoning
- Pass 3 promotion or KB package changes
- Full kidney prose/pathway explainer estate (P2 carry-forward)

## 2. P1-1 evidence used

- P1-1 recommended kidney function as first P1-2 domain (bounded scope, active eGFR/creatinine signals, tested collision model)
- Used existing packages: kb52c creatinine, kb47 eGFR, kb52c urea (optional confidence only)
- Reused retail explainer non-diagnostic framing for creatinine/eGFR
- IDL pattern: `ph_renal_stress_v1`

## 3. Runtime changes

| Area | Change |
|---|---|
| `knowledge_bus/compiled/` | Kidney filtration card YAML + compile manifest; estate index entry |
| `health_system_card_evidence.py` | Register `wave1_ren_glomerular_filtration` subsystem |
| `wave1_subsystem_evidence.py` | Add `wave1_kidney` domain order |
| `domain_score_assembler.py` | Fourth domain block; egfr/creatinine signal collection; exclude urea signals from launch-visible active list |
| `domain_narrative_wave1.py` | Kidney headline, contributor, consequence, confidence, next-step copy |
| `scoring_policy.yaml` | Kidney system biomarkers unchanged (`creatinine`, `urea`); eGFR scoring bands removed post-audit; eGFR directionality retained |
| `persisted_replay_contract_v1.py` | Add `wave1_kidney` to Wave 1 domain id set |
| Tests | `test_p1_2_kidney_domain_card.py`; updates to assembler and UX1C regression tests |

## 4. Safety boundaries

- Non-diagnostic wording throughout (no CKD staging, no “you have kidney disease”)
- Lab-provided reference ranges remain authoritative via existing scoring engine rules
- Urea signals excluded from `active_signal_ids` pending medical frame adjudication
- No Gemini, no frontend inference, no fallback parser logic

## 5. Tests and validation

**Commands run:**
```powershell
python -m pytest backend/tests/unit/test_p1_2_kidney_domain_card.py backend/tests/unit/test_domain_score_assembler_v1.py backend/tests/regression/test_domain_ux1c_governed_subsystem_evidence.py backend/tests/regression/test_signal_authority_collision_enforcement.py -q
```

**Result:** All targeted tests passed after compile-status validation fix.

**Not run in this session:** Full golden gate (invoked at kernel finish).

## 6. Carry-forwards

- **P2 prose:** urea and uacr retail explainers; dedicated renal pathway explainer
- **P3 safety:** urea medical frame index; legacy s24 creatinine medical review; ACR package decision
- **P5 UX:** frontend Wave 1 card rendering for fourth domain (render-only; no new medical logic)
- **Next domain:** P1-3 blood/iron/oxygen or P1-4 thyroid per programme sequencing
