# HealthIQ AI — Results page browser UAT (read-only)

**Date:** 2026-05-12  
**Environment:** `http://localhost:3000/results?analysis_id=b2dfa0c4-efd6-467f-9f2a-84bdf20d8d51`  
**Account:** `test-user3@example.com` (authenticated session)  
**Role:** Read-only browser UAT; no code changes.  
**JSON note:** `healthiq-analysis-2026-05-12.json` was not in the workspace at review time; alignment to backend facts used stakeholder-supplied key facts plus on-screen copy.

---

## 1. Overall verdict

**Classification: not launch-ready**

The shell (nav, typography, card layout, disclaimers) suggests a serious product, but **consumer-visible engineering language, raw markdown, backend slugs, and conflicting “primary” framing** undermine credibility. Several issues are **BLOCKER**-class for any external audience. “Close but needs polish” would understate the severity of leakage and rendering defects observed in Summary, Body overview, Next steps, and long-form narrative blocks.

---

## 2. Top 5 strengths

1. **Clear information hierarchy intent** — “Your results” → primary card → summary → drivers → domains reads like a deliberate journey.
2. **Strong uncertainty language in places** — e.g. confidence limits, “not a diagnosis,” MMA framed as clinician discussion.
3. **B12 counter-narrative is present** — Explicit bullet that B12 is in range and a B12-driven pattern is less likely on this panel alone.
4. **Methylation / MCV / homocysteine thread** — Plain-language cross-body section (“one-carbon / marrow context”) supports the clinical story described for this case.
5. **Actions hub legal framing** — Sensible “not a treatment plan” / education-only copy when that page loads.

---

## 3. Top 10 issues (ordered by user impact)

1. **Primary headline vs ranked lead mismatch** — Hero **“Vascular Inflammation Risk”** while Summary/body emphasise **Homocysteine Elevation Context** as the ranked lead pattern (confusing and undermines trust).
2. **“B12-associated pattern” as clinician block title** while B12 is in range and text elsewhere contradicts — reads like the wrong template or stale label.
3. **Raw `**markdown**` and broken snippets** — Literal asterisks, `(at_` / `at_risk)` style tokens, and awkward fragments visible in Summary and body text (screenshots in session evidence).
4. **Subtitle “Plain-language overview from the deterministic narrative compiler”** — “Deterministic” + “compiler” on the retail Summary card.
5. **Layer B / Layer C / “deterministic arbitration” / `cardiovascular_4_biomarkers`-style slugs** in body and next steps — architecture vocabulary on a consumer results page.
6. **`alcohol_intake_moderate_or_higher_with_one_carbon_lab_coherence`** (or equivalent long slug) visible in lifestyle bridge copy — unacceptable consumer leakage.
7. **`chain_001`, `Ranked #1 because mcv evidence; vitamin_b12 counter-evidence.`** — Evidence-chain and internal field naming in clinician section still in main scroll path.
8. **Trust strip vs headline scale** — “**77 markers**” vs “We received **9 of 9** expected markers for this interpretation” reads contradictory without explanation.
9. **Actions hub empty state** for this completed run — “No actions to show yet … did not include structured recommendation lines” while the results page has rich “Next steps” / follow-up narrative — **journey and data contract feel broken**.
10. **“Wave 1”** on domain cards — roadmap/internal product language on a patient-facing page.

---

## 4. Blockers (must fix before any external user sees this)

