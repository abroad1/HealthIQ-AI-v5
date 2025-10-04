# 🧠 Insight Module Design Outline

> **🎯 PURPOSE**: **DESIGN SPECIFICATION** - This document defines the biomarker requirements, calculation logic, and expected outputs for the 5 missing insight modules in HealthIQ AI v5.

> **Implementation Status**: Design phase only - not yet implemented. This document serves as the design baseline before coding the insight modules.

---

## 📋 Executive Summary

This document outlines the design specifications for 5 critical insight modules that are currently missing from the HealthIQ AI v5 platform:

1. **Metabolic Age Insight** - Biological age assessment based on metabolic biomarkers
2. **Heart Insight** - Cardiovascular health and risk assessment
3. **Inflammation Insight** - Systemic inflammation and immune health evaluation
4. **Fatigue Root Cause Insight** - Multi-factor fatigue analysis and root cause identification
5. **Detox Filtration Insight** - Liver and kidney detoxification capacity assessment

Each module is designed to integrate with the existing `BaseInsight` architecture and produce `BiomarkerInsight` results with actionable recommendations.

---

## 🧬 Module 1: Metabolic Age Insight

### **Purpose**
Calculate biological age based on metabolic biomarkers and compare against chronological age to identify accelerated aging patterns.

### **Required Biomarkers** (Canonical IDs from `ssot/biomarkers.yaml`)
- **Primary**: `glucose`, `hba1c`, `insulin`
- **Secondary**: `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`
- **Supporting**: `creatinine`, `bun` (for kidney function context)

### **Core Calculation Logic**

#### **Metabolic Age Score (0-100)**
```python
def calculate_metabolic_age_score(context: AnalysisContext) -> float:
    """
    Calculate metabolic age score based on biomarker patterns.
    
    Algorithm:
    1. HOMA-IR calculation: (glucose * insulin) / 405
    2. Lipid ratio: ldl_cholesterol / hdl_cholesterol
    3. Metabolic stress index: (hba1c * 10) + (triglycerides / 100)
    4. Weighted composite score with age adjustment
    """
    
    # HOMA-IR (Homeostatic Model Assessment of Insulin Resistance)
    homa_ir = (glucose * insulin) / 405
    
    # Lipid ratio (atherogenic index)
    lipid_ratio = ldl_cholesterol / hdl_cholesterol if hdl_cholesterol > 0 else 10
    
    # Metabolic stress index
    metabolic_stress = (hba1c * 10) + (triglycerides / 100)
    
    # Age-adjusted scoring
    chronological_age = context.user.age
    age_factor = min(chronological_age / 50, 1.2)  # Normalize to 50-year baseline
    
    # Composite score calculation
    score = (
        (homa_ir * 0.3) +           # Insulin resistance weight
        (lipid_ratio * 0.25) +      # Lipid profile weight
        (metabolic_stress * 0.2) +  # Metabolic stress weight
        (age_factor * 0.25)         # Age adjustment weight
    ) * 20  # Scale to 0-100
    
    return min(max(score, 0), 100)
```

#### **Biological Age Calculation**
```python
def calculate_biological_age(metabolic_score: float, chronological_age: int) -> int:
    """
    Calculate biological age based on metabolic score.
    
    Formula: biological_age = chronological_age + (metabolic_score - 50) * 0.8
    """
    age_difference = (metabolic_score - 50) * 0.8
    return int(chronological_age + age_difference)
```

### **Severity Levels**
- **Optimal (0-30)**: Biological age ≤ chronological age
- **Good (31-50)**: Biological age ≤ chronological age + 2 years
- **Moderate (51-70)**: Biological age ≤ chronological age + 5 years
- **Poor (71-85)**: Biological age ≤ chronological age + 10 years
- **Critical (86-100)**: Biological age > chronological age + 10 years

### **Biomarker Dependencies**
- **HOMA-IR**: Requires both `glucose` and `insulin` (fasting values preferred)
- **Lipid Ratio**: Requires both `ldl_cholesterol` and `hdl_cholesterol`
- **Metabolic Stress**: Can calculate with `hba1c` alone, enhanced with `triglycerides`

