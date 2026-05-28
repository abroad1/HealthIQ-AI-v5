# Post DOMAIN-LABEL1 Health Systems Card UAT — bb695d3c

**Auditor:** Cursor (browser + API DTO cross-check)  
**Scope:** Health Systems Card section only — investigate/report only, no code changes  
**Analysis:** `bb695d3c-453e-4e49-abff-ae80587b4248`  
**Git:** `main` @ `caf64cf`

---

## 1. Executive verdict

| Metric | Score |
|--------|-------|
| **Overall quality** | **7 / 10** |
| **“Wow” factor** | **5.5 / 10** |
| **Verdict** | **PASS WITH RESERVATIONS** |

The Health Systems Card section is a real product feature now, not a buried report extract. Collapsed cards communicate system name, plain-English descriptor, score ring, band, reliability, evidence completeness, and a headline read. Expanded cards deliver subsystem evidence chains with governed marker labels (HbA1c, CRP, LDL/HDL, TC:HDL ratio, Total Bilirubin) and explicit **Not uploaded** missing-marker chips. DOMAIN-UX1D + DOMAIN-LABEL1 deliver on the evidence-transparency scaffold.

It is not yet “wow.” Blood sugar shows **100 / 100 · Strong** alongside **Limited reliability** and **1 of 3 expected markers included** — the biggest trust risk on this panel. Copy is still compiler-flat in places (liver “Why this score”, generic “Based mainly on…” anchors). Source traces are suppressed in UI. Expanded cards repeat the descriptor and read as prose-heavy compared to the discussion doc’s “prose-light” ideal. The section proves HealthIQ is more than a biomarker table, but not yet at premium commercial bar.

---

## 2. Browser/session method

| Step | Result |
|------|--------|
| Login page opened first | Yes — navigated to `http://localhost:3000/login` (redirected to dashboard when session cold) |
| Login completed | Yes — `test-user3@example.com`; **Log out** visible after session established |
| Target URL opened after auth | Yes — `http://localhost:3000/results?analysis_id=bb695d3c-453e-4e49-abff-ae80587b4248` |
| Page fully loaded before inspection | Yes — after auth token available; initial browser fetch failed (`Failed to fetch`); retried after session token set; full journey rendered (**425** a11y refs, 77 markers) |
| Branch/SHA | `main` @ `caf64cf` |
| Cross-check | Authenticated API GET confirmed DTO matches rendered card text |

**Note:** First results load failed due to missing browser auth cookie; inspection deferred until session stable, per procedure.

---

## 3. Section placement and first impression

**Placement:** `Your health systems` sits in the main retail journey **after** “What’s working well” and **before** “Primary finding and why” (`page.tsx` embed with `embedInJourney`).

**First impression:** The section feels **appropriately important** — it is no longer buried in supplementary “Health domains.” The h2 **Your health systems** plus intro copy frames the feature clearly:

> How three focus areas look on your panel — scores from your markers, not a diagnosis. Open a card for detail.

On the audit viewport the three cards stack vertically (single column). On wider breakpoints the component uses a 3-column grid. The section reads as a **dedicated product module**, not a clinician appendix. It competes visually with the primary-finding block below rather than feeling like an afterthought.

---

## 4. Collapsed card audit

| Card | Score/status | Reliability | Evidence completeness | First impression | Issues |
|------|--------------|-------------|----------------------|------------------|--------|
| **Cardiovascular health** | **86 / 100** · **Strong** | **Good reliability** | **5 of 5** expected markers included | Confident, complete-evidence card; descriptor + “Based mainly on: Vascular Inflammation Risk” adds specificity | Headline prose is long and cautious; “not a simple all-clear” may feel alarmist on an 86 Strong card |
| **Blood sugar control** | **100 / 100** · **Strong** | **Limited reliability** | **1 of 3** expected markers included | Visually dominant perfect score; amber “Limited marker coverage on this panel” present | **Misleading juxtaposition:** 100/100 Strong overpowering limited reliability and 1/3 completeness |
| **Liver health** | **73 / 100** · **Stable** | **Limited reliability** | **1 of 2** expected markers included | Appropriately muted ring; limited-coverage hint visible | Domain completeness **1 of 2** feels at odds with many included markers in expanded view (confusing rollup) |