| Item | Evidence |
|------|----------|
| **Internal pipeline vocabulary in retail and mid-page copy** | “deterministic narrative compiler,” “Layer B,” “Layer C,” “deterministic arbitration,” “governed capacity score,” etc., visible without entering a clearly labelled “developer only” mode. |
| **Backend / bridge slugs in narrative** | Lifestyle line exposing `…_lab_coherence` style identifier (from `alcohol` search hit). |
| **Raw markdown / broken tokens in user-visible prose** | `**…**` not rendered; fragments like `(at_` / `at_risk)` in Summary (screenshots). |
| **Conflicting primary story** | Primary finding card title vs ranked “Homocysteine Elevation Context” story — user cannot tell what the “main result” is. |
| **Clinician block title “B12-associated pattern”** vs in-range B12 evidence — coherent safety story is damaged. |
| **Technical strip when expanded** | Session showed **analysis UUID**, **N/A** for completed, raw **77** split — telemetry mistaken for user-facing metadata (full-page capture in session). |

---

## 5. Important but non-blocking issues (HIGH / MEDIUM)

- **HIGH:** Marker list uses **snake_case** labels (`apoa1`, `total_cholesterol`, `homocysteine`) in “What’s driving this” — should be human labels everywhere above the fold.
- **HIGH:** Governance banner typo / garble: **“AI-per narrative”** (screenshot) — reads broken or like a leaked token.
- **HIGH:** Long prose columns **truncated or oddly wrapped** in narrative sections (multiple screenshot descriptions: right-edge clipping, short orphan lines).
- **HIGH:** “Top ranked **signal**” in hero subline — “signal” is acceptable in a biomarker product but here it stacks with other engineering words and feels like pipeline language.
- **MEDIUM:** Duplicate **“What this means”** headings (intro vs deeper block) — navigation/mental model cost.
- **MEDIUM:** **“3 pattern group s”** spacing typo in Body overview (from a11y snapshot).
- **MEDIUM:** **“Wave 1”** on domain section heading.
- **MEDIUM:** Actions hub copy **“structured recommendation lines in the data we receive”** — engineering-facing empty state.

---

## 6. Polish / backlog (LOW)

- Primary finding line lists **“Homocysteine, Vitamin B1”** — odd pairing; scan for copy/template bugs.
- **“See all markers”** did not obviously change the a11y tree in-session (may be in-page anchor); confirm expected behaviour and focus management.
- **Search-highlight false positives** — substring matches (e.g. “ALT” inside “Health”) make Ctrl+F style checks noisy; not a product bug but slowed review.
- Minor grammar/clipping in hero (“review and lifestyle” type fixes from screenshot notes).

---

## 7. Evidence / screenshots captured (session machine)

Saved under (local Cursor browser screenshots path from session):

