# FE-VISUALISATION — Strategic Feedback & Recommendations

**Prepared for:** HealthIQ Product Team  
**Re:** Surface Policy for Four Core Components  
**Context:** Alignment with "Flatiron for Metabolic Dysfunction" positioning  
**Date:** 2026-04-05

---

## Executive Summary

Your discussion paper correctly identifies the critical risk: **FE-VISUALISATION is where engine capability becomes product reality.**

This review evaluates the four components against your strategic positioning:
- **Clinical rigor over wellness vibes** (physician-grade credibility)
- **Longitudinal data moat** (retention through repeat testing)
- **Systems thinking over isolated markers** (competitive differentiation)
- **Pharma platform foundation** (dataset value creation)

**Key recommendation:** Use a **tiered disclosure strategy** that serves three user personas with increasing depth while maintaining clinical credibility at every level.

---

## Strategic Context: Why This Decision Matters Beyond UX

### The Positioning Risk

You're building toward a $400M-800M exit by becoming "Flatiron for metabolic dysfunction."

**If FE-VISUALISATION looks like consumer wellness:**
- Physicians won't trust it → No clinic partnerships → No longitudinal data
- Pharma won't buy it → No dataset monetization → Lower exit multiple
- Users treat it like "interesting but optional" → Low repeat testing → No moat

**If FE-VISUALISATION looks like clinical intelligence:**
- Physicians show it to patients → Clinic partnerships scale → Longitudinal data compounds
- Pharma sees structured phenotypes → Dataset becomes valuable → Premium exit multiple
- Users feel compelled to retest → Repeat rate >40% → Dataset moat forms

**The stakes: This UI layer determines whether you're InsideTracker ($200M exit) or Cleerly ($1B+ valuation).**

---

## User Persona Framework (Tiered Disclosure Model)

Before deciding component-by-component, establish your three target users:

### **Tier 1: Standard Consumer** (Primary Volume)
**Profile:**
- Health-conscious but not medically trained
- Wants actionable insights, not data dumps
- Needs: "What's wrong? How bad? What do I do?"
- Retention trigger: See improvement in 90 days

**Surface needs:**
- Simple, confidence-building
- Biological language (not engineering labels)
- Clear next actions
- Evidence of sophistication (without overwhelming detail)

**What drives repeat testing:**
- Gamification (metabolic age, percentile ranking)
- "You improved from 40th → 68th percentile"
- "Your TyG index dropped 0.3 units - this reduces diabetes risk"

---

### **Tier 2: Advanced User / Biohacker** (High Engagement)
**Profile:**
- Quantified-self enthusiast, reads PubMed abstracts
- Understands HbA1c, ApoB, hsCRP
- Wants mechanistic depth
- Already testing quarterly

**Surface needs:**
- Access to signal chains (insulin resistance → atherogenic dyslipidemia)
- Confidence intervals, evidence citations
- Competing hypotheses visible
- Raw biomarker trends over time

