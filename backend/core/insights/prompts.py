"""
Insight generation prompt templates - structured prompts for LLM-based insight synthesis.
"""

from typing import Dict, List, Any
from core.models.insight import InsightTemplate


class InsightPromptTemplates:
    """Collection of structured prompt templates for insight generation."""
    
    # Base system prompt for all insight generation
    SYSTEM_PROMPT = """You are a clinical biomarker analysis expert. Your role is to generate clinically meaningful insights by combining biomarker scores, clustering results, and lifestyle context.

Key requirements:
1. Generate insights that are clinically relevant and actionable
2. Base insights on biomarker patterns and lifestyle factors
3. Provide structured, explainable insights (no free-text advice)
4. Include confidence scores based on data quality and biomarker coverage
5. Focus on patterns that indicate health risks or opportunities

Output format: Always return insights in the specified JSON structure."""

    # Metabolic health insight template
    METABOLIC_INSIGHT_TEMPLATE = """
Analyze the following metabolic biomarker data and lifestyle factors to generate insights:

**Biomarker Scores:**
{biomarker_scores}

**Lifestyle Profile:**
- Diet Level: {diet_level}
- Exercise: {exercise_minutes_per_week} minutes/week
- Sleep: {sleep_hours} hours/night
- Stress Level: {stress_level}
- Smoking Status: {smoking_status}
- Smoking Status: {smoking_status}

**Clustering Results:**
{clustering_results}

Generate 1-3 metabolic health insights focusing on:
- Insulin resistance patterns (glucose, hba1c, insulin markers)
- Metabolic syndrome indicators
- Lifestyle impact on metabolic markers
- Risk factors and protective factors

Return insights in this JSON format:
{{
    "insights": [
        {{
            "id": "metabolic_insight_1",
            "category": "metabolic",
            "summary": "Brief summary of the insight",
            "evidence": {{
                "biomarkers": ["glucose", "hba1c", "insulin", "relevant", "biomarkers"],
                "scores": {{"biomarker_name": score_value}},
                "lifestyle_factors": ["relevant", "lifestyle", "factors"]
            }},
            "confidence": 0.85,
            "severity": "warning",
            "recommendations": ["actionable", "recommendation", "1", "actionable", "recommendation", "2"],
            "biomarkers_involved": ["biomarker1", "biomarker2"],
            "lifestyle_factors": ["diet", "exercise"]
        }}
    ]
}}
"""

    # Cardiovascular health insight template
    CARDIOVASCULAR_INSIGHT_TEMPLATE = """
Analyze the following cardiovascular biomarker data and lifestyle factors to generate insights:

**Biomarker Scores:**
{biomarker_scores}

**Lifestyle Profile:**
- Diet Level: {diet_level}
- Exercise: {exercise_minutes_per_week} minutes/week
- Sleep: {sleep_hours} hours/night
- Smoking Status: {smoking_status}
- Stress Level: {stress_level}

**Clustering Results:**
{clustering_results}

Generate 1-3 cardiovascular health insights focusing on:
- Heart disease risk factors
- Cholesterol and lipid patterns
- Lifestyle impact on cardiovascular markers
- Risk stratification and prevention opportunities

Return insights in this JSON format:
{{
    "insights": [
        {{
            "id": "cardiovascular_insight_1",
            "category": "cardiovascular",
            "summary": "Brief summary of the insight",
            "evidence": {{
                "biomarkers": ["total_cholesterol", "ldl_cholesterol", "hdl_cholesterol", "relevant", "biomarkers"],
                "scores": {{"biomarker_name": score_value}},
                "lifestyle_factors": ["relevant", "lifestyle", "factors"]
            }},
            "confidence": 0.85,
            "severity": "warning",
            "recommendations": ["actionable", "recommendation", "1", "actionable", "recommendation", "2"],
            "biomarkers_involved": ["biomarker1", "biomarker2"],
            "lifestyle_factors": ["diet", "exercise"]
        }}
    ]
}}
"""

    # Inflammatory health insight template
    INFLAMMATORY_INSIGHT_TEMPLATE = """
Analyze the following inflammatory biomarker data and lifestyle factors to generate insights:

**Biomarker Scores:**
{biomarker_scores}

**Lifestyle Profile:**
- Diet Level: {diet_level}
- Exercise: {exercise_minutes_per_week} minutes/week
- Sleep: {sleep_hours} hours/night
- Stress Level: {stress_level}
- Smoking Status: {smoking_status}

**Clustering Results:**
{clustering_results}

Generate 1-3 inflammatory health insights focusing on:
- Chronic inflammation patterns (CRP, ESR markers)
- Lifestyle impact on inflammatory markers
- Risk factors for inflammatory conditions
- Anti-inflammatory lifestyle opportunities

Return insights in this JSON format:
{{
    "insights": [
        {{
            "id": "inflammatory_insight_1",
            "category": "inflammatory",
            "summary": "Brief summary of the insight",
            "evidence": {{
                "biomarkers": ["crp", "esr", "relevant", "biomarkers"],
                "scores": {{"biomarker_name": score_value}},
                "lifestyle_factors": ["relevant", "lifestyle", "factors"]
            }},
            "confidence": 0.85,
            "severity": "warning",
            "recommendations": ["actionable", "recommendation", "1", "actionable", "recommendation", "2"],
            "biomarkers_involved": ["biomarker1", "biomarker2"],
            "lifestyle_factors": ["diet", "exercise"]
        }}
    ]
}}
"""

    # Organ health insight template
    ORGAN_INSIGHT_TEMPLATE = """
Analyze the following organ health biomarker data and lifestyle factors to generate insights:

**Biomarker Scores:**
{biomarker_scores}

**Lifestyle Profile:**
- Diet Level: {diet_level}
- Exercise: {exercise_minutes_per_week} minutes/week
- Sleep: {sleep_hours} hours/night
- Stress Level: {stress_level}
- Smoking Status: {smoking_status}
- Alcohol: {alcohol_units_per_week} units/week

**Clustering Results:**
{clustering_results}

Generate 1-3 organ health insights focusing on:
- Liver function patterns (ALT, AST, GGT markers)
- Kidney function indicators
- Organ stress and damage markers
- Lifestyle impact on organ health

Return insights in this JSON format:
{{
    "insights": [
        {{
            "id": "organ_insight_1",
            "category": "organ",
            "summary": "Brief summary of the insight",
            "evidence": {{
                "biomarkers": ["alt", "ast", "ggt", "relevant", "biomarkers"],
                "scores": {{"biomarker_name": score_value}},
                "lifestyle_factors": ["relevant", "lifestyle", "factors"]
            }},
            "confidence": 0.85,
            "severity": "warning",
            "recommendations": ["actionable", "recommendation", "1", "actionable", "recommendation", "2"],
            "biomarkers_involved": ["biomarker1", "biomarker2"],
            "lifestyle_factors": ["diet", "exercise"]
        }}
    ]
}}
"""

    # Nutritional health insight template
    NUTRITIONAL_INSIGHT_TEMPLATE = """
Analyze the following nutritional biomarker data and lifestyle factors to generate insights:

**Biomarker Scores:**
{biomarker_scores}

**Lifestyle Profile:**
- Diet Level: {diet_level}
- Exercise: {exercise_minutes_per_week} minutes/week
- Sleep: {sleep_hours} hours/night
- Stress Level: {stress_level}
- Smoking Status: {smoking_status}

**Clustering Results:**
{clustering_results}

Generate 1-3 nutritional health insights focusing on:
- Vitamin and mineral status
- Nutritional deficiency assessment and excesses
- Lifestyle impact on nutritional markers
- Dietary optimization opportunities

Return insights in this JSON format:
{{
    "insights": [
        {{
            "id": "nutritional_insight_1",
            "category": "nutritional",
            "summary": "Brief summary of the insight",
            "evidence": {{
                "biomarkers": ["vitamin_d", "b12", "folate", "relevant", "biomarkers"],
                "scores": {{"biomarker_name": score_value}},
                "lifestyle_factors": ["relevant", "lifestyle", "factors"]
            }},
            "confidence": 0.85,
            "severity": "warning",
            "recommendations": ["actionable", "recommendation", "1", "actionable", "recommendation", "2"],
            "biomarkers_involved": ["biomarker1", "biomarker2"],
            "lifestyle_factors": ["diet", "exercise"]
        }}
    ]
}}
"""

    # Hormonal health insight template
    HORMONAL_INSIGHT_TEMPLATE = """
Analyze the following hormonal biomarker data and lifestyle factors to generate insights:

**Biomarker Scores:**
{biomarker_scores}

**Lifestyle Profile:**
- Diet Level: {diet_level}
- Exercise: {exercise_minutes_per_week} minutes/week
- Sleep: {sleep_hours} hours/night
- Stress Level: {stress_level}
- Smoking Status: {smoking_status}

**Clustering Results:**
{clustering_results}

Generate 1-3 hormonal health insights focusing on:
- Hormonal balance patterns
- Stress hormone indicators (cortisol, testosterone, estradiol)
- Lifestyle impact on hormonal markers
- Hormonal optimization opportunities

Return insights in this JSON format:
{{
    "insights": [
        {{
            "id": "hormonal_insight_1",
            "category": "hormonal",
            "summary": "Brief summary of the insight",
            "evidence": {{
                "biomarkers": ["cortisol", "testosterone", "estradiol", "relevant", "biomarkers"],
                "scores": {{"biomarker_name": score_value}},
                "lifestyle_factors": ["relevant", "lifestyle", "factors"]
            }},
            "confidence": 0.85,
            "severity": "warning",
            "recommendations": ["actionable", "recommendation", "1", "actionable", "recommendation", "2"],
            "biomarkers_involved": ["biomarker1", "biomarker2"],
            "lifestyle_factors": ["diet", "exercise"]
        }}
    ]
}}
"""

    @classmethod
    def get_template(cls, category: str) -> str:
        """
        Get prompt template for a specific health category.
        
        Args:
            category: Health category (metabolic, cardiovascular, inflammatory, etc.)
            
        Returns:
            Prompt template string
            
        Raises:
            ValueError: If category not supported
        """
        templates = {
            "metabolic": cls.METABOLIC_INSIGHT_TEMPLATE,
            "cardiovascular": cls.CARDIOVASCULAR_INSIGHT_TEMPLATE,
            "inflammatory": cls.INFLAMMATORY_INSIGHT_TEMPLATE,
            "organ": cls.ORGAN_INSIGHT_TEMPLATE,
            "nutritional": cls.NUTRITIONAL_INSIGHT_TEMPLATE,
            "hormonal": cls.HORMONAL_INSIGHT_TEMPLATE
        }
        
        if category not in templates:
            raise ValueError(f"Unsupported insight category: {category}")
        
        return templates[category]
    
    @classmethod
    def get_system_prompt(cls) -> str:
        """
        Get the system prompt for insight generation.
        
        Returns:
            System prompt string
        """
        return cls.SYSTEM_PROMPT
    
    @classmethod
    def get_supported_categories(cls) -> List[str]:
        """
        Get list of supported health categories.
        
        Returns:
            List of supported categories
        """
        return ["metabolic", "cardiovascular", "inflammatory", "organ", "nutritional", "hormonal"]
    
    @classmethod
    def format_template(
        cls, 
        category: str, 
        biomarker_scores: Dict[str, Any],
        lifestyle_profile: Dict[str, Any],
        clustering_results: Dict[str, Any]
    ) -> str:
        """
        Format a prompt template with actual data.
        
        Args:
            category: Health category
            biomarker_scores: Biomarker scoring results
            lifestyle_profile: User lifestyle profile
            clustering_results: Clustering analysis results
            
        Returns:
            Formatted prompt string
        """
        template = cls.get_template(category)
        
        # Format the template with provided data
        formatted_prompt = template.format(
            biomarker_scores=biomarker_scores,
            diet_level=lifestyle_profile.get("diet_level", "average"),
            exercise_minutes_per_week=lifestyle_profile.get("exercise_minutes_per_week", 150),
            sleep_hours=lifestyle_profile.get("sleep_hours", 7.0),
            stress_level=lifestyle_profile.get("stress_level", "average"),
            smoking_status=lifestyle_profile.get("smoking_status", "never"),
            alcohol_units_per_week=lifestyle_profile.get("alcohol_units_per_week", 5),
            clustering_results=clustering_results
        )
        
        return formatted_prompt


def create_insight_templates() -> List[InsightTemplate]:
    """
    Create insight template objects for all supported categories.
    
    Returns:
        List of InsightTemplate objects
    """
    templates = []
    
    for category in InsightPromptTemplates.get_supported_categories():
        template = InsightTemplate(
            template_id=f"{category}_insight_template",
            name=f"{category.title()} Health Insight Template",
            category=category,
            prompt_template=InsightPromptTemplates.get_template(category),
            required_biomarkers=[],  # Will be populated based on category
            required_lifestyle_factors=["diet_level", "exercise_minutes_per_week", "sleep_hours", "stress_level"],
            output_format={
                "type": "json",
                "structure": "insights_array",
                "required_fields": ["id", "category", "summary", "evidence", "confidence", "severity", "recommendations"]
            },
            version="1.0",
            is_active=True
        )
        templates.append(template)
    
    return templates