`c:\Users\abroa\AppData\Local\Temp\cursor\screenshots\`

| File | What it shows |
|------|----------------|
| `uat-results-fullpage.png` | Upper results layout (toolbar, governance strip, start of hero). |
| `uat-hero-primary.png` | “Your results,” governance disclaimer, **77 markers**, action buttons. |
| `uat-summary-section.png` | Summary card: **deterministic narrative compiler** subline, markdown / Layer B / `(at_` issues. |
| `uat-actions-hub.png` | Actions hub **empty state** + “Back to results” while authenticated. |

Additional **search-driven** views (browser search highlights) documented: **Layer B** (17 hits), **deterministic** (8), **Layer C** (3), **arbitration** (2), **governed** (6), **alcohol** slug hit, **Haemoglobin** in long-form narrative.

---

## 8. Specific text examples that should be rewritten (samples)

- Summary **subtitle:** “Plain-language overview from the deterministic narrative compiler.”
- Summary **body patterns:** “The ranked lead pattern is `**Homocysteine Elevation Context**` … `Layer B` …” (rendered as literal `**` and internal layer names).
- Body overview style: “… **deterministic system snapshot** … **deterministic arbitration**): `cardiovascular_4_biomarkers` … **governed capacity score** ≥90 …”
- Next steps: “Safe next-step framing (**Layer C**, bounded):” and bullets referencing **Layer C** again.
- Lifestyle bridge: text containing **`alcohol_…_coherence`**-style slug.
- Evidence list: “**Ranked #1 because mcv evidence; vitamin_b12 counter-evidence.**”
- Advanced blurb: “… **Layer C insights**, and the long-form report.”
- Governance strip: “… **governed** clinical rules … **AI-per** narrative is not active …”

---

## 9. Suspected data / unit / status defects (visible or not verified)

| Concern from brief | Browser observation |
|---------------------|---------------------|
| Haemoglobin 144 **g/dL** vs range in **g/L** | **`144` not found** in visible searched viewport; **not verified** on this pass (may sit in biomarker dials / below fold). |
| Haematocrit **0.438** with **%** | Not explicitly searched; **not verified**. |
| **ALT** low vs **critical** status | **Not verified** (search for “ALT” matched substrings like “Health”). |
| **Transferrin** low vs narrative | **Visible:** “transferrin **2 g/L · Critical**” in driver list — aligns with “critical” display; narrative consistency not fully audited sentence-by-sentence. |
| **HbA1c** % vs mmol/mol range | **No “HbA1c”** match in viewport searches — **not verified**. |
| **Free testosterone** unknown | **Not verified**. |
| **BMI** 53.4593 | **No “BMI”** match — **not verified** on page text this session. |

**Separate UI defect (layout / highlighting):** Long-form narrative areas show **severe line clipping** and odd **partial highlights** (e.g. inside normal words) in screenshots — treat as **HIGH** presentation risk even before debating lab units.

---

## 10. LC-S4 / LC-S5 surface checklist (browser)

| Surface | Visible? | Location / notes | Readability / leakage |
|--------|----------|------------------|------------------------|
| **Mock-mode honesty banner** | **Partial / unclear** | No **“mock”** string on Ctrl+F. There **is** a top **governance / mode** strip (“governed clinical rules … narrative not active”). | Copy damaged (**“AI-per”**); “governed” reads governance/engineering, not plain “demo/mock” honesty. |
| **Hero section** | **Yes** | Top: Primary finding card **Vascular Inflammation Risk**. | Strong card design; **conflicts** with deeper ranked-lead story; “signal” + pattern naming mixed. |
| **Retail summary** | **Yes** | **Summary** region + **What’s driving this** list. | **Not retail-grade** due to compiler subtitle, markdown, Layer B, snake_case markers. |
| **“What this means” (default open)** | **Partially** | **“Hide”** control **expanded** early → at least one disclosure open; duplicate **“What this means”** headings later. | Confusing structure; deeper block still says “**Deterministic explanation**…”. |
| **Body overview** | **Yes** | Mid-page **Body overview** card. | Dense; **arbitration**, **at_risk**, system slugs, markdown. |
| **Lead narrative** | **Yes** (fragmented) | Summary + Methylation pathway + investigation path. | Coherent threads exist but **fight the hero headline** and internal tokens. |
| **Next steps** | **Yes** | **Direction and follow-up** / Next steps. | Sensible clinician framing **marred by Layer C** and markdown issues in the same band (per search screenshot). |
| **Domain cards** | **Yes** | **Your health domains (Wave 1)** — CV / metabolic / liver. | Generally readable; **“Wave 1”** leakage; metabolic copy may overreach vs stated lipids picture (content risk, not tool-verified against JSON). |
| **Actions (section + page)** | **Section: Yes** (heading + pointer to hub). **Page: Yes** | `/actions` after session settled showed **Log out** + **empty state**. | **Empty hub** vs rich results = **broken journey**; empty-state copy is engineer-tinged. |
| **Advanced / clinician** | **Yes** | **Clinician-structured “why”**, chain IDs, ranking line, **Advanced & clinician report** teaser. | Appropriately “clinical” **but** chain IDs and `vitamin_b12` tokens should be **behind** a stronger gate or rendered as human prose only. |

---

## 11. Legacy “Metabolic / Cardiovascular focus … summarise structured signals …” strings

**Not found** on results (searches for **“Metabolic focus”** and **“Cardiovascular focus”** returned no matches). **No blocker** for that specific legacy phrasing on this run.

---

## 12. Internal-language leakage table (representative)

| Term / pattern | Classification |
|----------------|----------------|
| **Layer B** (many hits, including Summary) | **Unacceptable consumer leakage** |
| **Layer C** (Next steps + Advanced teaser) | **Unacceptable consumer leakage** |
| **deterministic** / **Deterministic** | **Unacceptable** in retail; **unacceptable** in “plain-language” subtitle |
| **narrative compiler** | **Unacceptable consumer leakage** |
| **deterministic arbitration**, **governed capacity score** | **Unacceptable consumer leakage** |
| **`cardiovascular_4_biomarkers`** (system slug) | **Unacceptable consumer leakage** |
| **`alcohol_intake_…_coherence`** style slug | **BLOCKER** |
| **`chain_001` / `chain_002`**, `mcv evidence; vitamin_b12` | **Unacceptable** in default scroll path (acceptable only if buried behind a strict clinician-only gate with no accidental scroll exposure) |
| **signal** (hero “Top ranked signal…”) | **Borderline** — alone maybe OK; **with** Layer/compiler language reads like pipeline |
| **signal_id**, **root_cause_v1**, **runtime**, **manifest**, **legacy_v1**, **payload**, **cardio_risk**, **`signal_homocysteine_elevation_context`** exact | **Not observed** as raw substrings in searches performed |
| **compiler** (word “compiler”) | **Present** in Summary subtitle |
| **governed** | **Multiple hits** — governance concept OK in principle; **highlight/badge treatment** reads like a token, not user copy |

---

## 13. Clinical / content coherence (against stated key facts)

- **Why homocysteine leads:** Explained in Summary and methylation sections, **but** the **hero primary finding** still shouts **Vascular Inflammation Risk** — user may not understand that homocysteine is the ranked lead.
- **B12 in range, cause not proven:** **Well handled** in evidence bullets; **undermined** by **“B12-associated pattern”** heading.
- **Avoid claiming exact cause:** Mostly cautious language; **slug** and **ranking machine prose** imply mechanistic false precision.
- **Alcohol / MCV / homocysteine in plain English:** Partially; **slug** destroys the plain-English bar.
- **Alarmism / unsupported causality:** Generally restrained; risk is more **false technical authority** than sensationalism.
- **Next steps / no meds:** No supplement/medication prescribing observed; **MMA with clinician** is appropriate **test** framing.

---

## 14. Visual hierarchy and journey

- **Most important finding:** **Not obvious** — dual headline problem.
- **Page length:** Long; acceptable for power users, **heavy** for a first-time consumer without cleaner retail layer.
- **Expandables:** Some disclosure open (**Hide** expanded); duplicate section names reduce clarity.
- **Domain cards:** Useful structure; **Wave 1** and confidence badges need product-language pass.
- **Advanced separation:** Teaser mentions **Layer C** — boundary feels **permeable** rather than “safely separated.”

---

## 15. Recommendation: ready for controlled external testing?

**No.**

---

## 16. Recommended next work package (suggested)

**Title:** “Results retail hardening — copy, markdown, and internal-token gating”

**Objective:** Make the default results view read as **patient English only**: render or strip markdown; remove Layer A/B/C, compiler, arbitration, and slug leakage from retail and from ungated scroll regions; **align hero primary label with ranked lead** or explicitly subordinate one; fix governance/mock-honesty banner copy; **wire Actions hub** to the same recommendation/next-step source shown on results **or** remove the empty hub contradiction; fix layout clipping in long narrative; validate biomarker table units/status against JSON in a **separate** data QA pass.

---

## 17. Reproduction notes (browser)

Log in on `/login`, wait for **Log out**, open the results URL above, optionally toggle **Show technical detail** for metadata strip, visit **`/actions`** after session stabilises (hard navigation may briefly show **Sign in** until hydration).