### **Expected Outputs** (InsightResult fields)
```python
{
    "insight_id": "metabolic_age_001",
    "title": "Metabolic Age Assessment",
    "description": f"Your biological age is {biological_age} years vs chronological age of {chronological_age} years, indicating {'accelerated' if biological_age > chronological_age else 'slowed'} aging.",
    "category": "metabolic",
    "confidence": 0.85,  # Based on biomarker completeness
    "severity": "moderate",  # Based on score
    "biomarkers": ["glucose", "hba1c", "insulin", "ldl_cholesterol", "hdl_cholesterol"],
    "recommendations": [
        "Consider intermittent fasting to improve insulin sensitivity",
        "Increase omega-3 fatty acids to improve lipid profile",
        "Regular exercise to enhance metabolic flexibility"
    ]
}
```

---

## ❤️ Module 2: Heart Insight

### **Purpose**
Comprehensive cardiovascular health assessment focusing on heart function, arterial health, and cardiovascular risk factors.

### **Required Biomarkers** (Canonical IDs from `ssot/biomarkers.yaml`)
- **Primary**: `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`, `triglycerides`
- **Secondary**: `glucose`, `hba1c` (for diabetes risk)
- **Supporting**: `hemoglobin`, `hematocrit` (for oxygen transport)

### **Core Calculation Logic**

#### **Cardiovascular Risk Score (0-100)**
```python
def calculate_heart_insight_score(context: AnalysisContext) -> float:
    """
    Calculate cardiovascular health score based on lipid profile and risk factors.
    
    Algorithm:
    1. Lipid profile assessment (LDL/HDL ratio, total cholesterol)
    2. Triglyceride risk assessment
    3. Diabetes risk factor (glucose/HbA1c)
    4. Oxygen transport efficiency (hemoglobin/hematocrit)
    """
    
    # Lipid profile score (0-40 points)
    ldl_hdl_ratio = ldl_cholesterol / hdl_cholesterol if hdl_cholesterol > 0 else 10
    lipid_score = max(0, 40 - (ldl_hdl_ratio * 8))  # Optimal ratio < 2.5
    
    # Triglyceride score (0-20 points)
    trig_score = max(0, 20 - (triglycerides / 25))  # Optimal < 150 mg/dL
    
    # Diabetes risk score (0-20 points)
    diabetes_risk = 0
    if glucose > 100:  # Pre-diabetes threshold
        diabetes_risk += 10
    if hba1c > 5.7:  # Pre-diabetes HbA1c
        diabetes_risk += 10
    diabetes_score = max(0, 20 - diabetes_risk)
    
    # Oxygen transport score (0-20 points)
    oxygen_score = 20  # Default optimal
    if hemoglobin < 12:  # Anemia threshold
        oxygen_score -= 10
    if hematocrit < 36:  # Low hematocrit
        oxygen_score -= 10
    
    total_score = lipid_score + trig_score + diabetes_score + oxygen_score
    return min(max(total_score, 0), 100)
```

#### **Risk Category Classification**
```python
def classify_heart_risk(score: float) -> str:
    """Classify cardiovascular risk based on score."""
    if score >= 80:
        return "low"
    elif score >= 60:
        return "moderate"
    elif score >= 40:
        return "high"
    else:
        return "very_high"
```

### **Severity Levels**
- **Excellent (80-100)**: Low cardiovascular risk
- **Good (60-79)**: Moderate risk, lifestyle improvements recommended
- **Fair (40-59)**: High risk, medical consultation advised
- **Poor (20-39)**: Very high risk, immediate medical attention
- **Critical (0-19)**: Extremely high risk, urgent medical intervention

### **Biomarker Dependencies**
- **Lipid Profile**: Requires `total_cholesterol`, `ldl_cholesterol`, `hdl_cholesterol`
- **Triglyceride Assessment**: Independent calculation
- **Diabetes Risk**: Enhanced with both `glucose` and `hba1c`
- **Oxygen Transport**: Requires `hemoglobin` and `hematocrit`

