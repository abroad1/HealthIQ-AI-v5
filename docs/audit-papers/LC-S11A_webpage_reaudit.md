# LC-S11A — Webpage-Only Human UAT Re-Audit

**Audit date:** 2026-05-17  
**Auditor:** Claude Code (forensic product/architecture auditor — no code changes)  
**Branch audited:** `launch-core/lc-s11a-trust-blocker-correction`  
**Supersedes:** Previous audit (pre-regeneration, analysis_id `c440dfa2-12a1-4e29-95a5-ee07a2397c59`)

---

## 1. Executive Verdict

**PASS WITH GAPS**

The live webpage on the post-fix regenerated analysis (`e3a1ee79-963e-46a1-afee-58657d1ffb55`) is acceptable for supervised external human testing. Three of the four original trust blockers are fully resolved at the headline level. One blocker (blood sugar) is partially addressed — the original false claim is gone but two residual phrases in the expanded detail contradict the data. One additional item (ApoA1 dial scoring direction) is not surfaced in the main narrative but remains directionally wrong in the advanced biomarker section.

No single remaining issue would cause a reasonable external tester to distrust the platform. However, the blood sugar detail copy ("sustained glycaemic strain") directly contradicts the 100/100 score and should be corrected before wide or unsupervised release.

---

## 2. Page Reviewed

| Field | Value |
|---|---|
| URL | `http://localhost:3000/results?analysis_id=e3a1ee79-963e-46a1-afee-58657d1ffb55` |
| Login used | `test-user3@example.com` |
| Loaded successfully | Yes — full results page rendered, 77 markers |
| Console errors at load | CORS errors from stale Playwright session; resolved by fresh browser login |
| Page title | "Your results" |
| Markers displayed | 77 |
| Analysis origin | Post-fix regenerated analysis (generated after LC-S11A code commits) |

---

## 3. Four Trust Blockers Replay

| # | Blocker | Previous issue | Current webpage evidence | Verdict |
|---|---|---|---|---|
| 1 | Legacy `insights[]` placeholder text | Visible placeholder text "summarise structured signals; review with your clinician" | No placeholder text found anywhere on the page. All sections carry real interpretation content. The insights surface renders live data throughout. | **RESOLVED ✓** |
| 2 | Blood sugar domain unsupported narrative | Page claimed "early impaired sugar and lipid handling" despite no active glycaemic signals | The original false headline claim is gone. Headline now correctly reads "HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers." Score: 100/100 / Limited confidence. However: the card summary text still reads "Your blood sugar and metabolic context still has active signals to address in care planning, even if some results look in range on the surface." And in the expanded detail: "What this may mean: Sustained glycaemic strain raises long-term metabolic and vascular risk." Neither phrase is supported — no glycaemic strain exists on this panel. | **PARTIAL — original claim removed; two residual phrases remain** |
| 3 | ApoA1 directionality | ApoA1 presented as a negative cardiovascular risk driver purely because it was elevated | ApoA1 does not appear in the main narrative, "What's driving this", cardiovascular domain card, or any patient-facing driving-factors section. ApoB/ApoA1 ratio correctly shows 0.4 / 100/100. In the advanced biomarker dials section, ApoA1 (1.7 g/L, range 0.79–1.69 g/L) is scored 28/100 — directionally incorrect for a protective marker that is only marginally above the upper reference range. This score is not surfaced as a cardiovascular driver anywhere on the main page. | **SUBSTANTIALLY RESOLVED in narrative; ApoA1 dial score direction remains wrong in advanced section** |
| 4 | Low ALT liver false alarm | ALT 7 U/L driving 5/100 "Needs review" with MASLD/fibrosis language | Liver card now reads: 77/100 / Stable / Limited confidence. Headline: "Your liver health looks broadly stable based on your current enzyme markers." ALT (7.0 U/L, range 10–49) is scored 77/100 in the biomarker dial — no alarm. The expanded "What this may mean" section carries "Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored" — generic copy not driven by the actual enzyme picture, but this is behind a user-initiated expand and is not the headline. | **RESOLVED at headline; generic boilerplate survives in expanded detail** |

---

## 4. Human UI Observations

### Hero / Primary Finding
- **Heading:** "Homocysteine Elevation Context: warrants attention on this panel"
- **Label:** Primary finding · Strong Signal
- **System context:** Vascular Inflammation Risk
- Homocysteine correctly leads. Phrasing "warrants attention on this panel" is calibrated — neither dismissive nor catastrophising. Trust notice banner is prominent: "Your report is built from structured clinical rules applied to your lab data. AI-personalised narrative is not active in this view."
- **Assessment: Coherent and trustworthy ✓**

### Summary Section
- Centres correctly on Homocysteine Elevation Context (at_risk).
- Secondary note: Methylation pathway pattern (strong signal) — well-framed.
- No placeholder text or mechanical language.
- **Assessment: Coherent ✓**

### What's Driving This
Three drivers listed:
1. Homocysteine 16.23 umol/L · Elevated ✓
2. Total Cholesterol 5.26 mmol/L · Elevated ✓
3. Transferrin 2 g/L · **Critical** ⚠