**Shared collapsed elements (all three):**
- Plain-English descriptor (e.g. `Heart, arteries and circulation`)
- Evidence anchor line (`Based mainly on: …`)
- Score ring + band label
- Coverage panel: Score reliability + Evidence completeness
- Headline sentence under metrics

**Insufficient-data state:** Not triggered on this panel (all cards have `numerator > 0`). Zero-evidence behaviour not observed live; code path exists (`Not enough data`).

---

## 5. Expanded card audit

| Card | Subsystems visible? | Included markers visible? | Missing markers visible? | Label quality | Evidence chain clarity | Issues |
|------|---------------------|---------------------------|--------------------------|---------------|------------------------|--------|
| **Cardiovascular** | Yes — Lipid transport; Homocysteine pathway; Vascular strain context | Yes — HDL Cholesterol, LDL Cholesterol, TC:HDL ratio, Total Cholesterol, Triglycerides, Homocysteine, CRP | None (full coverage) | **Good** — consumer-safe governed labels | Clear subsystem → marker grouping | No source trace visible (filtered); descriptor duplicated; no subsystem status chips |
| **Blood sugar** | Yes — Glycaemic control; Insulin and metabolic context | HbA1c; Triglycerides | Glucose **Not uploaded**; Insulin **Not uploaded** | **Good** — HbA1c, Glucose, Insulin, Triglycerides | Missing markers clearly separated from included | 100/100 vs missing glucose/insulin undermines trust; expanded prose repeats descriptor |
| **Liver** | Yes — Liver enzyme pattern; Liver processing context | ALT, GGT, Albumin, ALP, Bilirubin | AST **Not uploaded**; Total Bilirubin **Not uploaded** | **Good** — Total Bilirubin fix confirmed | Subsystems show breadth; domain “1 of 2” vs many included markers is confusing | **Weak “Why this score”** copy; confidence text mentions GGT/ALP/albumin as missing though they appear included; caveat_flags paragraph is dense |

**Expanded structure (all cards):** Why this score · Confidence · What this may mean · What to do next · Evidence by subsystem (with INCLUDED / MISSING MARKERS chips).

---

## 6. Copy audit

| Visible text | Location | Assessment | Recommended action |
|--------------|----------|------------|-------------------|
| `How three focus areas look on your panel — scores from your markers, not a diagnosis. Open a card for detail.` | Section intro | **Strong** — sets evidence-built framing | Keep |
| `Heart, arteries and circulation` | CV collapsed descriptor | **Strong** — plain English | Keep |
| `Based mainly on: Vascular Inflammation Risk` | CV evidence anchor | **Strong** — specific, traceable | Extend specificity to BS/Liver where possible |
| `Based mainly on: your blood sugar and metabolic markers from your panel.` | BS evidence anchor | **Weak/generic** — could be any app | Copy refinement sprint |
| `Based mainly on: your liver-related markers from your panel.` | Liver evidence anchor | **Weak/generic** | Copy refinement sprint |
| `Your cardiovascular read on this panel is not a simple all-clear: the leading pattern here still deserves clinical context alongside your numbers.` | CV headline | **Cautious but wordy** | Tighten; balance with 86 Strong |
| `Your blood sugar control looks strong based on your current results.` | BS headline | **Misleading alone** with 100/100 + 1/3 markers | Low-evidence semantics sprint |
| `Limited marker coverage on this panel` | BS/Liver under band | **Strong** — good guardrail | Increase visual weight vs score ring |
| `Limited reliability` | BS/Liver reliability | **Strong** — honest | Pair with stronger score de-emphasis |
| `1 of 3 expected markers included` | BS completeness | **Strong** — transparent | User may not know which 3 — subsystem section helps |
| `HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers.` | BS expanded Why | **Strong** — explains limitation clearly | Keep |
| `Confidence is limited — additional glycaemic markers would strengthen the read.` | BS Confidence | **Strong** | Keep |
| `This pattern is worth following with a clinician in context of your other results.` | Liver Why this score | **Weak/mechanical** — placeholder feel | Copy refinement sprint |
| `Confidence is limited — a fuller liver function panel (including GGT, ALP, albumin) would improve the read.` | Liver Confidence | **Confusing** — GGT, ALP, albumin are included in subsystems | Backend/compiler alignment or copy fix |
| `Only the liver markers available on this panel are used here…` | Liver caveat block | **Too cautious/dense** for consumer card | Shorten or collapse |
| `NOT UPLOADED` | Missing marker chips | **Strong** — clear, not alarming | Keep |
| `EVIDENCE BY SUBSYSTEM` / `INCLUDED MARKERS` / `MISSING MARKERS` | Expanded labels | **Mechanical but clear** | Visual polish — sentence case vs ALL CAPS |