### **Expected Outputs** (InsightResult fields)
```python
{
    "insight_id": "heart_insight_001",
    "title": "Cardiovascular Health Assessment",
    "description": f"Your cardiovascular risk is {risk_category} with a score of {score}/100. Key factors: LDL/HDL ratio {ldl_hdl_ratio:.1f}, triglycerides {triglycerides} mg/dL.",
    "category": "cardiovascular",
    "confidence": 0.90,  # Based on biomarker completeness
    "severity": "moderate",  # Based on risk category
    "biomarkers": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol", "triglycerides"],
    "recommendations": [
        "Consider Mediterranean diet to improve lipid profile",
        "Regular aerobic exercise to strengthen heart muscle",
        "Monitor blood pressure regularly",
        "Consider omega-3 supplementation"
    ]
}
```

---

## 🔥 Module 3: Inflammation Insight

### **Purpose**
Assess systemic inflammation levels and immune system health using inflammatory markers and supporting biomarkers.

### **Required Biomarkers** (Canonical IDs from `ssot/biomarkers.yaml`)
- **Primary**: `crp` (C-reactive protein)
- **Secondary**: `white_blood_cells`, `hemoglobin`, `hematocrit`
- **Supporting**: `glucose`, `hba1c` (for metabolic inflammation)

### **Core Calculation Logic**

#### **Inflammation Score (0-100)**
```python
def calculate_inflammation_score(context: AnalysisContext) -> float:
    """
    Calculate systemic inflammation score based on inflammatory markers.
    
    Algorithm:
    1. CRP level assessment (primary inflammatory marker)
    2. White blood cell count analysis
    3. Anemia indicators (hemoglobin/hematocrit)
    4. Metabolic inflammation (glucose/HbA1c)
    """
    
    # CRP score (0-40 points) - Primary inflammatory marker
    crp_score = 40  # Start with optimal
    if crp > 3.0:  # High risk threshold
        crp_score -= 30
    elif crp > 1.0:  # Moderate risk threshold
        crp_score -= 15
    elif crp > 0.3:  # Low risk threshold
        crp_score -= 5
    
    # White blood cell score (0-25 points)
    wbc_score = 25  # Start with optimal
    if white_blood_cells > 11.0:  # High WBC (infection/inflammation)
        wbc_score -= 15
    elif white_blood_cells < 4.0:  # Low WBC (immune suppression)
        wbc_score -= 10
    elif white_blood_cells > 10.0:  # Elevated WBC
        wbc_score -= 5
    
    # Anemia score (0-20 points) - Chronic inflammation can cause anemia
    anemia_score = 20  # Start with optimal
    if hemoglobin < 12:  # Anemia threshold
        anemia_score -= 10
    if hematocrit < 36:  # Low hematocrit
        anemia_score -= 10
    
    # Metabolic inflammation score (0-15 points)
    metabolic_score = 15  # Start with optimal
    if glucose > 100:  # Pre-diabetes (metabolic inflammation)
        metabolic_score -= 8
    if hba1c > 5.7:  # Pre-diabetes HbA1c
        metabolic_score -= 7
    
    total_score = crp_score + wbc_score + anemia_score + metabolic_score
    return min(max(total_score, 0), 100)
```

#### **Inflammation Category Classification**
```python
def classify_inflammation_level(score: float) -> str:
    """Classify inflammation level based on score."""
    if score >= 80:
        return "low"
    elif score >= 60:
        return "moderate"
    elif score >= 40:
        return "high"
    else:
        return "very_high"
```

### **Severity Levels**
- **Optimal (80-100)**: Low systemic inflammation
- **Good (60-79)**: Moderate inflammation, lifestyle improvements recommended
- **Fair (40-59)**: High inflammation, medical consultation advised
- **Poor (20-39)**: Very high inflammation, immediate attention needed
- **Critical (0-19)**: Extremely high inflammation, urgent medical intervention

### **Biomarker Dependencies**
- **Primary**: `crp` (essential for inflammation assessment)
- **Immune Function**: `white_blood_cells` (infection/inflammation indicator)
- **Anemia Indicators**: `hemoglobin`, `hematocrit` (chronic inflammation markers)
- **Metabolic Inflammation**: `glucose`, `hba1c` (diabetes-related inflammation)