ApoA1 is absent from this section — the original blocker 3 is resolved here.

The word **Critical** for Transferrin is worth noting. Transferrin is 2.0 g/L against a lower bound of 2.15 g/L (scored 5/100). The "Critical" label will alarm first-time users, though the underlying signal (Transferrin as a supporting marker in the methylation pathway pattern) is correctly contextualised in the deeper sections.

No placeholder text, no raw signal IDs.

### Domain Cards

**Cardiovascular: 88/100 · Strong · High confidence**
- Driven by Vascular Inflammation Risk pattern. No ApoA1 mentioned. Follow-up text sensible.
- Expanded detail is appropriately framed.
- **Assessment: Coherent ✓**

**Blood Sugar: 100/100 · Strong · Limited confidence**
- Headline: "HbA1c is within range on this panel. Glucose and insulin were not included, so a fuller glycaemic read would require those markers." ← Honest ✓
- Score 100/100 with "Limited confidence" ← Appropriate framing ✓
- Card summary: "Your blood sugar and metabolic context still has active signals to address in care planning, even if some results look in range on the surface." ← **Contradicts the 100/100 score and absence of active glycaemic signals.**
- Expanded "Why this score": repeats the honest headline copy ✓
- Expanded "Confidence": "Confidence is limited — additional glycaemic markers would strengthen the read." ✓
- Expanded "What this may mean": **"Sustained glycaemic strain raises long-term metabolic and vascular risk."** ← **Directly contradicts the data. HbA1c is in range; no glycaemic strain is evidenced on this panel.**
- "What would improve confidence" correctly lists glucose and insulin ✓
- **Assessment: Headline honest; detail carries two residual unsupported alarming phrases.**

**Liver: 77/100 · Stable · Limited confidence**
- Headline: "Your liver health looks broadly stable based on your current enzyme markers." ← Appropriate ✓
- Confidence note: "a fuller liver function panel (including GGT, ALP, albumin) would improve the read." ← Appropriate ✓ (Note: GGT 15, ALP 46, albumin 44 are all on the panel and in range — so this confidence caveat may overstate incompleteness, but it is not harmful)
- Expanded "What this may mean": "Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored." ← Generic boilerplate not arising from the data. All liver markers except ALT are normal; ALT being low does not indicate liver strain. Remains a low-visibility issue (behind user-initiated expand).
- **Assessment: Substantially resolved; generic alarming copy survives in expanded detail only.**

### Body Overview
- Lead: Homocysteine Elevation Context (at_risk) · Cardiovascular · 4 biomarkers ✓
- Related systems: Autonomic, Cardiovascular, Hematological, Hepatic, Hormonal, Immune, Metabolic, Musculoskeletal + 3 others — no internal IDs visible ✓
- Pattern group counts: **0 Needs attention / 0 Explore further / 3 Stable**
- The "0 Needs attention" count is visually inconsistent with the lead finding carrying an "at_risk" tag and "Strong Signal" badge. A user who reads both could reasonably ask "if 0 patterns need attention, why does the lead finding say it warrants attention?" This is a UI coherence issue.

### Alcohol / Lifestyle Bridge
- Lifestyle context is acknowledged in next-steps copy: "Review lifestyle context already captured in your questionnaire."
- The explicit alcohol/lifestyle bridge visible in the previous pre-fix analysis ("Your questionnaire suggests moderate alcohol intake, which can be relevant when interpreting homocysteine...") **is not present on this analysis**. It is possible this panel run did not include questionnaire data with an alcohol signal, or the bridge was rendered from questionnaire inputs specific to the previous run.
- The absence of the bridge from this rendered page is notable but cannot be confirmed as a regression without knowing the questionnaire inputs for this analysis_id.

### Patterns Across Your Body
- Methylation pathway pattern — Strong Signal — correct framing ✓
- Supporting markers: Homocysteine, Vitamin B12, Folate, Transferrin ✓

### Long-Form Evidence ("What This Means")
- Primary focus (one-carbon / methylation network): thorough, neutral, clinically appropriate ✓
- Secondary patterns (lipid transport): correctly discusses apoB-rich particle burden — ApoA1 is not invoked as a negative driver ✓
- Confidence framing and clarification paths present throughout ✓
- Technical governance token visible inline: "Confidence framing (governed label): moderate_by_default" — this internal engine label renders in the user-facing long-form text. Not a clinical trust risk but is an internal artefact visible to users.

