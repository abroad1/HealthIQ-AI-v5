# LAUNCH-CORE-2 — Multi-Panel Launch Readiness UAT

**Repo:** `main` @ `6dd54b2` (branch `work/LAUNCH-CORE-2-multi-panel-launch-readiness-uat`)  
**Date:** 2026-05-30  
**Mode:** Investigation only — no production code changes.

---

## 1. Executive verdict

### **PASS WITH RESERVATIONS**

| Layer | Verdict |
|-------|---------|
| **Current code path (fresh analysis)** | **PASS** — validated on `746f2b0a` |
| **Persisted legacy analyses** | **FAIL hygiene** — pre-LC-1 DTOs still served unchanged |
| **ARCH-RT-6 / unit guardrails** | **PASS** |
| **Launch recommendation** | Proceed with Wave 1 card journey **after** defining persisted-result replay or “re-run analysis” policy for existing users |

**Headline:** LAUNCH-CORE-1 fixes are **correct and stable** on analyses produced after merge. Two of three tested panels are **stale persisted snapshots** that still emit old completeness math, legacy subsystem traces, and (on `bb695d3c`) the **`total_bilirubin` false-missing** defect. This is a **replay/persistence gap**, not a regression in current assembly code.

---

## 2. Preflight evidence

### Baseline (before kernel start)

| Check | Result |
|-------|--------|
| Branch | `main` @ `48b078b` == `origin/main` |
| LAUNCH-CORE-1 merged | Yes (`b35d195`, `48b078b`) |
| Stash list | **Empty** — no governed stash triage required |
| Working tree (initial) | Dirty: LC-1B audit docs (untracked) + LC-2 bus activation (modified) |
| Resolution | Committed LC-1B deliverables + LC-2 activation on `main`; created work branch |

### Kernel

| Step | Result |
|------|--------|
| `run_work_package.py start` | **OK** — token written |
| Active `work_id` | `LAUNCH-CORE-2_multi_panel_launch_readiness_uat` |
| Branch | `work/LAUNCH-CORE-2-multi-panel-launch-readiness-uat` |

---

## 3. Analyses tested

| Analysis ID | Created (UTC) | Panel biomarkers | Persistence era | Role in audit |
|-------------|---------------|------------------|-----------------|---------------|
| `746f2b0a-b470-4d87-8ed8-e2c3d1e68c02` | 2026-05-30 11:42 | 79 | **Post-LC-1** | Primary PASS reference |
| `18e14232-9f93-45e6-820c-004ab5a16235` | 2026-05-30 10:55 | 79 | Post–compiled-cards, **pre-LC-1 completeness** | Stale completeness mismatch |
| `bb695d3c-453e-4e49-abff-ae80587b4248` | 2026-05-27 17:34 | 79 | **Pre-ARCH-RT / pre-LC-1** | Legacy DTO + false-missing bilirubin |

All three are accessible via API and browser for `test-user3@example.com`.

---

## 4. Screenshots

| File | Analysis | Content |
|------|----------|---------|
| `docs/audit-papers/assets/lc2-746f2b0a-health-systems.png` | `746f2b0a` | Results journey header (post-LC-1 reference panel) |
| `docs/audit-papers/assets/lc2-bb695d3c-stale-panel.png` | `bb695d3c` | Results journey header (legacy persisted panel) |

Browser-expanded card verification for `746f2b0a` (accessibility/DOM):

- Completeness: **7/7**, **2/4**, **5/6**
- Hero: **“Raised homocysteine pattern”** (no HEC)
- MCV: **“(related markers: MCV)”**
- Role chips: **“Used in this score”**, **“Supports confidence”**, **“Context marker”**
- Score qualification: **“Score based on available markers”**
- No mojibake (`â`) in rendered body text

---

## 5. Console and network

| Finding | Result |
|---------|--------|
| Console errors/warnings | **None** observed across tested pages |
| `GET /api/analysis/result` | 200 for all three IDs |
| Forbidden DOM tokens (`signal_*`, `pkg_*`, raw `score_contributor`, HEC, `compile_manifest`, etc.) | **Not visible** on `746f2b0a` |

---

## 6. Card completeness table (API DTO)

### 6.1 Post-LC-1 reference — `746f2b0a` ✅

| Domain | Card summary | Subsystem union | Match? |
|--------|--------------|-----------------|--------|
| Cardiovascular | **7 / 7** | 7 included / 7 expected | **Yes** |
| Blood sugar | **2 / 4** | 2 included / 4 expected | **Yes** |
| Liver | **5 / 6** | 5 included / 6 expected | **Yes** |

### 6.2 Stale — `18e14232` ⚠️

| Domain | Card summary (stale rail) | Subsystem union (current schema in payload) | Match? |
|--------|---------------------------|---------------------------------------------|--------|
| Cardiovascular | **5 / 5** | 7 / 7 | **No** |
| Blood sugar | **1 / 3** | 2 / 4 | **No** |
| Liver | **1 / 2** | 5 / 6 | **No** |

Compiled card evidence **is** present (`health_system_card_evidence_v1:` traces); bilirubin **not** falsely missing.

### 6.3 Legacy — `bb695d3c` ⚠️ / ❌

| Domain | Card summary (stale) | Subsystem union | Match? |
|--------|----------------------|-----------------|--------|
| Cardiovascular | **5 / 5** | 7 / 7 | **No** |
| Blood sugar | **1 / 3** | 2 / 4 | **No** |
| Liver | **1 / 2** | 5 / **7** | **No** |

Legacy `wave1_subsystem_evidence_v1:` traces (not compiled). **`total_bilirubin`** falsely missing while **`bilirubin`** scored.

---

## 7. Subsystem included/missing detail