### **Expected Outputs** (InsightResult fields)
```python
{
    "insight_id": "inflammation_insight_001",
    "title": "Systemic Inflammation Assessment",
    "description": f"Your inflammation level is {inflammation_level} with a score of {score}/100. CRP: {crp} mg/L, WBC: {white_blood_cells} K/μL.",
    "category": "inflammatory",
    "confidence": 0.75,  # Based on biomarker completeness
    "severity": "moderate",  # Based on inflammation level
    "biomarkers": ["crp", "white_blood_cells", "hemoglobin", "hematocrit"],
    "recommendations": [
        "Consider anti-inflammatory diet (Mediterranean, DASH)",
        "Regular exercise to reduce chronic inflammation",
        "Stress management techniques (meditation, yoga)",
        "Consider omega-3 and turmeric supplementation"
    ]
}
```

---

## 😴 Module 4: Fatigue Root Cause Insight

### **Purpose**
Identify potential root causes of fatigue by analyzing multiple biomarker systems that contribute to energy production and utilization.

### **Required Biomarkers** (Canonical IDs from `ssot/biomarkers.yaml`)
- **Primary**: `hemoglobin`, `hematocrit` (oxygen transport)
- **Secondary**: `glucose`, `hba1c`, `insulin` (energy metabolism)
- **Supporting**: `creatinine`, `bun` (kidney function), `alt`, `ast` (liver function)

### **Core Calculation Logic**

#### **Fatigue Root Cause Score (0-100)**
```python
def calculate_fatigue_insight_score(context: AnalysisContext) -> float:
    """
    Calculate fatigue root cause score based on multiple biomarker systems.
    
    Algorithm:
    1. Oxygen transport efficiency (hemoglobin/hematocrit)
    2. Energy metabolism (glucose/insulin/HbA1c)
    3. Organ function (kidney/liver markers)
    4. Composite fatigue risk assessment
    """
    
    # Oxygen transport score (0-35 points) - Primary fatigue cause
    oxygen_score = 35  # Start with optimal
    if hemoglobin < 12:  # Anemia threshold
        oxygen_score -= 20
    elif hemoglobin < 13:  # Mild anemia
        oxygen_score -= 10
    if hematocrit < 36:  # Low hematocrit
        oxygen_score -= 15
    elif hematocrit < 40:  # Mild low hematocrit
        oxygen_score -= 8
    
    # Energy metabolism score (0-30 points)
    energy_score = 30  # Start with optimal
    if glucose > 100:  # Pre-diabetes (energy dysregulation)
        energy_score -= 10
    if hba1c > 5.7:  # Pre-diabetes HbA1c
        energy_score -= 8
    if insulin > 25:  # High insulin (insulin resistance)
        energy_score -= 12
    
    # Organ function score (0-25 points)
    organ_score = 25  # Start with optimal
    if creatinine > 1.2:  # Kidney function impairment
        organ_score -= 10
    if bun > 20:  # High BUN (kidney stress)
        organ_score -= 8
    if alt > 40:  # Liver function impairment
        organ_score -= 7
    
    # Lifestyle factors (0-10 points) - From questionnaire
    lifestyle_score = 10  # Start with optimal
    if context.lifestyle_factors:
        if context.lifestyle_factors.get('sleep_quality', 'good') == 'poor':
            lifestyle_score -= 5
        if context.lifestyle_factors.get('stress_level', 'low') == 'high':
            lifestyle_score -= 3
        if context.lifestyle_factors.get('exercise_frequency', 'regular') == 'sedentary':
            lifestyle_score -= 2
    
    total_score = oxygen_score + energy_score + organ_score + lifestyle_score
    return min(max(total_score, 0), 100)
```

#### **Root Cause Classification**
```python
def classify_fatigue_root_cause(score: float, biomarkers: Dict) -> str:
    """Classify primary fatigue root cause based on score and biomarker patterns."""
    if score >= 80:
        return "optimal_energy"
    elif score >= 60:
        return "mild_fatigue"
    elif score >= 40:
        return "moderate_fatigue"
    else:
        return "severe_fatigue"
```

