# V5 Runtime Authority Integrity — Pre-change Evidence

**Work ID:** `V5-RUNTIME-AUTHORITY-INTEGRITY-1`  
**Branch:** `fix/v5-runtime-authority-integrity-1`  
**Captured before mutation:** 2026-08-08

## 1. Ratified prohibition

`docs/architecture/ARCH-CONV-A_wave2_lipid_gate1_gate2_decision.md` (Gate 1 + Gate 2, 2026-07-28) states:

- Do not create or activate `signal_total_cholesterol_high`
- Do not create or activate `signal_lipid_transport_dysfunction`
- Do not create or activate `signal_apoa1_cardio_risk`

Machine register: `docs/architecture/ARCH-CONV-A_wave2_medical_decision_register.yaml` `blocked_targets:` all three with `status: NOT_AUTHORISED`.

Compiled WHY (partial coverage only): `anthony_decision: NOT_AUTHORISED_WAVE2` on the two `signal_total_cholesterol_high::*` activation keys. ApoA1 cardio-risk and lipid-transport are absent from that register; Wave 2 `blocked_targets` remains the estate-wide explicit prohibition for all three.

## 2. Runtime activation authority (pre-change)

`knowledge_bus/governance/package_runtime_activation_register_v1.yaml` (`activated_frame_count: 177`) contained:

| activation_key | package_id |
|---|---|
| `signal_apoa1_cardio_risk::inv_apoa1_low_cardio_risk` | `pkg_kb45_apoa1_low_cardio_risk` |
| `signal_lipid_transport_dysfunction::KBP-0001` | `KBP-0001` |
| `signal_lipid_transport_dysfunction::inv_transport` | `pkg_lipid_transport` |
| `signal_total_cholesterol_high::inv_total_cholesterol_high_atherogenic_hypercholesterolemia` | `pkg_kb60_total_cholesterol_high_atherogenic_hypercholesterolemia` |
| `signal_total_cholesterol_high::inv_total_cholesterol_high_hdl_dominant_elevation_pattern` | `pkg_kb60_total_cholesterol_high_hdl_dominant_elevation_pattern` |

## 3. Loader path

`SignalRegistry._load` (`backend/core/analytics/signal_evaluator.py`) admits a governed non-launch-critical frame when:

1. package eligibility / provenance checks pass,
2. `frame_runtime_authority_v1` does **not** exclude it (`authority_state == REJECTED` only),
3. `package_activation_register_v1.frame_activation_exclusion_reason` is `None` (key listed in `activated_frames`).

Pre-change reproduction:

```text
loaded_count 183 unique 128
signal_total_cholesterol_high 2 [...]
signal_lipid_transport_dysfunction 2 [...]
signal_apoa1_cardio_risk 1 [...]
```

## 4. Bootstrap / introduction mechanism

`package_runtime_activation_register_v1.yaml` was introduced by ARCH-CONV-E (`a260c53`, 2026-07-31) as an activation boundary bootstrapped from then-current production reachability. Later ARCH-CONV-E3 ratification retained the lipid keys. No cross-check against Wave 2 `blocked_targets` / `NOT_AUTHORISED_WAVE2` was enforced at bootstrap or thereafter.

## 5. Why existing validators missed it

| Mechanism | What it checks | Why lipids leaked |
|---|---|---|
| `frame_runtime_authority_v1` | `authority_state == REJECTED` | Lipids are `LEGACY_RETIRED` / absent, not `REJECTED` |
| `why_authority_v1` | WHICH WHY asset may serve a frame | Explicitly allows WHY-retired signals to still evaluate |
| Day-one architecture validator | Launch/card/PSI/etc. | No cross-check of activation register vs medical `blocked_targets` / `NOT_AUTHORISED*` |
| Medical intelligence sentinel | Pass-3 / governance isolation | Does not reconcile activation prohibitions |

Root gap: missing fail-closed invariant between **explicit activation prohibition** and **runtime activation register**.