### `746f2b0a` — all domains consistent

**Blood sugar (2/4):** HbA1c ✓, Triglycerides ✓ | Glucose ✗, Insulin ✗ (true absences)  
**Liver (5/6):** ALT, GGT, ALP, Albumin, Bilirubin ✓ | AST ✗ (true absence)  
**CV (7/7):** all lipid + homocysteine + CRP ✓

### `bb695d3c` — legacy liver processing

**Liver processing context:** included `albumin`, `alp`, `bilirubin` | missing **`total_bilirubin`**  
→ **False missing** (bilirubin present at 17 µmol/L). API `missing_markers` label: **“Total Bilirubin”**.

---

## 8. LAUNCH-CORE-1 fix checklist (on `746f2b0a`)

| Check | Result |
|-------|--------|
| Completeness aligns with expanded subsystems | **PASS** |
| Consumer-safe role chips | **PASS** |
| No visible “Homocysteine Elevation Context” | **PASS** (scrubbed → “Raised homocysteine pattern”) |
| MCV as `MCV` | **PASS** |
| No visible mojibake | **PASS** |
| Score qualification when limited | **PASS** |
| All 7 subsystems compiled card evidence | **PASS** |
| No internal IDs/traces visible | **PASS** |
| `total_bilirubin` not falsely missing | **PASS** |

---

## 9. False-missing marker check

| Analysis | False missing found? | Detail |
|----------|---------------------|--------|
| `746f2b0a` | **No** | All missing markers genuinely absent from panel |
| `18e14232` | **No** | Same panel as `746f2b0a`; bilirubin canonical |
| `bb695d3c` | **Yes** | `total_bilirubin` missing while `bilirubin` present — **legacy persisted DTO only** |

**Classification:** Blocker for **stale record display**; **not** a blocker for **new analysis runs**.

---

## 10. Internal ID / copy visibility

| Issue | Visible on `746f2b0a`? | In API payload? | Severity |
|-------|------------------------|-----------------|----------|
| Raw `marker_role` enums | **No** | Yes (DTO) | — |
| “Homocysteine Elevation Context” | **No** | Yes (narrative/clinician) | Post-launch hygiene |
| “Vascular Inflammation Risk” anchor | **Yes** | Yes | Launch polish |
| “Strong Signal” severity chip | **Yes** | Yes | Launch polish |
| `source_trace` / `compile_manifest_ref` | **No** | Yes | — |
| Mojibake in rendered body | **No** | Some fields in stale payloads | Post-launch hygiene |

---

## 11. Defects and severity

| ID | Defect | Severity | Layer | Recommendation |
|----|--------|----------|-------|----------------|
| D1 | Persisted pre-LC-1 analyses serve stale completeness (1/3 vs 2/4) | **launch polish** (existing users) | Persistence / replay | **Fix before launch:** replay or re-run policy |
| D2 | `bb695d3c` false-missing `total_bilirubin` | **blocker** (for that record) | Stale persisted DTO | Same replay policy; not a code fix in this sprint |
| D3 | “Vascular Inflammation Risk” reads internal | launch polish | DTO / copy deck | Post-launch or copy sprint |
| D4 | “Strong Signal” mechanical badge | launch polish | Frontend rendering | Product decision |
| D5 | Raw HEC / mojibake in API not UI | post-launch hygiene | Backend narrative persist | Recompile / encoding fix |
| D6 | 100/100 blood sugar with 2/4 markers | needs product decision | Scoring semantics | Already partially mitigated by qualification line |

---

## 12. Validators and tests

| Command | Result |
|---------|--------|
| `python backend/scripts/validate_day_one_architecture.py` | **PASS** |
| `pytest backend/tests/architecture/test_day_one_architecture_guardrails.py -q` | **4 passed** |
| `pytest backend/tests/unit/test_launch_core1_card_coherence.py -q` | **2 passed** |
| `npm test tests/lib/cardEvidenceConsumerCopy.test.ts tests/lib/retailNarrativeSanitize.test.ts` | **8 passed** |

---

## 13. API payload fields involved

| Field | Notes |
|-------|-------|
| `consumer_domain_scores[].evidence_completeness_*` | LC-1 subsystem union on fresh runs only |
| `consumer_domain_scores[].subsystems[]` | Included/missing + compiled `source_trace` |
| `narrative_report_v1`, `clinician_report_v1` | Raw compiler strings (FE-scrubbed) |
| `created_at` | Determines stale vs fresh DTO era |

Runtime inspection payloads (not committed): `automation_bus/_lc2_*.json`

---

## 14. Recommended next actions

| Priority | Action | Owner |
|----------|--------|-------|
| **P0** | Define and execute **persisted-result replay** (or user re-run) so pre-LC-1 analyses get refreshed DTOs | Backend / ops |
| **P1** | Document in launch notes: “Results viewed before [date] may show outdated marker counts” | Product |
| **P2** | Plain-language cardiovascular anchor copy | Copy / DTO |
| **P3** | Backend narrative compiler retail labels + UTF-8 persist hygiene | Backend assembly |

---

## 15. Launch-readiness recommendation

**Ship the LAUNCH-CORE-1 results-page code path** — it is stable on fresh analyses across the tested 79-marker panel.

**Do not treat multi-panel UAT as all-clear for historical records.** Until replay is resolved, existing users opening analyses like `bb695d3c` or `18e14232` will still see completeness mismatch and (for oldest records) bilirubin false-missing.

**Follow-up before broad launch:** persisted-result refresh strategy (backend replay job or forced re-analysis).

---

## 16. Closure hygiene note

Investigation artefacts under `automation_bus/_lc2_*.json` were used locally and **not committed** (per sprint scope). Only this report and screenshot assets are deliverables.