### **Severity Levels**
- **Optimal (80-100)**: Excellent energy levels, no fatigue concerns
- **Good (60-79)**: Mild fatigue, minor lifestyle adjustments needed
- **Fair (40-59)**: Moderate fatigue, medical consultation recommended
- **Poor (20-39)**: Severe fatigue, immediate attention needed
- **Critical (0-19)**: Extreme fatigue, urgent medical intervention

### **Biomarker Dependencies**
- **Oxygen Transport**: `hemoglobin`, `hematocrit` (essential for energy production)
- **Energy Metabolism**: `glucose`, `hba1c`, `insulin` (cellular energy)
- **Organ Function**: `creatinine`, `bun`, `alt`, `ast` (detoxification and energy)
- **Lifestyle Factors**: Questionnaire data (sleep, stress, exercise)

### **Expected Outputs** (InsightResult fields)
```python
{
    "insight_id": "fatigue_insight_001",
    "title": "Fatigue Root Cause Analysis",
    "description": f"Your fatigue level is {fatigue_level} with a score of {score}/100. Primary contributors: {'oxygen transport' if hemoglobin < 12 else 'energy metabolism' if glucose > 100 else 'organ function'}.",
    "category": "energy",
    "confidence": 0.80,  # Based on biomarker completeness
    "severity": "moderate",  # Based on fatigue level
    "biomarkers": ["hemoglobin", "hematocrit", "glucose", "hba1c", "insulin"],
    "recommendations": [
        "Address iron deficiency if hemoglobin is low",
        "Optimize blood sugar levels through diet and exercise",
        "Improve sleep quality and stress management",
        "Consider B-complex vitamins for energy metabolism"
    ]
}
```

---

## 🧹 Module 5: Detox Filtration Insight

### **Purpose**
Assess liver and kidney detoxification capacity and overall filtration efficiency of the body's waste removal systems.

### **Required Biomarkers** (Canonical IDs from `ssot/biomarkers.yaml`)
- **Primary**: `creatinine`, `bun` (kidney function)
- **Secondary**: `alt`, `ast` (liver function)
- **Supporting**: `total_cholesterol`, `triglycerides` (liver lipid processing)

### **Core Calculation Logic**

#### **Detox Filtration Score (0-100)**
```python
def calculate_detox_insight_score(context: AnalysisContext) -> float:
    """
    Calculate detoxification and filtration capacity score.
    
    Algorithm:
    1. Kidney function assessment (creatinine, BUN)
    2. Liver function assessment (ALT, AST)
    3. Lipid processing efficiency (cholesterol, triglycerides)
    4. Overall detoxification capacity
    """
    
    # Kidney function score (0-40 points)
    kidney_score = 40  # Start with optimal
    if creatinine > 1.2:  # Kidney function impairment
        kidney_score -= 20
    elif creatinine > 1.0:  # Mild kidney stress
        kidney_score -= 10
    if bun > 20:  # High BUN (kidney stress)
        kidney_score -= 15
    elif bun > 15:  # Mild BUN elevation
        kidney_score -= 8
    
    # Liver function score (0-35 points)
    liver_score = 35  # Start with optimal
    if alt > 40:  # Liver function impairment
        liver_score -= 20
    elif alt > 30:  # Mild liver stress
        liver_score -= 10
    if ast > 40:  # Liver function impairment
        liver_score -= 15
    elif ast > 30:  # Mild liver stress
        liver_score -= 8
    
    # Lipid processing score (0-25 points)
    lipid_score = 25  # Start with optimal
    if total_cholesterol > 200:  # High cholesterol (liver processing)
        lipid_score -= 10
    if triglycerides > 150:  # High triglycerides (liver processing)
        lipid_score -= 15
    
    total_score = kidney_score + liver_score + lipid_score
    return min(max(total_score, 0), 100)
```

#### **Detoxification Category Classification**
```python
def classify_detox_capacity(score: float) -> str:
    """Classify detoxification capacity based on score."""
    if score >= 80:
        return "excellent"
    elif score >= 60:
        return "good"
    elif score >= 40:
        return "moderate"
    else:
        return "poor"
```