### Advanced / Biomarker Dials (77 markers)
Key markers:
| Marker | Value | Range | Score | Note |
|---|---|---|---|---|
| Homocysteine | 16.2 µmol/L | 3.7–13.9 | 19 | Correctly low ✓ |
| MCV | 99.5 fL | 80–96 | 19 | Correctly low ✓ |
| Transferrin | 2.0 g/L | 2.15–3.65 | 5 | Below range; consistent with narrative ✓ |
| ALT | 7.0 U/L | 10–49 | 77 | Low but not alarming in dial ✓ |
| ApoA1 | 1.7 g/L | 0.79–1.69 | **28** | Marginally above range; score direction wrong for protective marker ⚠ |
| ApoB/ApoA1 ratio | 0.4 | — | 100 | Reassuring ✓ |
| ApoB | 0.7 g/L | 0.46–1.74 | 98 | ✓ |
| HbA1c | 26 mmol/mol | — | 100 | In range ✓ |
| LDL | 2.8 mmol/L | 2.59–3.34 | 100 | ✓ |
| HDL | 2.2 mmol/L | — | 100 | ✓ |
| Total Cholesterol/HDL ratio | 2.4 | 0–5 | 100 | ✓ |

No raw signal IDs, no sprint tokens, no debug strings visible. Units and labels are sensible throughout.

### Trust / Data Quality Strip
- "Quality checks passed" · "We received 8 of 8 expected markers for this interpretation." ✓

---

## 5. Remaining User Trust Risks

| Severity | Issue |
|---|---|
| **HIGH** | Blood sugar card summary: "Your blood sugar and metabolic context still has active signals to address in care planning, even if some results look in range on the surface." Score is 100/100; HbA1c is in range. This statement implies active concern where none is evidenced. Visible on the collapsed card — no expand required. |
| **HIGH** | Blood sugar expanded "What this may mean": "Sustained glycaemic strain raises long-term metabolic and vascular risk." Directly contradicts the data. Generic boilerplate that should be gated to panels where glycaemic strain is actually evidenced. |
| **MEDIUM** | ApoA1 biomarker dial scored 28/100 for a value 0.01 g/L above the upper reference range on a protective marker. This is directionally wrong — elevated ApoA1 is generally favourable. Visible to any user who opens the advanced section and reviews dials. Does not drive any headline narrative. |
| **MEDIUM** | Body overview pattern count shows "0 Needs attention" while the lead finding carries "at_risk" status and a Strong Signal badge. These are visually inconsistent for users who read both sections. |
| **MEDIUM** | Liver expanded "What this may mean": "Early liver-strain patterns are a key lane toward MASLD/fibrosis risk if ignored." Generic copy not grounded in the actual data (all liver markers except ALT are within range). Behind a user-initiated expand; not a headline risk, but inconsistent with the "broadly stable" framing directly above it. |
| **MEDIUM** | Internal governance label "Confidence framing (governed label): moderate_by_default" renders inline in the user-facing "What this means" long-form text. This is an engine token leaking into user-visible narrative. |
| **LOW** | Transferrin labelled "Critical" in "What's driving this." Factually accurate per the scoring (5/100, below range), but the word "Critical" is disproportionate in context — low Transferrin is contextualised correctly in the methylation pattern detail. |
| **LOW** | Alcohol/lifestyle bridge not visible in this analysis. Cannot confirm regression without knowing questionnaire inputs for this analysis_id; flagged for human verification. |
| **POLISH** | "umol/L" renders instead of "µmol/L" for Homocysteine (micro sign rendering issue — pre-existing). |
| **POLISH** | "What's driving this" lists Total Cholesterol alongside methylation markers without distinguishing which drivers belong to the lead pattern vs. other active signals. |

---

## 6. Final Recommendation

**Approve with follow-up items — conditional pass for supervised external UAT.**

The page is coherent and trustworthy at the headline level. The primary finding (Homocysteine elevation, methylation pathway, vascular risk context) is well-framed. Liver and cardiovascular domains read honestly at the headline. The page is free of placeholder text, raw signal IDs, sprint/debug strings, and ApoA1 false cardiovascular narratives.

**Fix before wide or unsupervised release (HIGH items):**

1. **Blood sugar card summary line:** Replace "Your blood sugar and metabolic context still has active signals to address in care planning, even if some results look in range on the surface" with copy appropriate to the 100/100 / HbA1c-in-range state — e.g. "HbA1c is within range. No active glycaemic signals detected on this panel. Confidence is limited by the absence of glucose and insulin."

2. **Blood sugar expanded "What this may mean":** Replace "Sustained glycaemic strain raises long-term metabolic and vascular risk" with neutral framing that applies only when glycaemic strain is actually evidenced. The current copy implies a condition that does not exist on this panel.

**Follow-up sprints (MEDIUM items — not blocking supervised UAT):**

3. ApoA1 dial scoring direction — evaluate whether the scoring function correctly handles protective markers that sit marginally above the upper reference range.

4. Body overview pattern count — reconcile "0 Needs attention" display with "at_risk" lead finding label.

5. Liver expanded "What this may mean" — scope boilerplate to data-evidenced states only.

6. Governance label token leak — strip "Confidence framing (governed label):" prefix from user-facing long-form narrative text.

**Verify before certifying UAT complete:**

7. Confirm alcohol/lifestyle bridge is present when questionnaire data includes alcohol input — check that this analysis_id was submitted with the same questionnaire as the previous reference run, or document that the bridge is questionnaire-conditional by design.