**What drives retention:**
- Depth unavailable elsewhere (InsideTracker can't match this)
- Ability to experiment and track responses
- Community leaderboards

---

### **Tier 3: Clinician Partner** (B2B Revenue + Data Quality)
**Profile:**
- Functional medicine MD, preventive cardiologist, longevity clinic
- Needs clinical decision support
- Shows reports to patients
- Must defend recommendations

**Surface needs:**
- Evidence citations for every claim
- Ranked differential diagnosis
- Confirmatory test suggestions
- Deterministic, auditable reasoning
- Export to EMR/patient portal

**What drives retention:**
- Saves time (replaces manual interpretation)
- Improves patient outcomes (trackable)
- Defensible recommendations (peer-reviewed algorithms)

---

## Component-by-Component Recommendations

### **1. BiomarkerChart**

#### **Purpose**
Visual anchor for understanding a single biomarker's value, context, and importance.

#### **Who it's for**
- **Standard user:** Simple value + range visualization
- **Advanced user:** + historical trend + signal contribution
- **Clinician:** + lab-specific effective-from notes + reference band details

#### **Approved data contract (inputs)**
```yaml
biomarker_id: string
value: float
unit: string
lab_range: {low, high, type}
lab_band_profile: {bands, effective_from, note}
interpretation_state: enum (normal, borderline, abnormal)
importance_score: float (0-1)  # NEW - for ranking/sorting
trend_history: array (optional, multi-panel)
signal_contributions: array (optional, advanced mode)
```

#### **Standard user surface (DEFAULT)**
**Show:**
- Biomarker name (in plain language: "Triglycerides" not "TG")
- Current value + unit
- Visual bar/range indicator (lab-specific range, not generic)
- Interpretation badge (Normal / Borderline / Elevated / High)
- One-sentence explanation: "Triglycerides are fats in blood that contribute to heart disease risk when elevated"

**Example visual:**
```
┌─────────────────────────────────────────┐
│ Triglycerides                    150 mg/dL │
│                                              │
│ ├──────────●──────┤                         │
│ Low    Normal   High                        │
│ <150   150-199  ≥200                        │
│                                              │
│ ✓ Normal                                     │
│ Fats in blood that contribute to           │
│ cardiovascular risk when elevated          │
└─────────────────────────────────────────┘
```

**Don't show:**
- Raw backend field names
- Implementation artifacts (cluster IDs, pipeline stages)
- Confidence scores (save for advanced mode)

---

#### **Advanced mode (EXPANDABLE)**
**Additional elements:**
- Historical trend line (if 2+ panels exist)
- Contributing to signals: "Part of Atherogenic Dyslipidemia pattern"
- Evidence citation: "Normal range per NCEP ATP III guidelines"
- Lab-specific notes: "Reference range effective from 2024-01-15"

**Example expanded view:**
```
┌─────────────────────────────────────────┐
│ Triglycerides - Detailed View             │
│                                              │
│ Current: 150 mg/dL (Normal)                │
│ Previous: 175 mg/dL (3 months ago)         │
│ Trend: ↓ Improving                         │
│                                              │
│ [Trend chart: 3 data points]               │
│                                              │
│ Contributing to:                            │
│ • Atherogenic Dyslipidemia (confidence 0.7)│
│                                              │
│ Clinical context:                           │
│ Elevated TG often seen with insulin        │
│ resistance. Your TG/HDL ratio is 2.8       │
│ (optimal <2.0)                              │
│                                              │
│ Evidence: NCEP ATP III (2001)              │
└─────────────────────────────────────────┘
```

---

#### **Clinician mode (B2B partners only)**
**Additional elements:**
- Lab-specific band profile details
- Effective-from date (for range changes)
- One-sided bound handling notes
- Export button (PDF, EMR-compatible format)

---

#### **NEVER show (Internal/Debug only)**
- Raw cluster object IDs
- Pipeline execution logs
- Backend validation states
- Database field names
- Signal evaluation intermediate states

---

#### **Key design principle for BiomarkerChart**

> **"Trust through simplicity, depth on demand"**

The standard view should look professional but approachable—something a physician can confidently show a patient.

The advanced view should reward curiosity without requiring it.

---

### **2. ClusterCard**

#### **Purpose**
System-level interpretation that shows biological patterns across multiple biomarkers.

**This is where HealthIQ demonstrates systems thinking (competitive moat).**

#### **Strategic importance**
- **Consumer wellness companies show:** Individual marker flags (green/yellow/red)
- **HealthIQ shows:** "Your markers suggest insulin resistance pattern affecting lipid metabolism and inflammation"

**This is the differentiation that justifies premium pricing and pharma interest.**

#### **Who it's for**
- **Standard user:** Biological system summary in plain language
- **Advanced user:** + signal chains, contributing markers, evidence
- **Clinician:** + differential diagnosis, confirmatory tests

---

#### **Approved data contract (inputs)**
```yaml
cluster_id: string (internal only, not displayed)
system_name: string  # User-facing: "Metabolic Health", "Lipid Transport"
pattern_name: string  # "Insulin Resistance", "Atherogenic Dyslipidemia"
severity: enum (mild, moderate, significant)
confidence: float (0-1)
primary_markers: array
supporting_markers: array
signal_chain: array (optional, for advanced mode)
why_it_matters: string  # Plain language explanation
evidence_summary: string
suggested_actions: array
```

---

#### **Standard user surface (DEFAULT)**

**Show:**
- System/pattern name in biological language
- Severity indicator (mild/moderate/significant - NOT red/yellow/green)
- Top 3 contributing markers
- One-paragraph explanation of what this means biologically
- Why it matters (clinical relevance)
- Top 3 actionable recommendations

**Example:**
```
┌─────────────────────────────────────────────────┐
│ 🔍 Insulin Resistance Pattern Detected          │
│                                                   │
│ Severity: Moderate                               │
│                                                   │
│ Key markers:                                     │
│ • TyG Index: 8.6 (elevated)                     │
│ • Triglycerides: 175 mg/dL (borderline high)    │
│ • Fasting Glucose: 102 mg/dL (borderline)       │
│                                                   │
│ What this means:                                 │
│ Your body appears less responsive to insulin,   │
│ the hormone that regulates blood sugar. This    │
│ pattern often precedes type 2 diabetes by 5-10  │
│ years and increases cardiovascular risk.        │
│                                                   │
│ Why it matters:                                  │
│ Early detection allows lifestyle changes that   │
│ can reverse insulin resistance and prevent      │
│ progression to diabetes.                         │
│                                                   │
│ Recommended actions:                             │
│ 1. Reduce refined carbohydrates (bread, sugar)  │
│ 2. Increase physical activity (150 min/week)    │
│ 3. Consider time-restricted eating (16:8)       │
│                                                   │
│ [Learn more ↗] [Track progress →]               │
└─────────────────────────────────────────────────┘
```

**Don't show:**
- Engineering cluster IDs ("cluster_metabolic_001")
- Raw confidence scores without context
- Technical signal chain notation
- Implementation artifacts

---

#### **Advanced mode (EXPANDABLE)**

**Additional elements:**
- Full signal chain visualization
- All contributing markers (not just top 3)
- Evidence citations with DOIs
- Confidence score with explanation
- Competing patterns (if ranked ambiguity applies)
- Historical progression (if multi-panel)

**Example expanded:**
```
┌─────────────────────────────────────────────────┐
│ Insulin Resistance Pattern - Detailed Analysis │
│                                                   │
│ Signal Chain:                                    │
│ Insulin Resistance (0.8) →                      │
│   Atherogenic Dyslipidemia (0.7) →              │
│     Systemic Inflammation (0.6) →               │
│       Cardiovascular Risk (0.7)                  │
│                                                   │
│ All contributing markers:                        │
│ Primary:                                         │
│ • TyG Index: 8.6 (HR 6.87 for diabetes)¹        │
│ • TG/HDL ratio: 3.2 (optimal <2.0)²             │
│ • Fasting glucose: 102 mg/dL                    │
│                                                   │
│ Supporting:                                      │
│ • HbA1c: 5.8% (prediabetes range)               │
│ • HDL: 42 mg/dL (low)                           │
│ • Waist circumference: 38 inches (elevated)     │
│                                                   │
│ Confidence: 0.8 (High)                           │
│ Basis: 5/6 primary markers positive,            │
│ validated against Navarro-González 2016 cohort  │
│                                                   │
│ Evidence:                                        │
│ ¹ Navarro-González et al. Diabetes Care 2016    │
│   (n=4,820, 8-year follow-up)                   │
│ ² Gaziano et al. JAMA 1997                      │
│                                                   │
│ Intervention evidence:                           │
│ DPP trial: 58% diabetes risk reduction with     │
│ lifestyle intervention in similar cohort        │
│                                                   │
│ [View full research →]                           │
└─────────────────────────────────────────────────┘
```

---

#### **Clinician mode**

**Additional elements:**
- Differential diagnosis (competing patterns)
- Confirmatory tests recommended
- Treatment guidelines reference
- Export for patient chart

---

#### **CRITICAL: What ClusterCard should NEVER do**

**❌ Don't:**
- Display raw cluster computation artifacts
- Use engineering labels as user-facing copy
- Show "Cluster_ID_7482" or similar implementation details
- Present patterns without biological translation
- Claim diagnostic certainty ("You have insulin resistance")

**✅ Do:**
- Translate technical patterns into biological language
- Frame as "pattern detected" not "diagnosis confirmed"
- Always provide evidence basis
- Explain clinical relevance clearly
- Link to actionable next steps

---

#### **Key design principle for ClusterCard**

> **"Show systems thinking without exposing system internals"**

This component is your competitive moat. It must demonstrate depth while remaining accessible.

Users should think: "Wow, this is way smarter than my lab report."

They should NOT think: "What is cluster_metabolic_dysfunction_v2?"

---

### **3. InsightPanel**

#### **Purpose**
**This is the hero component.** Main structured interpretation surface that synthesizes everything into actionable intelligence.

**Strategic role:** This is where ranked ambiguity, primary concern logic, and WHY hypotheses become user-facing value.

#### **Who it's for**
- **Standard user:** Primary concern + top 3 actions
- **Advanced user:** + competing interpretations + confirmatory tests
- **Clinician:** + full differential + evidence trail

---

#### **Approved data contract (inputs)**
```yaml
primary_concern: {
  pattern: string,
  severity: enum,
  confidence: float,
  explanation: string,
  evidence: array
}
ranked_ambiguity: array[{
  pattern: string,
  confidence: float,
  distinguishing_tests: array
}]
key_findings: array[{
  finding: string,
  importance: float,
  explanation: string
}]
recommended_actions: array[{
  action: string,
  priority: enum (high, medium, low),
  evidence_basis: string,
  timeframe: string
}]
confirmatory_tests: array (optional, advanced mode)
why_hypotheses: array (optional, for explanation depth)
```

---

#### **Standard user surface (DEFAULT)**

**Structure:**
1. **Primary Concern** (one clear lead interpretation)
2. **Why This Matters** (clinical relevance)
3. **Top 3 Actions** (evidence-backed, prioritized)
4. **What to Watch** (red flags, when to retest)

**Example:**
```
┌─────────────────────────────────────────────────┐
│ 🎯 Your Primary Health Focus                    │
│                                                   │
│ INSULIN RESISTANCE PATTERN                       │
│ Severity: Moderate | Confidence: High            │
│                                                   │
│ What we found:                                   │
│ Your biomarkers show an early insulin resistance│
│ pattern - your body is becoming less responsive │
│ to insulin, the hormone that regulates blood    │
│ sugar. This pattern typically appears 5-10 years│
│ before type 2 diabetes develops.                 │
│                                                   │
│ Supporting evidence:                             │
│ • TyG Index: 8.6 (predicts 6.87× diabetes risk) │
│ • TG/HDL ratio: 3.2 (optimal <2.0)              │
│ • Fasting glucose: 102 mg/dL (prediabetes)      │
│                                                   │
│ Why this matters:                                │
│ Catching insulin resistance early is crucial.   │
│ At this stage, lifestyle changes can often      │
│ reverse the pattern and prevent diabetes. Once  │
│ diabetes develops, management becomes lifelong. │
│                                                   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                   │
│ 📋 Your Action Plan (Evidence-Based)            │
│                                                   │
│ 1. DIETARY CHANGES (Highest Impact)             │
│    Reduce refined carbs, increase fiber          │
│    Evidence: DPP trial showed 58% risk reduction│
│    Timeline: Start this week, reassess in 90d   │
│                                                   │
│ 2. PHYSICAL ACTIVITY                             │
│    150 minutes/week moderate exercise            │
│    Evidence: Reduces insulin resistance 25-40%  │
│    Timeline: Build up over 4 weeks               │
│                                                   │
│ 3. TIME-RESTRICTED EATING                        │
│    Consider 16:8 fasting window                  │
│    Evidence: Improves insulin sensitivity       │
│    Timeline: Trial for 8 weeks                   │
│                                                   │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ │
│                                                   │
│ ⚠️  What to Watch                                │
│ Retest in 90 days to track progress.            │
│ See a doctor if you develop: excessive thirst,  │
│ frequent urination, unexplained weight loss.    │
│                                                   │
│ [Start 90-day challenge →]                       │
│ [See competing patterns ↓] (Advanced)           │
└─────────────────────────────────────────────────┘
```

---

#### **Advanced mode (EXPANDABLE)**

**Additional sections:**
- **Competing Interpretations** (ranked ambiguity visible)
- **Confirmatory Tests** (what would clarify uncertainty)
- **Full Evidence Trail** (citations, cohort details)
- **Signal Chain Detail** (mechanism explanation)

**Example competing patterns section:**
```
┌─────────────────────────────────────────────────┐
│ 🔍 Competing Patterns (Ranked by Confidence)    │
│                                                   │
│ 1. Insulin Resistance (0.82 confidence)         │
│    [Primary interpretation above]                │
│                                                   │
│ 2. Early Hepatic Dysfunction (0.45 confidence)  │
│    Your ALT (42 U/L) is mildly elevated.        │
│    Could indicate fatty liver, but less certain.│
│                                                   │
│    To clarify: Add GGT, AST, consider ultrasound│
│                                                   │
│ 3. Thyroid-Metabolic Interaction (0.38)         │
│    TSH borderline (3.8). Could contribute to    │
│    metabolic pattern, but confidence is lower.  │
│                                                   │
│    To clarify: Add Free T4, Free T3              │
│                                                   │
│ Current recommendation:                          │
│ Focus on insulin resistance (highest confidence)│
│ Retest in 90 days. If pattern persists, add     │
│ hepatic and thyroid markers for clarity.         │
└─────────────────────────────────────────────────┘
```

---

#### **Clinician mode**

**Additional elements:**
- Full differential diagnosis
- Guidelines-based recommendations (ADA, AHA, etc.)
- ICD-10 codes for billing (if applicable)
- Export to patient chart
- Printable patient handout

---

#### **What InsightPanel should NEVER do**

**❌ Don't:**
- Make definitive medical diagnoses ("You have diabetes")
- Recommend pharmaceuticals (prescription authority violation)
- Overclaim certainty ("100% confident you have...")
- Hide uncertainty when it exists (ranked ambiguity IS valuable)
- Use fear tactics ("You'll die if you don't...")

**✅ Do:**
- Frame as "pattern detected" or "biomarkers suggest"
- Recommend lifestyle interventions with evidence
- Be honest about confidence levels
- Acknowledge competing interpretations when relevant
- Always direct to physician for medical decisions

---

#### **Key design principle for InsightPanel**

> **"Confident guidance without overstepping clinical boundaries"**

This panel should make users feel:
- **Informed:** "I understand what's happening in my body"
- **Empowered:** "I know what to do next"
- **Confident in HealthIQ:** "This is way deeper than my lab report"
- **Appropriately cautious:** "I should discuss this with my doctor"

---

### **4. PipelineStatus**

#### **Purpose (CONTESTED - Needs Team Decision)**

**The core question:** Is this truly end-user-facing, or is it infrastructure visibility?

**Two valid approaches:**

#### **Option A: User-Facing Data Quality Component** (RECOMMENDED)
Translate pipeline internals into user-relevant confidence context.

#### **Option B: Internal/Debug Only**
Keep raw pipeline status for QA, support, and admin users only.

---

#### **Recommendation: Option A (User-Facing, Translated)**

**Rationale:**
- Users DO benefit from knowing data quality limitations
- Transparency builds trust ("Some markers were outside lab reference context")
- Sets realistic expectations for confidence levels
- Differentiates from black-box consumer wellness apps

**But:** Must be translated out of engineering language.

---

#### **If user-facing, approved data contract (inputs)**
```yaml
analysis_status: enum (complete, partial, limited_context)
data_quality_flags: array[{
  category: enum (missing_markers, range_context, historical_gap),
  severity: enum (minor, moderate, significant),
  user_message: string,
  impact_on_confidence: string
}]
confidence_context: {
  overall_confidence: enum (high, moderate, limited),
  limiting_factors: array,
  what_would_improve: array
}
completeness_score: float (0-1)
```

---

#### **Standard user surface (DEFAULT - if Option A chosen)**

**Show:**
- Overall analysis status (complete vs limited)
- Plain-language explanation of any limitations
- Impact on confidence (what's less certain because of gaps)
- What additional data would improve certainty

**Example (complete analysis):**
```
┌─────────────────────────────────────────────────┐
│ ✓ Analysis Complete                             │
│                                                   │
│ Data quality: High                               │
│ All key metabolic markers present                │
│ Lab ranges available for all biomarkers         │
│                                                   │
│ Confidence level: High for primary patterns     │
└─────────────────────────────────────────────────┘
```

**Example (limited analysis):**
```
┌─────────────────────────────────────────────────┐
│ ⚠️  Analysis Complete (with limitations)        │
│                                                   │
│ Data quality: Moderate                           │
│                                                   │
│ What's limiting confidence:                      │
│ • Missing HbA1c (would strengthen insulin       │
│   resistance assessment)                         │
│ • Missing ApoB (would clarify cardiovascular    │
│   risk more precisely)                           │
│                                                   │
│ Your results are still meaningful, but adding   │
│ these markers would improve certainty.           │
│                                                   │
│ Current confidence: Moderate for metabolic      │
│ patterns, Limited for cardiovascular detail     │
│                                                   │
│ [See what to add next test →]                   │
└─────────────────────────────────────────────────┘
```

---

#### **What PipelineStatus should NEVER show (if user-facing)**

**❌ Don't show:**
- Raw pipeline stage names ("signal_evaluation_complete: true")
- Backend error codes
- Database query status
- Execution timestamps
- Engineering-level logs

**✅ Do show:**
- User-impact translation ("Missing data limits confidence in...")
- Constructive guidance ("Adding X would clarify Y")
- Honest limitations without alarm
- Path to completeness

---

#### **Alternative: Option B (Internal/Debug Only)**

**If team decides PipelineStatus is not user-facing:**

Move all pipeline internals to admin/debug interface only.

**Standard users see:** Nothing (confidence is communicated through InsightPanel instead)

**Advanced users see:** Data quality summary (translated, as in Option A)

**Admin/support see:** Full pipeline execution details, logs, validation states

---

#### **Key design principle for PipelineStatus**

> **"Transparency without exposing plumbing"**

If user-facing: Translate pipeline reality into confidence context.

If internal-only: Keep it entirely out of the product surface.

**Team must decide:** Does showing data quality limitations build trust or create confusion?

---

## Tiered Disclosure Strategy (Summary Table)

| Component | Standard User | Advanced User | Clinician | Internal/Debug |
|-----------|---------------|---------------|-----------|----------------|
| **BiomarkerChart** | Value + range + state | + Trend + signals | + Lab notes + export | Pipeline logs, validation states |
| **ClusterCard** | System + severity + top actions | + Full chain + evidence | + Differential + confirmatory | Cluster IDs, computation artifacts |
| **InsightPanel** | Primary concern + top 3 actions | + Competing patterns + tests | + Full differential + guidelines | Raw hypothesis scoring, pipeline intermediate states |
| **PipelineStatus** | Data quality summary (translated) OR hidden | Same or expanded | Same + support mode | Full pipeline execution details |

---

## Critical Design Principles (Apply to All Components)

### **1. Clinical Credibility > Consumer Friendliness**

**Every component must be defensible to a physician.**

Test: "Would a functional medicine MD feel comfortable showing this to a patient?"

- ✅ If yes: Clinical credibility maintained
- ❌ If no: Risk of being dismissed as "wellness fluff"

---

### **2. Evidence-Backed > Generic Advice**

**Every recommendation must cite evidence.**

**Bad (consumer wellness):**
> "Your triglycerides are high. Eat less sugar."

**Good (clinical intelligence):**
> "Your triglycerides (175 mg/dL) contribute to atherogenic dyslipidemia pattern. Reducing refined carbohydrates by 50% showed 25-30% TG reduction in Diabetes Care 2019 study (n=412)."

The second builds trust. The first is generic noise.

---

### **3. Systems Over Symptoms**

**Show biological connections, not just isolated flags.**

**Bad:**
> "High triglycerides ⚠️"
> "High glucose ⚠️"
> "Low HDL ⚠️"

**Good:**
> "Your markers suggest an insulin resistance pattern affecting lipid metabolism:
> - Insulin resistance (TyG 8.6) →
> - Atherogenic dyslipidemia (TG/HDL 3.2) →
> - Increased cardiovascular risk"

This is your competitive moat. Don't give it away by showing disconnected markers.

---

### **4. Confidence Transparency > False Certainty**

**When you're not sure, say so.**

**Bad:**
> "You have insulin resistance and early liver disease."

**Good:**
> "Primary pattern: Insulin resistance (high confidence, 0.82)
> Secondary concern: Possible hepatic involvement (moderate confidence, 0.45)
> Confirmatory tests would clarify: GGT, AST, abdominal ultrasound"

Honesty about uncertainty builds trust. Overconfidence destroys it.

---

### **5. Retention Mechanics Baked In**

**Every component should create desire to retest.**

**BiomarkerChart:** Show historical trend (if multi-panel) → "See how you're improving"

**ClusterCard:** "Retest in 90 days to track pattern changes"

**InsightPanel:** "Start 90-day challenge to reverse this pattern"

**PipelineStatus:** "Adding HbA1c next test would strengthen confidence"

Without repeat testing, your dataset moat doesn't form. UI must drive this.

---

## Specific Recommendations by User Type

### **For Standard Consumer Users**

**Philosophy:** Trust through simplicity, not dumbing down.

**BiomarkerChart:**
- ✅ Simple value + range visualization
- ✅ Plain language explanations
- ✅ One-sentence biological context
- ❌ No trend (until 2nd panel)
- ❌ No confidence scores
- ❌ No raw technical details

**ClusterCard:**
- ✅ System name in biological language
- ✅ Severity indicator
- ✅ Top 3 contributing markers
- ✅ Why it matters (clinical relevance)
- ✅ Top 3 actions
- ❌ No signal chains (save for advanced)
- ❌ No confidence scores
- ❌ No competing patterns (unless high ambiguity)

**InsightPanel:**
- ✅ ONE primary concern (not 5 competing patterns)
- ✅ Clear explanation
- ✅ Top 3 prioritized actions
- ✅ Evidence basis (brief)
- ✅ When to retest
- ❌ No full differential diagnosis
- ❌ No confirmatory test lists
- ❌ No medical jargon

**PipelineStatus:**
- ✅ Data quality summary (if Option A chosen)
- ✅ Plain language limitations
- ❌ No pipeline internals
- ❌ No execution logs

---

### **For Advanced Users / Biohackers**

**Philosophy:** Reward curiosity, enable experimentation.

**BiomarkerChart:**
- ✅ Everything from standard mode
- ✅ Historical trend visualization
- ✅ Signal contributions
- ✅ Evidence citations
- ✅ Export data (CSV)

**ClusterCard:**
- ✅ Everything from standard mode
- ✅ Full signal chain visualization
- ✅ All contributing markers
- ✅ Confidence scores with explanation
- ✅ Competing patterns (ranked ambiguity)
- ✅ Full evidence trail with DOIs

**InsightPanel:**
- ✅ Everything from standard mode
- ✅ Competing interpretations ranked
- ✅ Confirmatory tests to clarify uncertainty
- ✅ Full evidence references
- ✅ Mechanism explanations (signal chains)
- ✅ Intervention response tracking (multi-panel)

**PipelineStatus:**
- ✅ Detailed data quality report
- ✅ What's missing and why it matters
- ✅ Completeness scoring
- ❌ Still no raw pipeline logs

---

### **For Clinician Partners (B2B)**

**Philosophy:** Clinical decision support, not replacement.

**All components get additional:**
- ✅ Full evidence citations (PubMed IDs, DOIs)
- ✅ Clinical guidelines references (ADA, AHA, AACE)
- ✅ Differential diagnosis reasoning
- ✅ Confirmatory test recommendations
- ✅ Export to EMR/PDF
- ✅ Patient handout generation
- ✅ ICD-10 codes (if applicable for billing)

**Plus clinician-specific features:**
- Practice-level analytics dashboard
- Patient cohort tracking
- Outcome reporting
- Custom lab integration
- White-label option

---

## Addressing Your Seven Discussion Questions

### **1. What is the minimum set of information a standard user must see to feel the app is genuinely useful?**

**Minimum viable:**
- **What:** Which biomarkers are concerning
- **Why:** What this means biologically (system-level, not just "high")
- **So what:** Why it matters clinically
- **Now what:** What to do about it (evidence-backed actions)
- **What next:** When to retest to track progress

**If missing any of these, the app feels incomplete.**

**Implementation:**
- BiomarkerChart handles "What"
- ClusterCard handles "Why" (systems thinking)
- InsightPanel handles "So what" + "Now what" + "What next"

---

### **2. Which of the four components are truly user-facing, and which are partially internal by nature?**

**Truly user-facing (all user types):**
- BiomarkerChart ✅
- ClusterCard ✅
- InsightPanel ✅

**Contested (team must decide):**
- PipelineStatus (user-facing translated OR internal-only)

**My recommendation:** Make PipelineStatus user-facing but translated (Option A). Transparency about data quality builds trust and sets realistic expectations.

---

### **3. What should be visible in default mode versus advanced mode?**

**See tiered disclosure table above.**

**General rule:**
- **Default mode:** One primary interpretation, top 3 actions, minimal noise
- **Advanced mode:** Competing patterns, full evidence, confirmatory tests, signal chains

**Toggle placement:** Single "Advanced view" toggle per component (not global setting)

**Why:** Some users want detail on ClusterCard but simplicity on BiomarkerChart.

---

### **4. Do we want to show only biomarker-level information, or also system-level interpretation from day one?**

**Show system-level from day one. This is your moat.**

**Rationale:**
- Consumer wellness apps show biomarker flags (generic)
- HealthIQ shows biological systems and patterns (defensible)
- Physicians care about systems, not isolated markers
- Pharma pays for phenotypes, not individual TG values

**But:** Translate technical clusters into biological language.

**Bad:** "cluster_metabolic_dysfunction_v2 detected"

**Good:** "Insulin resistance pattern affecting lipid metabolism"

---

### **5. How much of the ranked-ambiguity/uncertainty model should be visible to users versus hidden behind clinician/advanced layers?**

**Standard users:**
- Primary concern only (highest confidence pattern)
- Brief mention of uncertainty if relevant: "Moderate confidence. Confirmatory tests would clarify."
- No competing patterns unless specifically high ambiguity case

**Advanced users:**
- Full ranked ambiguity visible
- All competing patterns with confidence scores
- Explicit "what would clarify" guidance

**Clinicians:**
- Full differential diagnosis
- All patterns ranked
- Confirmatory test recommendations
- Diagnostic reasoning trail

**Why this tiering:**
- Most users want clear guidance, not options paralysis
- Advanced users value transparency about uncertainty
- Clinicians need full differential for clinical decision-making

---

### **6. How do we stop technical implementation artefacts leaking onto the product surface?**

**Three-layer content policy (from your paper):**

**Layer 1: Standard user surface**
- Only biological language
- No backend field names
- No cluster IDs
- No pipeline stages
- No database artifacts

**Layer 2: Advanced mode**
- Still product-legible
- Signal chains OK (if explained)
- Confidence scores OK (with context)
- Evidence citations OK
- Still no raw backend labels

**Layer 3: Internal/debug**
- Everything else
- Raw pipeline logs
- Validation states
- Database query results
- Execution timestamps

**Enforcement mechanism:**

Create a **translation layer** in frontend code:

```typescript
// BAD (implementation leak)
<ClusterCard 
  clusterId="cluster_metabolic_dysfunction_v2"
  signalChain={raw_backend_object}
/>

// GOOD (translated)
<ClusterCard
  systemName="Metabolic Health"
  patternName="Insulin Resistance"
  explanation={translated_explanation}
  evidenceBasis={formatted_citations}
/>
```

**Code review checklist:**
- [ ] No backend field names visible to user
- [ ] No cluster/signal IDs in UI text
- [ ] No pipeline stage names displayed
- [ ] All technical terms translated to biological language
- [ ] Evidence citations formatted for readability

---

### **7. What would make these four components feel like a coherent product rather than four disconnected widgets?**

**Visual coherence:**
- Consistent design language
- Shared color system (not traffic lights - see below)
- Unified typography
- Common interaction patterns

**Narrative coherence:**
- BiomarkerChart → Introduces individual markers
- ClusterCard → Connects markers into systems
- InsightPanel → Synthesizes into actionable intelligence
- PipelineStatus → Contextualizes confidence

**Information hierarchy:**
- InsightPanel is the hero (main focus)
- ClusterCard supports with system-level detail
- BiomarkerChart allows drill-down into specifics
- PipelineStatus provides context for confidence

**Navigation flow:**
- User lands on InsightPanel (primary concern)
- Clicks into ClusterCard for system detail
- Clicks into BiomarkerChart for specific marker context
- PipelineStatus visible but not intrusive

**Shared interaction model:**
- Click to expand (standard → advanced)
- Hover for tooltips (evidence citations)
- Export button in same place on all components
- "Learn more" links to knowledge base

---

## Color System Recommendation (Critical for Product Perception)

### **DON'T use traffic light colors (red/yellow/green)**

**Why avoid:**
- Consumer wellness cliché
- Medically imprecise (severity isn't binary)
- Creates alarm without context
- Physicians distrust this approach

### **DO use a clinical credibility palette**

**Severity indicators:**
- **Normal:** Neutral gray or subtle blue
- **Borderline:** Amber/gold (not yellow - less alarm)
- **Elevated:** Warm orange (concern without panic)
- **High:** Deep red (reserved for truly significant)

**Confidence indicators:**
- **High confidence:** Solid fill
- **Moderate confidence:** Textured/hatched
- **Low confidence:** Outline only

**System health:**
- **Optimal:** Soft green (not bright green)
- **At risk:** Warm amber
- **Concerning:** Deep orange/red

**Visual reference:**
```
┌─────────────────────────────────────────┐
│ Severity Scale (Not Traffic Lights)    │
│                                          │
│ ▓ Normal     (Neutral gray/blue)       │
│ ▒ Borderline (Amber/gold)              │
│ ░ Elevated   (Warm orange)             │
│ █ High       (Deep red)                │
└─────────────────────────────────────────┘
```

---

## Implementation Priority (Phased Rollout)

**Don't try to build everything at once.** Phase the depth.

### **Phase 1: MVP (Week 1-2)**
**Goal:** Something clinicians can show patients immediately.

**Build:**
- BiomarkerChart (standard mode only)
- InsightPanel (primary concern only, no ranked ambiguity yet)
- PipelineStatus (simple "analysis complete" indicator)

**Skip for now:**
- ClusterCard (requires more translation work)
- Advanced modes
- Trend visualization (no multi-panel data yet)

**Success metric:** 5 clinic partners willing to show this to patients.

---

### **Phase 2: Depth (Week 3-4)**
**Goal:** Demonstrate systems thinking (competitive moat).

**Add:**
- ClusterCard (standard mode)
- InsightPanel (add ranked ambiguity for advanced users)
- BiomarkerChart (add trend if multi-panel data exists)

**Success metric:** Advanced users engage with expanded views >60% of sessions.

---

### **Phase 3: Clinical Features (Week 5-6)**
**Goal:** B2B-ready for clinic partnerships.

**Add:**
- Clinician mode for all components
- Export functionality
- Evidence citation formatting
- Patient handout generation

**Success metric:** Clinicians use export feature >40% of analyses.

---

## Risk Assessment & Mitigation

### **Risk 1: Overclaiming (Looks Like Diagnosis)**

**Manifestation:**
- "You have insulin resistance" (definitive)
- "Your diabetes risk is 87%" (false precision)
- "You will develop X disease" (prediction overreach)

**Mitigation:**
- Frame as "pattern detected" not "diagnosis confirmed"
- Avoid percentage predictions unless peer-reviewed validation exists
- Always include physician consultation disclaimer
- Use confidence language: "suggests", "indicates", "consistent with"

---

### **Risk 2: Consumer Wellness Drift**

**Manifestation:**
- Traffic light colors (red/yellow/green)
- Generic advice ("eat healthier, exercise more")
- No evidence citations
- Looks like InsideTracker clone

**Mitigation:**
- Clinical color palette (not traffic lights)
- Evidence-backed recommendations with citations
- Systems thinking (patterns, not isolated markers)
- Physician-grade explanations

---

### **Risk 3: Technical Leak (Backend Artifacts Visible)**

**Manifestation:**
- "cluster_metabolic_dysfunction_v2"
- "signal_evaluation_complete: true"
- "confidence_score: 0.847392"
- Pipeline stage names in UI

**Mitigation:**
- Translation layer in frontend (no raw backend objects)
- Code review checklist (no implementation artifacts)
- Designer review (catch technical language)
- User testing with non-technical users

---

### **Risk 4: Information Overload (Too Much Depth)**

**Manifestation:**
- 10 competing patterns shown simultaneously
- Every biomarker flagged as important
- 20 recommended actions
- Users paralyzed, don't know where to start

**Mitigation:**
- Primary concern prominence (one main thing)
- Top 3 actions only (not exhaustive list)
- Advanced mode for detail (don't force it)
- Clear visual hierarchy (what matters most)

---

### **Risk 5: Low Retention (No Retest Incentive)**

**Manifestation:**
- Static results (no time-based value)
- No gamification
- No progress tracking
- Users upload once, never return

**Mitigation:**
- Trend visualization (requires 2+ panels to unlock)
- 90-day challenge prompts
- Percentile ranking ("You're top 15% for your age")
- "Your metabolic age improved from 50 → 46"

---

## Alignment with Strategic Objectives

### **Does this FE-VISUALISATION strategy support your 3 critical execution steps?**

#### **Step #1: Prove Repeat Testing Works**

**BiomarkerChart:**
- ✅ Historical trend requires 2+ panels (incentive to retest)
- ✅ "See improvement" messaging

**ClusterCard:**
- ✅ "Retest in 90 days to track pattern changes"
- ✅ Severity tracking over time

**InsightPanel:**
- ✅ "Start 90-day challenge"
- ✅ Action plan with timeframe
- ✅ "When to retest" guidance

**Net effect:** Every component creates desire for longitudinal tracking.

---

#### **Step #2: Validate Algorithms Predict Outcomes**

**InsightPanel:**
- ✅ Evidence citations visible (sets expectation for validation)
- ✅ Confidence transparency (matches academic rigor)

**ClusterCard:**
- ✅ Shows signal chains (demonstrates mechanistic thinking)
- ✅ "Why it matters" links to outcomes

**Net effect:** Product demonstrates validation-readiness even before publications exist.

---

#### **Step #3: Land $1M+ Pharma Contract**

**All components:**
- ✅ Deterministic, auditable (pharma requirement)
- ✅ Phenotype-tagged (cohort discovery ready)
- ✅ Structured output (data licensing ready)

**ClusterCard specifically:**
- ✅ System-level patterns = pharma phenotypes
- ✅ "Insulin resistance pattern" = trial recruitment criteria

**Net effect:** Product surface demonstrates dataset value to pharma buyers.

---

## Final Recommendations

### **1. Component Priority Ranking**

**Must build well:**
1. **InsightPanel** (hero component, primary value)
2. **ClusterCard** (competitive moat, systems thinking)
3. **BiomarkerChart** (foundational, but commodity)
4. **PipelineStatus** (nice-to-have, context)

**If resource-constrained, build in this order.**

---

### **2. Mode Strategy**

**Standard mode (default):**
- One primary concern
- Top 3 actions
- Minimal noise
- High confidence

**Advanced mode (opt-in per component):**
- Competing patterns
- Full evidence
- Confirmatory tests
- Signal chains

**Clinician mode (B2B partners only):**
- Full differential
- Export tools
- Guidelines references
- Patient handouts

---

### **3. Translation Layer (Non-Negotiable)**

**Create a strict boundary between backend and frontend:**

```typescript
// Backend outputs (Layer B)
{
  cluster_id: "cluster_metabolic_001",
  confidence: 0.847392,
  signal_chain: ["sig_ir", "sig_athero", "sig_inflam"]
}

// Translation layer (Layer C)
{
  systemName: "Metabolic Health",
  patternName: "Insulin Resistance",
  confidenceLevel: "high",  // rounded from 0.847392
  explanation: "Your body shows reduced insulin sensitivity...",
  signalChainExplanation: "Insulin resistance → Atherogenic dyslipidemia → Inflammation"
}

// Frontend displays (what user sees)
"Insulin Resistance Pattern Detected
Confidence: High
[Biological explanation in plain language]"
```

**No backend artifacts escape this translation.**

---

### **4. Evidence Citation Standard**

**Every recommendation must include:**
- Study author + year: "Navarro-González 2016"
- Population: "(n=4,820, 8-year follow-up)"
- Outcome: "HR 6.87 for incident diabetes"
- Journal: "Diabetes Care" (for credibility)
- DOI link (advanced mode)

**This separates HealthIQ from consumer wellness apps that make unsubstantiated claims.**

---

### **5. User Testing Protocol**

**Before launch, test with:**

**Group 1: Non-technical consumers (n=5)**
- Can they understand primary concern?
- Do they know what to do next?
- Does anything confuse them?
- Would they retest in 90 days?

**Group 2: Biohackers / advanced users (n=5)**
- Do they engage with advanced mode?
- Is depth sufficient to justify premium pricing?
- Does evidence citation build trust?

**Group 3: Physicians (n=3)**
- Would they show this to patients?
- Do they trust the recommendations?
- Are evidence citations adequate?
- Any credibility concerns?

**Success criteria:**
- ✅ 80% of Group 1 understand primary concern
- ✅ 60% of Group 2 engage with advanced mode
- ✅ 100% of Group 3 would show to patients

---

## Conclusion

**Your discussion paper asks the right question:**

> "What should HealthIQ surface to the user, in what form, and with what level of interpretation?"

**The answer is not binary (simple vs detailed).**

**The answer is tiered disclosure:**
- Standard users get confidence through simplicity
- Advanced users get depth on demand
- Clinicians get clinical-grade decision support

**Every component should:**
1. Build clinical credibility (physician-showable)
2. Demonstrate systems thinking (competitive moat)
3. Drive repeat testing (longitudinal retention)
4. Structure data for pharma (dataset value)

**Critical success factor:**

> **Translate backend sophistication into biological intelligence without exposing implementation plumbing.**

**If you achieve this, FE-VISUALISATION becomes the moment HealthIQ stops being "a better blood test app" and starts being "clinical-grade metabolic intelligence platform."**

**That's the difference between a $200M exit and a $600M exit.**

**Build this right. The stakes are high.**

---

**Next steps:**
1. Team review this document
2. Decide PipelineStatus strategy (user-facing vs internal)
3. Approve tiered disclosure model
4. Build Phase 1 MVP (InsightPanel + BiomarkerChart standard modes)
5. User test with 3 physicians before broader rollout

**Questions? Need clarification on any component? Ready to decide.**