### **Severity Levels**
- **Excellent (80-100)**: Optimal detoxification and filtration
- **Good (60-79)**: Good function, minor optimizations recommended
- **Fair (40-59)**: Moderate impairment, lifestyle changes needed
- **Poor (20-39)**: Significant impairment, medical consultation advised
- **Critical (0-19)**: Severe impairment, urgent medical attention

### **Biomarker Dependencies**
- **Kidney Function**: `creatinine`, `bun` (essential for waste filtration)
- **Liver Function**: `alt`, `ast` (essential for toxin processing)
- **Lipid Processing**: `total_cholesterol`, `triglycerides` (liver efficiency)
- **Supporting**: Additional liver markers if available

### **Expected Outputs** (InsightResult fields)
```python
{
    "insight_id": "detox_insight_001",
    "title": "Detoxification & Filtration Assessment",
    "description": f"Your detoxification capacity is {detox_capacity} with a score of {score}/100. Kidney function: {'optimal' if creatinine < 1.0 else 'impaired'}, Liver function: {'optimal' if alt < 30 else 'stressed'}.",
    "category": "detoxification",
    "confidence": 0.85,  # Based on biomarker completeness
    "severity": "moderate",  # Based on detox capacity
    "biomarkers": ["creatinine", "bun", "alt", "ast", "total_cholesterol"],
    "recommendations": [
        "Increase water intake to support kidney function",
        "Consider liver-supporting herbs (milk thistle, dandelion)",
        "Reduce processed foods and alcohol consumption",
        "Regular exercise to support lymphatic drainage"
    ]
}
```

---

## 🔧 Implementation Architecture

### **Module Integration Requirements**

#### **BaseInsight Implementation**
Each module must implement the `BaseInsight` abstract class:

```python
class MetabolicAgeInsight(BaseInsight):
    def get_required_biomarkers(self) -> List[str]:
        return ["glucose", "hba1c", "insulin", "ldl_cholesterol", "hdl_cholesterol"]
    
    def analyze(self, context: AnalysisContext) -> List[BiomarkerInsight]:
        # Implementation logic here
        pass
    
    def get_insight_category(self) -> str:
        return "metabolic"
```

#### **Registry Integration**
All modules must be registered in the `InsightRegistry`:

```python
# In core/insights/__init__.py
from .modules.metabolic_age import MetabolicAgeInsight
from .modules.heart_insight import HeartInsight
from .modules.inflammation_insight import InflammationInsight
from .modules.fatigue_insight import FatigueInsight
from .modules.detox_insight import DetoxInsight

# Register all insight modules
insight_registry.register(MetabolicAgeInsight)
insight_registry.register(HeartInsight)
insight_registry.register(InflammationInsight)
insight_registry.register(FatigueInsight)
insight_registry.register(DetoxInsight)
```

### **Data Flow Integration**

#### **Orchestrator Integration**
Modules integrate with the existing pipeline orchestrator:

```python
# In core/pipeline/orchestrator.py
def generate_insights(self, context: AnalysisContext) -> List[BiomarkerInsight]:
    """Generate insights using all registered modules."""
    insights = []
    
    for insight_module in insight_registry.get_all_insights():
        if insight_module.can_analyze(context):
            module_insights = insight_module.analyze(context)
            insights.extend(module_insights)
    
    return insights
```

#### **DTO Integration**
Insights flow through the existing DTO architecture:

```python
# In core/dto/builders.py
def build_insight_dto(insight: BiomarkerInsight) -> InsightResult:
    """Convert BiomarkerInsight to InsightResult DTO."""
    return InsightResult(
        insight_id=insight.insight_id,
        title=insight.title,
        description=insight.description,
        category=insight.category,
        confidence=insight.confidence,
        severity=insight.severity,
        biomarkers=insight.biomarkers,
        recommendations=insight.recommendations
    )
```

---

## 📊 Biomarker Coverage Analysis

### **Required Biomarker Summary**
- **Total Unique Biomarkers**: 12
- **Primary Biomarkers**: 8 (essential for core functionality)
- **Secondary Biomarkers**: 4 (enhance accuracy and confidence)

