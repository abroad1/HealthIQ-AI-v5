# P2-2+P2-3 — Retail and Pathway Explainer Expansion

**Work ID:** P2-2+P2-3  
**Date closed:** 2026-06-27

## 1. Start state

Retail registry held 17 biomarker entries. Pathway pack held 4 domains (homocysteine, lipid, iron, thyroid). No missing-marker explainer pack existed.

## 2. Registry paths confirmed

* Retail: `backend/ssot/retail_explainer_v1/registry.yaml`
* Pathway: `knowledge_bus/pathway_explainers_v1/pathway_explainers_v1.yaml`
* Missing-marker (new): `knowledge_bus/missing_marker_explainers_v1/missing_marker_explainers_v1.yaml`

## 3. Retail explainer expansion result

Added 23 Wave 1 priority biomarkers (iron, thyroid, kidney, homocysteine, inflammation, liver, electrolytes). Total biomarker coverage: **40**.

## 4. Pathway / missing-marker result

Added `renal_filtration_handling_v1` pathway. Bootstrapped missing-marker pack with six cautionary entries for iron, thyroid, renal, and homocysteine contexts.

## 5. Validation result

Retail SSOT gate, pathway schema tests, missing-marker tests, and P2-2+P2-3 sprint tests pass. P1-26 M1 iron `signal_library.yaml` package_id headers corrected (3 files).

## 6. Carry-forwards

See `P2-2_P2-3_carry_forward.yaml`. P2-FRAME-ROUTING, P2-4, Gemini, TSAT, WBC remain deferred/blocked.

## 7. Recommended next sprint

P2-FRAME-ROUTING-ARCHITECTURE-1 or continued retail coverage expansion toward full panel breadth per programme register.
