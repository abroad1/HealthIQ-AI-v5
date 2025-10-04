# 🧠 Insight Engine Development Brief

> **Last Updated**: January 27, 2025  
> **Purpose**: Single reference point for all contributors on Insight Engine development in HealthIQ AI v5

---

## 🎯 Purpose

To define how we will implement HealthIQ AI's Insight Engines, pre-calculated rules, and supporting workflow (including questionnaire inputs) so that personalised health reports are delivered consistently, credibly, and in alignment with the v5 Intelligence Lifecycle.

---

## 🛠️ Core Principles

### 1. **Lab Ranges First**
- Always use the user's own lab reference ranges
- Never hard-code universal ranges except for derived ratios (TG:HDL, HOMA-IR, ALT:AST, NLR, etc.)

### 2. **Deterministic Engines**
- Engines perform all calculations, thresholds, and cluster detection
- LLMs never calculate, only narrate

### 3. **Confidence Transparency**
- Stage 3.5 (Data Completeness Gate) produces a confidence score
- Score reflects marker availability and sufficiency for each engine
- Propagated through to user dashboards

---

## 🧩 Workflow Overview

### **Inputs**
- **Lab Panel Upload**: Lab results with ranges and values
- **Questionnaire**: Age, sex, ethnicity, lifestyle, stress, diet, exercise, alcohol, smoking, supplements, goals

### **Pipeline Stages**

| Stage | Description | Output |
|-------|-------------|---------|
| **1. Parsing** | Extract biomarkers and ranges | Raw biomarker data |
| **2. Canonical Normalisation** | Map to canonical IDs, apply lab ranges | Normalized biomarker panel |
| **3. Data Completeness Gate** | Assign confidence scores | Confidence assessment |
| **4. Engine Execution** | Run Insight Engines | Structured JSON outputs |
| **5. Correlation Rules Layer** | Pre-calculated patterns from YAML rules | Pattern matches |
| **6. Insight Synthesis** | LLM receives structured outputs and narrates | Natural language insights |
| **7. Visualisation** | Dials, scores, cluster breakdowns | User interface elements |
| **8. Recommendations** | Behavioural/diet/supplement guidance | Actionable advice |

### **Engine Execution Details**
Each engine:
- Uses biomarkers + questionnaire context
- Applies deterministic rules (ratios, thresholds, correlations)
- Outputs structured JSON (score, severity, clusters, drivers, recommendations, confidence)

---

## 📐 Insight Engines (Initial Set)

| Engine | Primary Biomarkers | Purpose |
|--------|-------------------|---------|
| **Metabolic Age Insight** | Insulin, HbA1c, TG:HDL, ALT | Biological age assessment based on metabolic biomarkers |
| **Cardiovascular Insight** | LDL/HDL, ApoB proxies, CRP, triglycerides | Cardiovascular health and risk assessment |
| **Inflammation Insight** | CRP, NLR, ferritin/albumin | Systemic inflammation and immune health evaluation |
| **Fatigue Root Cause Insight** | Iron transport, thyroid, cortisol, vitamin D, B12 | Multi-factor fatigue analysis and root cause identification |
| **Detox & Filtration Insight** | ALT, AST, GGT, eGFR, urea:creatinine | Liver and kidney detoxification capacity assessment |

### **Engine Specifications**
- **Metabolic Age Insight**: Insulin resistance (HOMA-IR), lipid ratios, metabolic stress index
- **Cardiovascular Insight**: Lipid profile assessment, diabetes risk factors, oxygen transport efficiency
- **Inflammation Insight**: CRP levels, white blood cell analysis, anemia indicators, metabolic inflammation
- **Fatigue Root Cause Insight**: Oxygen transport, energy metabolism, organ function, lifestyle factors
- **Detox & Filtration Insight**: Kidney function, liver function, lipid processing efficiency

---

## 🧠 Questionnaire Role

### **Primary Functions**

#### **1. Normalisation**
- Confirms context (age/sex → reference ranges)
- Ensures proper biomarker interpretation

#### **2. Weighting**
- Ethnicity and lifestyle adjust severity rules in engines
- Personalizes risk assessment

#### **3. Insight Context**
- Stress, diet, alcohol, smoking, supplement use → influences interpretation
- Provides lifestyle context for biomarker analysis

#### **4. Completeness**
- Ensures missing lab data can be partly offset with context
- Improves confidence scores when biomarkers are incomplete