### **Biomarker Usage Matrix**
| Biomarker | Metabolic Age | Heart | Inflammation | Fatigue | Detox |
|-----------|---------------|-------|--------------|---------|-------|
| glucose | ✅ Primary | ✅ Secondary | ✅ Supporting | ✅ Secondary | ❌ |
| hba1c | ✅ Primary | ✅ Secondary | ✅ Supporting | ✅ Secondary | ❌ |
| insulin | ✅ Primary | ❌ | ❌ | ✅ Secondary | ❌ |
| total_cholesterol | ✅ Secondary | ✅ Primary | ❌ | ❌ | ✅ Supporting |
| ldl_cholesterol | ✅ Secondary | ✅ Primary | ❌ | ❌ | ❌ |
| hdl_cholesterol | ✅ Secondary | ✅ Primary | ❌ | ❌ | ❌ |
| triglycerides | ✅ Secondary | ✅ Primary | ❌ | ❌ | ✅ Supporting |
| crp | ❌ | ❌ | ✅ Primary | ❌ | ❌ |
| hemoglobin | ❌ | ✅ Supporting | ✅ Secondary | ✅ Primary | ❌ |
| hematocrit | ❌ | ✅ Supporting | ✅ Secondary | ✅ Primary | ❌ |
| white_blood_cells | ❌ | ❌ | ✅ Secondary | ❌ | ❌ |
| creatinine | ✅ Supporting | ❌ | ❌ | ✅ Supporting | ✅ Primary |
| bun | ✅ Supporting | ❌ | ❌ | ✅ Supporting | ✅ Primary |
| alt | ❌ | ❌ | ❌ | ✅ Supporting | ✅ Secondary |
| ast | ❌ | ❌ | ❌ | ✅ Supporting | ✅ Secondary |

### **Coverage Requirements**
- **Minimum Biomarkers**: 3 per module for basic functionality
- **Optimal Biomarkers**: 5+ per module for high confidence
- **Fallback Logic**: Graceful degradation when biomarkers are missing

---

## 🧪 Testing Strategy

### **High-Value Test Scenarios**
Each module requires comprehensive testing for:

1. **Biomarker Completeness**: Test with missing biomarkers
2. **Score Calculation**: Validate mathematical accuracy
3. **Severity Classification**: Test threshold boundaries
4. **Recommendation Generation**: Ensure actionable advice
5. **Integration Testing**: Verify orchestrator integration

### **Test Coverage Requirements**
- **Unit Tests**: ≥60% coverage for business-critical logic
- **Integration Tests**: Full pipeline integration
- **Edge Cases**: Missing biomarkers, extreme values
- **Performance Tests**: Sub-second calculation time

### **Test Documentation**
All high-value tests must be documented in `TEST_LEDGER.md` with:
- Business justification
- Run commands
- Expected outcomes
- Failure impact analysis

---

## 🚀 Implementation Priority

### **Phase 1: Core Modules (Sprint 6)**
1. **Metabolic Age Insight** - Highest business value
2. **Heart Insight** - Critical health assessment
3. **Inflammation Insight** - Important for overall health

### **Phase 2: Advanced Modules (Sprint 7)**
4. **Fatigue Root Cause Insight** - Complex multi-factor analysis
5. **Detox Filtration Insight** - Organ function assessment

### **Dependencies**
- **Sprint 6**: Insight synthesis infrastructure
- **Sprint 7**: LLM integration for enhanced recommendations
- **Sprint 8**: Frontend integration and visualization

---

## 📋 Success Criteria

### **Functional Requirements**
- [ ] All 5 modules implement `BaseInsight` interface
- [ ] Modules integrate with existing orchestrator
- [ ] Insights generate actionable recommendations
- [ ] Graceful degradation with missing biomarkers

### **Performance Requirements**
- [ ] Sub-second calculation time per module
- [ ] Memory usage < 100MB per analysis
- [ ] 99.9% uptime during testing

### **Quality Requirements**
- [ ] ≥60% test coverage for business-critical logic
- [ ] Zero linting errors
- [ ] Type safety validation
- [ ] Medical accuracy validation

---

**Design Document Status**: ✅ **COMPLETE**  
**Next Phase**: Implementation in Sprint 6-7  
**Dependencies**: Insight synthesis infrastructure, LLM integration  
**Estimated Implementation Time**: 4-6 weeks (2 sprints)