---

## 7. Visual UX audit

| Element | Assessment |
|---------|------------|
| **Score visual** | Premium enough for v1 — indigo ring, bold numeric, band label. **Limited-coverage** cards use lighter ring colour + amber hint; still not enough when score is **100**. |
| **Card layout** | Clean cards, good spacing, descriptor + anchor line hierarchy works. Coverage panel (reliability + completeness) is a trust highlight. |
| **Expanded reveal** | Functional accordion; border-top separation works. Feels **information-dense** — four prose blocks before subsystem chips. |
| **Marker chips** | Included = green; missing = grey + **Not uploaded**. **Clear and not alarming.** |
| **Missing marker state** | Well differentiated from abnormal markers — no red “critical” styling on missing. |
| **Typography** | Consistent slate palette; uppercase micro-labels (`SCORE RELIABILITY`) feel slightly report-like vs premium consumer. |
| **Mobile** | Single-column stack readable; expanded subsystem chips wrap well. Score ring + metrics row should remain legible on narrow screens. |
| **Overall** | **Product feature, not report extract** — but expanded state still prose-heavy vs discussion doc “prose-light” target. |

---

## 8. Label authority verification

**Governed labels observed (expanded subsystems):**

| Marker ID (backend) | Visible label | Verdict |
|---------------------|---------------|---------|
| hba1c | **HbA1c** | ✅ Correct |
| crp | **CRP** | ✅ Correct |
| ldl_cholesterol | **LDL Cholesterol** | ✅ Correct |
| hdl_cholesterol | **HDL Cholesterol** | ✅ Correct |
| tc_hdl_ratio | **TC:HDL ratio** | ✅ Correct |
| total_bilirubin | **Total Bilirubin** | ✅ Correct (DOMAIN-LABEL1 patch verified) |
| homocysteine | **Homocysteine** | ✅ Correct |
| total_cholesterol | **Total Cholesterol** | ✅ Correct |

**Poor labels not found:** No visible `hba1c`, `crp`, `Ldl Cholesterol`, `Hdl Cholesterol`, `Tc Hdl Ratio`, or raw `total_bilirubin` in Health Systems Card chips.

**Source trace:** Backend emits values like `wave1_subsystem_evidence_v1:wave1_cardiovascular:lipid_transport` — **correctly hidden** by frontend consumer-safe filter (contains `_`). Trade-off: less literal “source trace” visibility for users.

---

## 9. Misleading-state check

| Risk | Present on bb695d3c? | Evidence |
|------|----------------------|----------|
| **0 / 100 when no evidence** | **No** | All numerators ≥ 1 |
| **Needs attention for missing evidence** | **No** | Missing markers use **Not uploaded**, not alarm bands |
| **100 / 100 with low completeness** | **Yes — Blood sugar** | 100 Strong + Limited reliability + 1/3 markers |
| **Score visual overpowering reliability warning** | **Yes — Blood sugar** | Large 100 ring dominates; amber hint is secondary |
| **Missing markers look abnormal** | **No** | Grey chips, explicit Not uploaded |
| **Subsystem evidence over-clinical** | **Low risk** | No fake subsystem status labels; marker names only (no values) |