### **Questionnaire Data Flow**
```
Questionnaire Responses → Lifestyle Factors → Engine Context → Insight Generation
```

---

## 🚀 Development Plan

### **Phase 1: Foundation (Sprint 6)**
1. **Re-baseline Docs** ✅ (done) – Insight engines marked as scaffold only, design outline documented
2. **Implement Base Engine Contract** – Registry, DTOs, auto-discovery
3. **Define Calculation Rules** – Derived ratios, thresholds, correlation YAML

### **Phase 2: Engine Implementation (Sprint 6-7)**
4. **Build Engines Iteratively** – Implement one engine at a time with tests
   - Start with Metabolic Age Insight (highest business value)
   - Follow with Cardiovascular Insight (critical health assessment)
   - Complete with Inflammation, Fatigue, and Detox insights

### **Phase 3: Integration (Sprint 7-8)**
5. **Integrate Questionnaire** – Ensure context fields flow into engine execution
6. **Frontend Integration** – Map engine outputs → dials, confidence score, clusters, narrative

### **Implementation Priority**
- **Sprint 6**: Core modules (Metabolic Age, Heart, Inflammation)
- **Sprint 7**: Advanced modules (Fatigue, Detox) + LLM integration
- **Sprint 8**: Frontend integration and visualization

---

## 🏗️ Architectural Rules

### **Critical Enforcement Rules**

#### **1. Lab Ranges Only**
- ✅ **ALWAYS** use lab-provided reference ranges
- ❌ **NEVER** hard-code universal ranges
- ✅ **EXCEPTION**: Derived ratios/indices defined in code (TG:HDL, HOMA-IR, ALT:AST, NLR)

#### **2. Deterministic Calculations**
- ✅ **ENGINES** perform all calculations, thresholds, and cluster detection
- ❌ **LLMs** never calculate thresholds (only narrate)
- ✅ **STRUCTURED** JSON outputs from engines

#### **3. Confidence Scoring**
- ✅ **STAGE 3.5** (Data Completeness Gate) produces confidence score
- ✅ **REFLECTS** marker availability and sufficiency for each engine
- ✅ **PROPAGATED** through to user dashboards

#### **4. Integration Requirements**
- ✅ **BaseInsight** interface implementation
- ✅ **Registry** system for auto-discovery
- ✅ **Orchestrator** integration for pipeline flow
- ✅ **DTO** architecture for frontend consumption

---

## ✅ Expected Outcomes

### **Technical Outcomes**
- Engines deliver deterministic, reproducible results
- LLM narrates structured outputs, never invents thresholds
- Sub-second calculation time per engine
- ≥60% test coverage for business-critical logic

### **User Experience Outcomes**
- User sees:
  - Dials with confidence rating
  - Insight narratives
  - Clear next steps (recommendations, retesting)
- Consistent, credible health reports
- Actionable recommendations based on biomarker analysis

### **Business Outcomes**
- Clinically relevant insights
- Scalable architecture for additional engines
- Maintainable codebase with clear separation of concerns
- Production-ready implementation

---

## 📊 Success Metrics

### **Functional Requirements**
- [ ] All 5 engines implement `BaseInsight` interface
- [ ] Engines integrate with existing orchestrator
- [ ] Insights generate actionable recommendations
- [ ] Graceful degradation with missing biomarkers

### **Performance Requirements**
- [ ] Sub-second calculation time per engine
- [ ] Memory usage < 100MB per analysis
- [ ] 99.9% uptime during testing

### **Quality Requirements**
- [ ] ≥60% test coverage for business-critical logic
- [ ] Zero linting errors
- [ ] Type safety validation
- [ ] Medical accuracy validation

---

## 🔗 Related Documentation

- **Design Specification**: `docs/insight_design_outline.md`
- **Implementation Plan**: `docs/context/IMPLEMENTATION_PLAN.md`
- **Project Structure**: `docs/context/PROJECT_STRUCTURE.md`
- **Architecture Review**: `docs/ARCHITECTURE_REVIEW_REPORT.md`

---

**Document Status**: ✅ **COMPLETE**  
**Next Phase**: Engine Implementation (Sprint 6-7)  
**Dependencies**: Insight synthesis infrastructure, LLM integration  
**Estimated Implementation Time**: 4-6 weeks (2 sprints)