**Verdict:** One **material misleading state** (blood sugar perfect score vs thin evidence). Cardiovascular and liver partial-evidence handling is **directionally honest** but liver completeness rollup vs subsystem detail may confuse.

---

## 10. USP expression

**Does the section show HealthIQ scores are evidence-built?**

| USP element | Visible? | Notes |
|-------------|----------|-------|
| System-level score/status | ✅ | Ring + Strong/Stable band |
| Evidence completeness | ✅ | “X of Y expected markers included” |
| Score reliability | ✅ | Good / Limited reliability |
| Included markers | ✅ | Green chips per subsystem |
| Missing markers | ✅ | Grey + Not uploaded |
| Subsystem evidence chain | ✅ | Evidence by subsystem sections |
| Not opinion-generated | **Partially** | Intro copy states “scores from your markers”; subsystem chips prove it; prose blocks still feel compiler-generated |

**Conclusion:** The cards **do** demonstrate HealthIQ is more than a high/low biomarker table — especially in expanded subsystem view. They **do not yet fully sell** the differentiation in collapsed state for partial-evidence domains because the score ring still reads like a fitness app grade.

---

## 11. Recommended next action

**Run a low-evidence semantics sprint** (frontend presentation + copy rules for partial/zero evidence — e.g. cap or de-emphasise score ring when `confidence_tier === 'low'` or `numerator < denominator`; headline must not say “looks strong” at 100/100 with 1/3 markers).

**Why not other options first:**

| Option | Why not first |
|--------|----------------|
| Proceed to next planned sprint | Blood sugar misleading state is a trust defect |
| Visual polish only | Polish won’t fix 100/100 + limited reliability |
| Copy sprint alone | Needs interaction rules, not just words |
| Label/data bug patch | Labels are fixed on this panel |
| PATTERN-C1 | Out of scope for Health Systems Cards |

Follow with a **copy/prose refinement sprint** for liver Why-this-score, generic evidence anchors, and confidence/caveat contradictions.

---

## 12. Prioritised issue list

| Priority | Issue | Severity | Fix type | Suggested sprint |
|----------|-------|----------|----------|------------------|
| **Must fix** | Blood sugar **100/100 Strong** with **Limited reliability** and **1/3** markers — headline says “looks strong” | High | Low-evidence semantics (presentation rules) | Low-evidence semantics sprint |
| **Must fix** | Score ring visually dominates reliability/completeness warnings on partial-evidence cards | High | Visual hierarchy / score de-emphasis when `limitedCoverage` | Low-evidence semantics sprint |
| **Should fix soon** | Liver **Why this score**: `This pattern is worth following with a clinician in context of your other results.` — generic | Medium | Copy/compiler prose | Copy refinement sprint |
| **Should fix soon** | Liver confidence mentions GGT/ALP/albumin as needed though they appear in included markers | Medium | Compiler/copy alignment | Copy refinement sprint |
| **Should fix soon** | Domain evidence completeness (1/2, 1/3) vs richer subsystem marker lists — user may not understand rollup | Medium | UX copy explainer or label tweak | Low-evidence semantics or copy sprint |
| **Should fix soon** | Expanded card repeats plain-English descriptor immediately after collapse | Low | Frontend dedup | Visual polish / small FE fix |
| **Should fix soon** | Generic evidence anchors on BS/Liver (`Based mainly on: your … markers from your panel`) | Medium | Copy refinement | Copy sprint |
| **Can defer** | Source trace hidden (underscore filter) — reduces power-user transparency | Low | Governed consumer-safe trace format | Backend + frontend trace sprint |
| **Can defer** | No marker values/units in subsystem chips (DOMAIN-UX1D Option B) | Low | Planned backlog | DOMAIN-UX2 or later |
| **Can defer** | No subsystem `status_label` badges | Low | When backend emits | Future DOMAIN sprint |
| **Can defer** | ALL CAPS micro-labels (`SCORE RELIABILITY`) feel clinical | Low | Typography polish | Visual polish sprint |
| **Can defer** | CV headline overly cautious for 86 Strong | Low | Compiler tone | Copy sprint |

---

*Investigation complete. No repository code modified.*
